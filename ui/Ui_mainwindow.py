# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Tue Aug  3 21:24:10 2010
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
        self.gridLayout_6 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.params = QtGui.QGroupBox(self.centralwidget)
        self.params.setObjectName("params")
        self.gridLayout = QtGui.QGridLayout(self.params)
        self.gridLayout.setObjectName("gridLayout")
        self.params_tab = QtGui.QTabWidget(self.params)
        self.params_tab.setObjectName("params_tab")
        self.Criterions = QtGui.QWidget()
        self.Criterions.setObjectName("Criterions")
        self.gridLayout_2 = QtGui.QGridLayout(self.Criterions)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table_crit = QtGui.QTableWidget(self.Criterions)
        self.table_crit.setDragEnabled(False)
        self.table_crit.setAlternatingRowColors(False)
        self.table_crit.setShowGrid(False)
        self.table_crit.setCornerButtonEnabled(False)
        self.table_crit.setRowCount(0)
        self.table_crit.setObjectName("table_crit")
        self.table_crit.setColumnCount(3)
        self.table_crit.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_crit.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_crit.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_crit.setHorizontalHeaderItem(2, item)
        self.table_crit.horizontalHeader().setVisible(True)
        self.table_crit.horizontalHeader().setDefaultSectionSize(100)
        self.table_crit.horizontalHeader().setHighlightSections(False)
        self.table_crit.verticalHeader().setVisible(False)
        self.table_crit.verticalHeader().setHighlightSections(False)
        self.table_crit.verticalHeader().setSortIndicatorShown(False)
        self.gridLayout_2.addWidget(self.table_crit, 0, 0, 1, 1)
        self.params_tab.addTab(self.Criterions, "")
        self.Profiles = QtGui.QWidget()
        self.Profiles.setObjectName("Profiles")
        self.gridLayout_5 = QtGui.QGridLayout(self.Profiles)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.table_prof = QtGui.QTableWidget(self.Profiles)
        self.table_prof.setObjectName("table_prof")
        self.table_prof.setColumnCount(0)
        self.table_prof.setRowCount(0)
        self.gridLayout_5.addWidget(self.table_prof, 0, 0, 1, 1)
        self.table_thres = QtGui.QTableWidget(self.Profiles)
        self.table_thres.setObjectName("table_thres")
        self.table_thres.setColumnCount(3)
        self.table_thres.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_thres.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_thres.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_thres.setHorizontalHeaderItem(2, item)
        self.gridLayout_5.addWidget(self.table_thres, 1, 0, 1, 1)
        self.params_tab.addTab(self.Profiles, "")
        self.gridLayout.addWidget(self.params_tab, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.params, 0, 1, 1, 1)
        self.options = QtGui.QGroupBox(self.centralwidget)
        self.options.setMaximumSize(QtCore.QSize(388, 16777215))
        self.options.setObjectName("options")
        self.formLayout = QtGui.QFormLayout(self.options)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.Badd_profile = QtGui.QCommandLinkButton(self.options)
        self.Badd_profile.setObjectName("Badd_profile")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.Badd_profile)
        self.Bdel_profile = QtGui.QCommandLinkButton(self.options)
        self.Bdel_profile.setObjectName("Bdel_profile")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.Bdel_profile)
        self.gridLayout_6.addWidget(self.options, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.params_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.params.setTitle(QtGui.QApplication.translate("MainWindow", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Criteria", None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Weight", None, QtGui.QApplication.UnicodeUTF8))
        self.params_tab.setTabText(self.params_tab.indexOf(self.Criterions), QtGui.QApplication.translate("MainWindow", "Criterions", None, QtGui.QApplication.UnicodeUTF8))
        self.table_thres.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Q (Indifference)", None, QtGui.QApplication.UnicodeUTF8))
        self.table_thres.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "P (Preference)", None, QtGui.QApplication.UnicodeUTF8))
        self.table_thres.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "V (Veto)", None, QtGui.QApplication.UnicodeUTF8))
        self.params_tab.setTabText(self.params_tab.indexOf(self.Profiles), QtGui.QApplication.translate("MainWindow", "Profiles", None, QtGui.QApplication.UnicodeUTF8))
        self.options.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.Badd_profile.setText(QtGui.QApplication.translate("MainWindow", "Add Profile", None, QtGui.QApplication.UnicodeUTF8))
        self.Bdel_profile.setText(QtGui.QApplication.translate("MainWindow", "Del Profile", None, QtGui.QApplication.UnicodeUTF8))

