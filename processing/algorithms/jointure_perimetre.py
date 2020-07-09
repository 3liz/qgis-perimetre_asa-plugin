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

import processing
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterCrs,
    QgsProcessingOutputString,
    QgsExpressionContextUtils,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsVectorLayerJoinInfo,
    QgsProcessingMultiStepFeedback,
    QgsVectorLayer
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
        count = 0
        feedback = QgsProcessingMultiStepFeedback(1, feedback)
        results = {}
        outputs = {}

        fields_test = {
            'clef_2': 'asa_id_parcelle',
            'nom_asa': 'nom_asa',
            'souscrite': 'asa_droitdeau',
            'cod_reseau': 'asa_cod_reseau',
            'reseau': 'asa_reseau',
            'num_propri': 'asa_num_adherent',
            'proprio': 'asa_nom',
            'pro_adr1': 'asa_adresse',
            'pro_adr2': 'asa_adresse2',
            'pro_ville': 'asa_commune',
            'pro_cp': 'asa_cp',
            'cod_statio': 'asa_cod_station',
            'station': 'asa_station',
            'cod_tarif': 'asa_cod_tarif',
            'tarif': 'asa_tarif',
            'cod_cultur': 'asa_cod_culture',
            'culture': 'asa_culture'
        }
        number_item = len(fields_test)
        role.startEditing()
        for field in role.fields():
            f = field.name().lower()
            idx = role.fields().indexFromName(field.name())
            role.renameAttribute(idx, f)
            if f in fields_test.keys():
                role.renameAttribute(idx, fields_test[f])
                count += 1
                del fields_test[f]

        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idu',
            'FIELDS_TO_COPY': None,
            'FIELD_2': 'asa_id_parcelle',
            'INPUT': cadastre,
            'INPUT_2': role,
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters[self.FEATURE_SINK]
        }
        if count == number_item:
            outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            layer = outputs['JoinAttributesByFieldValue']['OUTPUT']

            #return feature sink
            results[self.FEATURE_SINK] = layer
        else:
            msg = 'Erreur dans les champs de la couche de jointure, il manques:'
            for k in fields_test.keys():
                msg += ' ' + k + ','
            results[self.OUTPUT_STRING] = msg
        role.rollBack()
        return results
