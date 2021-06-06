import collections
import itertools
import math

import wrapt_timeout_decorator

from common.primer import CachedPrimer


PRIMER = CachedPrimer()


# def smallest_possible_500_factors():  # INCORRECT
#     first_500_primes = PRIMER.primes_up_to(stop_at_n_primes=500)
#     best = math.inf
#     prime_count = 500
#     while prime_count > 1:
#         factors = itertools.chain(*zip(*(first_500_primes for _ in range(prime_count))))
#         candidate = 1
#         used_factors = collections.Counter()

#         while math.prod(used_factors.values()) < 500:
#             factor = next(factors)
#             used_factors[factor] += 1
#             candidate *= factor

#             if prime_count == 4:
#                 print(factor)

#         prime_count -= 1

#         best = min(candidate, best)
#     return best


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    76576500
    """

    primer = CachedPrimer()
    number = 1
    print(
        candidates,
        smallest_possible_500_factors,
        primer.factors_count(smallest_possible_500_factors),
    )
    index = 1
    best_count = 0
    while (count := primer.factors_count(number)) <= 500:
        index += 1
        number += index
        if count >= best_count:
            best_count = count
            print(number, best_count)
    else:
        return number


print(smallest_possible_500_factors())
