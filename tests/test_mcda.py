import sys
sys.path.insert(0, "..")
from mcda.types import Criteria
from qgis_etri.mcda.xml_writer import tostring
from qgis_etri.xml_utils import safe_fromstring
from data_ticino_new import *

crit = c.to_xmcda()
print(tostring(crit).decode())

crit2 = Criteria()
crit2.from_xmcda(safe_fromstring(tostring(crit)))
print(crit2)

xmcda = a.to_xmcda()
print(tostring(xmcda[0]).decode())
print(tostring(xmcda[1]).decode())
