import math

import wrapt_timeout_decorator


def is_palindrome(number):
    s = str(number)
    check_count = math.ceil(len(s) / 2)

    for index in range(check_count):
        if s[index] != s[-index - 1]:
            return False

    return True


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    906609
    """

    largest = 0
    for a in range(100, 1000):
        for b in range(100, 1000):
            product = a * b
            if product > largest and is_palindrome(product):
                largest = product
    return largest
