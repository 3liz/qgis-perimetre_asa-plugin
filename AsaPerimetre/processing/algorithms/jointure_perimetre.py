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
    QgsProcessingOutputString,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsProcessingUtils,
)
import copy

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
                self.LAYER, 'Couche parcelle',
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

        fields_needed = copy.deepcopy(fields_test)

        number_item = len(fields_test)

        for field in role.fields():
            f = field.name().lower()
            if f in fields_test.keys():
                count += 1
                del fields_needed[f]

        if count < number_item:

            msg = 'Erreur dans les champs de la couche de jointure, il manque : '
            msg += ', '.join(fields_needed.keys())
            results[self.OUTPUT_STRING] = msg
            return results

        alg_params = {
            'DISCARD_NONMATCHING': True,
            'FIELD': 'idu',
            'FIELDS_TO_COPY': None,
            'FIELD_2': 'CLEF_2',
            'INPUT': cadastre,
            'INPUT_2': role,
            'METHOD': 1,
            'PREFIX': 'asa_tmp_',
            'OUTPUT': 'memory:'
        }

        outputs['JoinAttributesByFieldValue'] = processing.run(
            'native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True
        )
        layerPath = outputs['JoinAttributesByFieldValue']['OUTPUT']

        layer = QgsProcessingUtils.mapLayerFromString(layerPath, context=context)

        feedback.pushInfo('### RENOMMAGE DES CHAMPS ###')

        refactor_fields = {
            'FIELDS_MAPPING': [],
            'INPUT': layer,
            'OUTPUT': parameters[self.FEATURE_SINK]
        }

        asa_fields_needed = []
        cad_field_mapping = []
        asa_fields_mapping = []

        for field in layer.fields():
            new_name = ''
            start_field = field.name().lower()
            if start_field.startswith('asa_tmp_'):
                new_field = start_field.replace('asa_tmp_', '')
                if new_field in fields_test.keys():
                    new_name = fields_test[new_field]
                    asa_fields_needed.append({
                        'expression': '"'+start_field+'"',
                        'length': field.length(),
                        'name': new_name,
                        'precision': field.precision(),
                        'type': field.type()
                    })
                elif new_field == 'commune':
                    new_name = 'asa_commune_2'
                    asa_fields_mapping.append({
                        'expression': '"'+start_field+'"',
                        'length': field.length(),
                        'name': new_name,
                        'precision': field.precision(),
                        'type': field.type()
                    })
                else:
                    new_name = 'asa_'+new_field
                    asa_fields_mapping.append({
                        'expression': '"'+start_field+'"',
                        'length': field.length(),
                        'name': new_name,
                        'precision': field.precision(),
                        'type': field.type()
                    })
            else:
                new_name = 'cad_'+start_field
                cad_field_mapping.append({
                    'expression': '"'+start_field+'"',
                    'length': field.length(),
                    'name': new_name,
                    'precision': field.precision(),
                    'type': field.type()
                })

        refactor_fields['FIELDS_MAPPING'].extend(cad_field_mapping)
        refactor_fields['FIELDS_MAPPING'].extend(asa_fields_needed)
        refactor_fields['FIELDS_MAPPING'].extend(asa_fields_mapping)

        outputs['refactorFields'] = processing.run(
            'qgis:refactorfields', refactor_fields, context=context, feedback=feedback, is_child_algorithm=True
        )
        layerPath = outputs['refactorFields']['OUTPUT']

        # return feature sink
        results[self.FEATURE_SINK] = layerPath
        results[self.OUTPUT_STRING] = "Success"

        return results
