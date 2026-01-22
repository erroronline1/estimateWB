## Estimate Workbench 

A FreeCAD workbench to estimate material quantity by volume or weight for selected parts

You can display the volume or expected weight of selected objects at the push of a button. Both display with the decimal precision as set in FreeCAD's settings (2 by default if not specified). Rounding has been adjusted to ignore floating point offsets and limit confusion with defined 1cm³ cubes displaying 1.01 cm³. This might lead to a slight but most likely negligible rounding error, as the output enables you to estimate or calculate the necessary amount of material for additive manufacturing - @100 % infill, ignoring support structures, purging and other slicer settings that add anyway.

Some common 3d-printing materials are supported by default, but you can always select the weight calculation with a custom selected density in g/cm³.

![screenshot](https://raw.githubusercontent.com/erroronline1/estimateWB/master/freecad/estimateWB/resources/screenshot.png)

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

Thats all. Basically the workbench reads the objects shape.volume-property provided by FreeCAD, which is conveniently returned in mm³.

### Bug/Feedback

Please report bugs to the [issue queue](https://github.com/erroronline1/estimateWB/issues) and ping the [dedicated estimateWB FreeCAD forum thread](https://forum.freecad.org/viewtopic.php?f=22&t=67078) to discuss said issue or feedback in general.   