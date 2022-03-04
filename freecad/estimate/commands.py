import FreeCADGui
from . import tools
import os
from . import ICONPATH

class BaseCommand():
	name = ""
	function = None
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
		pass 
		"""Do something here"""
		FreeCADGui.doCommandGui("freecad.estimate.commands.{}.do()".format(self.__class__.__name__))

	@classmethod
	def do(cls):
		cls.function()
		
################################################################################

class Estimate_Volume(BaseCommand):
	name = "estimate volume"
	function = tools.estimateVolume
	pixmap = os.path.join(ICONPATH, "icon.svg")
	menuText = "estimate volume"
	toolTip = "selected body's volume rounded up to whole cm³"