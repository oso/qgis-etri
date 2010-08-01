from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow
from qgis.core import *
from qgis.gui import *

qgis_prefix = "/usr"

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)

	QgsApplication.setPrefixPath(qgis_prefix, True)
	QgsApplication.initQgis()

	ui = MainWindow()
	ui.show()

	rc = app.exec_()

	QgsApplication.exitQgis()
	sys.exit(rc)
