import os
from conversion import val2asm, float2hex

def create_pchtxt(template_dir, out_dir, aspect_ratio, versions):

    if aspect_ratio >= 16/9:
        scaling_factor = aspect_ratio / (16/9)
    else:
        scaling_factor = (16/9) / aspect_ratio
        
    hexvals = {'hex1': float2hex(aspect_ratio),
               'hex2': val2asm(aspect_ratio),
               'hex3': val2asm(aspect_ratio),
               'hex4': float2hex(scaling_factor)}
    
    for version in versions:
        
        template_path = os.path.join(template_dir, f'main-{version}.pchtxt')
        with open(template_path, 'r') as f:
            content = f.read()
        
        content_patched = content.format(**hexvals)
        
        out_path = os.path.join(out_dir, f'main-{version}.pchtxt')
        with open(out_path, 'w') as f:
            f.write(content_patched)
      