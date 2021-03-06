import os
from datetime import datetime
from decimal import Decimal, ROUND_UP
import json
import FreeCAD, FreeCADGui
from PySide import QtGui
from . import LANGUAGEPATH, ICONPATH

# supported materials. dependence with command-icons. name:density

with open(os.path.join(ICONPATH, 'materials.json'), 'r') as jsonfile:
		materials= json.loads(jsonfile.read().replace('\n', ''))
CURRENTSCALE="cm"

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
	factor={"mm": 1 , "cm": 1000, "m": 1000000}
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
		report(f"{object} {LANG.chunk('needsMaterialOf')[0]} {roundup(mass)} g {LANG.chunk('needsMaterialOf')[1] + material if material else ''}")
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