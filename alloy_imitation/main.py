import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

def energy(path):
    return sum(math.hypot(path[i][0] - path[i+1][0], path[i][1] - path[i+1][1]) for i in range(len(path)-1)) + \
     math.hypot(path[0][0] - path[-1][0], path[0][1] - path[-1][1])

def swap_cities(path):
    new_path = path.copy()
    i, j = random.randint(0, len(path) - 1), random.randint(0, len(path) - 1)
    new_path[i], new_path[j] = new_path[j], new_path[i]
    return new_path

def inverse_path_between_cities(path):
    i, j = random.randint(0, len(path) - 1), random.randint(0, len(path) - 1)
    if i > j: i, j = j, i

    new_path = path.copy()
    new_path[i:j] = list(reversed(new_path[i:j]))

    return new_path

def find_maximum_simulated_annealing(func, start, neighbor_func, difference_func, temp=100):
    '''
        func - функция, максимум который надо найти
        start - первый попробованный аргумент
        neighbor_func - функция, принимающая аргумент и возвращающая близкий к нему аргумент
        difference_func - функция,
    '''

    current_coord = start
    while temp > 0:
        temp -= 1
        working_coord = neighbor(current_coord)

def optimize_path_simple(path, max_iter_time=1):
    current_path = path
    current_energy = energy(path)

    t = time.perf_counter()
    while True:
        new_path = inverse_path_between_cities(current_path)
        new_energy = energy(new_path)

        if time.perf_counter() > t + max_iter_time:
            break

        if new_energy < current_energy:
            current_path = new_path
            current_energy = new_energy
            print(time.perf_counter() -t)
            t = time.perf_counter()

    return current_path

def optimize_path_simulated_annealing(path, temp=10, min_temp = 0.00001):

    def transition_probability(e, t):
        return np.exp(-e / t)

    def decreased_temp(temp, i):
        #~ return temp * 0.1 / i
        return temp * 0.999

    current_path = path
    current_energy = energy(path)

    for i in range(1, 100000):

        new_path = inverse_path_between_cities(current_path)
        new_energy = energy(new_path)

        if new_energy < current_energy:
            current_path = new_path
            current_energy = new_energy

        elif transition_probability(new_energy - current_energy, temp) > random.uniform(0, 1):
            current_path = new_path
            current_energy = new_energy


        temp = decreased_temp(temp, i)

        print(temp)

        if temp < min_temp:
            break

    return current_path


cities = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(100)]
path = cities; random.shuffle(path)

path = optimize_path_simple(path)
print('Path energy is: {}'.format(energy(path)))
#~ path = optimize_path_simulated_annealing(path)


line = plt.Line2D(*zip(*path))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.add_line(line)

plt.scatter(*zip(*cities))

#~ plt.add_line(line)
plt.show()
