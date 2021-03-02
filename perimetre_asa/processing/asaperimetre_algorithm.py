"""AsaPerimetre base class algorithm."""

from qgis.core import QgsProcessingAlgorithm

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class AsaPerimetreAlgorithm(QgsProcessingAlgorithm):

    def __init__(self):
        super().__init__()

    def createInstance(self):
        return type(self)()

    def flags(self):
        return super().flags()
