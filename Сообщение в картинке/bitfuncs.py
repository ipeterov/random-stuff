def tobits(string):
    result = []
    for char in string:
        bits = bin(ord(char))[2:]
        bits = ('0'*8)[len(bits):] + bits
        result.extend([int(bit) for bit in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def setbit(color, newbit, i):
    bits = bin(color)[2:]
    bits = ('0'*8)[len(bits):] + bits
    bits = bits[:i] + str(newbit) + bits[i+1:]
    return int(bits, 2)

def getbit(color, i):
    bits = bin(color)[2:]
    bits = ('0'*8)[len(bits):] + bits
    return int(bits[i])
