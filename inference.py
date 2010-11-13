from PyQt4 import QtCore, QtGui
from Ui_inference import Ui_InferenceDialog
from qgis_utils import *

class InferenceDialog(QtGui.QDialog, Ui_InferenceDialog):

    def __init__(self, parent, iface):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface

    def add_text(self, text):
        self.textBrowser.append(text)
