from tkinter import *
from random import *
from math import *

class body:
    def __init__(self, x=0, y=0, xs=0, ys=0, density = 1, radius = 25):
        self.mass = pi * radius**2 * density
        self.density = density
        self.radius = radius
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys

    def dist(self, otherbody):
        return ((self.x - otherbody.x)**2 + (self.y - otherbody.y)**2)**0.5

    def gravity(self, otherbody):
        distance = self.dist(otherbody)
        a = self.mass / (distance**2 * otherbody.mass)
        otherbody.xs += (self.x-otherbody.x) / distance * a
        otherbody.ys += (self.y-otherbody.y) / distance * a

    def collision(self, otherbody):
        distance = self.dist(otherbody)
        if distance < (self.radius + otherbody.radius):
            otherbody.xs = -otherbody.xs + 2*(otherbody.mass*otherbody.xs + self.mass*self.xs) / (self.mass + otherbody.mass)
            otherbody.ys = -otherbody.ys + 2*(otherbody.mass*otherbody.ys + self.mass*self.ys) / (self.mass + otherbody.mass)

    def tick(self):
        self.x += self.xs
        self.y += self.ys

class animate():
    def __init__(self):
        self.canvaswidth = 900
        self.canvasheight = 900
        self.bodys = []
        #~ for i in range(5):
            #~ angle = uniform(0, 2*pi)
            #~ radius = randint(1,20)
            #~ speed = uniform(0.5, 2)
            #~ spcoeff = 0.1

            #~ xs = sin(angle) * speed * spcoeff
            #~ ys = cos(angle) * speed * spcoeff
            #~ self.bodys.append(body(x = randint(radius, 900 - radius), y = randint(radius, 900 - radius), radius = radius, xs = xs, ys = ys))
        #~ self.bodys.append(body(x = 100, y = 450, radius = 3, ys = 0))
        #~ self.bodys.append(body(x = 100, y = 450, radius = 10, ys = 0.54))
        self.bodys.append(body(x = 800, y = 450, radius = 10, ys = -0.54))
        self.bodys.append(body(x = 450, y = 450, radius = 100))
        self.root = Tk()
        self.canvas = Canvas(self.root, width = self.canvaswidth, height = self.canvasheight)
        self.canvas.pack()
        for body1 in self.bodys:
            body1.canvasobject = self.canvas.create_oval(body1.x-body1.radius, body1.y-body1.radius, body1.x+body1.radius, body1.y+body1.radius, fill = 'black')

        self.frame()
        self.root.mainloop()

    def frame(self):
        for body1 in self.bodys:
            self.canvas.coords(body1.canvasobject, body1.x-body1.radius, body1.y-body1.radius, body1.x+body1.radius, body1.y+body1.radius)
            body1.tick()
        #print(self.bodys[0].xs, self.bodys[0].ys)
        #print(self.bodys[0].dist(self.bodys[1]))
        for body1 in self.bodys:
            for body2 in self.bodys:
                if not body1 is body2:
                    body1.gravity(body2)
                    body1.collision(body2)


        self.root.after(1, self.frame)

animate()
