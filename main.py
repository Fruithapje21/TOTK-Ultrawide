import os
import sys
import shutil
from romfs_script import patch_romfs
from exefs_srcipt import create_pchtxt
from romfs_script_1610 import patch_romfs_1610
from exefs_srcipt_1610 import create_pchtxt_1610
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
    if aspect_ratio == 16/10:
        patch_romfs_1610(extracted_blarc_dir)
    else:
        patch_romfs(extracted_blarc_dir, aspect_ratio, hud_pos)
    print('Repacking blarc')
    repack_blarc(extracted_blarc_dir, blarc_path)
    print('Compressing zs')
    compress_zs(blarc_path, patched_zs_path, zsdic_path)
    
sys.excepthook = myexcepthook

supported_versions = ['1.0.0', '1.1.0', '1.1.1', '1.1.2', '1.2.0', 'all']
layout_filenames = ['Common.Product.100.Nin_NX_NVN', 'Common.Product.110.Nin_NX_NVN']

working_dir = os.path.dirname(sys.argv[0])
zsdic_path = os.path.join(working_dir, 'zs.zsdic')
temp_dir = os.path.join(working_dir, 'temp')
mod_dir = os.path.join(working_dir, 'TOTK-Ultrawide')
exefs_dir = os.path.join(mod_dir, 'exefs')
LayouArchive_dir = os.path.join(mod_dir, 'romfs', 'UI', 'LayoutArchive')

aspect_ratio = float(eval(input('Enter your aspect ratio (e.g. 21.5/9, 3440/1440 or 2.38889): ')))

if aspect_ratio < 16/9 and aspect_ratio != 16/10:
    raise Exception('Aspect ratios smaller than 16/9 are not supported with the exception of 16/10')

if aspect_ratio != 16/10:
    hud_pos = input('Where would you like the HUD (center or corner): ')
    if hud_pos not in ['center', 'corner']:
        raise Exception('HUD position can only be "center" or "corner"')
    
print('Clearing workspace')
shutil.rmtree(temp_dir, ignore_errors=True)
shutil.rmtree(mod_dir, ignore_errors=True)

print('Creating folders')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(mod_dir, exist_ok=True)
os.makedirs(exefs_dir, exist_ok=True)
os.makedirs(LayouArchive_dir, exist_ok=True)

print('Generating pchtxt files')
if aspect_ratio == 16/10:
    create_pchtxt_1610(exefs_dir)
else:
    create_pchtxt(exefs_dir, aspect_ratio)

for lyt in layout_filenames:
    print(f'Creating patch for {lyt}')
    patch_zs(lyt)
    
print('Deleting temp folder')
shutil.rmtree(temp_dir, ignore_errors=True)

print('Done!')
