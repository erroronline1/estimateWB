import os
from . import ICONPATH
from . import tools

import FreeCADGui
from FreeCADGui import Selection

class BaseCommand():
	fnParams = None
	FreeCADGui.doCommandGui("import freecad.estimateWB.commands")

	def __init__(self):
		pass

	def GetResources(self):
		return {'Pixmap': self.pixmap,
				'MenuText': self.menuText,
				'ToolTip': self.toolTip}

	def Activated(self):
		FreeCADGui.doCommandGui(f"freecad.estimateWB.commands.{self.__class__.__name__}.do('{self.fnParams}')")

	@classmethod
	def do(self, fnParams=None):
		self.function(fnParams)

################################################################################

class Estimate_Volume(BaseCommand):
	name = tools.LANG.chunk("estimateVolumeName")[0]
	function = tools.estimateVolume
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = tools.LANG.chunk("estimateVolumeMenuText")[0]
	toolTip = tools.LANG.chunk("estimateVolumeToolTip")[0]
	def IsActive(self):
		return Selection.hasSelection()

###############################################################################

class Estimate_Weight(BaseCommand):
	function = tools.estimateWeight
	def __init__(self, fnParams):
		self.fnParams = fnParams
		self.name = f"{tools.LANG.chunk('estimateWeightName')[0]} {fnParams} {tools.LANG.chunk('estimateWeightName')[1]}"
		self.pixmap = os.path.join(ICONPATH, f"{fnParams}.svg")
		self.menuText = f"{tools.LANG.chunk('estimateWeightMenuText')[0]} {fnParams}"
		self.toolTip = f"{tools.LANG.chunk('estimateWeightToolTip')[0]} {fnParams}"
	def IsActive(self):
		return Selection.hasSelection()

class Estimate_Weight_Custom(BaseCommand):
	name = tools.LANG.chunk('estimateWeightCustomName')[0]
	function = tools.estimateWeight
	pixmap = os.path.join(ICONPATH, "none.svg")
	menuText = tools.LANG.chunk('estimateWeightCustomMenuText')[0]
	toolTip = tools.LANG.chunk('estimateWeightCustomToolTip')[0]
	def IsActive(self):
		return Selection.hasSelection()

class Set_Scale(BaseCommand):
	function = tools.setScale
	def __init__(self, fnParams):
		self.fnParams = fnParams
		self.name = f"{tools.LANG.chunk('scaleName')[0]} {fnParams}"
		self.pixmap = os.path.join(ICONPATH, f"scale{fnParams}.svg")
		self.menuText = f"{tools.LANG.chunk('scaleMenuText')[0]} {fnParams}"
		self.toolTip = f"{tools.LANG.chunk('scaleToolTip')[0]} {fnParams}"
	def IsActive(self):
		return tools.CURRENTSCALE != self.fnParams

class Set_Weight_Unit(BaseCommand):
	function = tools.setWeightUnit
	def __init__(self, fnParams):
		self.fnParams = fnParams 
		self.name = f"{tools.LANG.chunk('weightName')[0]} {fnParams}" 
		self.pixmap = os.path.join(ICONPATH, f"weight_{fnParams}.svg")
		self.menuText = f"{tools.LANG.chunk('weightName')[0]} {fnParams}" 
		self.toolTip = f"{tools.LANG.chunk('weightName')[0]} {fnParams}" 
	def IsActive(self):
		return tools.CURRENTUNIT != self.fnParams

class Toggle_Report(BaseCommand):
	function = tools.toggleReport
	def __init__(self, fnParams):
		self.fnParams = fnParams 
		self.name = f"{tools.LANG.chunk('reportSet')[0]} {fnParams}{tools.LANG.chunk('reportSet')[1]}" 
		self.pixmap = os.path.join(ICONPATH, f"report_{fnParams}.svg")
		self.menuText = f"{tools.LANG.chunk('reportSet')[0]} {fnParams}{tools.LANG.chunk('reportSet')[1]}"
		self.toolTip = f"{tools.LANG.chunk('reportSet')[0]} {fnParams}{tools.LANG.chunk('reportSet')[1]}"
	def IsActive(self):
		return self.fnParams != tools.CURRENTREPORT
