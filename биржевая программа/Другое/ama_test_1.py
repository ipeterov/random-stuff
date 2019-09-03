import pickle
import matplotlib.pyplot as plt

def ama(function, f, s, first_sc, n):
    def vol(function, sc):
        def ema(function, sc):
            sc = 2 / (sc+1)
            emas = []
            prev_ema = function[0]
            emas.append(prev_ema)
            for i in range(1, len(function)):
                if function[i] != None:
                    ema = sc * function[i] + (1-sc) * prev_ema
                    prev_ema = ema            
                    emas.append(prev_ema)
                else:
                    prev_ema = function[i+1]
            return emas
        emas = ema(function, sc)
        diffs = [abs(i - ema_val) for i in function for ema_val in emas]
        return sum(diffs)

    amas = []
    prev_ama = function[0]
    fastest = 2 / (f+1)
    slowest = 2 / (s+1)
    tocontinue = 1
    prev_sc = first_sc

    for i in range(n, len(function)):
        if tocontinue:
            amas.append(function[i])
            tocontinue -= 1
            continue
        if None not in function[i-n-1: i+1]:         
            direction = abs(function[i] - function[i-n-1])
            volatility = vol(function[i-n-1: i], prev_sc)
            try:
                eff_ratio = direction / volatility
            except:
                eff_ratio = 1
            eff_ratio = 1
            sc = eff_ratio * (fastest - slowest) + slowest
            ama = sc * function[i] + (1-sc) * prev_ama
            amas.append(ama)
            prev_sc = sc
            prev_ama = ama
        else:
            prev_ama = function[i+n+1]
            tocontinue = n
    return amas


in_deal = 0
money = 100000
buy_fee = 0.5
sell_fee = 1
average_deal_length = 4
f = 100; s = 360; n = 22
first_sc = (f+s)/2

function = pickle.load(open('function', 'rb'))[:20000]
amas = ama(function, f, s, first_sc, n)
#amas = ama(function, 100, 360, , n)
function = function[n:]
deals = []
money_values = []
buy_value = 0
start_money = money
deal_type = 'none'
deal_lengths = []
in_deal = 0
deal_just_closed = 0

for i in range(1, len(function) - 300):
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
            deal_just_closed = 1

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

plt.subplot(2,1,1)
for deal in deals:
    if deal['profitable']:
        plt.plot(deal['xcoords'], deal['ycoords'], 'g')
    else:
        plt.plot(deal['xcoords'], deal['ycoords'], 'r')
plt.plot(list(range(len(function))), function, 'b')
plt.plot(list(range(len(amas))), amas, 'y')
plt.ylabel('Value')
plt.xlabel('Minute')

plt.subplot(2,1,2)
plt.plot(money_values, color = 'g')

plt.show()

        
        


