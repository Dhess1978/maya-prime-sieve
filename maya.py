# MAYA Prime Sieve - optimized basic implementation

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

WEIGHTS = [1, 20, 360, 7200, 144000, 2880000]

# Precomputed residues: for each p, store [w % p for w in WEIGHTS]
RESIDUES = {
    p: [w % p for w in WEIGHTS]
    for p in PRIMES
}


def maya_decompose(n):
    A = []
    for w in reversed(WEIGHTS):
        a = n // w
        A.append(a)
        n -= a * w
    return list(reversed(A))


def maya_mod_from_coefficients(A, p):
    total = 0
    residues = RESIDUES[p]

    for a, r in zip(A, residues):
        total += a * r

    return total % p


def maya_candidate(n):
    if n % 2 == 0:
        return False

    # Decompose only once per number
    A = maya_decompose(n)

    for p in PRIMES:
        if maya_mod_from_coefficients(A, p) == 0 and n != p:
            return False

    return True


if __name__ == "__main__":
    test_numbers = [17, 19, 21, 25, 31, 37]

    for n in test_numbers:
        print(n, "→", maya_candidate(n))
