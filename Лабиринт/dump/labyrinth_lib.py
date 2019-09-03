from random import *
import tkinter

class cell:
    def __init__(self, x, y, r, d, state):
        self.x = x
        self.y = y
        self.coords = [x, y]
        self.r = r
        self.d = d
        state = state
    

class labyrinth_object:

    def __init__(self, size = (100, 100), method = 'backtrack'):
        self.method = method
        self.size = size
        self.labyrinth = []
        for x in range(size[0]):
            self.labyrinth.append([])
            for y in range(size[1]):
                self.labyrinth[-1].append(cell(x, y, 1, 1, None))
                
    def init_from_labyrinth(self, labyrinth):
        self.size = len(labyrinth), len(labyrinth[0])
        
        self.labyrinth = []
        for x in range(self.size[0]):
            self.labyrinth.append([])
            for y in range(self.size[1]):
                self.labyrinth[-1].append(cell(x, y, labyrinth[x][y]['r'], labyrinth[x][y]['d'], None))
                
    def coords_valid(self, coords):
        if 0 <= coords[0] < self.size[0] and 0 <= coords[1] < self.size[1]:
            return True
        else:
            return False 
    
    def get_cell(self, coords):
        if self.coords_valid(coords):
            return self.labyrinth[coords[0]][coords[1]]
    
    def cells_relation(self, cell1, cell2):
        # Возвращает положение второй клетки относительно первой
        if cell1.x - cell2.x == -1 and cell1.y - cell2.y == 0:
            return 'right'
        elif cell1.x - cell2.x == 1 and cell1.y - cell2.y == 0:
            return 'left'
        elif cell1.x - cell2.x == 0 and cell1.y - cell2.y == -1:
            return 'down'
        elif cell1.x - cell2.x == 0 and cell1.y - cell2.y == 1:
            return 'up'
        else:
            return False

    
    def ispath(self, cell1, cell2):
        position = self.cells_relation(cell1, cell2)
        return_stuff = False
        
        if position == 'right':
            if cell1.r == 0:
                return_stuff = True
        elif position == 'left':
            if cell2.r == 0:
                return_stuff = True
        elif position == 'down':
            if cell1.d == 0:
                return_stuff = True
        elif position == 'up':
            if cell2.d == 0:
                return_stuff = True

        return return_stuff
        
        
    def add_path(self, cell1, cell2):
        position = self.cells_relation(cell1, cell2)
        
        if position == 'right':
            cell2.r = 1
        elif position == 'left':
            cell1.r = 1
        elif position == 'down':
            cell2.d = 1
        elif position == 'up':
            cell1.d = 1
        
    def remove_path(self, cell1, cell2):
        position = self.cells_relation(cell1, cell2)
        
        if position == 'right':
            cell2.r = 0
        elif position == 'left':
            cell1.r = 0
        elif position == 'down':
            cell2.d = 0
        elif position == 'up':
            cell1.d = 0

    def near_passable_cells(self, cell):
        near_cells = []
        for coord_diff in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            coords = cell.x + coord_diff[0], cell.y + coord_diff[1]
            othercell = self.get_cell(coords)
            if self.coords_valid(coords) and self.ispath(cell, othercell):
                near_cells.append(othercell)
        return near_cells
    
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
                for j in range(2):
                    solution[i][j] *= cell_size
                    solution[i][j] += cell_size / 2
                a = solution[i][0]
                solution[i][0] =  solution[i][1]
                solution[i][1] = a

            canv.create_line(solution, fill = 'red')
        
        bbox = [line_width, line_width, width, height]
        canv.create_rectangle(bbox, width = line_width)
        canv.pack()
        root.mainloop()
