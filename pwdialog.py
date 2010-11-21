from PyQt4 import QtCore, QtGui
from Ui_pwdialog import Ui_PleaseWaitDialog

class PwDialog(QtGui.QDialog, Ui_PleaseWaitDialog):

    def __init__(self, parent, oncancel):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.oncancel = oncancel 

    def reject(self):
        self.oncancel()
