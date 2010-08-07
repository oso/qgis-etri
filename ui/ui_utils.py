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

def addtocDialog(parent, filename):
    addToTOC = QMessageBox.question(parent, "Decision MAP layer created", "Would you like to add the new layer to the TOC?", QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
    if addToTOC == QMessageBox.Yes:
        vlayer = QgsVectorLayer(filename, "decision", "ogr")

#        s=QgsSymbol(QGis.Polygon)
#        s.setColor(QColor(255,0,0))
#        s.setBrush(QBrush(QColor(0,255,0)))
#        sr=QgsSingleSymbolRenderer(QGis.Polygon)
#        sr.addSymbol(s)
#        vlayer.setRenderer(sr)

        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
