import sys
sys.path.insert(0, "..")
from mcda.types import criterion
from xml.etree import ElementTree
from data_ticino_new import *

crit = c.to_xmcda()
ElementTree.dump(crit)

crit2 = criteria()
crit2.from_xmcda(crit)
print crit2

xmcda = a.to_xmcda()
ElementTree.dump(xmcda[0])
ElementTree.dump(xmcda[1])

#a = a1.to_xmcda()
#ElementTree.dump(a[0])
#ElementTree.dump(a[1])
