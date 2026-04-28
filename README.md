# MAYA Prime Sieve

---

## Overview

MAYA Prime Sieve is a pre-filter designed to reduce the number of candidates passed to computationally expensive primality tests such as Miller–Rabin.

The method is based on positional decomposition and is used as an optimization layer within a primality testing pipeline.

This is not a standalone primality test.

---

## Pipeline

odd numbers
→ Wheel30030
→ MAYA (lookup)
→ Miller–Rabin

---

## Key Idea (v2.03)

Version 2.03 replaces runtime computation with a precomputed lookup.

Previous form:

pass(n) = Wheel(n) && Maya(n)

## Current form:

pass(n) = LOOKUP(index(n))

---

## Decision cost:

O(1) per number

---

## Results
## 1000M Test

* ~77% reduction in Miller–Rabin calls
* ~8% runtime improvement vs baseline
* identical prime counts (no observed false negatives)

## Interpretation

* Reduction remains stable across the full range
* Lookup removes most of the filter computation cost
* Performance improves as scale increases

---

## Scaling

Range         Result
10M           ✔ faster
100M          ✔ stable
1000M         ✔ scalable

---

## Evolution

## v1.00

* ~77% MR reduction
* small speed improvement (~1–2%)
* limited by per-candidate computation cost

## v2.02

* improved rolling computation
* still CPU-bound

## v2.03

* lookup-based filtering
* reduced filter cost
* improved scalability

---

## Benchmark Data

Benchmark datasets (10M / 100M / 1000M) are included in the repository.

### Direct access:

* [10M dataset](data/v2.03-c/10M/)
* [100M dataset](data/v2.03-c/100M/)
* [1000M dataset](data/v2.03-c/1000M/)

Each dataset contains:

* progress.csv – intermediate measurements
* summary.csv – final results

### Example files

- [10M summary](data/v2.03-c/10M/maya_benchmark_2_03_10M_lookup_summary.csv)
- [100M summary](data/v2.03-c/100M/maya_benchmark_2_03_100M_lookup_summary.csv)
- [1000M summary](data/v2.03-c/1000M/maya_benchmark_2_03_1000M_lookup_summary.csv)

All benchmark results can be independently verified using the provided datasets.

---

## Current Limitation

The current implementation requires:

O(N) memory

Example:

- 100M candidates ≈ 1 GB

---

## Next Steps (v2.04)

Planned work:

* modular lookup compression (n % M)
* layer-aware filtering
* node-based elimination
* partial wheel reinforcement (17 / 19)

---

## Design Goals

* reduce runtime computation
* move work to precomputation
* preserve correctness
* scale to large input ranges

---

## Purpose

Pre-filter layer for primality testing pipelines.

---

## Disclaimer

This is not a primality test.
It does not prove primality.

---

## Status

Active development.
Next version: v2.04

---

## Citation

DOI: https://doi.org/10.5281/zenodo.19807084

---

## Visualization

![MAYA 1000M](docs/maya_1000M.png)

---

## Author

David Hess
© 2026 

