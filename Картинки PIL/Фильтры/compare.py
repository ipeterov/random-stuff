import random
from PIL import Image, ImageDraw

img1 = Image.open('one.jpg')
img2 = Image.open('two.jpg')

draw1 = ImageDraw.Draw(img1)
draw1 = ImageDraw.Draw(img2)
#width = image.size[0]
#height = image.size[1]
pix1 = img1.load()
pix2 = img2.load()


for i in range(img1.size[0]):
    for j in range(img1.size[1]):
        a = pix1[i, j][0]
        b = pix1[i, j][1]
        c = pix1[i, j][2]
        S = (a + b + c) // 3
        draw1.point((i, j), (S, S, S))

for i in range(img2.size[0]):
    for j in range(img2.size[1]):
        a = pix2[i, j][0]
        b = pix2[i, j][1]
        c = pix2[i, j][2]
        S = (a + b + c) // 3
        draw2.point((i, j), (S, S, S))

for i in range(min(img1.size[0], img2.size[0])):
    for j in range(min(img1.size[1], img2.size[1])):
        S = abs(pix1[i, j][0] - pix2[i, j][0])
        draw1.point((i, j), (S, S, S))

img1.crop(0,0,min(img1.size[0], img2.size[0]),min(img1.size[1], img2.size[1])).save('result.bmp', 'BMP')
