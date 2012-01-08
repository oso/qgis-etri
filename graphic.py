from PyQt4 import QtCore
from PyQt4 import QtGui
from etri import electre_tri
import colorsys

class axis(QtGui.QGraphicsItem):

    def __init__(self, x1, y1, x2, y2, direction, parent=None):
        super(QtGui.QGraphicsItem, self).__init__(parent)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.path = QtGui.QPainterPath()
        self.path.moveTo(x1, y1)
        self.path.lineTo(x2, y2)
        self.__set_arrow(direction)

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter, option, widget=None):
        pen = QtGui.QPen()
        pen.setWidth(2)
        brush = QtGui.QBrush(QtGui.QColor("black"))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPath(self.path)

    def __set_arrow(self, direction):
        if direction == -1:
            x = self.x1
            y = self.y1
        else:
            x = self.x2
            y = self.y2

        self.path.moveTo(x, y)
        self.path.lineTo(x-3, y+direction*6)
        self.path.lineTo(x+3, y+direction*6)
        self.path.closeSubpath()


class graph_etri(QtGui.QGraphicsScene):

    def __init__(self, model, size, criteria_name=None, parent=None):
        super(QtGui.QGraphicsScene, self).__init__(parent)
        self.model = model
        self.criteria_name = None
        self.update(size)

    def update(self, size):
        self.size = size
        self.axis_height = self.size.height()-45
        self.model_height = self.axis_height-25

        self.hspacing = size.width()/len(self.model.criteria)
        if self.hspacing < 100:
            self.hspacing = 100

        self.clear()
        self.__plot_axis()
        self.__plot_profiles()
        self.update_criteria_name(self.criteria_name)
        self.setSceneRect(self.itemsBoundingRect())

    def update_criteria_name(self, criteria_name):
        if criteria_name == None:
            return

        self.criteria_name = criteria_name

        for criterion, text in self.criteria_text.iteritems():
            if criteria_name.has_key(criterion) == False:
                return

            oldwidth = text.boundingRect().width()
            text.setPlainText(criteria_name[criterion])
            newwidth = text.boundingRect().width()
            diffwidth = newwidth-oldwidth
            text.moveBy(-diffwidth/2, 0)

        self.setSceneRect(self.itemsBoundingRect())

    def __plot_axis(self):
        directions = self.model.directions
        self.criteria_text = {}

        for i, criterion in enumerate(self.model.criteria):
            x = i*self.hspacing

            line = axis(x, 0, x, -self.axis_height, directions[criterion])
            line.setZValue(1)
            self.addItem(line)

            text = self.addText(criterion)
            font = QtGui.QFont()
            font.setBold(True)
            text.setFont(font)
            text.setZValue(1)
            text.setPos(x-text.boundingRect().width()/2, 0)

            self.criteria_text[criterion] = text

    def __d_substract(self, a, b):
        return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

    def __profile_get_points(self, profile):
        minima = self.model.model_min
        maxima = self.model.model_max
        diff = self.__d_substract(maxima, minima) 

        axis_unused = self.axis_height-self.model_height
        limsup = -self.axis_height+axis_unused/2
        liminf = -axis_unused/2

        n = len(self.model.criteria)
        points = []
        for i, criterion in enumerate(self.model.criteria):
            x = i*self.hspacing

            num = profile[criterion]-minima[criterion]
            den = diff[criterion] 
            if den == 0:
                p = QtCore.QPointF(x, liminf)
            elif num == 0:
                p = QtCore.QPointF(x, liminf)
            else:
                y = liminf+(limsup-liminf)*num/den
                p = QtCore.QPointF(x, y)

            text = self.addText("%g" % profile[criterion])
            font = QtGui.QFont()
            font.setBold(True)
            font.setPointSize(6)
            text.setFont(font)
            text.setPos(p)
            if i == n-1:
                text.moveBy(-text.boundingRect().width(), 0)
            text.setZValue(1)

            points.append(p)

        return points

    def __get_category_brush(self, category):
        ncategories = len(self.model.profiles)+1
        color = QtGui.QColor(0, 255-220*(ncategories-category)/(ncategories), 0)
        return QtGui.QBrush(QtGui.QColor(color))

    def __plot_profiles(self):
        profiles = self.model.profiles
        minima = self.model.model_min
        maxima = self.model.model_max

        polygon_list = []
        below = self.__profile_get_points(minima)
        for i, profile in enumerate(profiles):
            below.reverse()
            above = self.__profile_get_points(profile['refs'])
            ppoints = below + above
            polygon = QtGui.QPolygonF(ppoints)
            polygon_list.append(polygon)
            brush = self.__get_category_brush(i)
            self.addPolygon(polygon, QtGui.QPen(), brush)
            below = above[:]

        i = len(profiles)-1
        above = self.__profile_get_points(maxima)
        below.reverse()
        ppoints = below + above
        polygon = QtGui.QPolygonF(ppoints)
        polygon_list.append(polygon)
        brush = self.__get_category_brush(i+1)
        self.addPolygon(polygon, QtGui.QPen(), brush)

        for i, p in enumerate(polygon_list):
            for j, q in enumerate(polygon_list):
                if j >= i:
                    continue

                u = p.intersected(q)
                if u == None:
                    continue

                brush = QtGui.QBrush()
                brush.setColor(QtGui.QColor("yellow"))
                brush.setStyle(QtCore.Qt.SolidPattern)
                self.addPolygon(u, QtGui.QPen(), brush)
