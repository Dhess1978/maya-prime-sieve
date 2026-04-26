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

- A_k are positional coefficients  
- w_k are weights defined as:

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

## Usage (Python)

```python
from maya import maya_candidate

if maya_candidate(n):
    # pass to Miller–Rabin
    is_prime = True
```

---

## Purpose

This method acts as a pre-sieve, not a standalone primality test.

It reduces the number of candidates before applying probabilistic tests.

---

## Features

* low computational overhead
* simple implementation
* suitable for large-scale number testing 

---

## Disclaimer

This is not a proof of primality.

It only filters composite numbers based on small prime divisibility.

---

## Author

David Hess  
© 2026
