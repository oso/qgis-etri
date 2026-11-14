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


def one_threshold_per_profile(xmcda):
    """Replace the 'b' threshold of the q, p and v tables by the same
    threshold for each profile (b1, b2), with a different value."""
    def per_profile(match):
        ap = match.group(0)
        b1 = ap.replace('"b"', '"b1"').replace('>b<', '>b1<')
        b2 = ap.replace('"b"', '"b2"').replace('>b<', '>b2<')
        b2 = re.sub(r'<integer>(\d+)</integer>',
                    lambda m: '<integer>%d</integer>' % (int(m[1]) + 1), b2)
        return b1 + b2
    return re.sub(r'<alternativePerformances id="b">.*?'
                  r'</alternativePerformances>', per_profile, xmcda)


@pytest.fixture
def load_xmcda(monkeypatch, tmp_path):
    """Return a function loading an XMCDA string with the 'Load' button"""
    import qgis_etri.main

    def load(window, xmcda):
        path = str(tmp_path / "model.xmcda")
        with open(path, "w") as f:
            f.write(xmcda)
        monkeypatch.setattr(qgis_etri.main, "saveDialog",
                            lambda *args: (path, "UTF-8"))
        window.on_button_loadxmcda_pressed()

    return load


def test_load_model_with_thresholds_after_mrsort_model(make_window,
                                                       load_xmcda):
    window = make_window("ticino", ticino_xmcda(q=None, p=None, v=None))
    assert window.cbox_mrsort.isChecked()
    assert window.cbox_noveto.isChecked()

    load_xmcda(window, ticino_xmcda())

    assert not window.cbox_mrsort.isChecked()
    assert not window.cbox_noveto.isChecked()
    assert threshold_tabs(window) == [window.tab_indiff, window.tab_pref,
                                      window.tab_veto]
    assert window.qpt['b'].performances['PRICE'] == 15
    assert window.ppt['b'].performances['PRICE'] == 40
    assert window.vpt['b'].performances['PRICE'] == 100
    assert window.table_indiff.item(0, 0).text() == "15"
    assert window.table_veto.item(0, 0).text() == "100"


def test_load_model_with_one_threshold_per_profile(make_window, load_xmcda):
    window = make_window("ticino")
    assert window.cbox_samethresholds.isChecked()

    load_xmcda(window, one_threshold_per_profile(ticino_xmcda()))

    assert not window.cbox_samethresholds.isChecked()
    assert window.qpt.keys() == ['b1', 'b2']
    assert window.qpt['b2'].performances['PRICE'] == 16
    assert window.table_indiff.rowCount() == 2
    assert window.table_indiff.item(1, 0).text() == "16"


def test_save_and_load_xmcda(make_window, load_xmcda, tmp_path):
    window = make_window("ticino")
    path = str(tmp_path / "saved.xmcda")
    window.save_to_xmcda(path)

    with open(path) as f:
        saved = f.read()
    assert saved.startswith('<xmcda:XMCDA xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">')

    window2 = make_window("ticino", ticino_xmcda(q=None, p=None, v=None))
    load_xmcda(window2, saved)

    assert list(window2.criteria) == list(window.criteria)
    assert list(window2.cv) == list(window.cv)
    for pt in ['bpt', 'qpt', 'ppt', 'vpt']:
        assert list(getattr(window2, pt)) == list(getattr(window, pt))
    assert window2.spinbox_cutlevel.value() == window.spinbox_cutlevel.value()
