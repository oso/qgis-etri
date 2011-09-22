#!/usr/bin/python
import sys
sys.path.insert(0, "..")
from PyQt4 import QtCore
from PyQt4 import QtGui
from mcda.types import criterion
from ui.table import criteria_table, profiles_table
from data_ticino_new import *

crit_table = None

def criterion_direction_changed(criterion):
    print criterion.id, ":", criterion.direction

def criterion_state_changed(criterion):
    print criterion.id, ":", criterion.disabled

    print "# of criteria:", crit_table.ncriteria
    print "Criteria enabled:", crit_table.criteria_enabled

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    crit_table = criteria_table(criteria)
    prof_table = profiles_table(criteria)

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
    layout.addWidget(prof_table)
    dialog = QtGui.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
