import os

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
