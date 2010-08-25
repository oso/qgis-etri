from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from ui.mainwindow import MainWindow

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
        print 'Unloading plugin'

    def run(self):
        ui = MainWindow(self.iface.mainWindow())

        mapCanvas = self.iface.mapCanvas()
        for i in range(mapCanvas.layerCount()):
            layer = mapCanvas.layer(i)
            ui.add_crit_layer(layer)
#            if i == 0:
#                ui.set_crit_layer(layer)

        ui.show()
