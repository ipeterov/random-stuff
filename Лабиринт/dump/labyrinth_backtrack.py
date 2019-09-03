import random, pickle, tkinter

def display_labyrinth(labyrinth, cell_size = 10,  display_set = 0, max_size = 1400, line_width = 1, solution = None):
    
    root = tkinter.Tk()
    
    if len(labyrinth[0]) * cell_size > max_size or len(labyrinth) * cell_size > max_size:
        cell_size *= max_size / (len(labyrinth[0]) * cell_size)
    width = len(labyrinth[0]) * cell_size + line_width
    height = len(labyrinth) * cell_size + line_width
    canv = tkinter.Canvas(root, width = width, height = height, bg = 'white')
    
    for y in range(len(labyrinth)):
        for x in range(len(labyrinth[y])):
            if labyrinth[y][x]['r'] == 1:
                canv.create_line((x + 1) * cell_size + line_width, y * cell_size + line_width, (x + 1) * cell_size + line_width, (y + 1) * cell_size + line_width, width = line_width, capstyle = tkinter.PROJECTING)
            if labyrinth[y][x]['d'] == 1:
                canv.create_line(x * cell_size + line_width, (y + 1) * cell_size + line_width, (x + 1) * cell_size + line_width, (y + 1) * cell_size + line_width, width = line_width, capstyle = tkinter.PROJECTING)
            if display_set == 1:
                canv.create_text((x+0.5)*cell_size, (y+0.5)*cell_size, text= labyrinth[y][x]['set'])
    
    if solution:
        #~ print(solution)
        for i in range(len(solution)):
            for j in range(2):
                solution[i][j] *= cell_size
                solution[i][j] += cell_size / 2
            a = solution[i][0]
            solution[i][0] =  solution[i][1]
            solution[i][1] = a

        canv.create_line(solution, fill = 'red')
    
    #~ bbox = [line_width, line_width, width, height]
    #~ canv.create_rectangle(bbox, width = line_width)
    canv.pack()
    root.mainloop()

def create_labyrinth_backtrack(width = 100, height = 100):
    
    def coords_valid(coords, borders):
        if 0 <= coords[0] < borders[0] and 0 <= coords[1] < borders[1]:
            return True
        else:
            return False

    def remove_border(coords1, coords2):
        
        #~ print(coords1[0] - coords2[0], coords1[1] - coords2[1])
        
        if coords1[0] - coords2[0] == 1 and coords1[1] - coords2[1] == 0:
            labyrinth[coords2[0]][coords2[1]]['d'] = 0
        if coords1[0] - coords2[0] == -1 and coords1[1] - coords2[1] == 0:
            labyrinth[coords1[0]][coords1[1]]['d'] = 0
        if coords1[0] - coords2[0] == 0 and coords1[1] - coords2[1] == 1:
            labyrinth[coords2[0]][coords2[1]]['r'] = 0
        if coords1[0] - coords2[0] == 0 and coords1[1] - coords2[1] == -1:
            labyrinth[coords1[0]][coords1[1]]['r'] = 0

    labyrinth = []
    for i in range(width):
        labyrinth.append([])
        for j in range(height):
            labyrinth[-1].append({'r' : 1, 'd' : 1, 'state' : 'blanc'}) # state can be 'blanc', 'pink', 'white'
    
    
    start_coords = [random.randint(0,width), random.randint(0,height)]
    coords = start_coords
    path = []
    
    finished = False
    count = 0
    while not finished:
        
        count += 1
        near_blanc_cells = []
        for coord_diff in (1, 0), (-1, 0), (0, 1), (0, -1):
            new_coords = coords[0] + coord_diff[0], coords[1] + coord_diff[1]
            if coords_valid(new_coords, (width, height)) and labyrinth[new_coords[0]][new_coords[1]]['state'] == 'blanc':
                near_blanc_cells.append(new_coords)
                #~ print(new_coords)
        
        if near_blanc_cells:
            labyrinth[coords[0]][coords[1]]['state'] = 'pink'
            chosen_coords = random.choice(near_blanc_cells)
            remove_border(coords, chosen_coords)
            path.append(coords)
            #~ if abs(coords[0] - chosen_coords[0]) > 1 or abs(coords[1] - chosen_coords[1]) > 1:
            #~ display_labyrinth(labyrinth)
            coords = chosen_coords
        else:
            labyrinth[coords[0]][coords[1]]['state'] = 'white'
            coords = path.pop()
            
        if coords == start_coords and count != 1:
            finished = True
            
    return labyrinth
    

a = create_labyrinth_backtrack(25, 25)
#~ pickle.dump(a, open('labyrinth_backtrack', 'wb'))
#~ a = pickle.load(open('labyrinth_backtrack', 'rb'))
#~ b = pickle.load(open('labyrinth_solution', 'rb'))
#~ print(a)
display_labyrinth(a)
