from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
import sys, os

from etrimain import EtriMainWindow

class etri_plugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/etri/etri.png"), "Electre Tri Plugin", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        ui = EtriMainWindow(self.iface)

        mapCanvas = self.iface.mapCanvas()
        for i in range(mapCanvas.layerCount()):
            layer = mapCanvas.layer(i)
            ui.add_crit_layer(layer)

        ui.show()
