import pickle
import matplotlib.pyplot as plt

def ema_percent_envelope(function, sc, percent):
    sc = 2 / (sc+1)
    emas = [[], []]
    prev_ema = function[0]   
    for value in function[1:]:
        ema = sc * value + (1-sc) * prev_ema
        emas[1].append(prev_ema*(1-percent)) 
        emas[0].append(prev_ema*(1+percent))
        prev_ema = ema
    return emas        
        
buy_fee = 0.5
sell_fee = 1
adl = 100 #adl (average deal length) - средняя длина сделки, используется, чтобы не заключать сделки незадолго до конца дня
scs = [1.2] #sc (smoothing constant) - сглаживающая константа x / 10 for x in range(1, 10000)
pfes = [0.00001] #pfe (percent for envelope) - значение отклонения (в процентах) для процентного конверта
tntbs = [102] #tntb (time not to buy) - время в начале дня, когда не совершаются покупки

days = pickle.load(open('function_days', 'rb'))[365*0:10]
max_money = 0

for pfe in pfes:
    for sc in scs:
        for tntb in tntbs:
            money = 100000
            whole_function = []
            whole_emas = [[], []]
            whole_deals = []
            before_length = 0
            money_hist = []
            day_ends = [[], []]

            for day in days:
                deals = []
                emas = ema_percent_envelope(day, sc, pfe)
                in_deal = 0
                
                for i in range(len(day)):
                    if in_deal:
                        deal_closing = 0
                        if ((day[i] <= emas[0][i] and day[i-1] > emas[0][i-1]) or i == len(day) - 1) and deal_type == 'long':             
                            money *= day[i] / buy_value
                            deal_closing = 1
                        elif ((day[i] >= emas[0][i] and day[i-1] < emas[0][i-1]) or i == len(day) - 1) and deal_type == 'short':     
                            money *= buy_value / day[i]
                            deal_closing = 1
                            
                
                        if deal_closing:
                            in_deal = 0
                            money -= sell_fee
                            deals[-1][0].append(i)
                            deals[-1][1].append(day[i])
                            if start_money <= money:
                                deals[-1][2] = 1
                
                    if not in_deal and i > tntb and len(day) - i > adl:
                        deal_opening = 0
            
                        if day[i] >= emas[1][i] and day[i-1] < emas[1][i-1]:
                            deal_type = 'long'
                            deal_opening = 1
                        elif day[i] <= emas[1][i] and day[i-1] > emas[1][i-1]:
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
                whole_emas[0].extend(emas[0])
                whole_emas[1].extend(emas[1])
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
            
            if money > max_money * 0.999:
                if money > max_money:
                    max_money = money
                print('Деньги: {}, sc: {}, pfe: {}, tntb: {}.'.format(money, sc, pfe, tntb))
            plt.subplot(2,1,1)
            for deal in whole_deals:
                if deal[2]:
                    plt.plot(deal[0], deal[1], 'g')
                else:
                    plt.plot(deal[0], deal[1], 'r')
            plt.plot(list(range(len(whole_emas[0]))), whole_emas[0], 'y')
            plt.plot(list(range(len(whole_emas[1]))), whole_emas[1], 'y')
            plt.plot(list(range(len(whole_function))), whole_function, 'b')
            plt.plot(day_ends[0], day_ends[1], 'rs')
            plt.subplot(2,1,2)
            plt.plot(money_hist, color = 'g')