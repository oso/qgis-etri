import sys
sys.path.append("..")
import os
from qgis.core import QgsVectorLayer, QgsApplication
from layer import criteria_layer

if __name__ == "__main__":
    QgsApplication.setPrefixPath("/usr", True)
    QgsApplication.initQgis()

    layer = QgsVectorLayer("./data/ticino/criteria.shp", "criteria", "ogr")
    if not layer.isValid():
        raise NameError("Layer failed to load!")

    layer = criteria_layer(layer)

    print(layer.criteria)

    QgsApplication.exitQgis()
