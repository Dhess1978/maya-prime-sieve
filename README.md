# MAYA Test Sieve v2.04

**Smart pre-filtering for prime testing**

MAYA Test Sieve is a modular pre-sieve designed to reduce the number of candidates passed to expensive primality tests such as Miller–Rabin.

---

## 🔬 Core Idea

Instead of testing all odd numbers directly:

odd numbers → Miller–Rabin

MAYA introduces a structured filtering pipeline:

1. Odd filter
2. Wheel30030 (2, 3, 5, 7, 11, 13)
3. Partial wheel lookup (17 / 19)
4. MAYA positional filter (residue-based projection)
5. Miller–Rabin

---

## 🚀 Results (10B numbers)

- **Numbers tested:** 10,000,000,000  
- **Primes found:** 882,206,715  
- **Validation:** ✔ identical across all methods  

### Performance

| Method | Time | Speed vs baseline |
|--------|------|------------------|
| Baseline (MR only) | 9010 s | — |
| Rolling MAYA (reference) | 7963 s | **+11.62%** |
| v2.04 compact | 14461 s | -60.50% |
| v2.04b key | 13585 s | -50.78% |

---

## 📉 Miller–Rabin Workload Reduction

All MAYA variants achieved:

~77.05% reduction in MR calls

This demonstrates:

> Filtering quality is stable across implementations,  
> but runtime performance depends on execution strategy.

---

## ⚙️ Key Insight

There are two fundamentally different approaches:

### 1. Rolling MAYA (v2.03 – reference)
- Computes projection on-the-fly  
- Lower overhead  
- Best real-world performance  

### 2. Lookup / Compact MAYA (v2.04)
- Precomputed modular lookup  
- O(1) decision per candidate  
- Higher memory and modulo overhead  

---

## 🧩 Original MAYA Principle

MAYA does **not** rely on direct division.

Instead, it uses:

- positional decomposition (base-20 inspired)  
- projection coefficients  
- residue matrices  

This enables detection of composite numbers via structured arithmetic rather than repeated modulo division.

---

## 📊 Why v2.04 matters

Even though v2.04 is slower:

- ✔ proves correctness of compact representation  
- ✔ preserves identical filtering behavior  
- ✔ validates modular / lookup-based approach  
- ✔ separates **algorithmic idea vs implementation strategy**

---

## 🔄 Next Steps

- Hybrid pipeline (Rolling + selective lookup)  
- Modular compression of lookup tables  
- SIMD / vectorization  
- Hardware-aware optimizations  

---

## 📁 Data

Benchmark outputs:

- `maya_benchmark_2_04_10000M_progress.csv`
- `maya_benchmark_2_04_10000M_summary.csv`

---

## ⚠️ Note

MAYA Test Sieve is a **pre-filter**, not a primality test.

Final correctness always depends on Miller–Rabin (or equivalent).

---

## 🧠 Conclusion

MAYA Test Sieve demonstrates that structured, residue-based pre-filtering can significantly reduce the workload of probabilistic primality tests without affecting correctness.

The experiments on a 10B range confirm that:

- large-scale candidate reduction (~77%) is achievable
- filtering behavior remains stable across implementations
- performance depends more on execution strategy than on the mathematical filter itself

This highlights an important distinction between:

- **algorithmic design** (filtering quality)
- **implementation strategy** (runtime efficiency)

The MAYA approach opens a path toward hybrid and hardware-aware filtering systems that can further optimize large-scale prime testing.

---

## 👤 Author

David Hess  
2026
