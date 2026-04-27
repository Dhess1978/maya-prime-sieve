# Performance Analysis

## Key Observation

The MayaMOD filter reduces Miller–Rabin calls by ~77%, yet total runtime improves only by ~1.8%.

## Interpretation

This indicates that:

- Miller–Rabin is not the dominant performance bottleneck
- The computational cost of MayaMOD is comparable to the cost of avoided Miller–Rabin calls

## Pipeline Breakdown

Full pipeline:

N → odd filter → Wheel30030 → MayaMOD → Miller–Rabin

Reduction:

- ~61% removed by Wheel30030
- ~40% removed by MayaMOD (from remaining)
- ~77% total reduction of Miller–Rabin workload

## Bottlenecks

Main computational costs:

- Integer division (n / 20, n / 360, …)
- Modular reduction (total % p)
- Memory access (RESIDUES lookup)

## Implications

The algorithm is already near optimal balance between:

filter cost vs. avoided primality testing

## Optimization Directions

Further improvements may include:

- Eliminating division via rolling coefficients
- Loop unrolling for MayaMOD
- Cache optimization for residue tables
- SIMD/vectorization

## Conclusion

MayaMOD is an effective modular pre-sieve that significantly reduces primality test workload while maintaining correctness and scalability.
