from etri_plugin import etri_plugin

def name():
    return "Electre Tri plugin"

def description():
    return "A decision aid plugin based on ELECTRE TRI"

def version():
    return "0.3.1"

def qgisMinimumVersion():
    return "1.4"

def author():
    return "Olivier Sobrie"

def email():
    return "olivier@sobrie.be"

def classFactory(iface):
    return etri_plugin(iface)
