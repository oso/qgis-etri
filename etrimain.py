from PyQt4 import QtCore, QtGui
from ui.etrimain import Ui_EtriMainWindow
from qgis_utils import *
from etri import *
from refsdialog import *
from infdialog import *
from pwdialog import *
from xml.etree import ElementTree as ET
from graphic import graph_etri
import os
import time
import threading
import xmcda
import ui_utils
from ui.pwdialog import * 
#from ui.pwdialog import Ui_PleaseWaitDialog

COL_CRITERIONS = 2
COL_DIRECTION = 1

class EtriMainWindow(QtGui.QMainWindow, Ui_EtriMainWindow):

    def __init__(self, iface, map_canvas=None):
        self.map_canvas = map_canvas
        self.iface = iface
        parent = self.iface.mainWindow()
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.criteria_activated = []
        self.ncriteria = 0
        self.samethresholds = 0
        self.sameqp = 0
        self.noveto = 0
        self.crit_layers = []
        self.refs_ids = []

        self.__update_layer_list(map_canvas)

        self.table_crit.setColumnWidth(0, 235)
        self.table_crit.setColumnWidth(1, 60)
        self.table_crit.setColumnWidth(2, 50)

    def closeEvent(self, event):
        if self.isEnabled() == False:
            event.ignore();

    def __update_layer_list(self, map_canvas):
        if map_canvas == None:
            return

        for i in range(map_canvas.layerCount()):
            layer = map_canvas.layer(i)
            self.combo_layer.addItem(layer.name())
            self.crit_layers.append(layer)

    def clear_rows(self, table):
        nrows = table.rowCount()
        for i in range(nrows):
            table.removeRow(i)
        table.setRowCount(0)

    def clear_table(self, table):
        nrows = table.rowCount()
        ncols = table.columnCount()
        for i in range(nrows):
            table.removeRow(i)
        for i in range(ncols):
            table.removeColumn(i)
        table.setRowCount(0)
        table.setColumnCount(0)

    def set_crit_layer(self, layer):
        self.criteria_activated = []
        self.ncriteria = 0
        self.samethresholds = 0
        self.sameqp = 0
        self.noveto = 0
        self.clear_rows(self.table_crit)
        self.clear_table(self.table_prof)
        self.clear_table(self.table_indiff)
        self.clear_table(self.table_pref)
        self.clear_table(self.table_veto)
        self.table_refs.setColumnCount(1)
        self.table_refs.setRowCount(0)

        self.crit_layer_load(layer)
        self.crit_layer = layer
        self.update_model_graph()

        self.Badd_profile.setEnabled(True)
        self.Bdel_profile.setEnabled(True)
        self.Bgenerate.setEnabled(True)
        self.Bchooserefs.setEnabled(True)
        self.Bloadxmcda.setEnabled(True)
        self.Bsavexmcda.setEnabled(True)

    def crit_layer_load(self, layer):
        self.criteria = layer_get_criteria(layer)
        for crit in self.criteria:
            self.add_criterion(crit)

        self.actions = layer_get_attributes(layer)

        xmcda_file = os.path.splitext(str(layer.source()))[0] + ".xmcda"
        if os.path.exists(xmcda_file) == True:
            try:
                self.load_xmcda_data(xmcda_file)
            except:
                self.add_profile(0)
        else:
            self.add_profile(0)

    def get_active_row(self, table, index):
        ncols = table.columnCount()
        values = {}
        for j in self.criteria_activated:
            criterion = self.criteria[j]['id']
            item = table.item(index, j)
            if item <> None and len(item.text()) > 0:
                values["%s" % criterion] = round(float(item.text()), 2)
        return values

    def get_row_as_str(self, table, index):
        ncols = table.columnCount()
        values = []
        for j in range(ncols):
            item = table.item(index, j)
            if item <> None:
                values.append(str(item.text()))
            else:
                values.append("")

        return values

    def set_row(self, table, index, vector):
        for j in range(len(vector)):
            item = QtGui.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            try:
                item.setText(str(round(float(vector[j]),2)))
            except:
                pass

            table.setItem(index, j, item)

    def add_profile(self, index):
        nprof = self.table_prof.rowCount()
        if index > nprof or index == -1:
            index = nprof

        # Profiles table
        self.table_prof.insertRow(index)

        if nprof == 0:
            val = [x['mean'] for x in self.criteria]
        else:
            val = self.get_row_as_str(self.table_prof, index-1)

        self.set_row(self.table_prof, index, val)

        # P, Q thresholds table
        self.table_pref.insertRow(nprof)
        self.table_indiff.insertRow(nprof)
        self.table_veto.insertRow(nprof)
        for table in [self.table_pref, self.table_indiff]:
            if index == 0:
                thresholds = [0] * table.columnCount()
            else:
                thresholds = self.get_row_as_str(table, index-1)
            self.set_row(table, index, thresholds)
            if self.samethresholds == 1:
                table.setRowHidden(index, 1)

        # V thresholds table
        if index == 0:
            thresholds = [""] * table.columnCount()
        else:
            thresholds = self.get_row_as_str(self.table_veto, index-1)
        self.set_row(self.table_veto, index, thresholds)

        if self.samethresholds == 1:
            self.table_veto.setRowHidden(index, 1)

        # update label
        self.label_ncategories.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">%s</span></p></body></html>" % (nprof+2))

        # update reference comboboxes
        for i in range(self.table_refs.rowCount()):
            combobox = self.table_refs.cellWidget(i, 0)
            if combobox.count() < (nprof+2):
                combobox.addItem(str(nprof+2))

        self.update_model_graph()

    def del_profile(self, index):
        nprof = self.table_prof.rowCount()
        if index > nprof or index < 1:
            return #FIXME: Add dialog box warning

        self.table_prof.removeRow(index)
        self.table_pref.removeRow(index)
        self.table_indiff.removeRow(index)
        self.table_veto.removeRow(index)

        # update label
        self.label_ncategories.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">%s</span></p></body></html>" % (nprof))

        # update reference comboboxes
        for i in range(self.table_refs.rowCount()):
            combobox = self.table_refs.cellWidget(i, 0)
            combobox.removeItem(nprof)

    def add_criterion(self, crit):
        # Add row in criteria table
        nrow = self.table_crit.rowCount()
        self.table_crit.insertRow(nrow)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.table_crit.setItem(nrow, 0, item)

        item = QtGui.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsTristate)
        self.table_crit.setItem(nrow, 1, item)

        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        item.setText("10.0")
        self.table_crit.setItem(nrow, 2, item)
        
        checkBox = QtGui.QCheckBox(self)
        checkBox.setCheckState(QtCore.Qt.Checked)
        checkBox.setText(QtGui.QApplication.translate("MainWindow", crit['name'], None, QtGui.QApplication.UnicodeUTF8))
        self.table_crit.setCellWidget(nrow, 0, checkBox)

        signalMapper = QtCore.QSignalMapper(self)
        QtCore.QObject.connect(checkBox, QtCore.SIGNAL("stateChanged(int)"), signalMapper, QtCore.SLOT("map()"))
        signalMapper.setMapping(checkBox, nrow)
        QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped(int)"), self.on_criterion_stateChanged)

        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("Max")
        comboBox.addItem("Min")
        self.table_crit.setCellWidget(nrow, 1, comboBox)

        # Add column in profiles and thresholds table
        for table in [ self.table_prof, self.table_pref, self.table_indiff, self.table_veto ]:
            table.insertColumn(nrow)
            item = QtGui.QTableWidgetItem()
            table.setHorizontalHeaderItem(nrow, item)
            table.horizontalHeaderItem(nrow).setText(crit['name'])

        # Add column in assignment table
        self.table_refs.insertColumn(nrow+1)
        item = QtGui.QTableWidgetItem()
        self.table_refs.setHorizontalHeaderItem(nrow+1, item)
        self.table_refs.horizontalHeaderItem(nrow+1).setText(crit['name'])

        self.ncriteria += 1
        self.criteria_activated.append(nrow)
        self.criteria_activated.sort()

    def get_criteria_index(self):
        index = []
        for i in self.criteria_activated:
            index.append(self.criteria[i]['id'])
        return index

    def get_actions(self):
        index = self.get_criteria_index()

        actions = {}
        for action, attrs in self.actions.iteritems():
            attributes = {}
            for id in index:
                attributes["%s" % id] = attrs[id]
            actions[action] = attributes

        return actions

    def get_criteria_weights(self):
        W = {}
        for i in self.criteria_activated:
            criterion = self.criteria[i]['id']
            w = self.table_crit.item(i,2) 
            W["%s" % criterion] = round(float(w.text()), 2)

        return W

    def get_criteria_directions(self):
        directions = {}
        for i in self.criteria_activated:
            criterion = self.criteria[i]['id']
            item = self.table_crit.cellWidget(i, COL_DIRECTION)
            index = item.currentIndex()
            if index == 0:
                directions["%s" % criterion] = 1 
            else:
                directions["%s" % criterion] = -1 

        return directions

    def get_profiles(self):
        nrows = self.table_prof.rowCount()
        ncols = self.table_prof.columnCount()

        profiles = []
        for row in range(nrows):
            prof = self.get_active_row(self.table_prof, row)

            if row == 0 or self.samethresholds == 1: 
                index = 0
            else:
                index = row

            p = self.get_active_row(self.table_pref, index)

            if self.sameqp == 1:
                q = p
            else:
                q = self.get_active_row(self.table_indiff, index)

            if self.noveto <> 1:
                v = self.get_active_row(self.table_veto, index)
            else:
                v = {}

            profile = { 'refs':prof, 'q': q, 'p': p, 'v': v}

            profiles.append(profile)

        return profiles

    def check_is_float(self, table, row, column):
        item = table.item(row, column)
        val = item.text()
        try:
            round(float(val), 2)
        except:
            item.setBackgroundColor(QtCore.Qt.red)
            return

        item.setBackgroundColor(QtCore.Qt.white)

    def check_is_float_or_empty(self, table, row, column):
        item = table.item(row, column)
        val = item.text()
        if len(val) == 0:
            item.setBackgroundColor(QtCore.Qt.white)
            return

        try:
            round(float(val), 2)
        except:
            item.setBackgroundColor(QtCore.Qt.red)
            return

        item.setBackgroundColor(QtCore.Qt.white)

    def check_profile_crit(self, row, column):
        item = self.table_prof.item(row, column)
        val = item.text()
        try:
            val = round(float(val), 2)
        except:
            item.setBackgroundColor(QtCore.Qt.red)
            return False

        if val < self.criteria[column]['min'] or val > self.criteria[column]['max']:
            item.setBackgroundColor(QtCore.Qt.red)
            return False

        item.setBackgroundColor(QtCore.Qt.white)

    def goto_next_cell(self, table, c_row, c_col):
        if table.currentRow() == c_row and table.currentColumn() == c_col:
            table.focusNextChild() 

    def on_table_crit_cellChanged(self, row, column):
        if column == COL_CRITERIONS:
            self.check_is_float(self.table_crit, row, column)

        self.table_crit.setCurrentCell(row+1,column)

    def on_criterion_stateChanged(self, row):
        item = self.table_crit.cellWidget(row, 0)
        if item.isChecked() == False:
            self.table_prof.setColumnHidden(row, 1)
            self.table_indiff.setColumnHidden(row, 1)
            self.table_pref.setColumnHidden(row, 1)
            self.table_veto.setColumnHidden(row, 1)
            self.table_refs.setColumnHidden(row+1, 1)
            self.criteria_activated.remove(row)
        else:
            self.table_prof.setColumnHidden(row, 0)
            self.table_indiff.setColumnHidden(row, 0)
            self.table_pref.setColumnHidden(row, 0)
            self.table_veto.setColumnHidden(row, 0)
            self.table_refs.setColumnHidden(row+1, 0)
            self.criteria_activated.append(row)
            self.criteria_activated.sort()

        self.update_model_graph()

    def on_Bloadlayer_pressed(self):
        index = self.combo_layer.currentIndex()
        try:
            self.set_crit_layer(self.crit_layers[index])
        except:
            QMessageBox.information(None, "Warning", "Cannot load specified layer!")

    def on_Badd_profile_pressed(self):
        self.add_profile(-1)
        self.update_model_graph()

    def on_Bdel_profile_pressed(self):
        self.del_profile(self.table_prof.rowCount()-1)
        self.update_model_graph()

    def on_table_prof_cellChanged(self, row, column):
        self.check_profile_crit(row, column)
        if self.table_prof.currentRow() == row and self.table_prof.currentColumn() == column:
            self.table_prof.focusNextChild()
            try:
                self.update_model_graph()
            except:
                pass

    def on_table_indiff_cellChanged(self, row, column):
        self.check_is_float(self.table_indiff, row, column)
        self.goto_next_cell(self.table_indiff, row, column)

    def on_table_pref_cellChanged(self, row, column):
        self.check_is_float(self.table_pref, row, column)
        self.goto_next_cell(self.table_pref, row, column)

    def on_table_veto_cellChanged(self, row, column):
        self.check_is_float_or_empty(self.table_veto, row, column)
        self.goto_next_cell(self.table_veto, row, column)

    def on_cbox_samethresholds_stateChanged(self, state):
        if state == 0:
            self.samethresholds = 0
            for i in range(1, self.ncriteria):
                self.table_indiff.setRowHidden(i, 0)
                self.table_pref.setRowHidden(i, 0)
                self.table_veto.setRowHidden(i, 0)
        else:
            self.samethresholds = 1
            for i in range(1, self.ncriteria):
                self.table_indiff.setRowHidden(i, 1)
                self.table_pref.setRowHidden(i, 1)
                self.table_veto.setRowHidden(i, 1)

    def on_cbox_noveto_stateChanged(self, state):
        if state == 0:
            self.noveto = 0
            self.tab_thresholds.insertTab(2, self.tab_veto, "Veto")
        else:
            self.noveto = 1
            index = self.tab_thresholds.indexOf(self.tab_veto)
            self.tab_thresholds.removeTab(index)

    def on_cbox_sameqp_stateChanged(self, state):
        if state == 0:
            self.sameqp = 0
            self.tab_thresholds.insertTab(0, self.tab_indiff, "Indifference")
        else:
            self.sameqp = 1
            index = self.tab_thresholds.indexOf(self.tab_indiff)
            self.tab_thresholds.removeTab(index)

    def on_Bgenerate_pressed(self):
        ( file, encoding ) = saveDialog(self)
        if file is None or encoding is None:
            return # FIXME

        #print "Generate Decision Map"
        weights = self.get_criteria_weights()
        #print "Weights:", weights
        directions = self.get_criteria_directions()
        #print "Directions:", directions
        profiles = self.get_profiles()
        #print "Profiles:", profiles
        actions = self.get_actions()
        #print "Actions:", actions
        cutlevel = self.spinbox_cutlevel.value()
        #print "Cutting level:", cutlevel

        tri = electre_tri(actions, profiles, weights, cutlevel, directions)

        if self.combo_procedure.currentIndex() == 1:
            affectations = tri.optimist()
        else:
            affectations = tri.pessimist()

        #print "Affectations:", affectations

        generate_decision_map(self.crit_layer, affectations, file, encoding)
        self.save_xmcda_data(os.path.splitext(file)[0]+".xmcda")

        addtocDialog(self, file, self.table_prof.rowCount())

    def on_Bchooserefs_pressed(self):
        if hasattr(self, 'crit_layer'):
            refs_dialog = RefsDialog(self, self.iface, self.crit_layer, self.refs_ids[:])
            refs_dialog.show()

    def set_reference_actions(self, feat_ids):
        # Remove old reference actions
        to_del = []
        for i, featid in enumerate(self.refs_ids):
            if featid not in list(feat_ids):
                to_del.append(i)

        to_del.sort()
        to_del.reverse()
        for i in to_del:
                self.table_refs.removeRow(i)

        # Add new reference actions
        for i, featid in enumerate(feat_ids):
            if featid not in self.refs_ids:
                attr = layer_get_feature_attribute(self.crit_layer, featid)
                self.table_refs_add_row(attr)

        self.refs_ids = feat_ids[:]
        if len(self.refs_ids) > 0:
            self.Binfer.setEnabled(True)
        else:
            self.Binfer.setEnabled(False)

    def table_refs_add_row(self, attr):
        nrow = self.table_refs.rowCount()
        self.table_refs.insertRow(nrow)
        for crit in self.criteria:
            crit_id = crit['id']
            item = QtGui.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            item.setText(attr[crit_id])
            self.table_refs.setItem(nrow, crit_id+1, item)

            item = QtGui.QTableWidgetItem()
            self.table_refs.setItem(nrow, 0, item)
            comboBox = QtGui.QComboBox(self)
            for i in range(self.table_prof.rowCount()+1):
                comboBox.addItem(str(i+1))
            self.table_refs.setCellWidget(nrow, 0, comboBox)

    def create_xmcda_input(self):
        nalts = self.table_refs.rowCount()

        alts = []
        for i in range(nalts):
            alts.append("%d" % (i+1))
        xmcda_alts = xmcda.format_alternatives(alts)

        crit = []
        for i in self.criteria_activated:
            crit.append("%s" % self.criteria[i]['id'])

        directions = self.get_criteria_directions()
        xmcda_crit = xmcda.format_criteria(crit, directions)

        alts_perfs = {}
        affect = {}
        ncat = self.table_prof.rowCount()+1 
        for i in range(nalts):
            item = self.table_refs.cellWidget(i, 0)
            cat = item.currentIndex()+1
            affect["%d" % (i+1)] = "%d" % cat
            alt_perfs = {}
            for j in self.criteria_activated:
                evaluation = self.table_refs.item(i,j+1).text()
                critid = self.criteria[j]['id']
                alt_perfs["%s" % critid] = evaluation
            alts_perfs["%d" % (i+1)] = alt_perfs
        xmcda_pt = xmcda.format_performances_table(alts_perfs)
        xmcda_affect = xmcda.format_affectations(affect)

        cats = []
        for i in range(ncat):
            cats.append("%d" % (i+1))
        xmcda_cats = xmcda.format_categories(cats) 
        
        xmcda_data = {}
        xmcda_data['alternatives'] = xmcda.add_xmcda_tags(xmcda_alts)
        xmcda_data['criteria'] = xmcda.add_xmcda_tags(xmcda_crit)
        xmcda_data['categories'] = xmcda.add_xmcda_tags(xmcda_cats)
        xmcda_data['perfs_table'] = xmcda.add_xmcda_tags(xmcda_pt)
        xmcda_data['assign'] = xmcda.add_xmcda_tags(xmcda_affect)

        #print xmcda_alts
        #print xmcda_crit
        #print xmcda_cats
        #print xmcda_pt
        #print xmcda_affect

        if self.combo_inference.currentIndex() == 1:
            weights = self.get_criteria_weights()
            xmcda_weights = xmcda.format_criteria_weights(weights)
            cutlevel = self.spinbox_cutlevel.value()
            xmcda_cutlevel = xmcda.format_lambda(cutlevel)

            #print xmcda_weights
            #print xmcda_cutlevel

            xmcda_data['crit_weights'] = xmcda.add_xmcda_tags(xmcda_weights)
            xmcda_data['lambda'] = xmcda.add_xmcda_tags(xmcda_cutlevel)
        elif self.combo_inference.currentIndex() == 2:
            profiles = self.get_profiles()
            refs = [ profile['refs'] for profile in profiles ]
            ref_alts = [ "b%d" % (i+1) for i in range(len(refs))]
            xmcda_catprof = xmcda.format_category_profiles(refs, ref_alts, cats)
            xmcda_refalts = xmcda.format_pt_reference_alternatives(profiles, ref_alts, crit)

            #print xmcda_catprof
            #print xmcda_refalts

            xmcda_data['cat_profiles'] = xmcda.add_xmcda_tags(xmcda_catprof)
            xmcda_data['reference_alts'] = xmcda.add_xmcda_tags(xmcda_refalts)
        else:
            pass

        return xmcda_data

    def parse_xmcda_output(self, solution):
        xmcda_msg = ET.ElementTree(ET.fromstring(str(solution.messages)))
        xmcda_cat_prof = ET.ElementTree(ET.fromstring(str(solution.cat_profiles)))
        xmcda_refalts_pt = ET.ElementTree(ET.fromstring(str(getattr(solution, 'reference_alts'))))
        xmcda_crit_weights = ET.ElementTree(ET.fromstring(str(solution.crit_weights)))
        xmcda_compat_alts = ET.ElementTree(ET.fromstring(str(getattr(solution, 'compatible_alts'))))
        xmcda_lambda = ET.ElementTree(ET.fromstring(str(getattr(solution, 'lambda'))))

        nprofiles = self.table_prof.rowCount()
        ref_alts = [ "b%d" % (i+1) for i in range(nprofiles)]

        crit = []
        for i in self.criteria_activated:
            crit.append("%s" % self.criteria[i]['id'])

        message = xmcda.get_method_messages(xmcda_msg)
        if message == None:
            message = xmcda.get_method_errors(xmcda_msg)

        profiles = xmcda.get_performance_table(xmcda_refalts_pt, ref_alts, crit) 
        weights = xmcda.get_criterion_value(xmcda_crit_weights, crit)
        compat_alts = xmcda.get_alternatives_id(xmcda_compat_alts)
        lbda = xmcda.get_lambda(xmcda_lambda) 

        return (message, profiles, weights, lbda, compat_alts)

    def display_inference_results(self, solution):
        try:
            self.inference_out = self.parse_xmcda_output(solution)
        except:
            QMessageBox.information(None, "Warning", "Cannot parse XMCDA output")
            return

        messages = self.inference_out[0]
        profiles = self.inference_out[1]
        weights = self.inference_out[2]
        lbda = self.inference_out[3]
        compat_alts = self.inference_out[4]

        for crit, val in weights.iteritems():
            weights[crit] = val*1000

        inference_dialog = InferenceDialog(self, self.on_inference_accept)
        inference_dialog.show()
        inference_dialog.set_xmcda_text("Inference Procedure results")
        inference_dialog.set_xmcda_text("===========================\n")
        for msg in messages:
            inference_dialog.set_xmcda_text(msg)

        if messages[0] <> "Execution ok":
            return

        inference_dialog.set_xmcda_text("\nLambda = %f\n" % lbda)


        criterion_names = {}
        for i in self.criteria_activated:
            criterion_names["%d" % i] = self.criteria[i]['name'] 

        inference_dialog.set_weights(criterion_names, weights)
        inference_dialog.set_profiles(criterion_names, profiles)

        str = "Compatible alternatives = "
        for i, alt in enumerate(compat_alts):
            str += "%d" % (i+1)
            if i != len(compat_alts)-1:
                str += ", "
        str += "\n"
        inference_dialog.set_xmcda_text(str)

    def on_inference_accept(self):
        messages = self.inference_out[0]
        profiles = self.inference_out[1]
        weights = self.inference_out[2]
        lbda = self.inference_out[3]
        compat_alts = self.inference_out[4]

        if messages[0] <> "Execution ok":
            return

        self.set_weights(weights)
        self.set_profiles(profiles)
        self.set_lambda(lbda)

    def set_weights(self, weights):
        for crit_id, val in weights.iteritems():
            value = "%.2f" % val
            id = int(crit_id)
            self.table_crit.item(id,2).setText(value)

    def set_directions(self, directions):
        for crit_id, direction in directions.iteritems():
            id = int(crit_id)
            item = self.table_crit.cellWidget(id, 1)
            if direction == 'min':
                item.setCurrentIndex(1)
            else:
                item.setCurrentIndex(0)

    def set_profiles(self, profiles, thresholds=None):
        nprofiles = len(profiles)
        self.clear_rows(self.table_prof)
        self.clear_rows(self.table_indiff)
        self.clear_rows(self.table_pref)
        self.clear_rows(self.table_veto)
        for i in range(nprofiles):
            profile_name = "b%d" % (i+1)
            values = []
            for j in range(len(self.criteria)):
                if j in self.criteria_activated:
                    values.append(profiles[profile_name]["%d" % j]) 
                else:
                    values.append(0)
            self.add_profile(i)
            self.set_row(self.table_prof, i, values) 

            if thresholds:
                q_values = []
                p_values = []
                v_values = []
                for j in range(len(self.criteria)):
                    if j in self.criteria_activated:
                        q_values.append(thresholds["%d" % j]["q%d" % (i+1)])
                        p_values.append(thresholds["%d" % j]["p%d" % (i+1)])
                        if thresholds["%d" % j].has_key("v%d" % (i+1)): 
                            v_values.append(thresholds["%d" % j]["v%d" % (i+1)])
                        else:
                            v_values.append("")
                    else:
                        q_values.append(0)
                        p_values.append(0)
                        v_values.append("")
                self.set_row(self.table_indiff, i, q_values)
                self.set_row(self.table_pref, i, p_values)
                self.set_row(self.table_veto, i, v_values)

    def set_lambda(self, lbda):
        self.spinbox_cutlevel.setValue(lbda)

    def on_inference_cancel(self):
        self.inf_canceled = 1

    def on_inference_found(self, solution):
        if self.inf_canceled == 0:
            self.inf_solution = solution

    def on_Binfer_pressed(self):
        pw_dialog = PwDialog(self, self.on_inference_cancel)
        pw_dialog.show()

        xmcda_data = self.create_xmcda_input()
        self.inf_solution = None
        self.inf_canceled = 0
        inf_task = inference_task(self.on_inference_found, xmcda_data)
        inf_task.start()

        while self.inf_canceled == 0 and self.inf_solution == None:
            QApplication.processEvents()

        pw_dialog.destroy()
        inf_task.stop()

        if self.inf_solution and self.inf_canceled == 0:
            self.display_inference_results(self.inf_solution)

    def load_xmcda_data(self, file):
        xmcda_file = ET.parse(open(file, 'r'))
        criteria = xmcda.get_criteria_id(xmcda_file)
        self.cbox_samethresholds.setChecked(False)
        self.cbox_sameqp.setChecked(False)
        self.cbox_noveto.setChecked(False)
        # FIXME: use ID of criterion
        for i, crit in enumerate(self.criteria):
            item = self.table_crit.cellWidget(i, 0)
            if str(i) not in criteria:
                item.setChecked(False)
            else:
                item.setChecked(True)

        profile_names = xmcda.get_alternatives_id(xmcda_file)
        profiles = xmcda.get_performance_table(xmcda_file, profile_names, criteria) 
        thresholds = xmcda.get_thresholds(xmcda_file, criteria)
        weights = xmcda.get_criterion_value(xmcda_file, criteria)
        directions = xmcda.get_criteria_directions(xmcda_file)
        compat_alts = xmcda.get_alternatives_id(xmcda_file)
        lbda = xmcda.get_lambda(xmcda_file) 

        self.set_directions(directions)
        self.set_weights(weights)
        self.set_profiles(profiles, thresholds)
        self.set_lambda(lbda)

    def on_Bloadxmcda_pressed(self):
        (file, encoding) = ui_utils.xmcda_load_dialog(self)
        if file is None:
            return

        self.load_xmcda_data(file)

    def save_xmcda_data(self, file):
        weights = self.get_criteria_weights()
        criteria = weights.keys()
        nprofiles = self.table_prof.rowCount()
        profile_names = [ "b%d" % (i+1) for i in range(nprofiles)]
        directions = self.get_criteria_directions()
        profiles = self.get_profiles()
        cutlevel = self.spinbox_cutlevel.value()
        q_thresholds = [ profile['q'] for profile in profiles ]
        p_thresholds = [ profile['p'] for profile in profiles ]
        v_thresholds = [ profile['v'] for profile in profiles ]

        xmcda_criteria = xmcda.format_criteria(criteria, directions, q_thresholds, p_thresholds, v_thresholds)
        xmcda_profiles = xmcda.format_pt_reference_alternatives(profiles, profile_names, criteria)
        xmcda_profile_names = xmcda.format_alternatives(profile_names)
        xmcda_weights = xmcda.format_criteria_weights(weights)
        xmcda_cutlevel = xmcda.format_lambda(cutlevel)

        xmcda.save_file(file, xmcda_criteria+xmcda_profile_names+xmcda_profiles+xmcda_weights+xmcda_cutlevel) 

    def on_Bsavexmcda_pressed(self):
        (file, encoding) = ui_utils.xmcda_save_dialog(self)
        if file is None:
            return

        self.save_xmcda_data(file)

    def update_model_graph(self):
        if hasattr(self, 'crit_layer') == False:
            return

        weights = self.get_criteria_weights()
        directions = self.get_criteria_directions()
        profiles = self.get_profiles()
        actions = self.get_actions()
        cutlevel = self.spinbox_cutlevel.value()

        criteria = []
        criteria_name = {}
        for i in self.criteria_activated:
            criterion = str(self.criteria[i]['id'])
            criteria.append(criterion)
            criteria_name[criterion] = self.criteria[i]['name']

        etri = electre_tri(actions, profiles, weights, cutlevel, directions, criteria)
        graph = graph_etri(etri, self.graph_plot.size()) 
        graph.update_criteria_name(criteria_name)
        self.graph_plot.setScene(graph)
        self.graph_plot_2.setScene(graph)

class inference_task(threading.Thread):

    def __init__(self, on_found, xmcda_input):
        self.xmcda_input = xmcda_input 
        self.on_found = on_found
        self.terminated = False
        self._stopevent = threading.Event( )
        threading.Thread.__init__( self )

    def run(self):
        ticket = xmcda.submit_problem(xmcda.ETRI_BM_URL, self.xmcda_input)
        while True: 
            solution = xmcda.request_solution(xmcda.ETRI_BM_URL, ticket, 0)
            if self._stopevent.isSet() == True:
                return
            if solution:
                break
            time.sleep(0.5)

        self.on_found(solution)

    def stop(self):
        self._stopevent.set()
