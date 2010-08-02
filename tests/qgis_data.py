#!/usr/bin/python

from qgis.core import *
import sys

def load_layer(path, name):
	layerPath = path
	layerName = name
	layerProvider = "ogr"
	layer = QgsVectorLayer(layerPath, layerName, layerProvider)
	if not layer.isValid():
		raise NameError,"Layer failed to load!"

	return layer

def get_field_list(provider):
	fields = provider.fields()
	a = []
	for (i, field) in fields.iteritems():
		print i,":", field.name().trimmed()
		str = '%s' % field.name().trimmed()
		#b = 'coucou'
		a.append(i)
	
	print a

	return fields

def main(argv):
	QgsApplication.setPrefixPath("/usr", True)
	QgsApplication.initQgis()

	layer = load_layer("/home/oso/tfe/qgis_data/france.shp", "criterions")

	provider = layer.dataProvider()
	fields = get_field_list(provider)
	print "fields:", fields

	QgsApplication.exitQgis()


if __name__ == "__main__":
	main(sys.argv)
