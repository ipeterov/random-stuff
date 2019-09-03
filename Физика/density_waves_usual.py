from random import *
from math import *
from tkinter import *

class atom:
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.xb = 0
        self.yb = 0

def main(quantity, radius, speed, max_x, max_y, min_x=0, min_y=0):

    def collision(f_i, s_i):

        f_atom = atom_list[f_i]; s_atom = atom_list[s_i]
        dist = hypot((f_atom.x - s_atom.x), (f_atom.y - s_atom.y))

        if dist < radius * 2 and f_i != s_i:

            co = abs((s_atom.x - f_atom.x) / dist)
            si = abs((s_atom.y - f_atom.y) / dist)
            sphere_dist = radius - dist / 2

            f_atom.s = (f_atom.xs**2 + f_atom.ys**2)**0.5
            s_atom.s = (s_atom.xs**2 + s_atom.ys**2)**0.5

            if f_atom.x > s_atom.x:
                f_atom.xb += sphere_dist * si
                s_atom.xb -= sphere_dist * si
                f_atom.xs = si * s_atom.s
                s_atom.xs = -si * f_atom.s
            else:
                f_atom.xb -= sphere_dist * si
                s_atom.xb += sphere_dist * si
                f_atom.xs = -si * s_atom.s
                s_atom.xs = si * f_atom.s

            if f_atom.y > s_atom.y:
                f_atom.yb += sphere_dist * co
                s_atom.yb -= sphere_dist * co
                f_atom.ys = co * s_atom.s
                s_atom.ys = -co * f_atom.s
            else:
                f_atom.yb -= sphere_dist * co
                s_atom.yb += sphere_dist * co
                f_atom.ys = -co * s_atom.s
                s_atom.ys = co * f_atom.s

    def update_atoms():

        #Find collisions
        for (x, y) in non_empty_cells:

            other_atoms_i = grid[x][y] + grid[x][y-1] + grid[x+1][y-1] + grid[x+1][y] + grid[x+1][y+1]

            for atom_i in grid[x][y]:
                for other_atom_i in other_atoms_i:
                    collision(atom_i, other_atom_i)

        # Apply speed
        for atom in atom_list:
            if atom.x - radius < min_x:
                atom.x = min_x + radius
                atom.xs *= -1
            elif atom.x + radius > max_x:
                atom.x = max_x - radius
                atom.xs *= -1

            if atom.y - radius < min_y:
                atom.y = min_y + radius
                atom.ys *= -1
            elif atom.y + radius > max_y:
                atom.y = max_y - radius
                atom.ys *= -1

            atom.x += atom.xs + atom.xb
            atom.y += atom.ys + atom.yb

            atom.xb = 0; atom.yb = 0

        #Update grid
        for (x, y) in non_empty_cells.copy():

            for atom_i in grid[x][y].copy():

                nx, ny = int(atom_list[atom_i].x / diam), int(atom_list[atom_i].y / diam)

                if (nx, ny) != (x, y):
                    grid[x][y].remove(atom_i)
                    grid[nx][ny].append(atom_i)
                    if (nx, ny) not in non_empty_cells:
                        non_empty_cells.append((nx, ny))

            if len(grid[x][y]) == 0:
                non_empty_cells.remove((x, y))
                
    def frame():
        update_atoms()
        for atom in atom_list:
            canvas.coords(atom.canvasobject, atom.x - radius, atom.y - radius, atom.x + radius, atom.y + radius)
        root.after(1, frame)

    diam = radius * 2
    width = max_x - min_x
    height = max_y - min_y

    atom_list = []
    for i in range(quantity):
        angle = uniform(0, 2*pi)
        coeff = 1 #uniform(0.5,2)
        atom_list.append(atom(
            uniform(min_x + radius, max_x - radius),
            uniform(min_y + radius, max_y - radius),
            sin(angle) * speed * coeff,
            cos(angle) * speed * coeff))

    grid = []
    for x in range(int(width / diam) + 2):
        grid.append([])
        for y in range(int(height / diam) + 2):
            grid[-1].append([])

    non_empty_cells = []
    for i in range(len(atom_list)):
        x, y = int(atom_list[i].x / diam), int(atom_list[i].y / diam)
        grid[x][y].append(i)
        if (x, y) not in non_empty_cells:
            non_empty_cells.append((x, y))
            
    # Initialize canvas
    root = Tk()
    canvas = Canvas(root, width = width, height = height)
    canvas.pack()
    for atom_inst in atom_list:
        atom_inst.canvasobject = canvas.create_oval(atom_inst.x - radius, atom_inst.y - radius, atom_inst.x + radius, atom_inst.y + radius, fill = 'black')
    
    # Main loop
    frame()
    root.mainloop()


main(quantity = 300, radius = 5, speed = 1, max_x = 700, max_y = 700)
