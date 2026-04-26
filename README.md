# MAYA Prime Sieve

A modular pre-sieve for efficient primality testing based on the MayaMOD framework.

---

## Overview

MAYA Prime Sieve is a lightweight pre-filter designed to reduce the number of candidates passed to computationally expensive primality tests such as Miller–Rabin.

The method is based on a positional decomposition derived from the Mayan number system.

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

## C Benchmark

The main performance implementation is written in C.

File:

maya_benchmark.c

Compile:

bash gcc -O3 maya_benchmark.c -o maya_benchmark 

Run:

bash ./maya_benchmark 

---

## Benchmark Result

Validation benchmark over 2,000,000 odd numbers:

Baseline: Miller-Rabin only 
Prime count: 283145 
Time: 0.587613 s  

MAYA pipeline: MayaMOD + Miller-Rabin 
Maya candidates passed to MR: 611413 
Prime count: 283145 
Time: 0.592562 s  

Miller-Rabin calls avoided: 1388587 
Miller-Rabin workload reduction: 69.43%

The MAYA pipeline preserved identical prime detection results while avoiding 69.43% of Miller–Rabin calls, with runtime nearly identical to the baseline.

---

## Python Reference

The Python implementation is included only as a readable reference version.

It is not optimized for performance.

See:

python_reference/

---

## Purpose

This method acts as a pre-sieve, not a standalone primality test.

It reduces the number of candidates before applying probabilistic tests.

---

## Disclaimer

This is not a proof of primality.

It only filters composite numbers before final primality testing.

---

## Author

David Hess  
© 2026
This transforms large-number arithmetic into operations on small modular values.

---

## C Benchmark

The main performance implementation is written in C.

File:

text maya_benchmark.c 

Compile:

bash gcc -O3 maya_benchmark.c -o maya_benchmark 

Run:

bash ./maya_benchmark 

---

## Benchmark Result

Validation benchmark over 2,000,000 odd numbers:

Baseline: Miller-Rabin only
Prime count: 283145
Time: 0.587613 s

MAYA pipeline: MayaMOD + Miller-Rabin
Maya candidates passed to MR: 611413
Prime count: 283145
Time: 0.592562 s

Miller-Rabin calls avoided: 1388587
Miller-Rabin workload reduction: 69.43%

The MAYA pipeline preserved identical prime detection results while avoiding 69.43% of Miller–Rabin calls, with runtime nearly identical to the baseline.

---

## Python Reference

The Python implementation is included only as a readable reference version.

It is not optimized for performance.

See:

text python_reference/ 

---

## Purpose

This method acts as a pre-sieve, not a standalone primality test.

It reduces the number of candidates before applying probabilistic tests.

---

## Disclaimer

This is not a proof of primality.

It only filters composite numbers before final primality testing.

---

## Author

David Hess  
© 2026
