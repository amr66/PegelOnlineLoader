# -*- coding: utf-8 -*-
"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsApplication,
                       QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureRequest)
from qgis.core import (QgsProcessingParameterString,
                       QgsProcessingParameterEnum,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
import processing, sys

# use this to import local modules
sys.path.append(QgsApplication.qgisSettingsDirPath() + '\\processing\\scripts')
from pomodules.poqgsstations import PoQgsStations
from pomodules.poqgscurrentw import PoQgsCurrentW

class PegelOnlineLoader(QgsProcessingAlgorithm):
    INPUT = 'Query'
    OUTPUT = 'Result'
    QUERY_OPTIONS = ['Stations', 'Waterlevels']


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return PegelOnlineLoader()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'PegelOnlineLoader'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('PegelOnline')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'PegelOnline'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr('PegelOnline short description: to do')

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterEnum(self.INPUT,
                                         self.tr(self.INPUT),
                                         self.QUERY_OPTIONS))
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT,
                                              self.tr('Output layer'),
                                              QgsProcessing.TypeVectorAnyGeometry))


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        qx = self.parameterAsInt(parameters, self.INPUT, context)
        feedback.pushInfo(str(qx))
        query = self.QUERY_OPTIONS[qx]
        feedback.pushInfo(query)

        # we're loading from PegelOnline
        if query == 'Stations':
            stat = PoQgsStations()
        elif query == 'Waterlevels':
            stat = PoQgsCurrentW()

        features = stat.getFeatures()
        # field definitions for stations
        fields = stat.fields
        crs = stat.crs

        # our output to qgis
        sink, dest_id = self.parameterAsSink(parameters, self.OUTPUT, context, fields, QgsWkbTypes.Point, crs)

        feedback.pushInfo(str('Total Length {}'.format(len(features))))

        for f in features:
            sink.addFeature(f, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}
