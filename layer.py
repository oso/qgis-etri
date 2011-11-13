from qgis.core import QgsVectorLayer, QgsFeature
from mcda.types import criteria, criterion, alternative, alternatives
from mcda.types import performance_table, alternative_performances

class criteria_layer(QgsVectorLayer):

    def __init__(self, layer):
        self.layer = layer
        self.criteria = None
        self.alternatives = None
        self.pt = None
        self.get_criteria()
        self.get_alternatives_and_pt()

    def get_criteria(self):
        provider = self.layer.dataProvider()
        fields = provider.fields()
        self.criteria = criteria([])
        for id, field in fields.iteritems():
            name = str(field.name().trimmed())
            crit = criterion(str(id), name)
            self.criteria.append(crit)

    def get_alternatives_and_pt(self):
        provider = self.layer.dataProvider()
        attrib_index = provider.attributeIndexes()
        provider.select(attrib_index)
        feat = QgsFeature()

        self.alternatives = alternatives([])
        self.pt = performance_table([])
        while provider.nextFeature(feat):
            attrs = feat.attributeMap()
            perfs = {}
            for (k, attr) in attrs.iteritems():
                perfs[str(k)] = attr.toDouble()[0]
            self.alternatives.append(alternative(str(feat.id()),
                                                 str(feat.id())))
            self.pt.append(alternative_performances(str(feat.id()), perfs))

def layer_get_attributes(layer):
    provider = layer.dataProvider()
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)
    feat = QgsFeature()

    actions = {}
    while provider.nextFeature(feat):
        attrs = feat.attributeMap()
        attributes = {}
        for (k, attr) in attrs.iteritems():
            attributes[k] = attr.toDouble()[0]

        actions[feat.id()] = attributes

    return actions
