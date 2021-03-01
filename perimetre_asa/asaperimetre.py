"""
/***************************************************************************
 asa-perimetre
                                 A QGIS plugin
                              -------------------
        begin                : 2018-12-19
        copyright            : (C) 2018 by 3liz
        email                : info@3liz.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = '3liz'
__date__ = '2018-12-19'
__copyright__ = '(C) 2018 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

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

    def unload(self):
        """Unload the plugin."""
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)
        iface.removeDockWidget(self.dock)
        self.dock.deleteLater()
