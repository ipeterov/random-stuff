from math import *
from pickle import *

width = 100
height = 100

dists = {}
for x in range(int(-width/2), int(width/2)):
    for y in range(int(-height/2), int(height/2)):
        dist = sqrt(x**2 + y**2)
        try:
            dists[dist].append((x,y))
        except:
            dists[dist] = [(x,y)]

keys = list(dists.keys())
keys.sort()

array = []
for key in keys:
    array += dists[key]


dump(tuple(array), open('patterns', 'wb'))
