__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import QgsApplication
from qgis.utils import iface
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .dock import AsaPerimetreDock
from .processing.provider import AsaPerimetreProvider
from .qgis_plugin_tools.tools.resources import resources_path


class AsaPerimetre:

    def __init__(self):
        self.provider = None
        self.menu = None
        self.dock = None
        self.dock_action = None

    def initProcessing(self):
        """ Init Processing provider for QGIS >= 3.8. """
        self.provider = AsaPerimetreProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """ Init the user interface. """
        self.initProcessing()
        self.dock = AsaPerimetreDock()

        iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)

        icon = QIcon(resources_path('icons', 'icon.png'))

        # Plugin menu
        self.dock_action = QAction(icon, "Périmètre d'ASA", iface.mainWindow())
        self.dock_action.triggered.connect(self.manage_dock)
        iface.pluginMenu().addAction(self.dock_action)

        # Plugin toolbar
        iface.addToolBarIcon(self.dock_action)

    def manage_dock(self):
        """ Open or close the dock. """
        if self.dock.isVisible():
            self.dock.close()
        else:
            self.dock.show()
            self.dock.raise_()

    def unload(self):
        """ Unload the plugin. """
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            del self.provider

        if self.dock_action:
            iface.pluginMenu().removeAction(self.dock_action)
            iface.removeToolBarIcon(self.dock_action)
            del self.dock_action

        if self.dock:
            iface.removeDockWidget(self.dock)
            self.dock.deleteLater()
            del self.dock
