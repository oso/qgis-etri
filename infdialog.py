from PyQt4 import QtCore, QtGui
from ui.infdialog import Ui_InferenceDialog
from qgis_utils import *

class InferenceDialog(QtGui.QDialog, Ui_InferenceDialog):

    def __init__(self, parent, on_accept):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.on_accept = on_accept

    def set_xmcda_text(self, text):
        self.textb_xmcda.append(text)

    def set_weights(self, criterion_names, weights):
        criteria = criterion_names.keys()
        criteria.sort()
        self.table_weights.insertRow(0)
        for i, criterion in enumerate(criteria):
            self.table_weights.insertColumn(i)
            item = QtGui.QTableWidgetItem()
            self.table_weights.setHorizontalHeaderItem(i, item)
            self.table_weights.horizontalHeaderItem(i).setText(criterion_names[criterion])
            item = QtGui.QTableWidgetItem()
            item.setText(str(weights[criterion]))
            self.table_weights.setItem(0, i, item)

    def set_profiles(self, criterion_names, profiles):
        criteria = criterion_names.keys()
        criteria.sort()
        self.table_prof.setRowCount(len(profiles))
        for i, criterion in enumerate(criteria):
            self.table_prof.insertColumn(i)
            item = QtGui.QTableWidgetItem()
            self.table_prof.setHorizontalHeaderItem(i, item)
            self.table_prof.horizontalHeaderItem(i).setText(criterion_names[criterion])
            for j in range(len(profiles)):
                item = QtGui.QTableWidgetItem()
                item.setText(str(profiles["b%d" % (j+1)][criterion]))
                self.table_prof.setItem(j, i, item)

    def accept(self):
        self.on_accept()
        QDialog.accept(self)
