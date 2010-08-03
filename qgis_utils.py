from qgis.core import *
from qgis.gui import *

def layer_get_criterions(layer):
    provider = layer.dataProvider()
    fields = provider.fields()
    criterions = []
    for (i, field) in fields.iteritems():
        str = '%s' % field.name().trimmed()
        criterions.append(str)

    return criterions

def layer_load(path, name):
    layerProvider = "ogr"
    layer = QgsVectorLayer(path, name, layerProvider)
    if not layer.isValid():
        raise NameError,"Layer failed to load!"

    return layer
