from multiprocessing import *
from tkinter import *
from random import *
from math import *

class atom:
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys

def main(quantity, radius, speed, max_x, max_y, min_x=0, min_y=0):

    lock = Lock()

    diam = radius * 2
    width = max_x - min_x
    height = max_y - min_y

    atom_list = []
    for i in range(quantity):
        angle = uniform(0, 2*pi)
        coeff = uniform(0.5,2)
        self.atom_list.append(atom(
            uniform(self.min_x + self.radius, self.max_x - self.radius),
            uniform(self.min_y + self.radius, self.max_y - self.radius),
            sin(angle) * self.speed * coeff,
            cos(angle) * self.speed * coeff))

    self.canvaswidth = self.atoms.max_x - self.atoms.min_x
    self.canvasheight = self.atoms.max_y - self.atoms.min_y
    self.root = Tk()
    self.canvas = Canvas(self.root, width = self.canvaswidth, height = self.canvasheight)
    self.canvas.pack()
    for atom in self.atoms.atom_list:
        atom.canvasobject = self.canvas.create_oval(atom.x-self.atoms.radius, atom.y-self.atoms.radius, atom.x+self.atoms.radius, atom.y+self.atoms.radius, fill = 'black')

    self.frame()
    self.root.mainloop()

    def physics(conn_start):

        def update_atoms():

            def collisions():

                def collision(f_i, s_i):
                    f_atom = atom_list[f_i]; s_atom = atom_list[s_i]
                    dist = ((f_atom.x - s_atom.x)**2 + (f_atom.y - s_atom.y)**2)**0.5
                    if dist < self.radius * 2 and f_i != s_i:
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

                for i in range(len(self.atom_list)):
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
                    if atom.x < self.min_x:
                        atom.x += width
                    elif atom.x > self.max_x:
                        atom.x -= width

                    atom.y += atom.ys
                    if atom.y < self.min_y:
                        atom.y += height
                    elif atom.y > self.max_y:
                        atom.y -= height

            with lock:
                collisions()
                apply_speed()


    def graphics(conn_end):
        pass
