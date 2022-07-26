from pickle import *
rf = load(open('leaps_array','rb'))
pf = load(open('pseudo_leaps_array','rb'))
for key in rf:
    if key in pf:
        print(rf[key]-pf[key],(rf[key]-pf[key])/rf[key])
    else:
        print(rf[key], '!')
