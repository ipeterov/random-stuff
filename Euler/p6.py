import wrapt_timeout_decorator


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    25164150
    """

    N = 100

    sum_of_squares = sum(n ** 2 for n in range(1, N + 1))
    square_of_sum = sum(n for n in range(1, N + 1)) ** 2

    return square_of_sum - sum_of_squares
