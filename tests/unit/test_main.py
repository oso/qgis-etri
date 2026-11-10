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


@pytest.mark.parametrize("mrsort", [True, False])
def test_delete_profile_with_one_threshold_per_profile(make_window, mrsort):
    window = make_window(xmcda=False)
    window.cbox_samethresholds.setChecked(False)
    window.cbox_mrsort.setChecked(mrsort)
    assert window.cbox_noveto.isChecked()

    window.on_button_add_profile_pressed()
    assert window.bpt.keys() == ['b1', 'b2']
    if not mrsort:
        assert window.qpt.keys() == window.ppt.keys() == ['b1', 'b2']

    window.on_button_del_profile_pressed()
    assert window.bpt.keys() == ['b1']
    assert window.table_prof.rowCount() == 1
    assert len(window.categories) == 2
    assert window.vpt is None
    if mrsort:
        assert window.qpt is None and window.ppt is None
    else:
        assert window.qpt.keys() == window.ppt.keys() == ['b1']
        assert window.table_indiff.rowCount() == 1
        assert window.table_pref.rowCount() == 1
