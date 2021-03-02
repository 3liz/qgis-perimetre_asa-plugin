from qgis.core import (
    QgsApplication,
)
from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings,
)
from qgis.testing import unittest
from processing.core.Processing import Processing

from ..processing.provider import PerimetreAsaProvider as Provider

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class BaseTestProcessing(unittest.TestCase):

    """ Base test class for Processing. """

    # noinspection PyCallByClass,PyArgumentList
    @classmethod
    def setUpClass(cls):
        """ Run before all tests and set up environment. """
        # Don't mess with actual user settings
        QCoreApplication.setOrganizationName('3Liz')
        QCoreApplication.setOrganizationDomain('3liz.com')
        QCoreApplication.setApplicationName('AsaPerimetre')
        QSettings().clear()

        Processing.initialize()

    def setUp(self) -> None:
        registry = QgsApplication.processingRegistry()

        self.provider = Provider()
        if not registry.providerById(self.provider.id()):
            registry.addProvider(self.provider)

    def tearDown(self) -> None:
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
