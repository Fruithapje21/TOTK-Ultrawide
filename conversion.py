import math
import struct

def val2asm(x):
    """
    Converts the instruction 'fmov s0, #x' to hex
    """
    p = math.floor(math.log(x, 2))
    a = round(16*(p-2) + x / 2**(p-4))
    if a<0: a += 128
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