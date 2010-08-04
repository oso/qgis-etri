from qgis.core import *
from qgis.gui import *

def layer_get_criterions(layer):
    provider = layer.dataProvider()
    fields = provider.fields()
    criterions = []
    for (i, field) in fields.iteritems():
        print "type=", field.type()
        str = '%s' % field.name().trimmed()
        criterions.append(str)

    return criterions

def layer_load(path, name):
    layerProvider = "ogr"
    layer = QgsVectorLayer(path, name, layerProvider)
    if not layer.isValid():
        raise NameError,"Layer failed to load!"

    return layer

def layer_get_minmax(layer):
    provider = layer.dataProvider()
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)
    feat = QgsFeature()

    first = True
    while provider.nextFeature(feat):
        attrs = feat.attributeMap()
        if first == True:
            mins = []
            maxs = []
            for (k, attr) in attrs.iteritems():
                value = attr.toFloat()[0]
                mins.append(value)
                maxs.append(value)
            first = False
        else:
            for (k, attr) in attrs.iteritems():
                value = attr.toFloat()[0]
                if mins[k] > value: mins[k] = value
                if maxs[k] < value: maxs[k] = value

    return [mins, maxs]

def layer_get_values(layer):
    provider = layer.dataProvider()
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)
    feat = QgsFeature()

    actions = []
    while provider.nextFeature(feat):
        attrs = feat.attributeMap()

        action = []
        for (k, attr) in attrs.iteritems():
            value = attr.toFloat()[0]
            action.append(value)
        actions.append(action)

    return actions
