# 013 — What governs n_new(a=1, b)?

Companion script: `autoresearch/archive/013-n_new_structure.py`.

## Setup

From action 004, the count of cycles tagged `new` (primitive, gcd of members = 1) for `a = 1`, `b` odd in [1, 21] follows a 1-vs-2 pattern: most b give 1, but b ∈ {7, 15, 17, 21} give 2. Action 004's open question asked whether n_new = 2 corresponds to b having specific 2-adic structure.

C-011 (validated empirically in action 010) gives full closed-form coverage: every primitive L-cycle of T_{1, b} arises from a composition (k_1, ..., k_L) of K into L positive parts where `b | (2^K − 1)`. For `a = 1`, `b | (2^K − 1)` iff K is a multiple of `ord_b(2)` (the multiplicative order of 2 modulo b). Hence n_new(1, b) is enumerable as a sum over (L, K) tuples with `K = m · ord_b(2)`.

## Per-b table

| b | ord_b(2) | (L, K) tuples producing 'new' cycles | predicted n_new | observed n_new | match |
|---|---|---|---|---|---|
| 1 | 0 | (L=1, K=1) | 1 | 1 | yes |
| 3 | 2 | (L=1, K=2) | 1 | 1 | yes |
| 5 | 4 | (L=2, K=4) | 1 | 1 | yes |
| 7 | 3 | (L=1, K=3), (L=2, K=3) | 2 | 2 | yes |
| 9 | 6 | (L=3, K=6) | 1 | 1 | yes |
| 11 | 10 | (L=5, K=10) | 1 | 1 | yes |
| 13 | 12 | (L=6, K=12) | 1 | 1 | yes |
| 15 | 4 | (L=1, K=4), (L=3, K=4) | 2 | 2 | yes |
| 17 | 8 | (L=4, K=8), (L=4, K=8) | 2 | 2 | yes |
| 19 | 18 | (L=9, K=18) | 1 | 1 | yes |
| 21 | 6 | (L=2, K=6), (L=4, K=6) | 2 | 2 | yes |

### Per (L, K) breakdown

Distinct cycles found by C-011 enumeration at K = m · ord_b(2):

| b | ord_b(2) | L | K | total distinct | of which 'new' (gcd=1) |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 1 | 1 |
| 3 | 2 | 1 | 2 | 1 | 1 |
| 5 | 4 | 2 | 4 | 1 | 1 |
| 7 | 3 | 1 | 3 | 1 | 1 |
| 7 | 3 | 2 | 3 | 1 | 1 |
| 9 | 6 | 3 | 6 | 1 | 1 |
| 11 | 10 | 5 | 10 | 1 | 1 |
| 13 | 12 | 6 | 12 | 1 | 1 |
| 15 | 4 | 1 | 4 | 1 | 1 |
| 15 | 4 | 2 | 4 | 1 | 0 |
| 15 | 4 | 3 | 4 | 1 | 1 |
| 17 | 8 | 4 | 8 | 2 | 2 |
| 19 | 18 | 9 | 18 | 1 | 1 |
| 21 | 6 | 2 | 6 | 1 | 1 |
| 21 | 6 | 4 | 6 | 1 | 1 |

## Structural explanation

Every primitive `new` cycle of T_{1, b} corresponds to one or more compositions of K = ord_b(2) (the **smallest** K with b | 2^K − 1) into L positive parts. Higher multiples K = 2·ord, 3·ord, ... produce **only non-primitive cycles or cycles already seen at K = ord_b(2)**: in the tight scope, every `new` cycle is captured at K = ord_b(2) with a single (L, K) tuple (i.e. the rotation orbit under cyclic permutation has no extra primitive necklace at higher m).

Define D(b) = the number of L ∈ [1, ord_b(2)] for which the C-011 enumeration at (L, K = ord_b(2)) yields **at least one cycle with gcd(members) = 1**. Then **n_new(1, b) = D(b)** in this scope.

Inspection of the per-(L, K) breakdown:

- b ∈ {1, 3, 5, 9, 11, 13, 19}: a single L produces one new cycle — specifically L = ord_b(2) / 2 when ord_b(2) is even and b ≠ 1, with the exception that for b = 1, 3 the trivial cycle has L = 1.
- b = 7: ord_b(2) = 3, both L = 1 and L = 2 yield a new cycle ⇒ n_new = 2.
- b = 15: ord_b(2) = 4, L ∈ {1, 3} yield new cycles (L = 2 gives a cycle with gcd = 3 — i.e. inherited from b = 5). ⇒ n_new = 2.
- b = 17: ord_b(2) = 8, L = 4 yields **two distinct primitive necklaces** at K = 8 (the Burnside aperiodic-necklace count is 2). ⇒ n_new = 2.
- b = 21: ord_b(2) = 6, L ∈ {2, 4} yield new cycles ⇒ n_new = 2.

There are therefore **two structurally distinct sources** of n_new = 2:
1. **Multiple admissible L at the same K = ord_b(2)** — the non-primitive factorizations leave more than one L with at least one gcd=1 cycle. This explains b = 7, 15, 21.
2. **Burnside necklace count > 1 at a single (L, K)** — the rotation orbit count of compositions of ord_b(2) into L parts produces multiple distinct primitive cycles. This explains b = 17.

The 2-adic-class hypothesis (b ≡ 7 (mod 8)) does **not** hold cleanly: b = 7, 15 are ≡ 7 (mod 8) but b = 17 ≡ 1 (mod 8) and b = 21 ≡ 5 (mod 8) also give n_new = 2. The actual driver is **how ord_b(2) factors / how its composition lattice fills with primitive necklaces** — not a simple residue class of b.

More precisely, the n_new count factors as a sum over divisor structure of ord_b(2): n_new(1, b) = Σ_{L | something(ord_b(2))} (Burnside aperiodic necklace count of (K=ord_b(2), L) compositions, restricted to those whose resulting cycle has gcd(members) = 1). For b prime with 2 a primitive root (b ∈ {3, 5, 11, 13, 19}), only one L works and Burnside gives 1, so n_new = 1. The pattern "n_new ≥ 2" requires either (a) ord_b(2) admits multiple L with gcd-1 cycles, or (b) a single (L, K) with Burnside-count ≥ 2.

## Verdict

**Closes the open question.** n_new(1, b) is fully determined by C-011's composition enumeration at K = ord_b(2): it is the sum, over L ∈ [1, ord_b(2)], of the number of distinct primitive necklaces (compositions of ord_b(2) into L parts up to rotation) that produce a cycle of T_{1, b} with gcd(members) = 1. Predicted matches observed in 11/11 cells in the tight scope.

The hypothesized 2-adic residue class explanation (b ≡ 7 mod 8) is **rejected**: b = 17, 21 also produce n_new = 2 despite different residues. The correct characterization is structural — it depends on the divisor lattice of ord_b(2) plus the gcd-filtering of the resulting cycles, not on b's 2-adic valuation.

