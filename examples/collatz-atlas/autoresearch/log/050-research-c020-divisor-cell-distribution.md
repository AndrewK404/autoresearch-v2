# res 050 — C-020: cycle-count distribution across divisor cells (off-hypersurface generalization)

## What & why
C-019′ (action 049) gave the exact primitive-cycle count for cells on the
m=1 hypersurface — `(a, b = 2^K − a^L)`. The natural generalization: what
is the cycle count for *any* cell `(a, b)` with `b | (2^K − a^L)` (i.e., m
arbitrary)? This includes the iconic open cell `(3, 1)` (classical
Collatz) and `(5, 1)` (5n+1, with known non-trivial cycles).

## Result — Theorem C-020 (cycle distribution across divisor cells)

For any odd a ≥ 3 and L, K ≥ 1 with `N_a := 2^K − a^L > 0`:

For each odd divisor `m` of `N_a`, the cell `(a, b = N_a / m)` admits
exactly

  **N(a, b, L, K) = #{ primitive rotation-orbit classes k of (L, K) : m | S(k, a, L) }**

primitive cycles of length K + L. Here S(k, a, L) = Σ_{i=0}^{L-1} a^{L-1-i}·2^{k_1+...+k_i}
is the cycle-equation sum.

**Corollaries:**

- **m = 1 (hypersurface):** N = L_{K,L} (Lyndon-word count). This is C-019′.
- **m = N_a (cell (a, 1)):** N = #{ primitive orbits k : N_a | S(k) }.
  This is precisely the divisibility condition behind the Collatz open
  problem: the absence of additional cycles in 3n+1 reduces to "no
  primitive composition has S(k) divisible by 2^K − 3^L".
- **Total cycles at (L, K) summed over all valid b:**
  Σ_{m | N_a, odd} N(a, N_a/m, L, K) = Σ_{orbits k} #{ odd divisors of gcd(N_a, S(k)) }.

## Empirical examples

Sample of off-hypersurface contributions (a, L, K → cell (a, b) → cycle
count via m):

| (a, L, K) | N_a | L_{K,L} | cell (a, b) | m | cycles |
|---|---:|---:|---|---:|---:|
| (3, 2, 6) | 55 | 2 | (3, 55) | 1 | 2 |
| (3, 2, 6) | 55 | 2 | (3, 11) | 5 | 1 |
| (5, 3, 7) | 3 | 5 | (5, 3) | 1 | 5 |
| (5, 3, 7) | 3 | 5 | **(5, 1)** | 3 | **2** ⟵ the 13- and 17-cycles of 5n+1 |
| (3, 4, 8) | 175 | 8 | (3, 175) | 1 | 8 |
| (3, 4, 8) | 175 | 8 | (3, 35) | 5 | 2 |
| (3, 4, 8) | 175 | 8 | (3, 25) | 7 | 1 |
| (3, 4, 12) | 4015 | 40 | (3, 4015) | 1 | 40 |
| (3, 4, 12) | 4015 | 40 | (3, 803) | 5 | 10 |
| (3, 4, 12) | 4015 | 40 | (3, 365) | 11 | 4 |
| (3, 4, 12) | 4015 | 40 | (3, 73) | 55 | 1 |
| (3, 4, 12) | 4015 | 40 | (3, 55) | 73 | 1 |

The (5, 1) row is the classical 5n+1 result reframed: **the m=3 cells'
primitive composition orbits** with `3 | S(k, 5, 3)` give the 13-cycle
(orbit (1,1,5)) and the 17-cycle (orbit (1,3,3)).

## Connection to the Collatz conjecture

For `(3, 1)` (classical 3n+1 problem), we'd need a primitive composition
k of some (L, K) with `(2^K − 3^L) | S(k, 3, L)`. The trivial cycle
{1,2,4} corresponds to (L=1, K=2): N_a = 4 − 3 = 1, S = 1, 1 | 1 ✓.

For any *other* primitive cycle, we'd need (L, K) with `2^K − 3^L > 1`
and `(2^K − 3^L) | S(k)` for some primitive k. **The Collatz conjecture
is exactly the assertion that this divisibility never holds for non-trivial
(L, K).**

This reformulation is well-known (it's essentially Steiner's argument /
Crandall's bound in modern form), but C-020 makes it a clean
combinatorial divisibility condition: the open problem reduces to
"`N_a` divides `S(k)` for no primitive composition k except the trivial
one".

## Status
**Surviving** — proven in closed form (the formula follows directly from
C-011 + the cycle equation + Möbius dedup). Empirically verified across
119 (a, L, K) cells with at least one non-trivial m value.

This is **not a novel mathematical theorem**. It's a clean combinatorial
restatement of the Belaga-Mignotte cycle equation parameterized by the
divisor lattice of N_a. The novelty lies in the explicit per-cell count
formula (S(k) divisibility), which makes the structure transparent.

## Reasoning
The natural endpoint of the C-019/C-019′ line. C-019 covers m=1 (the
"easy" cells where every composition contributes); C-019′ shows it's
exact at m=1 (no extras from alternate tuples at same T); C-020 covers
m > 1 (the "hard" cells where only some compositions contribute, via the
divisibility S ≡ 0 mod m).

Together, these give a complete picture of primitive cycle counts in
generalized Collatz cells, parameterized by (a, L, K) and the divisor
structure of N_a = 2^K − a^L.

The connection to the Collatz conjecture (the divisibility reformulation)
is the most attractive aspect: it gives an explicit combinatorial
condition that 3n+1 has no non-trivial cycles. This is folklore but
worth stating cleanly.

## Conclusion
**C-020 stands as a corollary completing the C-011 / C-019 / C-019′
framework.** Total primitive cycle count of (L, K) at any cell (a, b)
with b | N_a is determined by which primitive composition orbits k satisfy
m | S(k, a, L), where m = N_a/b. The Collatz conjecture is the absence of
such divisibility for (3, 1) at non-trivial (L, K).

## Next
- Look at the *total* primitive cycle count for (a, 1) cells across all
  (L, K) — this is the Collatz-conjecture-flavored question for general
  a. Empirically: (3, 1) has 1 cycle (trivial), (5, 1) has 1+2=3 known
  cycles (trivial plus two L=3 cycles), (7, 1) has only the trivial,
  (9, 1) has many...
- Investigate the structure of `gcd(N_a, S(k))` as a function of k —
  what determines which orbits "land" at smaller cells?

## Linked
- archive/050-off-hypersurface-count.py
- archive/050-general-m-count.py
