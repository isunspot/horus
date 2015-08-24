# -*- coding: utf-8 -*-
# This file is part of the Horus Project

__author__ = 'Jesús Arroyo Torrens <jesus.arroyo@bq.com>'
__copyright__ = 'Copyright (C) 2014-2015 Mundo Reader S.L.'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'


import wx._core

from horus.gui.util.customPanels import ExpandablePanel, Slider, CheckBox, Button, TextBox

from horus.util import profile, system as sys
from horus.gui.util.resolutionWindow import ResolutionWindow

from horus.engine.scan.ciclop_scan import CiclopScan
from horus.engine.algorithms.point_cloud_generation import PointCloudGeneration
from horus.engine.algorithms.point_cloud_roi import PointCloudROI

ciclop_scan = CiclopScan()
point_cloud_generation = PointCloudGeneration()
point_cloud_roi = PointCloudROI()


class ScanParameters(ExpandablePanel):

    def __init__(self, parent):
        ExpandablePanel.__init__(
            self, parent, _("Scan Parameters"), hasUndo=False, hasRestore=False)

        self.parent = parent

        self.clearSections()
        section = self.createSection('scan_parameters')
        section.addItem(CheckBox, 'capture_texture')
        section.addItem(CheckBox, 'use_left_laser')
        section.addItem(CheckBox, 'use_right_laser')

    def updateCallbacks(self):
        section = self.sections['scan_parameters']
        section.updateCallback('capture_texture', ciclop_scan.set_capture_texture)
        section.updateCallback('use_left_laser', ciclop_scan.set_use_left_laser)
        section.updateCallback('use_right_laser', ciclop_scan.set_use_right_laser)


class RotatingPlatform(ExpandablePanel):

    def __init__(self, parent):
        ExpandablePanel.__init__(self, parent, _("Rotating platform"), hasUndo=False)

        self.clearSections()
        section = self.createSection('rotating_platform')
        section.addItem(TextBox, 'motor_step_scanning')
        section.addItem(TextBox, 'motor_speed_scanning')
        section.addItem(TextBox, 'motor_acceleration_scanning')

    def updateCallbacks(self):
        section = self.sections['rotating_platform']
        section.updateCallback(
            'motor_step_scanning', lambda v: ciclop_scan.set_motor_step(self.getValueFloat(v)))
        section.updateCallback(
            'motor_speed_scanning', lambda v: ciclop_scan.set_motor_speed(self.getValueInteger(v)))
        section.updateCallback(
            'motor_acceleration_scanning', lambda v: ciclop_scan.set_motor_acceleration(self.getValueInteger(v)))

    # TODO: move
    def getValueInteger(self, value):
        try:
            return int(eval(value, {}, {}))
        except:
            return 0

    def getValueFloat(self, value):
        try:
            return float(eval(value.replace(',', '.'), {}, {}))
        except:
            return 0.0


class PointCloudROI(ExpandablePanel):

    def __init__(self, parent):
        ExpandablePanel.__init__(self, parent, _("Point cloud ROI"))

        self.main = self.GetParent().GetParent().GetParent().GetParent()

        self.clearSections()
        section = self.createSection('point_cloud_roi')
        section.addItem(CheckBox, 'roi_view', tooltip=_(
            "View the Region Of Interest (ROI). This cylindrical region is the one being scanned. All information outside won't be taken into account during the scanning process"))
        section.addItem(Slider, 'roi_diameter')
        section.addItem(Slider, 'roi_height')

    def updateCallbacks(self):
        section = self.sections['point_cloud_roi']
        #section.updateCallback('roi_view', lambda v: (
        #    point_cloud_roi.set_roi_view(bool(v)), self.main.sceneView.QueueRefresh()))
        section.updateCallback('roi_diameter', lambda v: (
            point_cloud_roi.set_diameter(int(v)), self.main.sceneView.QueueRefresh()))
        section.updateCallback('roi_height', lambda v: (
            point_cloud_roi.set_height(int(v)), self.main.sceneView.QueueRefresh()))


class PointCloudColor(ExpandablePanel):

    def __init__(self, parent):
        ExpandablePanel.__init__(
            self, parent, _("Point cloud color"), hasUndo=False, hasRestore=False)

        self.main = self.GetParent().GetParent().GetParent().GetParent()

        self.clearSections()
        section = self.createSection('point_cloud_color')
        section.addItem(Button, 'point_cloud_color')

    def updateCallbacks(self):
        section = self.sections['point_cloud_color']
        section.updateCallback('point_cloud_color', self.onColorPicker)

    def onColorPicker(self):
        data = wx.ColourData()
        data.SetColour(point_cloud_generation.color)
        dialog = wx.ColourDialog(self, data)
        dialog.GetColourData().SetChooseFull(True)
        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetColourData()
            color = data.GetColour().Get()
            point_cloud_generation.set_point_cloud_color(color)
            profile.putProfileSetting('point_cloud_color', "".join(map(chr, color)).encode('hex'))
        dialog.Destroy()
