from tkinter import *
from random import *
from math import *

class body:
    def __init__(self, x=0, y=0, xs=0, ys=0, density = 1, radius = 3):
        self.mass = pi * radius**2 * density
        self.density = density
        self.radius = radius
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.s = None
        self.momentum = None

    def dist(self, otherbody):
        return ((self.x - otherbody.x)**2 + (self.y - otherbody.y)**2)**0.5

    def gravity(self, otherbody):
        distance = self.dist(otherbody)
        a = self.mass / (distance**2 * otherbody.mass)
        otherbody.xs += (self.x-otherbody.x) / distance * a
        otherbody.ys += (self.y-otherbody.y) / distance * a

    def tick(self):
        self.s = ((self.xs)**2 + (self.ys)**2)**0.5
        self.momentum = self.s * self.mass
        self.x += self.xs
        self.y += self.ys


class bodysystem:
    def __init__(self):
        self.bodies = []

    def dist(self, body0, body1):
        return ((body0.x - body1.x)**2 + (body0.y - body1.y)**2)**0.5

    def collisions(self):
        def collide(body0, body1):
            a = 2 * (body0.momentum + body1.momentum) / (body0.mass + body1.mass)
            ispeed = -body0.s + a
            jspeed = -body1.s + a
            xpart = abs(body0.x - body1.x) / distance
            ypart = abs(body0.y - body1.y) / distance
            body0.xs = ispeed * xpart
            body0.ys = ispeed * ypart
            body1.xs = jspeed * xpart
            body1.ys = jspeed * ypart

        self.bodies.sort(key=lambda body: body.x)
        for i in range(len(self.bodies)):
            rightboard = self.bodies[i].x + self.bodies[i].radius
            for j in range(i+1, len(self.bodies)):
                leftboard = self.bodies[j].x - self.bodies[j].radius
                if rightboard < leftboard:
                    break
                distance = self.dist(self.bodies[i], self.bodies[j])
                if distance < (self.bodies[i].radius + self.bodies[j].radius):
                    collide(self.bodies[i], self.bodies[j])


    def gravity(self):
        for body0 in self.bodies:
            for body1 in self.bodies:
                if not body0 is body1:
                    body0.gravity(body1)

class animate():
    def __init__(self):
        self.canvaswidth = 900
        self.canvasheight = 900
        self.bodysystem = bodysystem()

        self.bodysystem.bodies.append(body(x = 0, y = 0, radius = 25, ys = 5, xs = 5, density = 0.5))
        for x in range(300, 600, 9):
            for y in range(300, 600, 9):
                self.bodysystem.bodies.append(body(x = x, y = y))
#        for i in range(400):
#            self.bodysystem.bodies.append(body(x = uniform(300, 600), y = uniform(300, 600)))
#        self.bodysystem.bodies.append(body(x = 900, y = 900, radius = 25, ys = -1, xs = -1))
        self.root = Tk()
        self.canvas = Canvas(self.root, width = self.canvaswidth, height = self.canvasheight)
        self.canvas.pack()
        for body1 in self.bodysystem.bodies:
            body1.canvasobject = self.canvas.create_oval(body1.x-body1.radius, body1.y-body1.radius, body1.x+body1.radius, body1.y+body1.radius, fill = 'black')
        self.frame()
        self.root.mainloop()

    def frame(self):
        for body1 in self.bodysystem.bodies:
            self.canvas.coords(body1.canvasobject, body1.x-body1.radius, body1.y-body1.radius, body1.x+body1.radius, body1.y+body1.radius)
            body1.tick()
#        for body1 in self.bodysystem.bodies:
#            for body2 in self.bodysystem.bodies:
#                if not body1 is body2:
#                    body1.gravity(body2)
        self.bodysystem.collisions()
#        self.bodysystem.gravity()
        self.root.after(1, self.frame)

animate()
