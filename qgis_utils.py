import os
import colorsys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

def layer_get_criterions(layer):
    minmax = layer_get_minmax(layer)
    mins = minmax['mins']
    maxs = minmax['maxs']

    provider = layer.dataProvider()
    fields = provider.fields()
    i = 0
    criterions = []
    for (id, field) in fields.iteritems():
        #FIXME: Check the type to only include numbers
        criteria = {}
        print "type=", field.type()
        str = '%s' % field.name().trimmed()
        criteria['name'] = str
        criteria['id'] = id
        criteria['min'] = mins[id]
        criteria['max'] = maxs[id]
        criteria['mean'] = (maxs[id]+mins[id])/2
        criteria['diff'] = maxs[id]-mins[id]
        criterions.append(criteria)

    print 'Criterions', criterions
    return criterions

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
            value = attr.toFloat()[0]
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
            attributes[k] = attr.toFloat()[0]

        actions[feat.id()] = attributes

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
        vlayer = QgsVectorLayer(filename, "decision", "ogr")
        render_decision_map(vlayer, nprofils)

        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

def render_decision_map(layer, nprofils):
    sr = QgsUniqueValueRenderer(layer.geometryType())
    sr.setClassificationField(0)

    for i in range(1, nprofils+2):
        s = QgsSymbol(layer.geometryType())
        r, g, b = colorsys.hls_to_rgb(0+float(i)/(nprofils+1), 0.5, 0.5)
        s.setBrush(QBrush(QColor(r*255, g*255, b*255)))
        label = 'Category %d' % i
        s.setLabel(label)
        s.setLowerValue(str(i))
        s.setUpperValue(str(i))
        sr.insertValue(str(i), s)

    layer.setRenderer(sr)
