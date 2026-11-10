import os
import shutil

import pytest
from qgis.core import QgsVectorLayer

from conftest import DATA_DIR

SHP_EXTENSIONS = (".shp", ".shx", ".dbf", ".prj")


@pytest.fixture
def make_window(qgis_app, tmp_path, no_message_box):
    """Return a function opening the main window on a copy of a test
    layer. The .xmcda model is copied too unless xmcda is False, or
    replaced by the given string."""
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


def test_initial_profile_is_in_the_middle_of_the_range(make_window):
    window = make_window(xmcda=False)

    mins = window.pt.get_min().performances
    maxs = window.pt.get_max().performances
    b1 = window.bpt['b1'].performances
    assert len(window.bpt) == 1
    for c in window.criteria:
        assert b1[c.id] == pytest.approx((mins[c.id] + maxs[c.id]) / 2)
        assert mins[c.id] <= b1[c.id] <= maxs[c.id]
