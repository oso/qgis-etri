from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

def xmcda_save_dialog(parent):
    settings = QSettings() 
    dirName = settings.value("/UI/lastXMCDAfileDir").toString()
    filtering = QString( "XMCDA files (*.xmcda)" )
    encode = settings.value( "/UI/encoding" ).toString()
    fileDialog = QgsEncodingFileDialog( parent, "Save output XMCDA file", dirName, filtering, encode )
    fileDialog.setDefaultSuffix( QString( "xmcda" ) )
    fileDialog.setFileMode( QFileDialog.AnyFile )
    fileDialog.setAcceptMode( QFileDialog.AcceptSave )
    fileDialog.setConfirmOverwrite( True )
    if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastXMCDAfileDir", QVariant( QFileInfo( unicode( files.first() ) ).absolutePath() ) )
    return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )

def xmcda_load_dialog(parent):
    settings = QSettings() 
    dirName = settings.value("/UI/lastXMCDAfileDir").toString()
    filtering = QString( "XMCDA files (*.xmcda)" )
    encode = settings.value( "/UI/encoding" ).toString()
    fileDialog = QgsEncodingFileDialog( parent, "Load input XMCDA file", dirName, filtering, encode )
    fileDialog.setDefaultSuffix( QString( "xmcda" ) )
    fileDialog.setFileMode( QFileDialog.AnyFile )
    fileDialog.setAcceptMode( QFileDialog.AcceptOpen )
    fileDialog.setConfirmOverwrite( False )
    if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastXMCDAfileDir", QVariant( QFileInfo( unicode( files.first() ) ).absolutePath() ) )
    return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )
