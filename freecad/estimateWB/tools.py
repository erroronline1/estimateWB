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

def volumeOf(name):
	t = FreeCAD.ActiveDocument.getObjectsByLabel(name)[0]
	if hasattr(t, 'Shape'):
		return t.Shape.Volume
	else:
		report(f"{name} {LANG.chunk('hasNoVolume')[0]}")
		return False

def selectedObject():
	sel = FreeCADGui.Selection.getSelection()
	return sel[0].Label if len(sel) else None

def estimateVolume(*void):
	object = selectedObject()
	volume = volumeOf(object)
	factor={"mm": 1 , "cm": 1000, "m": 1000000000}
	if object and volume:
		volume /= factor[CURRENTSCALE]
		report(f"{object} {LANG.chunk('hasVolumeOf')[0]} {roundup(volume)} {CURRENTSCALE}³")
	else:
		report(LANG.chunk('pleaseSelectPart')[0])

def estimateWeight(material = None):
	object = selectedObject()
	volume = volumeOf(object) / 1000
	if material == "None": # even None, if passed, ends up a string here
		material = None
	density = None
	if object and volume:
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

		report(f"{object} {LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} {CURRENTUNIT} {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")

		# Not sure this is the best way to report stuff in FreeCAD, not a whole lot of things open a new window. I just hate having to try and read
		# the report view for each result. - zackwhit
		msgBox = QtGui.QMessageBox() 
		msgBox.setIcon(QtGui.QMessageBox.Information)
		msgBox.setWindowTitle(LANG.chunk("weightPopTitle")[0])
		msgBox.setText(f"{object} {LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} {CURRENTUNIT} {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")
		msgBox.setStandardButtons(QtGui.QMessageBox.Ok)

		# Adding the result to the clipboard
		copyBtn = QtGui.QPushButton(LANG.chunk("weightPopCopy")[0])
		copyBtn.clicked.connect(lambda: saveToClipboard(f"{roundup(mass)}"))
		msgBox.addButton(copyBtn, QtGui.QMessageBox.AcceptRole)
		
		# Show result message box
		msgBox.exec()

	else:
		report(LANG.chunk('pleaseSelectPart')[0])

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