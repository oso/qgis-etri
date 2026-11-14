import os
import sys

from qgis.PyQt import uic

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

_UI_DIR = os.path.dirname(os.path.abspath(__file__))

Ui_main_window, _ = uic.loadUiType(os.path.join(_UI_DIR, "main_window.ui"))
