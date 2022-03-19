import FreeCADGui
import os
from . import ICONPATH
from . import tools

class BaseCommand():
	fnParams = None
	FreeCADGui.doCommandGui("import freecad.estimateWB.commands")

	def __init__(self):
		pass

	def IsActive(self):
		return bool(tools.selectedObject())

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

###############################################################################

class Estimate_Weight(BaseCommand):
	function = tools.estimateWeight
	def __init__(self, fnParams):
		self.fnParams = fnParams
		self.name = f"{tools.LANG.chunk('estimateWeightName')[0]} {fnParams} {tools.LANG.chunk('estimateWeightName')[1]}"
		self.pixmap = os.path.join(ICONPATH, f"{fnParams}.svg")
		self.menuText = f"{tools.LANG.chunk('estimateWeightMenuText')[0]} {fnParams}"
		self.toolTip = f"{tools.LANG.chunk('estimateWeightToolTip')[0]} {fnParams}"

class Estimate_Weight_Custom(BaseCommand):
	name = tools.LANG.chunk('estimateWeightCustomName')[0]
	function = tools.estimateWeight
	pixmap = os.path.join(ICONPATH, "none.svg")
	menuText = tools.LANG.chunk('estimateWeightCustomMenuText')[0]
	toolTip = tools.LANG.chunk('estimateWeightCustomToolTip')[0]
