#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import alternatives, criteria, performance_table
from table import qt_performance_table 
from xml.etree import ElementTree

ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
ElementTree.register_namespace("xmcda", "http://www.decision-deck.org/2009/XMCDA-2.1.0")

pt_table = None

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
    if not pt_table:
        return

    fname = save_dialog_box()
    if fname:
        root = ElementTree.Element('{http://www.decision-deck.org/2009/XMCDA-2.1.0}XMCDA')
        pt_xmcda = pt.to_xmcda()
        criteria_xmcda = c.to_xmcda()
        alternatives_xmcda = a.to_xmcda()[0]
        root.append(pt_xmcda)
        root.append(criteria_xmcda)
        root.append(alternatives_xmcda)
        ElementTree.dump(root)
        indent(root)
        ElementTree.ElementTree(root).write(fname, xml_declaration=True,
                                            encoding='utf-8', method='xml')

def load_from_xmcda():
    if not pt_table:
        return

    fname = load_dialog_box()
    if fname:
        tree = ElementTree.parse(fname)
        root = tree.getroot()
        ElementTree.dump(root)

        a = alternatives()
        a.from_xmcda(root)

        c = criteria()
        c.from_xmcda(root, root)

        pt = performance_table()
        pt.from_xmcda(root)

        pt_table.reset_table()
        pt_table.add_criteria(c)
        pt_table.add_pt(a, pt)

def add_alternative():
    string, ok = QtGui.QInputDialog.getText(None, "Add alternative", "Alternative name")
    if ok and not string.isEmpty():
        name = str(string.toUtf8())
        alt = alternative(name, name)
        alt_perfs = alternative_performances(alt.id)
        pt_table.add(alt, alt_perfs)
        a.append(alt)
        pt.append(alt_perfs)

def add_criterion():
    string, ok = QtGui.QInputDialog.getText(None, "Add criterion", "Criterion name")
    if ok and not string.isEmpty():
        name = str(string.toUtf8())
        crit = criterion(name, name, 0, 1, 10)
        pt_table.add_criterion(crit)
        c.append(crit)

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtGui.QApplication(sys.argv)
    pt_table = qt_performance_table(None, c, a, pt)

    button_add = QtGui.QPushButton("Add alternative")
    button_addc = QtGui.QPushButton("Add criterion")
    button_to_xmcda = QtGui.QPushButton("Save to XMCDA")
    button_from_xmcda = QtGui.QPushButton("Load from XMCDA")

    button_to_xmcda.connect(button_add,
                            QtCore.SIGNAL("clicked()"),
                            add_alternative)
    button_to_xmcda.connect(button_addc,
                            QtCore.SIGNAL("clicked()"),
                            add_criterion)
    button_to_xmcda.connect(button_to_xmcda,
                            QtCore.SIGNAL("clicked()"),
                            save_to_xmcda)
    button_from_xmcda.connect(button_from_xmcda,
                              QtCore.SIGNAL("clicked()"),
                              load_from_xmcda)

    layout = QtGui.QVBoxLayout()
    layout.addWidget(pt_table)
    layout.addWidget(button_add)
    layout.addWidget(button_addc)
    layout.addWidget(button_to_xmcda)
    layout.addWidget(button_from_xmcda)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
