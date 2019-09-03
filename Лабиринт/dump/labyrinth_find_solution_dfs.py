import labyrinth_lib, pickle, pprint

def find_path_dfs(my_labyrinth, start_coords = [0,0], finish_coords = None):
    
    def move(destination_coords):
              
        if destination_coords == finish_coords:
            return 'finished'
        
        visited.append(destination_coords)
        path.append(destination_coords)
        
        near_passables = my_labyrinth.near_passable_coords(destination_coords)
        for near_coords in near_passables.copy():
            if near_coords in visited:
                near_passables.remove(near_coords)
        
        if near_passables:
            for near_coords in near_passables:
                if move(near_coords) == 'finished':
                    return 'finished'
        else:
            path.remove(destination_coords)
    
    if not finish_coords:
        finish_coords = my_labyrinth.size[0] - 1, my_labyrinth.size[1] - 1
    
    visited = []
    path = []
    
    move(start_coords)
    
    return visited
    
name = 'labyrinth_backtrack'
labyrinth = labyrinth_lib.labyrinth_object()
labyrinth.init_from_labyrinth(pickle.load(open(name, 'rb')))

path = find_path_dfs(labyrinth, finish_coords = [99,99])
pprint.pprint(path)

#~ print(labyrinth.ispath(labyrinth.get_cell((0,0)), labyrinth.get_cell((0,1))))
#~ print(labyrinth.get_cell((0,1)).d)
#~ print(labyrinth.get_cell((1,0)).d)
#~ print(labyrinth.near_passable_cells(labyrinth.get_cell((0,0))))
#~ print([x.coords for x in labyrinth.near_passable_cells(labyrinth.get_cell((0,0)))])

labyrinth.display(path)


#~ pickle.dump(path, open('labyrinth_solution','wb'))

