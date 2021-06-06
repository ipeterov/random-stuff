import math

import wrapt_timeout_decorator


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    31875000
    """

    for c in range(335, 998):
        for b in range(math.ceil(c / 2), c):
            a = 1000 - c - b

            assert a + b + c == 1000

            if a ** 2 + b ** 2 == c ** 2:
                return a * b * c
