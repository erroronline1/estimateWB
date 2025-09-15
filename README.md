## Estimate Workbench 

A FreeCAD workbench to estimate material quantity by volume or weight for selected parts

### Background
[This frankenstein's monster of a workbench](#about-the-code) for FreeCAD has been somehow sewn together to work almost as expected.

You can display the volume or expected weight of selected objects at the push of a button. Both display with the decimal precision as set in FreeCAD's settings (2 by default if not specified). Rounding has been adjusted to ignore floating point offsets and limit confusion with defined 1cm³ cubes displaying 1.01 cm³. This might lead to a slight but most likely negligible rounding error, as the output enables you to estimate or calculate the necessary amount of material for additive manufacturing - @100 % infill, ignoring support structures, purging and other slicer settings that add anyway.

Some common 3d-printing materials are supported by default, but you can always select the weight calculation with a custom selected density in g/cm³.

![screenshot](https://raw.githubusercontent.com/erroronline1/estimateWB/master/freecad/estimateWB/resources/screenshot.png)

### Version compatibility

<details>
<summary>Confirmed latest stable FreeCad version 1.0 - Expand for more</summary>

* 1.1rc build 40041 x86_64
* 1.0
* 0.21.2
* 0.19

</details>

### Version update
* 0.1.5
    * same functionality, new codebase
    * settings as a single menu item and toolbar
    * storing last selected preferences
    * a lot of comments within the code for newcomers and future reference 

### Usage

Select objects, parts, groups or bodies and at the push of a button of the workbench the desired output is displayed in the report view panel or as a popup.

Two toolbars are available:

**Settings**
* Select the desired report mode for report view or popup
* Select the desired output for the volume in mm³, cm³ or m³
* Select the desired output for the weight in g, kg or lb 

**Estimate**
* The first option returns the volume of the selected object
* The second option prompts you to provide a decimal density to return the estimated specific but custom weight
* Any other option returns preset material weight estimations (currently ABS, NYLon, PA12, PolyCarbonate, PETG, PLA and TPU)

Thats all. Basically the workbench reads the objects shape.volume-property provided by FreeCAD, which is conveniently returned in mm³. So any output will be in metric units by default, lb and weight units toolbar work of [@zackwhit](https://github.com/zackwhit/). They also added a popup that has been applied to the volume as well in version 0.1.4 - now toggleable for either report view or popup.

[@PhoneDroid](https://github.com/PhoneDroid) added the result for *all selected* parts.

### Installation 

#### Automatic Installation (recommended)

This workbench is available via the FreeCAD [Addon Manager](https://wiki.freecad.org/Std_AddonMgr).

#### Manual Installation

<details>
<summary>Expand for directions to manually install this workbench</summary>

This workbench can be installed manually by adding the whole folder into the personal FreeCAD folder

- for Linux `~/.local/share/FreeCAD/Mod/` or `~/.var/app/org.freecad.FreeCAD/data/FreeCAD/Mod`
- for Windows `%APPDATA%\FreeCAD\Mod\` or `C:\Users\username\Appdata\Roaming\FreeCAD\Mod\`
- for Windows as portable app `wherever_stored\FreeCADPortable\Data\FreeCADAppData\Mod`
- for macOS `~/Library/Preferences/FreeCAD/Mod/`

</details>

### Customize

If you want to change standard materials you can do so by editing the materials.json-file and add a respective named icon to the ressources-folder. The list of buttons will update itself. If you are unsatisfied with the default densities you are free to edit these within the file as well.

Different languages according to user settings are technically supported - but actually restricted to english by default and german due to my own limitations. This might be more proof-of-concept than actually useful but feel free to contribute :) Since one does usually not switch languages by the minute I did not bother finding out how to update during runtime yet, so FreeCad has to be restarted to have language-changes take effect on this workbench.

### Bug/Feedback

Please report bugs to the [issue queue](https://github.com/erroronline1/estimateWB/issues) and ping the [dedicated estimateWB FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=67078) to discuss said issue or feedback in general.   

### About the code
Base of everything has been
* [freecad.workbench_starterkit](https://github.com/FreeCAD/freecad.workbench_starterkit/tree/master/freecad/workbench_starterkit) and
* [gears workbench](https://github.com/looooo/freecad.gears/tree/master/freecad/gears)

[Phonedroid](https://github.com/PhoneDroid) reached out to me in 9/25 if I would still be interested in keeping this workbench maintained. Since then I refactored the code as an attempt to declutter everything a bit. Also they stated the workbench_starterkit might be out of date. I followed the kind recommendations and tried to leave as much comments as reasonable in the code for anyone else to have a decent start for their own workbench:
* the folder structure is valid (root and /freecad/{workbench name})
* the BaseCommand supports multiple parameters for function calls
* you'll need basically only the
    * package.xml,
    * \_\_init__.py and
    * init_gui.py
* pyproject.toml is not mandatory but the way to go if you are in need to define dependent modules not part of the default python libraries
* the distribution of other files as well as the language model are just a decision, versionupdate.py is not more than a tiny helper tool you can easily omit. as far as i understand everything *could* go into the init_gui.py only.

## License

estimateWB is released under the LGPL3+ license. See [LICENSE](LICENSE).
