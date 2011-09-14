#!/usr/bin/python

import sys
sys.path.append("..")
from etri import electre_tri
from graphic import graph_etri
from PyQt4 import QtCore
from PyQt4 import QtGui
from data_loulouka import *

if __name__ == "__main__":
    etri = electre_tri(a, profiles, w, lbda)

    app = QtGui.QApplication(sys.argv)
    view = QtGui.QGraphicsView()
    view.setRenderHint(QtGui.QPainter.Antialiasing)
    layout = QtGui.QVBoxLayout()
    layout.addWidget(view)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    graph = graph_etri(etri, view.size())
    view.setScene(graph)
    dialog.show()
    app.exec_()
