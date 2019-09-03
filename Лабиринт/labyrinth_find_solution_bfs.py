import labyrinth_lib, pickle
from queue import *

def find_path_bfs(my_labyrinth, goal = None, start = (0,0)):

    if not goal:
        goal = my_labyrinth.size[0] - 1, my_labyrinth.size[1] - 1

    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():

        current = frontier.get()

        if current == goal:
            break

        for next_coords in my_labyrinth.near_passable_coords(current):
            if next_coords not in came_from:
                frontier.put(next_coords)
                came_from[next_coords] = current

    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)

    return path

name = 'labyrinth_backtrack'
labyrinth = labyrinth_lib.labyrinth_object()
labyrinth.init_from_labyrinth(pickle.load(open(name, 'rb')))

path = find_path_bfs(labyrinth)

labyrinth.display(path)
