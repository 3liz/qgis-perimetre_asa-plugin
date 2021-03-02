"""Dock file."""
from functools import partial

from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QDockWidget, QPushButton
from processing import execAlgorithmDialog

from .qgis_plugin_tools.tools.resources import load_ui, resources_path

DOCK_CLASS = load_ui('dock.ui')


__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class PerimetreAsaDock(QDockWidget, DOCK_CLASS):

    def __init__(self, parent=None):
        _ = parent
        super().__init__()

        self.setupUi(self)

        self.algorithms = [
            'jointure_perimetre',
        ]
        for alg in self.algorithms:
            button = self.findChild(QPushButton, 'button_algo_{}'.format(alg))
            if not button:
                continue
            button.clicked.connect(partial(self.run_algorithm, alg))

        html = '<hmtl><head><style>'
        html += 'body {font-family: '
        html += '\'Ubuntu\', \'Lucida Grande\', \'Segoe UI\', \'Arial\', sans-serif;'
        html += 'margin-left: 0px; margin-right: 0px; margin-top: 0px;'
        html += 'font-size: 14px;}'
        html += 'img {max-width: 100%; margin: 20px;}'
        html += 'h2 {color: #fff; background-color: #014571; line-height: 2; padding-left:5px; }'
        html += 'p {margin-left: 10px; }'
        html += '</style></head><body>'
        html += '<b><h2>Extension Périmètre d\'ASA</h2></b>'
        html += '<p>Une extension qui permet d\'effectuer une jointure entre '
        html += 'les données parcellaires et un fichier métier.</p>'
        html += '<p>Pour utiliser cette extension il faut cliquer sur le bouton '
        html += '"ASA jointure Périmètre" présent dans l\'image ci-dessous qui '
        html += 'lancera l\'algorithme de jointure.</p>'
        html += '<img src="{}" /><br><br>'.format('panneauasa.png')
        html += '<p>Voici l\'interface de l\'algorithme de jointure, il dispose de '
        html += 'trois paramètres: le premier concerne la couche des parcelles, '
        html += 'le deuxième la couche rôle et le dernier le dossier où l\'on '
        html += 'veut sauvegarder la couche périmètre.</p>'
        html += '<img src="{}" /><br><br>'.format('algoasa.png')
        html += '<p>Pour les deux premiers paramètres soit les couches sont dans '
        html += 'le projet QGIS et vous pourrez les sélectionner via la liste '
        html += 'déroulante. Soit vous cliquez sur le bouton avec les trois petits points '
        html += 'et une boîte de sélection de fichiers s\'ouvre comme l\'image ci-dessous. '
        html += 'Vous pourrez chercher votre ou vos fichier(s) de données comme le '
        html += 'fichier concernant la couche rôle.</p>'
        html += '<img src="{}" /><br><br>'.format('getFile.png')
        html += '<p>Pour le dernier paramètre, il faut cliquer sur le bouton '
        html += 'avec les trois petits points. Une liste de choix s\'affiche, il '
        html += 'faut cliquer sur "Enregistrer vers un fichier..." qui ouvrira '
        html += 'une boîte comme l\'image ci-dessous pour sélectionner le dossier '
        html += 'de sortie et le nom que vous donnerez à la couche ex: périmètre.shp</p>'
        html += '<img src="{}" /><br><br>'.format('getFolder.png')
        html += '<p>Pour finir, il faut cliquer sur le bouton "Exécuter" en bas '
        html += 'à droite de l\'interface présent sur la deuxième image.</p>'
        html += '</body></html>'

        # It must be a file, even if it does not exist on the file system.
        base_url = QUrl.fromLocalFile(resources_path('images', 'must_be_a_file.png'))
        self.documentation.setHtml(html, base_url)

    @staticmethod
    def run_algorithm(name):
        alg_name = 'perimetre_asa:{}'.format(name)
        execAlgorithmDialog(alg_name, {})
