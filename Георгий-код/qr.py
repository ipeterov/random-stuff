from math import *
from tkinter import *

code_length = 50
width = 800
height = 800

def converse(coords):
    points = []
    distortions = []
    max_horisontal_len = max(sqrt((coords[1][0] - coords[0][0])**2 + (coords[1][1] - coords[0][1])**2), sqrt((coords[3][0] - coords[2][0])**2 + (coords[3][1] - coords[2][1])**2))

    for i in range(code_length):
        left_point = (coords[0][0] + (coords[3][0] - coords[0][0]) / code_length * i, coords[0][1] + (coords[3][1] - coords[0][1]) / code_length * i)
        right_point = (coords[1][0] + (coords[2][0] - coords[1][0]) / code_length * i, coords[1][1] + (coords[2][1] - coords[1][1]) / code_length * i)
        current_len = sqrt((right_point[0] - left_point[0])**2 + (right_point[1] - left_point[1])**2)
        distortion = current_len / max_horisontal_len
        distortions.append(distortion)
        for j in range(code_length):
            x = left_point[0] + (right_point[0] - left_point[0]) / code_length * j
            y = left_point[1] + (right_point[1] - left_point[1]) / code_length * j
            points.append({'coords' : (x, y), 'color' : 'red'})
            y *= distortion
            y += 6

            points.append({'coords' : (x, y), 'color' : 'blue'})

    return points

def draw_points(points):
    root = Tk()
    canv = Canvas(root, width = width, height = height)
    for point in points:
        canv.create_oval(point['coords']*2, outline = point['color'])
    canv.pack()
    root.mainloop()

def draw_graph(points, scale = 40):
    line_coords = []
    root = Tk()
    canv = Canvas(root, width = len(points)*scale, height = (max(points) - min(points)) * scale * 10)
    for i in range(len(points)):
        point = i * scale, points[i] * scale
        line_coords.append((point[0], point[1]))
    canv.create_line(line_coords, width = 10)
    canv.pack()
    root.mainloop()

def save_bitmap(points):
    def pixel(pos, color):
        """Place pixel at pos=(x,y) on image, with color=(r,g,b)."""
        r,g,b = color
        x,y = pos
        image.put("#%02x%02x%02x" % (r,g,b), (x, y))
    root = Tk()
    image = PhotoImage(width = width, height = height)
    for point in points:
        for i in range(-2, 2):
            for j in range(-2, 2):
                pixel((point['coords'][0] + j,point['coords'][1] + i), (0,0,0))
    image.write('dotmap.png', format='png')

a = converse([(270,200) , (530,200), (600, 600), (200, 600)]) #[(1067,974) , (1986,980), (2174, 1476), (872, 1465)]

#save_bitmap(a)
draw_points(a)
