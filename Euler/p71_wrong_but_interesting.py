# Forgot the HCF rule, still pretty cool

import wrapt_timeout_decorator


target = 3 / 7
closest_numerator = 2
closest_denominator = 5
closest = closest_numerator / closest_denominator


def best_numerator_using_binary(denominator):
    best = 0

    def binary(left_boundary, right_boundary):
        nonlocal best

        if left_boundary == right_boundary:
            return left_boundary

        center = left_boundary + (right_boundary - left_boundary) // 2
        current = center / denominator

        if current > target:
            binary(left_boundary, center)
        else:
            if current > best / denominator:
                best = center
            binary(center + 1, right_boundary)

    binary(0, denominator)

    return best


@wrapt_timeout_decorator.timeout(60)
def solve():
    for denominator in range(1, 1000001):
        if denominator % 1000 == 0:
            print(denominator)

        numerator = best_numerator_using_binary(denominator)
        result = numerator / denominator
        if result < target and result > closest:
            closest = result
            closest_numerator = numerator
            closest_denominator = denominator

    # I would have thought this one would be the best, but no
    n = best_numerator_using_binary(1000000)
    print(n / 1000000, n, 1000000)

    # Really close one, but not quite
    print(closest, closest_numerator, closest_denominator)
