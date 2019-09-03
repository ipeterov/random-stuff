import pickle
import matplotlib.pyplot as plt
from numpy import arange

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

def trix(function, sc):
    trixs = []    
    emas = ema(function, sc)
    dmas = ema(emas, sc)
    tmas = ema(dmas, sc)
    prev_value = tmas[0]
    for value in tmas[1:]:
        trixs.append((value - prev_value) / prev_value * 100)
        prev_value = value
    return trixs
    
        
buy_fee = 1
sell_fee = 0.5
spread_loss = 0.99992
scs = [x for x in range(1000)] #sc (smoothing constant) - сглаживающая константа 37.3
sls = [0.00354] #sl (signal line) - сигнальная линия, при пересечении которой графиком trix совершаются дейтвия 

days = pickle.load(open('function_days', 'rb'))[:]
log = open('log.txt', 'a')
max_money = 0




for sl in sls:
    for sc in scs:
        money = 100000
        whole_function = []
        whole_trixs = []
        whole_deals = []
        before_length = 0
        money_hist = []
        day_ends = [[], []]
        for day in days:
            deals = []
            trixs = trix(day, sc)
            day = day[4:]
            in_deal = 0
            
            for i in range(1, len(day)):
                if in_deal:
                    deal_closing = 0
                    if i == len(day) - 1 or (deal_type == 'long' and trixs[i-1] > sl and trixs[i] <= sl) or (deal_type == 'short' and trixs[i-1] < sl and trixs[i] >= sl):
                        if deal_type == 'long':
                            deal_closing = 1
                            money *= day[i] / buy_value
                        elif deal_type == 'short':
                            deal_closing = 1
                            money *= buy_value / day[i]
                    
                    if deal_closing:
                        in_deal = 0
                        money *= spread_loss
                        money -= sell_fee
                        deals[-1][0].append(i)
                        deals[-1][1].append(day[i])
                        if start_money <= money:
                            deals[-1][2] = 1
                            
         
        
            
                if not in_deal:
                    deal_opening = 0
                    if trixs[i-1] < sl and trixs[i] >= sl:
                        deal_type = 'long'
                        deal_opening = 1
                    elif trixs[i-1] > sl and trixs[i] <= sl:                      
                        deal_type = 'short'
                        deal_opening = 1  
        
                    if deal_opening:
                        buy_time = i
                        buy_value = day[i]
                        in_deal = 1
                        start_money = money
                        deals.append([[],[],0])
                        deals[-1][0].append(i)
                        deals[-1][1].append(buy_value)
                        money *= spread_loss
                        money -= buy_fee

                money_hist.append(money)
                
            whole_function.extend(day)
            whole_trixs.extend(trixs)
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
        log.write('Деньги: {}, sc: {}, sl: {}.\n'.format(money,sc,sl))
        log.flush()
        
#        plt.subplot(3,1,1)
#        for deal in whole_deals:
#            if deal[2]:
#                plt.plot(deal[0], deal[1], 'g')
#            else:
#                plt.plot(deal[0], deal[1], 'r')
#        plt.plot(list(range(len(whole_function))), whole_function, 'b')
#        plt.plot(day_ends[0], day_ends[1], 'rs')
#        plt.subplot(3,1,2)
#        plt.plot(whole_trixs)
#        plt.subplot(3,1,3)
#        plt.plot(money_hist, color = 'g')
        print(money)