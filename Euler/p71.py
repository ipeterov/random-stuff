import wrapt_timeout_decorator

from common.primer import CachedPrimer


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


@wrapt_timeout_decorator.timeout(60)
def solve():
    """
    >>> solve()
    428570
    """

    best = 2 / 5, 2, 5
    primer = CachedPrimer()

    for denominator in range(2, 1000001):
        if denominator % 1000 == 0:
            print(denominator)

        denominator_prime_factors = primer.prime_factors(denominator).keys()

        numerator = best_numerator_using_binary(denominator)

        assert numerator / denominator < TARGET

        def hcf_is_1(numerator):
            common_factors = (
                primer.prime_factors(numerator).keys() & denominator_prime_factors
            )
            return not common_factors

        while numerator / denominator > best[0] and not hcf_is_1(numerator):
            numerator -= 1

        current = numerator / denominator
        assert current < TARGET

        if current > best[0]:
            best = current, numerator, denominator

    # Ended up using the code from both wrong solutions. Cool!
    return best[1]  # (0.42857128571385716, 428570, 999997)
