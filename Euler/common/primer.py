import bisect
import collections
import itertools
import math


class CachedPrimer:
    def __init__(self):
        # Pre-fill it a bit to make handling the edge case "2" easier:
        # it's the only even prime, we can then check just odd numbers
        self.known_primes = [2, 3]
        self.known_primes_set = {2, 3}
        self.biggest_checked = 3

    def _generate_primes(self, stop_at_candidate=None, stop_at_n_primes=None) -> None:
        def should_stop(candidate):
            if stop_at_n_primes is not None:
                return len(self.known_primes) >= stop_at_n_primes

            return candidate > stop_at_candidate

        step = 2  # because even numbers cannot be primes
        candidate = self.biggest_checked + step
        while not should_stop(candidate):

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
                self.known_primes_set.add(candidate)

            self.biggest_checked = candidate

            candidate += step

    def is_prime(self, candidate) -> bool:
        self._generate_primes(stop_at_candidate=candidate)
        return candidate in self.known_primes_set

    def primes_up_to(self, stop_at_candidate=None, stop_at_n_primes=None) -> list[int]:
        """
        >>> len(primer.primes_up_to(stop_at_n_primes=10001))
        10001
        >>> primer.primes_up_to(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        >>> primer.primes_up_to(stop_at_n_primes=10)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        """

        assert (
            stop_at_candidate is not None or stop_at_n_primes is not None
        ), "Must provide stop_at_candidate or stop_at_n_primes"

        if stop_at_candidate is not None and stop_at_candidate <= self.biggest_checked:
            index = bisect.bisect_right(self.known_primes, stop_at_candidate)
            return self.known_primes[:index]

        if stop_at_n_primes is not None and stop_at_n_primes <= len(self.known_primes):
            return self.known_primes[:stop_at_n_primes]

        self._generate_primes(stop_at_candidate, stop_at_n_primes)

        return self.known_primes

    def prime_factors(self, number) -> list[int]:
        """
        >>> primer.prime_factors(0)
        Counter()
        >>> primer.prime_factors(1)
        Counter()
        >>> primer.prime_factors(2)
        Counter({2: 1})
        >>> primer.prime_factors(30)
        Counter({2: 1, 3: 1, 5: 1})
        >>> primer.prime_factors(1920)
        Counter({2: 7, 3: 1, 5: 1})
        >>> primer.prime_factors(212930)
        Counter({2: 1, 5: 1, 107: 1, 199: 1})
        """

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
        """
        >>> primer.factors_count(0)
        1
        >>> primer.factors_count(1)
        1
        >>> primer.factors_count(2)
        2
        >>> primer.factors_count(30)
        8
        """

        factors = self.prime_factors(number)
        return math.prod(power + 1 for power in factors.values())

    def factors(self, number) -> list[int]:
        """
        >>> primer.factors(0)
        [1]
        >>> primer.factors(1)
        [1]
        >>> primer.factors(2)
        [1, 2]
        >>> primer.factors(30)
        [1, 5, 3, 15, 2, 10, 6, 30]
        """

        factor_lists = []
        for prime_factor, max_power in self.prime_factors(number).items():
            factors = []
            for power in range(max_power + 1):
                factors.append(prime_factor ** power)
            factor_lists.append(factors)

        return [
            math.prod(factor_options)
            for factor_options in itertools.product(*factor_lists)
        ]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True, extraglobs={"primer": CachedPrimer()})
