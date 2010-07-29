from qgis.core import *
import sys

class qgis_criterions_layer:

	def __init__(self, layer):
		self.layer = layer
		self.provider = self.layer.dataProvider()
		self.criterions = self.provider.attributeIndexes()

	def get_fields(self):
		return self.provider.fields()

	def get_fieldnames(self):
		fields = self.provider.fields()
		names = []
		for (i, field) in fields.iteritems():
			str = '"%s"' % field.name().trimmed()
			names.append(str)
		return names

	def get_criterion_names(self):
		fields = self.provider.fields()
		names = []
		for (i, field) in fields.iteritems():
			if i in self.criterions:
				name = '"%s"' % field.name().trimmed()
				names.append(name)
		return names

	def get_actions(self):
		feat = QgsFeature()
		self.provider.select(self.criterions, QgsRectangle(), False)
	
		actions = []
		while self.provider.nextFeature(feat):
			attrs = feat.attributeMap()
			action = []
			for (k,attr) in attrs.iteritems():
				val = attr.toDouble()
				action.append(val[0])
	
			actions.append(action)
	
		return actions

def main(argv):
	QgsApplication.setPrefixPath("/usr", True)
	QgsApplication.initQgis()

	layerPath = "/home/oso/tfe/qgis_data/france.shp"
	layerName = "criterions"
	layerProvider = "ogr"

	layer = QgsVectorLayer(layerPath, layerName, layerProvider)
	if not layer.isValid():
		print "Layer failed to load!"

	clayer = qgis_criterions_layer(layer)
	print "fields\n", clayer.get_fieldnames()
	print "criterions\n", clayer.get_criterion_names()
	print "actions\n", clayer.get_actions()

	QgsApplication.exitQgis()
	
if __name__ == "__main__":
	main(sys.argv)
