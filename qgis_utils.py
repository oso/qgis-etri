import os
import colorsys

from PyQt4 import QtGui, QtCore
from qgis.core import *
from qgis.gui import *

def layer_get_criteria(layer):
    minmax = layer_get_minmax(layer)
    mins = minmax['mins']
    maxs = minmax['maxs']

    provider = layer.dataProvider()
    fields = provider.fields()
    i = 0
    criteria = []
    for (id, field) in fields.iteritems():
        #FIXME: Check the type to only include numbers
        criterion = {}
        str = '%s' % field.name().trimmed()
        criterion['name'] = str
        criterion['id'] = id
        criterion['min'] = mins[id]
        criterion['max'] = maxs[id]
        criterion['mean'] = (maxs[id]+mins[id])/2
        criterion['diff'] = maxs[id]-mins[id]
        criteria.append(criterion)

    return criteria

def layer_get_minmax(layer):
    provider = layer.dataProvider()
    allAttrs = provider.attributeIndexes()
    provider.select(allAttrs)
    feat = QgsFeature()

    first = True
    mins = {}
    maxs = {}
    while provider.nextFeature(feat):
        attrs = feat.attributeMap()
        for (k, attr) in attrs.iteritems():
            value = attr.toDouble()[0]
            if first == True:
                mins[k] = value
                maxs[k] = value
            else:
                if value < mins[k]:
                    mins[k] = value
                if value > maxs[k]:
                    maxs[k] = value

        first = False

    return {'mins': mins, 'maxs': maxs}

def layer_load(path, name):
    layerProvider = "ogr"
    layer = QgsVectorLayer(path, name, layerProvider)
    if not layer.isValid():
        raise NameError,"Layer failed to load!"

    return layer

def layer_get_feature_attribute(layer, featid):
    provider = layer.dataProvider()
    feat = QgsFeature()
    allAttrs = provider.attributeIndexes()
    provider.featureAtId(featid, feat, False, allAttrs)
    attrs = feat.attributeMap()

    attributes = {}
    for (k, attr) in attrs.iteritems():
        try:
            attributes[k] = str(attr.toString()).trimmed()
        except:
            attributes[k] = attr.toString().trimmed()

    return attributes

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

def generate_decision_map(layer_in, aa, out, out_encoding):
    vprovider = layer_in.dataProvider()
    allAttrs = vprovider.attributeIndexes()
    fields = QgsFields()
    fields.append(QgsField("Category", QtCore.QVariant.Int))

    try:
        os.unlink(out)
    except:
        pass

    writer = QgsVectorFileWriter(out, out_encoding, fields, vprovider.geometryType(), vprovider.crs())

    outFeat = QgsFeature(fields)
    nFeat = vprovider.featureCount()

    for feat in layer_in.getFeatures():
        inGeom = feat.geometry()
        inGeom = QgsGeometry()
        id = str(feat.id())
        if inGeom is not None:
            outFeat.setGeometry(inGeom)
        outFeat.setAttribute(0, aa[id].category_id)
        writer.addFeature(outFeat)

    del writer

def saveDialog(parent, title, filtering, extension, acceptmode):
    settings = QtCore.QSettings()

    try:
        dirName = settings.value("/UI/lastShapefileDir").toString()
    except:
        dirName = str(settings.value("/UI/lastShapefileDir"))

    try:
        encode = settings.value("/UI/encoding").toString()
    except:
        encode = str(settings.value("/UI/encoding"))

    fileDialog = QgsEncodingFileDialog(parent, title, dirName,
                                       filtering, encode)
    fileDialog.setDefaultSuffix(extension)
    fileDialog.setFileMode(QtGui.QFileDialog.AnyFile)
    fileDialog.setAcceptMode(acceptmode)
    fileDialog.setConfirmOverwrite(True)
    if not fileDialog.exec_() == QtGui.QDialog.Accepted:
            return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastShapefileDir",
                      QtCore.QFileInfo(unicode(files[0])).absolutePath())

    return (unicode(files[0]), unicode(fileDialog.encoding()))

def addtocDialog(parent, filename, nprofils):
    addToTOC = QtGui.QMessageBox.question(parent,
                    "Decision MAP layer created",
                    "Would you like to add the new layer to the TOC?",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,
                    QtGui.QMessageBox.NoButton)

    if addToTOC == QtGui.QMessageBox.Yes:
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]
        vlayer = QgsVectorLayer(filename, name, "ogr")
        render_decision_map(vlayer, nprofils)

        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

def render_decision_map_new(layer, nprofils):
    cat_list = []
    nclasses = nprofils + 1
    for i in range(1, nclasses + 1):
        s = QgsSymbolV2.defaultSymbol(layer.geometryType())
        color = QtGui.QColor(0,
                             255 - 220 * i / nclasses,
                             0)
        s.setColor(color)
        cat_list.append(QgsRendererCategoryV2(i, s, "Category %d" % i))

    sr = QgsCategorizedSymbolRendererV2("categories", cat_list)
    sr.setClassAttribute("category")
    layer.setRendererV2(sr)

def render_decision_map(layer, nprofils):
    render_decision_map_new(layer, nprofils)
