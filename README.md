# TOTK-Ultrawide
A tool that generates the necessary exefs and romfs files to play the game in ultrawide (>16:9) aspect ratios.
## Usage
1. Download the latest release
2. Run the `CustomAspect.bat` file
3. Follow the instructions
4. Wait for the script to finish
5. Copy the contents of the Result folder to your mods folder
6. Disable any other aspect ratio mods, controller mods and/or BlackscreenFIX before using this mod
## Merging mods
This tool makes it easy to merge the UI fixes with other mods that change the `Common.Product` file such as controllor mods. Simply replace the `Common.Product` file with the one from the controller mod and run the tool as normal. Do not forget to copy over the `Font` folder to the `\Result\...\romfs` folder created by the program.
## How to build
Compile the files `/src/UIFIX.py` and `/src/pchtxtCreator.py` into an executable using pyinstaller and place them inside the `/bin` folder.
## Known issues
* UI elements belonging to 3D game objects (NPC text balloons, enemy health bars, item descriptions, etc.) are still stretched.  
* Pre-rendered cutscenes play stretched.  
* In the quest menu, part of the map is duplicated.  
* Pictures taken with the in-game camera are squished.  
## Credits
TotkMods for creating [Totk.ZStdTool](https://github.com/TotkMods/Totk.ZStdTool)  
aboood40091 for creating [SARC-Tool](https://github.com/aboood40091/SARC-Tool)  
MarethyuX for his [BlackscreenFIX](https://www.reddit.com/r/NewYuzuPiracy/comments/13hq70a/60_fps_mod_black_screen_fix_not_thoroughly_tested/)  
theboy181 for the orignal asm-patches  
Nintendo for the original game
