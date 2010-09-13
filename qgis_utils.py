import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
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

    actions = {}
    while provider.nextFeature(feat):
        attrs = feat.attributeMap()

        action = []
        for (k, attr) in attrs.iteritems():
            value = attr.toFloat()[0]
            action.append(value)

        actions[feat.id()] = action 

    return actions

def generate_decision_map(layer_in, affectations, out, out_encoding):
    print "Generate Decision Map"
    vprovider = layer_in.dataProvider()
    allAttrs = vprovider.attributeIndexes()
    vprovider.select( allAttrs )
    fields = {0:QgsField("Category", QVariant.Int)}

    try:
        os.unlink(out)
    except:
        pass

    writer = QgsVectorFileWriter(out, out_encoding, fields, vprovider.geometryType(), vprovider.crs())

    inFeat = QgsFeature()
    outFeat = QgsFeature()
    inGeom = QgsGeometry()
    nFeat = vprovider.featureCount()
    nElement = 0 
    while vprovider.nextFeature(inFeat):
        inGeom = inFeat.geometry()
        outFeat.setGeometry(inGeom)
        outFeat.addAttribute(0, affectations[nElement])
        writer.addFeature(outFeat)
        nElement += 1
    del writer
