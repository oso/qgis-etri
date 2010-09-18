import colorsys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

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
    sr = QgsUniqueValueRenderer(QGis.Polygon)
    sr.setClassificationField(0)

    for i in range(1, nprofils+2):
        s = QgsSymbol(QGis.Polygon)
        r, g, b = colorsys.hls_to_rgb(0+float(i)/(nprofils+1), 0.5, 0.5)
        s.setBrush(QBrush(QColor(r*255, g*255, b*255)))
        label = 'Category %d' % i
        s.setLabel(label)
        s.setLowerValue(str(i))
        s.setUpperValue(str(i))
        sr.insertValue(str(i), s)

    layer.setRenderer(sr)
