import FreeCAD

class Settings():
    """
        this could be placed somewhere else as well, but this file would be empty otherwise
        and it initiates, in fact, the current settings for the workbench
        from . import estimateSettings
    """
    options = {
        "sizeScale": {
            "mm": 1,
            "cm": 1000,
            "m": 1000000000
        },
        "weightUnit": {
            "g": 1,
            "kg": 0.001,
            "lb": 0.00220462262185
        },
        "reportOutput": [
            "console",
            "popup"
        ]
    }

    def __init__ (self):
        # default settings
        self.current = {
            "sizeScale": "cm",
            "sizeScaleFactor": 1000,
            "weightUnit": "g",
            "weightUnitFactor": 1,
            "reportOutput": "console"
        }

        # load last user preferences
        try:
            for type in ["sizeScale", "weightUnit", "reportOutput"]:
                value = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/estimateWB").GetString(type)
                if value:
                    self.current.update({type: value})
                    if type in["weightUnit", "sizeScale"]:
                        self.current.update({type + "Factor": self.options.get(type).get(value)})
        except:
            pass
    
    def get(self, type: str):
        """
            use e.g. like estimateSettings.get("sizeScale")  
            available options are
            * sizeScale
            * sizeScaleFactor
            * weightUnit
            * weightUnitFactor
            * reportOutput
        """
        return self.current.get(type)
    
    def set(self, type:str, value: str):
        """
            use e.g. like estimateSettings.set("sizeScale", "cm")  
            available options are
            * sizeScale - mm, cm and m
            * weightUnit - g, kg and lb
            * reportOutput - console and popup

            sizeScaleFactor and weightUnitFactor are set accordingly
            settings are stored in the workbenchs preferences
        """
        if type in list(self.options.keys()):
            self.current.update({type: value})

            FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/estimateWB").SetString(type, value)

            if type in["weightUnit", "sizeScale"]:
                self.current.update({type + "Factor": self.options.get(type).get(value)})

        return None

estimateSettings = Settings()