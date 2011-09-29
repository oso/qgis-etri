import sys
sys.path.insert(0, "..")
from data_ticino_new import *
from mcda.types import criterion
from xml.etree import ElementTree

ElementTree.dump(criteria.to_xmcda())
