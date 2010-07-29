#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
from qgis.core import *
from qgis.gui import *

from Ui_mainwindow import Ui_MainWindow

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		self.canvas = QgsMapCanvas()
		self.canvas.setCanvasColor(QtGui.QColor(255,255,255))
		self.canvas.enableAntiAliasing(True)
		self.canvas.show()

		self.layout = QtGui.QVBoxLayout(self.map_frame)
		self.layout.addWidget(self.canvas)

		# create the actions behaviours
		self.connect(self.mpActionAddLayer, QtCore.SIGNAL("triggered()"), self.addLayer)
#		self.connect(self.mpActionZoomIn, QtCore.SIGNAL("triggered()"), self.zoomIn)
#		self.connect(self.mpActionZoomOut, QtCore.SIGNAL("triggered()"), self.zoomOut)
#		self.connect(self.mpActionPan, QtCore.SIGNAL("triggered()"), self.pan)

		# create a little toolbar
		self.toolbar = self.addToolBar("File");
		self.toolbar.addAction(self.mpActionAddLayer);
#		self.toolbar.addAction(self.mpActionZoomIn);
#		self.toolbar.addAction(self.mpActionZoomOut);
#		self.toolbar.addAction(self.mpActionPan);

#		# create the map tools
#		self.toolPan = QgsMapToolPan(self.canvas)
#		self.toolPan.setAction(self.mpActionPan)
#		self.toolZoomIn = QgsMapToolZoom(self.canvas, False)
#		self.toolZoomIn.setAction(self.mpActionZoomIn)
#		self.toolZoomOut = QgsMapToolZoom(self.canvas, True)
#		self.toolZoomOut.setAction(self.mpActionZoomOut)

	def zoomIn(self):
		self.canvas.setMapTool(self.toolZoomIn)

	def zoomOut(self):
		self.canvas.setMapTool(self.toolZoomOut)

	def pan(self):
		self.canvas.setMapTool(self.toolPan)

	def addLayer(self):
		"""add a (hardcoded) layer and zoom to its extent"""

		layerPath = "/home/oso/qgis_france/DEPARTEMENT.SHP"
		layerName = "DEPARTEMENT"
		layerProvider = "ogr"
		layer = QgsVectorLayer(layerPath, layerName, layerProvider)

		if not layer.isValid():
			return

		QgsMapLayerRegistry.instance().addMapLayer(layer);

		self.canvas.setExtent(layer.extent())

		cl = QgsMapCanvasLayer(layer)
		layers = [cl]
		self.canvas.setLayerSet(layers)

#		layerPath = "/home/oso/qgis_france/DEPARTEMENT.SHP"
#		layerName = "DEPARTEMENT"
#		layerProvider = "ogr"
#		layer = QgsVectorLayer(layerPath, layerName, layerProvider)
#
#		if not layer.isValid():
#			return
#
#		QgsMapLayerRegistry.instance().addMapLayer(layer);
#
#		self.canvas.setExtent(layer.extent())
#
#		cl = QgsMapCanvasLayer(layer)
#		layers = [cl]
#		self.canvas.setLayerSet(layers)
