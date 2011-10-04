#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import criterion
from table import criteria_table, profiles_table, threshold_table

crit_table = None
prof_table = None
indif_table = None
pref_table = None
veto_table = None

def criterion_direction_changed(criterion):
    print criterion.id, ":", criterion.direction

def criterion_state_changed(criterion):
    print "Criteria enabled:", crit_table.criteria_enabled
    for table in [ prof_table, indif_table, pref_table, veto_table ]:
        if table != None:
            table.disable_criterion(criterion)

def add_tab(tabs, table, name):
    tab = QtGui.QWidget()
    layout = QtGui.QVBoxLayout(tab)
    layout.addWidget(table)
    tabs.addTab(tab, name)

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtGui.QApplication(sys.argv)
    crit_table = criteria_table(None, c)
    prof_table = profiles_table(None, c, profiles)

    indif_table = threshold_table(None, c)
    pref_table = threshold_table(None, c)
    veto_table = threshold_table(None, c)
    for profile in profiles:
        indif_table.add(q)
        pref_table.add(p)
        veto_table.add(v)

    tabs = QtGui.QTabWidget()
    add_tab(tabs, prof_table, "Profiles")
    add_tab(tabs, indif_table, "Indifference")
    add_tab(tabs, pref_table, "Preference")
    add_tab(tabs, veto_table, "Veto")

    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_state_changed"),
                       criterion_state_changed)
    crit_table.connect(crit_table,
                       QtCore.SIGNAL("criterion_direction_changed"),
                       criterion_direction_changed)

    print "# of criteria:", crit_table.ncriteria
    print "Criteria enabled:", crit_table.criteria_enabled

    layout = QtGui.QVBoxLayout()
    layout.addWidget(crit_table)
    layout.addWidget(tabs)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
