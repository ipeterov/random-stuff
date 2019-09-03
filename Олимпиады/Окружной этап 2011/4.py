for x in range(3):
    for y in range(3):
        if matrix[x][y] == 9:
            startcoords = x,y

while True:
    maxnext = 0
    nextmove = None
    for i in (-1,0,1):
        for j in (-1,0,1):
            if matrix[startcoords[0]+i][startcoords[1]+j] > maxnext:
                maxnext = matrix[startcoords[0]+i][startcoords[1]+j]
                nextmove = i, j
