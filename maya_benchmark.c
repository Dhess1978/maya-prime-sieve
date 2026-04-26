#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <time.h>

static const uint64_t PRIMES[] = {
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31
};

static const uint64_t WEIGHTS[] = {
    1, 20, 360, 7200, 144000, 2880000
};

#define PRIME_COUNT 10
#define WEIGHT_COUNT 6


bool maya_candidate(uint64_t n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if ((n % 2) == 0) return false;

    uint64_t coefficients[WEIGHT_COUNT];
    uint64_t remainder = n;

    for (int i = WEIGHT_COUNT - 1; i >= 0; i--) {
        coefficients[i] = remainder / WEIGHTS[i];
        remainder -= coefficients[i] * WEIGHTS[i];
    }

    for (int i = 0; i < PRIME_COUNT; i++) {
        uint64_t p = PRIMES[i];

        if (n == p) return true;

        uint64_t total = 0;

        for (int k = 0; k < WEIGHT_COUNT; k++) {
            total += coefficients[k] * (WEIGHTS[k] % p);
        }

        if ((total % p) == 0) {
            return false;
        }
    }

    return true;
}


bool miller_rabin(uint64_t n) {
    if (n < 2) return false;

    static const uint64_t small_primes[] = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
    };

    for (int i = 0; i < 11; i++) {
        uint64_t p = small_primes[i];

        if (n == p) return true;
        if (n % p == 0) return false;
    }

    uint64_t d = n - 1;
    int s = 0;

    while ((d & 1) == 0) {
        s++;
        d >>= 1;
    }

    static const uint64_t bases[] = {
        2, 3, 5, 7, 11, 13, 17
    };

    for (int i = 0; i < 7; i++) {
        uint64_t a = bases[i];

        if (a >= n) continue;

        __uint128_t x = 1;
        __uint128_t base = a;
        uint64_t exp = d;

        while (exp > 0) {
            if (exp & 1) {
                x = (x * base) % n;
            }
            base = (base * base) % n;
            exp >>= 1;
        }

        if (x == 1 || x == n - 1) {
            continue;
        }

        bool composite = true;

        for (int r = 1; r < s; r++) {
            x = (x * x) % n;

            if (x == n - 1) {
                composite = false;
                break;
            }
        }

        if (composite) {
            return false;
        }
    }

    return true;
}


int main(void) {
    uint64_t limit = 4000003; // cca 2 000 000 lichých čísel
    uint64_t total = 0;

    clock_t start, end;

    uint64_t baseline_prime_count = 0;

    start = clock();

    for (uint64_t n = 3; n < limit; n += 2) {
        total++;

        if (miller_rabin(n)) {
            baseline_prime_count++;
        }
    }

    end = clock();

    double baseline_time = (double)(end - start) / CLOCKS_PER_SEC;

    uint64_t maya_prime_count = 0;
    uint64_t maya_candidates = 0;

    start = clock();

    for (uint64_t n = 3; n < limit; n += 2) {
        if (maya_candidate(n)) {
            maya_candidates++;

            if (miller_rabin(n)) {
                maya_prime_count++;
            }
        }
    }

    end = clock();

    double maya_time = (double)(end - start) / CLOCKS_PER_SEC;

    uint64_t avoided_mr = total - maya_candidates;
    double avoided_percent = 100.0 * avoided_mr / total;

    printf("=== RESULTS ===\n");
    printf("Total tested: %llu\n\n", total);

    printf("Baseline: Miller-Rabin only\n");
    printf("  Prime count: %llu\n", baseline_prime_count);
    printf("  Time: %.6f s\n\n", baseline_time);

    printf("MAYA pipeline: MayaMOD + Miller-Rabin\n");
    printf("  Maya candidates passed to MR: %llu\n", maya_candidates);
    printf("  Prime count: %llu\n", maya_prime_count);
    printf("  Time: %.6f s\n\n", maya_time);

    if (baseline_prime_count == maya_prime_count) {
        printf("Validation: OK - both methods found the same number of primes\n");
    } else {
        printf("Validation: WARNING - methods differ\n");
    }

    printf("Miller-Rabin calls avoided: %llu\n", avoided_mr);
    printf("Miller-Rabin workload reduction: %.2f%%\n", avoided_percent);

    return 0;
}
