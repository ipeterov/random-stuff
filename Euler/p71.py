TARGET = 3 / 7


def best_numerator_using_binary(denominator):
    best = 0

    def binary(left_boundary, right_boundary):
        nonlocal best

        if left_boundary == right_boundary:
            return left_boundary

        center = left_boundary + (right_boundary - left_boundary) // 2
        current = center / denominator

        if current >= TARGET:
            binary(left_boundary, center)
        else:
            if current > best / denominator:
                best = center
            binary(center + 1, right_boundary)

    binary(0, denominator)

    return best


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
    factors = set()
    while number > 1:
        for prime in known_primes:
            if number % prime == 0:
                number = number / prime
                factors.add(prime)
                break
    return factors


best = 2 / 5, 2, 5

for denominator in range(2, 1000001):
    if denominator % 1000 == 0:
        print(denominator)

    denominator_prime_factors = number_prime_factors(denominator)

    numerator = best_numerator_using_binary(denominator)

    assert numerator / denominator < TARGET

    def hcf_is_1(numerator):
        common_factors = number_prime_factors(numerator) & denominator_prime_factors
        return not common_factors

    while numerator / denominator > best[0] and not hcf_is_1(numerator):
        numerator -= 1

    current = numerator / denominator
    assert current < TARGET

    if current > best[0]:
        best = current, numerator, denominator

# Ended up using the code from both wrong solutions. Cool!
print(best)  # (0.42857128571385716, 428570, 999997)
