def collatz_chain_length(starting):
    current = starting
    length = 1
    while current > 1:
        if current % 2 == 0:
            current = current / 2
        else:
            current = current * 3 + 1
        length += 1
    return length


best = 0
best_number = 0
for n in range(1000000):
    if n % 10000 == 0:
        print(n)

    length = collatz_chain_length(n)
    if length > best:
        best = length
        best_number = n

print(best, best_number)
