# res 006 — 10× horizon falsification sweep + sub-lattice attractivity probe

## What & why
Queue items #3, #4, #5 — the consolidated falsification cycle for the
opening conjectures. Two jobs combined:

- **Job A:** re-run the opening sweep at 10× horizons (S=10⁵, H=10¹³,
  T=10⁵). Test C-001 (a-axis dichotomy at higher horizon), C-003 (a=7
  rigidity), C-004 (3,13 cycle count stability).
- **Job B:** sub-lattice attractivity probe (C-006). For each (a, b)
  with composite b and odd λ > 1 with λ | b, log first hit time into λZ
  for every seed n₀ ∉ λZ.

Predictions before dispatch:
- C-001 confirmed: zero a∈{1,3} seeds exceed H at 10× horizon.
- C-003 confirmed: a=7 row only reaches L1 cycles {b, 2b, 4b, 8b}.
- C-004: I expected possibly 1–2 new cycles for (3, 13) at higher
  horizon. *Was wrong.*
- C-006: I expected forward-attractivity to *hold* for a ∈ {1, 3} but
  *probably fail* for a ∈ {5, 7}. The actual result was sharper.

## Done
Sub-agent built `006-sweep.py` extending 001's suffix-memoized sweep
plus the attractivity logging. Total 2.2M a∈{1,3} trajectories +
2.2M a∈{5,7} trajectories = 4.4M total. Runtime: 46.4s wall-clock —
well within budget; 10× horizon expansion was effectively free.

Outputs:
- `autoresearch/archive/006-sweep.py`
- `autoresearch/archive/006-results.parquet`
- `autoresearch/archive/006-cycles.parquet`
- `autoresearch/archive/006-attractivity.parquet`
- `autoresearch/archive/006-summary.md`

## Result
n/a (research-only)

**C-001 — CONFIRMED at 10× horizon.** All 2.2M trajectories for
a ∈ {1, 3}, b odd in [1, 21], n₀ ∈ [1, 10⁵] reach a cycle within
T = 10⁵ steps without exceeding H = 10¹³. Zero falsifiers.

**C-003 — CONFIRMED at 10× horizon.** For (a=7, b ∈ {1, 3, 7, 13, 17, 21}),
the only cycles reached by any seed in [1, 10⁵] are the L1 cycles
{b, 2b, 4b, 8b}. No new or longer cycles. The vast majority of seeds
still exceed H = 10¹³ — the rigidity holds *and* the divergence holds
together.

**C-004 / C-008 — both reinforced.** (3, 13) cycle count remains 10 at
10× horizon. The 7 primitive L=5 cycles in C-008 are still all that
appear at L=5; no new ones emerge.

**Across the whole atlas: zero new cycles at 10× horizon.** All 153
cycles in 001-cycles.parquet appear in 006-cycles.parquet with
`new_in_006 = False`. **The cycle inventory at the tight scope is
empirically complete at S = 10⁴.** This is itself a significant
finding — it means seeds beyond 10⁴ don't open up new attractor
structure for these (a, b).

**C-006 — FALSIFIED, dramatically.**
543,514 counterexamples: seeds n₀ ∉ λZ that exceed H = 10¹³ without
ever entering λZ. Per (a, b, λ) (largest cells):
- (5, 9, 3): 55,644
- (7, 9, 3): 66,598
- (5, 15, 3): 64,463
- (7, 15, 3): 66,128
- (7, 15, 5): 78,754
- (5, 21, 3): 65,079
- (5, 21, 7): 80,181
- (7, 21, 3): 66,667

For a = 3, λZ *is* forward-attractive: max hit time ≤ 17 steps across
all (3, b) with composite b. So the failure is specifically at
a ∈ {5, 7} when b is composite — exactly the cells where the sub-system
*on the complement of λZ* carries enough divergent mass to escape H
without crossing into λZ.

## Thoughts
The biggest revelation: **the cycle inventory is complete at S = 10⁴ for
the tight scope.** I had assumed extending to 10⁵ would surface new
small-period cycles missed by the smaller seed range. It didn't. Two
interpretations:

1. The cycle structure is genuinely complete at this scope — every
   primitive cycle of T_{a, b} for these (a, b) reaches at least one
   seed in [1, 10⁴]. That's a strong claim.
2. There are cycles at higher orbits (large cycle_min) that no seed in
   [1, 10⁵] reaches. The convergence basins of those cycles may live
   in regions of the integers we didn't probe.

The C-006 falsification is structurally important. It says:

> When a ∈ {5, 7} and b is composite, the sub-system on integers *not*
> divisible by λ (for proper divisors λ | b) has its own divergent
> dynamics. The bZ ⊂ ℤ embedding is *not* a "trap" that absorbs
> non-bZ seeds.

This rules out reductionist arguments that try to reduce (a, λb)'s
behavior to (a, b)'s asymptotically. The two sub-systems are
independent, and the divergent one dominates statistically.

For a = 3 the situation is opposite: λZ *is* forward-attractive (max
hit time ≤ 17 steps). So a = 3 has the reductionist property; a ∈ {5, 7}
doesn't. **This is a sharp split that traces back to the heuristic
expansion ratio (a · n + b)/n ≈ a / 2**: for a = 3 the contraction by
1/2 dominates over the expansion by 3/2, on average per shortcut step;
for a = 5, 7 it doesn't.

Combined with C-009 (period law t_period ≈ L · (1 + log₂ a)), we have
two related phenomena:
- a = 1, 3: convergent dynamics, attractive sub-systems, cycles cover
  small integers densely.
- a = 5, 7: divergent dynamics for most seeds, non-attractive sub-systems,
  cycles are sparse and most mass escapes.

## Conclusion
*Tentative.* The tight scope is mostly mapped. Conjectures C-001 and
C-003 have survived two independent falsification attempts (original
sweep + 10× horizon). C-006 is dead. C-008 (3,13)'s 7-cycle family
holds firm. Key candidates for promotion to LESSONS.md (pending user
confirmation):

- C-001 (a-axis dichotomy in tight scope) — survived
- C-003 (a=7 row rigid L1 cycle pattern) — survived
- C-007′ (n_inherited ≥ d(b)−1 for a=1) — probed once, holds
- C-008 (3,13) 7 primitive L=5 cycles family — probed once, holds; needs
  algebraic enumeration to be definitive (action 008)
- C-009 (period law) — probed once, deviation < 4% across 153 cycles
- (Falsification record:) C-006 forward-attractivity falsified with
  543k counterexamples — record this as a *negative finding* per
  TASK.md's "negative results count" instruction.

## Reasoning
Key inferences for next steps:

1. **At least 4 conjectures (C-001, C-003, C-008, C-009) plus C-007′ and
   the C-006 falsification are ready to ping the user about** per the
   pre-agreed cadence ("only at conjecture promotion or strategy
   escalation"). I should hand the list to the user with a recommended
   read-off.

2. **Strategy escalation L1 → L2.** The tight scope is mapped; further
   compute on it produces no new cycles. Continuing on the tight scope
   would be diminishing returns. L2 = systematic exploration (extend
   the b range, add divisor c variation, possibly extend a). This is
   exactly the L1 → L2 transition the skill prescribes.

3. **One more conjecture-prep dispatch is worth it before pinging:**
   the algebraic enumeration of (3, 13)'s L = 5 cycle equation (action
   008) closes C-008 — if it confirms exactly 7 valid integer
   solutions, C-008 promotes. If it disagrees with the empirical 7,
   we have either a sweep miss or an algebraic miscount. Either way,
   the user-facing report on C-008 is sharper.

## Next
- **CONJECTURES.md updates:**
  - C-001: status proposed → surviving.
  - C-003: status proposed → surviving.
  - C-008: status proposed → probed (+ schedule action 008 to promote
    to surviving with algebraic verification).
  - C-009: status probed.
  - C-006: status falsified (with full evidence in 006-attractivity.parquet).
- **MEMORY.md ## Recent + ## Status:** record action 006 outcomes;
  signal L1 → L2 escalation candidacy.
- **Dispatch action 008:** algebraic enumeration of (3, 13) L=5 cycle
  equation. Quick analyst task.
- **Then ping user** with the survivor list + escalation question.

## Linked
- autoresearch/archive/006-sweep.py
- autoresearch/archive/006-results.parquet
- autoresearch/archive/006-cycles.parquet
- autoresearch/archive/006-attractivity.parquet
- autoresearch/archive/006-summary.md
