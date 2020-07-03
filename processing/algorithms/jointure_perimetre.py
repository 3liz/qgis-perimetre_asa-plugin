"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '3liz'
__date__ = '2020-06-30'
__copyright__ = '(C) 2020 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import configparser
import os
import processing

from db_manager.db_plugins import createDbPlugin
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterCrs,
    QgsProcessingOutputString,
    QgsExpressionContextUtils,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsVectorLayerJoinInfo,
    QgsFeatureSink,
    QgsProcessingMultiStepFeedback
)

from ..asaperimetre_algorithm import AsaPerimetreAlgorithm



class JointurePerimetre(AsaPerimetreAlgorithm):

    LAYER = 'LAYER'
    ROLE = 'ROLE'
    FEATURE_SINK = 'FEATURE_SINK'
    OUTPUT_VECTOR_LAYER_MERGED = 'OUTPUT_VECTOR_LAYER_MERGED'
    OUTPUT_STRING = 'OUTPUT_STRING'

    def name(self):
        return 'jointure_perimetre'

    def displayName(self):
        return 'Jointure de périmètre avec le cadastre'

    def shortHelpString(self) -> str:
        return (
            'Créer une couche SIG issue d\'une jointure entre le cadastre '
            'et un fichier provenant d\'une application métier')

    def group(self):
        return 'Jointure'

    def groupId(self):
        return 'asaperimetre_jointure'

    def initAlgorithm(self, config):

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LAYER, 'Couche cadastre',
                [QgsProcessing.TypeVector],
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.ROLE, 'Fichier Role',
                [QgsProcessing.TypeVector],
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FEATURE_SINK, 'Output', optional=True,
                type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None
            )
        )
        self.addOutput(
            QgsProcessingOutputString(
                self.OUTPUT_STRING,
                'Message de sortie'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        cadastre = self.parameterAsVectorLayer(parameters, self.LAYER, context)
        role = self.parameterAsVectorLayer(parameters, self.ROLE, context)

        feedback = QgsProcessingMultiStepFeedback(1, feedback)
        results = {}
        outputs = {}

        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idu',
            'FIELDS_TO_COPY': None,
            'FIELD_2': 'clef_2',
            'INPUT': cadastre,
            'INPUT_2': role,
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters[self.FEATURE_SINK]
        }

        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        #return feature sink
        results[self.FEATURE_SINK] = outputs['JoinAttributesByFieldValue']['OUTPUT']
        return results
