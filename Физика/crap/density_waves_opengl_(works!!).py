import numpy as np
from vispy import app
from vispy import gloo
from random import *
from math import *

class atom:
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys

def main(quantity, radius, speed, max_x, max_y, min_x=0, min_y=0):

    def update_atoms():

        def collisions():

            def collision(f_i, s_i):
                f_atom = atom_list[f_i]; s_atom = atom_list[s_i]
                dist = ((f_atom.x - s_atom.x)**2 + (f_atom.y - s_atom.y)**2)**0.5
                if dist < radius * 2 and f_i != s_i:
                    co = abs((s_atom.x - f_atom.x) / dist)
                    si = abs((s_atom.y - f_atom.y) / dist)

                    f_atom.s = (f_atom.xs**2 + f_atom.ys**2)**0.5
                    s_atom.s = (s_atom.xs**2 + s_atom.ys**2)**0.5

                    if f_atom.x > s_atom.x:
                        f_atom.x += (radius - dist / 2) * si
                        s_atom.x -= (radius - dist / 2) * si
                        f_atom.xs = si * s_atom.s
                        s_atom.xs = -si * f_atom.s
                    else:
                        f_atom.x -= (radius - dist / 2) * si
                        s_atom.x += (radius - dist / 2) * si
                        f_atom.xs = -si * s_atom.s
                        s_atom.xs = si * f_atom.s

                    if f_atom.y > s_atom.y:
                        f_atom.y += (radius - dist / 2) * co
                        s_atom.y -= (radius - dist / 2) * co
                        f_atom.ys = co * s_atom.s
                        s_atom.ys = -co * f_atom.s
                    else:
                        f_atom.y -= (radius - dist / 2) * co
                        s_atom.y += (radius - dist / 2) * co
                        f_atom.ys = -co * s_atom.s
                        s_atom.ys = co * f_atom.s

            grid = []
            non_empty_cells = []

            for x in range(int(width / diam) + 2):
                grid.append([])
                for y in range(int(height / diam) + 2):
                    grid[-1].append([])

            for i in range(len(atom_list)):
                grid[int(atom_list[i].x / diam)][int(atom_list[i].y / diam)].append(i)
                non_empty_cells.append((int(atom_list[i].x / diam), int(atom_list[i].y / diam)))

            for x,y in non_empty_cells:
                others = grid[x][y] + grid[x+1][y] + grid[x][y+1] + grid[x+1][y-1] + grid[x+1][y+1]
                for atom_i in grid[x][y]:
                    for other_atom_i in others:
                        collision(atom_i, other_atom_i)

        def apply_speed():
            for atom in atom_list:
                atom.x += atom.xs
                if atom.x < min_x:
                    atom.x += width
                elif atom.x > max_x:
                    atom.x -= width

                atom.y += atom.ys
                if atom.y < min_y:
                    atom.y += height
                elif atom.y > max_y:
                    atom.y -= height

        collisions()
        apply_speed()

    diam = radius * 2
    width = max_x - min_x
    height = max_y - min_y

    atom_list = []
    for i in range(quantity):
        angle = uniform(0, 2*pi)
        coeff = 1#uniform(0.5,2)
        atom_list.append(atom(
            uniform(min_x + radius, max_x - radius),
            uniform(min_y + radius, max_y - radius),
            sin(angle) * speed * coeff,
            cos(angle) * speed * coeff))

    c = app.Canvas(keys='interactive', size=(width, height))

    vertex = """
        attribute vec2 positions;
        uniform float radius;

        void main (void)
        {
            gl_Position = vec4(positions, 0.0, 1.0);
            gl_PointSize = 2.0*(radius);
        }
    """

    fragment = """
        uniform vec2 positions;
        uniform float radius;

        void main()
        {
            gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
        }
    """
    program = gloo.Program(vertex, fragment)
    program['radius'] = radius
    program['positions'] = [[(atom.x - width / 2) / width * 2, (atom.y - height / 2) / height * 2] for atom in atom_list]

    @c.connect
    def on_resize(event):
        gloo.set_viewport(0, 0, *event.size)

    @c.connect
    def on_draw(event):
        update_atoms()
        program['positions'] = [[(atom.x - width / 2) / width * 2, (atom.y - height / 2) / height * 2] for atom in atom_list]
        gloo.clear((1,1,1,1))
        program.draw('points')
        c.update()

    c.show()
    app.run()

main(100, 5, 1, 600, 600)
