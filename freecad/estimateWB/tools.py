import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import json
import FreeCAD, FreeCADGui
from PySide import QtGui
from . import LANGUAGEPATH, ICONPATH

# supported materials. dependence with command-icons. name:density

with open(os.path.join(ICONPATH, 'materials.json'), 'r') as jsonfile:
		materials= json.loads(jsonfile.read().replace('\n', ''))
CURRENTSCALE="cm"

CURRENTUNIT="g"

UNITSCALER = 1; # Defaults to grams

def saveToClipboard(textToSave):
	QtGui.QGuiApplication.clipboard().setText(textToSave)

def report(msg):
	now = datetime.now().strftime("%H:%M:%S")
	FreeCAD.Console.PrintMessage(f"\n{now} {msg}")

def roundup(number):
	precision = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals")
	precision = 2 if not precision else precision
	return Decimal(number).quantize(Decimal("1e" + str(-precision)), rounding = ROUND_HALF_UP)

def volumeOf( object ):
	if hasattr(object, 'Shape'):
		return object.Shape.Volume
	else:
		report(f"'{ object.Label }' {LANG.chunk('hasNoVolume')[0]}")
		return 0.0

def estimateVolume(*void):
	
	objects = FreeCADGui.Selection.getSelection()

	volume = 0.0

	for object in objects:
		volume += volumeOf(object)

	if volume == 0:

		if len(objects) > 1 :
			report(LANG.chunk('selectionNoVolume')[0])

		return

	factor={"mm": 1 , "cm": 1000, "m": 1000000000}
	
	volume /= factor[CURRENTSCALE]
	
	report(f"{LANG.chunk('hasVolumeOf')[0]} {roundup(volume)} {CURRENTSCALE}³")


def estimateWeight(material = None):
	
	objects = FreeCADGui.Selection.getSelection()

	volume = 0.0

	for object in objects:
		volume += volumeOf(object)
		
	if volume == 0:

		if len(objects) > 1 :
			report(LANG.chunk('selectionNoVolume')[0])

		return

	volume /= 1000
	
	if material == "None": # even None, if passed, ends up a string here
		material = None
	
	density = None

	if material:
		density = materials[material]
	else:
		try:
			density = float(QtGui.QInputDialog.getText(None, LANG.chunk('densityPromptTitle')[0], LANG.chunk('densityPromptText')[0])[0].replace(",", "."))
		except:
			pass
	if not density:
		report(LANG.chunk('noDensityEntered')[0])
		return
	
	mass = volume * density
	mass = mass*UNITSCALER

	report(f"{LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} {CURRENTUNIT} {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")

	# Not sure this is the best way to report stuff in FreeCAD, not a whole lot of things open a new window. I just hate having to try and read
	# the report view for each result. - zackwhit
	msgBox = QtGui.QMessageBox() 
	msgBox.setIcon(QtGui.QMessageBox.Information)
	msgBox.setWindowTitle(LANG.chunk("weightPopTitle")[0])
	msgBox.setText(f"{LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} {CURRENTUNIT} {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")
	msgBox.setStandardButtons(QtGui.QMessageBox.Ok)

	# Adding the result to the clipboard
	copyBtn = QtGui.QPushButton(LANG.chunk("weightPopCopy")[0])
	copyBtn.clicked.connect(lambda: saveToClipboard(f"{roundup(mass)}"))
	msgBox.addButton(copyBtn, QtGui.QMessageBox.AcceptRole)
	
	# Show result message box
	msgBox.exec()

class language:
	def __init__(self):
		try:
			'''load settings'''
			with open(f'{os.path.join(LANGUAGEPATH, FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetString("Language"))}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))
		except:
			with open(f'{os.path.join(LANGUAGEPATH, "English")}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))
	def chunk(self, chunk):
		return self.language[chunk]
LANG=language()

def setScale(to):
	global CURRENTSCALE
	CURRENTSCALE=to

def setWeightUnit(weightUnit):
	global CURRENTUNIT
	global UNITSCALER
	CURRENTUNIT = weightUnit

	# this is probably a terrible approach
	if (weightUnit == "g"):
		UNITSCALER = 1
	elif (weightUnit == "kg"):
		UNITSCALER = 0.001
	elif (weightUnit == "lb"):
		UNITSCALER = 0.00220462262185