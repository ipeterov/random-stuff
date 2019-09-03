import string
allchars = {}
for i in range(0, 10):
    allchars[str(i)] = i
i = 9
for letter in string.ascii_uppercase:
    i += 1
    allchars[letter] = i

def findMinCountSys(number):
    minCountSys = 0
    for letter in number:
        if allchars[letter] > minCountSys:
            minCountSys = allchars[letter]
    return minCountSys + 1

def transferTo10th(ground, number):
    result = 0
    i = len(number) - 1
    for letter in number:
        result += allchars[letter] * ground**i
        i -= 1
    return result

a, b, c = input().split()

minCountSys = max([findMinCountSys(x) for x in [a, b, c]])

for i in range(minCountSys, 36):
    if transferTo10th(i, a) + transferTo10th(i, b) == transferTo10th(i, c):
        print(i)
        break
else:
    print(-1)
