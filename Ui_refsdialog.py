# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'refsdialog.ui'
#
# Created: Fri Nov 26 18:45:03 2010
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
        RefsDialog.resize(800, 300)
        self.gridLayout = QtGui.QGridLayout(RefsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_refs = QtGui.QTableWidget(RefsDialog)
        self.table_refs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_refs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table_refs.setCornerButtonEnabled(False)
        self.table_refs.setObjectName(_fromUtf8("table_refs"))
        self.table_refs.setColumnCount(1)
        self.table_refs.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_refs.setHorizontalHeaderItem(0, item)
        self.table_refs.horizontalHeader().setHighlightSections(False)
        self.table_refs.verticalHeader().setHighlightSections(False)
        self.gridLayout.addWidget(self.table_refs, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cbox_hide = QtGui.QCheckBox(RefsDialog)
        self.cbox_hide.setObjectName(_fromUtf8("cbox_hide"))
        self.horizontalLayout.addWidget(self.cbox_hide)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Bzoom = QtGui.QPushButton(RefsDialog)
        self.Bzoom.setObjectName(_fromUtf8("Bzoom"))
        self.horizontalLayout.addWidget(self.Bzoom)
        self.Bdisplay = QtGui.QPushButton(RefsDialog)
        self.Bdisplay.setObjectName(_fromUtf8("Bdisplay"))
        self.horizontalLayout.addWidget(self.Bdisplay)
        self.buttonBox = QtGui.QDialogButtonBox(RefsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(RefsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RefsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RefsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RefsDialog)

    def retranslateUi(self, RefsDialog):
        RefsDialog.setWindowTitle(QtGui.QApplication.translate("RefsDialog", "Choose reference actions", None, QtGui.QApplication.UnicodeUTF8))
        self.cbox_hide.setText(QtGui.QApplication.translate("RefsDialog", "Hide non criteria columns", None, QtGui.QApplication.UnicodeUTF8))
        self.Bzoom.setText(QtGui.QApplication.translate("RefsDialog", "Zoom to selection", None, QtGui.QApplication.UnicodeUTF8))
        self.Bdisplay.setText(QtGui.QApplication.translate("RefsDialog", "Display selection", None, QtGui.QApplication.UnicodeUTF8))

