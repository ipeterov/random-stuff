import math, numpy

def getext(function, step1, range2, onlymax = 0):
    timerow = []
    exts = []
    for i in numpy.arange(range2[0], range2[1], step1):
        timerow.append([i, function(i)])
    
    for i in range(1, len(timerow) - 2):
        if timerow[i-1][1] < timerow[i][1] > timerow[i+1][1]:
            exts.append(timerow[i][0])
        elif timerow[i-1][1] > timerow[i][1] < timerow[i+1][1] and not onlymax:
            exts.append(i)
    return exts

def get_acceptable_step(function, range1, step, example_range = 1/5):
    range2 = [range1[0], int((range1[1]-range1[0]) * example_range + range1[0])]
    needed_ext_count = len(countext(function, step, range2))
    for newstep in range(int((range1[1]-range1[0]) / 2), step):
        if len(countext(function, newstep, range2)) >= needed_ext_count:
            return newstep
    else:
        return step

def get_all_maxs(function, step, goodstep, range1):
    def binfindmax(range1):
        while True:
            point = sum(range1) / 2
            print(function(point - goodstep), function(point), function(point + goodstep), point - goodstep, point, point + goodstep)
            if function(point - goodstep) <= function(point) >= function(point + goodstep) or range1[0] == range1[1]:
                return point
            elif function(point - goodstep) < function(point) < function(point + goodstep):
                range1 = [point, range1[1]]        
            elif function(point - goodstep) > function(point) > function(point + goodstep):
                range1 = [range1[0], point]            
    result = []
    exts = getext(function, step, range1, onlymax = 1)
    for i in range(len(exts)):
        exts[i] = [exts[i] - step, exts[i] + step]
    for range2 in exts:
        result.append(binfindmax(range2))
    return result

def example(x):
    return -(x**2) + 200 * math.sin(0.5 * x)

print(get_all_maxs(example, 1, 0.001, [-10, 10]))
    