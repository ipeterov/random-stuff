from vispy import app
from vispy import gloo
from math import *
import time
from vec import Vec

class Body:
    def __init__(self, x=0, y=0, xs=0, ys=0, mass=1, radius=1, angle=None, speed=None):
        self.coords = Vec(x,y)
        if angle == None or speed == None:
            self.speed = Vec(xs, ys)
        else:
            rad_angle = (-angle+90) / (180 / pi)
            self.speed = Vec(sin(rad_angle) * speed, cos(rad_angle) * speed)
        self.mass = mass
        self.radius = radius
        self.frozen = False
        self.angle = angle

    @property
    def x(self):
        return self.coords.x

    @property
    def y(self):
        return self.coords.y

    @property
    def density(self):
        return self.mass / (pi * self.radius ** 2)

    def tick(self, forces, dt):
        if not self.frozen:
            acceleration = Vec(0, 0)
            for force in forces:
                acceleration += force / self.mass
            self.speed += acceleration * dt
            self.coords += self.speed * dt

class World:
    def __init__(self, g=0, drag=0, dt_coeff=1):
        self.g = g
        self.drag = drag

        self.bodies = []

        self.drawer = Drawer(self.tick, dt_coeff)

    def start(self):
        self.drawer.start()

    def add_body(self, *args, **kwargs):
        body = Body(*args, **kwargs)
        self.bodies.append(body)

    def tick(self, dt):
        for body in self.bodies:
            forces = []

            # Gravity
            forces.append(Vec(0, -body.mass*self.g))

            # Drag
            drag = -body.speed.normalize() * body.speed.len()**2 * body.radius * self.drag
            #~ if not body.frozen:
                #~ print(body.coords, drag.len())
            forces.append(drag)

            # Floor
            if body.y < -1 and not body.frozen:
                body.frozen = True # Остановка
                print(body.x, body.angle)
                #~ body.speed.y *= -1 # Отскок

            body.tick(forces, dt)

        return [(body.x, body.y, body.radius) for body in self.bodies]

class Drawer:
    def __init__(self, point_function, dt_coeff, width=900, height=900):

        self.point_function = point_function
        self.dt_coeff = dt_coeff

        vertex ="""
            attribute vec3 circle;

            void main(void)
            {
                gl_Position = vec4(circle[0], circle[1], 0.0, 1.0);
                gl_PointSize = 2.0*(circle[2]);
            }
        """

        fragment = """
            void main(void)
            {
                float distance = length(vec2(0.5, 0.5) - gl_PointCoord);

                if (distance <= 0.5)
                    gl_FragColor = vec4(1, 1, 1, 1);
                else
                    discard;
            }
        """

        program = gloo.Program(vertex, fragment)

        c = app.Canvas(keys='interactive', size=(width, height))
        gloo.clear()
        self.c = c

        self.prev_tick_time = None

        @c.connect
        def on_draw(event):
            if self.prev_tick_time == None:
                self.prev_tick_time = time.perf_counter()

            dt = (time.perf_counter() - self.prev_tick_time) * self.dt_coeff

            circles = self.point_function(dt)
            program['circle'] = circles

            #~ gloo.clear()
            program.draw('points')
            c.update()

        @c.connect
        def on_resize(event):
            gloo.set_viewport(0, 0, *event.size)

    def start(self):
        self.c.show()
        app.run()


if __name__ == '__main__':
    #~ earth = World(g=0.00002, drag=0, dt_coeff=0.1)
    earth = World(g=0.000005, drag=2, dt_coeff=0.1)
    #~ earth.add_body(x=-1, y=0.0001, xs=0.02, ys=0.02)
    #~ earth.add_body(x=-1, y=0.0001, xs=0.02, ys=0.01)
    #~ earth.add_body(x=-1, y=-1, speed=0.1, angle=15, radius=1)
    #~ earth.add_body(x=-1, y=-1, speed=0.01, angle=30, radius=1)
    #~ earth.add_body(x=-1, y=-1, speed=0.01, angle=45, radius=1)
    #~ earth.add_body(x=-1, y=-1, speed=0.1, angle=60, radius=1)
    #~ earth.add_body(x=-1, y=-1, speed=0.1, angle=75, radius=1)

    for angle in range(0, 90, 15):
        earth.add_body(x=-1, y=-1, speed=0.004, angle=angle, radius=1)

    earth.start()
