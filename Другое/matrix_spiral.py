N = 10
START = (0, 0)
DIRECTIONS = list(reversed([(0, 1), (1, 0), (0, -1), (-1, 0)]))


matrix = [[None for _ in range(N)] for _ in range(N)]
position = START
direction_i = 0
number = 0
matrix[position[0]][position[1]] = number
while True:
    new_position = [position[i] + DIRECTIONS[direction_i][i] for i in range(len(position))]
    if new_position[0] in range(0, N) and new_position[1]  in range(0, N) and matrix[new_position[0]][new_position[1]] == None:
        position = new_position
        number += 1
        matrix[position[0]][position[1]] = number

    else:
        if direction_i == 3:
            direction_i = 0
        elif direction_i < 3:
            direction_i += 1
        new_position = [position[i] + DIRECTIONS[direction_i][i] for i in range(len(position))]
        if matrix[new_position[0]][new_position[1]] != None:
            break
    
for row in matrix:
    print(*row, sep='\t')
    
