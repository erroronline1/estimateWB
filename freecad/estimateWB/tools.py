import math
import FreeCAD, FreeCADGui
from datetime import datetime

'''# for developement
def listProperties():
	sel = FreeCADGui.Selection.getSelection()
	for obj in sel:
		for p in dir(obj):
			FreeCAD.Console.PrintMessage("\n"+p)
'''

# supported materials. dependence with command-icons. name:density
materials={
	'ABS': 1.05,
	'PA12': 1.01,
	'PC': 1.4,
	'PLA': 1.25,
	'TPU': 1.22
}

def report(msg):
	FreeCAD.Console.PrintMessage("\n{0} {1}".format(datetime.now().strftime("%H:%M:%S"), msg))

def volumeOf(name):
	t = FreeCAD.ActiveDocument.getObjectsByLabel(name)[0]
	if hasattr(t, 'Shape'):
		return math.ceil(t.Shape.Volume/10) / 100
	else:
		report("{0} has no shape nor volume".format(name))
		return False

def selectedBody():
	sel = FreeCADGui.Selection.getSelection()
	if len(sel):
		for obj in sel:
			return obj.Label
	return None

def estimateVolume(*void):
	body = selectedBody()
	volume = volumeOf(body)
	if body and volume:
		report("{0} has a volume of {1} cm³".format(body, volume))
	else:
		report("please select a part or a body...")

def estimateWeight(material = None):
	body = selectedBody()
	volume = volumeOf(body)
	if body and volume and material:
		report("{0} needs about {1} g of {2}".format(body, math.ceil(volume * materials[material] * 100) / 100, material))
	else:
		report("please select a part or a body...")