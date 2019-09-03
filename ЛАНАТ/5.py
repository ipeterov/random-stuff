extra_corriculars = [int(x) for x in input().split()]
n = int(input())
pupils = {}
for i in range(n):
    inp = input().split()
    pupils[inp[0]] = [int(x) for x in inp[1:]]

for i in range(4):
    for key in pupils:
        if type(pupils[key]) is list:
            if pupils[key]:
                j = pupils[key].pop(0)
                if extra_corriculars[j]:
                    extra_corriculars[j] -= 1
                    pupils[key] = j
            else:
                for j in range(extra_corriculars):
                    if extra_corriculars[j]:
                        pupils[key] = j
                        extra_corriculars[j] -= 1

for key in pupils:
    print(key, pupils[key])
