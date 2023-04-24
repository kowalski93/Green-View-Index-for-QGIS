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
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsProcessingAlgorithm, QgsApplication
import processing

import os
import sys
import inspect

from qgis.core import QgsProcessingAlgorithm, QgsApplication
from .green_view_index_provider import GreenViewIndexProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class GreenViewIndexPlugin(object):

    def __init__(self,iface):
        self.provider = None
        self.iface = iface
        
    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = GreenViewIndexProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()
        #icon = os.path.join(os.path.join(cmd_folder, 'logo.png'))
        #self.action = QAction(QIcon(icon),u"Green View Index", self.iface.mainWindow())
        #self.action.triggered.connect(self.run)
        #self.iface.addPluginToMenu(u"&Green View Index", self.action)
        #self.iface.addToolBarIcon(self.action)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        #self.iface.removePluginMenu(u"&Green View Index", self.action)
        #self.iface.removeToolBarIcon(self.action)
        
    def run(self):
        processing.execAlgorithmDialog("Green View Index")