import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import criterion

COMBO_INDEX_MAX=0
COMBO_INDEX_MIN=1
COL_NAME = 0
COL_DIRECTION = 1
COL_WEIGHT = 2

class float_delegate(QtGui.QItemDelegate):

    def __init__(self, parent=None, columns=None):
        super(float_delegate, self).__init__(parent)
        self.columns = columns

    def createEditor(self, parent, option, index):
        if self.columns == None or index.column() in self.columns:
            line = QtGui.QLineEdit(parent)
            expr = QtCore.QRegExp("[0-9]*\.?[0-9]*")
            line.setValidator(QtGui.QRegExpValidator(expr, self))
            return line
        else:
            Qtgui.QItemDelegate.createEditor(self, parent, option, index)

class criteria_table(QtGui.QTableWidget):

    def __init__(self, parent=None, criteria=None):
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
        self.setColumnWidth(COL_NAME, 255)
        self.setColumnWidth(COL_DIRECTION, 60)
        self.setColumnWidth(COL_WEIGHT, 100)

        self.connect(self, QtCore.SIGNAL("cellChanged(int,int)"),
                     self.__cell_changed)
        self.setItemDelegate(float_delegate(self, [COL_WEIGHT]))

        if criteria != None:
            for criterion in criteria:
                self.add(criterion)

    def __cell_changed(self, row, col):
        if col == COL_WEIGHT:
            if self.row_crit.has_key(row) == False:
                return

            criterion = self.row_crit[row]
            item = self.cellWidget(row, col)
            if item == None:
                return

            try:
                criterion.weight = float(item.text())
            except:
                QtGui.QMessageBox.warning(self,
                                          "Criterion %s" % criterion.name,
                                          "Invalid weight value")

    def __add_headers(self):
        item = QtGui.QTableWidgetItem()
        item.setText("Criterion")
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.setHorizontalHeaderItem(COL_NAME, item)

        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(COL_DIRECTION, item)

        item = QtGui.QTableWidgetItem()
        item.setText("Weight")
        item.setTextAlignment(QtCore.Qt.AlignRight)
        self.setHorizontalHeaderItem(COL_WEIGHT, item)

    def add(self, criterion):
        row = self.rowCount()
        self.insertRow(row)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, COL_NAME, item)
        cbox = QtGui.QCheckBox(self)
        if criterion.disabled != True:
            cbox.setCheckState(QtCore.Qt.Checked)
        cbox.setText(criterion.name)
        self.__add_cbox_signal(cbox, row)
        self.setCellWidget(row, COL_NAME, cbox)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, COL_DIRECTION, item)
        combo = QtGui.QComboBox(self)
        combo.addItem("Max")
        combo.addItem("Min")
        if criterion.direction == -1:
            combo.setCurrentIndex(1)
        self.__add_combo_signal(combo, row)
        self.setCellWidget(row, COL_DIRECTION, combo)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        item.setText(str(criterion.weight))
        self.setItem(row, COL_WEIGHT, item)

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
        crit_row = dict([[v,k] for k,v in self.row_crit.items()])
        return crit_row[criterion]

    def update_criterion_enable(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, COL_NAME)
        if criterion.disabled == 0:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def update_criterion_direction(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, COL_DIRECTION)
        if criterion.direction == 1:
            item.setCurrentIndex(0)
        else:
            item.setCurrentIndex(1)

    def update_criterion_weight(self, criterion):
        row = self.__get_criterion_row(criterion)
        item = self.cellWidget(row, COL_WEIGHT)
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

class profiles_table(QtGui.QTableWidget):

    def __init__(self, parent=None, criteria=None, profiles=None):
        super(QtGui.QTableWidget, self).__init__(parent)
        self.parent = parent
        self.col_crit = {}

        self.setItemDelegate(float_delegate(self))

        if criteria != None:
            for criterion in criteria:
                self.add_criterion(criterion)

        if profiles != None:
            for profile in profiles:
                self.add(profile)

    def add_criterion(self, criterion):
        col = self.columnCount()
        self.insertColumn(col)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(col, item)
        self.horizontalHeaderItem(col).setText(criterion.name)
        if criterion.disabled:
            self.setColumnHidden(col, True)
        self.col_crit[col] = criterion

    def add(self, profile):
        row = self.rowCount()
        self.insertRow(row)
        for col, crit in self.col_crit.iteritems():
            item = QtGui.QTableWidgetItem()
            if profile.evaluations.has_key(crit):
                item.setText(str(profile.evaluations[crit]))
            self.setItem(row, col, item)

    def __get_criterion_col(self, criterion):
        crit_col = dict([[v,k] for k,v in self.col_crit.items()])
        return crit_col[criterion]

    def disable_criterion(self, criterion, disable):
        self.setColumnHidden(self.__get_criterion_col(criterion), disable)

class threshold_table(profiles_table):
    pass
