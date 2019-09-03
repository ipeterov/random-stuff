import math

a = int(input())
b = int(input())
c = int(input())

dist = c - a
firstjump = min(b-a, c-b)
dist -= firstjump

print(math.floor(math.log(dist, 2)) + 1)
