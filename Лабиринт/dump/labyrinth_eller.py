import pickle, tkinter, random

def display_labyrinth(labyrinth, cell_size = 10,  display_set = 0, max_size = 900, line_width = 1, solution = None):
    
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

def sets_array(labyrinth_part):
    sets = {}
    for i in range(len(labyrinth_part)):
        if labyrinth_part[i]['set'] not in sets:
            sets[labyrinth_part[i]['set']] = [i]
        else:
            sets[labyrinth_part[i]['set']].append(i)
    return sets

def create_labyrinth(width, height, right_density = 0.5):

    labyrinth = []
    labyrinth.append([])
    for x in range(width):
        labyrinth[0].append({'r' : -1, 'd' : -1, 'set' : x})
    for x in range(width-1):
        if random.random() > right_density:
            labyrinth[0][x]['r'] = 1
        else:
            labyrinth[0][x+1]['set'] = labyrinth[0][x]['set']
            labyrinth[0][x]['r'] = 0
    sets = sets_array(labyrinth[0])
    for key in sets:
            labyrinth[0][random.choice(sets[key])]['d'] = 0
    for x in range(width):
            if labyrinth[0][x]['d'] == -1:
               labyrinth[0][x]['d'] = 1

    for y in range(1,height):
        labyrinth.append([])
        for i in range(width):
            labyrinth[y].append({'r':labyrinth[y-1][i]['r'], 'd':labyrinth[y-1][i]['d'], 'set':labyrinth[y-1][i]['set']})
        for x in range(width):
            labyrinth[y][x]['r'] = -1
            if labyrinth[y][x]['d'] == 1:
                labyrinth[y][x]['set'] = -1
            labyrinth[y][x]['d'] = -1
        for x in range(width):
            if labyrinth[y][x]['set'] == -1:
                labyrinth[y][x]['set'] = x + y * width
        for x in range(width - 1):
            if labyrinth[y][x]['set'] == labyrinth[y][x+1]['set']:
                labyrinth[y][x]['r'] = 1
            else:
                if random.random() > right_density:
                    labyrinth[y][x]['r'] = 1
                else:
                    labyrinth[y][x]['r'] = 0
                    labyrinth[y][x+1]['set'] = labyrinth[y][x]['set']
        sets = sets_array(labyrinth[y])
        for key in sets:
            labyrinth[y][random.choice(sets[key])]['d'] = 0
        for x in range(width):
            if labyrinth[y][x]['d'] == -1:
               labyrinth[y][x]['d'] = 1
    for x in range(width-1):
        if labyrinth[height - 1][x]['set'] != labyrinth[height - 1][x + 1]['set']:
            labyrinth[height - 1][x]['r'] = 0
            labyrinth[height - 1][x+1]['set'] = labyrinth[height - 1][x]['set']
    return labyrinth

#~ a = create_labyrinth(100,100)
#~ pickle.dump(a, open('labyrinth', 'wb'))
a = pickle.load(open('labyrinth_backtrack', 'rb'))
#~ b = pickle.load(open('labyrinth_solution', 'rb'))
display_labyrinth(a)
