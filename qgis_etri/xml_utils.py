"""
Safe XML parsing helpers.

XMCDA files loaded by the plugin may come from untrusted sources. To protect
against XML attacks (billion laughs, external entity expansion, ...) any
document containing a DTD or an entity declaration is rejected before being
handed over to ElementTree.
"""

# Only parsed via safe_parse()

from xml.etree import ElementTree  # nosec B405
from xml.parsers import expat


class UnsafeXMLError(ValueError):
    pass


def _forbid_dtd(*args):
    raise UnsafeXMLError("DTD are not allowed in XML documents")


def _forbid_entity(*args):
    raise UnsafeXMLError("Entities are not allowed in XML documents")


def _check_xml(data):
    parser = expat.ParserCreate()
    parser.StartDoctypeDeclHandler = _forbid_dtd
    parser.EntityDeclHandler = _forbid_entity
    parser.UnparsedEntityDeclHandler = _forbid_entity
    parser.ExternalEntityRefHandler = _forbid_entity
    parser.Parse(data, True)


def safe_fromstring(data):
    _check_xml(data)
    # Checked by _check_xml()
    return ElementTree.fromstring(data)  # nosec B314


def safe_parse(source):
    with open(source, "rb") as f:
        data = f.read()
    return ElementTree.ElementTree(safe_fromstring(data))
