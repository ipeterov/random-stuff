l = int(input())
cards1 = input()
cards2 = input()

current = None
ans = ''

for _ in range(l*2):
    if current == None:
        current = cards1[0]

    if current == '0':
        current = '1'
        if cards1 and cards1[0] == '0':
            cards1 = cards1[1:]
            ans += '1'
        elif cards2 and cards2[0] == '0':
            cards2 = cards2[1:]
            ans += '2'

    elif current == '1':
        current = '0'
        if cards1 and  cards1[0] == '1':
            cards1 = cards1[1:]
            ans += '1'
        elif cards2 and  cards2[0] == '1':
            cards2 = cards2[1:]
            ans += '2'

print(ans)
