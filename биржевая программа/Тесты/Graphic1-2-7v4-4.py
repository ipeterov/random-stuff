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

D = pickle.load(open('function', 'rb'))[:5000000]

Directions = [-1,1]
Area_CheckMax_Values = [6,7,8,9,10]
Area_GiveAFuckAbouts = [4,5,6,7,8,9]
Points_UpperToBuys = [42,44,46,48,50,52,58,60,62,64,66,68]
Ms_LookToSells = [1]
Points_LowerToSells = [17,18,19,20,21]
Points_VBuy_Adds = [-24,-21,-18,-15,-10,-12,-8,-7,-6,-9,-11,-13]
Points_LowerThanBuyToSells = [10000]


for Area_CheckMax_Value in Area_CheckMax_Values:
    for Area_GiveAFuckAbout in Area_GiveAFuckAbouts:
        file = open("alldataGraphic1-2-7v4-4.txt", "a")
        if Area_GiveAFuckAbout < Area_CheckMax_Value:
            for Ms_LookToSell in Ms_LookToSells:
                for Points_UpperToBuy in Points_UpperToBuys:
                    for Points_LowerToSell in Points_LowerToSells:
                        for Points_VBuy_Add in Points_VBuy_Adds:
                            for Points_LowerThanBuyToSell in Points_LowerThanBuyToSells:
                                for Direction in Directions:
                                    if Direction == 1:

                                        NeedToCheckMax = 0
                                        V_Max = 0
                                        my_account = account()
                                        MN_MaxInArea = -1
                                        FallN = 0
                                        V_Buy = 2
                                        VFall = 0

                                        for MN in range(Area_CheckMax_Value+1, len(D) - Area_GiveAFuckAbout):

                                            if MN - Area_CheckMax_Value > MN_MaxInArea:
                                                V_MaxInArea = 0
                                                for MNiArea in range(MN - Area_CheckMax_Value,int(MN - Area_CheckMax_Value + Area_GiveAFuckAbout + 1)):
                                                    if D[MNiArea] >= V_MaxInArea:
                                                        V_MaxInArea = D[MNiArea]
                                                        MN_MaxInArea = MNiArea

                                            if D[MN] >= V_MaxInArea + Points_UpperToBuy / 10000:
                                                if my_account.Buy(D[MN]):
                                                    NeedToCheckMax = 1
                                                    V_Max = D[MN]
                                                    V_Buy = D[MN]
                                                    FallN = 0

                                            if D[int(MN - Area_CheckMax_Value + Area_GiveAFuckAbout + 1)] >= D[MN_MaxInArea]:
                                                MN_MaxInArea = int(MN - Area_CheckMax_Value + 1)
                                                V_MaxInArea = D[MN_MaxInArea]

                                            if NeedToCheckMax == 1:
                                                if D[MN] > V_Max:
                                                    V_Max = D[MN]

                                            if D[MN] - D[MN - Ms_LookToSell] <= -Points_LowerToSell/10000 and D[MN] != 0:
                                                FallN += 1
                                                if FallN == 1:
                                                    VFall = D[MN]

                                            if V_Buy - D[MN] >= Points_LowerThanBuyToSell/10000 and D[MN] != 0 or D[MN] >= V_Buy + Points_VBuy_Add/10000 and FallN == 1 or FallN > 1 and D[MN] < VFall - Points_LowerToSell/10000 and D[MN] != 0:
                                                my_account.Sell(D[MN], Direction)
                                                NeedToCheckMax = 0
                                                V_Max = 0
                                                FallN = 0

                                        if my_account.money > -10 and my_account.deal_count > 0:
                                            s1 = round(-(1 - my_account.money ** (1 / my_account.deal_count)) * 10000 * 1.25,4), Area_CheckMax_Value, Area_GiveAFuckAbout, "P", Points_UpperToBuy, Direction, "s", Ms_LookToSell, Points_LowerToSell, "buyadd", Points_VBuy_Add
                                            s2 = my_account.deal_count, my_account.indeal_count, my_account.money
                                            file.write(str(s1) + "\n" + str(s2) + "\n")
                                            print(str(s1))
                                            print(str(s2))
                                            if my_account.money > 1 and FirstMoney > 1:
                                                print ("@@@@@@@@@@@", (my_account.money * FirstMoney))
                                                s = "@@@@@@@@@@@",  (my_account.money * FirstMoney)
                                                file.write(str(s))
                                        else:
                                            print("No")

                                    else:

                                        NeedToCheckMax = 0
                                        V_Max = 2
                                        MN_MaxInArea = -1
                                        FallN = 0
                                        my_account = account()
                                        V_Buy = 0
                                        VFall = 2

                                        for MN in range(Area_CheckMax_Value+1, len(D) - Area_GiveAFuckAbout):

                                            if MN - Area_CheckMax_Value > MN_MaxInArea:
                                                V_MaxInArea = 2
                                                for MNiArea in range(MN - Area_CheckMax_Value,int(MN - Area_CheckMax_Value + Area_GiveAFuckAbout+1)):
                                                    if D[MNiArea] <= V_MaxInArea and D[MNiArea] !=0:
                                                        V_MaxInArea = D[MNiArea]
                                                        MN_MaxInArea = MNiArea

                                            if D[MN] <= V_MaxInArea - Points_UpperToBuy / 10000 and D[MN]!=0:
                                                if my_account.Buy(D[MN]):
                                                    NeedToCheckMax = 1
                                                    V_Max = D[MN]
                                                    V_Buy = D[MN]
                                                    FallN = 0

                                            if D[int(MN - Area_CheckMax_Value + Area_GiveAFuckAbout + 1)] <= D[MN_MaxInArea]:
                                                MN_MaxInArea = int(MN - Area_CheckMax_Value + 1)
                                                V_MaxInArea = D[MN_MaxInArea]

                                            if NeedToCheckMax == 1:
                                                if D[MN] < V_Max and D[MN] != 0:
                                                    V_Max = D[MN]

                                            if D[MN] - D[MN - Ms_LookToSell] >= Points_LowerToSell/10000 and D[MN - Ms_LookToSell] != 0:
                                                FallN += 1
                                                if FallN == 1:
                                                    VFall = D[MN]

                                            if V_Buy - D[MN] <= -Points_LowerThanBuyToSell/10000 and D[MN] != 0 or D[MN] != 0 and (D[MN] <= V_Buy - Points_VBuy_Add/10000 and FallN == 1 or FallN > 1 and D[MN] > VFall + Points_LowerToSell/10000):
                                                my_account.Sell(D[MN], Direction)
                                                NeedToCheckMax = 0
                                                V_Max = 2
                                                FallN = 0

                                        if my_account.money > -10 and my_account.deal_count > 0:
                                            s1 = round(-(1 - my_account.money ** (1 / my_account.deal_count)) * 10000 * 1.25,4), Area_CheckMax_Value, Area_GiveAFuckAbout, "P", Points_UpperToBuy, Direction, "s", Ms_LookToSell, Points_LowerToSell, "buyadd", Points_VBuy_Add
                                            s2 = my_account.deal_count, my_account.indeal_count, my_account.money
                                            file.write(str(s1) + "\n" + str(s2) + "\n")
                                            print(str(s1))
                                            print(str(s2))
                                            FirstMoney = my_account.money
                                        else:
                                            print("No")
                                            FirstMoney = 0
        file.close()
