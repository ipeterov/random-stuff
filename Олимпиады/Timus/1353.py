s = int(input())

#uniques = [s]
#for i in range(1,s):
    #uniques.append(int(str(i) + str(s-i)))

#print(uniques)

ns = []

for i in range(90, 900):
    if sum([int(x) for x in list(str(i))]) == s:
        ns.append(i)
print(ns)
print(len(ns))
