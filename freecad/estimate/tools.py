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

def volumeOf(name):
	t = FreeCAD.ActiveDocument.getObjectsByLabel(name)[0]
	if hasattr(t, 'Shape'):
		return "{0} cm³".format(math.ceil(t.Shape.Volume/1000))
	else:
		return False

def selectedBody():
	sel = FreeCADGui.Selection.getSelection()
	if len(sel):
		for obj in sel:
			return obj.Label
	return None

def estimateVolume():
	body = selectedBody()
	if not body:
		msg = "Please select a part or body..."
	else:
		volume=volumeOf(body)
		if volume:
			msg = "{0} has an approximate volume of {1}".format(body, volumeOf(body))
		else:
			msg = "{0} has no shape nor volume".format(body)
	FreeCAD.Console.PrintMessage("\n{0} {1}".format(datetime.now().strftime("%H:%M:%S"), msg))

