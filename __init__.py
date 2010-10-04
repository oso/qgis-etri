from etri_plugin import etri_plugin

def name():
    return "Electre Tri plugin"

def description():
    return "A simple Electre Tri plugin"

def version():
    return "0.1.1"

def qgisMinimumVersion():
    return "1.4"

def authorName():
    return "Olivier Sobrie"

def classFactory(iface):
    return etri_plugin(iface)
