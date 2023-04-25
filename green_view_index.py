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
        
        actionGen = QAction(
            QIcon(os.path.join(os.path.join(cmd_folder,'greenviewindex', 'rand_points_logo.png'))),
            u"Generate Sample Points", self.iface.mainWindow())
        actionGen.triggered.connect(self.runGen)

        actionDown = QAction(
            QIcon(os.path.join(os.path.join(cmd_folder,'greenviewindex', 'download_logo.png'))),
            u"Download Google Street View Images", self.iface.mainWindow())
        actionDown.triggered.connect(self.runDown)

        actionCalc = QAction(
            QIcon(os.path.join(os.path.join(cmd_folder,'greenviewindex', 'calculate_logo.png'))),
            u"Calculate Green View Index", self.iface.mainWindow())
        actionCalc.triggered.connect(self.runCalc)
        
        self.actions = [actionGen,actionDown,actionCalc]
        for action in self.actions:
            self.iface.addPluginToMenu(u"&Green View Index", action)
            self.iface.addToolBarIcon(action)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
        for action in self.actions:
            self.iface.removePluginMenu(u"&Green View Index", action)
            self.iface.removeToolBarIcon(action)
            del action
        
    def runGen(runGen):
        processing.execAlgorithmDialog("Green View Index:generate_sample_points")
    def runDown(runDown):
        processing.execAlgorithmDialog("Green View Index:download_gsv_images")
    def runCalc(runCalc):
        processing.execAlgorithmDialog("Green View Index:calculate_green_view_index")