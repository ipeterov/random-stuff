import random, colorsys
from PIL import Image, ImageDraw

image = Image.open("input.jpg") #Открываем изображение.
image = image.convert("HSL")
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

for i in range(width):
    for j in range(height):
        hls = colorsys.rgb_to_hls(pix[i, j])
        draw.point((i, j), (S, S, S))
image.save("gray.jpg", "JPEG")
