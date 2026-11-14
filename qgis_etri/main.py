import os
import sys
import traceback
from qgis.PyQt import QtCore
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from itertools import product
from qgis_etri.ui import Ui_main_window
from qgis_etri.layer import criteria_layer
from qgis_etri.mcda.electre_tri import ElectreTri
from qgis_etri.mcda.types import Criteria, CriteriaValues, CriterionValue
from qgis_etri.mcda.types import PerformanceTable, Alternatives
from qgis_etri.mcda.types import Alternative, AlternativePerformances
from qgis_etri.mcda.generate import generate_categories
from qgis_etri.mcda.xml_writer import Element, SubElement, tostring
from qgis_etri.mcda.generate import generate_categories_profiles
from qgis_etri.qgis_utils import generate_decision_map, saveDialog, addtocDialog
from qgis_etri.graphic import QGraphicsSceneEtri
from qgis_etri.xml_utils import safe_parse

XMCDA_URL = 'http://www.decision-deck.org/2009/XMCDA-2.0.0'

COMBO_PROC_PESSIMIST = 0
COMBO_PROC_OPTIMIST = 1


class main_window(QDialog, Ui_main_window):

    def __init__(self, iface=None, layer=None):
        QDialog.__init__(self)
        Ui_main_window.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.iface = iface
        self.layer_loaded = False

        if iface is not None:
            self.__update_layer_list(iface.mapCanvas())
        elif layer:
            self.layer = criteria_layer(layer)
            self.__loadlayer()
            self.__reset_buttons()

        self.table_criteria.criterion_state_changed.connect(self.__criterion_state_changed)

    def closeEvent(self, event):
        val = QMessageBox.question(
            self, "ELECTRE TRI",
            "Close ELECTRE TRI?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if val == QMessageBox.StandardButton.No:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

    def __update_layer_list(self, map_canvas):
        if map_canvas is None:
            return

        for i in range(map_canvas.layerCount()):
            layer = map_canvas.layer(i)
            self.combo_layer.addItem(layer.name())

    def __check_params_consistency(self, bpt, qpt, ppt, vpt):
        if len(bpt) < 1:
            raise Exception("Preference table has an invalid size")

        for i in range(1, len(bpt) + 1):
            altid = "b%d" % i

            if altid not in bpt.keys():
                raise Exception("Invalid profiles performance table")

            if qpt and len(qpt) > 1 and altid not in qpt:
                raise Exception("Invalid indifference performance table")

            if ppt and len(ppt) > 1 and altid not in ppt:
                raise Exception("Invalid preference performance table")

            if vpt and len(vpt) > 1 and altid not in vpt:
                raise Exception("Invalid veto performance table")

        if qpt and len(qpt) == 1 and "b" not in qpt:
            raise Exception("Invalid indifference performance table")

        if ppt and len(ppt) == 1 and "b" not in ppt:
            raise Exception("Invalid preference performance table")

        if vpt and len(vpt) == 1 and "b" not in vpt:
            raise Exception("Invalid veto performance table")

    def __load_from_xmcda(self, xmcda_file):
        tree = safe_parse(xmcda_file)
        root = tree.getroot()
        xmcda_crit = root.find('.//criteria')
        xmcda_critval = root.find('.//criteriaValues')
        xmcda_b = root.find('.//alternatives')
        xmcda_pt = root.findall('.//performanceTable')
        xmcda_lbda = root.find('.//methodParameters/parameter/value/real')

        # Update criteria direction
        criteria = Criteria().from_xmcda(xmcda_crit)
        for c in criteria:
            if c.id in self.criteria:
                self.criteria[c.id].disabled = c.disabled
                self.criteria[c.id].direction = c.direction

        # Remove criteria values that are not in the vector layer
        cvs = CriteriaValues()
        cvs.from_xmcda(xmcda_critval)
        for cv in cvs:
            if cv.id not in self.criteria:
                cvs.remove(cv.id)

        for c in self.criteria:
            # Disable criteria for which there are no weights
            if c.id not in cvs:
                c.disabled = True
                cvs.append(CriterionValue(c.id, 0))

        balternatives = Alternatives()
        balternatives.from_xmcda(xmcda_b)

        bpt = PerformanceTable()
        qpt, ppt, vpt = None, None, None

        for xmcda in xmcda_pt:
            if xmcda.get('id') is None:
                bpt.from_xmcda(xmcda)
                for bp, c in product(bpt, self.criteria.get_active()):
                    perfs = bp.performances
                    if c.id not in perfs or perfs[c.id] is None:
                        perfs[c.id] = 0
            elif xmcda.get('id') == 'q':
                qpt = PerformanceTable(id='q')
                qpt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'p':
                ppt = PerformanceTable(id='p')
                ppt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'v':
                vpt = PerformanceTable(id='v')
                vpt.from_xmcda(xmcda)

        # An empty threshold table is the same as a missing one
        if qpt is not None and len(qpt) == 0:
            qpt = None
        if ppt is not None and len(ppt) == 0:
            ppt = None
        if vpt is not None and len(vpt) == 0:
            vpt = None

        # The indifference and preference thresholds are enabled or
        # disabled together (MR-Sort checkbox). If only one of them is
        # given, use the same values for the other one.
        if qpt is None and ppt is not None:
            qpt = ppt.copy()
            qpt.id = "q"
        elif ppt is None and qpt is not None:
            ppt = qpt.copy()
            ppt.id = "p"

        lbda = float(xmcda_lbda.text)

        self.__check_params_consistency(bpt, qpt, ppt, vpt)

        # Everything is fine
        self.cv = cvs
        self.balternatives = balternatives
        self.bpt = bpt
        self.qpt = qpt
        self.ppt = ppt
        self.vpt = vpt
        self.lbda = lbda

        # Categories Profiles
        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix="")
        self.cat_profiles = generate_categories_profiles(self.categories)

    def __generate_initial_model(self):
        # Put the profile in the middle of the range of each criterion
        mins = self.pt.get_min().performances
        maxs = self.pt.get_max().performances

        self.cv = CriteriaValues()
        b1 = AlternativePerformances('b1', {})
        for crit in self.criteria:
            b1.performances[crit.id] = (mins[crit.id] + maxs[crit.id]) / 2
            cv = CriterionValue(crit.id, 1)
            self.cv.append(cv)

        self.balternatives = Alternatives([Alternative('b1', 'b1')])
        self.bpt = PerformanceTable([b1])
        self.cbox_mrsort.setChecked(True)
        self.cbox_noveto.setChecked(True)

        # Categories Profiles
        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix="")
        self.cat_profiles = generate_categories_profiles(self.categories)

        self.lbda = 0.75

    def on_button_loadlayer_pressed(self):
        index = self.combo_layer.currentIndex()
        map_canvas = self.iface.mapCanvas()
        try:
            self.layer = criteria_layer(map_canvas.layer(index))
            self.__clear_tables()
            self.__loadlayer()
            self.__reset_buttons()
        except Exception:
            traceback.print_exc(file=sys.stderr)
            QMessageBox.information(None, "Error",
                                          "Cannot load specified layer")
            return

    def __clear_tables(self):
        self.table_criteria.reset_table()
        self.table_prof.reset_table()
        self.table_indiff.reset_table()
        self.table_pref.reset_table()
        self.table_veto.reset_table()

    def same_pqv_thresholds_for_all_profiles(self):
        if self.ppt is not None:
            p = set(self.ppt.values())
            if len(p) > 1:
                return False

        if self.qpt is not None:
            q = set(self.qpt.values())
            if len(q) > 1:
                return False

        if self.vpt is not None:
            v = set(self.vpt.values())
            if len(v) > 1:
                return False

        return True

    def on_cbox_noveto_stateChanged(self, state):
        if self.cbox_noveto.isChecked():
            index = self.tab_thresholds.indexOf(self.tab_veto)
            self.tab_thresholds.removeTab(index)
            self.table_veto.remove_all()
            self.vpt = None
        else:
            self.tab_thresholds.insertTab(2, self.tab_veto, "Veto")

            if self.layer_loaded is False:
                # A model is being loaded, __fill_model_tables fills the
                # table with its veto thresholds
                return

            self.vpt = PerformanceTable(id='v')
            if self.cbox_samethresholds.isChecked() is True:
                self.set_same_threshold_for_all_profiles(self.vpt,
                                                         self.table_veto)
            else:
                self.set_one_threshold_per_profile(self.vpt,
                                                   self.table_veto)

    def on_cbox_mrsort_stateChanged(self, state):
        if self.cbox_mrsort.isChecked():
            index = self.tab_thresholds.indexOf(self.tab_indiff)
            self.tab_thresholds.removeTab(index)
            index = self.tab_thresholds.indexOf(self.tab_pref)
            self.tab_thresholds.removeTab(index)
            self.table_indiff.remove_all()
            self.table_pref.remove_all()
            self.qpt = None
            self.ppt = None
        else:
            self.tab_thresholds.insertTab(0, self.tab_indiff,
                                          "Indifference")
            self.tab_thresholds.insertTab(1, self.tab_pref, "Preference")

            if self.layer_loaded is False:
                # A model is being loaded, __fill_model_tables fills the
                # tables with its indifference and preference thresholds
                return

            self.qpt = PerformanceTable(id='q')
            self.ppt = PerformanceTable(id='p')
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
        if pt is None or self.layer_loaded is False:
            return

        table.remove_all()

        if pt and len(pt) > 0:
            bp = next(pt.itervalues())
        else:
            bp = AlternativePerformances('b', {c.id: None \
                                               for c in self.criteria})

        bp.id = 'b'
        pt.clear()
        pt.append(bp)

        table.add(Alternative('b'), bp)

    def set_one_threshold_per_profile(self, pt, table):
        if pt is None or self.layer_loaded is False:
            return

        table.remove_all()

        if pt and len(pt) > 0:
            bp = next(pt.itervalues())
        else:
            bp = AlternativePerformances('b', {c.id: None \
                                               for c in self.criteria})

        pt.clear()
        for b in self.balternatives:
            bp2 = bp.copy()
            bp2.id = b.id
            pt.append(bp2)

        table.add_pt(self.balternatives, pt)

    def on_cbox_samethresholds_stateChanged(self, state):
        if self.cbox_samethresholds.isChecked():
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
        # References to map criteria and alternatives
        self.criteria = self.layer.criteria
        self.alternatives = self.layer.alternatives
        self.pt = self.layer.pt

        try:
            xmcda_file = os.path.splitext(str(self.layer.layer.source()))[0] \
                            + ".xmcda"
            self.__load_from_xmcda(xmcda_file)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            self.__generate_initial_model()

        self.__fill_model_tables()

    def __fill_model_tables(self):
        self.layer_loaded = False

        self.table_criteria.add_criteria(self.criteria, self.cv)
        self.table_criteria.enable_export_fields(False)
        self.table_prof.add_criteria(self.criteria)

        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

        self.table_prof.add_pt(self.balternatives, self.bpt)
        self.label_ncategories.setText("%d" % (len(self.bpt) + 1))

        # The checkboxes keep the state of the previously loaded model,
        # set them in both directions. Their handlers do not touch the
        # threshold tables while layer_loaded is False.
        same_thresholds = self.same_pqv_thresholds_for_all_profiles()
        self.cbox_samethresholds.setChecked(same_thresholds)
        if same_thresholds:
            balternatives = Alternatives([Alternative('b')])
        else:
            balternatives = self.balternatives

        self.cbox_mrsort.setChecked(self.qpt is None and self.ppt is None)
        if self.qpt is not None:
            self.table_indiff.add_pt(balternatives, self.qpt)
            self.table_pref.add_pt(balternatives, self.ppt)

        self.cbox_noveto.setChecked(self.vpt is None)
        if self.vpt is not None:
            self.table_veto.add_pt(balternatives, self.vpt)

        self.spinbox_cutlevel.setValue(self.lbda)

        self.__update_graph()

        self.layer_loaded = True

    def __reset_buttons(self):
        self.button_add_profile.setEnabled(True)
        self.button_del_profile.setEnabled(True)
        self.button_generate.setEnabled(True)
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

        if self.cbox_samethresholds.isChecked() is False:
            if self.cbox_mrsort.isChecked() is False:
                qp = self.qpt["b%d" % len(self.qpt)].copy()
                pp = self.ppt["b%d" % len(self.ppt)].copy()
                qp.id, pp.id = name, name
                self.qpt.append(qp)
                self.ppt.append(pp)
                self.table_indiff.add(b, qp)
                self.table_pref.add(b, pp)

            if self.cbox_noveto.isChecked() is False:
                vp = self.vpt["b%d" % len(self.vpt)].copy()
                vp.id = name
                self.vpt.append(vp)
                self.table_veto.add(b, vp)

        self.label_ncategories.setText("%d" % (len(self.bpt) + 1))

        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix="")
        self.cat_profiles = generate_categories_profiles(self.categories)

    def on_button_del_profile_pressed(self):
        if len(self.bpt) == 1:
            QMessageBox.information(None, "Error",
                                    "Molel should have at least "
                                    "2 categories")
            return

        name = "b%d" % len(self.bpt)
        b = self.balternatives[name]
        self.table_prof.remove(b.id)
        self.balternatives.remove(b.id)
        self.bpt.remove(b.id)

        if self.cbox_samethresholds.isChecked() is False:
            # Threshold tables are None when MR-Sort or 'no veto' is
            # checked
            for pt, table in ((self.qpt, self.table_indiff),
                              (self.ppt, self.table_pref),
                              (self.vpt, self.table_veto)):
                if pt is not None:
                    table.remove(b.id)
                    pt.remove(b.id)

        self.label_ncategories.setText("%d" % (len(self.bpt) + 1))
        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix="")
        self.cat_profiles = generate_categories_profiles(self.categories)
        self.__update_graph()

    def on_button_generate_pressed(self):
        active_criteria = self.criteria.get_active()
        if self.bpt.is_complete(active_criteria.keys()) is False:
            QMessageBox.information(None, "Error",
                                          "Profile table is incomplete")
            return

        if self.cbox_samethresholds.isChecked() is True:
            if self.cbox_mrsort.isChecked() is False:
                qpt = PerformanceTable(id='q')
                ppt = PerformanceTable(id='p')
                for i in range(len(self.bpt)):
                    qp = next(self.qpt.itervalues()).copy()
                    pp = next(self.ppt.itervalues()).copy()
                    name = "b%d" % (i + 1)
                    qp.id, pp.id = name, name
                    qpt.append(qp), ppt.append(pp)
            else:
                qpt = None
                ppt = None

            if self.cbox_noveto.isChecked() is False:
                vpt = PerformanceTable(id='v')
                for i in range(len(self.bpt)):
                    vp = next(self.vpt.itervalues()).copy()
                    vp.id = "b%d" % (i + 1)
                    vpt.append(vp)
            else:
                vpt = None
        else:
            qpt = self.qpt
            ppt = self.ppt
            vpt = self.vpt

        lbda = self.spinbox_cutlevel.value()
        model = ElectreTri(self.criteria, self.cv, self.bpt, lbda,
                           self.cat_profiles, vpt, qpt, ppt)

        if self.combo_procedure.currentIndex() == COMBO_PROC_OPTIMIST:
            aa = model.optimist(self.pt)
        else:
            aa = model.pessimist(self.pt)

        (f, encoding) = saveDialog(self, "Save output shapefile",
                                   "Shapefiles (*.shp)", "shp",
                                   QFileDialog.AcceptMode.AcceptSave)
        if f is None or encoding is None:
            return

        export_fields = []
        if self.cbox_allfields.isChecked():
            export_fields = self.table_criteria.get_export_fields()
            print(export_fields)
        generate_decision_map(self.layer.layer, aa, f, encoding, export_fields)
        self.save_to_xmcda(os.path.splitext(f)[0] + ".xmcda")

        if self.iface is not None:
            addtocDialog(self, f, len(model.bpt))

    def on_table_prof_cellChanged(self, row, col):
        if self.layer_loaded is False:
            return

        self.__update_graph()

    def lambda_to_xmcda(self, lbda):
        root = Element('methodParameters')
        xmcda = SubElement(root, 'parameter')
        xmcda.set('name', 'lambda')
        xmcda = SubElement(xmcda, 'value')
        xmcda = SubElement(xmcda, 'real')
        xmcda.text = str(lbda)
        return root

    def on_button_savexmcda_pressed(self):
        (f, encoding) = saveDialog(self, "Save MCDA model",
                                   "XMCDA files (*.xmcda)", "xmcda",
                                   QFileDialog.AcceptMode.AcceptSave)
        if f is None:
            return

        self.save_to_xmcda(f)

    def save_to_xmcda(self, filepath):
        xmcda = Element("xmcda:XMCDA", {"xmlns:xmcda": XMCDA_URL})
        xmcda.append(self.criteria.to_xmcda())
        xmcda.append(self.cv.to_xmcda())
        xmcda.append(self.balternatives.to_xmcda())
        xmcda.append(self.bpt.to_xmcda())
        xmcda.append(self.lambda_to_xmcda(self.spinbox_cutlevel.value()))

        if self.qpt:
            xmcda.append(self.qpt.to_xmcda())

        if self.ppt:
            xmcda.append(self.ppt.to_xmcda())

        if self.vpt:
            xmcda.append(self.vpt.to_xmcda())

        f = open(filepath, "wb")
        buf = tostring(xmcda)
        f.write(buf)
        f.close()

    def on_button_loadxmcda_pressed(self):
        (f, encoding) = saveDialog(self, "Load MCDA model",
                                   "XMCDA files (*.xmcda)", "xmcda",
                                   QFileDialog.AcceptMode.AcceptOpen)
        if f is None:
            return

        try:
            self.__load_from_xmcda(f)
        except Exception:
            traceback.print_exc(file=sys.stderr)
            QMessageBox.information(None, "Error",
                                          "Cannot load XMCDA data")
            return

        self.__clear_tables()
        self.__fill_model_tables()

    def on_button_select_all_pressed(self):
        self.table_criteria.set_all_criteria(True)

    def on_button_select_none_pressed(self):
        self.table_criteria.set_all_criteria(False)

    def on_button_clone_selection_pressed(self):
        self.table_criteria.clone_selection()

    def on_cbox_allfields_stateChanged(self, state):
        self.table_criteria.enable_export_fields(
            self.cbox_allfields.isChecked())


if __name__ == "__main__":
    # from qgis.PyQt import QtGui
    from qgis.core import QgsApplication, QgsVectorLayer

    if len(sys.argv) != 2:
        print("usage: %s map.shp" % sys.argv[0])
        sys.exit(1)

    if os.path.isfile(sys.argv[1]) is False:
        print("file %s, doesn't exist" % sys.argv[1])
        sys.exit(1)

    QgsApplication.setPrefixPath("/usr/", True)
    QgsApplication.initQgis()

    layer = QgsVectorLayer('/home/oso/dev/qgis-etri/tests/data/loulouka/criteria.shp',
                           'criteria', 'ogr')
    if not layer.isValid():
        print("Failed to load layer!")
        sys.exit(1)

    app = QApplication(sys.argv)
    window = main_window(layer=layer)
    window.show()
    app.exec()
