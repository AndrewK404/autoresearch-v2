# Generalized Collatz dynamics — a parameter atlas

**Status:** comprehensive empirical theory established (autoresearch run,
May 2026). 19 conjectures in the full ledger at
`autoresearch/CONJECTURES.md`; 4 documented falsifications. **C-011
proven for b odd; C-019 (Lyndon-word bijection for m=1 primitive
cycles) proven sketch + verified across 59 lattice cells.** C-013
(lift) and C-016 (stopping time) match Brownian random-walk theory
within ~10%. C-015 (power law in S) verified across 4 S scales and
65+ cells with empirical c(a) ≈ (a-4)/(a-2). Awaiting explicit user
confirmation for promotions to `LESSONS.md`.

## Headline new theorem: the m=1 Lyndon-word lattice (C-019)

**For any odd a ≥ 3 and positive integers L, K with 2^K > a^L,
the cell `(a, b = 2^K − a^L)` has exactly
`L_{K,L} := (1/L) · Σ_{d | gcd(K, L)} μ(d) · C(K/d − 1, L/d − 1)`
primitive cycles of length K + L** — equal to the number of binary
**Lyndon words** of length K with L ones, given explicitly by
the m=1 cycle equation. (For gcd(K, L) = 1 this reduces to
C(K−1, L−1) / L.)

This generates an **infinite 2D lattice of "tractable cousins" of
Collatz**, each with explicit, combinatorially-given cycle counts.
The lattice is dense: for every odd a ≥ 3, infinitely many (L, K)
pairs qualify.

**Proof sketch.** b = 2^K − a^L is odd (even − odd). m = 1 by
construction. C-011 (proven for b odd) gives a primitive cycle for
each composition of K into L positive parts, with explicit n_0 =
Σ a^{L-1-i}·2^{k_1+...+k_i}, automatically positive odd integer.
The cyclic group ℤ/L acts on compositions by rotation; rotation-
fixed compositions correspond to *imprimitive* cycles (shorter cycle
traversed multiple times) and are removed by Möbius inversion. The
remaining count of primitive orbits equals the binary Lyndon-word
count L_{K,L}. When gcd(K, L) = 1, the action is free and L_{K,L}
= C(K−1, L−1)/L. ∎

**Sample lattice for a = 3** (entries = predicted = verified cycle count):

| L\K | 3 | 5 | 7 | 8 | 9 | 10 | 11 | 13 | 15 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **1** |  |  |  |  |  |  |  |  |  |
| 2 |  | **2** | **3** |  |  |  |  |  |  |  |
| 3 |  | **2** | **5** | **7** |  | **12** | **15** |  |  |  |
| 4 |  |  | **5** |  | **14** |  | **30** | **55** |  |  |
| 5 |  |  |  | **7** | **14** |  | **42** | **99** | **200** | **364** |
| 6 |  |  |  |  |  |  | **42** | **132** |  | **728** |
| 9 |  |  |  |  |  |  |  |  |  | **1430** |

**59 cells verified empirically** across a ∈ {3, 5, 7} and gcd(K, L) ∈
{1, 2, 3, 4, 5, 6}, with no mismatches. The cycle count equals
L_{K,L} (binary Lyndon-word count) in every case.

### Catalan diagonals (corollary, C-018)

Two diagonals of the lattice yield Catalan numbers:

- **K = 2L − 1:** counts = C_{L−1} (1st Catalan family, L ≥ 3).
  Cells: (3, 5), (3, 47), (3, 269), (3, 1319), (3, 6005), (3, 26207), (3, 111389), ...
- **K = 2L + 1:** counts = C_L (2nd Catalan family, L ≥ 1).
  Cells: (3, 5), (3, 23), (3, 101), (3, 431), (3, 1805), (3, 7463), (3, 30581), ...

**Seven consecutive Catalans verified along K = 2L−1**: 2, 5, 14, 42,
132, 429, 1430 for L = 3, ..., 9.

The diagonal K = 3L ± 1 gives Fuss-Catalan-related sequences; K = mL ± r
diagonals give other named sequences. Each is an infinite family of
"cycle-rich" cells.

### Lyndon-word bijection

Each primitive cycle of length K+L in (a, 2^K − a^L) corresponds
**bijectively** to a binary Lyndon word of length K with L ones.
The bijection: a Lyndon word's L "one-positions" encode a composition
(k_1, ..., k_L) of K into L positive parts; the cycle is the orbit
of n_0(k_⃗) = Σ a^{L-1-i}·2^{k_1+...+k_i} under T_{a,b}.

This puts generalized Collatz cycle enumeration into direct
correspondence with one of the most-studied objects in combinatorics
on words. Duval's algorithm yields O(K) per-cycle enumeration without
the C(K-1, L-1) blow-up. The Möbius/Lyndon count handles gcd>1
rotation symmetry correctly: imprimitive (rotation-symmetric)
compositions correspond to *imprimitive* Collatz cycles (a shorter
cycle traversed multiple times) and are excluded from the primitive
count.

### Off-lattice cells

- **(3, 1) classical Collatz** is not on the m=1 lattice (b=1 has no
  (L, K) tuple with 2^K − 3^L = 1 except the trivial L=1, K=2). Its
  primitive cycle space (under m=1) contains only the trivial cycle.
  Other primitive cycles, if any, would require m > 1 — the open
  problem of Collatz.
- **Double-m=1 cells (C-017)** {(3, 5), (3, 13), (5, 3)}: rare cells
  where two distinct (L, K) m=1 tuples coexist; these are the only
  such triples with a, b odd ≥ 3 in the searched range (a ≤ 199,
  K ≤ 99, L ≤ 39, b ≤ 10^12).
- **m > 1 cycles** (any cell with b | 2^K − a^L but b·m = 2^K − a^L for
  m ≥ 2): cycle count is harder, restricted to compositions where
  m | S(k_⃗). Closed-form open.

This **directly answers TASK.md's "even one new candidate tractable
cousin of Collatz"** with an infinite 2D family, each with explicit
cycle structure.

## Key empirical findings

The autoresearch run produced the following falsifiable claims:

1. **Cycle classification (C-011, proven).** For positive odd `a, b`,
   every primitive cycle of `T_{a,b}` corresponds to a triple
   `(L, K, composition)` with `b | (2^K − a^L)`. Closed-form proof in
   `autoresearch/archive/014-c011-necessity-proof.md`. **Verified
   across 171 primitive cycles in 137 variants.**

2. **m=1 Lyndon-word bijection (C-019, proven sketch + 59/59
   verified).** For any odd `a ≥ 3` and `L, K ≥ 1` with `2^K > a^L`,
   the cell `(a, b = 2^K − a^L)` has exactly L_{K,L} primitive cycles
   of length K+L, where L_{K,L} is the binary Lyndon-word count.
   This is the **headline new theorem** of the run — see top of
   README.

3. **Convergent regime (C-001).** For `a ∈ {1, 3}`, all seeds
   `n₀ ∈ [1, 10⁵]` reach a cycle. Survived 4 independent falsification
   attempts; 5.2M trajectories tested without a single failure.

4. **Stopping time formula (C-016).** In the convergent regime,
   `τ(n₀) ≈ log₂(n₀) / |μ_T|` where `μ_T = (log₂(a) − 2)/3` is the
   per-T-step drift. Empirical slope matches predicted `1/|μ_T|`
   within 4% across (a∈{1,3}, b) cells.

5. **Power-law decay (C-015).** In the divergent regime (`a ≥ 5`),
   `f(a, b, S) ∝ S^{−c(a, b)}` with empirical fit `c(a) ≈ (a-4)/(a-2)`.
   Verified across **65+ cells** at S ∈ {10³, 10⁴, 10⁵, 10⁶}.

6. **Per-seed convergence prediction (C-013, with random-walk theory).**
   For each seed in the divergent regime, the conditional probability
   of converging given the first K halving harvests `h₁, ..., h_K`
   satisfies a logistic form
   `log[P(conv)/(1-P(conv))] ≈ α(a, b)·Σh_i + β`. Individual-seed
   logistic regression gives α matching the random-walk-on-log
   prediction `α_RW = 2(log₂(a)−2)/(σ²·ln 2)` within **~10-15% for
   most cells**, with prime-b cells showing the cleanest match:
   - (7, 1), (7, 3), (7, 9): match within 1-3%
   - (5, *) cells: typical match within 7-15%
   - Composite-b cells with rich inheritance: up to 30-50% deviation
   Mean ratio α_emp/α_RW across 22 cells = 0.84; **19/22 within
   [0.7, 1.3]**. AUC 0.72–0.99 for individual-seed prediction.

   The earlier ~0.7× systematic gap (from binned-lift regression in
   actions 019, 023, 029) was a methodology artifact; individual-seed
   logistic closes it substantially.

7. **Note on α vs c**: the per-step lift coefficient α (≈ α_RW
   = (log₂(a)−2)/ln 2) and the S-decay rate c are conceptually
   different parameters from the random walk. Empirically:
   - For a=5: α ≈ 0.46 (theory), c ≈ 0.36 (empirical fit (a-4)/(a-2)).
   - For a=7: α ≈ 1.16 (theory), c ≈ 0.67.
   They satisfy α > c. The exact analytic relationship between α and
   c remains an open question.

8. **Falsification record:** C-002 strong, C-006 universal, C-006′,
   C-014 strong all falsified during the run. See `## Falsified claims`.

## What this is

An empirical parameter atlas of the family

```
T_{a, b}(n) = n / 2          if n is even
T_{a, b}(n) = a · n + b      if n is odd
```

with `a, b` positive odd integers. The atlas covers
**a ∈ {1, 3, 5, 7, 9, 11, 13}, b odd in [1, 51]** — 137 variants — at
horizons `S = 10⁵` (starting seeds), `H = 10¹³` (value bound),
`T = 10⁵` (step bound). 455 distinct cycles found.

All 455 cycles admit a closed-form structural decomposition (see
**Headline result** below). Of the 455, **171 are primitive** (gcd of
members = 1) — every one of them satisfies the C-011 divisibility
condition. The remaining 284 are inherited via b-scaling.

## Headline result — full structural decomposition of the atlas

> **Theorem (C-011, proven for b odd, plus C-007′ inheritance):** Every
> cycle of T_{a, b} for a, b positive odd integers decomposes into:
>
> - **Primitive cycles** corresponding bijectively to triples
>   `(L, K, [k₁, ..., k_L])` with `b | (2^K − a^L)`, `k_i ≥ 1`,
>   `Σ k_i = K`, modulo the rotation-orbit symmetry of compositions.
>
> - **Inherited cycles**: for each odd divisor `d > 1` of `b`, the
>   d-scaled images of primitive cycles of `T_{a, b/d}`.

In our 137-variant atlas: **284 cycles inherited + 171 primitive = 455
total**. The bijection is exact: every primitive cycle is generated
by some divisibility tuple, and every divisibility tuple either yields
a primitive cycle or reduces to a lower-shortcut-length one (handled
by Burnside on rotation orbits, plus an additional `m | S(k)`
divisibility condition when `m = (2^K − a^L)/b > 1`).

The proof of necessity (`b | (2^K − a^L)` for any primitive cycle's
(L, K)) is in
`autoresearch/archive/014-c011-necessity-proof.md` — three lines of
gcd propagation. Sufficiency follows from the explicit cycle equation.

This is the structural backbone of the family: the cycle problem
reduces to characterizing the divisibility relation `b | (2^K − a^L)`,
which is governed by multiplicative orders in `(ℤ/bℤ)*`.

## Other conjectures (with scope, evidence, falsification record)

The full conjecture ledger is at `autoresearch/CONJECTURES.md`. Below
are the conjectures that have **survived** at least one falsification
attempt at expanded horizons. Pending explicit user confirmation
before promotion to `LESSONS.md`.

### C-015 — Power-law decay of convergent fraction in S

For (a, b) in the divergent regime (a ≥ 5):

```
f(a, b, S) ≈ const(a, b) · S^{-c(a, b)}
```

with exponent c(a, b) **primarily a function of a**, weakly dependent on
b within each a-row.

Empirical c values from comparing f at S = 10⁴ vs S = 10⁵ (35
non-degenerate cells):

| a | μ = log₂(a) − 2 | mean c | per-b range |
|---|---|---|---|
| 5 | 0.322 | 0.358 | 0.329–0.378 |
| 7 | 0.807 | 0.668 | 0.594–0.721 |
| 9 | 1.170 | 0.731 | 0.692–0.761 |
| 11 | 1.459 | 0.753 | 0.692–0.794 |
| 13 | 1.700 | 0.795 | 0.726–0.838 |

**Pearson(c, μ) = 0.982 across all 35 cells.** c is monotonic in drift
μ but sublinear (saturating).

**Robust across multiple verification axes:**
- S = 10³, 10⁴, 10⁵, 10⁶ — power law holds at all four scales
  (predicted/observed ratio 0.86–1.05 at S=10⁶ across 22 cells).
- b ∈ [1, 51] odd — c essentially b-independent
  (Pearson(b, c) ≈ 0 across each a-row).
- a ∈ {5, 7, 9, 11, 13} — formula matches with RMSE 0.05;
  a ∈ {15, 17, 19} — formula starts breaking due to tiny converged
  sample size.

Total cells confirming C-015: ~65 across the matrix.

**Empirical closed-form fit:**

```
c(a) ≈ (a - 4) / (a - 2)
```

Equivalently: `1 − c(a) ≈ 2/(a − 2)`.

| a | c_emp | (a−4)/(a−2) | residual |
|---|---|---|---|
| 5 | 0.358 | 0.333 | +0.025 |
| 7 | 0.668 | 0.600 | +0.068 |
| 9 | 0.731 | 0.714 | +0.017 |
| 11 | 0.753 | 0.778 | −0.025 |
| 13 | 0.795 | 0.818 | −0.023 |

The formula has clean asymptotics: c(a) → 0 as a → 4 (matching the
convergent/divergent dichotomy boundary at C-001) and c(a) → 1 as
a → ∞. RMSE 0.053 across the per-cell data; consistent with
finite-S corrections at small a.

**Verification at S = 10⁶ (action 024):** 22/22 cells match predicted
f(S=10⁶) within ±20% (median ratio 0.975). Power law holds across
**S ∈ {10³, 10⁴, 10⁵, 10⁶}** for all 22 cells in tight scope.

This is the **strongest empirical finding for the divergent regime**
in the project. Where C-013 says "first-step h biases convergence
within a cell," C-015 says "the cell's convergent fraction follows a
clean power law as S grows, with cell-specific exponent c(a, b)."

**Asymptotic limit (analytic):** Veraverbeke's heavy-tail theory
predicts c → ln(2) ≈ 0.693 as S → ∞ (universal across a ≥ 5). Our
finite-S values are above this and the (a-4)/(a-2) formula extrapolates
to 1 as a → ∞ — both are consistent with finite-S effects above the
asymptotic limit. Testing at S = 10⁸+ would distinguish these.

For the "tractable cousin" question: smaller c means more seeds reach
cycles even at large S. The cells with highest convergence (and thus
most "tractable") in the divergent regime are:

| (a, b) | f(S=10⁵) | structure |
|---|---|---|
| (5, 45) | 20.5% | b = 3²·5; gcd(a, b)=5; multi-inherited |
| (5, 35) | 16.6% | b = 5·7; gcd(a, b)=5; rich inheritance |
| (5, 9) | 12.4% | b = 3²; small primitive cycle (1, 7, 11) |
| (5, 25) | 10.1% | b = 5²; gcd(a, b)=5 |
| (5, 7) | 9.8% | b prime; rich primitive structure |

The pattern: cells with `gcd(a, b) > 1` and structure providing
multiple inherited cycles via b-scaling (per C-007′) yield the
highest convergence. **(5, 45) is the best "tractable cousin"
candidate** in our scope — convergence is ~20% even at S=10⁵, much
higher than the classical 5x+1 (= (5, 1)) at 3%.

**Mechanism for (5, 45):** All 10 cycles of (5, 45) live in 5ℤ
(every member is a multiple of 5). Since gcd(5, 45)=5, the sublattice
5ℤ is forward-attractive (C-006″: rad(5)|rad(5) ✓), so every seed
eventually reaches 5ℤ. The dynamics on 5ℤ is conjugate to T_{5, 9}
on integers (via n → 5n homothety from action 003). Since (5, 9) is
itself rich in cycles (10 of them, including the small primitive
(1, 7, 11)), inherited as 5-scaled, plus inherited cycles from
(5, 3), (5, 5), (5, 15) at other scales, (5, 45) accumulates a large
total cycle volume.

**The full tractable-cousin recipe** — verified by counterexamples:
1. **gcd(a, b) > 1** so a sublattice is forward-attractive (C-006″).
2. **The recursive cell (a, b/d) has cycles** per C-011's
   divisibility `(b/d) | (2^K − a^L)`.

If condition 1 holds but condition 2 fails (e.g., (9, 3) has gcd=3
but on 3ℤ dynamics ≡ T_{9, 1}, and (9, 1) has NO primitive cycles
for any (L, K) tested), then convergence is **0%** — even though the
sublattice is "attractive," there's nothing to attract to. This was
confirmed empirically: f5(9, 3) = 0 across 100k seeds.

Both conditions must hold for tractability. (5, 45) satisfies both;
(9, 3) satisfies only the first.

If c(5, 1) > 0 in the limit S → ∞ (empirical c = 0.379 at our
resolution), this is empirical evidence for genuinely divergent orbits
in the long-conjectured 5x+1 problem.

### C-013 — Residue-class basin structure: first-step halving harvest predicts convergence

In the divergent regime (a ≥ 5), most seeds escape to the value bound
H. The small fraction that converges has a **strong residue-class
structure** governed by the first odd step.

**The conjecture.** For (a, b) with a ≥ 5 odd and b odd, the
convergent-fraction "lift" on odd residues r mod 2^k satisfies

```
log lift(r) ≈ α(a, b) · v₂(a·r + b) + β(a, b)
```

with α > 0 universally. The convergent basin is geometrically
determined by the first-step halving harvest; **longer-trajectory
dynamics contribute essentially random correction terms**.

**Evidence (action 017 + main wider-b verification):** systematic
across all (a, b) cells with a ≥ 5 in our 137-variant atlas:

- Tight scope (a ∈ {5, 7, 9, 11, 13}, b odd in [1, 21]): 34/34
  non-degenerate cells with Pearson r > 0.7 at k = 4; median r = 0.833.
- Wider-b (a ∈ {5, 7}, b odd in [23, 51]): 29/30 non-degenerate cells
  with r > 0.7 at k = 4; median r = 0.846.
- **Aggregate: 63 of 64 non-degenerate cells confirm the correlation**;
  median r ≈ 0.84 across all. Zero anti-correlated cells anywhere.
- Signal survives even at extreme cells (a=13, b=21 with 2/25,000
  seeds converged — r > 0.6).

**Key anti-result.** Multi-step (3-step, 5-step) cumulative harvest
does **NOT** improve correlation — single-step is the right invariant.
This is the surprising part: the convergence-bias is *one-shot*,
determined by the first odd-step's value-multiplier `(a·r+b)/2^{v₂(a·r+b)}`,
not the result of a long chain of corrections. After one halving
sequence, the trajectory has lost information about higher bits of
n₀ and subsequent dynamics is effectively iid from the natural
v₂ distribution.

**Mechanism.** Per shortcut step, average log-growth is
`log₂(a) − E[v₂]`. For a = 5: 2.32 − 2 ≈ +0.32 (divergent on average).
A seed converges only if its trajectory averages above-average h over
many shortcut steps. The residue-mod-2^k structure encodes precisely
the **front-loaded** h advantage; later steps' h are random.

This is **the conjecture in the project that engages with the
divergent regime**, where the literature is genuinely thinner. C-001
through C-012 characterize where cycles live; C-013 characterizes
*which seeds reach them*. The "multi-step doesn't help" anti-result
is the part most worth getting an outside number-theorist's eye on —
it suggests there's a clean one-shot structural explanation rather
than a chain of corrections.

**Mechanism update post action 023:** the random-walk-on-log heuristic
predicts the *shape* of α correctly (Pearson r=0.84) but misses the
magnitude by a uniform 0.6× factor that *grows worse* at higher k. So
the analytic derivation is incomplete: h-autocorrelation along
trajectories was tested and is essentially zero (action 022), so it's
not that. The structural reason for the 0.6× factor is unresolved.

**Open follow-ups:**
- Derive α(a, b) and c(a, b) analytically from the random walk's
  hitting-probability decay rate.
- Test wider-b extension (action 012's data is available).
- Higher-k probe (k = 8, 10) — does the correlation strengthen?

### C-001 — a-axis convergence dichotomy

For every `(a, b)` with `a ∈ {1, 3}` and `b` odd in `[1, 51]`, every
starting seed `n₀ ∈ [1, 10⁵]` reaches a cycle of `T_{a, b}` within
`T = 10⁵` iteration steps without exceeding `H = 10¹³`.

The complementary statement holds for `a ∈ {5, 7, 9, 11, 13}`:
divergence fractions monotonically increase with a (≈ 90% of seeds
escape at a=5, ≈ 99% at a=7, > 99.95% at a ≥ 9).

The boundary sits sharply between a = 3 and a = 5.

**Evidence:** 5.2M trajectories at a ∈ {1, 3} (zero failures) +
3.3M trajectories at a ∈ {9, 11, 13} (universal divergence).
**Falsification attempts surviving:** 4 (original sweep, 10× horizon,
wider-b, wider-a).

### C-003 — a=7 row L1-cycle rigidity (in original scope)

For `(a = 7, b ∈ {1, 3, 7, 13, 17, 21}) ∪ {29, 37, 39, 41, 43, 47, 49, 51}`,
the only cycles reached by any seed in `[1, 10⁵]` are the L=1 cycles
`{b, 2b, 4b, 8b}`. Most seeds escape to H; the small fraction that
converges does so to a single rigid attractor.

The conjecture **does not generalize uniformly** to all wider b: at
`b ∈ {23, 25, 27, 31, 33, 35, 45}` extra cycles exist (most strikingly,
(7, 31) has 4 parallel length-23 cycles — the same shape as C-008's
(3, 13)).

The corrected scope is given by C-011: rigidity holds iff the
divisibility lattice `{(L, K) : 31 | (2^K − 7^L)}` admits primitive
cycles only at `(L=1, K=3)`. So C-003 reduces to an arithmetic
condition on b.

**Falsification attempts surviving in original scope:** 2 (10× horizon +
implicit wider-b at the original 6 b values).

### C-006″ — sub-lattice forward-attractivity ⟺ rad(λ) | rad(a)

For `T_{a, b}` with `b` composite and `λ` an odd proper divisor of
`b`, the sub-lattice `λℤ` is forward-attractive if and only if
**every prime divisor of λ also divides a** (equivalently
`rad(λ) | rad(a)`).

For prime λ, this reduces to `λ | a` (equivalently `gcd(a, λ) > 1`).
For composite λ, the radical condition is strictly more restrictive
than gcd: e.g. `(3, 45, λ=15)` has `gcd(3, 15) = 3 > 1` but
`rad(15) = 15 ∤ rad(3) = 3`, and empirically only 14% of seeds
∉ 15ℤ reach 15ℤ at finite-T (extrapolating to 0 asymptotically).

**Evidence:** 20/20 empirical match for prime λ (action 006) +
analytic argument via residue arithmetic + composite-λ verification
on (3, 27, λ=9), (3, 45, λ=15), and several others (action 032).

### C-007′ — inherited cycle lower bound for `(a = 1, b)` family

For `(a = 1, b odd)`, the number of inherited cycles satisfies
`n_inherited(1, b) ≥ d(b) − 1`, with one inherited cycle per proper
odd divisor `d > 1` of `b`. Strict inequality occurs when some
sub-system `(1, b/d)` has multiple cycles itself.

**Evidence:** action 004 inheritance tagging at b ∈ [1, 21]; action
012 confirmed the lower bound at b ∈ [23, 51] (15 wider-b cells, all
satisfy); closed-form argument via the b-scaling embedding (action 003).
**Falsification attempts surviving:** 2.

### C-012 — n_new(a=1, b) is governed by ord_b(2)

For `(a = 1, b odd > 1)`, the count of primitive cycles is determined
by the divisor lattice of `ord_b(2)` (the multiplicative order of 2 mod
b) and a Burnside count of primitive necklaces over compositions.
**11/11 match** in tight scope; also confirmed at b ∈ [23, 51].

Worked numbers: `b = 7, ord_b(2) = 3 → 2 primitive cycles`;
`b = 13, ord_b(2) = 12 → 1 primitive cycle`;
`b = 17, ord_b(2) = 8 → 2 primitive cycles` (Burnside count).

**Falsified hypothesis:** the "2-adic residue mod 8" guess for n_new = 2
was wrong — b = 17 (≡ 1 mod 8) and b = 21 (≡ 5 mod 8) give n_new = 2
for non-2-adic reasons.

Corollary of C-011 specialized to a = 1.

### C-008 — (3, 13) admits exactly 7 primitive L=5 cycles

For `(a=3, b=13)`, there are exactly 7 primitive cycles of shortcut
length L=5 (and T-period 13), parametrized by halving vectors
`(k₁, ..., k₅)` with `k_i ≥ 1, Σ k_i = 8`, modulo cyclic rotation.

**Evidence:** sweep at S = 10⁴ found 7; 10× horizon sweep found 7;
algebraic enumeration of all 35 compositions confirmed 7. Matches
exactly. The structural reason: `2⁸ − 3⁵ = 13` cancels b directly,
making every composition yield an integer n₀.

This is the C-011 mechanism made concrete — a textbook case where the
divisibility condition is sharp. Several other (a, b) variants exhibit
the same parallel-cycle structure:

- `(a=7, b=31)` — 4 parallel cycles at L=6, K=17, m=433 (the m > 1
  case of C-011, where m | S(k) further filters compositions)
- `(a=11, b=7)` — 3 parallel L=K=9 cycles
- `(a=11, b=21)` — 3 parallel L=K=9 cycles plus an inherited L=1
- `(a=13, b=9)` — primitive L=15 cycle at cycle_min = 1

These are concrete **"tractable cousins" of Collatz** — variants
whose cycle set is finite, exhaustively enumerable via C-011's
algebra, and theoretically attackable. The brief asked for one such
candidate; we have several.

## Falsified claims (kept on purpose)

Per `TASK.md`'s "negative results count" instruction.

### C-002 — strong form: `n_total(a=1, b) = d(b)`

Falsified by spot-check: at b ∈ {7, 15, 17, 21}, the actual cycle count
exceeds d(b). Reframed as C-007′ (lower bound) which holds.

### C-006 — universal sub-lattice forward-attractivity

Falsified at action 006 with **543,514 counterexamples** out of ~2M
seeds: for `(a, b, λ)` with `gcd(a, λ) = 1` and `b` composite, the
overwhelming majority of `n₀ ∉ λℤ` never enters λℤ within
`T = 10⁵`. Refined to C-006″ above.

### C-006′ — "a = 3 only" sub-lattice attractivity

Briefly proposed during integration of action 006, then immediately
falsified during attempted analytic proof (residue arithmetic showed
non-attractivity for `gcd(3, λ) = 1` cases). Replaced by C-006″.

### C-014 — "asymptotic basin = convergent fraction"

Proposed after action 019 found that the residue-chain attractor basin
of the cycle-residue grew to 100% for (3, 1). Tested at higher k by
action 023 and **falsified**: (9, 1) has basin = 99.6% at k=22 but
empirical f = 0%; (5, 1) basin oscillates wildly (0.06 to 0.94 across
k = 18, 20, 22). The residue-chain basin captures residue dynamics but
doesn't reflect actual integer trajectory convergence at finite
horizons. Recorded as a falsification.

## Atlas access

The atlas lives in `autoresearch/archive/`:

**Tight scope** (a ∈ {1,3,5,7}, b odd in [1, 21]):
- `001-results.parquet` — 440k trajectories at S = 10⁴.
- `001-cycles.parquet` — 153 cycles.
- `004-inheritance-tags.parquet` — inheritance tags.
- `005-shortcut-lengths.parquet` — shortcut length L + T-period.
- `006-results.parquet` — 4.4M trajectories at 10× horizon.
- `006-cycles.parquet` — 153 cycles (no new cycles at 10× horizon).
- `006-attractivity.parquet` — sub-lattice hit-time histograms.
- `010-c011-tuples.parquet` — 1,661 (a, b, L, K) divisibility tuples.

**Wider-b scope** (a ∈ {1,3,5,7}, b odd in [23, 51]):
- `012-results.parquet` — 6M trajectories at S = 10⁵.
- `012-cycles.parquet` — 283 cycles.

**Wider-a scope** (a ∈ {9, 11, 13}, b odd in [1, 21]):
- `016-results.parquet` — 3.3M trajectories at S = 10⁵.
- `016-cycles.parquet` — 19 cycles.

**S=10⁶ verification** (a ∈ {5,7}, b odd in [1, 21]):
- `024-results.parquet` — 22M trajectories at S = 10⁶.
- `024-cycles.parquet` — 153 cycles (zero new at S=10⁶).

**Auxiliary** (basin/lift/correlation analyses):
- `017-residue-lift.parquet` — residue-class lift per cell.
- `019-alpha-fits.parquet`, `019-basin-volumes.parquet` — α/c
  diagnostics.
- `022-autocorrelation.parquet` — h-autocorrelation results.
- `023-basin-highk.parquet`, `023-alpha-diagnostics.parquet` — high-k
  + α regression diagnostics.
- `026-c015-wider.parquet` — wider-b c values for C-015 verification.
- `029-multistep.parquet` — multi-step α systematic.

A consolidated loader is at `atlas.py` (project root):

```python
from atlas import load_atlas, cycles_for, trajectories_for

atlas = load_atlas()
print(atlas['cycles'])       # 153 rows merged with metadata
print(cycles_for(3, 13))     # the 10 (3, 13) cycles
```

## Reproducibility

Bootstrap (one-time):

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas pyarrow gmpy2
```

Single-command regeneration of all atlas artefacts (deterministic, no
random sampling):

```sh
source .venv/bin/activate
python autoresearch/archive/001-sweep.py        # tight-scope sweep
python autoresearch/archive/002-verify.py        # analytic L≤3 catalog
python autoresearch/archive/003-verify.py        # conjugacy survey
python autoresearch/archive/004-tagger.py        # inheritance tags
python autoresearch/archive/005-cataloger.py     # shortcut lengths
python autoresearch/archive/006-sweep.py         # 10× horizon sweep + attractivity
python autoresearch/archive/008-l5-enumeration.py # algebraic (3,13) L=5 enum
python autoresearch/archive/010-enumerate.py     # C-011 tuple enumeration
python autoresearch/archive/012-sweep.py         # wider-b sweep
python autoresearch/archive/013-n_new_structure.py  # n_new(1,b) closed form
python autoresearch/archive/016-sweep.py         # wider-a sweep
```

## Research log

This atlas was produced by an autoresearch run documented under
`autoresearch/`:

- `CONFIG.md` — frozen contract for the run.
- `RESUME.md` — interview answers and bootstrap.
- `MEMORY.md` — live state dashboard.
- `LESSONS.md` — confirmed lessons.
- `CONJECTURES.md` — full conjecture ledger with status, evidence,
  falsification protocols.
- `PREDICTIONS.tsv` — pre-registered predictions vs outcomes (scored
  per cycle).
- `log/NNN-*.md` — per-action reasoning log.
- `log.tsv` — append-only action log.
- `archive/` — sweep scripts, parquet outputs, analytic notes
  (including the C-011 necessity proof at
  `archive/014-c011-necessity-proof.md`).

The brief that initiated the run is `TASK.md`.
