#!/usr/bin/python
import sys
sys.path.insert(0, "..")
import copy
from qgis.PyQt import QtCore
from qgis.PyQt import QtGui
from qgis.PyQt import QtWidgets
from qgis_etri.table import qt_criteria_table
from qgis_etri.table import qt_performance_table
from qgis_etri.table import qt_threshold_table
from xml.etree import ElementTree
from qgis_etri.mcda.electre_tri import ElectreTri
from qgis_etri.main import main_window

crit_table = None
prof_table = None
indif_table = None
pref_table = None
veto_table = None
thresh_cbox = None

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
    print(criterion.id, ":", criterion.direction)

def criterion_state_changed(criterion):
    criterion = c[criterion]
    print("Criteria state changed:", criterion)
    for table in [ perf_table, prof_table, indif_table, pref_table, veto_table ]:
        if table != None:
            table.disable_criterion(criterion)

def same_threshold_changed():
    for crit in c:
        if thresh_cbox.isChecked() is True:
            if crit.thresholds.has_threshold('q1'):
                q = copy.deepcopy(crit.thresholds['q1'])
                q.id = 'q'
                q.name = 'q'
            else:
                q = threshold('q', 'q', Constant(None, 0))

            if crit.thresholds.has_threshold('p1'):
                p = copy.deepcopy(crit.thresholds['p1'])
                p.id = 'p'
                p.name = 'p'
            else:
                p = threshold('p', 'p', Constant(None, 0))

            if crit.thresholds.has_threshold('v1'):
                v = copy.deepcopy(crit.thresholds['v1'])
                v.id = 'v'
                v.name = 'v'
            else:
                v = threshold('v', 'v', Constant(None, None))

            t = Thresholds([q, p, v])
            crit.thresholds = t
        else:
            t = Thresholds([])
            for i in range(1,len(b)+1):
                qid = 'q%d' % i
                pid = 'p%d' % i
                vid = 'v%d' % i
                if crit.thresholds.has_threshold('q'):
                    q = copy.deepcopy(crit.thresholds['q'])
                    q.id = qid 
                    q.name = qid
                else:
                    q = threshold(qid, qid, Constant(None, 0))
                if crit.thresholds.has_threshold('p'):
                    p = copy.deepcopy(crit.thresholds['p'])
                    p.id = pid 
                    p.name = pid
                else:
                    p = threshold(pid, pid, Constant(None, 0))
                if crit.thresholds.has_threshold('v'):
                    v = copy.deepcopy(crit.thresholds['v'])
                    v.id = vid
                    v.name = vid
                else:
                    v = threshold(vid, vid, Constant(None, None))

                t.append(q)
                t.append(p)
                t.append(v)

            crit.thresholds = t

    indif_table.reset_table()
    pref_table.reset_table()
    veto_table.reset_table()
    indif_table.add_criteria(c)
    pref_table.add_criteria(c)
    veto_table.add_criteria(c)
    if thresh_cbox.isChecked() is True: 
       indif_table.add_threshold('q', 'q')
       pref_table.add_threshold('p', 'p')
       veto_table.add_threshold('v', 'v')
    else:
       for i in range(1,len(b)+1):
           indi_thr = "q%d"% i
           pref_thr = "p%d"% i
           veto_thr = "v%d"% i
           indif_table.add_threshold(indi_thr, indi_thr)
           pref_table.add_threshold(pref_thr, pref_thr)
           veto_table.add_threshold(veto_thr, veto_thr)

def add_tab(tabs, table, name):
    tab = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(tab)
    if isinstance(table, list):
        for t in table:
            layout.addWidget(t)
    else:
        layout.addWidget(table)
    tabs.addTab(tab, name)

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
        indent(root)
        ElementTree.dump(root)
        buf = ElementTree.tostring(root, encoding="UTF-8", method="xml")
        with open(fname, 'wb') as f:
            f.write(buf)

def run_electre_tri():
    etri = ElectreTri(c, cv, ptb, lbda, cps)
    assignments = etri.pessimist(pt)
    cat_colors = main_window.generate_category_colors(len(b)+1)
    print([c.getRgb() for c in cat_colors.values()])
    perf_table.add_assignments(assignments, None)

if __name__ == "__main__":

    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        from data_loulouka_new import *
    else:
        from data_ticino_new import *

    app = QtWidgets.QApplication(sys.argv)
    perf_table = qt_performance_table(None, c, a, pt)
    crit_table = qt_criteria_table(None)
    crit_table.add_criteria(c, cv)
    prof_table = qt_performance_table(None, c, b, ptb)

    thresh_cbox = QtWidgets.QCheckBox('Use same thresholds for all profiles')
    indif_table = qt_threshold_table(None, c)
    pref_table = qt_threshold_table(None, c)
    veto_table = qt_threshold_table(None, c)

    crit = next(c.itervalues())
    for thres in crit.thresholds:
        print(thres)
    if crit.thresholds.has_threshold('q'):
        indif_table.add_threshold('q', 'q')
        pref_table.add_threshold('p', 'p')
        veto_table.add_threshold('v', 'v')
        thresh_cbox.setCheckState(QtCore.Qt.Checked)
    else:
        for i in range(1,len(b)+1):
            indi_thr = "q%d"% i
            pref_thr = "p%d"% i
            veto_thr = "v%d"% i
            indif_table.add_threshold(indi_thr, indi_thr)
            pref_table.add_threshold(pref_thr, pref_thr)
            veto_table.add_threshold(veto_thr, veto_thr)

    tabs = QtWidgets.QTabWidget()
    add_tab(tabs, perf_table, "Performance table")
    add_tab(tabs, crit_table, "Criteria")
    add_tab(tabs, prof_table, "Categories")
    add_tab(tabs, [thresh_cbox, indif_table, pref_table, veto_table], "Thresholds")

    button_to_xmcda = QtWidgets.QPushButton("Save to XMCDA")
    button_etri = QtWidgets.QPushButton("Apply ELECTRE TRI")

    crit_table.criterion_state_changed.connect(criterion_state_changed)
    crit_table.criterion_direction_changed.connect(criterion_direction_changed)
    thresh_cbox.clicked.connect(same_threshold_changed)

    button_to_xmcda.clicked.connect(save_to_xmcda)
    button_etri.clicked.connect(run_electre_tri)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(tabs)
    layout.addWidget(button_to_xmcda)
    layout.addWidget(button_etri)
    dialog = QtWidgets.QDialog()
    dialog.setLayout(layout)
    dialog.resize(640, 480)
    dialog.show()
    app.exec_()
