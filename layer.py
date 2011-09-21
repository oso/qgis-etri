from qgis.core import QgsVectorLayer
from mcda import criterion

class criteria_layer(QgsVectorLayer):

    def __init__(self, layer):
        self.layer = layer

    @property
    def criteria(self):
        provider = self.layer.dataProvider()
        fields = provider.fields()
        criteria = []
        for id, field in fields.iteritems():
            name = str(field.name().trimmed())
            crit = criterion(id, name)
            criteria.append(crit)

        return criteria
