# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pwdialog.ui'
#
# Created: Sat Nov 20 17:56:25 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PleaseWaitDialog(object):
    def setupUi(self, PleaseWaitDialog):
        PleaseWaitDialog.setObjectName(_fromUtf8("PleaseWaitDialog"))
        PleaseWaitDialog.resize(223, 45)
        self.horizontalLayout = QtGui.QHBoxLayout(PleaseWaitDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(PleaseWaitDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.buttonBox = QtGui.QDialogButtonBox(PleaseWaitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PleaseWaitDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PleaseWaitDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PleaseWaitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PleaseWaitDialog)

    def retranslateUi(self, PleaseWaitDialog):
        PleaseWaitDialog.setWindowTitle(QtGui.QApplication.translate("PleaseWaitDialog", "Please wait...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PleaseWaitDialog", "Please wait...", None, QtGui.QApplication.UnicodeUTF8))

