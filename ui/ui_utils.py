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
        sr = QgsContinuousColorRenderer(QGis.Polygon)
        sr.setClassificationField(0)

        s = QgsSymbol(QGis.Polygon)
        s.setBrush(QBrush(QColor(0,0,255)))
        s.setLowerValue(str(1))
        sr.setMaximumSymbol(s)

        s2 = QgsSymbol(QGis.Polygon)
        s2.setBrush(QBrush(QColor(0,0,100)))
        s2.setLowerValue(str(nprofils+1))
        sr.setMinimumSymbol(s2)

        layer.setRenderer(sr)
