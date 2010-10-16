from PyQt4 import QtCore, QtGui
from Ui_refsdialog import Ui_RefsDialog
from qgis_utils import *

class RefsDialog(QtGui.QDialog, Ui_RefsDialog):

    def __init__(self, parent, layer):
        QtGui.QDialog.__init__(self, parent)
        self.layer = layer 
        self.setupUi(self)
        self.load_attributes()
        self.setWindowFlags(QtCore.Qt.Window)

    def load_attributes(self):
        provider = self.layer.dataProvider()
        fields = provider.fields()

        # Add columns
        self.table_refs.insertColumn(0)
        item = QtGui.QTableWidgetItem()
        self.table_refs.setHorizontalHeaderItem(0, item)
        self.table_refs.horizontalHeaderItem(0).setText("")

        for (i, field) in fields.iteritems():
            self.table_refs.insertColumn(i+1)
            item = QtGui.QTableWidgetItem()
            self.table_refs.setHorizontalHeaderItem(i+1, item)
            self.table_refs.horizontalHeaderItem(i+1).setText(field.name().trimmed())

        # Add attributes
        allAttrs = provider.attributeIndexes()
        provider.select(allAttrs, QgsRectangle(), False)
        feat = QgsFeature()

        j = 0
        while provider.nextFeature(feat):
            attrMap = feat.attributeMap()

            self.table_refs.insertRow(j)

            for (i, attr) in attrMap.iteritems():
                item = QtGui.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                item.setText(attr.toString().trimmed())
                self.table_refs.setItem(j, i+1, item)

            j += 1
