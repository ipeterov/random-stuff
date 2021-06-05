import bisect
import collections
import math


class CachedPrimer:
    def __init__(self):
        self.known_primes = []
        self.biggest_checked = 2

    def primes_up_to(self, number) -> list[int]:
        if number <= self.biggest_checked:
            index = bisect.bisect_left(self.known_primes, number)
            return self.known_primes[:index + 1]

        for candidate in range(self.biggest_checked, number + 1):
            def is_prime(candidate):
                candidate_root = candidate ** 0.5
                for known_prime in self.known_primes:
                    if candidate % known_prime == 0:
                        return False
                    if known_prime > candidate_root:
                        return True
                return True

            if is_prime(candidate):
                self.known_primes.append(candidate)

        self.biggest_checked = number

        return self.known_primes

    def number_prime_factors(self, number) -> list[int]:
        factors = collections.Counter()
        remainder = number
        while remainder > 1:
            for prime in self.primes_up_to(remainder):
                if remainder % prime == 0:
                    remainder = remainder // prime
                    factors[prime] += 1
                    break
        return factors

    def factors_count(self, number) -> int:
        factors = self.number_prime_factors(number)
        return math.prod(power + 1 for power in factors.values())


PRIMER = CachedPrimer()
number = 1
index = 1
best_count = 0
while (count := PRIMER.factors_count(number))  <= 500:
    index += 1
    number += index
    if count >= best_count:
        best_count = count
        print(count, number)
else:
    print(count, number)
