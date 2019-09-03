n = int(input())
names = []
for  i in range(n):
    names.append(input().split())

for name in names:
    print(name[0], name[1][0] + '.' + name[2][0] + '.', name[3][-2:])
