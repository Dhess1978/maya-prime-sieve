# Benchmark Results

## 10M Test

Baseline: Miller–Rabin only  

Prime count: 1270606  

Time: 2.95 s  

Pipeline: Wheel30030 + MayaMOD + Miller–Rabin  

Prime count: 1270606  

Time: 2.89 s  

Miller–Rabin calls avoided: 7,703,881  

Workload reduction: 77.04%  

Speed improvement: ~1.85%

---

## 100M Test

Baseline: Miller–Rabin only  

Prime count: 11078936  

Time: 30.79 s  

Pipeline: Wheel30030 + MayaMOD + Miller–Rabin  

Prime count: 11078936  

Time: 30.22 s  

Miller–Rabin calls avoided: 77,051,836  

Workload reduction: 77.05%  

Speed improvement: ~1.84%

---

## Summary

- Identical prime counts across all tests (validated)

- Consistent ~77% reduction in Miller–Rabin calls

- Stable performance scaling from 10M to 100M

- Linear time complexity confirmed
