import os
import FreeCADGui
from . import ICONPATH, tools

class estimateWorkbench(FreeCADGui.Workbench):
	MenuText = "Estimate"
	ToolTip = "Display a bodys volume or weight to estimate costs of printing"
	Icon = os.path.join(ICONPATH, 'icon.svg')
	
	commands = [
		"Estimate_Volume"]
	for type in tools.materials:
		commands.append("Estimate_{}_Weight".format(type))

	def Initialize(self):
		"""This function is executed when FreeCAD starts"""
		from . import commands #, import here all the needed files that create your FreeCAD commands
		self.appendToolbar("Estimate", self.commands)
		self.appendMenu("Estimate", self.commands)

	def Activated(self):
		pass

	def Deactivated(self):
		pass

	def ContextMenu(self, recipient):
		# self.appendContextMenu("My commands",self.list) # add commands to the context menu / right click
		pass

	def GetClassName(self): 
		# This function is mandatory if this is a full Python workbench
		# This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
		return "Gui::PythonWorkbench"
	   
FreeCADGui.addWorkbench(estimateWorkbench())