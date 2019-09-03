import labyrinth_lib, pickle, random, time

def create_labyrinth_hunt_and_kill(size = (40, 40)):
    
    labyrinth = labyrinth_lib.labyrinth_object(size = size, method = 'hunt_and_kill')
    
    width = size[0]
    height = size[1]
    
    current = random.randint(0, width), random.randint(0, height)
    visited = []
    unvisited  = [(x, y) for x in range(width) for y in range(height)]
    
    while True:
        
        if unvisited:
            current = unvisited.pop(0)
        else:
            break
        
        while True:
            
            neighbours = [x for x in labyrinth.near_passable_coords(current, only_passable = 'not_only') if x not in visited]
            
            if current not in visited: visited.append(current)
            if current in unvisited: unvisited.remove(current)
            
            if neighbours:
                next_coords = random.choice(neighbours)
                labyrinth.remove_border(current, next_coords)
                current = next_coords
            else:
                labyrinth.remove_border(current, random.choice(labyrinth.near_passable_coords(current, only_passable = 'only_not')))
                break
    
    return labyrinth

a = create_labyrinth_hunt_and_kill()

a.display()
        
pickle.dump(a, open('labyrinth_hunt_and_kill', 'wb'))
