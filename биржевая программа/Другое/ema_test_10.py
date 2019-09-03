import pickle
#import matplotlib.pyplot as plt

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

buy_fee = 1
sell_fee = 0.5
spread_loss = 0.99992 #spread loss -
adls = [102] #adl (average deal length) - средняя длина сделки, используется, чтобы не заключать сделки незадолго до конца дня
scs = [22] #sc (smoothing constant) - сглаживающая константа
tntbs = [100] #tntb (time not to buy) - время в начале дня, когда не совершаются покупки, т.к. сглаживающая линия рассчитывается по малому кол-ву значений
nsps = [20] #nsp (not sell period) - время после начала сделки, когда мы не продаём
mcs = [0.0001] #mc (margin call) - убыток в пунктах, после которого надо продавать


days = pickle.load(open('function_days', 'rb'))[:100]
log = open('log.txt', 'a')
max_money = 0

for mc in mcs:
    for nsp in nsps:
        for adl in adls:
            for sc in scs:
                for tntb in tntbs:
                    money = 100000
                    whole_function = []
                    whole_emas = []
                    whole_deals = []
                    before_length = 0
                    money_hist = []
                    day_ends = [[], []]

                    for day in days:
                        deals = []
                        emas = ema(day, sc)
                        in_deal = 0

                        for i in range(len(day)):
                            if in_deal:
                                est_money = money * spread_loss - sell_fee
                                if (day[i] <= emas[i] and day[i-1] > emas[i-1] and buy_time + nsp <= i) or i == len(day) - 1 or (deal_type == 'long' and est_money < start_money - mc * start_money) or (deal_type == 'short' and est_money > start_money + mc * start_money):

                                    print(est_money - start_money - mc * start_money, deal_type)
                                    if deal_type == 'long':
                                        money *= day[i] / buy_value
                                    else:
                                        money *= buy_value / day[i]
                                    in_deal = 0
                                    money *= spread_loss
                                    money -= sell_fee
                                    deals[-1][0].append(i)
                                    deals[-1][1].append(day[i])
                                    if start_money <= money:
                                        deals[-1][2] = 1




                            if not in_deal and i > tntb and len(day) - i > adl:
                                deal_opening = 0

                                if day[i] >= emas[i] and day[i-1] < emas[i-1]:
                                    deal_type = 'long'
                                    deal_opening = 1
                                elif day[i] <= emas[i] and day[i-1] > emas[i-1]:
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
                    #log.write('Деньги: {}, sc: {}, tntb: {}, adl: {}.\n'.format(money, sc, tntb, adl))
                    #log.flush()

                    #plt.subplot(2,1,1)
                    #for deal in whole_deals:
                        #if deal[2]:
                            #plt.plot(deal[0], deal[1], 'g')
                        #else:
                            #plt.plot(deal[0], deal[1], 'r')
                    #plt.plot(list(range(len(whole_emas))), whole_emas, 'y')
                    #plt.plot(list(range(len(whole_function))), whole_function, 'b')
                    #plt.plot(day_ends[0], day_ends[1], 'rs')
                    #plt.subplot(2,1,2)
                    #plt.plot(money_hist, color = 'g')
                    #print(money)
                    pickle.dump(money_hist, open('money_hist', 'wb'))
