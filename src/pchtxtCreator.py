import sys
import math
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('output_dir')
parser.add_argument('aspect_ratio', type=float)
args = parser.parse_args()

ratio = args.aspect_ratio
scaling_factor = ratio / (16/9)

def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

def val2asm(x):
    """
    Converts the instruction 'fmov s0, #x' to hex
    """
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a = 128 + a
    a = 2*a + 1
    h = hex(a).lstrip('0x').rjust(2,'0').upper()
    s = '00' + h[1] + '02' + h[0] + '1E' 
    return s

def float2hex(f):
    """
    Converts float values into hex, strips the 0x prefix and prepends zeroes to
    always have length 8
    """
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()


versions = ['1.0.0', '1.1.0', '1.1.1', '1.1.2']
data = [['082CE09B06E33A123CB1E2770F5F9147709033DB', '0377AC54', '01968C2C'],
        ['D5AD6AC71EF53E3E52417C1B81DBC9B4142AA3B3', '0381B344', '019C2260'],
        ['168DD518D925C7A327677286E72FEDA833314919', '0382413C', '019C013C'],
        ['9A10ED9435C06733DA597D8094D9000AB5D3EE60', '03813D0C', '019B5480']]

for ii in range(len(versions)):
    with open(args.output_dir + '\\' + f'main-{versions[ii]}.pchtxt', 'w') as f:
        f.write(f'@nsobid-{data[ii][0]}\n\n')
        f.write('@flag print_values\n')
        f.write('@flag offset_shift 0x100\n\n')
        f.write('@enabled\n')
        f.write(f'{data[ii][1]} {float2hex(ratio)}\n')
        f.write(f'{data[ii][2]} {val2asm(ratio)}\n')
        f.write('@stop\n')

        if versions[ii] == '1.1.2':
            f.write('\n')
            content = f"""
                // Scaling factor
                @enabled
                036c9b00 {float2hex(scaling_factor)}
                @stop
                
                // NPC Marker Fix
                @enabled
                01ae0440 90A56F94 // bl #0x1BE9640
                036c9a80 A01B40BD // ldr s0, [x29,#0x18]
                036c9a84 E0C31FF8 // stur x0, [sp, #-4]
                036c9a88 00000090 // adrp x0, #0
                036c9a8c 01004BBD // ldr s1, [x0, #0xb00]
                036c9a90 E0C35FF8 // ldur x0, [sp, #-4]
                036c9a94 0008211E // fmul s0, s0, s1
                036c9a98 A11F40BD // ldr s1, [x29, #0x1c]
                036c9a9c C0035FD6 // ret
                @stop
                
                // NPC Text Balloon Fix
                @enabled
                01ae4c24 9F936F94 // bl #0x1BE4E7C
                036c9aa0 802240BD // ldr s0, [x20, #0x20]
                036c9aa4 E0C31FF8 // stur x0, [sp, #-4]
                036c9aa8 00000090 // adrp x0, #0
                036c9aac 01004BBD // ldr s1, [x0, #0xb00]
                036c9ab0 E0C35FF8 // ldur x0, [sp, #-4]
                036c9ab4 0008211E // fmul s0, s0, s1
                036c9ab8 812640BD // ldr s1, [x20, #0x24]
                036c9abc C0035FD6 // ret
                @stop
                
                // Item Description Fix
                @enabled
                01adf838 A2A86F94 // bl #0x1BEA288
                036c9ac0 E10B40BD // ldr s1, [sp, #0x8]
                036c9ac4 E0C31FF8 // stur x0, [sp, #-4]
                036c9ac8 00000090 // adrp x0, #0
                036c9acc 00004BBD // ldr s0, [x0, #0xb00]
                036c9ad0 E0C35FF8 // ldur x0, [sp, #-4]
                036c9ad4 2108201E // fmul s1, s1, s0
                036c9ad8 E00F40BD // ldr s0, [sp, #0xc]
                036c9adc C0035FD6 // ret
                @stop
                
                // Enemy Info Fix
                @enabled
                012c2418 B21D9094 // bl #0x24076C8
                036c9ae0 000140BD // ldr s0, [x8]
                036c9ae4 E0C31FF8 // stur x0, [sp, #-4]
                036c9ae8 00000090 // adrp x0, #0
                036c9aec 01004BBD // ldr s1, [x0, #0xb00]
                036c9af0 E0C35FF8 // ldur x0, [sp, #-4]
                036c9af4 0008211E // fmul s0, s0, s1
                036c9af8 010540BD // ldr s1, [x8, #0x4]
                036c9afc C0035FD6 // ret
                @stop
                """
            content_trimmed = trim(content)
            f.write(content_trimmed)
            f.write('\n')
            
        f.write('\n@fruithapje21')
                                    