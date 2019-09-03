import random, math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def game_round():
    
    c = 0
    
    while True:
        if random.randint(0,1) == 0:
            c += 1
        else:
            break
    
    return 2**c

def average(cycle_count):
    
    s = 0
    
    for i in range(cycle_count):
        s += game_round()
        
    return s / cycle_count

def average_hist(cycle_count, av_cycle_count):
    
    results = []
    
    while cycle_count:
        result = average(av_cycle_count)
        if result < 50:
            results.append(result)
            cycle_count -= 1
    
    return results

def game_distribution(cycle_count):
    
    results = {}
    
    for i in range(cycle_count):
        result = game_round()
        if result in results:
            results[result] += 1
        else:
            results[result] = 1
    
    results = list(results.items())
    results.sort(key = lambda x: x[0])
    results = [x[1] for x in results]
    
    return results
    
    
x = average_hist(1000,1000)
    
num_bins = 200
# the histogram of the data
n, bins, patches = plt.hist(x, num_bins, facecolor='green')

plt.show() 
    



