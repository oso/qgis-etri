#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

from Ui_mainwindow import Ui_MainWindow

criterions = [ "Densite_POP", "Tx chomage", "PIB" ]

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.table_crit.setColumnWidth(0, 200)
        self.table_crit.setColumnWidth(1, 50)
        self.table_prof.setColumnWidth(0, 50)
        self.table_prof.setColumnWidth(1, 50)
        self.table_prof.setColumnWidth(2, 50)
        self.set_data()

    def set_data(self):
        for crit in criterions:
            nrow = self.table_crit.rowCount()
            
            self.table_crit.insertRow(nrow)
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsTristate)
            self.table_crit.setItem(nrow, 0, item)
            
            checkbox = QtGui.QCheckBox(self)
            checkbox.setCheckState(QtCore.Qt.Checked)
            checkbox.setText(QtGui.QApplication.translate("MainWindow", crit, None, QtGui.QApplication.UnicodeUTF8))
            self.table_crit.setCellWidget(nrow, 0, checkbox)
