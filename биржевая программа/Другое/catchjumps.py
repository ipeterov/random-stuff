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
D.append(0)
D.extend(reversed(D))
myacc = account()

minGrowths = [x for x in range(2,20)]
checkAreas = [1,2,3,4,5]
maxFalls = [x for x in range(-2,20, 3)]

for minGrowth in minGrowths:
    minGrowth /= 10000
    file = open("catchjumpslog.txt", "a")
    for checkArea in checkAreas:
        for maxFall in maxFalls:
            maxFall /= 10000
            for MN in range(checkArea, len(D)):
                if myacc.in_deal == 0:
                    wantToOpen = 1
                    for i in range(checkArea):
                        if D[MN-i] - D[MN-i-1] < minGrowth or D[MN-i-1] == 0:
                            wantToOpen = 0

                    if wantToOpen:
                        myacc.Buy(D[MN])

                else:
                    wantToClose = 0
                    if D[MN] - D[MN - 1] > maxFall and D[MN - 1] != 0:
                        wantToClose = 1

                    if wantToClose:
                        myacc.Sell(D[MN], 1)
            if myacc.deal_count != 0 and myacc.money > 0:
                s1 = round(-(1 - myacc.money ** (1 / myacc.deal_count)) * 10000 * 1.25,4), minGrowth, checkArea, maxFall
                s2 = myacc.deal_count, myacc.indeal_count, myacc.money
                file.write(str(s1) + "\n" + str(s2) + "\n")
    file.close()
