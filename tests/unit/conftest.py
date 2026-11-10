import os
import shutil

# Must be set before the Qt application is created
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from qgis.testing import start_app

DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "data")


@pytest.fixture(scope="session")
def qgis_app():
    return start_app()


@pytest.fixture
def no_message_box(monkeypatch):
    """Record QMessageBox calls instead of opening blocking dialogs."""
    from qgis.PyQt.QtWidgets import QMessageBox

    calls = []

    def record(kind):
        def box(*args, **kwargs):
            calls.append((kind, args))
            return QMessageBox.StandardButton.Yes
        return staticmethod(box)

    for kind in ("information", "warning", "question", "critical"):
        monkeypatch.setattr(QMessageBox, kind, record(kind))

    return calls


SHP_EXTENSIONS = (".shp", ".shx", ".dbf", ".prj")


@pytest.fixture
def make_window(qgis_app, tmp_path, no_message_box):
    """Return a function opening the main window on a copy of a test
    layer. The .xmcda model is copied too unless xmcda is False, or
    replaced by the given string."""
    from qgis.core import QgsVectorLayer
    from qgis_etri.main import main_window

    windows = []

    def make(dataset="loulouka", xmcda=True):
        src = os.path.join(DATA_DIR, dataset, "criteria")
        dst = str(tmp_path / "criteria")
        for ext in SHP_EXTENSIONS:
            shutil.copy(src + ext, dst + ext)
        if xmcda is True:
            shutil.copy(src + ".xmcda", dst + ".xmcda")
        elif xmcda:
            with open(dst + ".xmcda", "w") as f:
                f.write(xmcda)

        layer = QgsVectorLayer(dst + ".shp", "criteria", "ogr")
        assert layer.isValid()
        window = main_window(layer=layer)
        # Keep the layer alive as long as the window
        window._test_layer = layer
        windows.append(window)
        return window

    yield make

    for window in windows:
        window.deleteLater()
