n, t = [int(x) for x in input().split()]

square = []
for h in range(n):
    square.append([int(x) for x in input().split()])

def tick(square):
    def countNeighbours(i, j):
        counter = 0
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if (not (x == y == 0)) and (0 <= i+x < n) and (0 <= j+y < n):
                    if square[i+x][j+y] == 1:
                        counter += 1
        return counter

    changes = []
    for a in range(n):
        for b in range(n):
            neighbourCount = countNeighbours(a, b)
            #print('Square [{}, {}] has {} neighbours.'.format(a,b,neighbourCount))
            if neighbourCount < 2:
                changes.append((a, b, 0))
                #print('    Square [{}, {}] set 0 cause was lonely.'.format(a,b))
            elif neighbourCount > 3:
                changes.append((a, b, 0))
                #print('    Square [{}, {}] set 0 cause was crowded.'.format(a,b))
            elif neighbourCount == 3 and square[a][b] == 0:
                changes.append((a, b, 1))
                #print('    Square [{}, {}] set 1 cause was infected.'.format(a,b))
    for change in changes:
        square[change[0]][change[1]] = change[2]

for i in range(t):
    tick(square)
    #print("##################################")
print(square)
