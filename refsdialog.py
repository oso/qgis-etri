from PyQt4 import QtCore, QtGui
from Ui_refsdialog import Ui_RefsDialog
from qgis_utils import *

class RefsDialog(QtGui.QDialog, Ui_RefsDialog):

    def __init__(self, parent, iface, layer, refs_actions):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.table_refs.setColumnWidth(0, 30)
        self.setWindowFlags(QtCore.Qt.Window)

        self.parent = parent

        self.layer = layer 
        self.row_ids = {}
        self.refs_actions = refs_actions
        self.load_attributes()

        self.parent.hide()

    def closeEvent(self, event):
        self.hide()
        self.parent.show()

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
            if feat.id() in self.refs_actions:
                checkBox.setCheckState(QtCore.Qt.Checked)
                item = self.table_refs.item(j, 0)
                item.setBackgroundColor(QtCore.Qt.green)
                activated = True
            else:
                checkBox.setCheckState(QtCore.Qt.Unchecked)
                activated = False
            self.table_refs.setCellWidget(j, 0, checkBox)

            signalMapper = QtCore.QSignalMapper(self)
            QtCore.QObject.connect(checkBox, QtCore.SIGNAL("stateChanged(int)"), signalMapper, QtCore.SLOT("map()"))
            signalMapper.setMapping(checkBox, j)
            QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped(int)"), self.on_astate_changed)

            self.row_ids[j] = feat.id()

            for (i, attr) in attrMap.iteritems():
                item = QtGui.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                if activated == True:
                    item.setBackgroundColor(QtCore.Qt.green)
                item.setText(attr.toString().trimmed())
                self.table_refs.setItem(j, i+1, item)

            j += 1

    def set_row_background(self, row, color):
        for i in range(self.table_refs.columnCount()):
            item = self.table_refs.item(row, i)
            item.setBackgroundColor(color)
        
    def on_astate_changed(self, row):
        item = self.table_refs.cellWidget(row, 0)
        if item.isChecked() == False:
            self.refs_actions.remove(self.row_ids[row])
            self.set_row_background(row, QtCore.Qt.white)
        else:
            self.refs_actions.append(self.row_ids[row])
            self.set_row_background(row, QtCore.Qt.green)

    def accept(self):
        self.parent.set_reference_actions(self.refs_actions)
        self.layer.setSelectedFeatures(self.refs_actions)
        self.hide()
        self.parent.show()
        QDialog.accept(self)

    def reject(self):
        self.hide()
        self.parent.show()
        QDialog.reject(self)

    def on_table_refs_itemDoubleClicked(self, item):
        row = item.row()
        featids = []
        featids.append(self.row_ids[row])
        self.layer.setSelectedFeatures(featids)

    def on_cbox_hide_stateChanged(self, state):
        ncrit = len(self.parent.criteria)
        for i in range(ncrit):
            if (i not in self.parent.criteria_activated) and (state == 2):
                self.table_refs.setColumnHidden(int(i+1), 1)
            else:
                self.table_refs.setColumnHidden(int(i+1), 0)

    def on_Bdisplay_pressed(self):
        self.layer.setSelectedFeatures(self.refs_actions)

    def on_Bzoom_pressed(self):
        self.layer.setSelectedFeatures(self.refs_actions)
        mc = self.iface.mapCanvas()
        rect = self.layer.boundingBoxOfSelected()
        rect.scale(2)
        mc.setExtent(rect)
        mc.refresh()
