import pickle

class account:
    def __init__(self):
        self.money = 1
        self.in_deal = 0
        self.comission = 0.0003
        self.deal_count = 0
        self.indeal_count = 0

    def buy(self, value):
        if not self.in_deal:
            self.buy_value = value
            self.in_deal = 1
            self.indeal_count+=1
            return 1
        else:
            return 0

    def sell(self, value):
        if self.in_deal:
            self.money *= (value - self.comission) / self.buy_value
            #print(value, self.buy_value, self.money)
            self.in_deal = 0
            self.deal_count += 1
            return 1
        else:
            return 0

def draw_timerows(timerows, zoom = 0.4):
    import tkinter
    root = tkinter.Tk()
    max_height = max(timerows[0]) - min(timerows[0])
    mtmh = max(timerows[0]) #mtmh - max timerow max height
    for i in range(1, len(timerows)):
        height = max(timerows[i]) - min(timerows[i])
        if height > max_height:
            max_height = height
            mtmh = max(timerows[i])

    canv = tkinter.Canvas(root, width = len(timerows[0]) * zoom, height = max_height * zoom)
    colors = ['green', 'blue', 'red']
    for timerow in timerows:
        import random
        coords = []
        color = colors.pop()
        for i in range(len(timerow)):
            if timerow[i] != 0:
                coords.append([i * zoom, -(timerow[i] - mtmh) * zoom])
        canv.create_line(coords, smooth = 1, splinesteps = 0, fill = color) #smooth = 1, splinesteps = 0,
    canv.pack()
    root.mainloop()

periods = [30,35,40]
sd = 0
function = pickle.load(open('function', 'rb'))[:1000]

functions = []
ewmas = []

for period in periods:
    sc = 10/period
    my_account = account()
    prev_ewma = function[period-1]
    for i in range(period, len(function)):
        if function[i] != 0:
            ewma = sc * function[i] + (1-sc) * prev_ewma
            if (function[i] - ewma < 0.0001) and (0 not in function[i: i+100]):
                my_account.buy(function[i])

            elif function[i] == 0:
                my_account.sell(function[i-1])

            if function[i] - ewma < 0.0002:
                if my_account.sell(function[i]):
                    sd+=1
            ewmas.append(ewma * 40000)
            functions.append(function[i] * 40000)
            prev_ewma = ewma
        else:
            prev_ewma = function[i + 1]
            for j in range(i+2, i + period + 2):
                ewma = sc * function[i] + (1-sc) * prev_ewma
            i=i + period + 1
    print((1 - my_account.money ** (1 / my_account.deal_count)) * 10000, period, sc)

#draw_timerows([functions, ewmas], zoom = 1.5)

