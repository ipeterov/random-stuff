# coding: utf-8

from math import factorial

import matplotlib.pyplot as plt
import numpy as np


def get_prob_of_conv_being_lower(converted, total, conversion):
    prob = 0
    for i in range(converted + 1):
        set_probability = conversion**i * (1 - conversion)**(total - i)
        mutation_count = (factorial(total) / factorial(total - i)) / factorial(i)
        prob += set_probability * mutation_count
    return prob


def get_prob_of_conv_being_between(conv1, conv2, converted, total):
    prob1 = get_prob_of_conv_being_lower(converted, total, conv1)
    prob2 = get_prob_of_conv_being_lower(converted, total, conv2)
    return abs(prob1 - prob2)


def get_distribution(total, converted, resolution=100):
    space = np.linspace(0, 1, num=resolution)
    points = []
    for i, val in enumerate(space[:-1]):
        next_val = space[i + 1]
        prob = get_prob_of_conv_being_between(val, next_val, converted, total)
        points.append(prob)
    return space[:-1], points


total = int(input('Кликов: '))
converted = int(input('Конверсий: '))
resolution = 1000

print get_prob_of_conv_being_between(0, 0.01, converted, total)

space, points = get_distribution(total, converted, resolution)
plt.plot(space, points)
plt.show()
