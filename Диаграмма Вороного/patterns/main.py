from random import *
from tkinter import *
from math import *
from pickle import *
from vectorisation import alloc_lines

dotcount = 30
width = 100
height = 100

patterns = load(open('patterns', 'rb'))

def pixel(image, pos, color):
    """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
    r,g,b = color
    x,y = pos
    image.put("#%02x%02x%02x" % (r,g,b), (x, y))

dot_bitmap = []
for x in range(width):
    dot_bitmap.append([])
    for y in range(height):
        dot_bitmap[x].append(0)

for i in range(dotcount):
    x = randint(0, width-1)
    y = randint(0, height-1)
    color = (randint(0,255), randint(0,255), randint(0,255))
    dot_bitmap[x][y] = color


bitmap = []
for x in range(width):
    bitmap.append([])
    for y in range(height):
        for dot in patterns:
            try:
                if dot_bitmap[x+dot[0]][y+dot[1]] != 0:
                    bitmap[x].append(dot_bitmap[x+dot[0]][y+dot[1]])
                    break
            except:
                pass

bitmap = alloc_lines(bitmap)

root = Tk()
image = PhotoImage(width = width, height = height)
for x in range(1, width):
    for y in range(height):
        pixel(image, (x,y), bitmap[x][y])
image.write('wallpaper.png', format='png')

#root = Tk()
#image = PhotoImage(width = 50, height = 50)
#for x in range(1, 50):
    #for y in range(50):
        #pixel(image, (x,y), (0,0,0))
#image.write('test.png', format='png')

