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
        
money = 100000
buy_fee = 0.5
sell_fee = 1
average_deal_length = 10
sc = 1.2

days = pickle.load(open('function_days', 'rb'))[:10]
whole_function = []
whole_emas = []
whole_deals = []
before_length = 0
money_hist = []
day_ends = [[], []]
start_money = money


for day in days:
    deals = []
    emas = ema(day, sc)
    in_deal = 0
    
    for i in range(len(day)):
        if in_deal:
            deal_closing = 0
            if ((day[i] <= emas[i] and day[i-1] > emas[i-1]) or i == len(day) - 1) and deal_type == 'long':             
                money *= day[i] / buy_value
                deal_closing = 1
            elif ((day[i] >= emas[i] and day[i-1] < emas[i-1]) or i == len(day) - 1) and deal_type == 'short':     
                money *= buy_value / day[i]
                deal_closing = 1
                
    
            if deal_closing:
                in_deal = 0
                money -= sell_fee
                deals[-1][0].append(i)
                deals[-1][1].append(day[i])
                if start_money <= money:
                    deals[-1][2] = 1
    
        if not in_deal and i > 102:
            deal_opening = 0

            if day[i] >= emas[i] and day[i-1] < emas[i-1]:
                deal_type = 'long'
                deal_opening = 1
            elif day[i] <= emas[i] and day[i-1] > emas[i-1]:
                deal_type = 'short'
                deal_opening = 1  

            if deal_opening:
                buy_value = day[i]
                in_deal = 1
                start_money = money
                deals.append([[],[],0])
                deals[-1][0].append(i)
                deals[-1][1].append(buy_value)
                money -= buy_fee
        money_hist.append(money)
        
    whole_function.extend(day)
    whole_emas.extend(emas)
    day_ends[0].append(len(whole_function) -1)
    day_ends[1].append(whole_function[-1])
    for i in range(len(deals)):
        for j in range(2):
            try:
                deals[i][0][j] += before_length
            except:
                pass
    whole_deals.extend(deals)
    before_length += len(day)
    
print(money)

plt.subplot(2,1,1)
for deal in whole_deals:
    if deal[2]:
        plt.plot(deal[0], deal[1], 'g')
    else:
        plt.plot(deal[0], deal[1], 'r')
plt.plot(list(range(len(whole_emas))), whole_emas, 'y')
plt.plot(list(range(len(whole_function))), whole_function, 'b')
#plt.plot(day_ends[0], day_ends[1], 'rs')

plt.ylabel('Value')
plt.xlabel('Minute')
 
plt.subplot(2,1,2)
plt.plot(money_hist, color = 'g')
