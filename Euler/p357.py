from common.primer import CachedPrimer


def sum_digits(n):
    return sum(int(char) for char in str(n))


PRIMER = CachedPrimer()
generators = []
for n in range(1, 100000001):
    last_digit = n % 10
    # if n > 6 and not last_digit in {2, 8, 0}:
    #     continue

    if all(PRIMER.is_prime(factor + n // factor) for factor in PRIMER.factors(n)):
        generators.append(n)
        print(n, last_digit in {2, 8, 0}, PRIMER.prime_factors(n))
