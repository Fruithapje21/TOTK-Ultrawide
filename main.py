import os
import sys
import shutil
from romfs_script import patch_romfs
from exefs_srcipt import create_pchtxt
from file_archive import compress_zs, decompress_zs, extract_blarc, repack_blarc

def myexcepthook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Press RETURN. ")

def patch_zs(filename):
    zs_path = os.path.join(working_dir, filename + '.blarc.zs')
    blarc_path = os.path.join(temp_dir, filename + '.blarc')
    extracted_blarc_dir = os.path.join(temp_dir, filename)
    patched_zs_path = os.path.join(LayouArchive_dir, filename + '.blarc.zs')
  
    print('Decompressing zs')
    decompress_zs(zs_path, blarc_path, zsdic_path)
    print('Extracting blarc')
    extract_blarc(blarc_path, extracted_blarc_dir)
    print('Patching contents')
    patch_romfs(extracted_blarc_dir, aspect_ratio, hud_pos)
    print('Repacking blarc')
    repack_blarc(extracted_blarc_dir, blarc_path)
    print('Compressing zs')
    compress_zs(blarc_path, patched_zs_path, zsdic_path)
    
sys.excepthook = myexcepthook

supported_versions = ['1.0.0', '1.1.0', '1.1.1', '1.1.2', '1.2.0', 'all']

aspect_ratio = float(eval(input('Enter your aspect ratio (e.g. 21.5/9, 3440/1440 or 2.38889): ')))
if aspect_ratio < 16/9:
    raise Exception('Aspect ratios smaller than 16/9 are not supported')
    
hud_pos = input('Where would you like the HUD (center or corner): ')
if hud_pos not in ['center', 'corner']:
    raise Exception('HUD position can only be "center" or "corner"')
    
game_version = input(f'Enter the game version for which you would like to generate the patch (must be one of {supported_versions}): ')
if game_version not in supported_versions:
    raise Exception('Game version is not supported')
    
working_dir = os.path.dirname(sys.argv[0])
zsdic_path = os.path.join(working_dir, 'zs.zsdic')
temp_dir = os.path.join(working_dir, 'temp')
mod_dir = os.path.join(working_dir, 'TOTK-Ultrawide')
exefs_dir = os.path.join(mod_dir, 'exefs')
LayouArchive_dir = os.path.join(mod_dir, 'romfs', 'UI', 'LayoutArchive')

print('Clearing workspace')
shutil.rmtree(temp_dir, ignore_errors=True)
shutil.rmtree(mod_dir, ignore_errors=True)

print('Creating folders')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(mod_dir, exist_ok=True)
os.makedirs(exefs_dir, exist_ok=True)
os.makedirs(LayouArchive_dir, exist_ok=True)

print('Generating pchtxt files')
create_pchtxt(exefs_dir, aspect_ratio)

if game_version in ['1.0.0', 'all']:
    filename = 'Common.Product.100.Nin_NX_NVN'
    print(f'Creating patch for {filename}')
    patch_zs(filename)
    
if game_version in ['1.1.0', '1.1.1', '1.1.2', '1.2.0', 'all']:
    filename = 'Common.Product.110.Nin_NX_NVN'
    print(f'Creating patch for {filename}')
    patch_zs(filename)
    
print('Deleting temp folder')
shutil.rmtree(temp_dir, ignore_errors=True)

print('Done!')
