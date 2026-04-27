The MayaMOD filter deterministically eliminates many composite numbers by testing divisibility in a transformed modular weight space, reducing the candidate set for subsequent primality testing.

This folder contains a simple reference implementation of MayaMOD in Python.

It is intended for readability, validation, and educational purposes.

The Python version is not optimized for performance and serves only as a conceptual demonstration of the algorithm.

In benchmark testing, the Python implementation is approximately 20–30× slower than the optimized C version, which is consistent with typical differences between interpreted and compiled languages.

For performance benchmarks and practical use, see the C implementation:

```text
maya_benchmark.c
