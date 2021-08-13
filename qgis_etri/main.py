import os, sys, traceback
from xml.etree import ElementTree
from qgis.PyQt import QtCore
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import QApplication, QDialog, QFileDialog, QInputDialog, QMessageBox
from itertools import product
from qgis_etri.ui.main_window import Ui_main_window
from qgis_etri.ui.inference_results import Ui_inference_results
from qgis_etri.layer import criteria_layer
from qgis_etri.mcda.electre_tri import ElectreTri
from qgis_etri.mcda.types import Criteria, CriteriaValues, CriterionValue
from qgis_etri.mcda.types import PerformanceTable, Alternatives
from qgis_etri.mcda.types import Alternative, AlternativePerformances
from qgis_etri.mcda.types import AlternativeAssignment, AlternativesAssignments
from qgis_etri.mcda.types import Thresholds, Threshold
from qgis_etri.mcda.generate import generate_categories
from qgis_etri.mcda.generate import generate_categories_profiles
from qgis_etri.qgis_utils import generate_decision_map, saveDialog, addtocDialog
from qgis_etri.graphic import QGraphicsSceneEtri
from qgis_etri.xmcda import submit_problem, request_solution

XMCDA_URL = 'http://www.decision-deck.org/2009/XMCDA-2.0.0'
ElementTree.register_namespace('xmcda', XMCDA_URL)
XMCDA_ETRIBMINFERENCE_URL = 'http://webservices.decision-deck.org/soap/ElectreTriBMInference-PyXMCDA.py'

COMBO_PROC_PESSIMIST = 0
COMBO_PROC_OPTIMIST = 1

COMBO_INFERENCE_GLOBAL = 0
COMBO_INFERENCE_PROFILES = 1
COMBO_INFERENCE_WEIGHTS = 2

class InferenceDialog(QDialog, Ui_inference_results):

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class main_window(QDialog, Ui_main_window):

    def __init__(self, iface = None, layer = None):
        QDialog.__init__(self)
        Ui_main_window.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)

        self.iface = iface

        if iface is not None:
            self.__update_layer_list(iface.mapCanvas())
        elif layer:
            self.layer = criteria_layer(layer)
            self.__loadlayer()
            self.__reset_buttons()
            self.button_show.setVisible(False)
            self.button_zoom.setVisible(False)

        self.table_criteria.criterion_state_changed.connect(self.__criterion_state_changed)

    def closeEvent(self, event):
        val = QMessageBox.question(
            self, "ELECTRE TRI",
            "Close ELECTRE TRI?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if val == QMessageBox.No:
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
        tree = ElementTree.parse(xmcda_file)
        root = tree.getroot()
#        ElementTree.dump(root)
        xmcda_formatversion = root.find('.//formatversion')
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
                qpt = PerformanceTable(id = 'q')
                qpt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'p':
                ppt = PerformanceTable(id = 'p')
                ppt.from_xmcda(xmcda)
            elif xmcda.get('id') == 'v':
                vpt = PerformanceTable(id = 'v')
                vpt.from_xmcda(xmcda)

        if qpt is not None and len(qpt) == 0 and len(ppt) > 0:
            qpt = ppt.copy()
            qpt.id = "q"

        if ppt is not None and len(ppt) == 0 and len(qpt) > 0:
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
                                              prefix = "")
        self.cat_profiles = generate_categories_profiles(self.categories)

    def __generate_initial_model(self):
        crit_min = {}
        crit_max = {}
        for altp in self.pt:
            for crit in self.criteria:
                d = crit.direction
                if (crit.id in crit_min) is False:
                    crit_min[crit.id] = altp.performances[crit.id]
                elif crit_min[crit.id]*d > altp(crit.id)*d:
                    crit_min[crit.id] = altp.performances[crit.id]

                if (crit.id in crit_max) is False:
                    crit_max[crit.id] = altp.performances[crit.id]
                elif crit_max[crit.id]*d < altp(crit.id)*d:
                    crit_max[crit.id] = altp.performances[crit.id]

        self.cv = CriteriaValues()
        b1 = AlternativePerformances('b1', {})
        for crit in self.criteria:
            b1.performances[crit.id] = (crit_max[crit.id]
                                        - crit_min[crit.id]) / 2
            cv = CriterionValue(crit.id, 1)
            self.cv.append(cv)

        self.balternatives = Alternatives([Alternative('b1', 'b1')])
        self.bpt = PerformanceTable([b1])
        self.cbox_mrsort.setChecked(True)
        self.cbox_noveto.setChecked(True)

        # Categories Profiles
        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix = "")
        self.cat_profiles = generate_categories_profiles(self.categories)

        self.lbda = 0.75

    def on_button_loadlayer_pressed(self):
        index = self.combo_layer.currentIndex()
        map_canvas = self.iface.mapCanvas()
        try:
            self.layer = criteria_layer(map_canvas.layer(index))
            self.__clear_tables()
            self.button_zoom.setEnabled(False)
            self.button_show.setEnabled(False)
            self.button_infer.setEnabled(False)
            self.__loadlayer()
            self.__reset_buttons()
        except:
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
        self.table_refs.reset_table()

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
        if state == QtCore.Qt.Checked:
            index = self.tab_thresholds.indexOf(self.tab_veto)
            self.tab_thresholds.removeTab(index)
            self.table_veto.remove_all()
            self.vpt = None
        else:
            self.tab_thresholds.insertTab(2, self.tab_veto, "Veto")

            self.vpt = PerformanceTable(id = 'v')
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
            self.table_indiff.remove_all()
            self.table_pref.remove_all()
            self.qpt = None
            self.ppt = None
        else:
            self.tab_thresholds.insertTab(0, self.tab_indiff,
                                          "Indifference")
            self.tab_thresholds.insertTab(1, self.tab_pref, "Preference")

            self.qpt = PerformanceTable(id = 'q')
            self.ppt = PerformanceTable(id = 'p')
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
            bp = next(pt.values())
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
            bp = next(pt.values())
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
        # References to map criteria and alternatives
        self.criteria = self.layer.criteria
        self.alternatives = self.layer.alternatives
        self.pt = self.layer.pt

        try:
            xmcda_file = os.path.splitext(str(self.layer.layer.source()))[0] \
                            + ".xmcda"
            self.__load_from_xmcda(xmcda_file)
        except:
            traceback.print_exc(file=sys.stderr)
            self.__generate_initial_model()

        self.__fill_model_tables()

    def __fill_model_tables(self):
        self.layer_loaded = False

        self.table_criteria.add_criteria(self.criteria, self.cv)
        self.table_prof.add_criteria(self.criteria)

        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

        self.table_prof.add_pt(self.balternatives, self.bpt)
        self.label_ncategories.setText("%d" % (len(self.bpt) + 1))

        if self.same_pqv_thresholds_for_all_profiles() is True:
            self.cbox_samethresholds.setChecked(True)
            balternatives = Alternatives([Alternative('b')])
        else:
            balternatives = self.balternatives

        if self.qpt is None and self.ppt is None:
            self.cbox_mrsort.setChecked(True)
        else:
            self.table_indiff.add_pt(balternatives, self.qpt)
            self.table_pref.add_pt(balternatives, self.ppt)

        if self.vpt is None:
           self.cbox_noveto.setChecked(True)
        else:
            self.table_veto.add_pt(balternatives, self.vpt)

        self.spinbox_cutlevel.setValue(self.lbda)

        self.__update_graph()

        self.layer_loaded = True

    def __reset_buttons(self):
        self.button_add_profile.setEnabled(True)
        self.button_del_profile.setEnabled(True)
        self.button_generate.setEnabled(True)
        self.button_chooseassign.setEnabled(True)
        self.button_loadxmcda.setEnabled(True)
        self.button_savexmcda.setEnabled(True)
        self.button_infer.setEnabled(False)
        self.button_zoom.setEnabled(False)
        self.button_show.setEnabled(False)

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
                                              prefix = "")
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
            self.table_indiff.remove(b.id)
            self.table_pref.remove(b.id)
            self.table_veto.remove(b.id)
            self.qpt.remove(b.id)
            self.ppt.remove(b.id)
            self.vpt.remove(b.id)

        self.label_ncategories.setText("%d" % (len(self.bpt) + 1))
        self.categories = generate_categories(len(self.bpt) + 1,
                                              prefix = "")
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
                qpt = PerformanceTable(id = 'q')
                ppt = PerformanceTable(id = 'p')
                for i in range(len(self.bpt)):
                    qp = next(self.qpt.values()).copy()
                    pp = next(self.ppt.values()).copy()
                    name = "b%d" % (i + 1)
                    qp.id, pp.id = name, name
                    qpt.append(qp), ppt.append(pp)
            else:
                qpt = None
                ppt = None

            if self.cbox_noveto.isChecked() is False:
                vpt = PerformanceTable(id = 'v')
                for i in range(len(self.bpt)):
                    vp = next(self.vpt.values()).copy()
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
                                   QFileDialog.AcceptSave)
        if f is None or encoding is None:
            return

        generate_decision_map(self.layer.layer, aa, f, encoding, self.cbox_allfields.isChecked())
        self.save_to_xmcda(os.path.splitext(f)[0] + ".xmcda")

        if self.iface is not None:
            addtocDialog(self, f, len(model.bpt))

    def on_table_prof_cellChanged(self, row, col):
        if self.layer_loaded is False:
            return

        self.__update_graph()

    def lambda_to_xmcda(self, lbda):
        root = ElementTree.Element('methodParameters')
        xmcda = ElementTree.SubElement(root, 'parameter')
        xmcda.set('name', 'lambda')
        xmcda = ElementTree.SubElement(xmcda, 'value')
        xmcda = ElementTree.SubElement(xmcda, 'real')
        xmcda.text = str(lbda)
        return root

    def on_button_savexmcda_pressed(self):
        (f, encoding) = saveDialog(self, "Save MCDA model",
                                   "XMCDA files (*.xmcda)", "xmcda",
                                   QFileDialog.AcceptSave)
        if f is None:
            return

        self.save_to_xmcda(f)

    def save_to_xmcda(self, filepath):
        xmcda = ElementTree.Element("{%s}XMCDA" % XMCDA_URL)
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
        buf = ElementTree.tostring(xmcda, encoding="UTF-8", method="xml")
        f.write(buf)
        f.close()

    def on_button_loadxmcda_pressed(self):
        (f, encoding) = saveDialog(self, "Load MCDA model",
                                   "XMCDA files (*.xmcda)", "xmcda",
                                   QFileDialog.AcceptOpen)
        if f is None:
            return

        try:
            self.__load_from_xmcda(f)
        except:
            traceback.print_exc(file=sys.stderr)
            QMessageBox.information(None, "Error",
                                          "Cannot load XMCDA data")
            return

        self.__clear_tables()
        self.button_zoom.setEnabled(False)
        self.button_show.setEnabled(False)
        self.button_infer.setEnabled(False)
        self.__fill_model_tables()

    @staticmethod
    def generate_category_colors(ncat):
        return {
            str(i): QColor(0, 255 - 220 * i / ncat, 0)
            for i in range(1, ncat+1)
        }

    def __generate_category_colors(self):
        ncat = len(self.bpt) + 1
        self.category_colors = self.generate_category_colors(ncat)

    def on_button_chooseassign_pressed(self):
        items = [c.id for c in self.criteria if c.disabled is True]
        if len(items) < 1:
            QMessageBox.information(None, "Error",
                                          "No assignment column")
            return

        item, ok = QInputDialog.getItem(self,
                                        "Select assignments column",
                                        "Column:", items, 0, False)
        if ok is False:
            return

        try:
            cid = item.toString()
        except:
            cid = str(item)

        ncat = len(self.bpt) + 1
        pt, aa = PerformanceTable(), AlternativesAssignments()
        for ap in self.pt:
            perf = int(ap.performances[cid])
            if perf > 0 and perf < (ncat + 1):
                pt.append(ap)
                aa.append(AlternativeAssignment(ap.id, str(perf)))

        if len(pt) < 1:
            QMessageBox.information(None, "Error",
                                    "No assignments examples found")
            return

        self.a_ref = Alternatives([Alternative(a.id) for a in aa])
        self.pt_ref = pt
        self.aa_ref = aa

        a = Alternatives([Alternative(aid) for aid in pt.keys()])

        self.table_refs.reset_table()

        self.table_refs.add_criteria(self.criteria)
        self.table_refs.add_pt(a, pt, False)
        self.__generate_category_colors()
        self.table_refs.add_assignments(aa, self.category_colors, True)

        self.button_zoom.setEnabled(True)
        self.button_show.setEnabled(True)

        self.button_infer.setEnabled(True)

    def __parse_xmcda_object(self, xmcda, tag, object_type):
        e = ElementTree.fromstring(str(xmcda))
        t = ElementTree.ElementTree(e)
        return object_type().from_xmcda(t.find(".//%s" % tag))

    def __parse_xmcda_lambda(self, xmcda):
        e = ElementTree.fromstring(str(xmcda))
        t = ElementTree.ElementTree(e)
        value = t.find('.//methodParameters/parameter/value/real')
        return float(value.text)

    def on_model_learned_accepted(self):
        for cid, cv in self.cv_learned.items():
            self.cv[cid].value = cv.value
        for bid, bp in self.bpt.items():
            bp.performances.update(self.bpt_learned[bid].performances)
        self.lbda = self.lbda_learned

        self.__clear_tables()
        self.button_zoom.setEnabled(False)
        self.button_show.setEnabled(False)
        self.button_infer.setEnabled(False)
        self.__fill_model_tables()
        self.cbox_samethresholds.setChecked(True)
        self.cbox_mrsort.setChecked(True)
        self.cbox_noveto.setChecked(True)

    def __show_model_learned(self, cv, bpt, lbda, a):
        dialog = InferenceDialog(self)
        dialog.setModal(True)
        self.accepted.connect(self.on_model_learned_accepted)
        dialog.show()

        model = ElectreTri(self.criteria, cv, bpt, lbda, self.cat_profiles)
        worst = self.pt.get_worst(self.criteria)
        best = self.pt.get_best(self.criteria)
        criteria_order = [c.id for c in self.criteria]
        graph = QGraphicsSceneEtri(model, worst, best,
                                   self.graph_plot.size(),
                                   criteria_order)
        dialog.graph_model.setScene(graph)
        dialog.label_lambda.setText("Lambda: %s" % str(lbda))

        a_incomp = Alternatives([aref for aref in self.a_ref
                                 if aref.id not in a.keys()])
        pt_incomp = PerformanceTable([ap for ap in self.pt_ref
                                      if ap.id in a_incomp.keys()])
        pt_comp = PerformanceTable([ap for ap in self.pt_ref
                                    if ap.id in a.keys()])

        dialog.table_comp.add_criteria(self.criteria)
        dialog.table_comp.add_pt(a, pt_comp)
        dialog.table_incomp.add_criteria(self.criteria)
        dialog.table_incomp.add_pt(a_incomp, pt_incomp)

    def on_inference_thread_finished(self, completed):
        try:
            self.cancelbox.close()
        except:
            pass

        if completed is False:
            return

        solution = self.inference_thread.solution

        try:
            msg = str(solution.messages)
        except:
            QMessageBox.information(None, "Error",
                                    "Invalid reply received, "
                                    "nothing received!")
            return

        xmcda_msg = ElementTree.ElementTree(ElementTree.fromstring(msg))
        if xmcda_msg.find(".//methodMessages") is None:
            QMessageBox.information(None, "Error",
                                    "Invalid reply received")
            return

        error = xmcda_msg.find(".//methodMessages/errorMessage/text")
        if error is not None:
            QMessageBox.information(None, "Error",
                                    "Webservice replied:\n" +
                                    error.text)
            return


        try:
            cv = self.__parse_xmcda_object(solution.crit_weights,
                                           "criteriaValues",
                                           CriteriaValues)
            bpt = self.__parse_xmcda_object(solution.reference_alts,
                                            "performanceTable",
                                            PerformanceTable)
            lbda = self.__parse_xmcda_lambda(getattr(solution, 'lambda'))
            a = self.__parse_xmcda_object(solution.compatible_alts,
                                          "alternatives", Alternatives)
        except:
            QMessageBox.information(None, "Error",
                                    "Cannot parse reply")
            return

        self.cv_learned = cv
        self.bpt_learned = bpt
        self.lbda_learned = lbda

        self.__show_model_learned(cv, bpt, lbda, a)

    def on_cancelbox_button_clicked(self, button):
        self.inference_thread.stop()

    def __xmcda_input(self, obj):
        xmcda = ElementTree.Element("{%s}XMCDA" % XMCDA_URL)
        xmcda.append(obj)
        return ElementTree.tostring(xmcda, encoding="UTF-8", method="xml")

    def __save_xmcda_files(self, xmcda):
        for name, xm in xmcda.items():
            f = open("/tmp/%s.xml" % name, "w")
            f.write(xm)
            f.close()

    def __generate_xmcda_input(self):
        # This ugly part is needed for the old version of the webservice
        # that doesn't handle correctly deactivated criteria
        criteria = self.criteria.get_active()
        pt_ref = self.pt_ref.copy()
        bpt = self.bpt.copy()
        for ap in pt_ref:
            for crit, value in ap.performances.items():
                if crit not in criteria.keys():
                    del ap.performances[crit]
        for ap in bpt:
            for crit, value in ap.performances.items():
                if crit not in criteria.keys():
                    del ap.performances[crit]

        xmcda = {}
        xmcda['alternatives'] = self.__xmcda_input(self.a_ref.to_xmcda())
        xmcda['criteria'] = self.__xmcda_input(criteria.to_xmcda())
        xmcda['categories'] = self.__xmcda_input(self.categories.to_xmcda())
        xmcda['perfs_table'] = self.__xmcda_input(pt_ref.to_xmcda())
        xmcda['assign'] = self.__xmcda_input(self.aa_ref.to_xmcda())
        self.__save_xmcda_files(xmcda)

        index = self.combo_inference.currentIndex()
        if index == COMBO_INFERENCE_PROFILES:
            lbda = self.spinbox_cutlevel.value()
            xmcda['crit_weights'] = self.cv.to_xmcda()
            xmcda['lambda'] = self.lambda_to_xmcda(lbda)
        elif index == COMBO_INFERENCE_WEIGHTS:
            xmcda['cat_profiles'] = self.cat_profiles.to_xmcda()
            xmcda['reference_alts'] = bpt.to_xmcda()

        return xmcda

    def on_button_infer_pressed(self):
        xmcda = self.__generate_xmcda_input()

        self.inference_thread = InferenceThread(xmcda, self)
        self.finished.connect(self.on_inference_thread_finished)
        self.inference_thread.start()

        self.cancelbox = QMessageBox(self)
        self.cancelbox.setWindowTitle('Please wait...')
        self.cancelbox.setText('Press cancel to stop inference')
        self.cancelbox.setStandardButtons(QMessageBox.Cancel)
        self.cancelbox.setModal(True)
        self.cancelbox.buttonClicked.connect(self.on_cancelbox_button_clicked)
        self.cancelbox.show()

    def on_button_zoom_pressed(self):
        if len(self.a_ref) < 1:
            return

        features = self.layer.get_features_ids(self.a_ref.keys())
        self.layer.layer.setSelectedFeatures(features)
        mc = self.iface.mapCanvas()
        rect = self.layer.layer.boundingBoxOfSelected()
        rect.scale(2)
        mc.setExtent(rect)
        mc.refresh()

    def on_button_show_pressed(self):
        if len(self.a_ref) < 1:
            return

        features = self.layer.get_features_ids(self.a_ref.keys())
        self.layer.layer.setSelectedFeatures(features)

class InferenceThread(QtCore.QThread):

    def __init__(self, xmcda_input, parent = None):
        super(InferenceThread, self).__init__(parent)
        self.stopped = False
        self.mutex = QtCore.QMutex()
        self.completed = False
        self.xmcda_input = xmcda_input

    def stop(self):
        try:
            self.mutex.lock()
            self.stopped = True
        finally:
            self.mutex.unlock()

    def is_stopped(self):
        try:
            self.mutex.lock()
            return self.stopped
        finally:
            self.mutex.unlock()

    def run(self):
        ticket = submit_problem(XMCDA_ETRIBMINFERENCE_URL,
                                self.xmcda_input)
        while True:
            solution = request_solution(XMCDA_ETRIBMINFERENCE_URL,
                                        ticket, 0)
            if self.is_stopped():
                break

            if solution:
                self.solution = solution
                self.completed = True
                break

            time.sleep(1)

        self.stop()
        self.finished.emit(self.completed)

if __name__ == "__main__":
    import sys
    # from qgis.PyQt import QtGui
    from qgis.core import *

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
    window = main_window(layer = layer)
    window.show()
    app.exec_()
