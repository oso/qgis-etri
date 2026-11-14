import pytest

from qgis_etri.mcda.xml_writer import Element, SubElement, tostring
from qgis_etri.xml_utils import UnsafeXMLError, safe_fromstring, safe_parse


def test_writer_escapes_text_and_attributes():
    root = Element('root', {'xmlns:x': 'urn:x'}, id='a"<&>\n')
    SubElement(root, 'child').text = '<&> "quoted"'
    SubElement(root, 'empty')

    buf = tostring(root)

    assert buf == (b'<root xmlns:x="urn:x" id="a&quot;&lt;&amp;&gt;&#10;">'
                   b'<child>&lt;&amp;&gt; "quoted"</child><empty /></root>')
    parsed = safe_fromstring(buf)
    assert parsed.get('id') == 'a"<&>\n'
    assert parsed.find('child').text == '<&> "quoted"'


def test_writer_xml_declaration():
    assert tostring(Element('a'), xml_declaration=True) == \
        b"<?xml version='1.0' encoding='UTF-8'?>\n<a />"


def test_writer_none_tag():
    root = Element('root')
    SubElement(root, None).text = '1 < 2'

    assert tostring(root) == b'<root>1 &lt; 2</root>'


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
