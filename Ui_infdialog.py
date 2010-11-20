# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infdialog.ui'
#
# Created: Sat Nov 20 17:33:24 2010
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
        self.groupBox = QtGui.QGroupBox(InferenceDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        self.textBrowser.setFont(font)
        self.textBrowser.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(InferenceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(InferenceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), InferenceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), InferenceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InferenceDialog)

    def retranslateUi(self, InferenceDialog):
        InferenceDialog.setWindowTitle(QtGui.QApplication.translate("InferenceDialog", "Electre Tri - Inference", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("InferenceDialog", "Results", None, QtGui.QApplication.UnicodeUTF8))

