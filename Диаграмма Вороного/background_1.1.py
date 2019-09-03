from random import *
from tkinter import *
from math import *
from pickle import *
import time

dotcount = 50
width = 400
height = 400
antialiasing = 1

def pixel(image, pos, color):
    """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
    r,g,b = color
    x,y = pos
    image.put("#%02x%02x%02x" % (r,g,b), (x, y))

def circle(pixel_q, dot_q, probability = 0.9):
    import math
    coeff = pixel_q / dot_q
    circle_area = math.log(probability, 1 - coeff)
    radius = round(sqrt(x / pi), 0)
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if sqrt(x^2 + y^2) < radius:
                dots.append((x,,y))
    return dots

circle_dots = circle(width*height)

dots = []
for i in range(dotcount):
    x = randint(0, width * antialiasing)
    y = randint(0, height * antialiasing)
    color = (randint(0,255), randint(0,255), randint(0,255))
    dots.append({'name' : i, 'pos' : (x, y), 'color' : color})


aabitmap = []
for x in range(width*antialiasing):
    aabitmap.append([])
    #print('Calc: '+ str(round(x/(width*antialiasing)*100, 1)) + '%')
    for y in range(height*antialiasing):
        min_dist = width*antialiasing + height*antialiasing
        for dot in dots:
            dist = sqrt(abs(dot['pos'][0] - x)**2 + abs(dot['pos'][1] - y)**2)
            if dist < min_dist:
                min_dist = dist
                color = dot['color']
                dot['lastused'] = 1
        aabitmap[x].append({'color' : color})
print('comp: ' + str(t_s))
print('all: ' + str(t_1_s))

if antialiasing != 1:
    bitmap = []
    for x in range(width):
        bitmap.append([])
        print('SSAA: ' + str(round(x/width*100, 1)) + '%')
        for y in range(height):
            r = 0
            g = 0
            b = 0
            for aax in range(antialiasing):
                for aay in range(antialiasing):
                        r += aabitmap[x*antialiasing + aax][y*antialiasing + aay]['color'][0]
                        g += aabitmap[x*antialiasing + aax][y*antialiasing + aay]['color'][1]
                        b += aabitmap[x*antialiasing + aax][y*antialiasing + aay]['color'][2]
            r = int(round(r / antialiasing**2, 0))
            g = int(round(g / antialiasing**2, 0))
            b = int(round(b / antialiasing**2, 0))
            bitmap[x].append({'color' : (r, g, b)})
else:
    bitmap = aabitmap

root = Tk()
image = PhotoImage(width = width, height = height)
for x in range(width):
    for y in range(height):
        pixel(image, (x,y), bitmap[x][y]['color'])
image.write('wallpaper.png', format='png')

#canv = Canvas(root, width = width, height = height)
#canv.create_image(0, 0, image = image, anchor=NW)
#canv.pack()
#root.mainloop()
