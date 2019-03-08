from PyQt5.QtCore import QVariant
from qgis.core import (QgsGeometry,
                       QgsFeature,
                       QgsField,
                       QgsFields,
                       QgsPoint,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)

from pomodules.currentw import CurrentW

class PoQgsCurrentW(CurrentW):

    def __init__(self):
        CurrentW.__init__(self)

        self.fields = None
        self.crs = None

    def getFeatures(self):
        data = self.getData()
        # 'uuid', 'shortname', 'time', 'value'
        self.fields = QgsFields()
        self.fields.append(QgsField(self._attdef[0], QVariant.String))
        self.fields.append(QgsField(self._attdef[1], QVariant.String))
        self.fields.append(QgsField(self._attdef[2], QVariant.Time))
        self.fields.append(QgsField(self._attdef[3], QVariant.Double))

        self.crs = QgsCoordinateReferenceSystem().fromSrsId(4326)

        features = []
        for d in data:
            f = QgsFeature(self.fields)

            f.setGeometry(QgsPoint(*d['geometry']))
            for i in range(len(self._attdef)):
                a = self._attdef[i]
                v = d['attributes'][i]
                f[a] = v
            features.append(f)

        return features

if __name__ == '__main__':

    stats = PoQgsCurrentW()
    print(stats.url)
    d = stats.getData()
    print(len(d))

    f = stats.getFeatures()