import pytest

from qgis_etri.xml_utils import UnsafeXMLError, safe_fromstring, safe_parse


def test_safe_parse(tmp_path):
    f = tmp_path / "ok.xmcda"
    f.write_bytes(b'<?xml version="1.0"?><x:XMCDA xmlns:x="urn:x">'
                  b'<criteria /></x:XMCDA>')

    assert safe_parse(str(f)).getroot().find('.//criteria') is not None


@pytest.mark.parametrize("data", [
    b'<!DOCTYPE a [<!ENTITY e "e">]><a>&e;</a>',
    b'<!DOCTYPE a [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;">]><a>&b;</a>',
    b'<!DOCTYPE a SYSTEM "file:///etc/passwd"><a />',
    b'<!DOCTYPE a [<!ENTITY e SYSTEM "file:///etc/passwd">]><a>&e;</a>',
])
def test_safe_fromstring_rejects_dtd(data):
    with pytest.raises(UnsafeXMLError):
        safe_fromstring(data)
