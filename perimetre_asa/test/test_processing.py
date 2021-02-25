from .base_test_processing import BaseTestProcessing
import processing
from ..qgis_plugin_tools.tools.resources import plugin_test_data_path
from qgis.core import (
    QgsProcessingUtils,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProject,
    QgsVectorLayer,
)

__copyright__ = 'Copyright 2020, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class TestProcessing(BaseTestProcessing):

    """ Tests for basic Processing algorithms. """

    def test_processing_algorithms(self):
        """ Tests we have all necessary algorithms. """
        for algorithm in self.provider.algorithms():
            self.assertTrue(algorithm.name(), 'Algorithm {} has no name'.format(algorithm.id()))

        self.assertEqual(len(self.provider.algorithms()), 1)

    def test_jointure_perimetre(self):
        """ Test if the algorithm works """

        params = {
            'LAYER': plugin_test_data_path('perimetre.gpkg|layername=parcelle_info'),
            'ROLE': plugin_test_data_path('perimetre.gpkg|layername=role'),
            'FEATURE_SINK': 'memory:'
        }

        project = QgsProject()
        feedback = QgsProcessingFeedback()
        context = QgsProcessingContext()

        context.setProject(project)
        context.setFeedback(feedback)

        # Run algorithm
        data = processing.run('asaperimetre:jointure_perimetre', params, context=context, feedback=feedback)

        # Testing outputs
        self.assertIn('FEATURE_SINK', data)
        self.assertIn('OUTPUT_STRING', data)

        self.assertEqual(data['OUTPUT_STRING'], 'Success')

        layer = data['FEATURE_SINK']
        if not isinstance(layer, QgsVectorLayer):
            layer = QgsProcessingUtils.mapLayerFromString(data['FEATURE_SINK'], context=context)
        refLayer = QgsProcessingUtils.mapLayerFromString(
            plugin_test_data_path('perimetre.gpkg|layername=perimetre'),
            context=context
        )

        not_found_fields = []
        for f in refLayer.fields():
            fname = f.name()
            if layer.fields().indexFromName(fname) < 0:
                not_found_fields.append(fname)

        self.assertListEqual(not_found_fields, ['fid'])
