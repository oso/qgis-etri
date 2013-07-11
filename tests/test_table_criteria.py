#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import Criterion
from table import qt_criteria_table
from xml.etree import ElementTree

ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
ElementTree.register_namespace("xmcda", "http://www.decision-deck.org/2009/XMCDA-2.1.0")

crit_table = None

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def save_dialog_box():
    fname = QtGui.QFileDialog.getSaveFileName(None,
                                              "Save XMCDA file", ".",
                                              "XMCDA files (*.xmcda)")
    fname = unicode(fname)
    if fname:
        if "." not in fname:
            fname += ".xmcda"

    return fname

def load_dialog_box():
    fname = QtGui.QFileDialog.getOpenFileName(None,
                                              "Load XMCDA file", ".",
                                              "XMCDA files (*.xmcda)")
    return unicode(fname)

def save_to_xmcda():
    if not crit_table:
        return

    fname = save_dialog_box()
    if fname:
        root = ElementTree.Element('{http://www.decision-deck.org/2009/XMCDA-2.1.0}XMCDA')
        criteria_xmcda = c.to_xmcda()
        criteria_values_xmcda = cv.to_xmcda()
        root.append(criteria_xmcda)
        root.append(criteria_values_xmcda)
        indent(root)
        ElementTree.ElementTree(root).write(fname, xml_declaration=True,
                                            encoding='utf-8', method='xml')

def load_from_xmcda():
    if not crit_table:
        return

    fname = load_dialog_box()
    if fname:
        tree = ElementTree.parse(fname)
        root = tree.getroot()
        ElementTree.dump(root)

        c = Criteria()
        c.from_xmcda(root.find('.//criteria'))

        cv = CriteriaValues()
        cv.from_xmcda(root.find('.//criteriaValues'))

        crit_table.reset_table()
        crit_table.add_criteria(c, cv)

def add_criterion():
    string, ok = QtGui.QInputDialog.getText(None, "Add criterion", "Criterion name")
    if ok and not string.isEmpty():
        name = str(string.toUtf8())
        crit = Criterion(name, name, 0, 1, 10)
        crit_table.add_criterion(crit)
        c.append(crit)

def criterion_direction_changed(criterion):
    print "Criterion direction changed:", criterion

def criterion_state_changed(criterion):
    print "Criterion state changed:", criterion

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtGui.QApplication(sys.argv)
    crit_table = qt_criteria_table(None)

    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_state_changed"),
                       criterion_state_changed)
    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_direction_changed"),
                       criterion_direction_changed)

    button_add = QtGui.QPushButton("Add criterion")
    button_to_xmcda = QtGui.QPushButton("Save to XMCDA")
    button_from_xmcda = QtGui.QPushButton("Load from XMCDA")

    button_to_xmcda.connect(button_add,
                            QtCore.SIGNAL("clicked()"),
                            add_criterion)
    button_to_xmcda.connect(button_to_xmcda,
                            QtCore.SIGNAL("clicked()"),
                            save_to_xmcda)
    button_from_xmcda.connect(button_from_xmcda,
                              QtCore.SIGNAL("clicked()"),
                              load_from_xmcda)

    crit_table.add_criteria(c, cv)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(crit_table)
    layout.addWidget(button_add)
    layout.addWidget(button_to_xmcda)
    layout.addWidget(button_from_xmcda)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
