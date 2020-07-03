"""
/***************************************************************************
 AsaPerimetre
                                 A QGIS plugin
                              -------------------
        begin                : 2020-06-30
        copyright            : (C) 2020 by 3liz
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
__date__ = '2020-06-30'
__copyright__ = '(C) 2020 by 3liz'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsProcessingProvider

from .algorithms.jointure_perimetre import JointurePerimetre
from ..qgis_plugin_tools.tools.resources import resources_path


class AsaPerimetreProvider(QgsProcessingProvider):

    def loadAlgorithms(self):
        self.addAlgorithm(JointurePerimetre())

    def id(self):
        return 'asaperimetre'

    def name(self):
        return 'AsaPerimetre'

    def longName(self):
        return 'Jointure de données cadastrale et de périmètre'
