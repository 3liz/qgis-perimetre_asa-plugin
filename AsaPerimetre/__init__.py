"""
/***************************************************************************
 AsaPerimetre
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
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = '3liz'
__date__ = '2018-12-19'
__copyright__ = '(C) 2018 by 3liz'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Raepa class from file Raepa.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .asaperimetre import AsaPerimetre
    return AsaPerimetre()
