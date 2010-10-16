from PyQt4 import QtCore, QtGui
from Ui_refsdialog import Ui_RefsDialog
from qgis_utils import *

class RefsDialog(QtGui.QDialog, Ui_RefsDialog):

    def __init__(self, parent, layer):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.table_refs.setColumnWidth(0, 30)
        self.setWindowFlags(QtCore.Qt.Window)

        self.layer = layer 
        self.row_ids = {}
        self.refs_actions = []
        self.load_attributes()

    def load_attributes(self):
        provider = self.layer.dataProvider()
        fields = provider.fields()

        # Add columns
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
            item = QtGui.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsTristate)
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.table_refs.setItem(j, 0, item)

            checkBox = QtGui.QCheckBox(self)
            checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.table_refs.setCellWidget(j, 0, checkBox)

            signalMapper = QtCore.QSignalMapper(self)
            QtCore.QObject.connect(checkBox, QtCore.SIGNAL("stateChanged(int)"), signalMapper, QtCore.SLOT("map()"))
            signalMapper.setMapping(checkBox, j)
            QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped(int)"), self.on_astate_changed)

            self.row_ids[j] = feat.id()

            for (i, attr) in attrMap.iteritems():
                item = QtGui.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                item.setText(attr.toString().trimmed())
                self.table_refs.setItem(j, i+1, item)

            j += 1

    def on_astate_changed(self, row):
        item = self.table_refs.cellWidget(row, 0)
        if item.isChecked() == False:
            self.refs_actions.remove(self.row_ids[row])
        else:
            self.refs_actions.append(self.row_ids[row])    

    def accept(self):
        print self.refs_actions

        QDialog.accept(self)
