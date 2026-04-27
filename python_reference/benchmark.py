import time

WHEEL = 30030
PRIME_COUNT = 24
WEIGHT_COUNT = 7

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
    c = maya_projection_coefficients(n)

    for p, residues in zip(PRIMES, RESIDUES):
        if n == p:
            return True

        total = (
            c[0] * residues[0]
            + c[1] * residues[1]
            + c[2] * residues[2]
            + c[3] * residues[3]
            + c[4] * residues[4]
            + c[5] * residues[5]
            + c[6] * residues[6]
        )

        if total % p == 0:
            return False

    return True


def miller_rabin(n):
    if n < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0

    while d & 1 == 0:
        s += 1
        d >>= 1

    bases = [2, 3, 5, 7, 11, 13, 17]

    for a in bases:
        if a >= n:
            continue

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        composite = True

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    return True


def run_benchmark(limit):
    total = 0

    start = time.time()
    baseline_prime_count = 0

    for n in range(3, limit, 2):
        total += 1

        if miller_rabin(n):
            baseline_prime_count += 1

    baseline_time = time.time() - start

    wheel_passed = 0
    maya_candidates = 0
    maya_prime_count = 0

    start = time.time()

    for n in range(3, limit, 2):
        if not wheel30030_candidate(n):
            continue

        wheel_passed += 1

        if maya_candidate(n):
            maya_candidates += 1

            if miller_rabin(n):
                maya_prime_count += 1

    pipeline_time = time.time() - start

    wheel_filtered = total - wheel_passed
    maya_filtered = wheel_passed - maya_candidates
    total_avoided_mr = total - maya_candidates

    print("=== RESULTS ===")
    print("Mode: Wheel30030 mask fixed + MayaMOD clean 24 filters + Miller-Rabin")
    print(f"Total tested: {total}")
    print()

    print("Baseline: Miller-Rabin only")
    print(f"  Prime count: {baseline_prime_count}")
    print(f"  Time: {baseline_time:.6f} s")
    print()

    print("Pipeline: Wheel30030 mask fixed + MayaMOD + Miller-Rabin")
    print(f"  Wheel30030 passed to MayaMOD: {wheel_passed}")
    print(f"  Maya candidates passed to MR: {maya_candidates}")
    print(f"  Prime count: {maya_prime_count}")
    print(f"  Time: {pipeline_time:.6f} s")
    print()

    if baseline_prime_count == maya_prime_count:
        print("Validation: OK - both methods found the same number of primes")
    else:
        print("Validation: WARNING - methods differ")

    print(f"Wheel30030 filtered: {wheel_filtered} ({100 * wheel_filtered / total:.2f}%)")
    print(
        f"MayaMOD filtered after wheel: {maya_filtered} "
        f"({100 * maya_filtered / wheel_passed:.2f}% of wheel-passed)"
    )
    print(f"Total Miller-Rabin calls avoided: {total_avoided_mr}")
    print(f"Total Miller-Rabin workload reduction: {100 * total_avoided_mr / total:.2f}%")


if __name__ == "__main__":
    init_wheel_mask()
    run_benchmark(20_000_003)
