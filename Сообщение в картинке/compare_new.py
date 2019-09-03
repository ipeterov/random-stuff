import random
from PIL import Image, ImageDraw

img1 = Image.open('one.jpg').convert('YCbCr')
img2 = Image.open('two.jpg').convert('YCbCr')

width = min(img1.size[0], img2.size[0])
height = min(img1.size[1], img2.size[1])

result = Image.new('RGB', (width, height))

draw_result = ImageDraw.Draw(result)

pix1 = img1.load()
pix2 = img2.load()

coeff = 0

for i in range(width):
    for j in range(height):
        S = abs(pix1[i, j][0] - pix2[i, j][0])
        if S > coeff: coeff = S
        draw_result.point((i, j), (S, S, S))

print(coeff)
result.save('result.bmp', 'BMP')
