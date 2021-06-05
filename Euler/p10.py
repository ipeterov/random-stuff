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


known_primes = primes_up_to(2000000)

print(sum(known_primes))

