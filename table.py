from PyQt4 import QtCore
from PyQt4 import QtGui
from collections import OrderedDict
from mcda.types import Criteria, Criterion, Constant

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
            QtGui.QItemDelegate.createEditor(self, parent, option, index)

class qt_criteria_table(QtGui.QTableWidget):

    def __init__(self, parent = None):
        super(qt_criteria_table, self).__init__(parent)

        self.row_crit = {}

        self.setColumnCount(3)
        self.setShowGrid(False)
        self.setDragEnabled(False)
        self.__add_headers()
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSortIndicatorShown(False)
        self.horizontalHeader().setHighlightSections(False)

        self.connect(self, QtCore.SIGNAL("cellChanged(int,int)"),
                     self.__cell_changed)
        self.setItemDelegate(float_delegate(self, [COL_WEIGHT]))

    def __cell_changed(self, row, col):
        if col == COL_WEIGHT:
            if self.row_crit.has_key(row) is False:
                return

            c, cv = self.row_crit[row]
            item = self.cellWidget(row, col)
            if item is None:
                return

            try:
                value = str(item.text())
                if value.find('.') == -1:
                    cv.value = int(value)
                else:
                    cv.value = float(value)
            except:
                QtGui.QMessageBox.warning(self,
                                          "Criterion [%s] %s"
                                          % (c.id, c.name),
                                          "Invalid weight value")
                item = QtGui.QTableWidgetItem()
                item.setText("0")
                item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                self.setItem(row, COL_WEIGHT, item)

    def reset_table(self):
        self.clearContents()
        self.setRowCount(0)
        self.row_crit = {}

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

    def __on_criterion_direction_changed(self, row):
        c, cv = self.row_crit[row]
        item = self.cellWidget(row, 1)
        if item.currentIndex() == 0:
            c.direction = 1
        else:
            c.direction = -1
        self.emit(QtCore.SIGNAL("criterion_direction_changed"), c.id)

    def __on_criterion_state_changed(self, row):
        c, cv = self.row_crit[row]
        item = self.cellWidget(row, COL_NAME)
        combo_dir = self.cellWidget(row, COL_DIRECTION)
        item_cv = self.item(row, COL_WEIGHT)
        if item.isChecked() is True:
            c.disabled = False
            item_cv.setText("0")
            combo_dir.setDisabled(False)
            item_cv.setFlags(item_cv.flags() | QtCore.Qt.ItemIsEnabled)
        else:
            c.disabled = True
            item_cv.setText("")
            combo_dir.setDisabled(True)
            item_cv.setFlags(item_cv.flags() & ~QtCore.Qt.ItemIsEnabled)
        self.emit(QtCore.SIGNAL("criterion_state_changed"), c)

    def __add_combo_signal(self, combo, row):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(combo,
                               QtCore.SIGNAL("currentIndexChanged(int)"),
                               smapper, QtCore.SLOT("map()"))
        smapper.setMapping(combo, row)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                               self.__on_criterion_direction_changed)

    def __add_cbox_signal(self, cbox, row):
        smapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(cbox, QtCore.SIGNAL("stateChanged(int)"),
                                smapper, QtCore.SLOT("map()"))
        smapper.setMapping(cbox, row)
        QtCore.QObject.connect(smapper, QtCore.SIGNAL("mapped(int)"),
                                self.__on_criterion_state_changed)

    def add_criterion(self, c, cv):
        row = self.rowCount()
        self.insertRow(row)

        self.row_crit[row] = (c, cv)

        # Add first cell with name and checkbox
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, COL_NAME, item)

        cbox = QtGui.QCheckBox(self)
        if c.disabled is not True:
            cbox.setCheckState(QtCore.Qt.Checked)
        if c.name:
            cbox.setText(c.name)
        else:
            cbox.setText(c.id)
        self.__add_cbox_signal(cbox, row)
        self.setCellWidget(row, COL_NAME, cbox)

        # Add direction cell
        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.setItem(row, COL_DIRECTION, item)
        combo = QtGui.QComboBox(self)
        combo.addItem("Max")
        combo.addItem("Min")
        if c.direction == -1:
            combo.setCurrentIndex(1)
        if c.disabled is True:
            combo.setDisabled(True)
        self.__add_combo_signal(combo, row)
        self.setCellWidget(row, COL_DIRECTION, combo)

        # Add weight column
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        if c.disabled is True:
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
        else:
            item.setText(str(cv.value))
        self.setItem(row, COL_WEIGHT, item)

    def add_criteria(self, cs, cvs):
        for c in cs:
            cv = cvs[c.id]
            self.add_criterion(c, cv)

class profiles_table(QtGui.QTableWidget):

    def __init__(self, parent=None, criteria=None, profiles=None):
        super(profiles_table, self).__init__(parent)
        self.parent = parent
        self.col_crit = {}

        self.setItemDelegate(float_delegate(self))

        if criteria != None:
            for criterion in criteria:
                self.add_criterion(criterion)

        if profiles != None:
            for profile in profiles:
                self.add(profile)

    def reset_table(self):
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)

    def add_criteria(self, criteria):
        for criterion in criteria:
            self.add_criterion(criterion)

    def add_criterion(self, criterion):
        col = self.columnCount()
        self.insertColumn(col)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(col, item)
        if criterion.name:
            self.horizontalHeaderItem(col).setText(criterion.name)
        else:
            self.horizontalHeaderItem(col).setText(criterion.id)
        if criterion.disabled:
            self.setColumnHidden(col, True)
        self.col_crit[col] = criterion

    def add(self, profile):
        row = self.rowCount()
        self.insertRow(row)
        for col, crit in self.col_crit.iteritems():
            item = QtGui.QTableWidgetItem()
            if profile.performances.has_key(crit):
                item.setText(str(profile.performances[crit]))
            self.setItem(row, col, item)

    def __get_criterion_col(self, criterion):
        crit_col = dict([[v,k] for k,v in self.col_crit.items()])
        return crit_col[criterion]

    def disable_criterion(self, criterion):
        self.setColumnHidden(self.__get_criterion_col(criterion),
                             criterion.disabled)

class threshold_table(profiles_table):
    pass

class qt_performance_table(QtGui.QTableWidget):

    def __init__(self, parent=None, criteria=None, alternatives=None, pt=None):
        super(qt_performance_table, self).__init__(parent)
        self.parent = parent
        self.col_crit = {}
        self.row_alt = []
        self.row_altp = []
        self.allownovalue = True

        self.setItemDelegate(float_delegate(self))

        if criteria is not None:
            self.add_criteria(criteria)

        if alternatives is not None and pt is not None:
            self.add_pt(alternatives, pt)

        self.connect(self, QtCore.SIGNAL("cellChanged(int,int)"),
                     self.__cell_changed)

    def reset_table(self):
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)
        self.col_crit = {}
        self.row_alt = []
        self.row_altp = []

    def add_criteria(self, criteria):
        for crit in criteria:
            self.add_criterion(crit)

    def add_criterion(self, criterion):
        col = self.columnCount()
        self.insertColumn(col)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(col, item)
        if criterion.name:
            self.horizontalHeaderItem(col).setText(criterion.name)
        else:
            self.horizontalHeaderItem(col).setText(criterion.id)
        if criterion.disabled is True:
            self.setColumnHidden(col, True)
        self.col_crit[col] = criterion

    def add_assignments(self, assignments, category_colors = None,
                        top = False):
        if top is True:
            col = 0
        else:
            col = self.columnCount()
        self.insertColumn(col)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(col, item)
        self.horizontalHeaderItem(col).setText('Category')
        for aa in assignments:
            item = QtGui.QTableWidgetItem()
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item.setText(str(aa.category_id))
            row = self.__get_alternative_row_by_id(aa.id)
            if category_colors is not None:
                item.setBackgroundColor(category_colors[aa.category_id])
            self.setItem(row, col, item)

    def __get_alternative_row_by_id(self, alternative_id):
        for i, alt in enumerate(self.row_alt):
            if alt.id == alternative_id:
                return i

        return None

    def __get_criterion_col(self, criterion):
        crit_col = dict([[v,k] for k,v in self.col_crit.items()])
        return crit_col[criterion]

    def disable_criterion(self, criterion):
        self.setColumnHidden(self.__get_criterion_col(criterion),
                             criterion.disabled)

    def add_pt(self, alternatives, pt, editable = True):
        for alternative in alternatives:
            self.add(alternative, pt[alternative.id], editable)

    def add(self, alternative, alt_perfs, editable = True):
        row = self.rowCount()
        self.insertRow(row)

        item = QtGui.QTableWidgetItem()
        self.setVerticalHeaderItem(row, item)
        if alternative.name:
            self.verticalHeaderItem(row).setText(alternative.name)
        else:
            self.verticalHeaderItem(row).setText(alternative.id)
        self.row_alt.append(alternative)

        performances = alt_perfs.performances
        for col, crit in self.col_crit.iteritems():
            item = QtGui.QTableWidgetItem()
            if performances.has_key(crit.id) and \
               performances[crit.id] is not None:
                 item.setText(str(performances[crit.id]))
            if editable is False:
                 item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.setItem(row, col, item)
        self.row_altp.append(alt_perfs)

    def remove_all(self):
        for i in range(len(self.row_alt)):
            self.removeRow(0)
            self.row_alt.pop(0)
            self.row_altp.pop(0)

    def remove(self, alternative_id):
        row = self.__get_alternative_row_by_id(alternative_id)
        self.removeRow(row)
        self.row_alt.pop(row)
        self.row_altp.pop(row)

    def __cell_changed(self, row, col):
        if self.col_crit.has_key(col) is False or   \
            row >= len(self.row_altp) or row < 0:
            return

        alt = self.row_alt[row]
        altp = self.row_altp[row]
        crit = self.col_crit[col]

        item = self.cellWidget(row, col)
        if item == None:
            return

        try:
            value = str(item.text())
            if len(value) == 0 and self.allownovalue:
                return

            if value.find('.') == -1:
               altp.performances[crit.id] = int(value)
            else:
               altp.performances[crit.id] = float(value)
        except:
            QtGui.QMessageBox.warning(self,
                                      "Alternative [%s] %s"
                                      % (alt.id, alt.name),
                                      "Invalid evaluation")

class qt_threshold_table(QtGui.QTableWidget):

    def __init__(self, parent=None, criteria=None):
        super(qt_threshold_table, self).__init__(parent)
        self.parent = parent
        self.col_crit = {}
        self.row_threshid = {}

        self.setItemDelegate(float_delegate(self)) 

        if criteria is not None:
            self.add_criteria(criteria)

        self.connect(self, QtCore.SIGNAL("cellChanged(int,int)"),
                     self.__cell_changed)

    def reset_table(self):
        self.clear()
        self.setRowCount(0)
        self.setColumnCount(0)

    def add_criteria(self, criteria):
        for crit in criteria:
            self.add_criterion(crit)

    def add_criterion(self, criterion):
        col = self.columnCount()
        self.insertColumn(col)
        item = QtGui.QTableWidgetItem()
        self.setHorizontalHeaderItem(col, item)
        if criterion.name:
            self.horizontalHeaderItem(col).setText(criterion.name)
        else:
            self.horizontalHeaderItem(col).setText(criterion.id)
        if criterion.disabled:
            self.setColumnHidden(col, True)
        self.col_crit[col] = criterion

    def __get_criterion_col(self, criterion):
        crit_col = dict([[v,k] for k,v in self.col_crit.items()])
        return crit_col[criterion]

    def disable_criterion(self, criterion):
        self.setColumnHidden(self.__get_criterion_col(criterion),
                             criterion.disabled)

    def add_threshold(self, threshold_id, threshold_name):
        row = self.rowCount()
        self.insertRow(row)

        item = QtGui.QTableWidgetItem()
        self.setVerticalHeaderItem(row, item)
        if threshold_name:
            self.verticalHeaderItem(row).setText(threshold_name)
        else:
            self.verticalHeaderItem(row).setText(threshold_id)
        self.row_threshid[row] = threshold_id

        for col, crit in self.col_crit.iteritems():
            item = QtGui.QTableWidgetItem()
            if crit.thresholds.has_threshold(threshold_id):
                t = crit.thresholds[threshold_id]
                # FIXME: handle other types
                if t.values.value is not None:
                    item.setText(str(t.values.value))

            self.setItem(row, col, item)

    def __cell_changed(self, row, col):
        if self.col_crit.has_key(col) is False or   \
            self.row_threshid.has_key(row) is False:
            return

        crit = self.col_crit[col]
        thresholds = crit.thresholds
        threshold_id = self.row_threshid[row]

        if thresholds.has_threshold(threshold_id) is False:
            return

        threshold = thresholds[threshold_id]

        item = self.cellWidget(row, col)
        if item == None:
            return

        # FIXME: Handle other types than constant
        try:
            value = str(item.text())
            if value == '':
                threshold.values.value = None
            elif value.find('.') == -1:
                threshold.values.value = int(value)
            else:
                threshold.values.value = float(value)
        except:
            QtGui.QMessageBox.warning(self,
                                          "Criterion [%s] %s"
                                          % (crit.id, crit.name),
                                          "Invalid threshold value")
