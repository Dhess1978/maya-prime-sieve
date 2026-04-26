# MAYA Prime Sieve - optimized basic implementation

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

WEIGHTS = [1, 20, 360, 7200, 144000, 2880000]

# Precomputed residues: for each p, store [w % p for w in WEIGHTS]
RESIDUES = {
    p: [w % p for w in WEIGHTS]
    for p in PRIMES
}


def maya_decompose(n):
    coefficients = []

    for weight in reversed(WEIGHTS):
        coefficient = n // weight
        coefficients.append(coefficient)
        n -= coefficient * weight

    return list(reversed(coefficients))


def maya_mod_from_coefficients(coefficients, p):
    total = 0
    residues = RESIDUES[p]

    for coefficient, residue in zip(coefficients, residues):
        total += coefficient * residue

    return total % p


def maya_candidate(n):
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    # Decompose only once per number
    coefficients = maya_decompose(n)

    for p in PRIMES:
        if n == p:
            return True

        if maya_mod_from_coefficients(coefficients, p) == 0:
            return False

    return True


if __name__ == "__main__":
    test_numbers = [1, 2, 3, 17, 19, 21, 25, 31, 37]

    for n in test_numbers:
        print(n, "→", maya_candidate(n))
