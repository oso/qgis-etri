# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/inference_results.ui'
#
# Created: Tue Nov 19 19:57:44 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui

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

class Ui_inference_results(object):
    def setupUi(self, inference_results):
        inference_results.setObjectName(_fromUtf8("inference_results"))
        inference_results.resize(800, 600)
        self.verticalLayout = QtGui.QVBoxLayout(inference_results)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(inference_results)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graph_model = _MyGraphicsview(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.graph_model.sizePolicy().hasHeightForWidth())
        self.graph_model.setSizePolicy(sizePolicy)
        self.graph_model.setStyleSheet(_fromUtf8("background-color: transparent;"))
        self.graph_model.setFrameShape(QtGui.QFrame.NoFrame)
        self.graph_model.setFrameShadow(QtGui.QFrame.Sunken)
        self.graph_model.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graph_model.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.graph_model.setAlignment(QtCore.Qt.AlignCenter)
        self.graph_model.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.graph_model.setObjectName(_fromUtf8("graph_model"))
        self.verticalLayout_2.addWidget(self.graph_model)
        self.label_lambda = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_lambda.setFont(font)
        self.label_lambda.setText(_fromUtf8(""))
        self.label_lambda.setObjectName(_fromUtf8("label_lambda"))
        self.verticalLayout_2.addWidget(self.label_lambda)
        self.verticalLayout.addWidget(self.groupBox)
        self.tabWidget = QtGui.QTabWidget(inference_results)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.table_comp = qt_performance_table(self.tab)
        self.table_comp.setObjectName(_fromUtf8("table_comp"))
        self.table_comp.setColumnCount(0)
        self.table_comp.setRowCount(0)
        self.verticalLayout_5.addWidget(self.table_comp)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.table_incomp = qt_performance_table(self.tab_2)
        self.table_incomp.setObjectName(_fromUtf8("table_incomp"))
        self.table_incomp.setColumnCount(0)
        self.table_incomp.setRowCount(0)
        self.verticalLayout_4.addWidget(self.table_incomp)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(inference_results)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(inference_results)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(inference_results.accept)
        self.buttonBox.rejected.connect(inference_results.reject)
        QtCore.QMetaObject.connectSlotsByName(inference_results)

    def retranslateUi(self, inference_results):
        inference_results.setWindowTitle(_translate("inference_results", "ELECTRE-TRI Inference results", None))
        self.groupBox.setTitle(_translate("inference_results", "Model learned", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("inference_results", "Compatible alternatives", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("inference_results", "Incompatible alternatives", None))

from qgis_etri.table import qt_performance_table
from qgis_etri.graphic import _MyGraphicsview
