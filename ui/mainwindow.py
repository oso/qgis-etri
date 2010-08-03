#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

from Ui_mainwindow import Ui_MainWindow
from qgis_utils import *
from utils import *

COL_CRITERIONS = 2

#criterions = [ "Densite_POP", "Tx chomage", "PIB" ]
weights = [ 10, 20, 30]

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.table_crit.setColumnWidth(0, 235)
        self.table_crit.setColumnWidth(1, 60)
        self.table_crit.setColumnWidth(2, 50)
        self.table_prof.setColumnWidth(0, 50)
        self.table_prof.setColumnWidth(1, 50)
        self.table_prof.setColumnWidth(2, 50)

        self.table_thres.setColumnWidth(0, 170)
        self.table_thres.setColumnWidth(1, 170)
        self.table_thres.setColumnWidth(2, 170)

        self.load_data()

    def load_data(self):
        self.crit_layer = layer_load("/home/oso/tfe/qgis_data/france.shp", "criterions")
        criterions = layer_get_criterions(self.crit_layer)
        self.add_criterions(criterions)

        minmax = layer_get_minmax(self.crit_layer)
        self.crit_min = minmax[0]
        self.crit_max = minmax[1]

        self.add_profile(0)

    def get_profile(self, n):
        ncrit = self.table_prof.columnCount()
        pvalues = []
        for j in range(crit):
            item = self.table_crit.item(n,j) 
            pvalues.append(round(float(item.text()), 2))

        return pvalues

    def add_profile(self, index):
        nprof = self.table_prof.rowCount()
        if index > nprof:
            index = nprof

        # Profiles table
        self.table_prof.insertRow(index)

        if index == 0:
            min = self.crit_min
        else:
            min = get_profile(index-1)

        if index == nprof:
            max = self.crit_max
        else:
            max = get_profile(index+1)

        abs = v_substract(max, min)
        mean = [x/2 for x in abs]

        for j in range(len(mean)):
            item = QtGui.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            item.setText(str(round(mean[j],2)))
            self.table_prof.setItem(index, j, item)

        # Thresholds table
        self.table_thres.insertRow(nprof)

    def add_criteria(self, crit):
        # Add row in criteria table
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
        item.setText("10.0")
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

        # Add column in profiles table
        self.table_prof.insertColumn(nrow)
        item = QtGui.QTableWidgetItem()
        self.table_prof.setHorizontalHeaderItem(nrow, item)
        self.table_prof.horizontalHeaderItem(nrow).setText(crit)

    def add_criterions(self, criterions):
        for crit in criterions:
            self.add_criteria(crit)

    def check_criteria_weight(self, item):
        val = item.text()
        try:
            round(float(val), 2)
            item.setBackgroundColor(QtCore.Qt.white)
        except:
            item.setBackgroundColor(QtCore.Qt.red)

    def on_table_crit_cellChanged(self, row, column):
        print "ceil changed: row",  row,  "column",  column

        if column == COL_CRITERIONS:
            item = self.table_crit.item(row, column)
            self.check_criteria_weight(item)

        self.table_crit.setCurrentCell(row+1,column)

    def on_criteria_stateChanged(self, row):
        print "Row", row
        item = self.table_crit.cellWidget(row, 0)
        print "Checked:", item.isChecked()

    def get_criterions_weights(self):
        nrows = self.table_crit.rowCount()
        W = []
        for i in range(nrows):
            w = self.table_crit.item(i,2) 
            W.append(round(float(w.text()), 2))

        return W
