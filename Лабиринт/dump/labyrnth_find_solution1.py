from labyrinth_lib import *

def find_path(my_labyrinth, start_coords = (0,0), finish_coords = None):
    if not finish_coords:
        finish_coords = (my_labyrinth.size[0] - 1, my_labyrinth.size[1] - 1)

    path = []
    all_path = []
    
    def move(coords):
        path.append(coords)
        all_path.append(coords)
        current_cell = my_labyrinth.get_cell(coords)
        near_valid_cells_arr = my_labyrinth.near_valid_cells(current_cell)
        #~ print(near_valid_cells_arr)
        
        for cell in near_valid_cells_arr.copy():
            ispath = my_labyrinth.ispath(current_cell, cell)
            #~ print(ispath)
            #~ print('11111111')
            if cell in all_path or (not ispath) or coords == finish_coords:
                #~ print(cell in path, not my_labyrinth.ispath(current_cell, cell), coords == finish_coords)
                near_valid_cells_arr.remove(cell)
        #~ print(near_valid_cells_arr)
                
        if near_valid_cells_arr:
            for cell in near_valid_cells_arr:
                #~ print(cell.coords)
                
                move(cell.coords)
        else:
            #~ print("near_valid_cells_arr is empty")
            path.pop()
            
            
        
    move(start_coords)
    
    return path
    
name = 'labyrinth'
my_labyrinth = labyrinth_object()
my_labyrinth.init_from_labyrinth(pickle.load(open(name, 'rb')))

path = find_path(my_labyrinth)
pickle.dump(path, open('labyrinth_solution_1','wb'))
