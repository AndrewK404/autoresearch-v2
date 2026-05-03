# res 047 — the general m=1 theorem (C-019): an infinite 2D lattice of tractable cousins

## What & why
After verifying L=9 of the Catalan family (K = 2L−1), I noticed K = 2L+1
ALSO gives Catalan numbers (different shift). This raised the obvious
question: **what counts emerge for general K?**

The answer: for any (a, K, L) with gcd(K, L) = 1 and 2^K > a^L, the
cell (a, b = 2^K − a^L) admits exactly C(K−1, L−1)/L primitive cycles
of length K+L via the m=1 mechanism. The Catalan families are special
cases.

## Done
1. Verified the general formula for a=3 across 28 (L, K) pairs with
   L∈[1,6], K∈[L+1, 4L), all gcd(K,L)=1.
2. Spot-checked a=5 (7 cells) and a=7 (7 cells).
3. **42/42 cells match the prediction exactly.**

Script: `archive/047-general-lattice.py` (and 047-catalan-k-2lp1.py
for the second-family discovery).

## Result

**Conjecture / theorem candidate (C-019):** For any odd a ≥ 3,
positive integers L, K with gcd(K, L) = 1 and 2^K > a^L:

  Let b = 2^K − a^L. Then b is odd, and the generalized Collatz
  map T_{a,b}(n) = n/2 if even, a·n+b if odd has at least
  
    **C(K−1, L−1) / L = (K−1)! / (L! · (K−L)!)**
  
  primitive cycles of length K+L, given explicitly by:
  
    cycle entry points n_0(k_⃗) = Σ_{i=0}^{L-1} a^{L-1-i} · 2^{k_1+...+k_i}
  
  for compositions k_⃗ = (k_1, ..., k_L) of K into L positive parts,
  with k_⃗ taken modulo cyclic rotation.

**Sample lattice for a=3:**

| L\K | 2 | 3 | 4 | 5 | 7 | 8 | 9 | 10 | 11 | 13 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **1** | **1** |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  | **2** | **3** |  |  |  |  |  |  |
| 3 |  |  |  | **2** | **5** | **7** |  | **12** | **15** |  |  |
| 4 |  |  |  |  | **5** |  | **14** |  | **30** | **55** |  |
| 5 |  |  |  |  |  | **7** | **14** |  | **42** | **99** | **364** |
| 6 |  |  |  |  |  |  |  |  | **42** | **132** | **728** |

Each entry is the predicted (and verified) number of primitive cycles
of length K+L in the cell (3, 2^K − 3^L). 42/42 cells verified.

The diagonal K = 2L−1 is the **first Catalan family** (L≥3): cycle
counts 2, 5, 14, 42, 132, ...
The diagonal K = 2L+1 is the **second Catalan family** (L≥1): cycle
counts 1, 2, 5, 14, 42, 132, 429, ...
The diagonal K = 3L−1, K = 3L+1, etc. give other named sequences
(Fuss-Catalan, ballot numbers, etc.).

## Proof sketch
1. **b is odd.** 2^K (even, K≥1) − a^L (odd, a odd) = odd.
2. **m = 1** by construction: b·1 = 2^K − a^L.
3. **Apply C-011** (proven for b odd): primitive cycles of T_{a,b}
   correspond to (L', K', composition k_⃗') with b | (2^{K'} − a^{L'})
   and n_0 = b·S(k_⃗') / (2^{K'} − a^{L'}). At m=1 with this (L, K),
   n_0 = S(k_⃗) directly.
4. **n_0 is a positive odd integer.** S(k_⃗) = Σ a^{L-1-i} · 2^{cum_i}
   with cum_0 = 0. The first term a^{L-1} is odd (a odd); all others
   have factor 2^{cum_i ≥ 1}, hence even. Sum: odd + even = odd. All
   terms positive ⟹ n_0 > 0.
5. **C(K−1, L−1) compositions** of K into L positive parts.
6. **Burnside dedup factor L.** gcd(K, L) = 1 ⟹ no composition is
   fixed by any non-trivial rotation (a fixed-point composition under
   r-fold rotation requires r | gcd(K, L)). So the cyclic group ℤ/L
   acts freely, and the number of orbits is C(K−1, L−1) / L.
∎

## Why this is a real result
This **directly answers TASK.md's "tractable cousin" prompt** — not
with a single example, but with a 2D infinite lattice of cells, each
with an EXPLICIT cycle count. Previously documented examples:

- **(3, 1)** classical Collatz (no extra cycles known): outside the
  m=1 lattice (b=1 ⟹ no K, L with 2^K − 3^L = 1 except trivial).
- **(3, 5)** at L=3, K=5: 2 cycles (matches first table entry).
- **(3, 7)** at L=2, K=4: gcd(4,2)=2, NOT in the gcd=1 lattice
  (different mechanism).
- **(3, 13)** at L=5, K=8: 7 cycles (table entry).
- **(3, 47)** at L=4, K=7: 5 cycles (table entry).

The lattice frames Collatz-family structure: cells on the lattice are
"cycle-rich"; off-lattice cells (like (3, 1) itself) have at most
inherited cycles.

## Connection to combinatorics on words
C(K-1, L-1)/L is the count of **aperiodic necklaces with L black and
K−L white beads** when gcd(K, L) = 1 (every necklace is aperiodic
in this case). Equivalently, the number of Lyndon words of length K
over {0, 1} with exactly L ones, restricted to gcd(K, L) = 1.

So C-019 establishes a **Lyndon-word ↔ primitive Collatz cycle**
bijection on the m=1 lattice. This is structurally clean and
falsifiable.

## Thoughts
This is substantially stronger than C-018 alone:
- C-018 gave one infinite Catalan family (a=3, K=2L−1).
- C-019 generalizes to a 2D lattice with arbitrary (a, K, L) gcd-1.

The total count of "tractable cousins" is now a 2-parameter infinity
per a value, not just a 1-parameter Catalan sequence.

The "≥" in the theorem statement (rather than "exactly") reflects
that other m > 1 tuples might produce additional primitive cycles in
the same (a, b). The double-m=1 cells (C-017) are precisely the rare
cases where two different (L, K) tuples produce m=1 simultaneously.

## Reasoning
This sequence — discover one Catalan family (C-018), notice the second
(K=2L+1), generalize to arbitrary (L, K) — is a classic "unlock the
big picture" cascade. The proof is essentially the same as C-018's,
just stated in greater generality. Each step (Burnside, n_0 oddness,
gcd⟹no symmetry) uses standard tools.

The novelty lies in the application: this is, to my knowledge, the
first systematic enumeration of m=1 primitive cycles across the
generalized Collatz family expressed as an explicit 2D lattice with
closed-form cycle counts.

## Conclusion
**C-019 conjectured + proof sketched + 42/42 empirical verifications.**

This is the right "main theorem" of the run. C-018 is now a corollary
(Catalan diagonal of the lattice). The autoresearch process produced:

1. C-011: cycle classification (proven necessary for b odd).
2. C-019: explicit cycle counts on the m=1 lattice (proven sketch +
   broad empirical verification).
3. C-018: Catalan diagonal as a special case.
4. C-017: rare double-m=1 coincidences.

Together these form a coherent structural picture of the m=1 part
of the cycle space.

## Next
- Document C-019 in CONJECTURES.md as the main theorem; demote
  C-018 to corollary.
- Update README.md headline to lead with C-019.
- Falsification target: find any (a, b, L, K) gcd=1 cell where the
  m=1 cycle count differs from C(K−1, L−1)/L. None found in 42 trials.
- Investigate the gcd(K, L) > 1 case: Burnside-Lothaire formula
  generalization. Should still give explicit closed form.

## Linked
- archive/047-general-lattice.py
- archive/047-catalan-k-2lp1.py
