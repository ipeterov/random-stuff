import pickle
import matplotlib.pyplot as plt

def ema(function, sc):
    sc = 2 / (sc+1)
    emas = []
    prev_ema = function[0]
    emas.append(function[0])
    for value in function[1:]:
        ema = sc * value + (1-sc) * prev_ema
        emas.append(ema)
        prev_ema = ema
    return emas


def getlever(money, reliability):
    """
        money - массив значений количества денег (в рублях) на множество моментов времени
        Желаемая надёжность (reliability) измеряется в вероятности проигрыша за 1 сделку
    """
    jumps = {}
    for i in range(len(money)-1):
        val = abs(round(money[i+1] - money[i], 0))
        if val == 0:
            continue
        if val in jumps:
            jumps[val] += 1
        else:
            jumps[val] = 1

    jumps = list(jumps.items())
    jumps.sort(key = lambda x: x[0])

    return jumps

result = getlever(pickle.load(open('money_hist', 'rb')), 'spam')

jumps, counters = zip(*result)
counters = ema(counters, 100)
plt.plot(jumps, counters)
plt.show()
