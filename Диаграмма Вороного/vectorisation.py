def alloc_lines(bitmap, monochrome = 0):
    from copy import deepcopy
    horisontal_bitmap = []
    for x in range(len(bitmap)):
        horisontal_bitmap.append([])
        for y in range(len(bitmap[0])):
            horisontal_bitmap[x].append((255,255,255))
    vertical_bitmap = deepcopy(horisontal_bitmap)

    bad_pattern = {(-1,0):(0,0,0), (0,1):(0,0,0), (1,0):(255,255,255), (1,-1):(255,255,255)}

    for x in range(len(bitmap)):
        for y in range(len(bitmap[0])-1):
            if bitmap[x][y] != bitmap[x][y+1]:
                vertical_bitmap[x][y] = (0,0,0)

    for y in range(len(bitmap[0])):
        for x in range(len(bitmap) - 1):
            if bitmap[x][y] != bitmap[x+1][y]:
                horisontal_bitmap[x][y] = (0,0,0)

    for x in range(len(bitmap)):
        for y in range(len(bitmap[0])):
            if vertical_bitmap[x][y] == (0,0,0):
                horisontal_bitmap[x][y] = (0,0,0)


    for x in range(1, len(bitmap)-1):
        for y in range(1, len(bitmap[0])-1):
            whiten = 1
            for key in bad_pattern:
                if horisontal_bitmap[x+key[0]][y+key[1]] != bad_pattern[key]:
                    whiten = 0
            if whiten == 1:
                horisontal_bitmap[x][y] = (255,255,255)

    return horisontal_bitmap


def make_line_objects(bitmap): #bw bitmap
    def to_binary(bitmap):
        for x in range(len(bitmap)):
            for y in range(len(bitmap[0])):
                if bitmap[x][y] == (0,0,0):
                    bitmap[x][y] = 1
                else:
                    bitmap[x][y] = 0
        return bitmap

    patterns = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]
    lines = []
    bitmap = to_binary(bitmap)


    #def appr_eq(value0, value1):
        #max_diff = 0.05
        #if value1 * (1-max_diff) < value0 < value1 * (1+max_diff):
            #return True
        #else:
            #return False

    #def check_dot(dot):
        #start_dot = lines[len(lines)-1]['start']
        #start_k = lines[len(lines)-1]['k']
        #k = (start_dot[0] - dot[0]) / (start_dot[1] - dot[1])
        #if appr_eq(k, start_k):
            #lines[len(lines)-1]['k'] = k
            #return 1
        #else:
            #del lines[len(lines)-1]['k']
            #lines[len(lines)-1]['end'] = dot
            #lines.append()
            #return 0

    tobreak = 0
    for x in range(len(bitmap)):
        for y in range(len(bitmap[0])):
            if bitmap[x][y] == 1:
                coords = (x,y)
                tobreak = 1
                break
        if tobreak == 1:
            break

    import time
    lines = [[coords]]
    bitmap[coords[0]][coords[1]] = 0
    finished = 0
    node_coords = []
    pre_node  = 0
    while not finished:
        count = 0
        for pattern in patterns:
            try:
                if bitmap[coords[0]+pattern[0]][coords[1]+pattern[1]] == 1:
                    count += 1
                    if count == 1:
                        coords = coords[0]+pattern[0], coords[1]+pattern[1]
            except:
                pass
        print(coords, count)
        if count >= 3:
            #if pre_node == 1:
            print('node')
            lines[len(lines)-1].append(coords)
            lines.append([coords])
            node_coords.append(coords)
                #pre_node = 0
            #else:
                #pre_node = 1

        elif count == 0:
            print('dead end')
            bitmap[coords[0]][coords[1]] = 0
            lines[len(lines)-1].append(coords)
            if len(node_coords) > 0:
                coords = node_coords.pop()
            else:
                finished = 1
        else:
            bitmap[coords[0]][coords[1]] = 0

    return lines

