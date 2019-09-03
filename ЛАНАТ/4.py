n, x, y = [int(x) for  x in input().split()]
strings = 0; crutches = 0

for i in range(n):
    a, b = [int(x) for x in input().split()]
    strings += (min(22,b) - a) * x; crutches += (min(22,b) - a) * y
    if b > 22:
        strings += (b-22) * x / 2; crutches += (b-22) * y * 2

print(crutches/strings)
