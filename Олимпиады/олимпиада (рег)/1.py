a, b = [int(x) for x in input().split()]

maxherons = min(a, b)
minherons = max(a, b) // 2

print(minherons, maxherons)
