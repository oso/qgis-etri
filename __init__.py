from etri_plugin import etri_plugin

def name():
    return "Electre Tri plugin"

def description():
    return "A decision aid plugin based on ELECTRE TRI"

def version():
    return "0.3"

def qgisMinimumVersion():
    return "1.4"

def authorName():
    return "Olivier Sobrie"

def classFactory(iface):
    return etri_plugin(iface)
