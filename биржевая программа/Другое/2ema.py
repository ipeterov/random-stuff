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

buy_fee = 0
sell_fee = 0
spread_loss = 0.99988 #spread loss -
adls = [50,200,400,800] #adl (average deal length) - средняя длина сделки, используется, чтобы не заключать сделки незадолго до конца дня
lscs = [10,30,100,300] #lsc (little smoothing constant) - сглаживающая константа на большом промежутке
bscs = [3,10,30,100,300] #bsc (big smoothing constant) - сглаживающая константа на маленьком промежутке
tntbs = [0,50,200] #tntb (time not to buy) - время в начале дня, когда не совершаются покупки, т.к. сглаживающая линия рассчитывается по малому кол-ву значений
nsps = [0,10,30,100,300] #nsp (not sell period) - время после начала сделки, когда мы не продаём
mcs = [0, 0.001, 0.003, 0.01, 0.03] #mc (margin call) - убыток в пунктах, после которого надо продавать


days = pickle.load(open('function_days', 'rb'))[:]
log = open('log.txt', 'a')
max_money = 0

for bsc in bscs:
    for mc in mcs:
        for nsp in nsps:
            for adl in adls:
                for lsc in lscs:
                    for tntb in tntbs:
                        money = 100000
                        whole_function = []
                        whole_lemas = []
                        whole_bemas = []
                        whole_deals = []
                        before_length = 0
                        money_hist = []
                        day_ends = [[], []]
                        deal_profits = []

                        for day in days:
                            deals = []
                            lemas = ema(day, lsc)
                            bemas = ema(day, bsc)
                            in_deal = 0

                            for i in range(len(day)):
                                if in_deal:
                                    est_money = money * spread_loss - sell_fee
                                    if (lemas[i] <= bemas[i] and lemas[i-1] > bemas[i-1] and buy_time + nsp <= i) or i == len(lemas) - 1 or (deal_type == 'long' and est_money < start_money - mc * start_money) or (deal_type == 'short' and est_money > start_money + mc * start_money):
                                        if deal_type == 'long':
                                            money *= lemas[i] / buy_value
                                        else:
                                            money *= buy_value / lemas[i]
                                        in_deal = 0
                                        money *= spread_loss
                                        money -= sell_fee
                                        deals[-1][0].append(i)
                                        deals[-1][1].append(lemas[i])
                                        if start_money <= money:
                                            deals[-1][2] = 1
                                        deal_profits.append(money / start_money)

                                if not in_deal and i > tntb and len(lemas) - i > adl:
                                    deal_opening = 0

                                    if lemas[i] >= bemas[i] and lemas[i-1] < bemas[i-1]:
                                        deal_type = 'long'
                                        deal_opening = 1
                                    elif lemas[i] <= bemas[i] and lemas[i-1] > bemas[i-1]:
                                        deal_type = 'short'
                                        deal_opening = 1

                                    if deal_opening:
                                        buy_time = i
                                        buy_value = lemas[i]
                                        in_deal = 1
                                        start_money = money
                                        deals.append([[],[],0])
                                        deals[-1][0].append(i)
                                        deals[-1][1].append(buy_value)
                                        money *= spread_loss
                                        money -= buy_fee
                            average_deal_profit = sum(deal_profits) / len(deal_profits)
#                                money_hist.append(money)

#                            whole_function.extend(day)
#                            whole_lemas.extend(lemas)
#                            whole_bemas.extend(bemas)
#                            day_ends[0].append(len(whole_function) -1)
#                            day_ends[1].append(whole_function[-1])
#                            for i in range(len(deals)):
#                                for j in range(2):
#                                    try:
#                                        deals[i][0][j] += before_length
#                                    except:
#                                        pass
#                            whole_deals.extend(deals)
#                            before_length += len(day)

                        log.write('Деньги: {}, bsc: {}, lsc: {}, tntb: {}, adl: {}, average deal profit: {}, nsp: {}, mc: {}, deal count: {}.\n'.format(money, bsc, lsc, tntb, adl, average_deal_profit, nsp, mc, len(deal_profits)))
                        log.flush()
#
#                        plt.subplot(2,1,1)
#                        for deal in whole_deals:
#                            if deal[2]:
#                                plt.plot(deal[0], deal[1], 'g')
#                            else:
#                                plt.plot(deal[0], deal[1], 'r')
#                        plt.plot(list(range(len(whole_lemas))), whole_lemas, 'y')
#                        plt.plot(list(range(len(whole_bemas))), whole_bemas, 'y')
#                        plt.plot(list(range(len(whole_function))), whole_function, 'b')
#                        plt.plot(day_ends[0], day_ends[1], 'rs')
#                        plt.subplot(2,1,2)
#                        plt.plot(money_hist, color = 'g')
                        print(1)
