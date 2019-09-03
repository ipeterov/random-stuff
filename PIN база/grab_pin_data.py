import random, pickle
from PIL import Image, ImageDraw
image = Image.open("grid.png") #Открываем изображение.
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

datatable = []

for x in range(100):
    for y in range(100):
        x = str(x)
        y = str(y)
        if len(x) == 1:
            x = '0' + x
        if len(y) == 1:
            y = '0' + y
        datatable.append([x+y, pix[int(x), int(y)]])

datatable.sort(key=lambda x: x[1])
datatable.reverse()

log = open('pin_base.txt', 'w')

for item in datatable:
    log.write(str(item[0]))
    log.write(' ')
    log.write(str(item[1]))
    log.write('\n')
