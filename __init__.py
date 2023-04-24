# -*- coding: utf-8 -*-

"""
/***************************************************************************
 GreenViewIndex
                                 A QGIS plugin
 A plugin for Green View Index (GVI) operations
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-04-21
        copyright            : (C) 2023 by Alexandros Voukenas
        email                : avoukenas@gmail.com
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

__author__ = 'Alexandros Voukenas'
__date__ = '2023-04-21'
__copyright__ = '(C) 2023 by Alexandros Voukenas'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GreenViewIndex class from file GreenViewIndex.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .green_view_index import GreenViewIndexPlugin
    return GreenViewIndexPlugin(iface)
