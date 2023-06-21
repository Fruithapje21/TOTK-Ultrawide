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
        
        if versions[ii] == '1.0.0':
            f.write('\n')
            content = f"""
                // Scaling factor
                @enabled
                03774580 {float2hex(scaling_factor)}
                @stop

                // NPC Marker Fix
                @enabled
                01a8f18c DD947394 // bl #0x1CE5374
                03774500 A01B40BD // ldr s0, [x29,#0x18]
                03774504 E0C31FF8 // stur x0, [sp, #-4]
                03774508 00000090 // adrp x0, #0
                0377450c 018045BD // ldr s1, [x0, #0x580]
                03774510 E0C35FF8 // ldur x0, [sp, #-4]
                03774514 0008211E // fmul s0, s0, s1
                03774518 A11F40BD // ldr s1, [x29, #0x1c]
                0377451c C0035FD6 // ret
                @stop

                // NPC Text Balloon Fix
                @enabled
                01a93954 F3827394 // bl #0x1CE0BCC
                03774520 802240BD // ldr s0, [x20, #0x20]
                03774524 E0C31FF8 // stur x0, [sp, #-4]
                03774528 00000090 // adrp x0, #0
                0377452c 018045BD // ldr s1, [x0, #0x580]
                03774530 E0C35FF8 // ldur x0, [sp, #-4]
                03774534 0008211E // fmul s0, s0, s1
                03774538 812640BD // ldr s1, [x20, #0x24]
                0377453c C0035FD6 // ret
                @stop

                // Item Description Fix
                @enabled
                01a8e69c A9977394 // bl #0x1CE5EA4
                03774540 E00B40BD // ldr s0, [sp, #0x8]
                03774544 E0C31FF8 // stur x0, [sp, #-4]
                03774548 00000090 // adrp x0, #0
                0377454c 018045BD // ldr s1, [x0, #0x580]
                03774550 E0C35FF8 // ldur x0, [sp, #-4]
                03774554 0008211E // fmul s0, s0, s1
                03774558 E10F40BD // ldr s1, [sp, #0xc]
                0377455c C0035FD6 // ret
                @stop

                // Enemy Info Fix
                @enabled
                012ade68 BE199394 // bl #0x24C66F8
                03774560 000140BD // ldr s0, [x8]
                03774564 E0C31FF8 // stur x0, [sp, #-4]
                03774568 00000090 // adrp x0, #0
                0377456c 018045BD // ldr s1, [x0, #0x580]
                03774570 E0C35FF8 // ldur x0, [sp, #-4]
                03774574 0008211E // fmul s0, s0, s1
                03774578 010540BD // ldr s1, [x8, #0x4]
                0377457c C0035FD6 // ret
                @stop
                """
            content_trimmed = trim(content)
            f.write(content_trimmed)
            f.write('\n')
            
        if versions[ii] == '1.1.0':
            f.write('\n')
            content = f"""
                // Scaling factor
                @enabled
                036d1100 {float2hex(scaling_factor)}
                @stop

                // NPC Marker Fix
                @enabled
                01aec24c 8D936F94 // bl #0x1BE4E34
                036d1080 A01B40BD // ldr s0, [x29,#0x18]
                036d1084 E0C31FF8 // stur x0, [sp, #-4]
                036d1088 00000090 // adrp x0, #0
                036d108c 010041BD // ldr s1, [x0, #0x100]
                036d1090 E0C35FF8 // ldur x0, [sp, #-4]
                036d1094 0008211E // fmul s0, s0, s1
                036d1098 A11F40BD // ldr s1, [x29, #0x1c]
                036d109c C0035FD6 // ret
                @stop

                // NPC Text Balloon Fix
                @enabled
                01af0a2c 9D816F94 // bl #0x1BE0674
                036d10a0 802240BD // ldr s0, [x20, #0x20]
                036d10a4 E0C31FF8 // stur x0, [sp, #-4]
                036d10a8 00000090 // adrp x0, #0
                036d10ac 010041BD // ldr s1, [x0, #0x100]
                036d10b0 E0C35FF8 // ldur x0, [sp, #-4]
                036d10b4 0008211E // fmul s0, s0, s1
                036d10b8 812640BD // ldr s1, [x20, #0x24]
                036d10bc C0035FD6 // ret
                @stop

                // Item Description Fix
                @enabled
                01aeb644 9F966F94 // bl #0x1BE5A7C
                036d10c0 E10B40BD // ldr s1, [sp, #0x8]
                036d10c4 E0C31FF8 // stur x0, [sp, #-4]
                036d10c8 00000090 // adrp x0, #0
                036d10cc 000041BD // ldr s0, [x0, #0x100]
                036d10d0 E0C35FF8 // ldur x0, [sp, #-4]
                036d10d4 2108201E // fmul s1, s1, s0
                036d10d8 E00F40BD // ldr s0, [sp, #0xc]
                036d10dc C0035FD6 // ret
                @stop

                // Enemy Info Fix
                @enabled
                012e5a18 B2AD8F94 // bl #0x23EB6C8
                036d10e0 000140BD // ldr s0, [x8]
                036d10e4 E0C31FF8 // stur x0, [sp, #-4]
                036d10e8 00000090 // adrp x0, #0
                036d10ec 010041BD // ldr s1, [x0, #0x100]
                036d10f0 E0C35FF8 // ldur x0, [sp, #-4]
                036d10f4 0008211E // fmul s0, s0, s1
                036d10f8 010540BD // ldr s1, [x8, #0x4]
                036d10fc C0035FD6 // ret
                @stop
                """
            content_trimmed = trim(content)
            f.write(content_trimmed)
            f.write('\n')        
            
        if versions[ii] == '1.1.1':
            f.write('\n')
            content = f"""
                // Scaling factor
                @enabled
                036d9f60 {float2hex(scaling_factor)}
                @stop

                // NPC Marker Fix
                @enabled
                01ae9b14 F3C06F94 // bl #0x1BF03CC
                036d9ee0 A01B40BD // ldr s0, [x29,#0x18]
                036d9ee4 E0C31FF8 // stur x0, [sp, #-4]
                036d9ee8 00000090 // adrp x0, #0
                036d9eec 01604FBD // ldr s1, [x0, #0xf60]
                036d9ef0 E0C35FF8 // ldur x0, [sp, #-4]
                036d9ef4 0008211E // fmul s0, s0, s1
                036d9ef8 A11F40BD // ldr s1, [x29, #0x1c]
                036d9efc C0035FD6 // ret
                @stop

                // NPC Text Balloon Fix
                @enabled
                01aee304 FFAE6F94 // bl #0x1BEBBFC
                036d9f00 802240BD // ldr s0, [x20, #0x20]
                036d9f04 E0C31FF8 // stur x0, [sp, #-4]
                036d9f08 00000090 // adrp x0, #0
                036d9f0c 01604FBD // ldr s1, [x0, #0xf60]
                036d9f10 E0C35FF8 // ldur x0, [sp, #-4]
                036d9f14 0008211E // fmul s0, s0, s1
                036d9f18 812640BD // ldr s1, [x20, #0x24]
                036d9f1c C0035FD6 // ret
                @stop

                // Item Description Fix
                @enabled
                01ae8f0c 05C46F94 // bl #0x1BF1014
                036d9f20 E10B40BD // ldr s1, [sp, #0x8]
                036d9f24 E0C31FF8 // stur x0, [sp, #-4]
                036d9f28 00000090 // adrp x0, #0
                036d9f2c 00604FBD // ldr s0, [x0, #0xf60]
                036d9f30 E0C35FF8 // ldur x0, [sp, #-4]
                036d9f34 2108201E // fmul s1, s1, s0
                036d9f38 E00F40BD // ldr s0, [sp, #0xc]
                036d9f3c C0035FD6 // ret
                @stop

                // Enemy Info Fix
                @enabled
                012e3614 4BDA8F94 // bl #0x23F692C
                036d9f40 000140BD // ldr s0, [x8]
                036d9f44 E0C31FF8 // stur x0, [sp, #-4]
                036d9f48 00000090 // adrp x0, #0
                036d9f4c 01604FBD // ldr s1, [x0, #0xf60]
                036d9f50 E0C35FF8 // ldur x0, [sp, #-4]
                036d9f54 0008211E // fmul s0, s0, s1
                036d9f58 010540BD // ldr s1, [x8, #0x4]
                036d9f5c C0035FD6 // ret
                @stop
                """
            content_trimmed = trim(content)
            f.write(content_trimmed)
            f.write('\n')        

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
                                    