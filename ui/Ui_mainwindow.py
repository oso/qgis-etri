# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Jul 27 20:53:10 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(796, 606)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.map = QtGui.QWidget()
        self.map.setObjectName("map")
        self.gridLayout_2 = QtGui.QGridLayout(self.map)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.map_frame = QtGui.QFrame(self.map)
        self.map_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.map_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.map_frame.setObjectName("map_frame")
        self.gridLayout_2.addWidget(self.map_frame, 0, 0, 1, 1)
        self.tabWidget.addTab(self.map, "")
        self.criterions = QtGui.QWidget()
        self.criterions.setObjectName("criterions")
        self.tabWidget.addTab(self.criterions, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
	self.mpActionAddLayer = QtGui.QAction(MainWindow)
#        self.mpActionAddLayer.setIcon(QtGui.QIcon(":/mActionAddLayer.png"))
        self.mpActionAddLayer.setObjectName("mpActionAddLayer")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.map), QtGui.QApplication.translate("MainWindow", "Criterions Map", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.criterions), QtGui.QApplication.translate("MainWindow", "Criterions", None, QtGui.QApplication.UnicodeUTF8))

