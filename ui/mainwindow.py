#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui

from Ui_mainwindow import Ui_MainWindow
from qgis_utils import *
from utils import *
from etri import *

COL_CRITERIONS = 2
COL_DIRECTION = 1

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.table_crit.setColumnWidth(0, 235)
        self.table_crit.setColumnWidth(1, 60)
        self.table_crit.setColumnWidth(2, 50)

        self.criterions_activated = []
        self.ncriterions = 0
        self.load_data()

        self.table_prof.resizeColumnsToContents()
        self.table_indiff.resizeColumnsToContents()
        self.table_pref.resizeColumnsToContents()
        self.table_veto.resizeColumnsToContents()

    def load_data(self):
        self.crit_layer = layer_load("/home/oso/tfe/qgis_data/tessin.shp", "criterions")
        criterions = layer_get_criterions(self.crit_layer)
        self.add_criterions(criterions)

        minmax = layer_get_minmax(self.crit_layer)
        self.crit_min = minmax[0]
        self.crit_max = minmax[1]

        self.actions = layer_get_values(self.crit_layer)

        self.add_profile(0)

    def check_row_float(self, row):
        for i in row:
            round(float(i), 2)

    def get_row(self, table, index):
        ncols = table.columnCount()
        values = []
        for j in range(ncols):
            item = table.item(index, j)
            values.append(round(float(item.text()), 2))
        return values

    def get_row_as_str(self, table, index):
        ncols = table.columnCount()
        values = []
        for j in range(ncols):
            item = table.item(index, j)
            values.append(str(item.text()))
        return values

    def set_row(self, table, index, vector):
        for j in range(len(vector)):
            item = QtGui.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            item.setText(str(round(float(vector[j]),2)))
            table.setItem(index, j, item)

    def add_profile(self, index):
        nprof = self.table_prof.rowCount()
        if index > nprof or index == -1:
            index = nprof

        # Profiles table
        self.table_prof.insertRow(index)

        if nprof == 0:
            abs = v_add(self.crit_max, self.crit_min)
            val = [x/2 for x in abs]
        else:
            val = self.get_row_as_str(self.table_prof, index-1)

        self.set_row(self.table_prof, index, val)

        # Thresholds table
        self.table_pref.insertRow(nprof)
        self.table_indiff.insertRow(nprof)
        self.table_veto.insertRow(nprof)
        for table in [self.table_pref, self.table_indiff]:
            try:
                thresholds = self.get_row_as_str(table, index-1)
            except:
                thresholds = [0] * table.columnCount()
            self.set_row(table, index, thresholds)

        try:
            thresholds = self.get_row_as_str(table, index-1)
        except:
            thresholds = v_substract(self.crit_max, self.crit_min) 
        self.set_row(self.table_veto, index, thresholds)

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
        comboBox.addItem("Max")
        comboBox.addItem("Min")
        self.table_crit.setCellWidget(nrow, 1, comboBox)

        # Add column in profiles and thresholds table
        for table in [ self.table_prof, self.table_pref, self.table_indiff, self.table_veto ]:
            table.insertColumn(nrow)
            item = QtGui.QTableWidgetItem()
            table.setHorizontalHeaderItem(nrow, item)
            table.horizontalHeaderItem(nrow).setText(crit)

        self.ncriterions += 1
        self.criterions_activated.append(nrow)
        self.criterions_activated.sort()

    def add_criterions(self, criterions):
        for crit in criterions:
            self.add_criteria(crit)

    def get_criterions_weights(self):
        W = []
        for i in self.criterions_activated:
            w = self.table_crit.item(i,2) 
            W.append(round(float(w.text()), 2))

        return W

    def get_criterions_directions(self):
        nrows = self.table_crit.rowCount()

        directions = []
        for row in range(nrows):
            item = self.table_crit.cellWidget(row, COL_DIRECTION)
            index = item.currentIndex()
            if index == 0:
                directions.append(1)
            else:
                directions.append(-1)

        return directions

    def get_criterions_values(self, tablew):
        nrows = tablew.rowCount()
        ncols = tablew.columnCount()

        table_values = []
        for row in range(nrows):
            row_values = []
            for col in self.criterions_activated:
                item = tablew.item(row, col)
                row_values.append(round(float(item.text()), 2))
            table_values.append(row_values)

        return table_values

    def get_indiff_thresholds(self):
        return self.get_criterions_values(self.table_indiff)

    def get_pref_thresholds(self):
        return self.get_criterions_values(self.table_pref)

    def get_veto_thresholds(self):
        return self.get_criterions_values(self.table_veto)

    def get_profiles(self):
        nrows = self.table_prof.rowCount()
        ncols = self.table_prof.columnCount()

        profiles = []
        for row in range(nrows):
            r = self.get_row(self.table_prof, row) 
            q = self.get_row(self.table_indiff, row)
            p = self.get_row(self.table_pref, row)
            v = self.get_row(self.table_veto, row)
            profile = { 'refs':r, 'q': q, 'p': p, 'v': v }
            profiles.append(profile)

        return profiles

    def check_is_float(self, table, row, column):
        item = table.item(row, column)
        val = item.text()
        try:
            round(float(val), 2)
        except:
            item.setBackgroundColor(QtCore.Qt.red)
            return

        item.setBackgroundColor(QtCore.Qt.white)

    def check_profile_crit(self, row, column):
        item = self.table_prof.item(row, column)
        val = item.text()
        try:
            val = round(float(val), 2)
        except:
            item.setBackgroundColor(QtCore.Qt.red)
            return

        if val < self.crit_min[column] or val > self.crit_max[column]:
            item.setBackgroundColor(QtCore.Qt.red)
            return

        try:
            profile = self.get_row(self.table_prof, row-1)
            if profile[column] > val and profile[column] > self.crit_min[column] and profile[column] < self.crit_max[column]:
                item.setBackgroundColor(QtCore.Qt.red)
                return
            else:
                item2 = self.table_prof.item(row-1, column)
                item2.setBackgroundColor(QtCore.Qt.white)
        except:
            pass

        try:
            profile = self.get_row(self.table_prof, row+1)
            if profile[column] < val and profile[column] > self.crit_min[column] and profile[column] < self.crit_max[column]:
                item.setBackgroundColor(QtCore.Qt.red)
                return
            else:
                item2 = self.table_prof.item(row+1, column)
                item2.setBackgroundColor(QtCore.Qt.white)
        except:
            pass

        item.setBackgroundColor(QtCore.Qt.white)

    def goto_next_cell(self, table, c_row, c_col):
        nrows = table.rowCount()
        if c_row == nrows-1:
            table.setCurrentCell(0, c_col+1)
        else:
            table.setCurrentCell(c_row+1,c_col)

    def on_table_crit_cellChanged(self, row, column):
        if column == COL_CRITERIONS:
            self.check_is_float(self.table_crit, row, column)

        self.table_crit.setCurrentCell(row+1,column)

    def on_criteria_stateChanged(self, row):
        item = self.table_crit.cellWidget(row, 0)
        if item.isChecked() == False:
            self.table_prof.setColumnHidden(row, 1)
            self.table_indiff.setColumnHidden(row, 1)
            self.table_pref.setColumnHidden(row, 1)
            self.table_veto.setColumnHidden(row, 1)
            self.criterions_activated.append(row)
            self.criterions_activated.sort()
        else:
            self.table_prof.setColumnHidden(row, 0)
            self.table_indiff.setColumnHidden(row, 0)
            self.table_pref.setColumnHidden(row, 0)
            self.table_veto.setColumnHidden(row, 0)
            self.criterions_activated.remove(row)

    def on_Badd_profile_pressed(self):
        self.add_profile(-1)

    def on_table_prof_cellChanged(self, row, column):
        self.check_profile_crit(row, column)
        self.goto_next_cell(self.table_prof, row, column)

    def on_table_indiff_cellChanged(self, row, column):
        self.check_is_float(self.table_indiff, row, column)
        self.goto_next_cell(self.table_indiff, row, column)

    def on_table_pref_cellChanged(self, row, column):
        self.check_is_float(self.table_pref, row, column)
        self.goto_next_cell(self.table_pref, row, column)

    def on_table_veto_cellChanged(self, row, column):
        self.check_is_float(self.table_veto, row, column)
        self.goto_next_cell(self.table_veto, row, column)

    def on_Bgenerate_pressed(self):
        print "Generate Decision Map"
        weights = self.get_criterions_weights()
        print "Weights:", weights
        profiles = self.get_profiles()
        print "Profiles:", profiles

        directions = self.get_criterions_directions()
        actions = []
        for a in self.actions:
            action = []
            for j in self.criterions_activated:
                value = a[j]*directions[j]
                action.append(value)
            actions.append(action)
        print "Actions:", actions

        etri = electre_tri(actions, profiles, weights, 0.75)
        print "ELECTRE TRI - Pessimist:", etri.pessimist()
