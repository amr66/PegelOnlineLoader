import sys
import os
from qgis.core import (
     QgsApplication,
     QgsUserProfile,
     QgsProcessingFeedback,
     QgsVectorLayer
)

# See https://gis.stackexchange.com/a/155852/4972 for details about the prefix
pre = os.environ['QGIS_PREFIX_PATH']
home = os.environ['HOME']
QgsApplication.setPrefixPath(pre, True)

qgs = QgsApplication([], False, profileFolder="%s/.qgis3/profiles/default"%home)
qgs.initQgis()
print (QgsApplication.qgisSettingsDirPath())

# Append the path where processing plugin can be found
sys.path.append(pre + '\\python\\plugins')

import processing
from processing.core.Processing import Processing
Processing.initialize()

# parameters needed by the algorithm
params = {
    'Query' : 0,
    'Result' : 'c:/temp/stations.shp'
}
feedback = QgsProcessingFeedback()

res = processing.run('script:PegelOnlineLoader', params, feedback=feedback)
res['Result'] # Access your output layer