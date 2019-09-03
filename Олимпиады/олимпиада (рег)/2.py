b, g = [int(x) for x in input().split()]
result = ''

normalcount = min(b, g//2)
result += 'BGG' * normalcount
b -= normalcount
g -= normalcount*2

result += 'B' * b
result += 'G' * g

print(result)
