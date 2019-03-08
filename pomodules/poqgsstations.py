from PyQt5.QtCore import QVariant
from qgis.core import (QgsGeometry,
                       QgsFeature,
                       QgsField,
                       QgsFields,
                       QgsPoint,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)

from pomodules.stations import Stations

class PoQgsStations(Stations):

    def __init__(self):
        Stations.__init__(self)

        self.fields = None
        self.crs = None

    def getFeatures(self):
        data = self.getData()
        # 'uuid', 'number', 'shortname', 'longname', 'km', 'agency'
        self.fields = QgsFields()
        self.fields.append(QgsField(self._attdef[0], QVariant.String))
        self.fields.append(QgsField(self._attdef[1], QVariant.Int))
        self.fields.append(QgsField(self._attdef[2], QVariant.String))
        self.fields.append(QgsField(self._attdef[3], QVariant.String))
        self.fields.append(QgsField(self._attdef[4], QVariant.Double))
        self.fields.append(QgsField(self._attdef[5], QVariant.String))

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

    stats = PoQgsStations()
    print(stats.url)
    d = stats.getData()
    print(len(d))

    f = stats.getFeatures()
