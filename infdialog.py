from PyQt4 import QtCore, QtGui
from Ui_infdialog import Ui_InferenceDialog
from qgis_utils import *

class InferenceDialog(QtGui.QDialog, Ui_InferenceDialog):

    def __init__(self, parent, on_accept):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.on_accept = on_accept

    def add_text(self, text):
        self.textBrowser.append(text)

    def accept(self):
        self.on_accept()
        QDialog.accept(self)
