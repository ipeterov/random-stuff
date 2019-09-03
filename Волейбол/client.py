from random import *
from math import *
from tkinter import *
import time

class circle:
    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.xs = 0
        self.ys = 0
        self.xa = 0
        self.ya = 0

class line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

def main(quantity, radius, speed, width = 700, height = 700):

    def update():
        player1.x += player1.xs
        player1.y += player1.ys
        
    def key_press(e):
        if e.char == 'w':
            player1.y -= speed
        elif e.char == 's':
            player1.y += speed
        elif e.char == 'd':
            player1.x += speed
        elif e.char == 'a':
            player1.x -= speed
                
    def frame():
        update()
        canvas.coords(player1.canvasobject, player1.x - radius, player1.y - radius, player1.x + radius, player1.y + radius)
        root.after(1, frame)

    # Initialize canvas
    root = Tk()
    canvas = Canvas(root, width = width, height = height)
    canvas.bind('<Key>', key_press)
    canvas.pack()
    canvas.focus_set()
       
    player1 = circle(10, 100, 100)
    player1.canvasobject = canvas.create_oval(player1.x - radius, player1.y - radius, player1.x + radius, player1.y + radius, fill = 'black')
    
    # Main loop
    frame()
    root.mainloop()


main(quantity = 300, radius = 5, speed = 3, width = 700, height = 700)
