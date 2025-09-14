from .resources import icon, LANG
from . import tools, estimateSettings
import json

import FreeCADGui
from FreeCADGui import Selection

class BaseCommand():
	"""
		TMYK: here the commands are defined by child classes, each their own
		* name
		* function
		* pixmap (icon)
		* menu text
		* tooltip

		available commands (classes extending the base command) are initialized with their
		respective properties before FreeCAD calls their methods on interaction
	"""
	fnParams = {}
	FreeCADGui.doCommandGui("import freecad.estimateWB.commands")

	def __init__(self):
		pass

	def GetResources(self):
		return {"Pixmap": self.pixmap,
				"MenuText": self.menuText,
				"ToolTip": self.toolTip}

	def Activated(self):
		"""
			as opposed to the online ressources the parameters are converted to a tuple and json for string passing
			this allows for multiple parameters for commands
		"""
		FreeCADGui.doCommandGui(f"freecad.estimateWB.commands.{self.__class__.__name__}.do('{json.dumps(self.fnParams)}')")

	@classmethod
	def do(self, fnParams:str = ""):
		"""
			reconvert the former passed string back to a tuple and spread as non keyword parameters
		"""
		self.function(*json.loads(fnParams))

################################################################################

class Estimate_Volume(BaseCommand):
	# TMYK: without a parameter for the function the command can be set up just like this
	name = LANG.chunk("estimateVolumeName")
	function = tools.estimateVolume
	pixmap = icon("icon")
	menuText = LANG.chunk("estimateVolumeName")
	toolTip = LANG.chunk("estimateVolumeToolTip")
	def IsActive(self):
		return Selection.hasSelection()

################################################################################

class Estimate_Weight(BaseCommand):
	# TMYK: with a parameter for the function the command has to be set up with __init__
	function = tools.estimateWeight
	def __init__(self, *fnParams):
		self.fnParams = fnParams
		self.name = LANG.chunk("estimateWeightName", {":option": fnParams[0]})
		self.pixmap = icon(fnParams[0])
		self.menuText = LANG.chunk("estimateWeightName", {":option": fnParams[0]})
		self.toolTip = LANG.chunk("estimateWeightToolTip", {":option": fnParams[0]})
	def IsActive(self):
		return Selection.hasSelection()

class Estimate_Weight_Custom(BaseCommand):
	name = LANG.chunk("estimateWeightCustomName")
	function = tools.estimateWeight
	pixmap = icon("none")
	menuText = LANG.chunk("estimateWeightCustomName")
	toolTip = LANG.chunk("estimateWeightCustomToolTip")
	def IsActive(self):
		return Selection.hasSelection()

################################################################################

class Set_estimateSettings(BaseCommand):
	"""
		currently supported fnParams are
		* sizeScale - mm, cm and m
		* weightUnit - g, kg and lb
		* reportOutput - console and popup

		icons have to be named accordingly fnParams[0]_fnParams[1].svg
		language chunks as well

		see __init__.py and languages/*.json
	"""
	function = estimateSettings.set
	def __init__(self, *fnParams):
		self.fnParams = fnParams
		setting, value = fnParams
		self.name = LANG.chunk(setting + "_Setting", {":option": value})
		self.pixmap = icon(f"{setting}_{value}")
		self.menuText = LANG.chunk(setting + "_Setting", {":option": value})
		self.toolTip = LANG.chunk(setting + "_Setting", {":option": value})
	def IsActive(self):
		setting, value = self.fnParams
		return estimateSettings.get(setting) != value

