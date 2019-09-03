import random

output = open('output.txt', 'w')

quantity = int(input())

for i in range(quantity):
    passed = 0
    while not passed:
        numbers = []
        for j in range(2):
            numbers.append(random.randint(22, 28))
        for j in range(9):
            numbers.append(random.randint(13, 19))
        random.shuffle(numbers)
        if numbers[0] < 22:
            passed = 1

    for i in range(11):
        output.write(str(numbers.pop(random.randint(0, len(numbers)-1))) + ' | ')
    output.write('\n\n')
