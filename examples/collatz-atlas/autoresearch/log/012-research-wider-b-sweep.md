# res 012 — wider-b sweep at b ∈ {23, 25, ..., 51} odd

## What & why
First L2 dispatch — extend sweep to b range outside the tight scope.
Test whether C-001, C-003, C-007′, C-009, C-011 generalize. Predicted
before dispatch:
- C-001 should hold (a-axis dichotomy is structural).
- C-003 might weaken (rigidity scope was specific to particular b).
- C-007′ should hold (proven analytically for b odd).
- C-009 should hold for a ≥ 3 (a=1 is a known limitation).
- C-011 should hold 100% (proven analytically for b odd).

## Done
Sub-agent ran sweep for a ∈ {1, 3, 5, 7}, b ∈ {23, 25, 27, ..., 51}
odd (15 new b values × 4 a values = 60 new variants), at horizons
S=10⁵, H=10¹³, T=10⁵. Total 6M new trajectories; 22.4s wall-clock.

Outputs:
- `autoresearch/archive/012-sweep.py`
- `autoresearch/archive/012-results.parquet` (6M rows)
- `autoresearch/archive/012-cycles.parquet` (283 cycles)
- `autoresearch/archive/012-summary.md`

## Result
n/a (research-only)

**Headlines:**
- 283 distinct cycles across 60 new variants. 187 inherited + 96
  primitive (`new`).
- a ∈ {1, 3}: 100% reach cycle.
- a ∈ {5, 7}: most seeds escape. (a=5, b=33) found 18 cycles — record.
  (a=7) reachers: 10,083 of 1.5M.

**Conjecture verdicts:**
- **C-001** at wider b: **CONFIRMED.** 3M a∈{1,3} trajectories, zero
  failures. Total falsification attempts surviving: now **3**.
- **C-003** at wider b: **WEAKENED.** Rigidity holds for b ∈ {29, 37,
  39, 41, 43, 47, 49, 51} (8 of 15). Fails for b ∈ {23, 25, 27, 31,
  33, 35, 45}. Most striking violation: (7, 31) has 5 cycles
  including four parallel length-23 cycles. (7, 33) has a length-46
  cycle. So C-003 doesn't generalize beyond its original scope.
- **C-007′** at wider b: **CONFIRMED.** n_total ≥ d(b) − 1 holds for
  all 15 a=1 cells in new range; in fact n_total often substantially
  exceeds d(b) due to extra primitive cycles.
- **C-009** at wider b: holds for a ∈ {3, 5, 7} with deviations
  < 1.25; **fails for a = 1** (deviation up to 2.23). The heuristic
  `1 + log₂ a` collapses at a=1 (= 1) but actual t_period/L is
  2.5–3.2, dominated by many halvings between odd steps.
- **C-011** at wider b: **CONFIRMED at 100%.** All 96 primitive cycles
  satisfy `b | (2^K − a^L)`. Combined with tight scope: 160/160
  primitive cycles at 104 variants. The proven theorem holds.

**Interesting cells:**
- (5, 33): 18 cycles total — 3× the a=5 median.
- (7, 31): 5 cycles, four of which share length 23 (parallel L=K
  family — exactly the C-008 (3, 13) shape, but at a=7, b=31).
- (3, 47): 7 primitive cycles.
- (5, 23): 8 primitive cycles.
- (7, 45): 5 cycles.

## Thoughts
**C-003's narrowing is the most interesting finding.** The conjecture
held universally in the original scope, which was *exactly* the b
values where the L1-cycle is the only one C-011 admits. At wider b,
some b values admit additional (L, K) tuples with `b | (2^K − 7^L)`,
breaking rigidity. So C-003 is really:

> For (a=7, b), the rigid L1-cycle pattern holds **iff** the only
> (L, K) with `b | (2^K − 7^L)` and a primitive composition is
> (L=1, K=3).

This makes it a number-theoretic question about the multiplicative
orders of 2 and 7 modulo b. Given C-011's now-proven status, **C-003
reduces to a corollary** — its scope is exactly the b values where the
divisibility lattice for (a=7) is sparse.

(7, 31) with 4 parallel length-23 cycles is the C-008 shape repeated
at a different (a, b). C-008 was: (3, 13) L=5 K=8 with all 35
compositions valid because 2⁸ − 3⁵ = 13 cancels b. For (7, 31): need
2^K ≡ 7^L (mod 31). Easy to check 2^K cycles mod 31; 7^L cycles mod
31. Find a coincidence at small (L, K). Expected pattern: (L, K)
with K = some small multiple, all compositions yielding cycles. That
would explain the 4 cycles.

(5, 33) = 5 · 3 + 18: 18 cycles. b = 33 = 3·11, so inherited from
(5, 3) and (5, 11). plus primitives. That's a high count — pull it
into the structural analysis.

## Conclusion
*Solid.* L2 dispatch confirmed three of five conjectures unchanged
and refined two:
- C-001, C-007′, C-011 — confirmed.
- C-003 — refined to a number-theoretic condition on (a=7, b).
- C-009 — refined to "for a ≥ 3" (a=1 needs a different period law).

C-001 and C-011 are now near-irrefutable empirically (3 falsification
attempts each, all survived; 160/160 cycle decomposition).

## Reasoning
Two follow-ups suggest themselves:
1. **(7, 31) and similar**: structural probe like action 008 did for
   (3, 13). Find the (L, K) with `b | (2^K − 7^L)` and verify the 4
   parallel cycles via composition enumeration.
2. **a=1 period law**: for a=1, the law should be different — maybe
   `t_period/L ≈ 1 + 2 = 3` (one odd step + average 2 halvings? since
   T(odd n) = n + b for a=1, the result n + b is even iff n + b is
   even iff n is odd (b odd, so n + b even when n odd). So one halving
   each odd step on average is wrong — it's one halving every odd
   step, *plus* possibly more halvings if the result is divisible by
   higher 2-powers).

C-011 + b-scaling decomposition continues to fully account for the
atlas at 104 variants. At this point the **structural classification
theorem is the run's main deliverable.**

## Next
- **CONJECTURES.md updates:** record falsification attempts surviving
  for each (C-001 → 3 attempts; C-003 narrows scope; C-009 caveat for
  a=1; C-011 → 160/160 across 104 variants).
- **PREDICTIONS.tsv:** no new predictions registered for action 012;
  the conjecture-level falsifications are tracked in CONJECTURES.md.
- Wait for action 013 (n_new structural explanation).
- Consider an action 015: probe (7, 31) parallel cycles structurally.

## Linked
- autoresearch/archive/012-sweep.py
- autoresearch/archive/012-results.parquet
- autoresearch/archive/012-cycles.parquet
- autoresearch/archive/012-summary.md
