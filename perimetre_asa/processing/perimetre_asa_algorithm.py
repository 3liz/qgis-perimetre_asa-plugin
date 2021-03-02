"""AsaPerimetre base class algorithm."""
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingAlgorithm

from perimetre_asa.qgis_plugin_tools.tools.resources import resources_path

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class PerimetreAsaAlgorithm(QgsProcessingAlgorithm):

    def createInstance(self):
        return type(self)()

    def icon(self):
        return QIcon(resources_path("icons", "icon.png"))
