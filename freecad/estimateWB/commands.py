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
		return bool(tools.selectedBody())

	def GetResources(self):
		return {'Pixmap': self.pixmap,
				'MenuText': self.menuText,
				'ToolTip': self.toolTip}

	def Activated(self):
		FreeCADGui.doCommandGui("freecad.estimateWB.commands.{0}.do('{1}')".format(self.__class__.__name__, self.fnParams))

	@classmethod
	def do(self, fnParams=None):
		self.function(fnParams)

################################################################################

class Estimate_Volume(BaseCommand):
	name = "estimate volume"
	function = tools.estimateVolume
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = "volume"
	toolTip = "selected body's volume rounded up to whole cm³"

###############################################################################

class Estimate_Weight(BaseCommand):
	function = tools.estimateWeight
	def __init__(self, fnParams):
		self.fnParams = fnParams
		self.name = "estimate weight in {}".format(fnParams)
		self.pixmap = os.path.join(ICONPATH, "{}.svg".format(fnParams))
		self.menuText = "weight in {}".format(fnParams)
		self.toolTip = "selected body's approximate weight in {}".format(fnParams)

