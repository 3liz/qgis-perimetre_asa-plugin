"""Dock file."""
from functools import partial

from qgis.PyQt.QtWidgets import QDockWidget, QPushButton

try:
    # QGIS < 3.8
    # noinspection PyPep8Naming,PyUnresolvedReferences
    from processing import execAlgorithmDialog
except ModuleNotFoundError:
    # QGIS >= 3.8
    # noinspection PyPep8Naming,PyUnresolvedReferences
    from qgis.processing import execAlgorithmDialog


from .qgis_plugin_tools.tools.resources import load_ui

DOCK_CLASS = load_ui('dock.ui')


__copyright__ = 'Copyright 2020, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'
__revision__ = '$Format:%H$'


class AsaPerimetreDock(QDockWidget, DOCK_CLASS):

    def __init__(self, parent=None):
        super().__init__()

        self.setupUi(self)
        self.tab_widget.setCurrentIndex(0)

        self.algorithms = [
            'jointure_perimetre',
        ]
        for alg in self.algorithms:
            button = self.findChild(QPushButton, '{}{}'.format('button_algo_', alg))
            if not button:
                continue
            button.clicked.connect(partial(self.run_algorithm, alg))

        self.documentation.setHtml(
            '<b>Plugin ASA Périmètre</b><br><br>'
            '<p>Un plugin qui permet d\'effectuer un jointure entre'
            ' les données parcellaires et un fichier métier.</p><br>'
            '<p>Pour utiliser ce plugin il suffit de cliquer sur le bouton'
            ' "ASA jointure Perimetre" qui lancera l\'algorithme de jointure.</p><br>'
            '<p>Il vous suffira de renseigner votre couche de parcelle puis d\'aller'
            ' choisir votre fichier métier et enfin d\'aller sélectionner'
            ' l\'emplacement de sortie pour la couche qui sera le résultat de la'
            ' jointure.</p>'
        )

    @staticmethod
    def run_algorithm(name):
        alg_name = 'asaperimetre:{}'.format(name)
        execAlgorithmDialog(alg_name, {})
