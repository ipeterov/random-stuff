n = int(input())
a = int(input())
b = int(input())

if min(a,b) < n:
    print(min(a,b) + 1)
else:
    print(n+1)
