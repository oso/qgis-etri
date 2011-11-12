import os
from xml.etree import ElementTree
from PyQt4 import QtCore, QtGui
from ui.main_window import Ui_main_window 
from layer import criteria_layer
from mcda.electre_tri import electre_tri
from mcda.types import criteria, performance_table, alternatives

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

    def __load_from_xmcda(self, xmcda_file):
        tree = ElementTree.parse(xmcda_file)
        root = tree.getroot()
        ElementTree.dump(root)
        xmcda_crit = root.find('.//criteria')
        xmcda_ptb = root.find('.//performanceTable')
        xmcda_b = root.find('.//alternatives')
        xmcda_lbda = root.find('.//methodParameters')

        c = criteria()
        c.from_xmcda(xmcda_crit)
        ptb = performance_table()
        ptb.from_xmcda(xmcda_ptb)
        b = alternatives()
        b.from_xmcda(xmcda_b)

    def on_button_loadlayer_pressed(self):
        index = self.combo_layer.currentIndex()
        map_canvas = self.iface.mapCanvas()
        try:
            self.layer = criteria_layer(map_canvas.layer(index))
            self.__clear_tables()
            self.__loadlayer()
            self.__enable_buttons()
        except:
            QtGui.QMessageBox.information(None, "Error", "Cannot load specified layer")
            return

        try:
            xmcda_file = os.path.splitext(str(self.layer.layer.source()))[0] + ".xmcda"
            self.__load_from_xmcda(xmcda_file)
        except:
            pass

    def __clear_tables(self):
        self.table_criteria.reset_table()
        self.table_prof.reset_table()
        self.table_indiff.reset_table()
        self.table_pref.reset_table()
        self.table_veto.reset_table()

    def __loadlayer(self):
        self.criteria = self.layer.criteria
        self.table_criteria.add(self.criteria)
        self.table_prof.add_criteria(self.criteria)
        self.table_indiff.add_criteria(self.criteria)
        self.table_pref.add_criteria(self.criteria)
        self.table_veto.add_criteria(self.criteria)

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
