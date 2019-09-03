import pickle

def ama(function, f, s, n):
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
            volatility = float(volatility.std())
            try:
                eff_ratio = direction / volatility
            except:
                eff_ratio = 1
            #eff_ratio = 1/eff_ratio
            sc = eff_ratio * (fastest - slowest) + slowest
            ama = sc * function[i] + (1-sc) * prev_ama
            amas.append(ama)
            prev_ama = ama
        else:
            prev_ama = function[i+n+1]
            tocontinue = n
    return amas

def filter_kauf(amas, d, k):
    import numpy as np
    filters = []
    for i in range(d, len(amas)):
        ama_changes = []
        for j in range(i-d+1, i):
            ama_changes.append(amas[j] - amas[j-1])
        omega = np.array(ama_changes)
        omega = float(omega.std())
        filters.append(k * omega)
        
        
        

in_deal = 0
money = 100000
buy_fee = 0
sell_fee = 0
average_deal_length = 50
f = 315; s = 315; n = 22

function = pickle.load(open('function', 'rb'))[:16290]
amas = ama(function, f, s, n)
function = function[n:]
deals = []
money_values = []
buy_value = 0
start_money = money
deal_type = 'none'
deal_lengths = []

for i in range(1, len(function) - 100):
    if in_deal:
        deal_closing = 0
        if function[i] == None:
            if deal_type == 'long':                
                money *= function[i-1] / buy_value
            elif deal_type == 'short':
                money *= buy_value / function[i-1]
            deal_closing = 1
        elif function[i] <= amas[i] and function[i-1] > amas[i-1] and deal_type == 'long':             
            money *= function[i] / buy_value
            deal_closing = 1
        elif function[i] >= amas[i] and function[i-1] < amas[i-1] and deal_type == 'short':     
            money *= buy_value / function[i]
            deal_closing = 1

        if deal_closing:
            in_deal = 0
            money -= sell_fee
            deals[-1]['xcoords'].append(i)
            deals[-1]['ycoords'].append(function[i])
            if start_money < money:
                deals[-1]['profitable'] = 1
            deal_lengths.append(i - deals[-1]['xcoords'][0])

    if not in_deal and None not in function[i-1: i+average_deal_length]:
        deal_opening = 0
        if function[i] >= amas[i] and function[i-1] < amas[i-1]:
            deal_type = 'long'
            deal_opening = 1
        elif function[i] <= amas[i] and function[i-1] > amas[i-1]:
            deal_type = 'short'
            deal_opening = 1  
        if deal_opening:
            buy_value = function[i]
            in_deal = 1
            start_money = money
            deals.append({'xcoords' : [], 'ycoords' : [], 'profitable' : 0, 'deal_length' : 0})
            deals[-1]['xcoords'].append(i)
            deals[-1]['ycoords'].append(buy_value)
            money -= buy_fee
    money_values.append(money)

money_speed = []
prev_value = money_values[0]
for value in money_values:
    money_speed.append(value-prev_value)
    prev_value = value

print(money)
import matplotlib.pyplot as plt

plt.subplot(2,1,1)
for deal in deals:
    if deal['profitable']:
        plt.plot(deal['xcoords'], deal['ycoords'], 'y')
    else:
        plt.plot(deal['xcoords'], deal['ycoords'], 'r')
plt.plot(list(range(len(function))), function, 'b')
plt.plot(list(range(len(amas))), amas, 'g')
plt.ylabel('Value')
plt.xlabel('Minute')

plt.subplot(2,1,2)
plt.plot(money_values, color = 'g')

plt.show()

        
        


