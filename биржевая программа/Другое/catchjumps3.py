import pickle

class account:
    def __init__(self):
        self.money = 1
        self.in_deal = 0
        self.comission = 0.0003
        self.deal_count = 0
        self.indeal_count = 0

    def Buy(self, value):
        if not self.in_deal:
            self.buy_value = value
            self.in_deal = 1
            self.indeal_count+=1
            return 1
        else:
            return 0

    def Sell(self, value, direction):
        if self.in_deal:
            #self.money *= ((value - self.comission) / self.buy_value - 1)*30 + 1
            if direction == -1:
                self.money *= ((self.buy_value - self.comission) / value- 1)*1 + 1
            else:
                self.money *= ((value - self.comission) / self.buy_value- 1)*1 + 1
            #print(value, self.buy_value, self.money)
            self.in_deal = 0
            self.deal_count += 1
            return 1
        else:
            return 0

D = pickle.load(open('function', 'rb'))

minGrowths = [x for x in range(2,20, 3)]
growthCheckAreas = [1,2,3,4,5]
fallCheckAreas = [1,2,3,4,5]
maxFalls = [x for x in range(-2,20, 3)]
minMedProfits = [0,2,5,10,17]

for minMedProfit in minMedProfits:
    for minGrowth in minGrowths:
        minGrowth /= 10000
        file = open("catchjumpslog_3.txt", "a")
        for growthCheckArea in growthCheckAreas:
            for fallCheckArea in fallCheckAreas:
                for maxFall in maxFalls:
                    maxFall /= 10000
                    myacc = account()
                    money_hist = []
                    for MN in range(growthCheckArea, len(D)):
                        if myacc.in_deal == 0:
                            wantToOpen = 1
                            for i in range(growthCheckArea):
                                for i in range(growthCheckArea):
                                    if D[MN-i] - D[MN-i-1] >= D[MN-i-1] - D[MN-i-2] or D[MN-i-2] == 0 or D[MN-i] == 0 or D[MN-i-1] == 0:
                                        wantToOpen = 0
                                if (D[MN] - D[MN-fallCheckArea]) / fallCheckArea > -minMedProfit:
                                    wantToOpen = 0

                            if wantToOpen:
                                myacc.Buy(D[MN])

                        else:
                            wantToClose = 1
                            for i in range(fallCheckArea):
                                if D[MN-i] - D[MN-i-1] < maxFall or D[MN-i-1] == 0 or D[MN-i] == 0:
                                    wantToClose = 0
                            if wantToClose:
                                myacc.Sell(D[MN], -1)
                        money_hist.append(myacc.money)
                    if myacc.deal_count != 0 and myacc.money > 0:
                        s1 = round(-(1 - myacc.money ** (1 / myacc.deal_count)) * 10000 * 1.25,4), minGrowth, growthCheckArea, fallCheckArea, maxFall, -1,minMedProfit
                        s2 = myacc.deal_count, myacc.indeal_count, myacc.money
                        file.write(str(s1) + "\n" + str(s2) + "\n")
                        qwer = myacc.money
    #                plt.subplot(2,1,1)
    #                plt.plot(money_hist, color = 'g')


                    myacc = account()
                    money_hist = []
                    for MN in range(growthCheckArea, len(D)):
                        if myacc.in_deal == 0:
                            wantToOpen = 1
                            for i in range(growthCheckArea):
                                for i in range(growthCheckArea):
                                    if D[MN-i] - D[MN-i-1] <= D[MN-i-1] - D[MN-i-2] or D[MN-i-2] == 0 or D[MN-i] == 0 or D[MN-i-1] == 0:
                                        wantToOpen = 0
                                if (D[MN] - D[MN-fallCheckArea]) / fallCheckArea < minMedProfit:
                                    wantToOpen = 0

                            if wantToOpen:
                                myacc.Buy(D[MN])

                        else:
                            wantToClose = 1
                            for i in range(fallCheckArea):
                                if D[MN-i] - D[MN-i-1] > -maxFall or D[MN-i-1] == 0 or D[MN-i] == 0:
                                    wantToClose = 0
                            if wantToClose:
                                myacc.Sell(D[MN], 1)
                        money_hist.append(myacc.money)
                    if myacc.deal_count != 0 and myacc.money > 0:
                        s1 = round(-(1 - myacc.money ** (1 / myacc.deal_count)) * 10000 * 1.25,4), minGrowth, growthCheckArea, fallCheckArea, maxFall, 1, minMedProfit
                        s2 = myacc.deal_count, myacc.indeal_count, myacc.money
                        s3 = ''
                        print(qwer, myacc.money, myacc.deal_count)
                        if qwer > 1 and myacc.money > 1:
                            s3 = '@@@@@@@@@@@@' + str(myacc.money*qwer)
                            print(s3)
                        file.write(str(s1) + "\n" + str(s2) + "\n" + str(s3))
    #                plt.subplot(2,1,2)
    #                plt.plot(money_hist, color = 'g')
        file.close()
