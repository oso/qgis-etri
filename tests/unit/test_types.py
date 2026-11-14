from fractions import Fraction

import pytest

from qgis_etri.mcda.types import AlternativePerformances, marshal
from qgis_etri.mcda.types import unmarshal_value
from qgis_etri.mcda.xml_writer import tostring
from qgis_etri.xml_utils import safe_fromstring


@pytest.mark.parametrize("value, expected", [
    (3, b'<integer>3</integer>'),
    (True, b'<integer>1</integer>'),
    (1.5, b'<real>1.5</real>'),
    (Fraction(3, 2), b'<real>1.5</real>'),
])
def test_marshal_numbers(value, expected):
    assert tostring(marshal(value)) == expected


@pytest.mark.parametrize("value", [None, "1.5"])
def test_marshal_rejects_non_numbers(value):
    with pytest.raises(TypeError):
        marshal(value)


def test_performances_round_trip():
    ap = AlternativePerformances('a1', {'c1': Fraction(1, 2), 'c2': 3,
                                        'c3': None})

    buf = tostring(ap.to_xmcda())
    loaded = AlternativePerformances().from_xmcda(safe_fromstring(buf))

    assert loaded.performances == {'c1': 0.5, 'c2': 3, 'c3': None}


@pytest.mark.parametrize("value, expected", [
    (b'<value><real>1.5</real></value>', 1.5),
    (b'<value><integer>2</integer></value>', 2),
    (b'<value>1.5</value>', 1.5),
    (b'<value> 2 </value>', 2),
    (b'<value>None</value>', None),
    (b'<value />', None),
])
def test_unmarshal_value(value, expected):
    result = unmarshal_value(safe_fromstring(value))

    assert result == expected
    assert type(result) is type(expected)


def test_performances_untyped_values():
    xml = (b'<alternativePerformances>'
           b'<alternativeID>a1</alternativeID>'
           b'<performance><criterionID>c1</criterionID>'
           b'<value>1.5</value></performance>'
           b'<performance><criterionID>c2</criterionID>'
           b'<value>None</value></performance>'
           b'</alternativePerformances>')

    ap = AlternativePerformances().from_xmcda(safe_fromstring(xml))

    assert ap.performances == {'c1': 1.5, 'c2': None}
