# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created: Sun Jul 14 15:05:17 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_main_window(object):
    def setupUi(self, main_window):
        main_window.setObjectName(_fromUtf8("main_window"))
        main_window.resize(800, 606)
        self.horizontalLayout = QtGui.QHBoxLayout(main_window)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tab_parameters = QtGui.QTabWidget(main_window)
        self.tab_parameters.setObjectName(_fromUtf8("tab_parameters"))
        self.tab_criteria = QtGui.QWidget()
        self.tab_criteria.setObjectName(_fromUtf8("tab_criteria"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab_criteria)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.table_criteria = qt_criteria_table(self.tab_criteria)
        self.table_criteria.setColumnCount(3)
        self.table_criteria.setObjectName(_fromUtf8("table_criteria"))
        self.table_criteria.setRowCount(0)
        self.gridLayout_2.addWidget(self.table_criteria, 0, 0, 1, 1)
        self.tab_parameters.addTab(self.tab_criteria, _fromUtf8(""))
        self.tab_profiles = QtGui.QWidget()
        self.tab_profiles.setObjectName(_fromUtf8("tab_profiles"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab_profiles)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.graph_plot = mygraphicsview(self.tab_profiles)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.graph_plot.sizePolicy().hasHeightForWidth())
        self.graph_plot.setSizePolicy(sizePolicy)
        self.graph_plot.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.graph_plot.setFrameShape(QtGui.QFrame.NoFrame)
        self.graph_plot.setFrameShadow(QtGui.QFrame.Sunken)
        self.graph_plot.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graph_plot.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graph_plot.setAlignment(QtCore.Qt.AlignCenter)
        self.graph_plot.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.graph_plot.setObjectName(_fromUtf8("graph_plot"))
        self.gridLayout_5.addWidget(self.graph_plot, 1, 0, 1, 1)
        self.table_prof = qt_performance_table(self.tab_profiles)
        self.table_prof.setObjectName(_fromUtf8("table_prof"))
        self.table_prof.setColumnCount(0)
        self.table_prof.setRowCount(0)
        self.gridLayout_5.addWidget(self.table_prof, 0, 0, 1, 1)
        self.tab_parameters.addTab(self.tab_profiles, _fromUtf8(""))
        self.tab_plot = QtGui.QWidget()
        self.tab_plot.setObjectName(_fromUtf8("tab_plot"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_plot)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tab_thresholds = QtGui.QTabWidget(self.tab_plot)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tab_thresholds.sizePolicy().hasHeightForWidth())
        self.tab_thresholds.setSizePolicy(sizePolicy)
        self.tab_thresholds.setTabPosition(QtGui.QTabWidget.North)
        self.tab_thresholds.setTabShape(QtGui.QTabWidget.Rounded)
        self.tab_thresholds.setDocumentMode(False)
        self.tab_thresholds.setObjectName(_fromUtf8("tab_thresholds"))
        self.tab_indiff = QtGui.QWidget()
        self.tab_indiff.setObjectName(_fromUtf8("tab_indiff"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_indiff)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.table_indiff = qt_threshold_table(self.tab_indiff)
        self.table_indiff.setObjectName(_fromUtf8("table_indiff"))
        self.table_indiff.setColumnCount(0)
        self.table_indiff.setRowCount(0)
        self.gridLayout_3.addWidget(self.table_indiff, 0, 0, 1, 1)
        self.tab_thresholds.addTab(self.tab_indiff, _fromUtf8(""))
        self.tab_pref = QtGui.QWidget()
        self.tab_pref.setObjectName(_fromUtf8("tab_pref"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_pref)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.table_pref = qt_threshold_table(self.tab_pref)
        self.table_pref.setObjectName(_fromUtf8("table_pref"))
        self.table_pref.setColumnCount(0)
        self.table_pref.setRowCount(0)
        self.gridLayout_4.addWidget(self.table_pref, 0, 0, 1, 1)
        self.tab_thresholds.addTab(self.tab_pref, _fromUtf8(""))
        self.tab_veto = QtGui.QWidget()
        self.tab_veto.setObjectName(_fromUtf8("tab_veto"))
        self.gridLayout_7 = QtGui.QGridLayout(self.tab_veto)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.table_veto = qt_threshold_table(self.tab_veto)
        self.table_veto.setObjectName(_fromUtf8("table_veto"))
        self.table_veto.setColumnCount(0)
        self.table_veto.setRowCount(0)
        self.gridLayout_7.addWidget(self.table_veto, 0, 0, 1, 1)
        self.tab_thresholds.addTab(self.tab_veto, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.tab_thresholds)
        self.graph_plot2 = mygraphicsview(self.tab_plot)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.graph_plot2.sizePolicy().hasHeightForWidth())
        self.graph_plot2.setSizePolicy(sizePolicy)
        self.graph_plot2.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.graph_plot2.setFrameShape(QtGui.QFrame.NoFrame)
        self.graph_plot2.setFrameShadow(QtGui.QFrame.Sunken)
        self.graph_plot2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graph_plot2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graph_plot2.setAlignment(QtCore.Qt.AlignCenter)
        self.graph_plot2.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.graph_plot2.setObjectName(_fromUtf8("graph_plot2"))
        self.verticalLayout_4.addWidget(self.graph_plot2)
        self.tab_parameters.addTab(self.tab_plot, _fromUtf8(""))
        self.tab_inference = QtGui.QWidget()
        self.tab_inference.setObjectName(_fromUtf8("tab_inference"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_inference)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.group_refs = QtGui.QGroupBox(self.tab_inference)
        self.group_refs.setObjectName(_fromUtf8("group_refs"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.group_refs)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.table_refs = QtGui.QTableWidget(self.group_refs)
        self.table_refs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_refs.setObjectName(_fromUtf8("table_refs"))
        self.table_refs.setColumnCount(1)
        self.table_refs.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.table_refs.setHorizontalHeaderItem(0, item)
        self.verticalLayout_3.addWidget(self.table_refs)
        self.layout_choose = QtGui.QHBoxLayout()
        self.layout_choose.setObjectName(_fromUtf8("layout_choose"))
        self.button_chooserefs = QtGui.QPushButton(self.group_refs)
        self.button_chooserefs.setEnabled(False)
        self.button_chooserefs.setObjectName(_fromUtf8("button_chooserefs"))
        self.layout_choose.addWidget(self.button_chooserefs)
        self.button_infer = QtGui.QPushButton(self.group_refs)
        self.button_infer.setEnabled(False)
        self.button_infer.setObjectName(_fromUtf8("button_infer"))
        self.layout_choose.addWidget(self.button_infer)
        self.verticalLayout_3.addLayout(self.layout_choose)
        self.gridLayout_6.addWidget(self.group_refs, 1, 0, 1, 1)
        self.group_infparams = QtGui.QGroupBox(self.tab_inference)
        self.group_infparams.setObjectName(_fromUtf8("group_infparams"))
        self.verticalLayout = QtGui.QVBoxLayout(self.group_infparams)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout_model = QtGui.QHBoxLayout()
        self.layout_model.setObjectName(_fromUtf8("layout_model"))
        self.label_combo = QtGui.QLabel(self.group_infparams)
        self.label_combo.setObjectName(_fromUtf8("label_combo"))
        self.layout_model.addWidget(self.label_combo)
        self.combo_model = QtGui.QComboBox(self.group_infparams)
        self.combo_model.setObjectName(_fromUtf8("combo_model"))
        self.combo_model.addItem(_fromUtf8(""))
        self.layout_model.addWidget(self.combo_model)
        self.verticalLayout.addLayout(self.layout_model)
        self.layout_inference = QtGui.QHBoxLayout()
        self.layout_inference.setObjectName(_fromUtf8("layout_inference"))
        self.label_inference = QtGui.QLabel(self.group_infparams)
        self.label_inference.setObjectName(_fromUtf8("label_inference"))
        self.layout_inference.addWidget(self.label_inference)
        self.combo_inference = QtGui.QComboBox(self.group_infparams)
        self.combo_inference.setObjectName(_fromUtf8("combo_inference"))
        self.combo_inference.addItem(_fromUtf8(""))
        self.combo_inference.addItem(_fromUtf8(""))
        self.combo_inference.addItem(_fromUtf8(""))
        self.layout_inference.addWidget(self.combo_inference)
        self.verticalLayout.addLayout(self.layout_inference)
        self.gridLayout_6.addWidget(self.group_infparams, 0, 0, 1, 1)
        self.tab_parameters.addTab(self.tab_inference, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tab_parameters)
        self.right_layout = QtGui.QVBoxLayout()
        self.right_layout.setObjectName(_fromUtf8("right_layout"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.right_layout.addItem(spacerItem)
        self.group_options = QtGui.QGroupBox(main_window)
        self.group_options.setObjectName(_fromUtf8("group_options"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.group_options)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.button_loadxmcda = QtGui.QPushButton(self.group_options)
        self.button_loadxmcda.setEnabled(False)
        self.button_loadxmcda.setObjectName(_fromUtf8("button_loadxmcda"))
        self.verticalLayout_2.addWidget(self.button_loadxmcda)
        self.button_savexmcda = QtGui.QPushButton(self.group_options)
        self.button_savexmcda.setEnabled(False)
        self.button_savexmcda.setObjectName(_fromUtf8("button_savexmcda"))
        self.verticalLayout_2.addWidget(self.button_savexmcda)
        self.right_layout.addWidget(self.group_options)
        self.group_input = QtGui.QGroupBox(main_window)
        self.group_input.setObjectName(_fromUtf8("group_input"))
        self.gridLayout_9 = QtGui.QGridLayout(self.group_input)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.combo_layer = QtGui.QComboBox(self.group_input)
        self.combo_layer.setObjectName(_fromUtf8("combo_layer"))
        self.gridLayout_9.addWidget(self.combo_layer, 0, 0, 1, 1)
        self.button_loadlayer = QtGui.QPushButton(self.group_input)
        self.button_loadlayer.setObjectName(_fromUtf8("button_loadlayer"))
        self.gridLayout_9.addWidget(self.button_loadlayer, 0, 1, 1, 1)
        self.right_layout.addWidget(self.group_input)
        self.group_profiles = QtGui.QGroupBox(main_window)
        self.group_profiles.setObjectName(_fromUtf8("group_profiles"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.group_profiles)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.button_add_profile = QtGui.QPushButton(self.group_profiles)
        self.button_add_profile.setEnabled(False)
        self.button_add_profile.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/etri/images/plus.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_profile.setIcon(icon)
        self.button_add_profile.setObjectName(_fromUtf8("button_add_profile"))
        self.horizontalLayout_2.addWidget(self.button_add_profile)
        self.label_ncategories = QtGui.QLabel(self.group_profiles)
        self.label_ncategories.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_ncategories.setText(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">-</span></p></body></html>"))
        self.label_ncategories.setObjectName(_fromUtf8("label_ncategories"))
        self.horizontalLayout_2.addWidget(self.label_ncategories)
        self.button_del_profile = QtGui.QPushButton(self.group_profiles)
        self.button_del_profile.setEnabled(False)
        self.button_del_profile.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/etri/images/min.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_del_profile.setIcon(icon1)
        self.button_del_profile.setObjectName(_fromUtf8("button_del_profile"))
        self.horizontalLayout_2.addWidget(self.button_del_profile)
        self.right_layout.addWidget(self.group_profiles)
        self.group_thresholds = QtGui.QGroupBox(main_window)
        self.group_thresholds.setMaximumSize(QtCore.QSize(388, 16777215))
        self.group_thresholds.setObjectName(_fromUtf8("group_thresholds"))
        self.formLayout = QtGui.QFormLayout(self.group_thresholds)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.cbox_samethresholds = QtGui.QCheckBox(self.group_thresholds)
        self.cbox_samethresholds.setObjectName(_fromUtf8("cbox_samethresholds"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.cbox_samethresholds)
        self.cbox_noveto = QtGui.QCheckBox(self.group_thresholds)
        self.cbox_noveto.setObjectName(_fromUtf8("cbox_noveto"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.cbox_noveto)
        self.cbox_sameqp = QtGui.QCheckBox(self.group_thresholds)
        self.cbox_sameqp.setObjectName(_fromUtf8("cbox_sameqp"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.cbox_sameqp)
        self.right_layout.addWidget(self.group_thresholds)
        self.group_affectation = QtGui.QGroupBox(main_window)
        self.group_affectation.setObjectName(_fromUtf8("group_affectation"))
        self.gridLayout_8 = QtGui.QGridLayout(self.group_affectation)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.layout_cutlevel = QtGui.QHBoxLayout()
        self.layout_cutlevel.setObjectName(_fromUtf8("layout_cutlevel"))
        self.label_cutlevel = QtGui.QLabel(self.group_affectation)
        self.label_cutlevel.setObjectName(_fromUtf8("label_cutlevel"))
        self.layout_cutlevel.addWidget(self.label_cutlevel)
        self.spinbox_cutlevel = QtGui.QDoubleSpinBox(self.group_affectation)
        self.spinbox_cutlevel.setMinimum(0.5)
        self.spinbox_cutlevel.setMaximum(1.0)
        self.spinbox_cutlevel.setSingleStep(0.01)
        self.spinbox_cutlevel.setProperty("value", 0.75)
        self.spinbox_cutlevel.setObjectName(_fromUtf8("spinbox_cutlevel"))
        self.layout_cutlevel.addWidget(self.spinbox_cutlevel)
        self.gridLayout_8.addLayout(self.layout_cutlevel, 0, 0, 1, 1)
        self.layout_procedure = QtGui.QHBoxLayout()
        self.layout_procedure.setObjectName(_fromUtf8("layout_procedure"))
        self.label_procedure = QtGui.QLabel(self.group_affectation)
        self.label_procedure.setObjectName(_fromUtf8("label_procedure"))
        self.layout_procedure.addWidget(self.label_procedure)
        self.combo_procedure = QtGui.QComboBox(self.group_affectation)
        self.combo_procedure.setObjectName(_fromUtf8("combo_procedure"))
        self.combo_procedure.addItem(_fromUtf8(""))
        self.combo_procedure.addItem(_fromUtf8(""))
        self.layout_procedure.addWidget(self.combo_procedure)
        self.gridLayout_8.addLayout(self.layout_procedure, 1, 0, 1, 1)
        self.right_layout.addWidget(self.group_affectation)
        self.button_generate = QtGui.QPushButton(main_window)
        self.button_generate.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/etri/images/etri.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_generate.setIcon(icon2)
        self.button_generate.setObjectName(_fromUtf8("button_generate"))
        self.right_layout.addWidget(self.button_generate)
        self.horizontalLayout.addLayout(self.right_layout)

        self.retranslateUi(main_window)
        self.tab_parameters.setCurrentIndex(0)
        self.tab_thresholds.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(_translate("main_window", "ELECTRE TRI", None))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_criteria), _translate("main_window", "Criteria", None))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_profiles), _translate("main_window", "Profiles", None))
        self.tab_thresholds.setTabText(self.tab_thresholds.indexOf(self.tab_indiff), _translate("main_window", "Indifference", None))
        self.tab_thresholds.setTabText(self.tab_thresholds.indexOf(self.tab_pref), _translate("main_window", "Preference", None))
        self.tab_thresholds.setTabText(self.tab_thresholds.indexOf(self.tab_veto), _translate("main_window", "Veto", None))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_plot), _translate("main_window", "Thresholds", None))
        self.group_refs.setTitle(_translate("main_window", "Reference actions", None))
        item = self.table_refs.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Category", None))
        self.button_chooserefs.setText(_translate("main_window", "Choose reference actions", None))
        self.button_infer.setText(_translate("main_window", "Infer parameters", None))
        self.group_infparams.setTitle(_translate("main_window", "Parameters", None))
        self.label_combo.setText(_translate("main_window", "Electre Tri model:", None))
        self.combo_model.setItemText(0, _translate("main_window", "Bouyssou-Marchant (Pessimistic)", None))
        self.label_inference.setText(_translate("main_window", "Inference:", None))
        self.combo_inference.setItemText(0, _translate("main_window", "Global", None))
        self.combo_inference.setItemText(1, _translate("main_window", "Profiles", None))
        self.combo_inference.setItemText(2, _translate("main_window", "Weights and lambda", None))
        self.tab_parameters.setTabText(self.tab_parameters.indexOf(self.tab_inference), _translate("main_window", "Inference", None))
        self.group_options.setTitle(_translate("main_window", "XMCDA", None))
        self.button_loadxmcda.setText(_translate("main_window", "Load parameters", None))
        self.button_savexmcda.setText(_translate("main_window", "Save parameters", None))
        self.group_input.setTitle(_translate("main_window", "Input Layer", None))
        self.button_loadlayer.setText(_translate("main_window", "Load", None))
        self.group_profiles.setTitle(_translate("main_window", "Categories", None))
        self.group_thresholds.setTitle(_translate("main_window", "Thresholds", None))
        self.cbox_samethresholds.setText(_translate("main_window", "Use same for all profiles", None))
        self.cbox_noveto.setText(_translate("main_window", "No Veto", None))
        self.cbox_sameqp.setText(_translate("main_window", "Indifference = Preference", None))
        self.group_affectation.setTitle(_translate("main_window", "Affectation", None))
        self.label_cutlevel.setText(_translate("main_window", "Cutting level:", None))
        self.label_procedure.setText(_translate("main_window", "Procedure:", None))
        self.combo_procedure.setItemText(0, _translate("main_window", "Pessimistic", None))
        self.combo_procedure.setItemText(1, _translate("main_window", "Optimistic", None))
        self.button_generate.setText(_translate("main_window", "Generate Decision Map", None))

from table import qt_performance_table, qt_threshold_table, qt_criteria_table
from graphic import mygraphicsview
import resources_rc
