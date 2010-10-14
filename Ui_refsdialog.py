# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refsdialog.ui'
#
# Created: Thu Oct 14 22:34:08 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RefsDialog(object):
    def setupUi(self, RefsDialog):
        RefsDialog.setObjectName(_fromUtf8("RefsDialog"))
        RefsDialog.resize(600, 300)
        self.gridLayout = QtGui.QGridLayout(RefsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_refs = QtGui.QTableWidget(RefsDialog)
        self.table_refs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_refs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_refs.setObjectName(_fromUtf8("table_refs"))
        self.table_refs.setColumnCount(0)
        self.table_refs.setRowCount(0)
        self.gridLayout.addWidget(self.table_refs, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RefsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(RefsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RefsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RefsDialog)

    def retranslateUi(self, RefsDialog):
        RefsDialog.setWindowTitle(QtGui.QApplication.translate("RefsDialog", "Choose reference actions", None, QtGui.QApplication.UnicodeUTF8))

