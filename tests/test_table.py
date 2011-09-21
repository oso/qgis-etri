#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import criterion
from ui.table import criteria_table
from data_ticino import *

crit_table = None

def criterion_direction_changed(criterion):
    print criterion.id, ":", criterion.direction

def criterion_state_changed(criterion):
    print criterion.id, ":", criterion.disabled

    print "# of criteria:", crit_table.ncriteria
    print "Criteria enabled:", crit_table.criteria_enabled

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    table = criteria_table()
    crit_table = table

    for i, crit_name in enumerate(criteria):
        crit = criterion(i)
        crit.name = crit_name
        crit.weight = w[crit_name]
        crit.direction = d[crit_name] 
        table.add(crit)

    table.connect(table, QtCore.SIGNAL("criterion_state_changed"),
                  criterion_state_changed)
    table.connect(table, QtCore.SIGNAL("criterion_direction_changed"),
                  criterion_direction_changed)

    print "# of criteria:", table.ncriteria
    print "Criteria enabled:", table.criteria_enabled

    layout = QtGui.QVBoxLayout()
    layout.addWidget(table)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
