__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .algorithms.jointure_perimetre import JointurePerimetre
from ..qgis_plugin_tools.tools.resources import resources_path


class PerimetreAsaProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(JointurePerimetre())

    def id(self):
        return 'perimetre_asa'

    def name(self):
        return "Périmètre d'ASA"

    def longName(self):
        return 'Jointure de données cadastrale et de périmètre'

    def icon(self):
        return QIcon(resources_path("icons", "icon.png"))
