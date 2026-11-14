from qgis_etri.mcda.electre_tri import ElectreTri
from qgis_etri.mcda.generate import generate_categories
from qgis_etri.mcda.generate import generate_categories_profiles
from qgis_etri.mcda.types import AlternativePerformances, PerformanceTable
from qgis_etri.mcda.types import Criteria, Criterion
from qgis_etri.mcda.types import CriteriaValues, CriterionValue
from qgis_etri.mcda.xml_writer import tostring
from qgis_etri.xml_utils import safe_fromstring


def make_model():
    criteria = Criteria([Criterion('g1', 'g1'), Criterion('g2', 'g2')])
    cv = CriteriaValues([CriterionValue('g1', 2), CriterionValue('g2', 3)])
    bpt = PerformanceTable([
        AlternativePerformances('b1', {'g1': 5.0, 'g2': 5.0}),
        AlternativePerformances('b2', {'g1': 10.0, 'g2': 10.0}),
    ])
    cps = generate_categories_profiles(generate_categories(3))
    return ElectreTri(criteria, cv, bpt, 0.75, cps, id='model')


def test_xmcda_round_trip():
    model = make_model()

    xmcda = safe_fromstring(tostring(model.to_xmcda()))
    model2 = ElectreTri().from_xmcda(xmcda)

    assert model2.id == 'model'
    assert model2.lbda == 0.75
    assert list(model2.criteria) == list(model.criteria)
    assert list(model2.cv) == list(model.cv)
    assert list(model2.bpt) == list(model.bpt)
    assert model2.profiles == model.profiles
    assert model2.categories == model.categories
