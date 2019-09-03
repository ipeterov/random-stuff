import random
import matplotlib.pyplot as plt

dot_count = 200

def make_more_even(dots, coeff=0.5):
    dots.sort(key=lambda dot: dot[0])
    min_x, max_x = min(dots, key=lambda dot: dot[0])[0], max(dots, key=lambda dot: dot[0])[0]
    new_dots = []

    for i, dot in enumerate(dots):
        proper_place = min_x + (max_x - min_x) * i / (len(dots) - 1)
        new_dots.append((dot[0] + (proper_place - dot[0]) * coeff, dot[1]))

    return new_dots



def evenize(dots, coeff=0.5):

    def evenize_1d(coords):
        min_coord, max_coord = min(coords), max(coords)
        coords_sorted = sorted(coords)

        for i, coord in enumerate(coords_sorted):
            proper_place = min_coord + (max_coord - min_coord) * i / (len(coords_sorted) - 1)
            coords[coords.index(coord)] = coord + (proper_place - coord) * coeff

        return coords

    new_coords = []

    for coords in zip(*dots):
        coords = list(coords)
        new_coords.append(evenize_1d(coords))

    return zip(*new_coords)


def plot(dotsets):
    colors = ['red', 'blue', 'yellow', 'green', 'black']
    for dots in dotsets:
        color = colors.pop(0)
        for dot in dots:
            plt.scatter(*dot, color=color)
    plt.show()




dots = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(dot_count)]
#~ dots_iter_1 = make_more_even(dots)
dots_iter_1 = evenize(dots, coeff=1)

plot((dots, dots_iter_1))
