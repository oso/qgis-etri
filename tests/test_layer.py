from qgis.testing import start_app
from qgis.core import QgsVectorLayer
from qgis_etri.layer import criteria_layer

if __name__ == "__main__":

    start_app()

    layer = QgsVectorLayer("./data/ticino/criteria.shp", "criteria", "ogr")
    if not layer.isValid():
        raise NameError("Layer failed to load!")

    layer = criteria_layer(layer)

    print(layer.criteria)
    print(layer.alternatives)
    print(layer.pt)
