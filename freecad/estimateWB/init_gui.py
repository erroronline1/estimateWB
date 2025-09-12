import os
from . import ICONPATH, tools

import FreeCADGui

class estimateWB(FreeCADGui.Workbench):
	
	MenuText = "Estimate"
	ToolTip = tools.LANG.chunk("wbToolTip")[0] #"Display a body's volume or weight to estimate costs of printing"
	Icon = os.path.join(ICONPATH, "icon.svg")
	
	commands = [
		"Report_console", "Report_popup",
		"Scale_qmm", "Scale_qcm", "Scale_qm",
		"Weight_g", "Weight_kg", "Weight_lb",
		"Estimate_Volume", "Estimate_Weight_Custom",
		]
	
	for type in tools.materials:
		commands.append(f"Estimate_{type}_Weight")

	def Initialize(self):
		"""This function is executed when FreeCAD starts"""
		from . import commands #, import here all the needed files that create your FreeCAD commands

		self.appendToolbar("Report", self.commands[:2])
		self.appendMenu("Report", self.commands[:2])
		FreeCADGui.addCommand("Report_console", commands.Toggle_Report("console"))
		FreeCADGui.addCommand("Report_popup", commands.Toggle_Report("popup"))

		self.appendToolbar("Scale", self.commands[2:5])
		self.appendMenu("Scale", self.commands[2:5])
		for type in ['mm', 'cm', 'm']:
			FreeCADGui.addCommand(f"Scale_q{type}", commands.Set_Scale(type))

		# Handles the weight units (move to selecting based on preferences in freeCAD?)
		# I can foresee some cases in which you'd want to work in one unit system, yet
		# display the volume or weight in a different unit system.
		self.appendToolbar("Weight Units", self.commands[5:8])
		self.appendMenu("Weight Units", self.commands[5:8])
		for massUnit in ['lb', 'kg', 'g']:
			FreeCADGui.addCommand(f"Weight_{massUnit}", commands.Set_Weight_Unit(massUnit))

		self.appendToolbar("Estimate", self.commands[8:])
		self.appendMenu("Estimate", self.commands[8:])
		FreeCADGui.addCommand("Estimate_Volume", commands.Estimate_Volume())
		FreeCADGui.addCommand("Estimate_Weight_Custom", commands.Estimate_Weight_Custom())
		for type in tools.materials:
			FreeCADGui.addCommand(f"Estimate_{type}_Weight", commands.Estimate_Weight(type))

	def Activated(self):
		pass

	def Deactivated(self):
		pass

	def ContextMenu(self, recipient):
		# self.appendContextMenu("My commands",self.list) # add commands to the context menu / right click
		pass

	# This function is mandatory if this is a full Python workbench
	# This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
	
	def GetClassName(self): 
		return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(estimateWB())