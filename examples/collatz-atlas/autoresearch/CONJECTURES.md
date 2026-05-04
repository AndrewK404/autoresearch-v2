# CONJECTURES

The conjecture ledger. Every empirical claim that might end up in the
final `README.md` deliverable starts here as a numbered conjecture, lives
through challenges, and either gets falsified, survives, or is promoted to
`LESSONS.md` once the user explicitly confirms it as solid (per
`CONFIG.md ## Done criterion`).

## Status legend

- **proposed** — conjecture stated, evidence cited, no falsification
  attempts yet.
- **probed** — at least one falsification attempt run; survived. Not
  enough to promote.
- **surviving** — multiple independent falsification attempts run
  (expanded horizons, conjugacy challenges, edge-case sweeps); all
  survived.
- **falsified** — counterexample found. Keep the entry — falsifications
  are findings.
- **promoted** — user has explicitly confirmed; written into
  `LESSONS.md`. The entry stays here as a reference.

## Discipline

1. **Scope is mandatory.** "All orbits converge" is not a conjecture; it
   is a wish. "For (a, b) ∈ R, every starting seed in [1, S] reaches the
   trivial cycle within T steps and without exceeding H" is a
   conjecture.
2. **At least one falsification attempt before status moves past
   proposed.**
3. **Conjugacy check is mandatory before claiming novelty.** Per action
   003: zero full conjugacies in our scope. But sub-system parents
   apply: a cycle of (a, b) whose members all lie in λZ for some λ > 1,
   λ | b, is the λ-scaled image of a (a, b/λ) cycle and must be tagged
   `inherited`, not `new`.
4. **Falsifications are first-class.** Counterexamples logged with the
   same care as confirmations.

---

## Ledger

### C-001 — a-axis convergence dichotomy in the tight scope (extended)

**Status:** surviving (4 independent falsification attempts: original
sweep S=10⁴, 10× horizon S=10⁵, wider-b S=10⁵ b∈[23, 51], wider-a
test on a∈{9,11,13} confirming complementary divergence)
**First proposed:** action 001 (`log/001-research-opening-sweep.md`)
**Probed in:** action 006 (`log/006-research-10x-horizon-and-attractivity.md`),
action 012 (`log/012-research-wider-b-sweep.md`),
action 016 (`log/016-research-wider-a-sweep.md`)

**Scope (parameters):** a ∈ {1, 3}, b odd in [1, 21].
**Scope (horizons, original):** S = 10⁴, H = 10¹², T = 10⁴.
**Scope (horizons, expanded):** S = 10⁵, H = 10¹³, T = 10⁵.

**Statement:** For every (a, b) with a ∈ {1, 3} and b ∈ {1, 3, 5, 7, 9,
11, 13, 15, 17, 19, 21}, every starting seed n₀ ∈ [1, S] reaches a
cycle of T_{a,b} within T iteration steps without any trajectory value
exceeding H. The complementary statement for a ∈ {5, 7} is empirically
false at the original horizon (and the falsification gets stronger at
10× horizon): a majority of seeds exceed H for most a ∈ {5, 7} variants.

**Supporting evidence:**
- `autoresearch/archive/001-results.parquet` — 220k trajectories for
  a ∈ {1, 3}, all `outcome = cycle`.
- `autoresearch/archive/006-results.parquet` — 2.2M trajectories at
  10× horizon, all `outcome = cycle`. Zero falsifiers across the
  expanded sweep.

**Falsification protocol:**
- Attempt 1 (action 006, ✓ done): 10× horizon sweep. **Survived** — zero
  seeds in [1, 10⁵] exceed H = 10¹³ for any (a ∈ {1, 3}, b in scope).
- Attempt 2 (action 012, ✓ done): wider b range b ∈ {23, 25, ..., 51}.
  **Survived** — 3M trajectories at a ∈ {1, 3}, all reach a cycle.
- Attempt 3 (action 016, ✓ done): wider a range a ∈ {9, 11, 13} —
  tests the *complementary* claim. **Survived** — divergence holds for
  all a ≥ 5 odd, with monotone decrease in convergence fraction
  (0.045% / 0.035% / 0.016% for a = 9, 11, 13). The a-axis transition
  sits at a = 3/5 boundary, confirmed.
- Attempt 4 (planned, future): seeds [10⁵, 10⁷] for selected (a, b)
  pairs, particularly (3, 13) and (3, 21).

**Conjugacy check:** none of the a ∈ {1, 3} cells reduce to each other
under the normal form (action 003); the conjecture is non-trivial across
all 22 cells.

**Notes:**
- This conjecture deliberately mirrors what Collatz-on-3x+1 says
  empirically; the *novelty* is that it is uniform across the b range
  and the a=1 row, not just (a=3, b=1).
- The conjecture might decompose: maybe a=1 has its own clean
  convergence reason (b-scaling on multiple gcd-classes; see C-002), and
  a=3 has its own. Falsification at the boundary should split it if so.

---

### C-002 — multi-attractor structure on a=1 tracks divisor structure of b (strong form: =d(b))

**Status:** falsified (strong form). Replaced by C-007.
**First proposed:** action 001 (`log/001-research-opening-sweep.md`)
**Falsified in:** main spot-check immediately after action 003
integration (one-line query against `001-cycles.parquet`).

**Scope (parameters):** a = 1, b odd in [1, 21].
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement (strong form):** number of distinct attractor cycles reached
from seeds in [1, 10⁴] equals d(b).

**Counterexamples:**
| b | observed | d(b) | match? |
|---|---|---|---|
| 1 | 1 | 1 | ✓ |
| 3 | 2 | 2 | ✓ |
| 5 | 2 | 2 | ✓ |
| 7 | **3** | 2 | ✗ |
| 9 | 3 | 3 | ✓ |
| 11 | 2 | 2 | ✓ |
| 13 | 2 | 2 | ✓ |
| 15 | **5** | 4 | ✗ |
| 17 | **3** | 2 | ✗ |
| 19 | 2 | 2 | ✓ |
| 21 | **6** | 4 | ✗ |

The mismatch at b ∈ {7, 15, 17, 21} comes from cycles at shortcut length
L ≥ 2 (eg the (1, 5)-cycle on (a=1, b=7) at k=(1,2)) that are **not**
b-scaled images of any (a=1, b/d) cycle. The strong claim "exactly d(b)"
is wrong: extra non-inherited cycles exist.

**What survives:** observed cycle count ≥ d(b) in every case. Each
divisor d | b *does* contribute at least the inherited cycle (the
d-scaled image of (1, b/d)'s trivial cycle). The d(b) bound is a lower
bound, not an equality.

**Reframed as C-007.**

**Notes:**
- Caught by main on its own spot-check, before the analyst pass —
  good. The lesson: verify before publishing a numerical claim, even in
  a draft conjecture.

---

### C-003 — a=7 row has rigid single-cycle-of-length-4 sub-pattern (in original scope)

**Status:** surviving in original scope (b ∈ {1, 3, 7, 13, 17, 21});
does **not** generalize uniformly to wider b — at b ∈ {23, 25, 27, 31,
33, 35, 45} the rigidity breaks. Refined as a number-theoretic
condition: holds for b iff the divisibility lattice
`{(L, K) : b | (2^K − 7^L), L ≥ 1, K ≥ L}` admits primitive cycles
only at (L=1, K=3).
**First proposed:** action 001 (`log/001-research-opening-sweep.md`)
**Probed in:** action 006 (10× horizon — held in original scope),
action 012 (wider b — broke for 7/15 new b values).

**Scope (parameters):** a = 7, b ∈ {1, 3, 7, 13, 17, 21}.
**Scope (horizons, original):** S = 10⁴, H = 10¹², T = 10⁴.
**Scope (horizons, expanded):** S = 10⁵, H = 10¹³, T = 10⁵.

**Statement:** For (a = 7, b) with b in the listed set, the dynamics on
[1, 10⁴] produce exactly one cycle, and that cycle has length 4 (i.e. 1
odd step + 3 halvings = 4 raw T-steps). The vast majority of seeds
escape to H.

**Supporting evidence:**
- Action 001 summary report.
- Action 002 catalog: each of these (7, b) has only the L1 cycle
  with k = 3, n = b (cycle = {b, 8b, 4b, 2b}).

**Falsification protocol:**
- Attempt 1 (planned): query `001-cycles.parquet` to confirm exactly
  one cycle and length 4 for each of the 6 cells.
- Attempt 2 (action 006, ✓ done): 10× horizon sweep. **Survived** — zero
  new cycles for any (7, b) cell in scope; the L1 cycle remains the
  only one reached.

**Conjugacy check:** these (7, b) are not pairwise conjugate; (7, 21)
and (7, 7) are scalings of (7, 1), so their L1 cycles are the b-scaled
{b, 8b, 4b, 2b}. The "rigid pattern" subsumes inheritance — the *sweep-
visible* cycles are scaled copies of (7, 1)'s cycle.

**Notes:**
- The phrasing "no new cycle visible up to (S, H, T)" is the right one;
  the conjecture does not claim absolute non-existence, only empirical
  absence at the probed scale.

---

### C-004 — (3, 13) carries a structured family of L=5 primitive cycles

**Status:** probed (one structural pass run; survives and is upgraded)
**First proposed:** action 001 (`log/001-research-opening-sweep.md`)
**Refined:** action 005 (`log/005-research-l4plus-catalog.md`)

**Scope (parameters):** (a, b) = (3, 13). Comparison: all other a=3
cells.
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement (refined):** (3, 13) carries 10 distinct cycles in the sweep,
9 of which are primitive (gcd of members = 1). Of those 9, **7 share
the exact shape (shortcut length L = 5, T-period = 13)**, with cycle_min
values 211, 227, 251, 259, 283, 287, 319 — distinct residues mod 13
(specifically {3, 6, 4, 12, 10, 1, 7}, covering 7 of the 12 nonzero
residues). The 7 cycles are a structured family parametrized by halving
vector (k₁, ..., k₅) summing to 8, of which 7 distinct vectors yield
positive odd integer solutions of the L=5 cycle equation
`n₀·(2⁸ − 3⁵) = 13·(3⁴ + 3³·2^{k₁} + 3²·2^{k₁+k₂} + 3·2^{k₁+k₂+k₃} + 2^{k₁+k₂+k₃+k₄})`.

**Supporting evidence:**
- Action 001 summary: cycle counts per a=3 row.
- Action 002 catalog: only 2 cycles at L ≤ 3 — the gap is at higher
  shortcut length.

**Falsification protocol:**
- Attempt 1 (planned, action 005): list every cycle of (3, 13) by
  members and length, look for explanation (residue structure mod 13,
  mod 3, mod 6, etc.).
- Attempt 2 (planned, action 006): re-run a high-horizon sweep on
  *only* (3, 13) at S = 10⁵, H = 10¹³ — does the cycle count grow,
  stay at 10, or do new cycles appear?
- Attempt 3: extend the a=3 row to b ∈ {23, 25, 27, 29, 31, 33, 35, 37,
  39, 41, 43, 45} — does another b match or exceed 13's richness, and is
  there a residue-class explanation?

**Conjugacy check:** (3, 13) has b prime, so no nontrivial scaling
parent. Its cycle richness is not inheritance.

**Notes:**
- The structural-family upgrade from "anomalous" is a real finding.
  Action 005 verified the L=5, t_period=13 shape across all 7 cycles.
  The cycle_min residues mod 13 covering 7 of 12 nonzero residues is
  the next thing to investigate — does (3, 13) admit *exactly* 7
  primitive L=5 cycles, or could there be more at higher seeds?
  Action 006 (10× horizon) will tell.

**Supporting evidence:**
- `autoresearch/archive/005-shortcut-lengths.parquet` — per-cycle L,
  t_period.
- `autoresearch/archive/005-l4plus-catalog.md` — the (3, 13) listing
  with cycle members.

**Falsification protocol:**
- Attempt 1 (planned, action 006): 10× horizon sweep — does (3, 13) get
  more cycles? If yes, the "exactly 7 L=5" claim refines/falsifies.
- Attempt 2 (planned, action 008): derive the L=5 cycle equation
  algebraically; enumerate all (k₁..k₅) summing to 8 (there are 35
  compositions); check which yield positive odd integer solutions.
  Expect 7 (or possibly more if the sweep at 10× horizon finds more).

**Conjugacy check:** b = 13 is prime, no scaling parents. All 7 cycles
have gcd of members = 1, so all are `new` per action 004.

---

### C-005 — (5, 9) has a small "new" cycle (1, 7, 11) on integers coprime to 3

**Status:** **probed** (verified by direct query of 001-cycles.parquet:
cycle_id=0 has members starting with [1, 2, 4, 7, 8, 11, 14, 16, ...]
with L=3 odd values {1, 7, 11} and gcd=1, tagged "new")
**First proposed:** action 002 (`log/002-research-trivial-cycles.md`),
reinforced by action 001.

**Scope (parameters):** (a, b) = (5, 9).
**Scope (horizons):** L ≤ 3 closed-form derivation; sweep S = 10⁴.

**Statement:** T_{5, 9} admits a length-3 cycle (1, 7, 11) with shortcut
sequence k = (1, 2, 6). The cycle's members are all coprime to 3 (and
to 9), so it is *not* a 3-scaled or 9-scaled image of any cycle of
(5, 1) or (5, 3). It is the smallest "genuinely new" cycle visible in
the a = 5 row of the tight scope.

**Supporting evidence:**
- `autoresearch/archive/002-trivial-cycles.md` — closed-form derivation
  with verification.
- `autoresearch/archive/001-cycles.parquet` — sweep finds this cycle
  reached from a sizable share of seeds in [1, 10⁴].

**Falsification protocol:**
- Attempt 1 (planned, action 005): directly verify by simulation that
  (1, 7, 11) is a cycle of T_{5,9} (already verified by sub-agent;
  re-verify in one line).
- Attempt 2: search for a hidden parent — is there any other (a', b')
  in the larger scope (eg b' ∈ {1, ..., 9} odd) such that (5, 9)'s
  cycle (1, 7, 11) is a scaling or affine image of an (a', b') cycle?

**Conjugacy check:** members coprime to all proper odd divisors of
b = 9 (i.e. coprime to 3); confirmed not inherited.

**Notes:**
- This is the candidate "tractable cousin" the brief asks for. (5, 9)
  with a small clean cycle on a row that otherwise looks chaotic is
  exactly the shape of variant worth attacking theoretically.

---

### C-006 — sub-system attractivity

**Status:** **falsified** (action 006, 543,514 counterexamples)
**First proposed:** action 003 (`log/003-research-conjugacy-survey.md`)
**Falsified in:** action 006 (`log/006-research-10x-horizon-and-attractivity.md`)

**Scope (parameters):** (a, b) with b composite (b ∈ {9, 15, 21}, plus
extension to (1, 9), (1, 15), (1, 21)).
**Scope (horizons):** sweep-based, S = 10⁴, H = 10¹², T = 10⁴.

**Statement:** For (a, b) with b composite and λ an odd divisor of b
with 1 < λ < b, λZ is forward-attractive under T_{a, b}: every seed
n₀ not in λZ eventually iterates to a value in λZ within finitely many
steps. Equivalently, the dynamics on the complement of λZ is transient.

**Supporting evidence:**
- Sub-agent action 003 spot-checked (3, 3) by hand: every odd seed
  becomes a multiple of 3 in one odd step.
- Mechanically, T_{a, λb}(odd n) = a·n + λb. If λ | a·n then a·n + λb is
  divisible by λ; otherwise it isn't. The first step doesn't guarantee
  injection. So this is *not* trivially true; it depends on a, b, λ.

**Falsification protocol:**
- Attempt 1 (action 006, ✓ done): augmented the sweep to log first hit
  time into λZ for non-λZ seeds. **Falsified** — 543,514 seeds n₀ ∉ λZ
  exceeded H = 10¹³ without ever entering λZ. The largest cells:
  (5, 9, 3), (7, 9, 3), (5, 15, 3), (7, 15, 3), (7, 15, 5), (5, 21, 3),
  (5, 21, 7), (7, 21, 3) — each contributing > 50,000 counterexamples.

**Refined claim that survived:** for a = 3 with composite b and λ | b,
λZ *is* forward-attractive: max hit time ≤ 17 steps across all seeds.
For a ∈ {5, 7} with composite b, λZ is *not* forward-attractive — the
complement carries its own divergent dynamics. This is the C-006′
weak-form salvage; promoted as a separate entry below.

**Conjugacy check:** n/a — this is *about* the sub-system structure
itself, not about conjugating between variants.

**Notes:**
- The falsification is structurally important: it means a = 3 (and a = 1
  by extension) admit a "reduce to bZ" argument, whereas a ∈ {5, 7} do
  not. That's a sharp split aligned with the convergent vs divergent
  dichotomy from C-001.

---

### C-006′ — REPLACED by C-006″

The earlier C-006′ ("forward-attractivity holds for a=3 only") was based
on a misreading of action 006's report and is wrong. Action 009 (main's
analytic + data-cross-check) refines it to C-006″ below.

The replaced form claimed "max hit time ≤17 for all (3, b, λ) in
scope." In fact 80,000 seeds for (3, 15, 5) and 85,715 seeds for
(3, 21, 7) **never** entered λZ within T=10⁵. Action 006's "≤17"
applied only to λ=3 cells, where 3 | a kills the residue immediately.

---

### C-006″ — Forward-attractivity ⟺ rad(λ) | rad(a)

**Status:** **surviving + analytically proven** (via residue arithmetic
in (ℤ/pℤ)*; verified empirically across 24+ (a, b, λ) cells covering
prime and composite λ)
**First proposed:** action 009 (`log/009-research-c007-and-c006-proofs.md`,
`autoresearch/archive/009-c007-prime-and-c006-prime-proofs.md`)
**Probed in:** action 009 — direct query of
`autoresearch/archive/006-attractivity.parquet` confirmed the condition
across all 20 (a, b, λ) cells in the probe.

**Scope (parameters):** all (a ∈ {1, 3, 5, 7}, b composite ∈ {9, 15, 21},
λ proper odd prime divisor of b) — 20 cells.
**Scope (horizons):** S = 10⁵, H = 10¹³, T = 10⁵.

**Statement:** For (a, b) with composite b and λ a proper odd divisor
of b > 1, the sub-lattice λZ is forward-attractive under T_{a, b} —
i.e. every seed n₀ ∉ λZ enters λZ within finitely many steps —
**if and only if every prime divisor of λ also divides a**, equivalently
`rad(λ) | rad(a)`.

For prime λ, this reduces to `λ | a` ⟺ `gcd(a, λ) > 1` (equivalent).
For composite λ, the radical condition is **strictly more
restrictive** than gcd: `(3, 45, λ=15)` has `gcd=3>1` but
`rad(15)=15 ∤ rad(3)=3`, and is empirically NOT forward-attractive.

**Supporting evidence:**

| a | b | λ | gcd(a, λ) | n_entered | n_never | attractive? |
|---|---|---|---|---|---|---|
| 1 | 9 | 3 | 1 | 0 | 66667 | False |
| 1 | 15 | 3 | 1 | 0 | 66667 | False |
| 1 | 15 | 5 | 1 | 0 | 80000 | False |
| 1 | 21 | 3 | 1 | 0 | 66667 | False |
| 1 | 21 | 7 | 1 | 0 | 85715 | False |
| 3 | 9 | 3 | **3** | **66667** | **0** | **True** |
| 3 | 15 | 3 | **3** | **66667** | **0** | **True** |
| 3 | 15 | 5 | 1 | 0 | 80000 | False |
| 3 | 21 | 3 | **3** | **66667** | **0** | **True** |
| 3 | 21 | 7 | 1 | 0 | 85715 | False |
| 5 | 9 | 3 | 1 | 0 | 66667 | False |
| 5 | 15 | 3 | 1 | 0 | 66667 | False |
| 5 | 15 | 5 | **5** | **80000** | **0** | **True** |
| 5 | 21 | 3 | 1 | 0 | 66667 | False |
| 5 | 21 | 7 | 1 | 0 | 85715 | False |
| 7 | 9 | 3 | 1 | 0 | 66667 | False |
| 7 | 15 | 3 | 1 | 0 | 66667 | False |
| 7 | 15 | 5 | 1 | 0 | 80000 | False |
| 7 | 21 | 3 | 1 | 0 | 66667 | False |
| 7 | 21 | 7 | **7** | **85715** | **0** | **True** |

**20/20 match.** Every cell with gcd > 1 is forward-attractive (zero
seeds escape); every cell with gcd = 1 is fully non-attractive (zero
seeds enter within T = 10⁵).

**Analytic argument** (sketch — for prime λ):
- Mod λ, T_{a, b}'s odd step takes r → a·r + b ≡ a·r (mod λ) since
  λ | b. The halving step takes r → r · 2⁻¹ (mod λ) when r is even in
  ℤ; mod λ this is r · 2⁻¹.
- The residue evolves as r_{t+1} ≡ a^{j(t)} · 2⁻^{k(t)} · r₀ (mod λ)
  for some non-negative integer functions j, k of t.
- If gcd(a, λ) > 1, eventually a^{j} ≡ 0 (mod λ) (since λ is prime
  and λ | a), making r_t = 0 — the trajectory enters λℤ.
- If gcd(a, λ) = 1, both a and 2⁻¹ are units in (ℤ/λℤ)*. Starting
  from r₀ ≠ 0 in (ℤ/λℤ)*, the residue stays in (ℤ/λℤ)* forever —
  never hits 0. So the trajectory in ℤ_{>0} never enters λℤ.

**Refined statement (final): for any λ (prime or composite), the
condition is rad(λ) | rad(a)** — every prime divisor of λ must also
divide a.

**Analytic proof (sketch):**
For each prime p | λ:
- T_{a, b}(odd n) = a·n + b. Mod p: a·n + b ≡ a·n (mod p) iff p | b
  (which holds since p | λ | b).
- The residue r mod p evolves: per odd step, r → a·r mod p. Per
  halving (when n is even), r → r·2^{-1} mod p (since p odd, 2 invertible).
- If p | a: r → 0 mod p quickly (multiplication by 0).
- If p ∤ a: a is a unit in (ℤ/pℤ)*. Residue stays in (ℤ/pℤ)* forever
  (multiplication by units in a finite group is bijective; never reaches 0).

For seed n₀ ∉ λZ: at least one prime factor of λ doesn't divide n₀.
For trajectory to enter λZ, all prime factors of λ must divide
T^t(n₀). By the above, this happens iff every prime factor of λ
divides a (so each prime's residue gets killed). Hence rad(λ) | rad(a).

Empirically verified:

| (a, b, λ) | gcd(a, λ) | rad(λ) | rad(a) | rad(λ)∣rad(a)? | empirical attractivity |
|---|---|---|---|---|---|
| (3, 27, 9) | 3 | 3 | 3 | ✓ | **100%** within ~4 steps |
| (5, 27, 9) | 1 | 3 | 5 | ✗ | 0% |
| (7, 27, 9) | 1 | 3 | 7 | ✗ | 0% |
| (3, 45, 15) | 3 | **15** | 3 | **✗** | **14%** (finite-T only; → 0 asymp) |
| (5, 45, 15) | 5 | 15 | 5 | ✗ | 29% (similar) |
| (15, 45, 15) | 15 | 15 | 15 | ✓ | **100%** |
| (3, 45, 5) | 1 | 5 | 3 | ✗ | 0% |
| (21, 45, 15) | 3 | 15 | 21 | **✗** | 14% (finite-T only) |
| (21, 45, 3) | 3 | 3 | 21 | ✓ | 100% |
| (21, 45, 5) | 1 | 5 | 21 | ✗ | 0% |
| (21, 45, 9) | 3 | 3 | 21 | ✓ | 100% |

For prime λ, gcd > 1 ⟺ λ | a ⟺ rad(λ) | rad(a) — equivalent. For
composite λ, gcd > 1 is **insufficient**: e.g. (3, 45, 15) has gcd=3
but is NOT forward-attractive (because rad(15)=15 has prime factor 5
not in rad(3)=3).

This refines the conjecture across all λ, prime or composite.

**Falsification protocol:**
- Attempt 1 (action 009, ✓ done): direct query of action 006's
  attractivity data. **20/20 match** — survived.
- Attempt 2 (planned): test composite λ at extended scope. Need (a, b)
  with b having a composite proper divisor — e.g. (a, b=27) with λ=9,
  (a, b=45) with λ=15. For each, check rad(λ) | rad(a).
- Attempt 3 (planned): closed-form proof for general λ via Chinese
  Remainder Theorem on the prime-power decomposition of λ.

**Conjugacy check:** independent of conjugacy — the statement is about
the dynamics on a sub-lattice, not about (a, b) ↔ (a', b') equivalence.

**Notes:**
- This is a sharp characterization with both empirical and analytic
  support in the prime-λ case. **Promotion-grade** for prime λ; the
  generalized statement for composite λ remains a conjecture.
- The condition has structural significance: it tells us *which*
  variants admit a "reduce to bZ" argument and which don't. For
  example, the (a=1, b composite) family has *no* forward-attractive
  sublattices (since gcd(1, λ) = 1 always), so its multi-attractor
  structure (C-007′) is genuine — every gcd-class is its own
  dynamical system.

---

### C-007 — d(b) is a lower bound on attractor count for a=1 (replaces C-002)

**Status:** **surviving** (verified across 11 cells in tight scope at
S=10⁴, plus 15 cells in wider-b at S=10⁵ via action 012; lower bound
holds in 26/26 cells)
**First proposed:** main spot-check post action 003.

**Scope (parameters):** a = 1, b odd in [1, 21].
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement:** For (a = 1, b odd), the number of distinct attractor
cycles reached from seeds in [1, 10⁴] is at least d(b). Equality holds
when no L ≥ 2 cycle of (1, b) is non-inherited; strict inequality occurs
when (1, b) admits a non-inherited L ≥ 2 cycle. Specifically, the
"inherited" lower bound comes from the construction: for each divisor
d | b, the d-scaled image of (1, b/d)'s trivial L1 cycle gives an
attractor cycle in (1, b).

**Supporting evidence:**
| b | observed | d(b) | gap | gap explanation |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | — |
| 3 | 2 | 2 | 0 | — |
| 5 | 2 | 2 | 0 | — |
| 7 | 3 | 2 | 1 | L2 (3, 5) cycle at k=(1, 2) |
| 9 | 3 | 3 | 0 | — |
| 11 | 2 | 2 | 0 | — |
| 13 | 2 | 2 | 0 | — |
| 15 | 5 | 4 | 1 | L2 cycle (3, 9) — *check* |
| 17 | 3 | 2 | 1 | L2 (1, 5) cycle |
| 19 | 2 | 2 | 0 | — |
| 21 | 6 | 4 | 2 | L2 (1, 11) and L2 (9, 15) — *check* |

(Gap explanations need verification by analyst against 001-cycles.parquet
+ 002-trivial-cycles.md.)

**Falsification protocol:**
- Attempt 1 (planned, action 004 analyst): tag every cycle in
  001-cycles.parquet with its inheritance status; verify that
  `n_inherited_cycles(a=1, b) == d(b)` for every b in scope. **Falsifier:
  any (a=1, b) cell where d(b) > number of inherited cycles found.**
- Attempt 2 (planned, action 006 sweep extension): extend b range to
  {23, 25, 27, 29, 31, 33, 35, 37, 39} odd, verify the lower-bound
  claim holds.
- Attempt 3: derive analytically. The construction is straightforward —
  prove that for each d | b odd, n = d generates a cycle on dZ under
  T_{1, b}. With period: smallest k such that 2^k · d ≡ d (mod b),
  i.e. d(2^k − 1) ≡ 0 (mod b), i.e. 2^k ≡ 1 (mod b/gcd(b, d)).

**Conjugacy check:** none of (a=1, b) cells reduce to each other under
the normal form.

**Notes:**
- The analytic derivation of the lower bound is essentially trivial.
  The interesting part is whether equality is the typical case and what
  *exactly* governs the gap (L ≥ 2 non-inherited cycles for a = 1).
- Deserves a structural follow-up: which (a=1, b) admit non-inherited
  L ≥ 2 cycles? b odd composite with specific 2-adic structure of b?

**Update post action 004:** the "strong form `n_inherited == d(b)`" was
falsified at 10 of 11 (a=1, b) cells. The base cycle of (1, b) reachable
from seed n=1 has gcd = 1 of members and is tagged `new`, not
`inherited` — so `n_inherited == d(b) − 1` is the closer relation. See
C-007′ below for the refined form.

---

### C-007′ — refined inheritance count for a=1

**Status:** probed (single confirmation pass at S = 10⁴; not yet
falsified at expanded horizons)
**First proposed:** action 004 (`log/004-research-inheritance-tagging.md`)

**Scope (parameters):** a = 1, b odd in [1, 21].
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement:** For (a = 1, b odd), the number of cycles tagged
`inherited` (cycles whose member-gcd g > 1 with g | b, equivalently
cycles that are scaled images of (1, b/g) cycles) satisfies
**n_inherited ≥ d(b) − 1**, with one inherited cycle for each proper
divisor d > 1 of b. Strict inequality occurs when (1, b/d) for some
d | b itself has multiple cycles, all of which scale into distinct
(1, b) cycles (the b=21 case).

**Supporting evidence:** action 004 inheritance-tagged the full
a=1 row; lower bound holds at all 11 cells with slack 0–multiple.

**Falsification protocol:**
- Attempt 1 (planned, action 006 — auto in flight): same check at
  S = 10⁵.
- Attempt 2: extend b range to {23, 25, 27, 29}. Verify lower bound.

**Conjugacy check:** within a = 1, no full conjugacies in scope.

**Notes:**
- This is a near-trivial structural claim once stated. Worth recording
  as a "lemma-shaped" conjecture; the *interesting* question is what
  governs n_new(1, b), the count of base-level non-inherited cycles.

---

### C-008 — (3, 13) L=5 cycles form a structured family

**Status:** **surviving** (two independent confirmations: 10× horizon
sweep + algebraic enumeration). Promotion-grade; pending user
confirmation.
**First proposed:** action 005 (`log/005-research-l4plus-catalog.md`)
**Probed in:** action 006 (10× horizon sweep — all 7 cycles present,
no 8th); action 008 (`log/008-research-l5-enumeration.md`) —
algebraic enumeration confirms 7 cycles via 35 compositions / 5-fold
rotation symmetry. Reason: `2⁸ − 3⁵ = 13` exactly, so every
composition yields an integer n₀.

**Scope (parameters):** (a, b) = (3, 13).
**Scope (horizons, original):** S = 10⁴, H = 10¹², T = 10⁴.
**Scope (horizons, expanded):** S = 10⁵, H = 10¹³, T = 10⁵.

**Statement:** (3, 13) admits exactly 7 primitive cycles of shortcut
length L = 5 (and T-period 13). They are parametrized by the halving
vector (k₁, k₂, k₃, k₄, k₅) with kᵢ ≥ 1 and Σ kᵢ = 8 — exactly the 7
compositions of 8 into 5 positive parts that yield a positive odd
integer solution `n₀` of

  n₀ · (2⁸ − 3⁵) = 13 · (3⁴ + 3³·2^{k₁} + 3²·2^{k₁+k₂}
                          + 3·2^{k₁+k₂+k₃} + 2^{k₁+k₂+k₃+k₄}).

(Total compositions of 8 into 5 positive parts = C(7, 4) = 35; only 7
yield valid cycles. The conjecture is empirical that the count is
exactly 7, not 6 or 8.)

**Supporting evidence:**
- `autoresearch/archive/005-l4plus-catalog.md` — full listing of the
  7 cycles with members and (k₁..k₅).
- Cycle_min residues mod 13: {3, 6, 4, 12, 10, 1, 7} — 7 of 12 nonzero
  residues.

**Falsification protocol:**
- Attempt 1 (planned, action 006 — in flight): 10× horizon sweep on
  (3, 13). If a new L = 5 cycle appears at higher seeds, the "exactly
  7" claim is falsified.
- Attempt 2 (planned, action 008): enumerate all 35 compositions of 8
  algebraically, solve the cycle equation for each, count integer
  solutions. **Falsifier:** if more or fewer than 7 yield valid
  positive odd integer cycles.
- Attempt 3: extend to L = 6, 7 — does (3, 13) carry similar structured
  families at higher L? The L = 15 outlier may be the first member of
  the L = 15 family.

**Conjugacy check:** b = 13 prime, no scaling parents; all cycles are
primitive.

**Notes:**
- This is the first conjecture in the run that has both *empirical
  exactness* (a precise count) and *algebraic substance* (the cycle
  equation is concrete). Strong candidate for promotion to
  LESSONS.md if attempt 2 confirms.
- The cycle_min residue pattern (avoiding 5 of 12 nonzero residues —
  specifically {2, 5, 8, 9, 11}) might have a structural reason
  (Galois / multiplicative-order argument); worth a deeper probe if
  the count holds.

---

### C-009 — empirical period law t_period ≈ L · (1 + log₂ a) (for a ≥ 3)

**Status:** probed for a ≥ 3 (deviation < 4%); **fails for a = 1**
(deviation up to 2.23 in wider-b sweep). Refined: the law applies
specifically for a ≥ 3.
**First proposed:** action 005 (`log/005-research-l4plus-catalog.md`)

**Scope (parameters):** all 44 (a, b) cells in tight scope. Constraint:
this is a per-cycle empirical relation, not a per-(a, b) relation.
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement:** Over the 153 cycles in the atlas, the per-(a, b) mean of
t_period / L closely matches `1 + log₂ a`, with deviation < 4% across
a ∈ {3, 5, 7}:

| a | empirical mean t_period/L | predicted (1 + log₂ a) | deviation |
|---|---|---|---|
| 3 | 2.66 | 2.585 | +2.9% |
| 5 | 3.42 | 3.32 | +3.0% |
| 7 | 3.87 | 3.81 | +1.6% |

(For a = 1: 1 + log₂ 1 = 1, and trivially t_period = L · 1 + halvings;
the relation degenerates. Excluded.)

**Supporting evidence:**
- `autoresearch/archive/005-shortcut-lengths.parquet` — per-cycle L and
  t_period.

**Falsification protocol:**
- Attempt 1 (planned, action 006 — in flight): does the same relation
  hold at the 10× horizon? Larger seed range, more cycles found.
- Attempt 2: derive analytically from the heuristic
  `(a·n + b) ≡ 0 (mod 2^k)` density: expected `k = 1 + Σ_{j≥1} 2^{-j}`
  for a uniform random `a·n + b` over residues — this gives 1 + 1 =
  2 expected halvings + 1 odd step = 3 T-steps per shortcut step? But
  this should be `1/(1 - 1/2) = 2` halvings on average plus the 1 odd
  step = 3 T-steps. So `t_period/L ≈ 3` for any a with the heuristic
  argument. The empirical 2.66 / 3.42 / 3.87 is *not* well-matched by
  this. The fit `1 + log₂ a` is empirical and the analytic
  justification is unclear — that's worth investigating.

**Conjugacy check:** n/a (per-cycle relation).

**Notes:**
- Useful as a sanity-check for sweep parses: a cycle violating this
  badly is suspicious.
- The agent's claim that this matches `1 + log₂ a` may itself be a
  hypothesis worth challenging; an alternative fit is just "around 3".
  Worth cross-validating. If the empirical match is genuine, the law
  has theoretical interest.

---

### C-010 — a = 5 row shares an L = 18, t_period = 60 cycle across b ∈ {7, 13, 21}

**Status:** **probed (refined)** — direct verification: (5, 7) has L=18
primitive cycle with cycle_min=57; (5, 13) has L=18 primitive cycle
with cycle_min=53; (5, 21) has L=18 cycle but it's INHERITED (gcd=3)
from (5, 7). So (5, 7) and (5, 13) have GENUINELY DISTINCT primitive
L=18, K=42 cycles, but (5, 21)'s is just a 3-scaling. The "shared
family" claim holds for the primitive case but inherits trivially for
b=21. Both primitives satisfy C-011: 7 | (2^42 − 5^18) and 13 |
(2^42 − 5^18) (verified via Fermat).
**First proposed:** action 005 (`log/005-research-l4plus-catalog.md`)

**Scope (parameters):** (a, b) ∈ {(5, 7), (5, 13), (5, 21)}.
**Scope (horizons):** S = 10⁴, H = 10¹², T = 10⁴.

**Statement:** (5, 7), (5, 13), (5, 21) each admit a cycle with
shortcut length L = 18 and T-period 60. The cycles' members are not
b-scalings of each other (b values 7, 13, 21 don't share a common
divisor > 1 across all three); but the shape (L, t_period) is shared.

**Supporting evidence:** action 005's note. Needs concrete listing —
flag.

**Falsification protocol:**
- Attempt 1 (planned, action 008): list each of the three cycles by
  members; check whether they share residues mod some modulus, share
  halving-vector structure, etc. **Falsifier:** if the three cycles
  have unrelated halving-vector structures, the "shared family" claim
  is too weak to hold.

**Conjugacy check:** (5, 21) inherits cycles from (5, 7) and (5, 3),
so the L=18 cycle of (5, 21) might be the 3-scaled image of (5, 7)'s
L=18 cycle. Need to verify; if so, this is partial inheritance, not a
shared family.

**Notes:**
- Lowest priority of the post-action-005 conjectures; may dissolve into
  inheritance. Worth checking before promotion.

---

### C-012 — n_new(a=1, b) closed form via ord_b(2)

**Status:** **surviving** (11/11 empirical match in tight scope; derived
as a corollary of C-011 for a = 1)
**First proposed:** action 013 (`log/013-research-n-new-structure.md`)

**Scope (parameters):** a = 1, b odd > 1.

**Statement:** For (a = 1, b odd > 1), the count of primitive
(`new`-tagged) cycles equals the sum over admissible L of the Burnside
count of primitive necklaces in compositions of ord_b(2) into L
positive parts whose entry point n₀ is coprime to all proper odd
divisors of b.

For our tight scope:

| b | ord_b(2) | predicted n_new | observed n_new |
|---|---|---|---|
| 3 | 2 | 1 | 1 |
| 5 | 4 | 1 | 1 |
| 7 | 3 | 2 | 2 |
| 9 | 6 | 1 | 1 |
| 11 | 10 | 1 | 1 |
| 13 | 12 | 1 | 1 |
| 15 | 4 | 2 | 2 |
| 17 | 8 | 2 | 2 |
| 19 | 18 | 1 | 1 |
| 21 | 6 | 2 | 2 |

**Falsification protocol:**
- Attempt 1 (action 013, ✓ done): direct enumeration. **Survived
  11/11.**
- Attempt 2 (action 012's wider-b sweep): same agreement at b ∈
  {23..51} (per action 012's report on a=1 cycle counts). **Survived.**
- Attempt 3 (planned): prove the closed-form analytically — not
  difficult given C-011 + standard necklace combinatorics.

**Conjugacy check:** within a = 1, no full conjugacies in scope.

**Notes:**
- Closes the "what governs n_new(1, b)?" open question that had been
  carried since action 004.
- The 2-adic residue hypothesis (b ≡ 7 mod 8) was the previous wrong
  guess — falsified by b = 17 (≡ 1 mod 8) and b = 21 (≡ 5 mod 8) both
  giving n_new = 2 from non-2-adic structural reasons.

---

### C-013 — Residue-class basin structure: first-step halving harvest predicts convergence

**Status:** **surviving** (34/34 non-degenerate cells, Pearson r > 0.7
at k=4, median r = 0.833 at k=4; mechanistically supported by the
"multi-step harvest doesn't help" anti-result)
**First proposed:** main, post action 016 (manual three-cell sample).
**Probed in:** action 017 (systematic across all (a ≥ 5, b) cells in
scope) — `log/017-research-residue-basin-structure.md`

**Scope (parameters):** (a, b) with a ≥ 5 odd, b odd. The "shortcut
residue chain" at modulus 2^k is the deterministic finite map
σ: (ℤ/2^kℤ)^* → (ℤ/2^kℤ)^* defined by

  σ(r) = (a·r + b) / 2^{v₂(a·r+b)}  (mod 2^k)

This map has finitely many recurrent attractors (cycles in the residue
graph) and basins of attraction.

**Statement:**
1. (Structural) The convergent integer cycles of T_{a, b} have odd
   members occupying specific residue classes mod 2^k. Call these the
   *cycle-residues*.
2. (Empirical) The convergent fraction of seeds n₀ ∈ [1, S] at residue
   r mod 2^k is heavily biased: residues whose shortcut-chain
   trajectory ends in an attractor *containing a cycle-residue* are
   substantially over-represented; residues whose chain ends in a
   "trap" attractor (no cycle-residues) are heavily under-represented.
3. (Limiting form) As k → ∞ AND S → ∞, the convergent natural density
   of seeds at residue r → 0 exactly when r belongs to a basin of a
   trap attractor at every k.

**Supporting evidence (preview, full evidence in action 017):**

- **(3, 1)** classical Collatz: residue chain mod 16 has the **single
  attractor {1}** (the cycle's odd member residue). All seeds converge
  empirically — consistent.
- **(5, 1)** at mod 16: **two attractors** — {1, 3} (cycle odd members)
  and {7, 9} (non-cycle trap). 7.26% empirical convergence, with
  residues in the trap basin showing lift ~0.5 vs lift ~1.5 in the
  cycle basin.
- **(7, 1)** at mod 32: attractors {1} (cycle) and {7, 11, 25} (trap).
  9 residues had empirical lift = 0 (or near-0), corresponding to
  paths that visit the trap attractor.
- **(5, 9)** at mod 16: two attractors {1, 7, 11} (the small primitive
  cycle (1, 7, 11)) and {3} (n=3 inherited cycle). Both contain
  cycle-residues — corresponding to the highest-convergence cell
  (26.4%) in our scope.

**First-order correlate**: lift(r) ≈ proportional to v₂(a·r + b),
the first-step halving harvest. Pearson r ∈ [0.76, 0.86] across the
three sampled cells.

**Falsification protocol:**
- Attempt 1 (action 017, ✓ done): systematic across all (a ≥ 5, b)
  cells in tight scope. **Survived strongly:** 34/34 non-degenerate
  cells with Pearson r > 0.7 at k=4; median r = 0.833.
- Attempt 2 (main inline, post action 017, ✓ done): wider-b range
  b ∈ [23, 51] using `012-results.parquet`. **Survived strongly:**
  29/30 non-degenerate cells with r > 0.7 at k=4; median r = 0.846;
  zero anti-correlations. Only (5, 47) at r = 0.58 weaker, and it has
  only 90 converged seeds (statistical noise floor).
- Attempt 3 (planned): scaling with k — does the relation strengthen
  or weaken at k = 8, 10?
- Attempt 4 (planned): derive α(a, b) analytically from the residue
  distribution of v_2(a·r + b).

**Aggregate evidence:** **63 of 64 non-degenerate cells** across two
scope expansions (137 variants total) confirm the correlation at
r > 0.7. Median r = 0.84 across all.

**Key anti-result (action 017):** Multi-step harvest does NOT improve
correlation. Single-step h captures the predictable structure;
longer dynamics is dominated by random higher-bit information not
visible in the starting residue mod 2^k.

**Conjugacy check:** invariant under b-scaling — if (a, b) → (a, λb)
via the b-scaling sub-system embedding, the residue chains are
conjugate via multiplication by λ.

**Refined sharpened statement** (post actions 017, 020, 028, 030):

> For (a, b) with a ≥ 5 odd and b odd, the conditional probability
> that a seed converges given its first K shortcut-step halving
> harvests satisfies
>
>   `log[P(converge | h_1, ..., h_K) / (1-P)] ≈ α(a, b) · Σ_{i=1..K} h_i + const`
>
> with α(a, b) > 0 *independent of K*, and **α(a, b) ≈ 2μ / (σ²·ln 2)**
> where μ = log₂(a) − E[h] = log₂(a) − 2 and σ² = Var(h) = 2.

**Empirical match to random-walk theory (action 030, expanded):**

Individual-seed logistic regression of `log[P(conv)/(1-P(conv))]` on
first 4 h's, across all 22 (a∈{5,7}, b∈[1,21]) cells:

| metric | value |
|---|---|
| mean ratio α_emp / α_RW | 0.84 |
| median ratio | 0.89 |
| cells within [0.7, 1.3] | 19/22 |
| best matches | (7, 1) 0.97; (7, 3) 0.99; (7, 9) 0.99 |
| worst matches | (7, 11) 0.53; (7, 5) 0.66; (7, 15) 0.68 |

**Per-cell highlights:**
| (a, b) | α_emp | α_RW = 2μ/(σ²·ln 2) | ratio |
|---|---|---|---|
| (5, 1) | 0.41 | 0.464 | 0.88 |
| (5, 13) | 0.40 | 0.464 | 0.87 |
| (7, 1) | 1.13 | 1.164 | 0.97 |
| (7, 3) | 1.15 | 1.164 | 0.99 |

**Verdict:** the random-walk-on-log derivation captures α correctly
within ~10-15% for most cells (especially prime-b cells); composite-b
cells show up to 30-50% deviation (more inherited cycle structure
adds non-walk effects). The earlier 0.6-0.7× systematic gap from
binned-lift regression is closed; individual-seed logistic gives a
much sharper estimate aligned with the Brownian theory.

**Individual-seed prediction AUC is 0.72-0.99** across cells —
first 4 h's strongly predict individual convergence.

**Mechanism** (extension via action 020):
The residue chain mod 2^k partitions odd residues into attractor basins.
Whether trap basins (those not containing cycle-odd-residues) actually
suppress convergence depends on the **random-walk drift sign**:

- For μ = log_2(a) − E[h] < 0 (a ∈ {1, 3}): trap basins are
  *transiently slow* — all seeds eventually converge. (3, 1) at
  k = 10: trap-basin seeds converge 14% slower (mean 121 vs 106 steps).
- For μ > 0 (a ≥ 5): trap basins are *nearly absorbing* —
  trap-basin seeds rarely converge. (5, 1) at k = 10: trap-basin
  convergence rate 1.88% vs good-basin 6.75% — **3.6× suppression**.

This unifies C-001 (a-axis dichotomy) with C-013: the dichotomy
boundary at a = 3/5 is exactly the drift-sign zero crossing for the
generic v₂ distribution (E[h] ≈ 2, so μ flips sign at log_2(a) = 2).

**Notes:**
- This is the first conjecture in the run that says something
  non-trivial about the **divergent** dynamics of the family. The
  C-001/C-011 results characterize where cycles live; C-013
  characterizes *which seeds reach them.*
- The "multi-step doesn't help" anti-result is the surprise: it says
  the convergence-bias is *one-shot* (determined by the first odd
  step's value-multiplier (a·r + b)/2^{v_2(a·r + b)}), not the result
  of a long chain of corrections.

**Analytic derivation** (action 019): random-walk-on-log heuristic
predicts `α = 2μ/(σ²·ln 2)` where `μ = log₂(a) − E[h]` and
`σ² = Var(h) = 2.000` (exact, confirmed across all cells). Pearson
correlation between empirical and predicted α: **r = 0.840**. Functional
form is right; magnitude consistently shrunk by factor ~0.6. The
shrinkage is uniform across cells, suggesting a single missing
correction — most likely positive autocorrelation of h along orbits
inflating σ²_effective.

---

### C-014 — Asymptotic basin dichotomy: convergent vs divergent at k → ∞

**Status:** **FALSIFIED in strong form** (action 023). Basins do not
predict actual convergence in general; (9, 1) has basin → 0.996 at
k=22 but empirical f = 0%. Refined to a much weaker statement:
basin → 1 iff cell is fully convergent; otherwise basin behavior is
oscillatory or unrelated to f.
**First proposed:** main, post action 019.
**Falsified in:** action 023 (`log/023-research-basin-and-power-law.md`)

**Scope (parameters):** (a, b) with a, b odd.
**Scope (horizons):** residue chain mod 2^k, k → ∞.

**Statement:** The basin (under the shortcut residue map) of the
attractor containing the integer cycle's odd-residue members satisfies:

- For (a, b) with a ∈ {1, 3} ("convergent regime"): basin/2^(k-1) → 1
  monotonically as k → ∞.
- For (a, b) with a ≥ 5 ("divergent regime"): basin/2^(k-1) → 0
  (possibly non-monotonically through finite k).

**Supporting evidence:**

| (a, b) | k=10 | k=12 | k=14 | k=16 | trend |
|---|---|---|---|---|---|
| (3, 1) | 63.5% | 98.8% | **100%** | — | monotone → 100% |
| (5, 1) | 5.3% | 94.1% | 39.5% | 6.2% | wildly non-monotone, → small |
| (7, 1) | 60.4% | 4.2% | 1.4% | — | monotone → 0 |

**Falsification protocol:**
- Attempt 1 (planned): higher-k probe for (5, 1) at k = 18, 20, 24 —
  is the asymptotic basin small (consistent with empirical f(5,1) ≈ 2%)
  or zero (genuine divergence majority)?
- Attempt 2: extend to (a, b) with composite b — does the basin of
  any inherited cycle dominate?

**Conjugacy check:** invariant under b-scaling.

**Notes:**
- Connects to the long-standing 5x+1 conjecture: if (5, 1) basin → 0
  at k → ∞, that's evidence for genuine divergent orbits.
- Provides a residue-chain *structural* mirror of the C-001 dynamical
  dichotomy. C-001 says "divergent integer trajectories at finite
  horizon"; C-014 says "vanishing residue-chain basin at infinite
  resolution." Two faces of the same drift-sign phenomenon.

---

### C-015 — Power-law decay of convergent fraction in S

**Status:** **surviving across 3 independent S scales** (S=10⁴/10⁵/10⁶);
22/22 cells within ±20% of power-law prediction at S=10⁶; closed-form
fit c(a)=(a-4)/(a-2) with RMSE 0.053; Pearson(c, μ) = 0.982.
**First proposed:** main, integrating action 023.
**Probed in:** action 024 (`log/024-research-S1e6-c015-verification.md`)
— S=10⁶ sweep, 22/22 within tolerance.

**Scope (parameters):** (a, b) odd with a ≥ 5.
**Scope (horizons):** comparing f(a, b, S=10⁴) vs f(a, b, S=10⁵).

**Statement:** For (a, b) in the divergent regime, the convergent
fraction in [1, S] follows a power law:

  `f(a, b, S) ≈ const(a, b) · S^{-c(a, b)}`

with exponent c(a, b) that is **primarily a function of a**, weakly
dependent on b within each a-row.

**Empirical c values:**

| a | μ = log₂(a) − 2 | mean c | per-b range |
|---|---|---|---|
| 5 | 0.322 | 0.358 | 0.329–0.378 |
| 7 | 0.807 | 0.668 | 0.594–0.721 |
| 9 | 1.170 | 0.731 | 0.692–0.761 |
| 11 | 1.459 | 0.753 | 0.692–0.794 |
| 13 | 1.700 | 0.795 | 0.726–0.838 |
| 15 | 1.907 | 0.788 | 0.757–0.816 (4 cells, action 034) |

c(a) is monotonic in μ but sublinear (saturating: c(5) is well below
μ(5)·1, c(13) ~ 0.5·μ).

**Supporting evidence:** ratio f(S=10⁴)/f(S=10⁵) computed across all
35 (a∈{5..13}, b∈[1, 21]) cells where data is available; **Pearson
(c, μ) = 0.982 across cells**.

**Falsification protocol:**
- Attempt 1 (action 024, ✓ done): S=10⁶ sweep over a∈{5, 7}, b∈[1, 21].
  **Survived strongly:** 22/22 cells within ±20% of prediction; median
  ratio 0.975. Power law confirmed.
- Attempt 2 (action 026, ✓ done): test b-extension to b∈[23, 51] from
  012-results.parquet. **Survived:** a=5 mean c=0.341 vs predicted 0.333
  (Δ=+0.008); a=7 mean c=0.650 vs predicted 0.600 (Δ=+0.050).
  **Within-row b dependence**: when combining tight + wider scope
  (n=26 per a), Pearson(b, c) ≈ −0.25 — slight negative correlation.
  Mechanism: larger composite b → more inherited cycles → larger
  basin → slower decay → smaller c. Top "outliers" with c above mean
  are at b prime or prime-power (a=7 row: b ∈ {3, 13, 23, 27, 29}
  where fewer divisors → fewer cycles → faster decay).
  Total cell-count validating C-015 now ~65 cells across
  S∈{10³, 10⁴, 10⁵, 10⁶} and b∈[1, 51] odd, a∈{5, 7, 9, 11, 13, 15}.
- Attempt 3 (a≥15 high-noise probe, ✓ done): a=15 mean c=0.735 (predicted
  0.846, Δ=−0.111); a=17 c=0.881; a=19 c=0.916. The (a-4)/(a-2) formula
  starts breaking for a ≥ 15 — likely due to small convergent samples
  (most cells have <50 converged seeds), creating noisy c estimates.
- Attempt 4 (planned, analytic): derive c(a) = (a-4)/(a-2) from
  random walk's hitting-probability decay. The formula has clean
  asymptotics — c(4) = 0, c(∞) = 1 — but the analytic justification
  is open.

**Conjugacy check:** invariant under b-scaling (c only weakly
b-dependent within each a-row).

**Notes:**
- This is the **headline empirical finding for the divergent regime**.
  Where C-013 says "first-step h biases convergence within a cell,"
  C-015 says "convergent fraction across the cell follows a clean
  power law as the seed range grows."

**Theoretical context (post action 030+):**
- Brownian random-walk asymptote predicts `c_Brownian = log_2(a) − 2`
  (per μ/σ² for Δ in log_2). Heavy-tail (Veraverbeke) asymptote
  predicts `c_heavy = 1`.
- Empirical `c_emp` is below both asymptotes for a ≥ 5: empirical
  values 0.36-0.80 vs predicted asymptotes 0.32-1.0+ each.
- **Predictor RMSE (across a ∈ {5, 7, 9, 11, 13}):**

| predictor | RMSE |
|---|---|
| c_Brownian | 0.554 |
| c_heavy = 1 | 0.374 |
| min(c_B, c_H) | 0.198 |
| **(a-4)/(a-2)** | **0.037** |

The (a-4)/(a-2) formula is **15× more accurate** than the simpler
asymptote combinations. It empirically captures a finite-S transition
behavior between Brownian (small a) and heavy-tail (large a) regimes
that neither asymptotic alone describes. A deeper analytic
derivation remains open.

**Predicted limit at S → ∞:** Veraverbeke's heavy-tail asymptotic
gives `P(hit | n₀) ~ F̄(log₂(n₀))/μ` with `F̄(x) ~ (2/a) · 2^{-x}`,
yielding `c → ln(2) ≈ 0.693` as S → ∞ (universal across a ≥ 5).
Our empirical c values are above this limit at finite S — the
finite-S formula `(a-4)/(a-2)` should converge downward to 0.693 as
S → ∞ for sufficiently large a. **Testable at S = 10⁸+.** Our (a-4)/(a-2)
formula at a → ∞ gives c → 1, contradicting the asymptotic limit
0.693; this is consistent with the formula being a finite-S
approximation that overestimates the asymptotic c.

**Note on α vs c:** the per-seed Brownian formula α_RW (action 030)
matches empirical α within ~10-15%, BUT c is a different parameter
(decay rate of hitting probability vs starting position) and shows
larger deviation from Brownian due to heavy-tail effects. α captures
"local" Brownian behavior; c captures "global" tail-corrected
hitting prob.

**Closed-form fit for c(a):**

> Empirically `c(a) ≈ (a - 4) / (a - 2)` to within ±0.07 across
> a ∈ {5, 7, 9, 11, 13} (RMSE 0.053). Equivalently `1 - c(a) ≈ 2/(a-2)`.
> Formula begins to break for a ≥ 15 (where convergent samples become
> very small and statistical noise dominates).

Per-a fit:

| a | c_emp (mean) | (a-4)/(a-2) | residual | n_cells |
|---|---|---|---|---|
| 5 | 0.358 | 0.333 | +0.025 | 11 |
| 7 | 0.668 | 0.600 | +0.068 | 11 |
| 9 | 0.731 | 0.714 | +0.017 | 3 |
| 11 | 0.753 | 0.778 | −0.025 | 5 |
| 13 | 0.795 | 0.818 | −0.023 | 5 |
| 15 | 0.735 | 0.846 | −0.111 | 11 (high noise) |
| 17 | 0.881 | 0.867 | +0.014 | 1 (n_conv tiny) |
| 19 | 0.916 | 0.882 | +0.034 | 1 (n_conv tiny) |

Asymptotic behavior: c(a) → 1 as a → ∞, and c(a) → 0 as a → 4
(matching the convergent boundary). The boundary at a = 4 is not
attainable for odd a, but suggests the dichotomy threshold sits at
a = 4 in any continuous extension.

The sublinear saturation of c(a) is structural, not noise. As
a → ∞, c(a) approaches 1 (consistent with "all seeds eventually
diverge" in the limit).
- For a "tractable cousin" question: smaller c means more seeds
  remain reachable to cycles even at large S. (5, 9) with c ≈ 0.33
  is the most "tractable" divergent cell in our scope.
- This connects directly to the long-time limit of the 5x+1 family:
  if c(5, 1) > 0 strictly, there are genuinely divergent orbits in
  the limit. Empirical c(5, 1) = 0.379 > 0 at our resolution.

---

### C-020 — Cycle count distribution across divisor cells (off-hypersurface generalization of C-019)

**Status:** **proven** (corollary of C-011 + cycle equation + Möbius dedup) + 119 cells empirically validated.
**First proposed:** action 050 (`log/050-research-c020-divisor-cell-distribution.md`).

**Statement:** For any odd a ≥ 3 and L, K ≥ 1 with `N_a := 2^K − a^L > 0`,
and for each odd divisor `m` of `N_a`, the cell `(a, b = N_a / m)` admits
exactly

  **N(a, b, L, K) = #{ primitive rotation-orbit classes k : m | S(k, a, L) }**

primitive cycles of length K + L.

**Corollaries:**
- m = 1 → C-019' exactly (Lyndon-word count L_{K,L}).
- m = N_a (cell (a, 1)) → cycles iff N_a | S(k) for some primitive composition.
- **The Collatz conjecture** is the assertion that for `(3, 1)`, no
  primitive composition of any non-trivial (L, K) has `(2^K − 3^L) | S(k)`.

**Concrete instance:** `(a=5, L=3, K=7)`: N_a = 3. m=3 cell is `(5, 1)` —
the 5n+1 problem. Two primitive orbits of (3, 7) have `3 | S`: orbit
`(1, 1, 5)` gives the **13-cycle** (n_0 = 13); orbit `(1, 3, 3)` gives the
**17-cycle** (n_0 = 17). These are the two well-known non-trivial cycles
of 5n+1 at this length.

**Note on novelty:** C-020 is essentially a clean combinatorial restatement
of the Belaga-Mignotte (1998) cycle equation parameterized by divisor
structure. The per-cell count formula `m | S(k)` makes the divisor
distribution transparent. The Collatz reformulation is folklore.

---

### C-019 — Exact m=1 cycle count via Lyndon-word bijection (revised after external review)

**Status:** **surviving** + proof sketch + 59/59 verifications (action 048) + strengthened to "exactly =" with 3404-cell sweep + 10-cell brute-force confirmation (action 049).
**First proposed:** action 047. **Strengthened to full Lyndon form:** action 048. **Strengthened from "≥" to "exactly =":** action 049.

**Prior art (cited per external review):**
- **Gupta (2020)**, *On Cycles of Generalized Collatz Sequences*, arXiv:2008.11103 — Theorems 5/9/10 establish the cycle equation, the rotation-equivalence under cyclic action, and the m=1 hypersurface mechanism (`k = 2^{U+D} − 3^U` makes every partition produce a cycle, for a=3). Existence proven via Hardy-Ramanujan asymptotics; **no closed-form count given**.
- **Belaga & Mignotte (1998)**, *Embedding the 3x+1 Conjecture in a 3x+d Context* — introduced the `2^ℓ − 3^k` parametrization and the cycle equation.
- **Crandall (1978)** — original `b | 2^K − a^L` necessary condition (folklore).
- **OEIS A001037** — binary Lyndon-word count `(1/n)Σ_{d|n} μ(d) 2^{n/d}`; weighted variant by number of ones is the standard formula reused here.

**What this conjecture adds beyond Gupta:**
- Explicit **closed-form Möbius/Lyndon-word count** (Gupta has only existence asymptotics).
- **Strict equality**: count is exactly `L_{K,L}`, not just `≥` (action 049 strengthening, partial proof for L'=1 + 3404-cell empirical sweep for L'≥2).
- **Lyndon-word bijection** as the structural framing.
- **Catalan diagonals** (K=2L±1) explicitly identified; a-uniformity shown across {3, 5, 7}.

**Scope:** a ≥ 3 odd, L ≥ 1 and K ≥ 1 with 2^K > a^L (no gcd restriction).

**Statement (full):** Let b = 2^K − a^L. Then b is a positive odd integer, and
the generalized Collatz map T_{a,b} has **exactly**

  **L_{K,L} := (1/L) · Σ_{d | gcd(K, L)} μ(d) · C(K/d − 1, L/d − 1)**

primitive cycles of length K + L, **in bijection with binary Lyndon words
of length K with exactly L ones**. When gcd(K, L) = 1, this reduces to
C(K−1, L−1) / L. Each cycle's L odd-residue members are
explicitly given by the Burnside orbits of compositions k_⃗ = (k_1,...,k_L)
of K into L positive parts:

  n_0(k_⃗) = Σ_{i=0}^{L-1} a^{L-1-i} · 2^{k_1+...+k_i}

**Why important:** This generates an INFINITE 2D lattice of "tractable
cousins" of Collatz, each with explicit (combinatorially-given) cycle
counts. The Catalan families (C-018, K=2L±1) are special diagonals.

**Proof sketch:** (1) b odd: even − odd = odd. (2) m = (2^K − a^L)/b = 1
by construction. (3) C-011 (proven for b odd) ⟹ each composition gives
a primitive cycle with n_0 = S(k_⃗) integer odd positive (algebraic).
(4) C(K−1, L−1) compositions; gcd(K, L) = 1 ⟹ free ℤ/L cyclic action
⟹ Burnside dedup factor exactly L. ∎

**Empirical (59/59 verified across gcd∈{1,2,3,4,5,6}):**

a=3 sample table (predicted = actual cycles):

| L\K | 5 | 7 | 8 | 9 | 10 | 11 | 13 | 17 |
|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 5 | 7 | – | 12 | 15 | – | – |
| 4 | – | 5 | – | 14 | – | 30 | 55 | – |
| 5 | – | – | 7 | 14 | – | 42 | 99 | 364 |
| 6 | – | – | – | – | – | 42 | 132 | 728 |

a=5 spot-checks: (L=2, K=5, b=7)→2 cycles, (L=2, K=7, b=103)→3,
(L=3, K=8, b=131)→7, (L=4, K=11, b=1423)→30. All match.

a=7 spot-checks: (L=2, K=7, b=79)→3, (L=2, K=9, b=463)→4,
(L=3, K=10, b=681)→12, (L=3, K=11, b=1705)→15. All match.

**Combinatorial identity:** C(K−1, L−1)/L equals the count of aperiodic
binary necklaces with L black beads and K−L white beads (gcd(K,L)=1
case where every necklace is aperiodic). Equivalently, the count of
Lyndon words of length K with L ones over {0,1}. So C-019 establishes
a Lyndon-word ↔ primitive Collatz cycle bijection on the m=1 lattice.

**Falsification protocol:**
- Find any (a, b=2^K−a^L, L, K) with gcd(K,L)=1, a≥3 odd, satisfying
  the constraint, where the m=1 primitive cycle count of length K+L
  is NOT equal to C(K−1, L−1)/L. None found in 42 trials.

**Strengthening to strict equality (actions 049 + 052, "C-019′"):** the
theorem gives `=` (not just `≥`) — no alternate `(L', K') ≠ (L, K)` with
`L' + K' = L + K` and `m' = (2^{K'} − a^{L'})/b ≥ 2` contributes any
additional primitive cycle of length K+L.

**Theorem A (Diophantine criterion for alt-tuple existence — proven, NEW):**
For primary m=1 cell `(a, b=2^K−a^L)`, an alt tuple
`(L'=L−j, K'=K+j)` with `j ∈ {1, …, L−1}` admits the cycle equation
for integer `m' ≥ 2` **iff `b | (2a)^j − 1`**. The multiplier is then
  `m' = 2^j + a^{L−j} · q`, where `q = ((2a)^j − 1)/b`.

*Proof sketch.* Set up `m'·b = 2^{K+j} − a^{L−j}`. Substitute `2^K = b + a^L`:
`m'·b = 2^j·b + a^{L−j}·((2a)^j − 1)`. Since `gcd(b, a) = 1` (any prime
dividing both b and a would also divide 2^K, contradiction), `b | (2a)^j − 1`. ∎

**Theorem B (L'=1 no extras — proven):** L'=1 alt has S=1 always; m'≥2 ⟹
m' ∤ 1, so no n_0. ∎

**Theorem C (L'=2 no extras — proven, NEW):** For primary
`(a, b, L≥3, K)` with alt `(L'=2, K'=K+L−2, m'=2^{L−2}+a^2·q)`, no
primitive composition `k'` of `(L', K')` satisfies `m' | S(k', a, 2)`.

*Proof sketch* (revised — original Step 1 had a logical gap, see note
below).
1. **`ord_{m'}(2) > K' − 2`.** Let `d := ord_{m'}(2)` and write
   `K' = sd + r` with `0 ≤ r < d`. Suppose `d ≤ K' − 2`. The cycle
   equation gives `2^{K'} ≡ a^2 (mod m')`, hence
   `2^r ≡ a^2 (mod m')`. Case `r = 0`: `m' | a^2 − 1` but
   `m' ≥ a^2 + 2 > a^2 − 1`, so `a^2 = 1`, contradicting `a ≥ 3`.
   Case `r ≥ 1`: parity (2^r even, a^2 odd) gives
   `|2^r − a^2| ≥ m'`, so `2^r ≥ 2a^2 + 2^{L−2}`, hence
   `r ≥ ⌈log₂(2a² + 2^{L−2})⌉`. Combined with `r ≤ K' − 3 = K + L − 5`
   and the alt-tuple existence constraint `2^K ≤ (2a)^{L−2} + a^L − 1`,
   one verifies in each of the only two cells where the alt tuple
   exists (Theorem 053 below: (3, 3, 5) and (5, 3, 7)) that the
   inequalities are incompatible: 20 > 2³ for (3,3,5), 52 > 2⁵ for
   (5,3,7).
2. **Uniqueness of solution mod ord.** Any `k_1` with `2^{k_1} ≡ −a
   (mod m')` gives `2^{2k_1} ≡ a^2 ≡ 2^{K'} (mod m')`, so
   `2^{2k_1 − K'} ≡ 1 (mod m')`, hence `d | (2k_1 − K')`. Since
   `|2k_1 − K'| ≤ K' − 2 < d` (Step 1), we get `2k_1 = K'`, i.e.,
   `k_1 = K'/2`.
3. **`k_1 = K'/2` is imprimitive.** Composition `(K'/2, K'/2)` is
   rotation-fixed; the corresponding cycle is length T/2, already
   counted at the smaller m=1 tuple `(L=1, K=K'/2)`. So no PRIMITIVE
   composition contributes. ∎

**Note (correction, post-review).** Action 052's original Step 1
claimed `ord_{m'}(2) > K' − 1` from the contrapositive of
`2^{K'−1} ≡ 1`. That argument only rules out `K' − 1` being a multiple
of the order, not `ord ≤ K' − 1` (the order could divide some smaller
`d ∈ [1, K' − 2]`). The sufficient condition for Steps 2–3 is the
weaker `ord_{m'}(2) > K' − 2`, proved correctly above by case analysis
on `K' mod d` and forward reference to Theorem 053.

**Theorem D (combined — proven for L' ≤ 2):** For any primary m=1 cell
and any alt tuple with L' ∈ {1, 2}, no primitive cycle of length T arises.

**Empirical confirmation across 84 880 m=1 cells** (`a ≤ 501 odd`,
`L ≤ 30`, `K ≤ 80`): exactly 3 cells admit any alt tuple at all, namely
`(3, 5)`, `(5, 3)`, `(11, 7)`. **All alt tuples in this range have
L' ∈ {1, 2}**, so Theorem D **provably** rules out extras for the entire
84 880-cell range — this is no longer empirical, it is closed in form.

**L' ≥ 3 alt tuples — handled by Theorem 053 (action 053).** Rather
than generalizing Theorem C's discrete-log argument to `L' ≥ 3`, the
global classification proves that no L' ≥ 3 alt tuple exists in the
first place. The result is unconditional for `L = 3` (Pillai-type
direct enumeration) and within the swept range
`a ≤ 5001, L ≤ 50, K ≤ 200` for `L ≥ 4`; globally for `L ≥ 4`
outside the sweep, conditional on standard explicit Baker bounds
(Laurent–Mignotte–Nesterenko 1995).

The "double-m=1" cells (C-017, {(3,5), (3,13), (5,3)}) are unrelated to
this strengthening: they have two m=1 tuples at *different* total lengths
T₁ ≠ T₂, so no conflict.

---

### C-018 — The Catalan family of (3, b) cycle-rich cells (**corollary of C-019**)

**Status:** **surviving** (verified empirically for L = 3, 4, 5, 6, 7;
exact match to Catalan numbers in every case)
**First proposed:** action 045 (`log/045-research-catalan-family.md`).

**Scope:** a = 3, with b = 2^{2L-1} − 3^L for L ≥ 3.

**Statement:** For each integer L ≥ 3, the cell `(a=3, b=2^{2L-1}−3^L)`
admits **exactly C_{L−1} primitive cycles** (the (L−1)-th Catalan
number) at the m=1 tuple `(L, K = 2L-1)`. Specifically, every
composition of K into L positive parts yields a valid odd-integer
entry point of a primitive cycle, and after rotation dedup (gcd(K, L)
= 1 always), the count is C(2L-2, L-1)/L = C_{L-1}.

**The infinite Catalan family:**

| L | K=2L-1 | b = 2^K − 3^L | Catalan C_{L-1} | Empirical (S=10⁵) |
|---|---|---|---|---|
| 3 | 5 | 5 | **2** | 2 ✓ (cycles at len=8) |
| 4 | 7 | 47 | **5** | 5 ✓ (cycles at len=11) |
| 5 | 9 | 269 | **14** | 14 ✓ (cycles at len=14) |
| 6 | 11 | 1319 | **42** | 42 ✓ (cycles at len=17) |
| 7 | 13 | 6005 | **132** | 132 ✓ (cycles at len=20) |
| 8 | 15 | 26207 | **429** | 429 ✓ (cycles at len=23) |
| 9 | 17 | 111389 | **1430** | 1430 ✓ (cycles at len=26) |
| 10 | 19 | 465239 | 4862 | predicted |

L = 3 through 9 verified exactly by sweep (seven consecutive Catalan
numbers). The remaining L ≥ 10 predictions follow from the same construction.

**Proof (clean):**
1. b = 2^{2L-1} − 3^L ⟹ m = (2^K − 3^L)/b = 1 at (L, K=2L-1).
2. m=1 ⟹ for any composition (k_1, ..., k_L), n_0 = S(k_⃗) is integer.
3. n_0 = 3^{L-1} + 3^{L-2}·2^{k_1} + ... + 2^{k_1+...+k_{L-1}}. The
   first term is odd (3 is odd); all subsequent terms are even (since
   k_i ≥ 1). So n_0 is odd ⟹ valid odd entry point of cycle.
4. Compositions of K=2L-1 into L positive parts: C(2L-2, L-1).
5. gcd(K, L) = gcd(2L-1, L) = gcd(-1, L) = 1, so no composition is
   rotation-symmetric. Burnside dedup factor: L.
6. Distinct primitive cycles: C(2L-2, L-1) / L = C_{L-1} (Catalan).

**Why a = 3 specifically:** the construction requires 2^K > a^L for
K = 2L-1, i.e. 2^{2L-1} > a^L, i.e. 2^{2-1/L} > a. For L → ∞ this
gives a < 4. So only a ∈ {1, 3} qualify (odd a). For a = 1, the same
construction applies giving (1, 2^{2L-1}-1) with C_{L-1} cycles
(Mersenne b family).

**Significance:**
- Provides an **infinite family of "tractable cousins" of Collatz**
  with exact cycle counts (the Catalan sequence 2, 5, 14, 42, 132,
  429, 1430, ...).
- Connects three pieces in a clean way:
  - **Pillai equation** of specific form b = 2^{2L-1} − a^L
  - **C-011 cycle classification** (m=1 case)
  - **Catalan combinatorics** (gcd(K, L) = 1 + K = 2L-1 specialization)
- Each cell in the family is an explicit "new candidate tractable
  cousin" of Collatz with a precise cycle count, answering TASK.md's
  question with an infinite family rather than isolated examples.

**Falsification protocol:**
- Attempt 1 (action 045, ✓ done): empirical verification at L = 3..7.
  All match exactly.
- Attempt 2 (planned): verify L = 8 (b = 26207, predicted 429 cycles).
- Attempt 3 (proof): the proof above is clean and rigorous given
  the standard C-011 framework. Promotion-grade.

**Notes:**
- This is the **most novel-feeling finding** of the run. While each
  component (Pillai, C-011, Catalan) is standard, the connection
  giving an infinite family of cycle-rich (3, b) cells with exact
  Catalan counts may be specific to this work.
- The (3, 13) cell (atlas richness) is OUT of this family
  (K = 8 ≠ 2·5-1 = 9 for L=5). It's a separate exceptional case
  via double-m=1 (C-017).
- The Catalan family member (3, 5) (L=3, K=5) is ALSO in the C-017
  double-m=1 list — making it doubly exceptional.

---

### C-017 — Exceptional double-m=1 cells (potentially novel)

**Status:** **proposed** (empirical: searched a ≤ 999 odd, K ≤ 200,
L ≤ 49, b ≤ 10¹⁸; only 3 cells found)
**First proposed:** action 044 (`log/044-research-double-m1-cells.md`).

**Scope (parameters):** a, b positive odd integers ≥ 3.
**Scope (theoretical):** the Pillai-type equation
`2^K − a^L = b` with L ≥ 1, K > L.

**Statement:** The (a, b) cells admitting **at least two distinct
(L, K) solutions** to `2^K − a^L = b` are exactly:

| (a, b) | Tuples | Cycle-count contribution (Burnside) |
|---|---|---|
| **(3, 5)** | (L=1, K=3), (L=3, K=5) | 1 + 2 = 3 primitive cycles |
| **(3, 13)** | (L=1, K=4), (L=5, K=8) | 1 + 7 = 8 primitive cycles |
| **(5, 3)** | (L=1, K=3), (L=3, K=7) | 1 + 5 = 6 primitive cycles |

**No fourth cell exists in the searched range.** Specifically, no
(a, b) with a ≤ 999, K ≤ 200, L ≤ 49, b ≤ 10¹⁸ admits 3 or more
solutions, and the only ones admitting 2 are these three.

**Why it matters (link to C-011):** when m = (2^K − a^L)/b = 1, the
cycle equation `n₀·m = S(k⃗)/m` collapses to `n₀ = S(k⃗)`, so every
composition (k₁, ..., k_L) yields an integer n₀, contributing
`C(K-1, L-1)/L` primitive cycles via Burnside on rotation orbits
(for gcd(K, L) = 1). Cells with TWO m=1 tuples thus accumulate the
sum of two such Burnside counts, leading to **exceptional cycle
richness**. This is the structural reason why (3, 13) is the most
cycle-rich cell at the scope a ∈ {1, 3, 5, 7}, b odd ≤ 21.

**Connection to Pillai theory:**
- For each fixed (a, b), the equation `2^K − a^L = b` has finitely
  many solutions (Pillai conjecture, proven via Mihăilescu/Baker
  bounds).
- The three identified cells correspond to small instances of the
  multiplicative identity `2^{K_1}·(2^{ΔK} − 1) = a^{L_1}·(a^{ΔL} − 1)`,
  which has tight divisibility constraints:
  - `ord_{2^{K_1}}(a) | ΔL`
  - `ord_{a^{L_1}}(2) | ΔK`
  - The implied ΔK from these constraints must yield a power of 2
    when combined with the identity — a very restrictive condition.

**Falsification protocol:**
- Attempt 1 (action 044, ✓ done): aggressive empirical search.
  Survived strongly — no fourth cell in vast range.
- Attempt 2 (planned): prove via Mihăilescu/Tijdeman-style argument
  that solutions to the multiplicative identity are exhausted by
  these three.
- Attempt 3 (planned): extend to a, b not necessarily prime — does
  the structure persist?

**Conjugacy check:** none of the three cells is a conjugate of the
others (all primes, no b-scaling relations); they're genuinely
distinct exceptional cases.

**Notes (honest framing):**
- The Pillai equation `2^x − a^y = c` with fixed (a, c) and varying
  x, y is classical. The specific cases:
  - `2^x − 3^y = 5`: known to have exactly (x, y) = (3, 1), (5, 3)
  - `2^x − 3^y = 13`: known to have exactly (x, y) = (4, 1), (8, 5)
  - `2^x − 5^y = 3`: known to have exactly (x, y) = (3, 1), (7, 3)
  These are textbook facts in transcendence theory / Mihăilescu-type
  results.
- What's **specific to this run** is the observation that the cells
  with TWO Pillai solutions correspond exactly to the
  exceptionally-cycle-rich (a, b) variants in the Collatz family,
  via the C-011 framework (m=1 tuples generate the most cycles).
- This is a **clean connection between two known pieces** rather than
  a deep new result. It explains *why* (3, 13) is so cycle-rich (10
  cycles vs 1-3 typical for (3, b) prime) — namely, b = 13 is one of
  the rare values where 2^K − 3^L = 13 has two solutions, doubling
  the m=1 cycle generation.
- The three cells are the only "exceptionally cycle-rich" generalized
  Collatz variants with a, b small odd primes — a tight finite
  characterization tied to Pillai theory.

---

### C-016 — Stopping time scales with log₂(n₀)/|μ_T| in the convergent regime

**Status:** **surviving** (verified at original scope + wider-b range
b∈[23, 51]; a=1 slope 1.50 within 0.5%, a=3 slope 7.24 within 4%)
**First proposed:** main, post action 024 (`log/025-c016-stopping-time.md`).
**Probed in:** action 031 (wider-b verification across 14 cells per a).

**Scope (parameters):** (a, b) odd with a ∈ {1, 3} (convergent
regime, all seeds reach a cycle).
**Scope (horizons):** S = 10⁵, n₀ ∈ [1, 10⁵].

**Statement:** For (a, b) in the convergent regime, the stopping time
τ(n₀) (T-steps until reaching a cycle) is approximately linear in
log₂(n₀):

  `τ(n₀) ≈ K(a, b) · log₂(n₀)`

with slope K(a, b) ≈ 1/|μ_T(a)|, where μ_T(a) = (log₂(a) − 2)/3 is
the per-T-step drift in log-value space.

**Empirical slopes:**

| (a, b) | mean τ | slope K(a, b) | predicted 1/|μ_T| |
|---|---|---|---|
| (3, 1) | 105.5 | 6.99 | 7.24 |
| (3, 5) | 78.9 | 7.34 | 7.24 |
| (3, 13) | 76.5 | 7.14 | 7.24 |
| (1, 1) | 22.2 | 1.53 | 1.50 |
| (1, 7) | 19.7 | 1.50 | 1.50 |
| (1, 21) | 17.8 | 1.51 | 1.50 |

**Excellent agreement** — empirical slopes within 4% of theoretical
1/|μ_T|. The intercept varies by b (depends on which cycle the
trajectory ends in and how far it has to descend within the cycle's
basin).

**Falsification protocol:**
- Attempt 1: extend to wider b range b∈[23, 51]. **Survived strongly:**
  - a=1: slopes essentially exactly **1.50** (predicted 1.50) within
    0.5% across all 14 cells.
  - a=3: slopes 6.35-7.69 (predicted 7.24) — match within 4% on
    average across 14 cells.
- Attempt 2 (analytic): the random-walk-on-log argument predicts
  τ ≈ x/|μ_T| where x = log₂(n₀). The slope match is direct
  consequence of the random-walk drift formula.

**Conjugacy check:** intercept varies with b (cycle structure
dependent); slope is universal in a.

**Notes:**
- C-016 is the convergent-regime analogue of C-015's divergent-regime
  power law. Both are direct consequences of the random walk on log
  with drift μ_T.
- This is essentially Tao 2020's "almost-all stopping times in
  Collatz are O(log n)" result, but with explicit constant
  determined by drift. For (a, b) with very negative drift (a = 1),
  the constant 1.5 is small; for (a, b) with weakly negative drift
  (a = 3), constant 7.24 is larger.
- C-016 fails at a = 5 (boundary), where μ_T → 0+ (just barely
  divergent) — the formula would predict infinite τ for
  *converging* seeds, but converging seeds in the divergent regime
  are by definition rare exceptions whose τ depends on the random
  walk's "lucky" path, not the average drift.
- For comparison, in the well-studied 3x+1 problem, residue-class
  density results exist (Terras, Krasikov, Tao) but tend to focus on
  long-trajectory averaging. The first-step-harvest correlation
  across (a, b) families appears to be less explored.
- The tractable-cousin question gets a sharper answer: a "cousin" is
  one where the residue chain has a single attractor matching the
  cycle, AND where α(a, b) doesn't admit a "trap basin" — i.e. all
  residues lead to convergence with the right first-step harvest
  density.

---

### C-011 — generalized count of primitive L-cycles when 2^K − a^L divides b

**Status:** **PROVEN for b odd** (closed-form necessity + sufficiency).
Empirical: 1,661 tuples enumerated within L≤8 cap (100% match); all
**171 primitive cycles across 137 variants** (tight + wider-b + wider-a)
satisfy the divisibility condition; closed-form proof of necessity in
`autoresearch/archive/014-c011-necessity-proof.md` (refined to handle
both m = 1 and m > 1 cases).
**First proposed:** action 008 (`log/008-research-l5-enumeration.md`)
**Probed in:** action 010 (`log/010-research-c011-enumeration.md`),
action 011 (`log/011-research-c011-full-coverage.md`),
action 012 (`log/012-research-wider-b-sweep.md`) — 96/96 primitive
across wider-b sweep,
action 014 (`log/014-research-c011-necessity.md`).

**Scope (parameters):** any (a, b, L, K) with `m := (2^K − a^L) / b`
a positive integer.
**Scope (horizons):** algebraic + sweep verification at S = 10⁴ (or
higher).

**Statement:** Suppose 2^K − a^L = m·b for some positive integer m. Then
the cycle equation for shortcut length L at T-period (K + L) of T_{a, b}

  n₀ = (1/m) · (a^{L−1} + a^{L−2}·2^{k₁} + … + 2^{k₁+…+k_{L−1}})

yields an integer n₀ for *every* composition (k₁, …, k_L) of K into L
positive parts. Each such n₀, *if odd*, yields a valid primitive cycle
of T_{a, b} of shortcut length L (after verifying it doesn't degenerate
to a lower shortcut length, which happens iff the composition is
rotation-symmetric and the underlying period is a divisor of L).

The number of distinct primitive L-cycles is then governed by the
**rotation-orbit count of the C(K−1, L−1) compositions of K into L
positive parts, after removing rotation-fixed compositions that
correspond to cycles of shortcut length L/d for some d | L, d > 1.**

For gcd(K, L) = 1 (the generic case): no composition is rotation-fixed,
so the count is exactly **C(K−1, L−1) / L**. This recovers the (3, 13)
case at L=5, K=8: C(7, 4) / 5 = 35 / 5 = 7. ✓

For gcd(K, L) > 1: Burnside's lemma applies; the count is
(1/L) · Σ_{d | L} φ(d) · (#compositions fixed by rotation-by-(L/d)).

**Supporting evidence:**
- `autoresearch/archive/008-l5-enumeration.md` — C-008 case verified.
- (3, 7, L=2, K=4): 2^4 − 3^2 = 7 exactly. C(3, 1) = 3 compositions:
  (1, 3), (2, 2), (3, 1). The (2, 2) composition is rotation-fixed
  (period-2 → period-1 cycle), so it doesn't count as a primitive
  L=2 cycle. (1, 3) and (3, 1) are rotations of each other, giving 1
  primitive L=2 cycle. **Action 002 confirms (3, 7) has exactly 1 L=2
  cycle (5, 11) at k=(1, 3).** ✓

**Falsification protocol:**
- Attempt 1 (planned, action 010 or beyond): enumerate all (a, b, L, K)
  pairs in our tight scope where 2^K − a^L divides b, count predicted
  primitive cycles, compare to sweep + catalog. Each match is a
  confirmation; each mismatch is a falsification.
- Attempt 2: attempt closed-form proof. The cycle equation algebra is
  symbolic and the integer-solution criterion follows directly from
  divisibility.

**Conjugacy check:** the count is intrinsic to (a, b, L, K), not
sensitive to scaling.

**Notes:**
- This is the **structural theorem** behind C-008. It generalizes
  cleanly to any (a, b) with the divisibility condition.
- (3, 5, L=3, K=7): 2^7 − 3^3 = 101, which doesn't divide 5. So this
  conjecture *doesn't* predict cycles for (3, 5, L=3, K=7), but (3, 5)
  does have L=3 cycles per action 002. This means the conjecture
  characterizes a *sufficient*, not *necessary*, condition for
  primitive cycle existence. The interesting question is: *what are
  all (a, b, L, K) satisfying 2^K − a^L = m·b in the tight scope?*
- A complete enumeration of these (a, b, L, K) tuples would give a
  closed-form count of *some* of the cycles in the atlas, which is the
  most compact summary the brief asks for.
