from tkinter import *
from random import *
table = {0.05:-0.6, 0.1:-0.3, 0.2:-0.1, 0.3:0, 0.05:0.6, 0.1:0.3, 0.2:0.1}

class animate():
    def __init__(self):
        self.canvaswidth = 900
        self.canvasheight = 900
        self.dotcount = 200
        self.root = Tk()
        self.canvas = Canvas(self.root, width = self.canvaswidth, height = self.canvasheight)
        self.dots = []
        for i in range(self.dotcount):
            x = randint(0, self.canvaswidth)
            y = randint(0, self.canvasheight)
            self.dots.append({'object' : self.canvas.create_rectangle(x, y, x+1, y+1), 'xa': 0, 'ya' : 0})
        self.canvas.pack()
        self.frame()
        self.root.mainloop()

    def frame(self):
        for dot in self.dots:
            dot['xa'] += randint(-1,1)
            dot['ya'] += randint(-1,1)
            if abs(dot['xa']) > 5: dot['xa'] = randint(-2,2)
            if abs(dot['ya']) > 5: dot['ya'] = randint(-2,2)
            coords = self.canvas.coords(dot['object'])
            if coords[0] < 0 or coords[2] > self.canvaswidth:
                dot['xa'] *= -1
            if coords[1] < 0 or coords[3] > self.canvasheight:
                dot['ya'] *= -1
            self.canvas.move(dot['object'], int(round(dot['xa'])), int(round(dot['ya'])))
        self.root.after(17, self.frame)


animate()
