from random import *
import tkinter

class cell:
    def __init__(self, r, d, state = None):
        self.r = r
        self.d = d
        self.state = state
    

class labyrinth_object:

    def __init__(self, size = (100, 100), method = 'none'):
        self.method = method
        self.size = size
        self.labyrinth = [[cell(1,1,None) for y in range(self.size[1])] for x in range(self.size[0])]        
            
    def init_from_labyrinth(self, labyrinth):
        self.size = len(labyrinth), len(labyrinth[0])
        
        self.labyrinth = [[cell(1,1,None) for y in range(self.size[1])] for x in range(self.size[0])]
        
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.labyrinth[x][y] = cell(labyrinth[x][y]['r'], labyrinth[x][y]['d'], None)
                
    def coords_valid(self, coords):
        if 0 <= coords[0] < self.size[0] and 0 <= coords[1] < self.size[1]:
            return True
        else:
            return False 
    
    def get_cell(self, coords):
        if self.coords_valid(coords):
            return self.labyrinth[coords[0]][coords[1]]
    
    def coords_relation(self, coords1, coords2):
        xdif = coords1[0] - coords2[0]
        ydif = coords1[1] - coords2[1]
        
        if xdif == -1 and ydif == 0:
            return 'right'
        elif xdif == 1 and ydif == 0:
            return 'left'
        elif xdif == 0 and ydif == -1:
            return 'down'
        elif xdif == 0 and ydif == 1:
            return 'up'
        else:
            return False

    
    def ispath(self, coords1, coords2):
        position = self.coords_relation(coords1, coords2)
        return_stuff = False
        
        if position == 'right':
            if self.labyrinth[coords1[1]][coords1[0]].r == 0:
                return_stuff = True
        elif position == 'left':
            if self.labyrinth[coords2[1]][coords2[0]].r == 0:
                return_stuff = True
        elif position == 'down':
            if self.labyrinth[coords1[1]][coords1[0]].d == 0:
                return_stuff = True
        elif position == 'up':
            if self.labyrinth[coords2[1]][coords2[0]].d == 0:
                return_stuff = True

        return return_stuff
        
        
    def add_border(self, coords1, coords2):
        position = self.coords_relation(coords1, coords2)
        
        if position == 'right':
            self.labyrinth[coords1[1]][coords1[0]].r = 1
        elif position == 'left':
            self.labyrinth[coords2[1]][coords2[0]].r = 1
        elif position == 'down':
            self.labyrinth[coords1[1]][coords1[0]].d = 1
        elif position == 'up':
            self.labyrinth[coords2[1]][coords2[0]].d = 1
        
    def remove_border(self, coords1, coords2):
        position = self.coords_relation(coords1, coords2)
        
        if position == 'right':
            self.labyrinth[coords1[1]][coords1[0]].r = 0
        elif position == 'left':
            self.labyrinth[coords2[1]][coords2[0]].r = 0
        elif position == 'down':
            self.labyrinth[coords1[1]][coords1[0]].d = 0
        elif position == 'up':
            self.labyrinth[coords2[1]][coords2[0]].d = 0

    def near_passable_coords(self, coords, key = lambda x: True, only_passable = 'only'):
        near_coords = []
        for coord_diff in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            other_coords = coords[0] + coord_diff[0], coords[1] + coord_diff[1]
            
            if only_passable == 'only':
                arg = self.ispath(coords, other_coords)
            elif only_passable == 'not_only':
                arg = True
            elif only_passable == 'only_not':
                arg = not self.ispath(coords, other_coords)
            
            if self.coords_valid(other_coords) and arg and key(other_coords):
                near_coords.append(other_coords)
                
        return near_coords
    
    def display(self, solution = None, cell_size = 30,  max_size = 900, line_width = 1, display_state = 0):
        
        root = tkinter.Tk()
        
        if len(self.labyrinth[0]) * cell_size > max_size or len(self.labyrinth) * cell_size > max_size:
            cell_size *= max_size / (len(self.labyrinth[0]) * cell_size)
        width = len(self.labyrinth[0]) * cell_size + line_width
        height = len(self.labyrinth) * cell_size + line_width
        canv = tkinter.Canvas(root, width = width, height = height, bg = 'white')
        
        for x in range(len(self.labyrinth)):
            for y in range(len(self.labyrinth[0])):
                
                if self.labyrinth[y][x].r == 1:
                    canv.create_line((x + 1) * cell_size + line_width, y * cell_size + line_width, (x + 1) * cell_size + line_width, (y + 1) * cell_size + line_width, width = line_width, capstyle = tkinter.PROJECTING)
                if self.labyrinth[y][x].d == 1:
                    canv.create_line(x * cell_size + line_width, (y + 1) * cell_size + line_width, (x + 1) * cell_size + line_width, (y + 1) * cell_size + line_width, width = line_width, capstyle = tkinter.PROJECTING)
                
                if display_state:
                    color = 'grey'
                    if self.labyrinth[y][x].state in ['pink', 'white']:
                        color = self.labyrinth[y][x].state
                    canv.create_rectangle(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill = color)
                
        
        if solution:
            for i in range(len(solution)):
                solution[i] = [x * cell_size + cell_size / 2 + 1 for x in solution[i]]

            canv.create_line(solution, fill = 'red')
        
        bbox = [line_width, line_width, width, height]
        canv.create_rectangle(bbox, width = line_width)
        canv.pack()
        root.mainloop()
