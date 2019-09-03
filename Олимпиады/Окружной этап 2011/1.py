n = int(input())
a = int(input())
b = int(input())

if min(a,b) >= n:
    print(n+1)
else:
    print(min(a,b) + 1)
