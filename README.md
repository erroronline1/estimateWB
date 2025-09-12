## Estimate Workbench 

A FreeCAD workbench to estimate material quantity by volume or weight or selected parts

### Background
This frankenstein's monster of a workbench for FreeCAD has been somehow sewn together to work almost as expected.

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

### Usage

Select an object, part, group or body and at the push of a button of the workbench the desired output is displayed in the report view panel or as a popup.

Four toolbars are available:

**Report**
* Select the desired report mode for report view or popup

**Scale**
* Select the desired output for the volume in mm³, cm³ or m³

**Estimate**
* The first option returns the volume of the selected object
* The second option prompts you to provide a decimal density to return the estimated specific but custom weight
* Any other option returns preset material weight estimations (currently ABS, NYLon, PA12, PolyCarbonate, PETG, PLA and TPU)

**Weight Units**
* Select the desired output for the weight in g, kg or lb 

Thats all. Basically the workbench reads the objects shape.volume-property provided by FreeCAD, which is conveniently returned in mm³. So any output will be in metric units by default, lb and weight units toolbar work of [@zackwhit](https://github.com/zackwhit/). They also added a popup that has been applied to the volume as well in version 0.1.4 - now toggleable for either report view or popup.

[@PhoneDroid](https://github.com/PhoneDroid) added the result for all *selected* parts.

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

Occasionally rename from estimateWB-master to estimateWB if downloaded as zip from github

</details>

### Customize

If you want to change standard materials you can do so by editing the materials.json-file and add a respective named icon to the ressources-folder. The list of buttons will update itself. If you are unsatisfied with the default densities you are free to edit these within the file as well.

Different languages according to user settings are technically supported - but actually restricted to english by default and german due to my own limitations. This might be more proof-of-concept than actually useful but feel free to contribute :) Since one does usually not switch languages by the minute I did not bother finding out how to update during runtime yet, so FreeCad has to be restarted to have language-changes take effect on this workbench.

### Bug/Feedback

Please report bugs to the [issue queue](https://github.com/erroronline1/estimateWB/issues) and ping the [dedicated estimateWB FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=22&t=67078) to discuss said issue or feedback in general.   

## License

estimateWB is released under the LGPL3+ license. See [LICENSE](LICENSE).
