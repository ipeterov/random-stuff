import wrapt_timeout_decorator

from common.primer import CachedPrimer


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    142913828922
    """

    primer = CachedPrimer()
    known_primes = primer.primes_up_to(2000000)
    return sum(known_primes)
