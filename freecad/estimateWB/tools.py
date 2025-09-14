from .resources import materials, LANG
from . import estimateSettings
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

import FreeCAD
import FreeCADGui
from PySide import QtGui

################################################################################
# reporting
################################################################################

def report(msg: str):
	""" prints the message to the report view panel """
	now = datetime.now().strftime("%H:%M:%S")
	FreeCAD.Console.PrintMessage(f"\n{now} {msg}")


def msgbox(title: str, msg: str, copy: str):
	""" displays the result as a popup with option to copy a value """

	# Not sure this is the best way to report stuff in FreeCAD, not a whole lot of things open a new window. I just hate having to try and read
	# the report view for each result. - zackwhit
	msgBox = QtGui.QMessageBox() 
	msgBox.setIcon(QtGui.QMessageBox.Information)
	msgBox.setWindowTitle(title)
	msgBox.setText(msg)
	msgBox.setStandardButtons(QtGui.QMessageBox.Ok)

	# Adding the result to the clipboard
	copyBtn = QtGui.QPushButton(LANG.chunk("resultWeightPopCopy"))
	copyBtn.clicked.connect(lambda: saveToClipboard(copy))
	msgBox.addButton(copyBtn, QtGui.QMessageBox.AcceptRole)
	
	# Show result message box
	msgBox.exec()


def saveToClipboard(textToSave: str):
	"""	copies the parameter to clipboard """
	QtGui.QGuiApplication.clipboard().setText(textToSave)


################################################################################
# calculations
################################################################################

def roundup(number: float):
	""" returns the rounded number according to FreeCad settings"""
	precision = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals")
	precision = 2 if not precision else precision
	return Decimal(number).quantize(Decimal("1e" + str(-precision)), rounding = ROUND_HALF_UP)


def volumeOf(object: object):
	""" returns the volume of the passed object """
	if hasattr(object, "Shape"):
		return object.Shape.Volume
	else:
		report(LANG.chunk("resultHasNoVolume", {":object": object.Label}))
		return 0.0


def estimateVolume(*void):
	""" calculates the volume of selected objects and reports to the selected report option """
	objects = FreeCADGui.Selection.getSelection()

	volume = 0.0

	for object in objects:
		volume += volumeOf(object)

	if volume == 0:
		if len(objects) > 1 :
			report(LANG.chunk("resultSelectionNoVolume"))
		return

	volume /= float(estimateSettings.get("sizeScaleFactor"))
	
	msg = LANG.chunk("resultHasVolumeOf", {":volume" : str(roundup(volume)) + estimateSettings.get("sizeScale") + "³"})
	if estimateSettings.get("reportOutput") == "console":
		report(msg)
	elif estimateSettings.get("reportOutput") == "popup":
		msgbox(LANG.chunk("resultVolumePopTitle"), msg, f"{str(roundup(volume))}")


def estimateWeight(material : str|None = None):
	"""
		calculates the weight of the selected objects according to the passed material and reports to the selected report option  
		prompts for density if no material has been passed
	"""
	objects = FreeCADGui.Selection.getSelection()

	volume = 0.0

	for object in objects:
		volume += volumeOf(object)
		
	if volume == 0:
		if len(objects) > 1 :
			report(LANG.chunk("resultSelectionNoVolume"))
		return
    
	if material == "None": # even None, if passed, ends up a string here
		material = None
	
	density = None

	if material:
		density = materials[material]
	else:
		try:
			density = float(QtGui.QInputDialog.getText(None, LANG.chunk("promptDensityTitle"), LANG.chunk("promptDensityText"))[0].replace(",", "."))
		except:
			pass
	if not density:
		report(LANG.chunk("promptDensityError"))
		return
	
	# FreeCAD reported volume is always mm³
	# density is always g/cm³
	volume /= 1000
	
	mass = volume * density
	mass = mass * float(estimateSettings.get("weightUnitFactor"))

	msg = LANG.chunk("resultNeedsMaterialOf", {":amount" : str(roundup(mass)) + estimateSettings.get("weightUnit"), ":material": material if material else ""})
	if estimateSettings.get("reportOutput") == "console":
		report(msg)
	elif estimateSettings.get("reportOutput") == "popup":
		msgbox(LANG.chunk("resultWeightPopTitle"), msg, f"{roundup(mass)}")
