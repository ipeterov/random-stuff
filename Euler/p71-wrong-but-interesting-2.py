import itertools
import math

from collections import Counter
from functools import wraps
from time import perf_counter_ns


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = perf_counter_ns()
        result = f(*args, **kw)
        te = perf_counter_ns()
        print(f"func:{f.__name__} took: {te-ts}ns")
        return result

    return wrap


def primes_up_to(number) -> list[int]:
    known_primes = []
    for candidate in range(2, number + 1):

        def is_prime(candidate):
            candidate_root = candidate ** 0.5
            for known_prime in known_primes:
                if candidate % known_prime == 0:
                    return False
                if known_prime > candidate_root:
                    return True
            return True

        if is_prime(candidate):
            known_primes.append(candidate)

    return known_primes


known_primes = primes_up_to(1000000)


def number_prime_factors(number) -> list[int]:
    factors = Counter()
    while number > 1:
        for prime in known_primes:
            if number % prime == 0:
                number = number / prime
                factors[prime] += 1
                break
    return factors


def potential_factors(number):
    prime_factors = number_prime_factors(number)
    factor_lists = []
    for factor in prime_factors.keys():
        factors = []
        power = 1
        while factor ** power < number:
            factors.append(factor ** power)
            power += 1
        factor_lists.append(factors)
    return factor_lists


target = 3 / 7
best = 2 / 5, 2, 5

for denominator in range(1, 1000001):
    if denominator % 1000 == 0:
        print(denominator)

    for factors in itertools.product(*potential_factors(denominator)):
        numerator = math.prod(factors)

        current = numerator / denominator

        if current < best[0]:
            continue

        if current > target:
            continue

        best = current, numerator, denominator


# Wrong, but pretty interesting still - pirnts out the highest HCF variant, not the HFC=1 variant
print(best)
