import os
from datetime import datetime
from decimal import Decimal, ROUND_UP
import json
import FreeCAD, FreeCADGui
from PySide import QtGui
from . import LANGUAGEPATH

# supported materials. dependence with command-icons. name:density
materials={
	'ABS': 1.05,
	'NYL': 1.08,
	'PA12': 1.01,
	'PC': 1.4,
	'PETG': 1.27,
	'PLA': 1.25,
	'TPU': 1.22
}

def report(msg):
	now = datetime.now().strftime("%H:%M:%S")
	FreeCAD.Console.PrintMessage(f"\n{now} {msg}")

def roundup(number):
	precision = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Units").GetInt("Decimals")
	precision = 2 if not precision else precision
	return Decimal(number).quantize(Decimal("1e" + str(-precision)), rounding = ROUND_UP)

def volumeOf(name):
	t = FreeCAD.ActiveDocument.getObjectsByLabel(name)[0]
	if hasattr(t, 'Shape'):
		return t.Shape.Volume / 1000
	else:
		report(f"{name} {LANG.chunk('hasNoVolume')[0]}")
		return False

def selectedObject():
	sel = FreeCADGui.Selection.getSelection()
	return sel[0].Label if len(sel) else None

def estimateVolume(*void):
	object = selectedObject()
	volume = volumeOf(object)
	if object and volume:
		report(f"{object} {LANG.chunk('hasVolumeOf')[0]} {roundup(volume)} cm³")
	else:
		report(LANG.chunk('pleaseSelectPart')[0])

def estimateWeight(material = None):
	object = selectedObject()
	volume = volumeOf(object)
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
		report(f"{object} {LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} g {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")
	else:
		report(LANG.chunk('pleaseSelectPart')[0])

class language():
	def __init__(self):
		self.sysLang = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetString("Language")
		try:
			'''load settings'''
			with open(f'{os.path.join(LANGUAGEPATH, self.sysLang)}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))
		except:
			with open(f'{os.path.join(LANGUAGEPATH, "English")}.json', 'r') as jsonfile:
				self.language = json.loads(jsonfile.read().replace('\n', ''))

	def chunk(self, chunk):
		return self.language[chunk]
LANG=language()
