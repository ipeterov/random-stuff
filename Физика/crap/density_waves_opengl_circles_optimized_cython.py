from vispy import app, gloo
from random import *
from math import *
from atom_lib import *

class atom:
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys


def main(quantity, radius, speed, max_x, max_y, min_x=0, min_y=0):

    def update_atoms():

        # Finding collisions
        for (x, y) in non_empty_cells.copy():

            other_atoms_i = grid[x][y] | grid[x][y-1] | grid[x+1][y-1] | grid[x+1][y] | grid[x+1][y+1]

            for atom_i in grid[x][y].copy():
                for other_atom_i in other_atoms_i:

                    if atom_i != other_atom_i:
                        collision(atom_list[atom_i], atom_list[other_atom_i], radius)

                    nx, ny = int(atom_list[atom_i].x / diam), int(atom_list[atom_i].y / diam)

                    if (nx, ny) != (x, y):
                        grid[x][y].discard(atom_i)
                        grid[nx][ny].add(atom_i)
                        if (nx, ny) not in non_empty_cells:
                            non_empty_cells.append((nx, ny))

            if not grid[x][y]:
                non_empty_cells.remove((x, y))

        # Applying speed
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

            atom.x += atom.xs
            atom.y += atom.ys


    diam = radius * 2
    width = max_x - min_x
    height = max_y - min_y

    atom_list = []
    for i in range(quantity):
        angle = uniform(0, 2*pi)
        coeff = uniform(0.5,2)
        atom_list.append(atom(
            uniform(min_x + radius, max_x - radius),
            uniform(min_y + radius, max_y - radius),
            sin(angle) * speed * coeff,
            cos(angle) * speed * coeff))

    grid = []
    for x in range(int(width / diam) + 2):
        grid.append([])
        for y in range(int(height / diam) + 2):
            grid[-1].append(set())

    non_empty_cells = []
    for i in range(len(atom_list)):
        grid[int(atom_list[i].x / diam)][int(atom_list[i].y / diam)].add(i)
        non_empty_cells.append((int(atom_list[i].x / diam), int(atom_list[i].y / diam)))



    vertex = """
        attribute vec2 positions;
        uniform float radius;

        void main ()
        {
            gl_Position = vec4(positions, 0.0, 1.0);
            gl_PointSize = 2.0*(radius);
        }
    """

    fragment = """
        in vec2 gl_PointCoord;

        void main()
        {
            float distance = length(vec2(0.5, 0.5) - gl_PointCoord);

            if (distance <= 0.5)
                gl_FragColor = vec4(1, 1, 1, 1);
            else
                discard;
        }
    """

    program = gloo.Program(vertex, fragment)
    program['radius'] = radius

    c = app.Canvas(keys='interactive', size=(width, height))

    @c.connect
    def on_draw(event):
        update_atoms()
        program['positions'] = [[(atom.x - width / 2) / width * 2, (atom.y - height / 2) / height * 2] for atom in atom_list]
        gloo.clear()
        program.draw('points')
        c.update()


    @c.connect
    def on_resize(event):
        gloo.set_viewport(0, 0, *event.size)

    c.show()
    app.run()

main(quantity = 1000, radius = 3, speed = 1, max_x = 700, max_y = 700)
