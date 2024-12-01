import os, sys
import colorsys
from itertools import combinations
from qgis.PyQt import QtCore
from qgis.PyQt.QtGui import QBrush, QColor, QFont, QPen
from qgis.PyQt.QtWidgets import QGraphicsPathItem, QGraphicsScene, QGraphicsTextItem, QGraphicsView


class _MyGraphicsview(QGraphicsView):

    def __init__(self, parent=None):
        super(QGraphicsView, self).__init__(parent)

    def resizeEvent(self, event):
        scene = self.scene()
        if scene is None:
            return

        scene.update(self.size())
        self.resetCachedContent()


class QGraphicsSceneEtri(QGraphicsScene):

    def __init__(self, model, worst, best, size, criteria_order=None,
                 parent=None):
        super(QGraphicsSceneEtri, self).__init__(parent)
        self.model = model
        if criteria_order:
            self.criteria_order = criteria_order
        else:
            self.criteria_order = list(self.model.criteria.keys())
            self.criteria_order.sort()
        self.worst = worst
        self.best = best

        self.ap_items = {}

        self.update(size)

    def update(self, size):
        self.size = size
        self.axis_height = self.size.height() - 60
        self.ymax = -self.axis_height + 25 / 2
        self.ymin = -25 / 2

        self.hspacing = size.width()/len(self.model.criteria)
        if self.hspacing < 100:
            self.hspacing = 100

        self.clear()
        self.__plot_axis()
        self.__plot_profiles()
        self.__plot_categories()
        self.__higlight_intersections()
        self.__plot_alternatives()
        self.setSceneRect(self.itemsBoundingRect())

    def __create_axis(self, xmin, xmax, ymin, ymax, direction):
        item = QGraphicsPathItem()

        path = item.path()
        path.moveTo(xmin, ymin)
        path.lineTo(xmax, ymax)

        if direction == -1:
            x = xmin
            y = ymin
        else:
            x = xmax
            y = ymax

        path.moveTo(x, y)
        path.lineTo(x - 3, y + direction * 6)
        path.lineTo(x + 3, y + direction * 6)
        path.closeSubpath()

        pen = QPen()
        pen.setWidth(2)
        item.setPen(pen)

        brush = QBrush(QColor("black"))
        item.setBrush(brush)

        item.setPath(path)

        return item

    def __plot_axis(self):
        self.axis_text_items = {}
        self.axis_items = {}

        criteria = [c for c in self.criteria_order
                    if self.model.criteria[c].disabled is False]
        for i, id in enumerate(criteria):
            criterion = self.model.criteria[id]
            x = i * self.hspacing

            axis = self.__create_axis(x, x, 0, -self.axis_height,
                                      criterion.direction)
            axis.setZValue(1)
            self.addItem(axis)
            self.axis_items[id] = axis

            if criterion.name:
                txt = "%s\n(%g)" % (criterion.name, self.model.cv[id].value)
            else:
                txt = "%s (%g)" % (criterion.id, self.model.cv[id].value)

            text = QGraphicsTextItem()
            text.setHtml("<div align=\"center\">%s</div>" % txt)
            text.setTextWidth(text.boundingRect().width())
            font = QFont()
            font.setBold(True)
            text.setFont(font)
            text.setZValue(1)
            text.setPos(x - text.boundingRect().width() / 2, 0)
            self.addItem(text)

            self.axis_text_items[criterion] = text

    def __compute_y(self, ap, id):
        direction = self.model.criteria[id].direction
        if id in ap.performances:
            p = ap.performances[id] * direction
        else:
            p = None

        best = self.best.performances[id] * direction
        worst = self.worst.performances[id] * direction
        if p is None or p > best:
            p = best
        elif p < worst:
            p = worst

        num = p - worst
        den = best - worst

        if num == 0 or den == 0:
            return self.ymin

        return self.ymin + num / den * (self.ymax - self.ymin)

    def __create_text_value(self, value):
        item = QGraphicsTextItem()

        item.setPlainText(value)

        font = QFont()
        font.setBold(True)
        font.setPointSize(6)
        item.setFont(font)
        item.setZValue(1)

        return item

    def __create_profile(self, ap, print_values = False,
                         color = QColor("red")):
        item = QGraphicsPathItem()

        pen = QPen()
        pen.setBrush(color)
        item.setPen(pen)

        text_items = []

        path = item.path()
        criteria = [c for c in self.criteria_order
                    if self.model.criteria[c].disabled is False]
        for i, cid in enumerate(criteria):
            y = self.__compute_y(ap, cid)

            if i == 0:
                x = 0
                path.moveTo(0, y)
            else:
                x += self.hspacing
                path.lineTo(x, y)

            if print_values is True and cid in ap.performances:
                txt = "%g" % ap.performances[cid]
                txtitem = self.__create_text_value(txt)
                txtitem.setPos(x, y)
                text_items.append(txtitem)

        item.setPath(path)

        return item, text_items

    def __plot_profiles(self):
        self.profiles_items = {}
        self.profiles_text_items = {}

        bpt = self.model.bpt
        for profile in self.model.profiles:
            item, text_items = self.__create_profile(bpt[profile], True)
            self.addItem(item)
            self.profiles_items[profile] = item
            self.profiles_text_items[profile] = text_items
            for txtitem in text_items:
                self.addItem(txtitem)

        for profile in [self.worst, self.best]:
            item, text_items = self.__create_profile(profile)
            self.addItem(item)
            self.profiles_items[profile.id] = item
            self.profiles_text_items[profile.id] = text_items
            for txtitem in text_items:
                self.addItem(txtitem)

    def __get_category_color(self, i):
        n = len(self.model.categories)
        g = int(255 - 220 * (n - i) / n)
        return QColor(0, g, 0)

    def __create_category(self, i, path_below, path_above):
        item = QGraphicsPathItem()

        path = item.path()
        path.addPath(path_above)
        path.connectPath(path_below.toReversed())
        path.closeSubpath()

        color = self.__get_category_color(i)
        item.setBrush(color)

        item.setPath(path)

        return item

    def __plot_categories(self):
        self.category_items = {}
        for i, category in enumerate(self.model.categories):
            if i == 0:
                lower = self.profiles_items['worst']
            else:
                lower = self.profiles_items[self.model.profiles[i - 1]]
            if i == len(self.model.profiles):
                lower = self.profiles_items['best']
            else:
                upper = self.profiles_items[self.model.profiles[i]]

            item = self.__create_category(i, lower.path(), upper.path())
            self.addItem(item)

            self.category_items[category] = item

    def __clear_intersections(self):
        for item in self.intersection_items:
            self.removeItem(item)
        self.intersection_items = []

    def __higlight_intersections(self):
        self.intersection_items = []
        combis = list(combinations(self.category_items.values(), r=2))
        for combi in combis:
            a = combi[0].path()
            b = combi[1].path()
            c = a.intersected(b)

            item = QGraphicsPathItem(c)
            brush = QBrush(QColor("yellow"))
            item.setBrush(brush)
            self.addItem(item)

            self.intersection_items.append(item)

    def update_intersections(self):
        self.__clear_intersections()
        self.__higlight_intersections()

    def __plot_alternatives(self):
        for ap, item in self.ap_items.items():
            item, text_items = self.__create_profile(ap)
            self.addItem(item)

    def __update_category(self, i, cat, ap_below, ap_above):
        item = self.category_items[cat]
        path = item.path()

        criteria = [c for c in self.criteria_order
                    if self.model.criteria[c].disabled is False]
        for i, cid in enumerate(criteria):
            y_above = self.__compute_y(ap_above, cid)
            y_below = self.__compute_y(ap_below, cid)

            i2 = 2 * len(criteria) - 1 - i
            if i == 0:
                x = 0
            else:
                x += self.hspacing

            path.setElementPositionAt(i, x, y_above)
            path.setElementPositionAt(i2, x, y_below)

        item.setPath(path)

    def update_categories(self):
        ncat = len(self.model.categories)
        for i, cat in enumerate(self.model.categories):
            if i == 0:
                ap_below = self.worst
            else:
                ap_below = self.model.bpt[self.model.profiles[i - 1]]

            if i == ncat - 1:
                ap_above = self.best
            else:
                ap_above = self.model.bpt[self.model.profiles[i]]

            self.__update_category(i, cat, ap_below, ap_above)

        self.update_intersections()

    def update_profile(self, profile):
        item = self.profiles_items[profile]
        text_items = self.profiles_text_items[profile]
        if profile == 'worst':
            ap = self.worst
        elif profile == 'best':
            ap = self.best
        else:
            ap = self.model.bpt[profile]

        path = item.path()

        criteria = [c for c in self.criteria_order
                    if self.model.criteria[c].disabled is False]
        for i, cid in enumerate(criteria):
            y = self.__compute_y(ap, cid)

            if i == 0:
                x = 0
            else:
                x += self.hspacing

            path.setElementPositionAt(i, x, y)

            if len(text_items) > 0:
                txtitem = text_items[i]
                txtitem.setPos(x, y)
                txtitem.setPlainText("%g" % ap.performances[cid])

        item.setPath(path)

    def update_profiles(self):
        for profile in self.profiles_items.keys():
            self.update_profile(profile)

    def plot_alternative_performances(self, ap):
        item, text_items = self.__create_profile(ap)
        self.addItem(item)

        self.ap_items[ap] = item
