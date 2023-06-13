@echo off
set /p "filename=Enter the filename of the Common.Product file without .blarc.zs (e.g. Common.Product.110.Nin_NX_NVN): "
set /p "aspect=Enter aspect ratio as float (e.g. 2.38889 for 3440x1440): "
set /p "hud_pos=Enter HUD position ('center' or 'corner'): "

cd /d %~dp0
echo Clearing workspace
rmdir /s /q temp >nul 2>&1
rmdir /s /q Result >nul 2>&1
mkdir temp 
mkdir "Result\0100F2C0115B6000\Custom Aspect\romfs\UI\LayoutArchive"
mkdir "Result\0100F2C0115B6000\Custom Aspect\exefs"

echo Creating exefs patches
bin\pchtxtCreator.exe "%cd%\Result\0100F2C0115B6000\Custom Aspect\exefs" %aspect%

echo Decompressing %filename%.blarc.zs
bin\ZSTD-Tool-1.0.1.exe d "%cd%\%filename%.blarc.zs" -o "%cd%\temp\%filename%.blarc"
echo Unpacking %filename%.blarc
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename%.blarc" >nul 2>&1
echo Applying UI Fixes
bin\UIFIX.exe "%cd%\temp\%filename%" %aspect% %hud_pos%
echo Repacking %filename%
bin\sarc_tool_x64_v0.5\sarc_tool.exe "%cd%\temp\%filename%" >nul 2>&1
ren "%cd%\temp\%filename%.blarc" "%filename%.blarc_old"
ren "%cd%\temp\%filename%.sarc" "%filename%.blarc"
echo Compressing %filename%.blarc
bin\ZSTD-Tool-1.0.1.exe c "%cd%\temp\%filename%.blarc" -o "%cd%\Result\0100F2C0115B6000\Custom Aspect\romfs\UI\LayoutArchive\%filename%.blarc.zs"
echo Deleting temp folder
rmdir /s /q temp
echo Done!

pause
