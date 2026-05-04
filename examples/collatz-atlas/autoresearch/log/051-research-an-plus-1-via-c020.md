# res 051 — applying C-020 to the an+1 family

## What & why
Apply C-020 to enumerate cycles of T_{a, 1}(n) — the "an+1" generalization
of Collatz — for odd `a ∈ {3, 5, 7, 9, 11, 13, 15, 17, 25, 27}`. By C-020,
primitive cycles of `(a, 1)` at `(L, K)` exist iff `(2^K - a^L) | S(k, a, L)`
for some primitive composition k.

## Done
Sweep `L ≤ 12, K ≤ 22` for each odd a above. Enumerate primitive composition
orbits; for each, check the divisibility `(2^K − a^L) | S(k)`. Recover all
known small cycles plus any new ones in the search range.

Script: `archive/051-an-plus-1-enumeration.py`.

## Result

| a | non-trivial primitive cycles found in L≤12, K≤22 |
|---:|---|
| 3 | only the trivial `{1, 4, 2}` at (L=1, K=2). **No others** (consistent with Collatz conjecture, in this bound). |
| 5 | trivial `{1, 6, 3, 16, 8, 4, 2}` at (L=2, K=5); **13-cycle** `{13, 66, 33, ...}` at (L=3, K=7); **17-cycle** `{17, 86, 43, ...}` at (L=3, K=7). |
| 7 | only trivial `{1, 8, 4, 2}` at (L=1, K=3). |
| 9, 11, 13, 17, 25, 27 | no cycles found in bound. |
| 15 | only trivial `{1, 16, 8, 4, 2}` at (L=1, K=4). |

**Mersenne pattern:** `a = 2^k − 1` (i.e., a ∈ {3, 7, 15, 31, ...}) admit
the trivial cycle at (L=1, K=k) immediately, since 2^k = a + 1.

**5n+1 special structure:** N_a = 2^7 − 5^3 = 128 − 125 = **3**, the
smallest non-trivial (a, L, K) with N_a > 0 and N_a small relative to
typical S values. This smallness is *why* 5n+1 has multiple non-trivial
cycles — divisibility is easy when N_a is tiny.

## Why a=3 doesn't (in bound)

For `(3, 1)` at any (L, K) with `2^K > 3^L`, no primitive composition has
`(2^K − 3^L) | S(k, 3, L)` in the searched range. The closest "near miss"
is the (L=1, K=2) trivial cycle (N_a = 1, divisibility automatic). For
larger (L, K), N_a grows fast (N_a ≥ 2^L for K ≥ L+1, exponentially in L)
while S(k) for primitive k is bounded by `O(3^L · 2^K)` but the *specific*
divisibility is rare.

This is the **C-020-flavored reformulation of the Collatz conjecture**:
no primitive composition of any non-trivial `(L, K)` has its S-value
divisible by `2^K − 3^L`.

## Connection to atlas

The autoresearch atlas (137 variants) was built empirically; (5, 1) was
shown to have basin/divergence structure but the *number* of cycles
wasn't directly enumerated this way. C-020 gives a clean lookup: for any
(a, b) with b odd, total primitive cycles of length T = K+L is the count
of primitive composition orbits with `(2^K − a^L)/b | S(k)`.

## Conclusion
*Routine application of C-020.* Recovers known an+1 cycle structure
(trivial + the famous 5n+1 13/17 cycles) without surprises. The
Mersenne-pattern observation (`a = 2^k − 1` gives trivial cycle at L=1)
is folklore but emerges naturally.

The "why a=5 has non-trivial cycles and a=3 doesn't (in bound)" answer
is satisfyingly clean: smallness of `2^K − a^L` for some (L, K) is the
condition. For a=3, no small N_a; for a=5, N_a = 3 at (L=3, K=7).

## Reasoning
This closes the C-019 / C-019′ / C-020 trilogy. Together they describe:
- which cells (a, b) admit cycles at (L, K) [C-011 necessity];
- exactly how many on the m=1 hypersurface [C-019, C-019′, Lyndon-word
  closed form];
- how cycles distribute across off-hypersurface cells [C-020];
- and concrete instances for an+1 dynamics [this entry].

The whole framework is now: count of primitive cycles in (a, b) at length
T = K+L = (number of primitive compositions of (L, K) where
`(2^K − a^L)/b | S(k, a, L)`).

## Next
- The framework is complete enough to write up.
- Open theoretical question: prove the L'≥2 case of C-019' rigorously
  (the discrete-log angle from action 049).
- Possible exploration: the structure of `gcd(N_a, S(k))` as a function
  of k — i.e., for fixed (a, L, K), which orbits "land" at which divisor
  cells? Number-theoretically interesting (relates to multiplicative
  order of 2 mod various primes).

## Linked
- archive/051-an-plus-1-enumeration.py
