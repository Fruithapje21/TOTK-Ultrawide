# TOTK-Ultrawide
A tool that generates the necessary exefs and romfs files to play the game in ultrawide (>16:9) aspect ratios.
## Usage
1. Download the [latest release](https://github.com/Fruithapje21/TOTK-Ultrawide/releases/latest)
2. Run `TOTK-Ultrawide.exe`
3. Follow the instructions
4. Wait for the script to finish
5. Copy the newly created `/TOTK-Ultrawide` folder to your mods folder
6. Disable any other aspect ratio mods, controller mods and/or BlackscreenFIX before using this mod
   
## Pre-made mods
In case you have a common (ultrawide) aspect ratio, you can likely find a pre-made version in the `/mods` folder. It curretly includes mods for 18/9, 20/9, 21.5/9, 32/9 and 48/9.
## Merging mods
This tool makes it easy to merge the UI fixes with other mods that change the `Common.Product` file such as controllor mods. Simply replace the `Common.Product` file with the one from the controller mod and run the tool as normal. Do not forget to copy over the `Font` folder to the `/TOTK-Ultrawide/.../romfs` folder created by the program.
## How to build
Compile the file `main.py` into an executable using pyinstaller and place it inside the root folder.
## Known issues
* Pre-rendered cutscenes play stretched.
* In the quest menu, part of the map is duplicated.  
* Pictures taken with the in-game camera are squished.
## Additional note
The `/mods` folder also includes files to play the game in 16:10. You will however not be able to create these files using the tool (which is only for >16:9).
## Credits
MarethyuX for his BlackscreenFIX
theboy181 for some of the asm-patches  
Alerion921 for Steam Deck UI  
Silentverge for the FOV mod  
Nintendo for the original game
