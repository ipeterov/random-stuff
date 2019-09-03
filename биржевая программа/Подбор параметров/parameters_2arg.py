import math, numpy

def getmax(function, step, goodstep, rangev, rangeh): #step и goodstep в процентах

    def get_acceptable_step(example_scale = 1/5):
        '''Определяет среднее расстояние между экстремумами. На основании этого возвращает step, необходимый для того,
        чтобы не упустить больше 95% экстремумов.'''
        example_zone
        range2 = [range1[0], int((range1[1]-range1[0]) * example_range + range1[0])]
        needed_ext_count = len(countext(function, step, range2))
        for newstep in range(int((range1[1]-range1[0]) / 2), step):
            if len(countext(function, newstep, range2)) >= needed_ext_count:
                return newstep
        else:
            return step
        for x in range

    def getextzones(step, onlymax = 0): #step в процентах от range
        values = []
        stepv = (rangev[1] - rangev[0]) * step
        steph = (rangeh[1] - rangeh[0]) * step
        for x in numpy.arange(rangev[0], rangev[1], stepv):
            values.append([])
            for y in numpy.arange(rangeh[0], rangeh[1], steph):
                values[-1].append([[x,y], function(x,y)])
        extzones = []
        for i in range(1, len(values) - 1):
            for j in range(1, len(values[0]) - 1):
                isextremum = 1
                for ai in [-1,1]:
                    for aj in [-1,1]:
                        if values[i][j][1] < values[i+ai][j+aj][1]:
                            isextremum = 0
                if isextremum:
                    extzones.append([[values[i][j][0][0] - stepv, values[i][j][0][0] + stepv], [values[i][j][0][1] - steph, values[i][j][0][1]] + steph])
        return extzones

    def binfindmax(rangev, rangeh):
        goodstepv = (rangev[1] - rangev[0]) * goodstep
        goodsteph = (rangeh[1] - rangeh[0]) * goodstep
        while True:
            pointv = (rangev[1] - rangev[0]) / 2 + rangev[0]
            pointh = (rangeh[1] - rangeh[0]) / 2 + rangeh[0]
            val = function(pointv, pointh)
            vald = function(pointv - goodstepv, pointh)
            valu = function(pointv + goodstepv, pointh)
            valr = function(pointv, pointh + goodsteph)
            vall = function(pointv, pointh - goodsteph)

            if vall < val > valr and vald < val > valu:
                return pointv, pointh, val

            if vall < val < valr:
                rangev = [pointv, rangev[1]]
            elif vall > val > valr:
                rangev = [rangev[1], pointv]

            if vald < val < valu:
                rangeh = [pointh, rangeh[1]]
            elif vald > val > valu:
                rangeh = [rangeh[1], pointh]

    result = []
    acceptable_step = get_acceptable_step()
    extzones = getextzones(acceptable_step, onlymax = 1)
    for extzone in extzones:
        result.append(binfindmax(extzone[0], extzone[1]))
    return result


def example(x):
    return -(x**2) + 200 * math.sin(0.5 * x)

print(getmax(example, 1, 0.001, [-10, 10]))
