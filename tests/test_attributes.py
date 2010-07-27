from qgis.core import *
import sys

def main(argv):
	QgsApplication.setPrefixPath("/usr", True)
	QgsApplication.initQgis()

	layerPath = "/home/oso/qgis_france/DEPARTEMENT.SHP"
	layerName = "DEPARTEMENT"
	layerProvider = "ogr"

	layer = QgsVectorLayer(layerPath, layerName, layerProvider)

	if not layer.isValid():
		print "Layer failed to load!"

	provider = layer.dataProvider()
	feat = QgsFeature()
	allAttrs = provider.attributeIndexes()
	provider.select(allAttrs)

	# retreive every feature with its geometry and attributes
	while provider.nextFeature(feat):

		# fetch geometry
		geom = feat.geometry()
		print "Feature ID %d: " % feat.id() ,

		# show some information about the feature
		if geom.type() == QGis.Point:
			x = geom.asPoint()
			print "Point: " + str(x)
		elif geom.type() == QGis.Line:
			x = geom.asPolyline()
			print "Line: %d points" % len(x)
		elif geom.type() == QGis.Polygon:
			x = geom.asPolygon()
			numPts = 0
			for ring in x:
				numPts += len(ring)
				print "Polygon: %d rings with %d points" % (len(x), numPts)
		else:
			print "Unknown"

		# fetch map of attributes
		attrs = feat.attributeMap()

		# attrs is a dictionary: key = field index, value = QgsFeatureAttribute
		# show all attributes and their values
		for (k,attr) in attrs.iteritems():
			print "%d: %s" % (k, attr.toString())

	QgsApplication.exitQgis()

if __name__ == "__main__":
	main(sys.argv)
