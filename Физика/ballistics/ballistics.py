from tkinter import *
from math import *


class Body:
    def __init__(self, x, y, s_x=0, s_y=0, a_x=0, a_y=0):
        self.radius = 10
        self.x = x
        self.y = y
        self.s_x = s_x
        self.s_y = s_y
        self.a_x = a_x
        self.a_y = a_y

    def stop(self):
        self.s_x = 0
        self.s_y = 0
        self.a_x = 0
        self.a_y = 0

    def tick(self):
        self.s_x += self.a_x
        self.s_y += self.a_y
        self.x += self.s_x
        self.y += self.s_y

    def speed(self):
        return hypot(self.s_y, self.s_x)


class World:
    def __init__(self, bodies=[]):
        self.bodies = bodies
        self.g = -0.001
        self.density = 1

        self.root = Tk()
        self.canvas = Canvas(self.root, width=900, height=900)
        self.canvas.pack()
        for body in self.bodies:
            body.canvasobject = self.canvas.create_oval(body.x-body.radius, body.y-body.radius, body.x+body.radius, body.y+body.radius, fill = 'black')

        self.frame()
        self.root.mainloop()

    def frame(self):
        self.tick()
        for body in bodies:
            self.canvas.coords(body.canvasobject, body.x-body.radius, body.y-body.radius, body.x+body.radius, body.y+body.radius)

        self.root.after(1, self.frame)

    def body_tick(self, body):
        body.s_y -= self.g # gravity


        #~ body.s_y /= body.speed()**2 * self.density
        #~ body.s_x /= body.speed()**2 * self.density

        body.tick()
        if body.y >= 900:
            #~ body.stop()
            body.s_y *= -1
        #~ print(body.x, body.y)


    def tick(self):
        for body in bodies:
            self.body_tick(body)



angle = 10
coeff = 0.25
rad_angle = angle / (180 / pi)
bodies = [Body(0, 880, sin(rad_angle)*coeff, -cos(rad_angle)*coeff)]
a = World(bodies)
