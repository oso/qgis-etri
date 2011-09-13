from PyQt4 import QtCore
from PyQt4 import QtGui
from etri import electre_tri
import colorsys

class graph_etri(QtGui.QGraphicsScene):

    def __init__(self, model, size, parent=None):
        super(QtGui.QGraphicsScene, self).__init__(parent)
        self.model = model
        self.size = size

        self.hspacing = 100
        self.axis_height = self.size.height()-100
        self.model_height = self.axis_height-25

        self.update()

    def update(self):
        self.__plot_axis()
        self.__plot_profiles()

    def __plot_axis(self):
        directions = self.model.directions

        for i, criterion in enumerate(self.model.criteria):
            x = i*self.hspacing

            line = self.addLine(x, 0, x, -self.axis_height)
            line.setZValue(1)

            text = self.addText(criterion)
            text.setPos(x-text.boundingRect().width()/2, 0)

    def __d_substract(self, a, b):
        return dict( (n, a.get(n, 0)-b.get(n, 0)) for n in set(a)|set(b) )

    def __profile_get_points(self, profile):
        minima = self.model.get_model_min()
        maxima = self.model.get_model_max()
        diff = self.__d_substract(maxima, minima) 

        axis_unused = self.axis_height-self.model_height
        liminf = -self.axis_height+axis_unused/2
        limsup = -axis_unused/2

        points = []
        for i, criterion in enumerate(self.model.criteria):
            x = i*self.hspacing

            num = profile[criterion]-minima[criterion]
            den = diff[criterion] 
            if den == 0:
                p = QtCore.QPointF(x, liminf)
            elif num == 0:
                p = QtCore.QPointF(x, limsup)
            else:
                p = QtCore.QPointF(x, liminf*num/den)

            text = self.addText("%s" % profile[criterion])
            text.setPos(p)
            text.moveBy(0, -text.boundingRect().height()/2)
            text.setZValue(1)
            points.append(p)

        return points

    def __get_category_brush(self, category):
        print category
        h = 1-float(category)/(len(self.model.profiles)+1)
        r, g, b = colorsys.hls_to_rgb(h, 0.5, 0.5)
        return QtGui.QBrush(QtGui.QColor(r*255, g*255, b*255))
        
    def __plot_profiles(self):
        profiles = self.model.profiles
        minima = self.model.get_model_min()
        maxima = self.model.get_model_max()

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

                self.addPolygon(u, QtGui.QPen(), QtGui.QBrush(QtGui.QColor("yellow")))
