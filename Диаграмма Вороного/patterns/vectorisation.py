def alloc_lines(bitmap, monochrome = 0):
    from copy import deepcopy

    patterns = [(0,1), (0,-1), (1,0), (-1,0)]
    edgecolor = (0,0,0)
    maincolor = (255,255,255)
    source_bitmap = deepcopy(bitmap)

    for x in range(len(bitmap)):
        for y in range(len(bitmap[0])):
            blacken = 0
            for pattern in patterns:
                try:
                    if source_bitmap[x+pattern[0]][y+pattern[1]] != source_bitmap[x][y]:
                        blacken = 1
                except:
                    pass
            if blacken:
                bitmap[x][y] = edgecolor

    if monochrome:
        for x in range(len(bitmap)):
            for y in range(len(bitmap[0])):
                if bitmap[x][y] != edgecolor:
                    bitmap[x][y] = maincolor
    return bitmap
