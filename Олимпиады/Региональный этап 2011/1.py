a1, a2, a3, a4 = [int(x) for x in input().split()]

sqcount = min(a1, a2) + min(a3, a4)

i = 1
while 1:
    if i**2 > sqcount:
        print(i-1)
        break
    i += 1
