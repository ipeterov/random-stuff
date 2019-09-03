def sma(function, n): #n - сглаживающий интервал
    mvf = [] #mvf - moving average function
    for i in range(n, len(function)):
        average = 0
        for j in range(n+1):
            average += function[i-j]
        average /= n+1
        mvf.append(average)
    return(mvf)

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

def ama(function, f = 25, s = 28, n = 20):
    import numpy as np
    amas = []
    prev_ama = function[0]
    fastest = 2 / (f+1)
    slowest = 2 / (s+1)
    tocontinue = 1

    for i in range(n, len(function)):
        if tocontinue:
            amas.append(function[i])
            tocontinue -= 1
            continue
        if function[i] != None and function[i-n-1] != None:
            direction = abs(function[i] - function[i-n-1])
            volatility = np.array(function[i-n: i])
            volatility = abs(float(volatility.std()))
            try:
                eff_ratio = direction / volatility
            except:
                eff_ratio = 1
            sc = eff_ratio * (fastest - slowest) + slowest
            ama = sc * function[i] + (1-sc) * prev_ama
            amas.append(ama)
            prev_ama = ama
        else:
            prev_ama = function[i+n+1]
            tocontinue = n
    return amas

def derivatives(function, n):        
    for i in range(n):        
        sub_function = []
        for j in range(len(function)-1):
            sub_function.append(function[j+1] - function[j])
        function = sub_function
    return function

import pickle
import matplotlib.pyplot as plt

test_timerow = pickle.load(open('function', 'rb'))[:500]
#plt.plot(test_timerow[4:], 'b')
plt.plot(derivatives(test_timerow, 1), 'b')
plt.plot(derivatives(test_timerow, 2)[1:], 'r')

plt.show()


