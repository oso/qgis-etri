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

# Method used to update criteria from XMCDA file

class main_window(QtGui.QDialog, Ui_main_window):

    def __init__(self, iface):
        QtGui.QDialog.__init__(self)
        Ui_main_window.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)

        self.iface = iface

        self.__update_layer_list(iface.mapCanvas())
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
#        for c in self.criteria:
#            if criteria.has_criterion(c.id):
#            if c.id in self.criteria:
#                c2 = Criteria(c.id)
#                c.disabled = c2.disabled
#                c.direction = c2.direction
#                if c2.weight is not None:
#                    c.weight = c2.weight
#                else:
#                    c.weight = 0
#                c.thresholds = c2.thresholds
#            else:
#                c.disabled = True
#                c.weight = 0

    def __update_profiles(self, alternatives, pt):
        pass

    def __load_from_xmcda(self, xmcda_file):
        tree = ElementTree.parse(xmcda_file)
        root = tree.getroot()
        ElementTree.dump(root)
        xmcda_crit = root.find('.//criteria')
        xmcda_critval = root.find('.//criteriaValues')
        xmcda_b = root.find('.//alternatives')
        xmcda_bpt = root.find('.//performanceTable')
        xmcda_lbda = root.find('.//methodParameters')

        self.criteria = Criteria()
        self.criteria.from_xmcda(xmcda_crit)

        self.cv = CriteriaValues()
        self.cv.from_xmcda(xmcda_critval)

        self.balternatives = Alternatives()
        self.balternatives.from_xmcda(xmcda_b)

        self.bpt = PerformanceTable()
        self.bpt.from_xmcda(xmcda_bpt)

    def __generate_first_profile(self):
        crit_min = {}
        crit_max = {}
        for altp in self.pt:
            for crit in self.criteria:
                d = crit.direction
#                print altp
                if crit_min.has_key(crit.id) is False:
                    crit_min[crit.id] = altp(crit.id)
                elif crit_min[crit.id]*d > altp(crit.id)*d:
                    crit_min[crit.id] = altp(crit.id)

                if crit_max.has_key(crit.id) is False:
                    crit_max[crit.id] = altp(crit.id)
                elif crit_max[crit.id]*d < altp(crit.id)*d:
                    crit_max[crit.id] = altp(crit.id)

        b1 = AlternativePerformances('b1', {})
        for crit in self.criteria:
            b1.performances[crit.id] = (crit_max[crit.id]
                                        - crit_min[crit.id]) / 2
            q = Threshold('q', 'q', Constant(None, 0))
            p = Threshold('p', 'p', Constant(None, 0))
            v = Threshold('v', 'v', Constant(None, None))
            crit.thresholds = Thresholds([q, p, v])

        self.balternatives = Alternatives([Alternative('b1', 'b1')])
        self.bpt = PerformanceTable([b1])

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
            self.__generate_first_profile()

        self.table_criteria.add_criteria(self.criteria, self.cv)
        self.table_prof.add_criteria(self.criteria)

        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

        self.table_prof.add_pt(self.balternatives, self.bpt)

        thresholds = next(self.criteria.itervalues()).thresholds
        if thresholds:
            if thresholds.has_threshold('v'):
                self.cbox_samethresholds.setChecked(True)
                self.table_indiff.add_threshold('q', 'q')
                self.table_pref.add_threshold('p', 'p')
                self.table_veto.add_threshold('v', 'v')
            else:
                for i in range(1, len(self.balternatives) + 1):
                    ts_name = "q%d" % (i + 1)
                    self.table_indiff.add_threshold("q%d" % i , "q%d" % i)
                    self.table_pref.add_threshold("p%d" % i , "p%d" % i)
                    self.table_veto.add_threshold("v%d" % i , "v%d" % i)
        else:
            self.cbox_samethresholds.setChecked(True)
            self.cbox_sameqp.setChecked(True)
            self.cbox_noveto.setChecked(True)

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
