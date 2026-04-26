import time

from maya import maya_candidate


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

    while d % 2 == 0:
        s += 1
        d //= 2

    # Deterministic bases valid for 64-bit integers
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
    numbers = range(3, limit, 2)

    # BASELINE: Miller-Rabin for every number
    start = time.time()
    baseline_prime_count = 0

    for n in numbers:
        if miller_rabin(n):
            baseline_prime_count += 1

    baseline_time = time.time() - start

    # MAYA PIPELINE: Maya pre-sieve, then Miller-Rabin only for candidates
    start = time.time()
    maya_prime_count = 0
    maya_candidates = 0

    for n in numbers:
        if maya_candidate(n):
            maya_candidates += 1

            if miller_rabin(n):
                maya_prime_count += 1

    maya_time = time.time() - start

    total = len(numbers)
    avoided_mr = total - maya_candidates
    avoided_mr_percent = 100 * avoided_mr / total

    print("=== RESULTS ===")
    print(f"Total tested: {total}")
    print()

    print("Baseline: Miller-Rabin only")
    print(f"  Prime count: {baseline_prime_count}")
    print(f"  Time: {baseline_time:.4f}s")
    print()

    print("MAYA pipeline: MayaMOD + Miller-Rabin")
    print(f"  Maya candidates passed to MR: {maya_candidates}")
    print(f"  Prime count: {maya_prime_count}")
    print(f"  Time: {maya_time:.4f}s")
    print()

    if baseline_prime_count == maya_prime_count:
        print("Validation: OK - both methods found the same number of primes")
    else:
        print("Validation: WARNING - methods differ")

    print(f"Miller-Rabin calls avoided: {avoided_mr}")
    print(f"Miller-Rabin workload reduction: {avoided_mr_percent:.2f}%")


if __name__ == "__main__":
    run_benchmark(4_000_003)
