import FreeCAD, FreeCADGui
from datetime import datetime
from decimal import Decimal, ROUND_UP
from PySide import QtGui

# supported materials. dependence with command-icons. name:density
materials={
	'ABS': 1.05,
	'PA12': 1.01,
	'PC': 1.4,
	'PLA': 1.25,
	'TPU': 1.22
}

def report(msg):
	now=datetime.now().strftime("%H:%M:%S")
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
		report(f"{name} has no shape nor volume")
		return False

def selectedObject():
	sel = FreeCADGui.Selection.getSelection()
	return sel[0].Label if len(sel) else None

def estimateVolume(*void):
	object = selectedObject()
	volume = volumeOf(object)
	if object and volume:
		report(f"{object} has a volume of {roundup(volume)} cm³")
	else:
		report("please select a part or a body...")

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
				density=float(QtGui.QInputDialog.getText(None, "Custom", "Enter density:")[0].replace(",","."))
			except:
				pass
		if not density:
			report("no density entered, please use decimal numbers only...")
			return
		mass = volume * density
		report(f"{object} needs about {roundup(mass)} g {'of ' + material if material else ''}")
	else:
		report("please select a part or a body...")