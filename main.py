import os, sys, traceback
from xml.etree import ElementTree
from PyQt4 import QtCore, QtGui
from ui.main_window import Ui_main_window 
from layer import criteria_layer
from mcda.electre_tri import electre_tri
from mcda.types import criteria, performance_table, alternatives
from mcda.types import alternative, alternative_performances

# Method used to update criteria from XMCDA file

class main_window(QtGui.QMainWindow, Ui_main_window):

    def __init__(self, iface):
        super(QtGui.QMainWindow, self).__init__(iface.mainWindow())
        self.setupUi(self)

        self.iface = iface

        self.__update_layer_list(iface.mapCanvas())
        self.table_criteria.connect(self.table_criteria,
                                    QtCore.SIGNAL("criterion_state_changed"),
                                    self.__criterion_state_changed)

    def __update_layer_list(self, map_canvas):
        if map_canvas == None:
            return

        for i in range(map_canvas.layerCount()):
            layer = map_canvas.layer(i)
            self.combo_layer.addItem(layer.name())

    def __update_criteria(self, criteria):
        for c in self.criteria:
            if criteria.has_criterion(c.id): 
                c2 = criteria(c.id)
                c.disabled = c2.disabled
                c.direction = c2.direction
                if c2.weight is not None:
                    c.weight = c2.weight
                else:
                    c.weight = 0
                c.thresholds = c2.thresholds
            else:
                c.disabled = True
                c.weight = 0

    def __load_from_xmcda(self, xmcda_file):
        tree = ElementTree.parse(xmcda_file)
        root = tree.getroot()
        ElementTree.dump(root)
        xmcda_crit = root.find('.//criteria')
        xmcda_critval = root.find('.//criteriaValues')
        xmcda_b = root.find('.//alternatives')
        xmcda_ptb = root.find('.//performanceTable')
        xmcda_lbda = root.find('.//methodParameters')

        c = criteria()
        c.from_xmcda(xmcda_crit, xmcda_critval)
        self.__update_criteria(c)

#        b = alternatives()
#        b.from_xmcda(xmcda_b)
#
#        ptb = performance_table()
#        ptb.from_xmcda(xmcda_ptb)

    def __generate_first_profile(self):
        crit_min = {}
        crit_max = {}
        for altp in self.pt:
            for crit in self.criteria:
                d = crit.direction
                print altp
                if crit_min.has_key(crit.id) is False:
                    crit_min[crit.id] = altp(crit.id)
                elif crit_min[crit.id]*d > altp(crit.id)*d:
                    crit_min[crit.id] = altp(crit.id)

                if crit_max.has_key(crit.id) is False:
                    crit_max[crit.id] = altp(crit.id)
                elif crit_max[crit.id]*d < altp(crit.id)*d:
                    crit_max[crit.id] = altp(crit.id)

        b1 = alternative_performances('b1', {})
        for crit in self.criteria:
            b1.performances[crit.id] = (crit_max[crit.id]-crit_min[crit.id])/2
        self.balternatives = alternatives([alternative('b1', 'b1')])
        self.bpt = performance_table([b1])

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
            QtGui.QMessageBox.information(None, "Error", "Cannot load specified layer")
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

        self.__generate_first_profile()

        xmcda_file = os.path.splitext(str(self.layer.layer.source()))[0] \
                        + ".xmcda"
        self.__load_from_xmcda(xmcda_file)

        self.table_criteria.add(self.criteria)
        self.table_prof.add_criteria(self.criteria)
        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

        self.table_prof.add_pt(self.balternatives, self.bpt)

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
