import os
import re

import pytest

from conftest import DATA_DIR


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


def ticino_xmcda(**tables):
    """Return the Ticino model, with the threshold tables given as
    keyword arguments ('q', 'p' or 'v') removed (None) or emptied ('')."""
    with open(os.path.join(DATA_DIR, "ticino", "criteria.xmcda")) as f:
        xmcda = f.read()
    for tid, content in tables.items():
        pattern = r'<performanceTable id="%s">.*?</performanceTable>' % tid
        if content is None:
            replacement = ''
        else:
            replacement = ('<performanceTable id="%s">%s</performanceTable>'
                           % (tid, content))
        xmcda, n = re.subn(pattern, replacement, xmcda)
        assert n == 1
    return xmcda


def test_load_xmcda(make_window):
    window = make_window("ticino")

    assert window.bpt.keys() == ['b1', 'b2']
    assert window.qpt.keys() == window.ppt.keys() == window.vpt.keys() \
        == ['b']
    assert not window.cbox_mrsort.isChecked()
    assert not window.cbox_noveto.isChecked()


@pytest.mark.parametrize("tables", [
    {'q': '', 'p': None},
    {'q': None, 'p': ''},
    {'q': '', 'p': ''},
    {'q': None, 'p': None},
])
def test_load_xmcda_without_q_and_p(make_window, tables):
    window = make_window("ticino", ticino_xmcda(**tables))

    # The model is loaded from the file, not generated
    assert window.bpt.keys() == ['b1', 'b2']
    assert window.qpt is None and window.ppt is None
    assert window.cbox_mrsort.isChecked()


@pytest.mark.parametrize("tables", [
    {'q': ''}, {'q': None}, {'p': ''}, {'p': None},
])
def test_load_xmcda_with_only_q_or_p(make_window, tables):
    window = make_window("ticino", ticino_xmcda(**tables))

    assert window.bpt.keys() == ['b1', 'b2']
    assert window.qpt.keys() == window.ppt.keys() == ['b']
    assert window.qpt['b'].performances == window.ppt['b'].performances
    assert not window.cbox_mrsort.isChecked()


def test_load_xmcda_with_empty_veto(make_window):
    window = make_window("ticino", ticino_xmcda(v=''))

    assert window.bpt.keys() == ['b1', 'b2']
    assert window.vpt is None
    assert window.cbox_noveto.isChecked()


def threshold_tabs(window):
    tabs = window.tab_thresholds
    return [tabs.widget(i) for i in range(tabs.count())]


def test_mrsort_and_veto_checkboxes_toggle_tabs(make_window):
    window = make_window("ticino")
    indiff, pref, veto = window.tab_indiff, window.tab_pref, window.tab_veto
    assert threshold_tabs(window) == [indiff, pref, veto]

    window.cbox_mrsort.setChecked(True)
    assert threshold_tabs(window) == [veto]

    window.cbox_noveto.setChecked(True)
    assert threshold_tabs(window) == []

    window.cbox_mrsort.setChecked(False)
    assert threshold_tabs(window) == [indiff, pref]

    window.cbox_noveto.setChecked(False)
    assert threshold_tabs(window) == [indiff, pref, veto]
