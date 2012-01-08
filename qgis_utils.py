import os
import colorsys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
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

def generate_decision_map(layer_in, affectations, out, out_encoding):
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
    while vprovider.nextFeature(inFeat):
        inGeom = inFeat.geometry()
        id = inFeat.id()
        outFeat.setGeometry(inGeom)
        outFeat.addAttribute(0, affectations[id])
        writer.addFeature(outFeat)
    del writer

def saveDialog(parent):
    settings = QSettings() 
    dirName = settings.value( "/UI/lastShapefileDir" ).toString()
    filtering = QString( "Shapefiles (*.shp)" )
    encode = settings.value( "/UI/encoding" ).toString()
    fileDialog = QgsEncodingFileDialog( parent, "Save output shapefile", dirName, filtering, encode )
    fileDialog.setDefaultSuffix( QString( "shp" ) )
    fileDialog.setFileMode( QFileDialog.AnyFile )
    fileDialog.setAcceptMode( QFileDialog.AcceptSave )
    fileDialog.setConfirmOverwrite( True )
    if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastShapefileDir", QVariant( QFileInfo( unicode( files.first() ) ).absolutePath() ) )
    return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )

def addtocDialog(parent, filename, nprofils):
    addToTOC = QMessageBox.question(parent, "Decision MAP layer created", "Would you like to add the new layer to the TOC?", QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
    if addToTOC == QMessageBox.Yes:
        basename = os.path.basename(filename)
        name = os.path.splitext(basename)[0]
        vlayer = QgsVectorLayer(filename, name, "ogr")
        render_decision_map(vlayer, nprofils)

        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

def render_decision_map_old(layer, nprofils):
    sr = QgsUniqueValueRenderer(layer.geometryType())
    sr.setClassificationField(0)

    nclasses = nprofils+1
    for i in range(nclasses):
        s = QgsSymbol(layer.geometryType())
        color = QColor(0, 255-220*(nclasses-1-i)/(nclasses), 0)
        s.setBrush(QBrush(color))
        label = 'Category %d' % (i+1)
        s.setLabel(label)
        s.setLowerValue(str(i+1))
        s.setUpperValue(str(i+1))
        sr.insertValue(str(i+1), s)

    layer.setRenderer(sr)

def render_decision_map_new(layer, nprofils):
    cat_list = []
    nclasses = nprofils+1
    for i in range(nclasses):
        s = QgsSymbolV2.defaultSymbol(layer.geometryType())
        color = QColor(0, 255-220*(nclasses-1-i)/(nclasses), 0)
        s.setColor(color)
        cat_list.append(QgsRendererCategoryV2(i+1, s, 'Category %d' % (i+1)))

    sr = QgsCategorizedSymbolRendererV2("categories", cat_list)
    sr.setClassAttribute("category")
    layer.setRendererV2(sr)

def render_decision_map(layer, nprofils):
    if layer.isUsingRendererV2():
        render_decision_map_new(layer, nprofils)
    else:
        render_decision_map_old(layer, nprofils)
