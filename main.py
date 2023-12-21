import os
import sys
import shutil
from romfs_script import patch_romfs
from exefs_script import create_pchtxt
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

supported_versions = ['1.0.0', '1.1.0', '1.1.1', '1.1.2', '1.2.0', '1.2.1']
layout_filenames = ['Common.Product.100.Nin_NX_NVN', 'Common.Product.110.Nin_NX_NVN']
working_dir = os.path.dirname(sys.argv[0])
zsdic_path = os.path.join(working_dir, 'zs.zsdic')
temp_dir = os.path.join(working_dir, 'temp')
mod_dir = os.path.join(working_dir, 'TOTK-Ultrawide')
exefs_dir = os.path.join(mod_dir, 'exefs') 
LayouArchive_dir = os.path.join(mod_dir, 'romfs', 'UI', 'LayoutArchive')
exefs_template_dir = os.path.join(working_dir, 'exefs_template')

aspect_ratio = float(eval(input('Enter your aspect ratio (e.g. 21.5/9, 3440/1440 or 2.38889): ')))

if aspect_ratio < 1/8 or aspect_ratio > 31:
    raise Exception('Please enter a valid aspect ratio')

if aspect_ratio > 16/9:
    hud_pos = input('Where would you like the HUD (center or corner): ')
    if hud_pos not in ['center', 'corner']:
        raise Exception('HUD position can only be "center" or "corner"')
    template_dir = os.path.join(exefs_template_dir, 'super169')
else:
    hud_pos = 'corner'
    template_dir = os.path.join(exefs_template_dir, 'sub169')
    
print('Clearing workspace')
shutil.rmtree(temp_dir, ignore_errors=True)
shutil.rmtree(mod_dir, ignore_errors=True)

print('Creating folders')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(mod_dir, exist_ok=True)
os.makedirs(exefs_dir, exist_ok=True)
os.makedirs(LayouArchive_dir, exist_ok=True)

print('Generating pchtxt files')
create_pchtxt(template_dir, exefs_dir, aspect_ratio, supported_versions)

for lyt in layout_filenames:
    print(f'Creating patch for {lyt}')
    patch_zs(lyt)
    
print('Deleting temp folder')
shutil.rmtree(temp_dir, ignore_errors=True)

print('Done!')
