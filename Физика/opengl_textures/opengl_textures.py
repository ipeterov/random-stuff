from vispy import app, gloo, io
from vispy.gloo import Texture2D, Program, VertexBuffer
from random import *
from math import *
import time
import numpy as np

class atom:
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        self.xb = 0
        self.yb = 0

def main(quantity, radius, speed, max_x, max_y, min_x=0, min_y=0, loops = None):

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

        # Find collisions
        fcol_t = time.perf_counter()
        for (x, y) in non_empty_cells:

            other_atoms_i = grid[x][y] + grid[x][y-1] + grid[x+1][y-1] + grid[x+1][y] + grid[x+1][y+1]
            #~ other_atoms_i = (x for cell in (grid[x][y], grid[x][y-1], grid[x+1][y-1], grid[x+1][y], grid[x+1][y+1]) for x in cell)

            for atom_i in grid[x][y]:
                for other_atom_i in other_atoms_i:
                    collision(atom_i, other_atom_i)
        fcol_t = time.perf_counter() - fcol_t

        # Apply speed
        aplspd_t = time.perf_counter()
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
        aplspd_t = time.perf_counter() - aplspd_t

        # Update grid
        updgrd_t = time.perf_counter()
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
        updgrd_t = time.perf_counter() - updgrd_t

        # Return time spent
        return fcol_t, aplspd_t, updgrd_t

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


    vertex = """
        attribute vec3 positions;
        attribute vec2 a_texcoord;
        uniform float radius;

        varying vec2 v_texcoord;

        void main(void)
        {
            gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
            gl_PointSize = 2.0*(radius);
            v_texcoord = a_texcoord;
        }
    """

    fragment = """
        uniform sampler2D texture;

        varying vec2 v_texcoord;

        void main(void)
        {
            float distance = length(vec2(0.5, 0.5) - gl_PointCoord);

            if (distance <= 0.5)
                //gl_FragColor = vec4(1, 1, 1, 1);
                gl_FragColor = texture2D(texture, v_texcoord);
            else
                discard;
        }
    """

    #~ im = np.full((1,1), 0.5, 'float32')
    im = io.load_crate()

    positions_1 = np.array([  [-1, -1, 0.0], [+1, -1, 0.0],
                        [-1, +1, 0.0], [+1, +1, 0.0,] ], np.float32)
    texcoords_1 = np.array([  [1.0, 1.0], [0.0, 1.0],
                        [1.0, 0.0], [0.0, 0.0]], np.float32)

    texcoords = np.array([[1.0, 1.0], [0.0, 1.0],[1.0, 0.0], [0.0, 0.0]], np.float32)


    program = Program(vertex, fragment)

    program['texture'] = Texture2D(im)
    program['radius'] = radius
    program['a_texcoord'] = texcoords
    program['positions_1'] = positions_1
    program['texcoords_1']= texcoords_1


    c = app.Canvas(keys='interactive', size=(width, height))



    @c.connect
    def on_draw(event):

        #~ nonlocal loops
        runtime = update_atoms()
        #~ if loops != None:
            #~ update_times.append(runtime)
            #~ loops -= 1
            #~ if loops == 0:
                #~ fcol_t, aplspd_t, updgrd_t = [sum(times) / len(times) for times in zip(*update_times)]
                #~ print(fcol_t, aplspd_t, updgrd_t)
        positions = [[(atom.x - width / 2) / width * 2, (atom.y - height / 2) / height * 2, 0] for atom in atom_list]

        program['positions'] = positions
        gloo.clear()
        program.draw('points')
        c.update()

    @c.connect
    def on_resize(event):
        gloo.set_viewport(0, 0, *event.size)

    c.show()
    app.run()

main(quantity = 100, radius = 6, speed = 1, max_x = 900, max_y = 900, loops = 500)
