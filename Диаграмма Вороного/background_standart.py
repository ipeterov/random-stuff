from random import *
from tkinter import *
from math import *
from pickle import *
from vectorisation import *

dotcount = 20
width = 500
height = 500

def pixel(image, pos, color):
    """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
    r,g,b = color
    x,y = pos
    image.put("#%02x%02x%02x" % (r,g,b), (x, y))

dots = []
for i in range(dotcount):
    x = randint(0, width)
    y = randint(0, height)
    color = (randint(0,255), randint(0,255), randint(0,255))
    dots.append({'name' : i, 'pos' : (x, y), 'color' : color})


bitmap = []
for x in range(width):
    print(x / width)
    bitmap.append([])
    for y in range(height):
        min_dist = width + height
        for dot in dots:
            dist = sqrt(abs(dot['pos'][0] - x)**2 + abs(dot['pos'][1] - y)**2)
            if dist < min_dist:
                min_dist = dist
                color = dot['color']
                dot['lastused'] = 1
        bitmap[x].append(color)

bitmap = alloc_lines(bitmap, monochrome =1)


root = Tk()
image = PhotoImage(width = width, height = height)
for x in range(width):
    for y in range(height):
        if not (y == height - 1 and x == width - 1):
            pixel(image, (x,y), bitmap[x][y])
image.write('wallpaper.png', format='png')

print(make_line_objects(bitmap))
