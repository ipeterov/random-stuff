import os
from PIL import Image, ImageDraw
from bitfuncs import tobits, frombits, setbit, getbit

class MessageHider:
    def __init__(self):
        self.control_byte = [1,1,1,1,1,1,1,1]

    def encode(self, message, orig_filename, result_filename=None):

        if not result_filename:
            result_filename = 'result.bmp'

        image = Image.open(orig_filename)
        image.convert('RGB')
        pix = image.load()

        message_bits = tobits(message)
        message_bits.extend(self.control_byte)

        done = False

        for bit_i in range(7,-1,-1):
            for y in range(image.size[1]):
                for x in range(image.size[0]):
                    try:
                        bits = []
                        for _ in range(3):
                            bits.append(message_bits.pop(0))
                    except IndexError:
                        # Message remainder is empty, message is encoded
                        done = True

                    for i, bit in enumerate(bits):
                        pix[x, y] = pix[x, y][:i] + (setbit(pix[x, y][i], bit, bit_i), ) + pix[x, y][i+1:]

                    if done:
                        image.save(result_filename)
                        return

    def decode(self, filename=None):

        if not filename:
            filename = 'result.bmp'

        image = Image.open(filename)
        image.convert('RGB')
        pix = image.load()
        message_bits = []

        for bit_i in range(7,-1,-1):
            for y in range(image.size[1]):
                for x in range(image.size[0]):
                    for color in range(3):

                        message_bits.append(getbit(pix[x,y][color], bit_i))

                        if len(message_bits) % 8 == 0 and len(message_bits) >= 8 and message_bits[-8:] == self.control_byte:
                            # Message is collected
                            message = frombits(message_bits[:-8])
                            return message


encoder = MessageHider()

mode = input('Mode: ')

if mode == 'encode':
    message = input('Message: ')
    orig_filename = input('Original filename: ')
    result_filename = input('Result filename [result.bmp]: ')
    encoder.encode(message, orig_filename, result_filename)

elif mode == 'decode':
    filename = input('Filename [result.bmp]: ')
    message = encoder.decode(filename)
    print(message)
