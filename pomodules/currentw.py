import sys
import os
from pomodules.urlreader import Urlreader
from pomodules import poBaseURL


class CurrentW(object):

    def __init__(self):

        self.url = poBaseURL + 'stations.json?timeseries=W&includeTimeseries=true&includeCurrentMeasurement=true'
        self._geodef = ('longitude', 'latitude')
        self._attdef = ('uuid', 'shortname', 'time', 'value')

    def getData(self):

        ur = Urlreader(self.url)
        _data = ur.getJsonResponse()
        data = []

        for d in _data:
            try:
                data.append(
                    { 'geometry': ( d['longitude'], d['latitude']),
                      'attributes': ( d['uuid'],
                                      d['shortname'],
                                      d['timeseries'][0]['currentMeasurement']['timestamp'],
                                      d['timeseries'][0]['currentMeasurement']['value']
                                    )
                    })
            except Exception as e:
                continue

        return data

if __name__ == '__main__':

    stats = CurrentW()
    print(stats.url)
    d = stats.getData()
    print(len(d))