# Report — generalized Collatz dynamics, parameter atlas

## Task

Produce a falsifiable parameter atlas of the generalized Collatz family

  `T_{a,b}(n) = n/2 if n even,  a·n + b if n odd`   (a, b odd integers).

For each parameter set, classify the dynamics (all-converge to known cycle,
has additional cycle, has orbit unbounded up to horizon N), correlate the
classification with algebraic features (residues mod small primes, growth
rate of the average map, etc.), and propose falsifiable conjectures of the
form "for parameters in region R, behavior B holds." Maintain a research
log, a conjecture ledger with explicit falsification protocols, and a
prediction-vs-outcome record. Single-command reproducibility, fixed seeds,
laptop-scale (arbitrary-precision Python).

The bar for success: a small number of falsifiable empirical claims, each
with scope and evidence, plus the atlas in reusable form. *Even one new
candidate "tractable cousin" of Collatz would be a real contribution.*

Full brief: `TASK.md`.

## Main conclusion

**Starting point.** The brief (TASK.md) asked for a falsifiable atlas of the
family `T_{a,b}(n) = n/2 if even, a·n+b if odd` (a, b odd) and, ideally,
"even one new candidate tractable cousin of Collatz."

**Outcome (one-paragraph summary).** The autoresearch run produced a
genuinely new structural theorem (C-019): the primitive cycles of length
`K+L` of the cell `(a, b = 2^K − a^L)` — defined for any odd `a ≥ 3` and
positive integers `L, K` with `2^K > a^L` — are in explicit **bijection
with binary Lyndon words of length `K` with `L` ones**, and there are
exactly `L_{K,L} := (1/L)·Σ_{d|gcd(K,L)} μ(d)·C(K/d−1, L/d−1)` of them.
This produces an **infinite 2D lattice of tractable cousins of Collatz**
with explicit, combinatorially-given cycle counts; the previously
identified Catalan family is a corollary (the K = 2L−1 diagonal at a=3),
and a second Catalan family at K = 2L+1 falls out for free.

**Evidence.**
- **Proof sketch** (full in `autoresearch/CONJECTURES.md` C-019,
  `log/047-research-general-mequal1-theorem.md`,
  `log/048-research-lyndon-full-theorem.md`):
  1. b = 2^K − a^L is positive odd (even − odd, K ≥ 1, a odd).
  2. By construction `m := (2^K − a^L)/b = 1`, so by C-011 (proven
     necessary for b odd in `archive/014-c011-necessity-proof.md`),
     each composition `k⃗` of K into L positive parts yields a primitive
     cycle with explicit entry point
     `n₀(k⃗) = Σ_{i=0}^{L−1} a^{L−1−i} · 2^{k_1+…+k_i}`.
  3. `n₀(k⃗)` is a positive odd integer (first term odd, rest even).
  4. The cyclic group ℤ/L acts on compositions by rotation; rotation-
     fixed compositions correspond to imprimitive (shorter, repeated)
     cycles and are removed by Möbius inversion; the count of
     primitive orbits equals `L_{K,L}`. ∎
- **Empirical verification: 59/59 cells, no failures**, across
  a ∈ {3, 5, 7} and gcd(K, L) ∈ {1, 2, 3, 4, 5, 6}. Sample (a = 3):

  | L\K | 5 | 7 | 8 | 9 | 11 | 13 | 17 |
  |---|---|---|---|---|---|---|---|
  | 3 | 2 | 5 | 7 |   | 15 |   |   |
  | 4 |   | 5 |   | 14 | 30 | 55 |   |
  | 5 |   |   | 7 | 14 | 42 | 99 | 364 |
  | 6 |   |   |   |   | 42 | 132 | 728 |
  | 9 |   |   |   |   |   |   | 1430 |

  All entries match `L_{K,L}` exactly.
- **Catalan diagonals (corollary, C-018).**
  - `K = 2L − 1`: counts = `C_{L−1}` (Catalan). Verified for
    L = 3..9: 2, 5, 14, 42, 132, 429, 1430 in cells (3,5), (3,47),
    (3,269), (3,1319), (3,6005), (3,26207), (3,111389).
  - `K = 2L + 1`: counts = `C_L`. Verified for L = 1..7 in cells
    (3,5), (3,23), (3,101), (3,431), (3,1805), (3,7463), (3,30581).
- **Falsification protocol.** Find any cell `(a, 2^K − a^L)` with the
  count of primitive cycles of length `K+L` ≠ `L_{K,L}`. None found
  in 59 trials.

**How it compares to prior known results.**
- **Already known going in:** C-011 (cycle classification, proven
  necessary for b odd); the b-scaling embedding for inherited cycles
  (C-007′); per-cell empirical observations (C-001 a-axis convergence,
  C-013 lift, C-015 power-law decay, C-016 stopping time). These
  characterized convergence statistics but gave no closed-form cycle
  count outside hand-computed examples.
- **What's genuinely new:**
  1. C-019 — a single closed-form formula that enumerates the entire
     m=1 hypersurface across all (a, L, K). Previously, even the
     count for a single nontrivial cell (e.g. (3, 13) → 7 cycles)
     was a hand-crafted result (C-008).
  2. The Lyndon-word bijection itself — putting primitive Collatz
     cycles in correspondence with one of the most-studied objects
     in combinatorics on words. I have not seen this connection in
     the standard generalized-Collatz literature.
  3. The Catalan families (C-018, both K = 2L±1 diagonals at a=3) —
     concrete infinite families of tractable cousins, directly
     answering the TASK.md prompt.
- **Caveat.** The Lyndon-word count formula itself is classical;
  the novelty is the bijection with primitive Collatz cycles, not
  the formula. The theorem covers the m=1 slice only — m > 1 cycles
  (and the open Collatz problem at (3, 1)) require additional
  residue-class analysis and remain open.

---

## Steps of the model carried out

1. **Atlas construction (actions 001–016).** Built a reproducible
   parameter atlas covering 137 variants
   (a ∈ {1, 3, 5, 7, 9, 11, 13}, b ∈ [1, 51] odd) at S = 10⁵,
   H = 10¹³, T = 10⁵. Identified 171 primitive + 284 inherited cycles.
2. **Cycle classification (action 014).** Proved C-011 necessary for
   b odd via gcd propagation: every primitive cycle satisfies
   `b | (2^K − a^L)`. This is the structural backbone.
3. **Convergence statistics (actions 017–033).** Established C-013
   (per-seed lift–halving correlation, ~10–15% match to Brownian
   theory), C-015 (power-law `f ∝ S^{−c(a,b)}` with `c(a) ≈ (a-4)/(a-2)`),
   C-016 (stopping time `τ ≈ log₂(n)/|μ_T|`).
4. **Falsification cycle (actions 005–022).** Falsified C-002 strong,
   C-006 universal, C-006′, C-014 strong; reframed as C-006″ and C-007′
   with closed-form proofs.
5. **Hunt for cycle-rich cells (actions 040–044).** Systematic
   enumeration of `(a, b)` with `m = 1` for multiple `(L, K)` tuples;
   found exactly three "double-m=1" cells {(3,5), (3,13), (5,3)}
   (C-017).
6. **First Catalan family (action 045).** Noticed that for `K = 2L−1`,
   `gcd(K, L) = 1`, Burnside dedup gives `C(2L−2, L−1)/L = C_{L−1}`.
   Verified L=3..8 by direct sweep at (3, 2^{2L−1}−3^L).
7. **L=9 verification + b-typo correction (action 046).** Confirmed
   1430 cycles at (3, 111389), corrected b from log/045's 113213.
8. **Generalization to C-019 — gcd=1 case (action 047).** Tested
   `C(K−1, L−1)/L` across the (L, K) lattice for a ∈ {3, 5, 7}:
   42/42 cells matched. Discovered second Catalan family at K=2L+1.
9. **Strengthening via Möbius/Lyndon (action 048).** Extended to
   gcd > 1 via Möbius inversion (binary Lyndon-word count). Tested
   17 cells with gcd ∈ {2, 3, 4, 5, 6}: all matched. Total 59/59.
10. **Documentation.** Recorded C-019 (full Lyndon form) in
    `autoresearch/CONJECTURES.md`, demoted C-018 to corollary,
    rewrote README.md headline, updated MEMORY.md and log.tsv.

**Artifacts.** Atlas data: `atlas.py` + parquets in `autoresearch/archive/`.
Verification scripts: `archive/047-general-lattice.py`,
`archive/047-catalan-k-2lp1.py`, `archive/048-lyndon-full-lattice.py`,
`archive/046-catalan-l9-verify.py`. Full conjecture ledger:
`autoresearch/CONJECTURES.md`. Per-action logs: `autoresearch/log/`.
