#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from qgis.PyQt import QtCore
from qgis.PyQt import QtGui
from qgis.PyQt import QtWidgets
from qgis_etri.mcda.types import Criterion
from qgis_etri.table import qt_criteria_table
from qgis_etri.mcda.xml_writer import Element, tostring
from qgis_etri.xml_utils import safe_parse

crit_table = None

def save_dialog_box():
    fname = QtWidgets.QFileDialog.getSaveFileName(None,
                                              "Save XMCDA file", ".",
                                              "XMCDA files (*.xmcda)")
    if isinstance(fname, tuple):
        fname = fname[0]
    fname = str(fname)
    if fname:
        if "." not in fname:
            fname += ".xmcda"

    return fname

def load_dialog_box():
    fname = QtWidgets.QFileDialog.getOpenFileName(None,
                                              "Load XMCDA file", ".",
                                              "XMCDA files (*.xmcda)")
    if isinstance(fname, tuple):
        fname = fname[0]
    return str(fname)

def save_to_xmcda():
    if not crit_table:
        return

    fname = save_dialog_box()
    if fname:
        root = Element('xmcda:XMCDA', {'xmlns:xmcda': 'http://www.decision-deck.org/2009/XMCDA-2.1.0'})
        criteria_xmcda = c.to_xmcda()
        criteria_values_xmcda = cv.to_xmcda()
        root.append(criteria_xmcda)
        root.append(criteria_values_xmcda)
        with open(fname, 'wb') as f:
            f.write(tostring(root, xml_declaration=True))

def load_from_xmcda():
    if not crit_table:
        return

    fname = load_dialog_box()
    if fname:
        tree = safe_parse(fname)
        root = tree.getroot()

        c = Criteria()
        c.from_xmcda(root.find('.//criteria'))

        cv = CriteriaValues()
        cv.from_xmcda(root.find('.//criteriaValues'))

        crit_table.reset_table()
        crit_table.add_criteria(c, cv)

def add_criterion():
    name, ok = QtWidgets.QInputDialog.getText(None, "Add criterion", "Criterion name")
    if ok and name:
        # name = str(string.toUtf8())
        crit = Criterion(name, name, 0, 1, 10)
        critV = CriterionValue(name, 10)
        crit_table.add_criterion(crit, critV)
        c.append(crit)
        cv.append(critV)

def criterion_direction_changed(criterion):
    print("Criterion direction changed:", criterion)

def criterion_state_changed(criterion):
    print("Criterion state changed:", criterion)

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtWidgets.QApplication(sys.argv)
    crit_table = qt_criteria_table(None)

    crit_table.criterion_state_changed.connect(criterion_state_changed)
    crit_table.criterion_direction_changed.connect(criterion_direction_changed)

    button_add = QtWidgets.QPushButton("Add criterion")
    button_to_xmcda = QtWidgets.QPushButton("Save to XMCDA")
    button_from_xmcda = QtWidgets.QPushButton("Load from XMCDA")

    button_add.clicked.connect(add_criterion)
    button_to_xmcda.clicked.connect(save_to_xmcda)
    button_from_xmcda.clicked.connect(load_from_xmcda)

    crit_table.add_criteria(c, cv)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(crit_table)
    layout.addWidget(button_add)
    layout.addWidget(button_to_xmcda)
    layout.addWidget(button_from_xmcda)
    dialog = QtWidgets.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec()
