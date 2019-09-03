import pickle

def refactored_labyrinth(labyrinth):
    # 0 - верх, 1 право, 2 - лево, 3 - низ
    refactored_labyrinth = []
    for y in range(len(labyrinth)):
        refactored_labyrinth.append([])
        for x in range(len(labyrinth[0])):
            refactored_labyrinth[y].append([0,0,0,0])
    for y in range(len(labyrinth)):
        for x in range(len(labyrinth[0])):
            if labyrinth[y-1][x]['d'] == 1 or y == 0:
                refactored_labyrinth[y][x][0] = 1
            if labyrinth[y][x]['r'] == 1 or x == len(labyrinth[0]) - 1:
                refactored_labyrinth[y][x][1] = 1
            if labyrinth[y][x]['d'] == 1 or y == len(labyrinth) - 1:
                refactored_labyrinth[y][x][2] = 1
            if labyrinth[y][x-1]['r'] == 1 or x == 0:
                refactored_labyrinth[y][x][3] = 1
    return refactored_labyrinth

def find_path(labyrinth, start_coords = [0,0]):
    def move(current_coords, forbidden_move):
        if current_coords == goal_coords:
            #~ print('aaaaaaaa')
            for element in path:
                gpath.append(element)
            exit
            
        path.append(current_coords)
        dead_end = False
        print(current_coords)
        y = current_coords[0]
        x = current_coords[1]
        while not dead_end:
            for i in range(4):
                if labyrinth[y][x][i] != 1 and i != forbidden_move:
                    if i == 0:
                        move([y-1,x], 2)
                    elif i == 1:
                        move([y,x+1], 3)
                    elif i == 2:
                        move([y+1,x], 0)
                    elif i == 3:
                        move([y,x-1], 1)
                    i = 5
            if i != 5:
                dead_end = True
                try:
                    labyrinth[y + 1][x][0] = 1
                except:
                    pass
                try:
                    labyrinth[y][x - 1][1] = 1
                except:
                    pass
                try:
                    labyrinth[y - 1][x][2] = 1
                except:
                    pass
                try:
                    labyrinth[y][x + 1][3] = 1
                except:
                    pass
                path.pop()
    
    #~ print(labyrinth)
    labyrinth = refactored_labyrinth(labyrinth)
    #~ print(labyrinth)
    goal_coords = [99, 99]
    gpath = []
    path = []
    goal_reached = False
    move(start_coords, -1)
    if len(gpath) == 0:
        print('fuckfuckfuck')
        return None
    gpath.append(goal_coords)
    return gpath


name = 'labyrinth_backtrack'
labyrinth = pickle.load(open(name, 'rb'))

path = find_path(labyrinth)
pickle.dump(path, open('labyrinth_solution','wb'))
