# TOTK-Ultrawide
A tool that generates the necessary exefs and romfs files to play the game in custom aspect ratios.
## Usage
1. Download the [latest release](https://github.com/Fruithapje21/TOTK-Ultrawide/releases/latest)
2. Run `TOTK-Ultrawide.exe`
3. Follow the instructions
4. Wait for the script to finish
5. Copy the newly created `/TOTK-Ultrawide` folder to your mods folder
6. Disable any other aspect ratio mods, controller mods and/or BlackscreenFIX before using this mod
7. Select `Stretch to Window` under `configuration > Graphics > Aspect Ratio`
8. If using [TOTK Optimizer](https://github.com/MaxLastBreath/TOTK-mods) (which is recommended), open the file `maxlastbreath.ini` located in the `.../0100F2C0115B6000/!!!TOTK Optimizer/romfs/UltraCam` folder and change the values for `Width` and `Height` to match your screen resolution
## Pre-made mods
In case you have a common non-16:9 aspect ratio, you can likely find a pre-made version in the `/mods` folder. It curretly includes mods for 1-1, 5-4, 4-3, 3-2, 16-10, 256-135, 18-9, 19.5-9, 20-9, 21-9, 21.5-9, 32-9 and 48-9.
## Merging mods
This tool makes it easy to merge the UI fixes with other mods that change the `Common.Product` file such as controller mods. Simply replace the `Common.Product` file with the one from the controller mod and run the tool as normal. Do not forget to copy over the `Font` folder to the `/TOTK-Ultrawide/romfs` folder created by the program.
## How to build
Compile the file `main.py` into an executable using pyinstaller and place it inside the root folder.
## Known issues
* Pre-rendered cutscenes play stretched. 
* Pictures taken with the in-game camera are squished.
## Credits
MarethyuX for BlackscreenFIX  
theboy181 for some of the asm-patches   
Nintendo for the original game
