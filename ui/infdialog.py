# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infdialog.ui'
#
# Created: Mon Nov 22 21:12:54 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InferenceDialog(object):
    def setupUi(self, InferenceDialog):
        InferenceDialog.setObjectName(_fromUtf8("InferenceDialog"))
        InferenceDialog.setWindowModality(QtCore.Qt.WindowModal)
        InferenceDialog.resize(800, 600)
        self.gridLayout_2 = QtGui.QGridLayout(InferenceDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.group_weights = QtGui.QGroupBox(InferenceDialog)
        self.group_weights.setFlat(False)
        self.group_weights.setCheckable(False)
        self.group_weights.setObjectName(_fromUtf8("group_weights"))
        self.gridLayout = QtGui.QGridLayout(self.group_weights)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_weights = QtGui.QTableWidget(self.group_weights)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_weights.sizePolicy().hasHeightForWidth())
        self.table_weights.setSizePolicy(sizePolicy)
        self.table_weights.setMaximumSize(QtCore.QSize(16777215, 75))
        self.table_weights.setObjectName(_fromUtf8("table_weights"))
        self.table_weights.setColumnCount(0)
        self.table_weights.setRowCount(0)
        self.table_weights.horizontalHeader().setVisible(True)
        self.table_weights.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table_weights, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.group_weights, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InferenceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.group_xmcda = QtGui.QGroupBox(InferenceDialog)
        self.group_xmcda.setObjectName(_fromUtf8("group_xmcda"))
        self.verticalLayout = QtGui.QVBoxLayout(self.group_xmcda)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textb_xmcda = QtGui.QTextBrowser(self.group_xmcda)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        self.textb_xmcda.setFont(font)
        self.textb_xmcda.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textb_xmcda.setObjectName(_fromUtf8("textb_xmcda"))
        self.verticalLayout.addWidget(self.textb_xmcda)
        self.gridLayout_2.addWidget(self.group_xmcda, 0, 0, 1, 1)
        self.group_profiles = QtGui.QGroupBox(InferenceDialog)
        self.group_profiles.setObjectName(_fromUtf8("group_profiles"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.group_profiles)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.table_prof = QtGui.QTableWidget(self.group_profiles)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_prof.sizePolicy().hasHeightForWidth())
        self.table_prof.setSizePolicy(sizePolicy)
        self.table_prof.setObjectName(_fromUtf8("table_prof"))
        self.table_prof.setColumnCount(0)
        self.table_prof.setRowCount(0)
        self.verticalLayout_2.addWidget(self.table_prof)
        self.gridLayout_2.addWidget(self.group_profiles, 2, 0, 1, 1)

        self.retranslateUi(InferenceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InferenceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InferenceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InferenceDialog)

    def retranslateUi(self, InferenceDialog):
        InferenceDialog.setWindowTitle(QtGui.QApplication.translate("InferenceDialog", "Electre Tri - Inference", None, QtGui.QApplication.UnicodeUTF8))
        self.group_weights.setTitle(QtGui.QApplication.translate("InferenceDialog", "Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.group_xmcda.setTitle(QtGui.QApplication.translate("InferenceDialog", "XMCDA output:", None, QtGui.QApplication.UnicodeUTF8))
        self.group_profiles.setTitle(QtGui.QApplication.translate("InferenceDialog", "Profiles", None, QtGui.QApplication.UnicodeUTF8))

