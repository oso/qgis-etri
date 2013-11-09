import os, sys, traceback
from xml.etree import ElementTree
from PyQt4 import QtCore, QtGui
from ui.main_window import Ui_main_window
from layer import criteria_layer
from mcda.electre_tri import ElectreTri
from mcda.types import Criteria, CriteriaValues
from mcda.types import PerformanceTable, Alternatives
from mcda.types import Alternative, AlternativePerformances
from mcda.types import Thresholds, Threshold
from mcda.generate import generate_categories
from mcda.generate import generate_categories_profiles
from qgis_utils import generate_decision_map, saveDialog, addtocDialog
from graphic import QGraphicsSceneEtri

COMBO_PROC_PESSIMIST = 0
COMBO_PROC_OPTIMIST = 1

class main_window(QtGui.QDialog, Ui_main_window):

    def __init__(self, iface = None, layer = None):
        QtGui.QDialog.__init__(self)
        Ui_main_window.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)

        self.iface = iface

        if iface:
            self.__update_layer_list(iface.mapCanvas())
        elif layer:
            self.layer = criteria_layer(layer)
            self.__loadlayer()
            self.__enable_buttons()

        self.table_criteria.connect(self.table_criteria,
                                    QtCore.SIGNAL("criterion_state_changed"),
                                    self.__criterion_state_changed)

    def closeEvent(self, event):
        val = QtGui.QMessageBox.question(self, "ELECTRE TRI",
                    "Close ELECTRE TRI?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.No)
        if val == QtGui.QMessageBox.No:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def __update_layer_list(self, map_canvas):
        if map_canvas == None:
            return

        for i in range(map_canvas.layerCount()):
            layer = map_canvas.layer(i)
            self.combo_layer.addItem(layer.name())

    def __update_criteria(self, criteria):
        self.criteria = criteria
        pass

    def __update_profiles(self, alternatives, pt):
        pass

    def __load_from_xmcda(self, xmcda_file):
        tree = ElementTree.parse(xmcda_file)
        root = tree.getroot()
        ElementTree.dump(root)
        xmcda_formatversion = root.find('.//formatversion')
        xmcda_crit = root.find('.//criteria')
        xmcda_critval = root.find('.//criteriaValues')
        xmcda_b = root.find('.//alternatives')
        xmcda_pt = root.findall('.//performanceTable')
        xmcda_lbda = root.find('.//methodParameters/parameter/value/real')

        # Remove criteria values that are not in the vector layer
        self.cv = CriteriaValues()
        self.cv.from_xmcda(xmcda_critval)
        for cv in self.cv:
            if cv.id not in self.criteria:
                self.cv.remove(cv.id)

        # Disable criteria for which there are no weights
        for c in self.criteria:
            if c.id not in self.cv:
                c.disabled = True

        self.balternatives = Alternatives()
        self.balternatives.from_xmcda(xmcda_b)

        self.bpt = PerformanceTable()
        self.qpt = PerformanceTable()
        self.ppt = PerformanceTable()
        self.vpt = PerformanceTable()

        for xmcda in xmcda_pt:
            if xmcda.get('id') is None:
                self.bpt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'q':
                self.qpt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'p':
                self.ppt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'v':
                self.vpt.from_xmcda(xmcda)

        if len(self.qpt) == 0 and len(self.ppt) > 0:
            self.qpt = self.ppt.copy()
            self.qpt.id = "q"

        if len(self.ppt) == 0 and len(self.qpt) > 0:
            self.ppt = self.qpt.copy()
            self.ppt.id = "p"

        # Categories Profiles
        self.categories = generate_categories(len(self.bpt), prefix = "")
        self.cat_profiles = generate_categories_profiles(self.categories)

        self.lbda = float(xmcda_lbda.text)

    def __generate_first_profile(self):
        crit_min = {}
        crit_max = {}
        for altp in self.pt:
            for crit in self.criteria:
                d = crit.direction
                if crit_min.has_key(crit.id) is False:
                    crit_min[crit.id] = altp.performances[crit.id]
                elif crit_min[crit.id]*d > altp(crit.id)*d:
                    crit_min[crit.id] = altp.performances[crit.id]

                if crit_max.has_key(crit.id) is False:
                    crit_max[crit.id] = altp.performances[crit.id]
                elif crit_max[crit.id]*d < altp(crit.id)*d:
                    crit_max[crit.id] = altp.performances[crit.id]

        b1 = AlternativePerformances('b1', {})
        for crit in self.criteria:
            b1.performances[crit.id] = (crit_max[crit.id]
                                        - crit_min[crit.id]) / 2

        self.balternatives = Alternatives([Alternative('b1', 'b1')])
        self.bpt = PerformanceTable([b1])
        self.cbox_mrsort.setChecked(True)
        self.cbox_noveto.setChecked(True)

        # Categories Profiles
        self.categories = generate_categories(len(self.bpt), prefix = "")
        self.cat_profiles = generate_categories_profiles(self.categories)

        self.lbda = 0.75

    def on_button_loadlayer_pressed(self):
        index = self.combo_layer.currentIndex()
        map_canvas = self.iface.mapCanvas()
        try:
            self.layer = criteria_layer(map_canvas.layer(index))
            self.__clear_tables()
            self.__loadlayer()
            self.__enable_buttons()
        except:
            traceback.print_exc(sys.stderr)
            QtGui.QMessageBox.information(None, "Error",
                                          "Cannot load specified layer")
            return

    def __clear_tables(self):
        self.table_criteria.reset_table()
        self.table_prof.reset_table()
        self.table_indiff.reset_table()
        self.table_pref.reset_table()
        self.table_veto.reset_table()

    def same_pq_thresholds_for_all_profiles(self):
        if self.ppt:
            p = set(self.ppt.values())
            if len(p) > 1:
                return False

        if self.qpt:
            q = set(self.qpt.values())
            if len(q) > 1:
                return False

        return True

    def on_cbox_noveto_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            index = self.tab_thresholds.indexOf(self.tab_veto)
            self.tab_thresholds.removeTab(index)
            self.vpt = None
        else:
            self.tab_thresholds.insertTab(2, self.tab_veto, "Veto")

            if self.cbox_samethresholds.isChecked() is True:
                self.set_same_threshold_for_all_profiles(self.vpt,
                                                         self.table_veto)
            else:
                self.set_one_threshold_per_profile(self.vpt,
                                                   self.table_veto)

    def on_cbox_mrsort_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            index = self.tab_thresholds.indexOf(self.tab_indiff)
            self.tab_thresholds.removeTab(index)
            intex = self.tab_thresholds.indexOf(self.tab_pref)
            self.tab_thresholds.removeTab(index)
            self.qpt = None
            self.ppt = None
        else:
            self.tab_thresholds.insertTab(0, self.tab_indiff,
                                          "Indifference")
            self.tab_thresholds.insertTab(1, self.tab_pref, "Preference")

            if self.cbox_samethresholds.isChecked() is True:
                self.set_same_threshold_for_all_profiles(self.qpt,
                                                         self.table_indiff)
                self.set_same_threshold_for_all_profiles(self.ppt,
                                                         self.table_pref)
            else:
                self.set_one_threshold_per_profile(self.qpt,
                                                   self.table_indiff)
                self.set_one_threshold_per_profile(self.ppt,
                                                   self.table_pref)

    def set_same_threshold_for_all_profiles(self, pt, table):
        table.remove_all()

        if pt and len(pt) > 0:
            bp = next(pt.itervalues())
        else:
            bp = AlternativePerformances('b', {c: None \
                                               for c in self.criteria})

        bp.id = 'b'
        pt = PerformanceTable([bp])

        table.add(Alternative('b'), bp)

    def set_one_threshold_per_profile(self, pt, table):
        table.remove_all()

        if pt and len(pt) > 0:
            bp = next(pt.itervalues())
        else:
            bp = AlternativePerformances('b', {c: None \
                                               for c in self.criteria})

        pt = PerformanceTable([])
        for b in self.balternatives:
            bp2 = bp.copy()
            bp2.id = b.id
            pt.append(bp2)

        table.add_pt(self.balternatives, pt)

    def on_cbox_samethresholds_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.set_same_threshold_for_all_profiles(self.qpt,
                                                     self.table_indiff)
            self.set_same_threshold_for_all_profiles(self.ppt,
                                                     self.table_pref)

            self.set_same_threshold_for_all_profiles(self.vpt,
                                                     self.table_veto)
        else:
            self.set_one_threshold_per_profile(self.qpt,
                                               self.table_indiff)
            self.set_one_threshold_per_profile(self.ppt,
                                               self.table_pref)

            self.set_one_threshold_per_profile(self.vpt,
                                               self.table_veto)

    def __update_graph(self):
        lbda = self.spinbox_cutlevel.value()
        model = ElectreTri(self.criteria, self.cv, self.bpt, lbda,
                           self.cat_profiles, self.vpt, self.qpt, self.ppt)
        worst = self.pt.get_worst(self.criteria)
        best = self.pt.get_best(self.criteria)
        criteria_order = [c.id for c in self.criteria]
        graph = QGraphicsSceneEtri(model, worst, best,
                                   self.graph_plot.size(),
                                   criteria_order)
        self.graph_plot.setScene(graph)
        self.graph_plot2.setScene(graph)

    def __loadlayer(self):
        self.layer_loaded = False

        # References to map criteria and alternatives
        self.criteria = self.layer.criteria
        self.alternatives = self.layer.alternatives
        self.pt = self.layer.pt

        try:
            xmcda_file = os.path.splitext(str(self.layer.layer.source()))[0] \
                            + ".xmcda"
            self.__load_from_xmcda(xmcda_file)
        except:
            self.__generate_first_profile()

        self.table_criteria.add_criteria(self.criteria, self.cv)
        self.table_prof.add_criteria(self.criteria)

        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

        self.table_prof.add_pt(self.balternatives, self.bpt)
        self.label_ncategories.setText("%d" % len(self.bpt))

        if not self.qpt and not self.ppt:
            self.cbox_mrsort.setChecked(True)
        elif self.same_pq_thresholds_for_all_profiles():
            self.cbox_samethresholds.setChecked(True)
        else:
            self.table_indiff.add_pt(self.balternatives, self.qpt)
            self.table_pref.add_pt(self.balternatives, self.ppt)

        if self.vpt:
            self.table_veto.add_pt(self.balternatives, self.ppt)
        else:
            self.cbox_noveto.setChecked(True)
            self.tab_thresholds.setTabEnabled(2, False)

        if self.same_pq_thresholds_for_all_profiles():
            self.cbox_samethresholds.setChecked(True)

        self.spinbox_cutlevel.setValue(self.lbda)

        self.__update_graph()

        self.layer_loaded = True

    def __enable_buttons(self):
        self.button_add_profile.setEnabled(True)
        self.button_del_profile.setEnabled(True)
        self.button_generate.setEnabled(True)
        self.button_chooserefs.setEnabled(True)
        self.button_loadxmcda.setEnabled(True)
        self.button_savexmcda.setEnabled(True)

    def __criterion_state_changed(self, criterion):
        self.table_prof.disable_criterion(criterion)
        self.table_indiff.disable_criterion(criterion)
        self.table_pref.disable_criterion(criterion)
        self.table_veto.disable_criterion(criterion)

    def on_button_add_profile_pressed(self):
        name = "b%d" % (len(self.bpt) + 1)
        b = Alternative(name, name)
        ap = self.bpt["b%d" % len(self.bpt)].copy()
        ap.id = name
        self.balternatives.append(b)
        self.bpt.append(ap)
        self.table_prof.add(b, ap)
        self.label_ncategories.setText("%d" % len(self.bpt))

    def on_button_del_profile_pressed(self):
        name = "b%d" % len(self.bpt)
        b = self.balternatives[name]
        self.table_prof.remove(b.id)
        self.balternatives.remove(b.id)
        self.bpt.remove(b.id)
        self.label_ncategories.setText("%d" % len(self.bpt))

    def on_button_generate_pressed(self):
        lbda = self.spinbox_cutlevel.value()
        model = ElectreTri(self.criteria, self.cv, self.bpt, lbda,
                           self.cat_profiles, self.vpt, self.qpt, self.ppt)

        if self.combo_procedure.currentIndex() == COMBO_PROC_OPTIMIST:
            aa = model.optimist(self.pt)
        else:
            aa = model.pessimist(self.pt)

        (f, encoding) = saveDialog(self)
        if f is None or encoding is None:
            return

        generate_decision_map(self.layer.layer, aa, f, encoding)

        if self.iface is not None:
            addtocDialog(self, f, len(model.bpt))

    def on_table_prof_cellChanged(self, row, col):
        if self.layer_loaded is False:
            return

        self.__update_graph()

if __name__ == "__main__":
    from PyQt4 import QtGui
    from qgis.core import *

    QgsApplication.setPrefixPath("/usr/", True)
    QgsApplication.initQgis()

    layer = QgsVectorLayer('/home/oso/dev/qgis-etri/tests/data/loulouka/criteria.shp',
                           'criteria', 'ogr')
    if not layer.isValid():
        print("Layer failed to load!")
        sys.exit(1)

    app = QtGui.QApplication(sys.argv)
    window = main_window(layer = layer)
    window.show()
    app.exec_()
