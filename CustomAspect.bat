@echo off
set /p "aspect=Enter aspect ratio as float (e.g. 2.38889 for 3440x1440): "
set /p "hud_pos=Enter HUD position ('center' or 'corner'): "
set filename1=Common.Product.100.Nin_NX_NVN
set filename2=Common.Product.110.Nin_NX_NVN

cd /d %~dp0
echo Clearing workspace
rmdir /s /q temp >nul 2>&1
rmdir /s /q Result >nul 2>&1
mkdir temp 
mkdir "Result\0100F2C0115B6000\Custom Aspect\romfs\UI\LayoutArchive"
mkdir "Result\0100F2C0115B6000\Custom Aspect\exefs"

echo Creating exefs patches
bin\pchtxtCreator.exe "%cd%\Result\0100F2C0115B6000\Custom Aspect\exefs" %aspect%

echo Decompressing blarc.zs
bin\ZSTD-Tool-1.0.1.exe d "%cd%\%filename1%.blarc.zs" -o "%cd%\temp\%filename1%.blarc"
bin\ZSTD-Tool-1.0.1.exe d "%cd%\%filename2%.blarc.zs" -o "%cd%\temp\%filename2%.blarc"
echo Unpacking blarc
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename1%.blarc" >nul 2>&1
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename2%.blarc" >nul 2>&1
echo Applying UI Fixes
bin\UIFIX.exe "%cd%\temp\%filename1%" %aspect% %hud_pos%
bin\UIFIX.exe "%cd%\temp\%filename2%" %aspect% %hud_pos%
echo Repacking 
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename1%" >nul 2>&1
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename2%" >nul 2>&1
ren "%cd%\temp\%filename1%.blarc" "%filename1%.blarc_old"
ren "%cd%\temp\%filename2%.blarc" "%filename2%.blarc_old"
ren "%cd%\temp\%filename1%.sarc" "%filename1%.blarc"
ren "%cd%\temp\%filename2%.sarc" "%filename2%.blarc"
echo Compressing blarc
bin\ZSTD-Tool-1.0.1.exe c "%cd%\temp\%filename1%.blarc" -o "%cd%\Result\0100F2C0115B6000\Custom Aspect\romfs\UI\LayoutArchive\%filename1%.blarc.zs"
bin\ZSTD-Tool-1.0.1.exe c "%cd%\temp\%filename2%.blarc" -o "%cd%\Result\0100F2C0115B6000\Custom Aspect\romfs\UI\LayoutArchive\%filename2%.blarc.zs"
echo Deleting temp folder
rmdir /s /q temp
echo Done!

pause
