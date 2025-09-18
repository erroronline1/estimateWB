import freecad.estimateWB as module
from importlib import resources
import json
import FreeCAD

resourcefiles = resources.files(module) / "resources"
languagefiles = resources.files(module) / "languages"


def icon(name: str):
	"""	returns an icon file path """
	file = name + ".svg"
	icon = resourcefiles / file
	with resources.as_file(icon) as path:
		return str(path)


with resources.as_file(resourcefiles / "materials.json") as path:
	with open(str(path), "r") as jsonfile:
		""" preparing the material list with names and densities """
		materials = json.loads(jsonfile.read().replace("\n", ""))


class language:
	def __init__(self):
		# try to open the language file according to FreeCAD settings, default to english
		try:
			language = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/General").GetString("Language")
			with open(languagefiles / f"{language}.json", "r") as jsonfile:
				self.language = json.loads(jsonfile.read().replace("\n", ""))
		except:
			with open(languagefiles / "English.json", "r") as jsonfile:
				self.language = json.loads(jsonfile.read().replace("\n", ""))
	

	def chunk(self, chunk:str, replacements:dict = {}):
		"""
			returns the requested language chunk from the loaded language file
			a passed dict replaces found keys with the corresponding value
		"""
		chunk = self.language.get(chunk)
		if chunk and len(replacements):
			# replace found dict keys with their value
			for find, replace in replacements.items():
				chunk = chunk.replace(find, replace);
		return chunk

LANG = language()