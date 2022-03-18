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
	name = "estimate volume"
	function = tools.estimateVolume
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = "volume"
	toolTip = "selected body's approximate volume in cm³"

###############################################################################

class Estimate_Weight(BaseCommand):
	function = tools.estimateWeight
	def __init__(self, fnParams):
		self.fnParams = fnParams
		self.name = f"estimate weight in {fnParams}"
		self.pixmap = os.path.join(ICONPATH, f"{fnParams}.svg")
		self.menuText = f"weight in {fnParams}"
		self.toolTip = f"selected body's approximate weight in {fnParams}"

class Estimate_Weight_Custom(BaseCommand):
	name = "estimate weight with custom density"
	function = tools.estimateWeight
	pixmap = os.path.join(ICONPATH, "none.svg")
	menuText = "weight with custom density"
	toolTip = "selected body's approximate weight with custom density"
