import math
from collections import Counter, defaultdict


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


factors = Counter()
for i in range(1, 21):
    for factor, power in number_prime_factors(i).items():
        factors[factor] = max(power, factors[factor])


print(factors)
print(math.prod(factor ** power for factor, power in factors.items()))
