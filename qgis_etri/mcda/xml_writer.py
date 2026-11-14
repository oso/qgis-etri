"""
.. module:: xml_writer

Minimal XML tree builder and serializer used to export XMCDA documents.

It only implements the subset of the ElementTree API needed to generate XML
(Element, SubElement, set, text, append and tostring), so that ElementTree is
only used to parse documents (see qgis_etri.xml_utils).
"""


def _escape_text(text):
    return text.replace("&", "&amp;").replace("<", "&lt;") \
               .replace(">", "&gt;")


def _escape_attrib(text):
    return _escape_text(text).replace('"', "&quot;") \
                             .replace("\n", "&#10;") \
                             .replace("\r", "&#13;") \
                             .replace("\t", "&#09;")


class Element(object):

    def __init__(self, tag, attrib=None, **extra):
        self.tag = tag
        self.attrib = dict(attrib or {}, **extra)
        self.text = None
        self._children = []

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __iter__(self):
        return iter(self._children)

    def set(self, key, value):
        self.attrib[key] = value

    def get(self, key, default=None):
        return self.attrib.get(key, default)

    def append(self, element):
        self._children.append(element)

    def _serialize(self, write):
        if self.tag is None:
            # Like ElementTree, only write the text and the children
            if self.text is not None:
                write(_escape_text(str(self.text)))
            for child in self._children:
                child._serialize(write)
            return

        write("<" + self.tag)
        for key, value in self.attrib.items():
            write(' %s="%s"' % (key, _escape_attrib(str(value))))

        if self.text is None and not self._children:
            write(" />")
            return

        write(">")
        if self.text is not None:
            write(_escape_text(str(self.text)))
        for child in self._children:
            child._serialize(write)
        write("</%s>" % self.tag)


def SubElement(parent, tag, attrib=None, **extra):
    element = Element(tag, attrib, **extra)
    parent.append(element)
    return element


def tostring(element, xml_declaration=False):
    """Serialize an element tree to UTF-8 encoded bytes."""
    parts = []
    if xml_declaration:
        parts.append("<?xml version='1.0' encoding='UTF-8'?>\n")
    element._serialize(parts.append)
    return "".join(parts).encode("utf-8")
