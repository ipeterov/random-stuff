import math


for c in range(335, 998):
    for b in range(math.ceil(c / 2), c):
        a = 1000 - c - b

        assert a + b + c == 1000

        if a ** 2 + b ** 2 == c ** 2:
            print(a, b, c)
            print(a * b * c)
