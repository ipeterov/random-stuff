def findSimple(a):
    simples = {}
    for i in range(a//2, 1, -1): #int(a**0.5)
        while True:
            if a / i == a // i:
                if i in simples:
                    simples[i] += 1
                else:
                    simples[i] = 1
                a /= i
            else:
                break
    if not simples:
        simples[a] = 1
    return simples

n, k = [int(x) for x in input().split()]
ns, ks = findSimple(n), findSimple(k)
#print(ns, ks)
for key in ks:
    if key not in ns:
        ns[key] = ks[key]
    elif ks[key] > ns[key]:
        ns[key] = ks[key]

number = 1
for key in ns:
    number *= key * ns[key]
print(number)
