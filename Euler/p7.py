def first_n_primes(count):
    known_primes = []
    candidate = 2

    def is_prime(candidate):
        candidate_root = candidate ** 0.5
        for known_prime in known_primes:
            if candidate % known_prime == 0:
                return False
            if known_prime > candidate_root:
                return True
        return True

    while len(known_primes) < count:
        if is_prime(candidate):
            known_primes.append(candidate)
        candidate += 1

    return known_primes


primes = first_n_primes(10001)
print(primes[-1])
