## Estimate Workbench 

A FreeCAD workbench to estimate material quantity

### Background
This frankenstein's monster of a workbench for FreeCAD has been somehow sewn together to work almost as expected. The initial stage displays a selected body's volume rounded up to whole cm³. Furthermore, some materials are supported to calculate the volume with the material's density to get the expected weight. This estimation enables you to get or calculate the necessary amount of material for additive manufacturing (@100 % infill, ignoring support structures).

**Note:** I am quite new to FreeCAD and creating workbenches but nonetheless excited.

The workbench has been tested with FreeCAD v0.19

### Installation 

#### Manual Installation

This workbench can be installed manually by adding the whole folder into the personal FreeCAD folder

- for Linux `/home/user/.local/share/FreeCAD/Mod/`
- for Windows `%APPDATA%\FreeCAD\Mod\` or `C:\Users\username\Appdata\Roaming\FreeCAD\Mod\`
- for Windows as portable app `wherever_stored\FreeCADPortable\Data\FreeCADAppData\Mod`
- for macOS `~/Library/Preferences/FreeCAD/Mod/`

Occasionally rename from estimateWB-master to estimateWB if downloaded as zip from github

## License

estimateWB is released under the LGPL3+ license. See [LICENSE](LICENSE).
