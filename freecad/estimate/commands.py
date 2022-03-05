import FreeCADGui
import os
from . import ICONPATH
from . import tools

class BaseCommand():
	FreeCADGui.doCommandGui("import freecad.estimate.commands")

	def __init__(self):
		pass

	def IsActive(self):
		return bool(tools.selectedBody())

	def GetResources(self):
		return {'Pixmap': self.pixmap,
				'MenuText': self.menuText,
				'ToolTip': self.toolTip}

	def Activated(self):
		FreeCADGui.doCommandGui("freecad.estimate.commands.{}.do()".format(self.__class__.__name__))

	@classmethod
	def do(self):
		print ([p for p in dir(self)])
		self.function()

################################################################################

class Estimate_Volume(BaseCommand):
	name = "estimate volume"
	function = tools.estimateVolume
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = "volume"
	toolTip = "selected body's volume rounded up to whole cm³"
#
FreeCADGui.addCommand("Estimate_Volume", Estimate_Volume())

###############################################################################

class BaseWeight():
	def __init__(self, what):
		self.name = "estimate weight in {}".format(what)
		self.pixmap = os.path.join(ICONPATH, "{}.svg".format(what))
		self.menuText = "weight in {}".format(what)
		self.toolTip = "selected body's approximate weight in {}".format(what)


class Estimate_ABS_Weight(BaseCommand, BaseWeight):
	def __init__(self):
		BaseWeight.__init__(self, 'ABS')
	function = tools.estimateABSWeight
#
FreeCADGui.addCommand("Estimate_ABS_Weight", Estimate_ABS_Weight())


class Estimate_PA12_Weight(BaseCommand, BaseWeight):
	def __init__(self):
		BaseWeight.__init__(self, 'PA12')
	function = tools.estimatePA12Weight
#
FreeCADGui.addCommand("Estimate_PA12_Weight", Estimate_PA12_Weight())


class Estimate_PC_Weight(BaseCommand, BaseWeight):
	def __init__(self):
		BaseWeight.__init__(self, 'PC')
	function = tools.estimatePCWeight
#
FreeCADGui.addCommand("Estimate_PC_Weight", Estimate_PC_Weight())


class Estimate_PLA_Weight(BaseCommand, BaseWeight):
	def __init__(self):
		BaseWeight.__init__(self, 'PLA')
	function = tools.estimatePLAWeight
#
FreeCADGui.addCommand("Estimate_PLA_Weight", Estimate_PLA_Weight())


class Estimate_TPU_Weight(BaseCommand, BaseWeight):
	def __init__(self):
		BaseWeight.__init__(self, 'TPU')
	function = tools.estimateTPUWeight
#
FreeCADGui.addCommand("Estimate_TPU_Weight", Estimate_TPU_Weight())
