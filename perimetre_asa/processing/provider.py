__author__ = '3liz'
__date__ = '2020-06-30'
__copyright__ = '(C) 2020 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .algorithms.jointure_perimetre import JointurePerimetre
from ..qgis_plugin_tools.tools.resources import resources_path


class AsaPerimetreProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(JointurePerimetre())

    def id(self):
        return 'asaperimetre'

    def name(self):
        return "Perimètre d'ASA"

    def longName(self):
        return 'Jointure de données cadastrale et de périmètre'

    def icon(self):
        return QIcon(resources_path("icons", "icon.png"))
