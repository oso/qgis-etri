#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

from Ui_mainwindow import Ui_MainWindow

criterions = [ "Densite_POP", "Tx chomage", "PIB" ]
weights = [ 10, 20, 30]

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.table_crit.setColumnWidth(0, 200)
        self.table_crit.setColumnWidth(1, 60)
        self.table_crit.setColumnWidth(2, 50)
        self.table_prof.setColumnWidth(0, 50)
        self.table_prof.setColumnWidth(1, 50)
        self.table_prof.setColumnWidth(2, 50)
        self.add_criterions()

    def add_criteria(self, crit):
        nrow = self.table_crit.rowCount()
        self.table_crit.insertRow(nrow)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.table_crit.setItem(nrow, 0, item)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.table_crit.setItem(nrow, 1, item)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.table_crit.setItem(nrow, 2, item)
        
        checkBox = QtGui.QCheckBox(self)
        checkBox.setCheckState(QtCore.Qt.Checked)
        checkBox.setText(QtGui.QApplication.translate("MainWindow", crit, None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.setCellWidget(nrow, 0, checkBox)

        signalMapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(checkBox, QtCore.SIGNAL("stateChanged(int)"), signalMapper, QtCore.SLOT("map()"))
        signalMapper.setMapping(checkBox, nrow)
        QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped(int)"), self.on_criteria_stateChanged)

        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("Min")
        comboBox.addItem("Max")
        self.table_crit.setCellWidget(nrow, 1, comboBox)

    def add_criterions(self):
        for crit in criterions:
            self.add_criteria(crit)

    def on_table_crit_cellChanged(self, row, column):
        print "ceil changed: row",  row,  "column",  column
        self.table_crit.setCurrentCell(row+1,column)

    def on_criteria_stateChanged(self, row):
        print "Row", row
        item = self.table_crit.cellWidget(row, 0)
        print "Checked:", item.isChecked()
