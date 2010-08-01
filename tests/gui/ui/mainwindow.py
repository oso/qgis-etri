from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_mainwindow import Ui_MainWindow

criterions = ["Densite_Pop", "tx_chomage", "PIB" ]

class MainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self, parent = None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.set_data()
		self.table_crit.resizeColumnsToContents()

	def add_criteria(self, name):
		nrow = self.table_crit.rowCount()

		self.table_crit.insertRow(nrow)
		item = QTableWidgetItem()
		item.setFlags(Qt.ItemIsTristate)
		self.table_crit.setItem(nrow, 0, item)

		checkbox = QCheckBox(self)
		checkbox.setCheckState(Qt.Checked)
		checkbox.setText(QApplication.translate("MainWindow", name, None, QApplication.UnicodeUTF8))
		self.table_crit.setCellWidget(nrow, 0, checkbox)

	def set_data(self):
		for crit in criterions:
			self.add_criteria(crit)
    
	@pyqtSignature("int, int")
	def on_table_crit_cellEntered(self, row, column):
		"""
		Slot documentation goes here.
		"""
		# TODO: not implemented yet
		raise NotImplementedError
