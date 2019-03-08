import sys
import os
from pomodules.urlreader import Urlreader
from pomodules import poBaseURL


class Stations(object):

    def __init__(self):

        self.url = poBaseURL + 'stations.json'
        self._geodef = ('longitude', 'latitude')
        self._attdef = ('uuid', 'number', 'shortname', 'longname',
                        'km', 'agency')

    def getData(self):

        ur = Urlreader(self.url)
        _data = ur.getJsonResponse()
        data = []

        for d in _data:
            try:
                data.append( {
                        'geometry': (d['longitude'], d['latitude']),
                        'attributes': [d[k] for k in self._attdef]
                    })
            except Exception as e:
                continue

        return data

if __name__ == '__main__':

    stats = Stations()
    print(stats.url)
    d = stats.getData()
    print(len(d))