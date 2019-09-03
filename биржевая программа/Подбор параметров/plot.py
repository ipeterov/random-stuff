import matplotlib.pyplot as plt
import numpy
from math import *

def example(x):
    return sin(x) / x**(1.001)

def timerow(function, range1, step):
    result = []    
    for i in numpy.arange(range1[0], range1[1], step):
        result.append([i, function(i)])
    return result

plt.plot(*list(zip(*timerow(example, [-100,100], 0.01))))