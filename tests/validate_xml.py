import sys
from lxml import etree

XMCDA_21 = "http://www.decision-deck.org/xmcda/_downloads/XMCDA-2.1.0.xsd"

xmlschema_doc = etree.parse(XMCDA_21, etree.XMLParser(no_network=False))
xmlschema = etree.XMLSchema(xmlschema_doc)

if len(sys.argv) < 2:
    print("Need one or more xmcda files")

for i in range(1,len(sys.argv)):
    f = sys.argv[i]
    xmltree = etree.parse(open(f, 'r'))
    if xmlschema.validate(xmltree) is True:
        print("%s... OK" % f)
    else:
        print("%s... NOK" % f)
