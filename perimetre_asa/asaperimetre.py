__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsApplication
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QMenu

from .dock import AsaPerimetreDock
from .processing.provider import AsaPerimetreProvider


class AsaPerimetre:

    def __init__(self):
        self.provider = None
        self.menu = None
        self.dock = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = AsaPerimetreProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Init the user interface."""
        self.initProcessing()
        self.dock = AsaPerimetreDock()

        iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        action = self.dock.toggleViewAction()

        self.menu = QMenu("&Périmètre d'ASA")

        # Add Perimetre ASA to Extension menu
        self.menu.addAction(action)

        plugin_menu = iface.pluginMenu()
        plugin_menu.addMenu(self.menu)
        # Add Perimetre ASA toolbar
        iface.addToolBarIcon(action)

    # def unload(self):
    #     """Unload the plugin."""
    #     if self.provider:
    #         QgsApplication.processingRegistry().removeProvider(self.provider)
    #     iface.removeDockWidget(self.dock)
    #     iface.removePluginMenu(self.menu)
    #     iface.removeToolbarIcon(self.toolbar)
    #     self.dock.deleteLater()
