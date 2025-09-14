from .resources import icon, materials, LANG

import FreeCADGui

class estimateWB(FreeCADGui.Workbench):
	"""
		this is the main workbench class that embeds the menu and toolbar buttons with assigned functions
	"""

	MenuText = "Estimate"
	ToolTip = LANG.chunk("wbToolTip")
	Icon = icon("icon")
	
	def Initialize(self):
		"""
			This function is executed when FreeCAD starts
		"""

		# TMYK: import all the needed files that contain your FreeCAD commands here
		from . import commands 

		# setting commands
		fn = {
			"Report_console": commands.Set_estimateSettings("reportOutput", "console"),
			"Report_popup": commands.Set_estimateSettings("reportOutput", "popup"),
			"Scale_qmm": commands.Set_estimateSettings("sizeScale", "mm"),
			"Scale_qcm": commands.Set_estimateSettings("sizeScale", "cm"),
			"Scale_qm": commands.Set_estimateSettings("sizeScale", "m"),
			"Weight_g": commands.Set_estimateSettings("weightUnit", "g"),
			"Weight_kg": commands.Set_estimateSettings("weightUnit", "kg"),
			"Weight_lb": commands.Set_estimateSettings("weightUnit", "lb")
		}
		# TMYK: the first parameter is visible e.g as the menu entry, second parameter is a list of the assigned commands names
		# you could as well assign a manual list as second parameter
		self.appendToolbar(LANG.chunk("settingsMenuText"), list(fn.keys()))
		self.appendMenu(LANG.chunk("settingsMenuText"), list(fn.keys()))
		# you could as well add every command linewise, with the first parameter being the assigned command name, the second the respective function call
		for type in fn:
			FreeCADGui.addCommand(type, fn[type])

		# estimate commands
		# TMYK: but assigning like this is actually cool, because it is dynamically extendable
		fn = {
			"Estimate_Volume": commands.Estimate_Volume(),
			"Estimate_Weight_Custom": commands.Estimate_Weight_Custom()
		}
		for type in materials:
			fn[f"Estimate_{type}_Weight"] = commands.Estimate_Weight(type)

		self.appendToolbar(LANG.chunk("estimateMenuText"), list(fn.keys()))
		self.appendMenu(LANG.chunk("estimateMenuText"), list(fn.keys()))
		for type in fn:
			FreeCADGui.addCommand(type, fn[type])

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