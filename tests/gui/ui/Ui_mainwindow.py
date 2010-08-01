# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Sun Aug  1 21:08:00 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.criterions = QtGui.QWidget()
        self.criterions.setObjectName("criterions")
        self.gridLayout = QtGui.QGridLayout(self.criterions)
        self.gridLayout.setObjectName("gridLayout")
        self.table_crit = QtGui.QTableWidget(self.criterions)
        self.table_crit.setDragEnabled(False)
        self.table_crit.setAlternatingRowColors(False)
        self.table_crit.setShowGrid(False)
        self.table_crit.setCornerButtonEnabled(False)
        self.table_crit.setRowCount(0)
        self.table_crit.setObjectName("table_crit")
        self.table_crit.setColumnCount(2)
        self.table_crit.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_crit.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_crit.setHorizontalHeaderItem(1, item)
        self.table_crit.horizontalHeader().setVisible(True)
        self.table_crit.horizontalHeader().setDefaultSectionSize(100)
        self.table_crit.horizontalHeader().setHighlightSections(False)
        self.table_crit.verticalHeader().setVisible(False)
        self.table_crit.verticalHeader().setHighlightSections(False)
        self.table_crit.verticalHeader().setSortIndicatorShown(False)
        self.gridLayout.addWidget(self.table_crit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.criterions, "")
        self.profiles = QtGui.QWidget()
        self.profiles.setObjectName("profiles")
        self.tabWidget.addTab(self.profiles, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Criteria", None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Weight", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.criterions), QtGui.QApplication.translate("MainWindow", "Criterions", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.profiles), QtGui.QApplication.translate("MainWindow", "Profiles", None, QtGui.QApplication.UnicodeUTF8))

