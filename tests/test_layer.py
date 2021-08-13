import sys
sys.path.append("..")
import os
from qgis.core import QgsVectorLayer, QgsApplication
from qgis_etri.layer import criteria_layer

if __name__ == "__main__":
    QgsApplication.setPrefixPath("/usr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    layer = QgsVectorLayer("./data/ticino/criteria.shp", "criteria", "ogr")
    if not layer.isValid():
        raise NameError("Layer failed to load!")

    layer = criteria_layer(layer)

    print(layer.criteria)
    print(layer.alternatives)
    print(layer.pt)

    del layer

    qgs.exitQgis()
