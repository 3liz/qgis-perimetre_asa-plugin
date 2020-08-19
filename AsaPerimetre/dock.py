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

        html = '<b><h1> Plugin ASA Perimètre </h1></b>'
        html += '<p>Un plugin qui permet d\'effectuer une jointure entre '
        html += 'les données parcellaires et un fichier métier.</p>'
        html += '<p>Pour utiliser ce plugin il suffit de cliquer sur le bouton '
        html += '"ASA jointure Perimetre" présent ans l\'image ci-dessous qui '
        html += 'lancera l\'algorithme de jointure.</p>'
        html += '<img src="/resources/images/panneauasa.png"/><br><br>'
        html += '<p>Voici l\'interface de l\'algorithme de jointure, il dispose de '
        html += 'trois paramètres: le premier concerne la couche des parcelles, '
        html += 'le deuxième la couche rôle et le dernier le dossier où l\'on '
        html += 'veut sauvegarder la couche périmètre.</p>'
        html += '<img src="/resources/images/algoasa.png" /><br><br>'
        html += '<p>Pour les deux premiers paramètres soit vous avez les couches dans '
        html += 'un projet QGIS et alors vous pourrez les sélectionner via liste '
        html += 'déroulante. Soit vous cliquez sur le bouton avec trois points dessous '
        html += 'et une boîte de sélection de fichiers s\'ouvre comme l\'image ci-dessous '
        html += 'ou vous irez chercher votre ou vos fichier(s) de données comme le '
        html += 'fichier concernant la couche rôle.</p>'
        html += '<img src="/resources/images/getFile.png" /><br><br>'
        html += '<p>Pour le dernier paramètre il vous faut cliquer sur le bouton '
        html += 'avec les trois points. Une liste de choix s\'offre vous, il vous '
        html += 'faut cliquer sur "Enregistrer vers un fichier..." qui vous ouvrira '
        html += 'une boîte comme l\'image ci-dessous pour sélectionner le dossier '
        html += 'de sortie et le nom que vous donnerais à la couche ex: périmètre.shp</p>'
        html += '<img src="/resources/images/getFolder.png" /><br><br>'
        html += '<p>Pour finir il vous restera a cliquer sur le bouton "Exécuter" en bas '
        html += 'à droite de l\'interface de l\'algorithme présent sur la deuxième image.</p>'

        self.documentation.setHtml(html)

    @staticmethod
    def run_algorithm(name):
        alg_name = 'asaperimetre:{}'.format(name)
        execAlgorithmDialog(alg_name, {})
