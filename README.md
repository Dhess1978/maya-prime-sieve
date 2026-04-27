# MAYA Prime Sieve


A modular pre-sieve reducing primality test workload by ~77%.

---

## Overview

MAYA Prime Sieve is a lightweight pre-filter designed to reduce the number of candidates passed to computationally expensive primality tests such as Miller–Rabin.

The method is based on a positional decomposition inspired by the Mayan number system.

---

## Core Idea

A number is represented as:

N = Σ A_k · w_k

where:

w0 = 1 
w1 = 20 
w2 = 360 
w_k = 360 · 20^(k-2)

---

## Modular Transformation

Divisibility is computed as:

N mod p = (Σ A_k · (w_k mod p)) mod p

This transforms large-number arithmetic into operations on small modular values.

---

## Optimized Pipeline

The current optimized pipeline combines three stages:

Sequential input → odd numbers → Wheel30030 → MayaMOD → Miller–Rabin

* Wheel30030 removes multiples of small primes (2, 3, 5, 7, 11, 13)
* MayaMOD filters additional composite numbers using modular projection
* Miller–Rabin performs final probabilistic validation

---

## C Benchmark

The main performance implementation is written in C.

File:

maya_benchmark.c

Compile:

gcc -O3 maya_benchmark.c -o maya_benchmark

Run:

./maya_benchmark

---

## Benchmark Result (10M test)

Validation benchmark over ~10,000,000 numbers:

Baseline: Miller–Rabin only
Prime count: 1270606
Time: 2.954527 s

Pipeline: Wheel30030 + MayaMOD + Miller–Rabin
Maya candidates passed to MR: 2296119
Prime count: 1270606
Time: 2.899830 s

Miller–Rabin calls avoided: 7703881
Miller–Rabin workload reduction: 77.04%

---

* Preserved identical prime detection results
* Reduced Miller–Rabin workload by 77.04%
* Achieved a ~1.85% speed improvement over standalone Miller–Rabin

---

## Python Reference

The Python implementation is included as a readable reference version.

It is not optimized for performance and is intended for:

* validation
* clarity
* educational purposes

See:

python_reference/

---

## Purpose

This method acts as a pre-sieve, not a standalone primality test.

It reduces the number of candidates before applying probabilistic tests such as Miller–Rabin.

---

## Disclaimer

This is not a proof of primality.

It only filters composite numbers before final primality testing.

---

## Extended Documentation

For detailed benchmark results, scaling behavior, and theoretical background, see:

* Benchmark Results (10M, 100M)￼
* Performance Analysis￼
* Theory￼

---

## Author

David Hess
© 2026 

