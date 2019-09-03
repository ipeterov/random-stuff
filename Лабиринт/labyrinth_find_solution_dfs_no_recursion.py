import labyrinth_lib, pickle

def find_path_dfs(my_labyrinth, start_coords = [0,0], finish_coords = None):
    
    if not finish_coords:
        finish_coords = [my_labyrinth.size[0] - 1, my_labyrinth.size[1] - 1]
        
    current_coords = start_coords
    path = [current_coords]
    
    while True:

        if current_coords == finish_coords:
            break
        
        near_passables = my_labyrinth.near_passable_coords(current_coords, key = lambda x: my_labyrinth.labyrinth[x[0]][x[1]].state != 'blocked')
        near_passables.sort(key=lambda x: 2 * (my_labyrinth.labyrinth[x[0]][x[1]].state != None) + (path[-1] != x))

        if not near_passables or near_passables == [path[-1]]:
            my_labyrinth.labyrinth[current_coords[0]][current_coords[1]].state = 'blocked'
            current_coords = path.pop()

        else:
            path.append(current_coords)
            my_labyrinth.labyrinth[current_coords[0]][current_coords[1]].state = 'visited'
            current_coords = near_passables[0]

    path = path[1:]
    path.append(finish_coords)
    
    return path
    
name = 'labyrinth_hunt_and_kill'
#~ labyrinth = labyrinth_lib.labyrinth_object()
#~ labyrinth.init_from_labyrinth(pickle.load(open(name, 'rb')))

labyrinth = pickle.load(open(name, 'rb'))

path = find_path_dfs(labyrinth)

labyrinth.display(path)
