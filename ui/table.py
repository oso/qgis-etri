import sys
sys.path.append("..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda import criterion

COMBO_INDEX_MAX=0
COMBO_INDEX_MIN=1

class criteria_table(QtGui.QTableWidget):

    def __init__(self, parent=None):
        super(QtGui.QTableWidget, self).__init__(parent)
        self.parent = parent
        self.row_crit = {}

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

    def add(self, criterion):
        row = self.rowCount()
        self.insertRow(row)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, 0, item)
        cbox = QtGui.QCheckBox(self)
        if criterion.disabled != False:
            cbox.setCheckState(QtCore.Qt.Checked)
        cbox.setText(criterion.name)
        self.__add_cbox_signal(cbox, row)
        self.setCellWidget(row, 0, cbox)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, 1, item)
        combo = QtGui.QComboBox(self)
        combo.addItem("Max")
        combo.addItem("Min")
        if criterion.direction == -1:
            combo.setCurrentIndex(1)
        self.__add_combo_signal(combo, row)
        self.setCellWidget(row, 1, combo)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        item.setText(str(criterion.weight))
        self.setItem(row, 2, item)

        self.row_crit[row] = criterion

    def __add_cbox_signal(self, cbox, row):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(cbox, QtCore.SIGNAL("stateChanged(int)"),
                                smapper, QtCore.SLOT("map()"))
        smapper.setMapping(cbox, row)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                                self.__on_criterion_state_changed)

    def __add_combo_signal(self, combo, row):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(combo,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               smapper, QtCore.SLOT("map()"))
        smapper.setMapping(combo, row)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                               self.__on_criterion_direction_changed)

    def __on_criterion_state_changed(self, row):
        criterion = self.row_crit[row]
        item = self.cellWidget(row, 0)
        if item.isChecked() == 1:
            criterion.disabled = criterion.ENABLED
        else:
            criterion.disabled = criterion.DISABLED
        self.emit(QtCore.SIGNAL("criterion_state_changed"), criterion)

    def __on_criterion_direction_changed(self, row):
        criterion = self.row_crit[row]
        item = self.cellWidget(row, 1)
        if item.currentIndex() == COMBO_INDEX_MAX:
            criterion.direction = 1
        else:
            criterion.direction = -1
        self.emit(QtCore.SIGNAL("criterion_direction_changed"), criterion)

    def __get_criterion_row(self, criterion):
        crit_row = dict([[v,k] for k,v in mydict.items()])
        return crit_row[criterion]

    def update_criterion_enable(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, 1)
        if criterion.disabled == 0:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def update_criterion_direction(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, 1)
        if criterion.direction == 1:
            item.setCurrentIndex(0)
        else:
            item.setCurrentIndex(1)

    def update_criterion_weight(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, 2)
        item.setText(str(criterion.weight))

    @property
    def ncriteria(self):
        return len(self.row_crit)

    @property
    def criteria_enabled(self):
        criteria = []
        for row, crit in self.row_crit.iteritems():
            item = self.cellWidget(row, 0)
            if item.isChecked() == True:
                criteria.append(crit)
        return criteria
