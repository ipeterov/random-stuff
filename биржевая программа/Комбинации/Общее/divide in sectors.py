from pickle import *
import math
sectors_count = 5
function_t = load(open('function_1', 'rb'))
function = function_t
#for item in function_t:
    #function.append(float(item.strip('\n')))
sectors = []
for i in range(sectors_count + 1):
    sectors.append(function[int(round(len(function) / sectors_count * (i - 1), 0)):int(round(len(function) / sectors_count * i, 0))])
dump(sectors, open('sectors','wb'))
