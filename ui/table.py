from PyQt4 import QtCore
from PyQt4 import QtGui

INDEX_MAX=0
INDEX_MIN=1

class criteria_table(QtGui.QTableWidget):

    def __init__(self, parent=None):
        super(QtGui.QTableWidget, self).__init__(parent)
        self.parent = parent
        self.crit_row = {}

        self.setColumnCount(3)
        self.setShowGrid(False)
        self.setDragEnabled(False)
        self.__add_headers()
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSortIndicatorShown(False)
        self.horizontalHeader().setHighlightSections(False)
        self.setColumnWidth(0, 255)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 100)

    def __add_headers(self):
        item = QtGui.QTableWidgetItem()
        item.setText("Criterion")
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.setHorizontalHeaderItem(0, item)

        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)

        item = QtGui.QTableWidgetItem()
        item.setText("Weight")
        item.setTextAlignment(QtCore.Qt.AlignRight)
        self.setHorizontalHeaderItem(2, item)

    def add(self, crit_id, crit_name, enabled, weight):
        row = self.rowCount()
        self.insertRow(row)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, 0, item)
        cbox = QtGui.QCheckBox(self)
        if enabled == True:
            cbox.setCheckState(QtCore.Qt.Checked)
        cbox.setText(crit_name)
        self.__add_cbox_signal(cbox, crit_id)
        self.setCellWidget(row, 0, cbox)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, 1, item)
        combo = QtGui.QComboBox(self)
        combo.addItem("Max")
        combo.addItem("Min")
        self.__add_combo_signal(combo, crit_id)
        self.setCellWidget(row, 1, combo)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.setItem(row, 2, item)

        self.crit_row[crit_id] = row

    def __add_cbox_signal(self, cbox, crit_id):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(cbox, QtCore.SIGNAL("stateChanged(int)"),
                                smapper, QtCore.SLOT("map()"))
        smapper.setMapping(cbox, crit_id)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                                self.__on_criterion_state_changed)

    def __add_combo_signal(self, combo, crit_id):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(combo,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               smapper, QtCore.SLOT("map()"))
        smapper.setMapping(combo, crit_id)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                               self.__on_criterion_direction_changed)

    def __on_criterion_state_changed(self, crit_id):
        row = self.crit_row[crit_id]
        item = self.cellWidget(row, 0)
        self.emit(QtCore.SIGNAL("criterion_state_changed"), crit_id,
                  item.isChecked())

    def __on_criterion_direction_changed(self, crit_id):
        row = self.crit_row[crit_id]
        item = self.cellWidget(row, 1)
        self.emit(QtCore.SIGNAL("criterion_direction_changed"), crit_id,
                item.currentIndex())

    @property
    def ncriteria(self):
        return len(self.crit_row)

    @property
    def criteria_enabled(self):
        criteria = []
        for crit, row in self.crit_row.iteritems():
            item = self.cellWidget(row, 0)
            if item.isChecked() == True:
                criteria.append(crit)
        return criteria
