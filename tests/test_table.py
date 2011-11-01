#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import criterion
from table import qt_criteria_table, qt_performance_table, qt_threshold_table
from xml.etree import ElementTree

crit_table = None
prof_table = None
indif_table = None
pref_table = None
veto_table = None

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

def criterion_direction_changed(criterion):
    print criterion.id, ":", criterion.direction

def criterion_state_changed(criterion):
    print "Criteria enabled:", crit_table.criteria_enabled
    for table in [ perf_table, prof_table, indif_table, pref_table, veto_table ]:
        if table != None:
            table.disable_criterion(criterion)

def add_tab(tabs, table, name):
    tab = QtGui.QWidget()
    layout = QtGui.QVBoxLayout(tab)
    if isinstance(table, list):
        for t in table:
            layout.addWidget(t)
    else:
        layout.addWidget(table)
    tabs.addTab(tab, name)

def save_dialog_box():
    fname = QtGui.QFileDialog.getSaveFileName(None,
                                              "Save XMCDA file", ".",
                                              "XMCDA files (*.xmcda)")
    fname = unicode(fname)
    if fname:
        if "." not in fname:
            fname += ".xmcda"

    return fname

def save_to_xmcda():
    fname = save_dialog_box()
    if fname:
        root = ElementTree.Element('{http://www.decision-deck.org/2009/XMCDA-2.1.0}XMCDA')
        pt_xmcda = ptb.to_xmcda()
        criteria_xmcda = c.to_xmcda()
        alternatives_xmcda = b.to_xmcda()[0]
        root.append(pt_xmcda)
        root.append(criteria_xmcda)
        root.append(alternatives_xmcda)
        ElementTree.dump(root)
        indent(root)
        ElementTree.ElementTree(root).write(fname, xml_declaration=True,
                                            encoding='utf-8', method='xml')

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtGui.QApplication(sys.argv)
    perf_table = qt_performance_table(None, c, a, pt)
    crit_table = qt_criteria_table(None, c)
    prof_table = qt_performance_table(None, c, b, ptb)

    indif_table = qt_threshold_table(None, c)
    pref_table = qt_threshold_table(None, c)
    veto_table = qt_threshold_table(None, c)

    indif_table.add_threshold('q', 'q')
    pref_table.add_threshold('p', 'p')
    veto_table.add_threshold('v', 'v')

    tabs = QtGui.QTabWidget()
    add_tab(tabs, perf_table, "Performance table")
    add_tab(tabs, crit_table, "Criteria")
    add_tab(tabs, prof_table, "Categories")
    add_tab(tabs, [indif_table, pref_table, veto_table], "Thresholds")

    button_to_xmcda = QtGui.QPushButton("Save to XMCDA")

    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_state_changed"),
                       criterion_state_changed)
    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_direction_changed"),
                       criterion_direction_changed)
    button_to_xmcda.connect(button_to_xmcda,
                            QtCore.SIGNAL("clicked()"),
                            save_to_xmcda)

    print "# of criteria:", crit_table.ncriteria
    print "Criteria enabled:", crit_table.criteria_enabled

    layout = QtGui.QVBoxLayout()
    layout.addWidget(tabs)
    layout.addWidget(button_to_xmcda)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
