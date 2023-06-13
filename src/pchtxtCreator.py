import math
import struct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('output_dir')
parser.add_argument('aspect_ratio', type=float)
args = parser.parse_args()

ratio = args.aspect_ratio

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
