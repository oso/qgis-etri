from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import ui.resources_rc
import sys, os

from main import main_window

class etri_plugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/etri/images/etri.png"), "Electre Tri Plugin", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        ui = main_window(self.iface)
        ui.show()
        ui.exec_()
