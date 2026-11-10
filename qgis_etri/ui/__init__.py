import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")

from qgis.PyQt import uic

_UI_DIR = os.path.dirname(os.path.abspath(__file__))

Ui_main_window, _ = uic.loadUiType(os.path.join(_UI_DIR, "main_window.ui"))
Ui_inference_results, _ = uic.loadUiType(os.path.join(_UI_DIR,
                                                       "inference_results.ui"))
