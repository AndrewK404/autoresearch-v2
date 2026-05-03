# res 044 — exceptional "double-m=1" cells in the (a, b) family

## What & why
Following the user's directive to focus on one part and try to discover
something new, I examined the structural reason for cycle-richness in
specific (a, b) cells.

The cycle equation `n₀·(2^K − a^L) = b·S(k⃗)` (per C-011) is most
generative when `m := (2^K − a^L)/b = 1` — every composition yields
an integer n₀, contributing C(K-1, L-1)/L primitive cycles via Burnside
(for gcd(K, L) = 1).

**Question**: which (a, b) cells admit MULTIPLE such (L, K) tuples
with `2^K − a^L = b`?

## Done
Systematic enumeration over a ∈ [3, 199] odd, K ≤ 99, L ≤ 39, b ≤ 10¹².
Looked for (a, b) with at least 2 distinct (L, K) tuples.

## Result — likely new

**Exactly THREE "double-m=1" cells exist in the searched range:**

| (a, b) | Tuples | Multiplicative identity |
|---|---|---|
| (3, 5) | (L=1, K=3), (L=3, K=5) | 2³·(2² − 1) = 24 = 3·(3² − 1) |
| (3, 13) | (L=1, K=4), (L=5, K=8) | 2⁴·(2⁴ − 1) = 240 = 3·(3⁴ − 1) |
| (5, 3) | (L=1, K=3), (L=3, K=7) | 2³·(2⁴ − 1) = 120 = 5·(5² − 1) |

**Zero "triple-m=1" cells exist** in the same range.

## Cycle-count verification
Per Burnside (gcd(K, L) = 1 in all three cases):
- (3, 5): 1 + 2 = 3 primitive m=1 cycles ✓ (atlas has 6 = 3 m=1 + 1 inherited + 2 m>1)
- (3, 13): 1 + 7 = 8 primitive m=1 cycles ✓ (atlas has 10 = 8 m=1 + 1 inherited + 1 m>1)
- (5, 3): 1 + 5 = 6 primitive m=1 cycles ✓ (atlas has 7 = 6 m=1 + 1 inherited)

## Thoughts
This is a **Pillai-type Diophantine** observation: the equation
`2^K − a^L = b` with a, b odd integers and L, K ≥ 1 has finitely many
solutions for each (a, b) by Mihăilescu/Tijdeman bounds. Most
(a, b) admit ZERO or ONE solution. Only THREE cells in the searched
range admit TWO solutions.

The structural identity behind each two-solution case:
`2^{K_1}·(2^{ΔK} − 1) = a^{L_1}·(a^{ΔL} − 1)`

with the divisibility constraints:
- `2^{K_1} | (a^{ΔL} − 1)` — i.e., `ord_{2^{K_1}}(a) | ΔL`
- `a^{L_1} | (2^{ΔK} − 1)` — i.e., `ord_{a^{L_1}}(2) | ΔK`

These are tight number-theoretic constraints. The three solutions
correspond to small instances:
- (3, 5): ord_8(3) = 2, ord_3(2) = 2 → ΔL = ΔK = 2
- (3, 13): ord_16(3) = 4, ord_3(2) = 2 → ΔL = ΔK = 4
- (5, 3): ord_8(5) = 2, ord_5(2) = 4 → ΔL = 2, ΔK = 4

These three orderings happen to satisfy the multiplicative identity
exactly. For other (a, K_1, L_1), the identity fails (the implied ΔK
isn't a power of 2 mod the relevant modulus).

## Conclusion (NEW conjecture)

**Conjecture C-017**: The three cells (3, 5), (3, 13), (5, 3) are
the ONLY (a, b) with a, b odd ≥ 3 admitting two distinct (L, K)
tuples satisfying `2^K − a^L = b` with L ≥ 1, K > L.

These are precisely the cells with maximal "primary" cycle generation
in the C-011 framework. They constitute the small finite set of
"exceptionally cycle-rich" cells in the generalized Collatz family
(a · n + b with a, b odd).

This connects two pieces:
1. **Pillai/Mihăilescu Diophantine theory** (`2^K − a^L = c` has
   finitely many solutions for fixed c)
2. **C-011 primitive cycle classification** (cycles ↔ (L, K, composition)
   with `b | (2^K − a^L)`)

The intersection — cells where the Pillai equation has TWO solutions
— gives a tiny exceptional set in the cycle-classification framework.

## Reasoning
This is a small but clean structural finding. Whether it's truly
novel: the Pillai bound is classical (Mihăilescu theorem and
generalizations). The application to Collatz-type cycle structure
may be specific to this work — connecting two well-known pieces in
a way that gives a precise answer ("exactly these three cells").

The conjecture is falsifiable (find a fourth cell in extended search)
and precise (specific (a, b) list).

## Next
- Verify by independent enumeration at very large a, K, L (extending
  the search).
- Try to PROVE C-017 via Mihăilescu-style argument or Ku/Pillai
  results.
- Document in CONJECTURES.md as a candidate novel structural result.

## Linked
- (no archive — analysis is computational)
