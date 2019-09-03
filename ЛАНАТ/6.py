def rmov(s, c):
    c -= c // len(s) * len(s)
    return s[len(s) - c:] + s[:len(s) - c]

def rep(s, l):
    r = s * (l // len(s))
    r += s[:l - len(r)]
    return r

n = int(input())
chars = [int(x) for x in input().split()]
key = rep(input(), n)

for i in range(len(chars)):
    b = bin(chars[i])[2:]
    b = '0' * (8 - len(b)) + b
    chars[i] = chr(int(rmov(b, ord(key[i])), 2))

for c in chars:
    try:
        print(c)
    except:
        pass
