import wrapt_timeout_decorator


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


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    837799
    """

    best = 0
    best_number = 0
    for n in range(1000000):
        length = collatz_chain_length(n)
        if length > best:
            best = length
            best_number = n

    return best_number
