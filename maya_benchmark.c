#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <time.h>

#define WHEEL 30030
#define PRIME_COUNT 24
#define WEIGHT_COUNT 7

static bool WHEEL_MASK[WHEEL];

static const uint64_t PRIMES[] = {
    17,19,23,29,31,
    37,41,43,47,53,59,61,67,71,
    73,79,83,89,97,101,103,107,109,113
};

static const uint64_t RESIDUES[PRIME_COUNT][WEIGHT_COUNT] = {
    {1,3,3,9,10,13,5},
    {1,1,18,18,18,18,18},
    {1,20,15,1,20,9,19},
    {1,20,12,8,15,10,26},
    {1,20,19,8,5,7,16},
    {1,20,27,22,33,31,28},
    {1,20,32,25,8,37,2},
    {1,20,16,19,36,32,38},
    {1,20,31,9,39,28,43},
    {1,20,42,45,52,33,24},
    {1,20,6,2,40,33,11},
    {1,20,55,2,40,7,18},
    {1,20,25,31,17,5,33},
    {1,20,5,29,12,27,43},
    {1,20,68,46,44,4,7},
    {1,20,44,11,62,55,73},
    {1,20,28,62,78,66,75},
    {1,20,4,80,87,49,1},
    {1,20,69,22,52,70,42},
    {1,20,57,29,75,86,3},
    {1,20,51,93,6,17,31},
    {1,20,39,31,85,95,81},
    {1,20,33,6,11,2,40},
    {1,20,21,81,38,82,58}
};

void init_wheel_mask(void) {
    for (int i = 0; i < WHEEL; i++) {
        WHEEL_MASK[i] = false;
    }

    for (int r = 1; r < WHEEL; r += 2) {
        if ((r % 3 != 0) &&
            (r % 5 != 0) &&
            (r % 7 != 0) &&
            (r % 11 != 0) &&
            (r % 13 != 0)) {
            WHEEL_MASK[r] = true;
        }
    }
}

bool wheel30030_candidate(uint64_t n) {
    if (n == 3 || n == 5 || n == 7 || n == 11 || n == 13) {
        return true;
    }

    return WHEEL_MASK[n % WHEEL];
}

void maya_projection_coefficients(uint64_t n, uint64_t c[WEIGHT_COUNT]) {
    c[0] = n % 20;
    c[1] = (n / 20) % 18;
    c[2] = (n / 360) % 20;
    c[3] = (n / 7200) % 20;
    c[4] = (n / 144000) % 20;
    c[5] = (n / 2880000) % 20;
    c[6] = (n / 57600000) % 20;
}

bool maya_candidate(uint64_t n) {
    uint64_t c[WEIGHT_COUNT];
    maya_projection_coefficients(n, c);

    for (int i = 0; i < PRIME_COUNT; i++) {
        uint64_t p = PRIMES[i];

        if (n == p) return true;

        uint64_t total =
            c[0] * RESIDUES[i][0] +
            c[1] * RESIDUES[i][1] +
            c[2] * RESIDUES[i][2] +
            c[3] * RESIDUES[i][3] +
            c[4] * RESIDUES[i][4] +
            c[5] * RESIDUES[i][5] +
            c[6] * RESIDUES[i][6];

        if ((total % p) == 0) {
            return false;
        }
    }

    return true;
}

bool miller_rabin(uint64_t n) {
    if (n < 2) return false;

    static const uint64_t small_primes[] = {
        2,3,5,7,11,13,17,19,23,29,31
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

    static const uint64_t bases[] = {2,3,5,7,11,13,17};

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

        if (x == 1 || x == n - 1) continue;

        bool composite = true;

        for (int r = 1; r < s; r++) {
            x = (x * x) % n;

            if (x == n - 1) {
                composite = false;
                break;
            }
        }

        if (composite) return false;
    }

    return true;
}

int main(void) {
    init_wheel_mask();

    uint64_t limit = 20000003;
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

    uint64_t wheel_passed = 0;
    uint64_t maya_candidates = 0;
    uint64_t maya_prime_count = 0;

    start = clock();

    for (uint64_t n = 3; n < limit; n += 2) {
        if (!wheel30030_candidate(n)) continue;

        wheel_passed++;

        if (maya_candidate(n)) {
            maya_candidates++;

            if (miller_rabin(n)) {
                maya_prime_count++;
            }
        }
    }

    end = clock();

    double pipeline_time = (double)(end - start) / CLOCKS_PER_SEC;

    uint64_t wheel_filtered = total - wheel_passed;
    uint64_t maya_filtered = wheel_passed - maya_candidates;
    uint64_t total_avoided_mr = total - maya_candidates;

    printf("=== RESULTS ===\n");
    printf("Mode: Wheel30030 mask fixed + MayaMOD clean 24 filters + Miller-Rabin\n");
    printf("Total tested: %llu\n\n", total);

    printf("Baseline: Miller-Rabin only\n");
    printf("  Prime count: %llu\n", baseline_prime_count);
    printf("  Time: %.6f s\n\n", baseline_time);

    printf("Pipeline: Wheel30030 mask fixed + MayaMOD + Miller-Rabin\n");
    printf("  Wheel30030 passed to MayaMOD: %llu\n", wheel_passed);
    printf("  Maya candidates passed to MR: %llu\n", maya_candidates);
    printf("  Prime count: %llu\n", maya_prime_count);
    printf("  Time: %.6f s\n\n", pipeline_time);

    if (baseline_prime_count == maya_prime_count) {
        printf("Validation: OK - both methods found the same number of primes\n");
    } else {
        printf("Validation: WARNING - methods differ\n");
    }

    printf("Wheel30030 filtered: %llu (%.2f%%)\n",
        wheel_filtered, 100.0 * wheel_filtered / total);

    printf("MayaMOD filtered after wheel: %llu (%.2f%% of wheel-passed)\n",
        maya_filtered, 100.0 * maya_filtered / wheel_passed);

    printf("Total Miller-Rabin calls avoided: %llu\n", total_avoided_mr);
    printf("Total Miller-Rabin workload reduction: %.2f%%\n",
        100.0 * total_avoided_mr / total);

    return 0;
}
