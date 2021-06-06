import collections
import math

import wrapt_timeout_decorator

from common.primer import CachedPrimer


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    232792560
    """
    PRIMER = CachedPrimer()
    factors = collections.Counter()
    for i in range(1, 21):
        for factor, power in PRIMER.prime_factors(i).items():
            factors[factor] = max(power, factors[factor])

    return math.prod(factor ** power for factor, power in factors.items())


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
