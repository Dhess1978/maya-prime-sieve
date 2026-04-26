# MAYA Prime Sieve - basic implementation

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

WEIGHTS = [1, 20, 360, 7200, 144000, 2880000]


def maya_decompose(n):
    A = []
    for w in reversed(WEIGHTS):
        a = n // w
        A.append(a)
        n -= a * w
    return list(reversed(A))


def maya_mod(n, p):
    A = maya_decompose(n)
    total = 0
    for a, w in zip(A, WEIGHTS):
        total += a * (w % p)
    return total % p


def maya_candidate(n):
    # sudá čísla vyřadíme hned
    if n % 2 == 0:
        return False

    for p in PRIMES:
        if maya_mod(n, p) == 0 and n != p:
            return False
    return True


# TEST
# TEST

if __name__ == "__main__":
    test_numbers = [17, 19, 21, 25, 31, 37]

    for n in test_numbers:
        print(n, "→", maya_candidate(n))
