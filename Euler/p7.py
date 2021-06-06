import wrapt_timeout_decorator

from common.primer import CachedPrimer


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    104743
    """

    primer = CachedPrimer()

    primes = primer.primes_up_to(stop_at_n_primes=10001)

    return primes[-1]
