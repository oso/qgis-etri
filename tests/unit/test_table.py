import pytest

from qgis_etri.mcda.types import Alternative, AlternativePerformances
from qgis_etri.mcda.types import Criteria, Criterion
from qgis_etri.mcda.types import CriteriaValues, CriterionValue
from qgis_etri.table import COL_NAME, COL_WEIGHT
from qgis_etri.table import qt_criteria_table, qt_performance_table


@pytest.fixture
def criteria():
    return Criteria([Criterion('g1', 'g1'), Criterion('g2', 'g2')])


@pytest.fixture
def perf_table(qgis_app, criteria):
    ap = AlternativePerformances('b1', {'g1': 1, 'g2': 2})
    table = qt_performance_table(None, criteria)
    table.add(Alternative('b1'), ap)
    return table, ap


@pytest.fixture
def crit_table(qgis_app, criteria):
    cvs = CriteriaValues([CriterionValue('g1', 1), CriterionValue('g2', 1)])
    table = qt_criteria_table()
    table.add_criteria(criteria, cvs)
    return table, cvs


@pytest.mark.parametrize("text, expected", [("42", 42), ("2.5", 2.5)])
def test_performance_edit_updates_model(perf_table, text, expected):
    table, ap = perf_table
    table.item(0, 0).setText(text)
    assert ap.performances == {'g1': expected, 'g2': 2}


def test_performance_cleared_sets_none(perf_table):
    table, ap = perf_table
    table.item(0, 1).setText("")
    assert ap.performances['g2'] is None


@pytest.mark.parametrize("text, expected", [("7", 7), ("0.5", 0.5)])
def test_weight_edit_updates_model(crit_table, text, expected):
    table, cvs = crit_table
    table.item(0, COL_WEIGHT).setText(text)
    assert cvs['g1'].value == expected
    assert cvs['g2'].value == 1


def test_invalid_weight_is_reset_to_zero(crit_table, no_message_box):
    table, cvs = crit_table
    table.item(0, COL_WEIGHT).setText(".")
    assert [kind for kind, _ in no_message_box] == ["warning"]
    assert table.item(0, COL_WEIGHT).text() == "0"
    assert cvs['g1'].value == 0


def test_disabling_criterion_keeps_weight(crit_table, criteria,
                                          no_message_box):
    table, cvs = crit_table
    table.cellWidget(0, COL_NAME).setChecked(False)
    assert criteria['g1'].disabled is True
    assert cvs['g1'].value == 1
    assert no_message_box == []
