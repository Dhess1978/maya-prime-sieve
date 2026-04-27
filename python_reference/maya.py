# MAYA Prime Sieve - Python reference implementation
# Slow readable version corresponding to the optimized C pipeline

WHEEL = 30030

PRIMES = [
    17, 19, 23, 29, 31,
    37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113
]

RESIDUES = [
    [1, 3, 3, 9, 10, 13, 5],
    [1, 1, 18, 18, 18, 18, 18],
    [1, 20, 15, 1, 20, 9, 19],
    [1, 20, 12, 8, 15, 10, 26],
    [1, 20, 19, 8, 5, 7, 16],
    [1, 20, 27, 22, 33, 31, 28],
    [1, 20, 32, 25, 8, 37, 2],
    [1, 20, 16, 19, 36, 32, 38],
    [1, 20, 31, 9, 39, 28, 43],
    [1, 20, 42, 45, 52, 33, 24],
    [1, 20, 6, 2, 40, 33, 11],
    [1, 20, 55, 2, 40, 7, 18],
    [1, 20, 25, 31, 17, 5, 33],
    [1, 20, 5, 29, 12, 27, 43],
    [1, 20, 68, 46, 44, 4, 7],
    [1, 20, 44, 11, 62, 55, 73],
    [1, 20, 28, 62, 78, 66, 75],
    [1, 20, 4, 80, 87, 49, 1],
    [1, 20, 69, 22, 52, 70, 42],
    [1, 20, 57, 29, 75, 86, 3],
    [1, 20, 51, 93, 6, 17, 31],
    [1, 20, 39, 31, 85, 95, 81],
    [1, 20, 33, 6, 11, 2, 40],
    [1, 20, 21, 81, 38, 82, 58],
]

WHEEL_MASK = [False] * WHEEL


def init_wheel_mask():
    for r in range(1, WHEEL, 2):
        if (
            r % 3 != 0
            and r % 5 != 0
            and r % 7 != 0
            and r % 11 != 0
            and r % 13 != 0
        ):
            WHEEL_MASK[r] = True


def wheel30030_candidate(n):
    if n in (3, 5, 7, 11, 13):
        return True

    return WHEEL_MASK[n % WHEEL]


def maya_projection_coefficients(n):
    return [
        n % 20,
        (n // 20) % 18,
        (n // 360) % 20,
        (n // 7200) % 20,
        (n // 144000) % 20,
        (n // 2880000) % 20,
        (n // 57600000) % 20,
    ]


def maya_candidate(n):
    """
    Returns False if n is definitely composite.
    Returns True if n is a candidate and should be verified by Miller-Rabin.
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    if not wheel30030_candidate(n):
        return False

    coefficients = maya_projection_coefficients(n)

    for p, residues in zip(PRIMES, RESIDUES):
        if n == p:
            return True

        total = (
            coefficients[0] * residues[0]
            + coefficients[1] * residues[1]
            + coefficients[2] * residues[2]
            + coefficients[3] * residues[3]
            + coefficients[4] * residues[4]
            + coefficients[5] * residues[5]
            + coefficients[6] * residues[6]
        )

        if total % p == 0:
            return False

    return True


if __name__ == "__main__":
    init_wheel_mask()

    test_numbers = [1, 2, 3, 5, 7, 11, 13, 17, 19, 21, 25, 31, 37, 1_000_000]

    for n in test_numbers:
        print(n, "→", maya_candidate(n))
