#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from qgis.PyQt import QtCore
from qgis.PyQt import QtGui
from qgis.PyQt import QtWidgets
from qgis_etri.mcda.types import Alternatives, AlternativePerformances, Criteria, PerformanceTable
from qgis_etri.table import qt_performance_table
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
    if not pt_table:
        return

    fname = save_dialog_box()
    if fname:
        root = ElementTree.Element('{http://www.decision-deck.org/2009/XMCDA-2.1.0}XMCDA')
        pt_xmcda = pt.to_xmcda()
        criteria_xmcda = c.to_xmcda()
        alternatives_xmcda = a.to_xmcda()
        root.append(pt_xmcda)
        root.append(criteria_xmcda)
        root.append(alternatives_xmcda)
        indent(root)
        ElementTree.dump(root)
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

        a = Alternatives()
        a.from_xmcda(root.find('.//alternatives'))

        c = Criteria()
        c.from_xmcda(root.find('.//criteria'))

        pt = PerformanceTable()
        pt.from_xmcda(root.find('.//performanceTable'))

        pt_table.reset_table()
        pt_table.add_criteria(c)
        pt_table.add_pt(a, pt)

def add_alternative():
    name, ok = QtWidgets.QInputDialog.getText(None, "Add alternative", "Alternative name")
    if ok and name:
        alt = Alternative(name, name)
        alt_perfs = AlternativePerformances(alt.id, {id: 7 for id in c.iterkeys()})
        pt_table.add(alt, alt_perfs)
        a.append(alt)
        pt.append(alt_perfs)

def add_criterion():
    name, ok = QtWidgets.QInputDialog.getText(None, "Add criterion", "Criterion name")
    if ok and name:
        crit = Criterion(name, name, False, 1, 10)
        pt_table.add_criterion(crit)
        c.append(crit)
        for ap in pt.itervalues():
            ap.performances[name] = 88

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtWidgets.QApplication(sys.argv)
    pt_table = qt_performance_table(None, c, a, pt)

    button_add = QtWidgets.QPushButton("Add alternative")
    button_addc = QtWidgets.QPushButton("Add criterion")
    button_to_xmcda = QtWidgets.QPushButton("Save to XMCDA")
    button_from_xmcda = QtWidgets.QPushButton("Load from XMCDA")

    button_add.clicked.connect(add_alternative)
    button_addc.clicked.connect(add_criterion)
    button_to_xmcda.clicked.connect(save_to_xmcda)
    button_from_xmcda.clicked.connect(load_from_xmcda)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(pt_table)
    layout.addWidget(button_add)
    layout.addWidget(button_addc)
    layout.addWidget(button_to_xmcda)
    layout.addWidget(button_from_xmcda)
    dialog = QtWidgets.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
