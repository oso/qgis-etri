from fractions import Fraction

import pytest

from qgis_etri.mcda.types import AlternativePerformances, marshal
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
