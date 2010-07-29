from qgis.core import *
import sys

def main(argv):
	QgsApplication.setPrefixPath("/usr", True)
	QgsApplication.initQgis()

	layerPath = "/home/oso/tfe/qgis_data/france.shp"
	layerName = "criterions"
	layerProvider = "ogr"

	layer = QgsVectorLayer(layerPath, layerName, layerProvider)

	if not layer.isValid():
		print "Layer failed to load!"

	provider = layer.dataProvider()
	feat = QgsFeature()
	allAttrs = provider.attributeIndexes()
	print "attributes", allAttrs
	allAttrs = [1, 2, 3]
	print "attributes", allAttrs
	provider.select(allAttrs, QgsRectangle(), False)

	actions = []
	while provider.nextFeature(feat):
#		print "Feature ID %d: \n" % feat.id() ,
		attrs = feat.attributeMap()
		action = []
		for (k,attr) in attrs.iteritems():
			val = attr.toDouble()
			action.append(val[0])

		print action
		actions.append(action)

#	print actions

	QgsApplication.exitQgis()

if __name__ == "__main__":
	main(sys.argv)
