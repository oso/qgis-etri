from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
