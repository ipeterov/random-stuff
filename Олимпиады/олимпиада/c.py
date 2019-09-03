import math

a = int(input())
b = int(input())
c = int(input())

dist = max(b-a, c-b) - 1

i = 0
while True:
    dist = math.ceil(dist / 2)
    i += 1
    if dist == 1:
        break

print(i+1)
