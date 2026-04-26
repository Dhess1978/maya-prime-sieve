import time

from maya import maya_candidate

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]


def classic_candidate(n):
    if n % 2 == 0:
        return False
    for p in PRIMES:
        if n % p == 0 and n != p:
            return False
    return True


def run_benchmark(limit):
    numbers = range(3, limit, 2)

    # CLASSIC
    start = time.time()
    classic_pass = 0
    for n in numbers:
        if classic_candidate(n):
            classic_pass += 1
    classic_time = time.time() - start

    # MAYA
    start = time.time()
    maya_pass = 0
    for n in numbers:
        if maya_candidate(n):
            maya_pass += 1
    maya_time = time.time() - start

    total = len(numbers)

    print("=== RESULTS ===")
    print(f"Total tested: {total}")
    print()

    print("Classic:")
    print(f"  Passed: {classic_pass}")
    print(f"  Time: {classic_time:.4f}s")

    print()
    print("MayaMOD:")
    print(f"  Passed: {maya_pass}")
    print(f"  Time: {maya_time:.4f}s")

    print()
    reduction = 100 * (1 - maya_pass / total)
    print(f"Reduction: {reduction:.2f}% filtered")


if __name__ == "__main__":
    run_benchmark(1_000_000)
