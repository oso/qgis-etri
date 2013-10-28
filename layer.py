from PyQt4.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsFeature
from mcda.types import Criteria, Criterion, Alternative, Alternatives
from mcda.types import PerformanceTable, AlternativePerformances

class criteria_layer(QgsVectorLayer):

    def __init__(self, layer):
        self.layer = layer
        self.criteria = None
        self.alternatives = None
        self.pt = None
        self.get_criteria()
        self.get_alternatives_and_pt()

    def get_criteria(self):
        provider = self.layer.dataProvider()
        fields = provider.fields()
        self.criteria = Criteria([])

        for field in fields:
            ftype = field.type()
            if (ftype != QVariant.Bool) and (ftype != QVariant.Double) \
                                        and (ftype != QVariant.Int) \
                                        and (ftype != QVariant.LongLong):
                continue

            name = str(field.name())
            crit = Criterion(name, name)
            self.criteria.append(crit)

    def get_alternatives_and_pt(self):
        provider = self.layer.dataProvider()
        self.alternatives = Alternatives([])
        self.pt = PerformanceTable([])

        for feat in provider.getFeatures():
            featid = str(feat.id())
            perfs = {}
            for criterion in self.criteria:
                perfs[criterion.id] = float(feat[criterion.id])

            self.alternatives.append(Alternative(featid, featid))
            self.pt.append(AlternativePerformances(featid, perfs))
