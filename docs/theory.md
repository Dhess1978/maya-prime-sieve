# Theory

## Positional Representation

The MayaMOD framework represents integers using a mixed-base positional system:

N = Σ A_k · w_k

where:

w₀ = 1  
w₁ = 20  
w₂ = 360  
w_k = 360 · 20^(k−2)

## Modular Transformation

Divisibility is computed using:

N mod p = (Σ A_k · (w_k mod p)) mod p

This allows transformation of large-number arithmetic into operations on small modular values.

## Interpretation

The method can be viewed as:

- projecting integers into a modular residue space
- performing linear combination tests in that space

## Key Property

Precomputed residues:

w_k mod p

allow fast evaluation of divisibility without large integer operations.

## Relation to Classical Methods

- Similar in spirit to modular arithmetic sieves
- Differs by using positional decomposition rather than direct modular chains

## Role in Pipeline

MayaMOD acts as:

a deterministic composite filter before probabilistic primality testing

It is not a standalone primality test.
