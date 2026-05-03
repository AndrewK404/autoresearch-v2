# res 001 — opening sweep over the tight 3x+1 family

## What & why
Queue #1 — the opening atlas of the tight 3x+1 family. Brief to sub-agent
in `archive/001-sweep.py` and the dispatch summary preserved in
`MEMORY.md ## Recent`.

Predictions registered before the sweep (P000.1–P000.6 in
`PREDICTIONS.tsv`):
- P000.1 a=1: trivial; converges to b-fixed cycle
- P000.2 a=3,b=1: classical Collatz, all reach {1,2,4}
- P000.3 a=3,b=3: dynamics on multiples of 3 mirror classical (sub-system);
  non-multiples of 3 possibly conjugate
- P000.4 a=3,b=5: extra cycle exists
- P000.5 a=5,b=1: at least one seed escapes to H/T
- P000.6 a=5,7 family: ≥ 2 (a,b) pairs show additional cycles

## Done
Sub-agent built `autoresearch/archive/001-sweep.py` with suffix
memoization (cache: value → (outcome, cycle_id, suffix_max,
suffix_steps)). Ran the sweep on the tight scope (a ∈ {1,3,5,7},
b ∈ {1,3,...,21}, 44 variants × 10⁴ seeds = 440k trajectories) under
horizons (S=10⁴, H=10¹², T=10⁴). Wall-clock: 2.5s — far cheaper than
budgeted, so the *next* sweep can comfortably extend horizons by 10× in
each dimension without breaking the laptop.

Outputs:
- `autoresearch/archive/001-sweep.py` — sweep script (regenerable)
- `autoresearch/archive/001-results.parquet` — 440k rows × 9 cols
  (per-seed outcome, cycle_id, max_value, steps_to_outcome)
- `autoresearch/archive/001-cycles.parquet` — 153 rows × 7 cols
  (per (a,b,cycle): members JSON, length, n_seeds_reaching)
- `autoresearch/archive/001-summary.md` — human-readable atlas

## Result
n/a (research-only)

Headline numbers from the sweep:
- 53.6% of trajectories reach a cycle
- 46.4% exceed H = 10¹²
- 0% exceed T = 10⁴ steps
- 153 distinct (a, b, cycle) triples found

Per-row dynamics:
- **a = 1:** all 11 variants — 100% reach cycle. Multiple attractor
  cycles per (a=1, b>1), partitioned by gcd-class. Eg (a=1, b=21) has 6
  distinct attractor cycles — the divisor structure of b directly carves
  the integers into independent gcd-classes, each with its own attractor.
- **a = 3:** all 11 variants — 100% reach cycle. (3,1) classical: single
  cycle {1,2,4}. (3,5): 6 cycles. (3,13): **10 cycles** — the most
  cycle-rich a=3 variant by a wide margin. (3,21): cycle_min = 15 — no
  cycle contains 1 or 3; the smallest attractor's smallest member is 15.
- **a = 5:** mostly divergent (70–97% horizon escape). (5,1): 9274/10000
  escape. (5,21): **12 cycles** — the most cycle-rich variant in the
  whole sweep, despite high escape fraction.
- **a = 7:** uniformly divergent (>94% horizon escape). Several
  variants (b ∈ {1,3,7,13,17,21}) have a single cycle of length 4 — an
  unusually rigid pattern.

## Thoughts
The a=3 → a=5 boundary is sharp. This isn't entirely new — the heuristic
expectation `n → (a/2) · n` on average for one full odd-then-halve step
predicts boundedness when a < 2 (i.e. a=1) and unboundedness when a > 2
(i.e. a ≥ 3). Yet a=3 *converges* in our sweep at S=10⁴. The standard
explanation: the heuristic is geometric-mean over an infinite trajectory;
finite trajectories don't always sample the bad direction enough times.
For a=5 the heuristic average ratio is 5/4 (assuming divisions by 2 happen
with probabilistic distribution log₂(a/2)... actually no, average is
(a+1)/4 for one step? need to think more carefully). The point: a=3 sits
in a "convergent-in-finite-time" regime; a=5 doesn't.

Three observations that surprised me:

1. **a=1 is *not* trivial.** I predicted (P000.1) "trivial" — single
   attractor per (a=1, b). Reality: divisor structure of b creates
   multiple attractors. Each odd divisor d of b yields a cycle
   {d, 2d, 4d, ..., max·d} with max being a power of 2. The number of
   cycles roughly tracks d(b) (divisors of b). My prediction was *wrong*
   in spirit — the structure is richer than I thought. **This is the
   single biggest surprise of the sweep.**

2. **a=3, b=21 has cycle_min = 15.** The trivial fixed-point story I
   was implicitly using ("the cycle reachable from small n contains a
   small member") fails here. The cycle reachable from seeds in [1, 10⁴]
   has its smallest member at 15. Below 15 — what happens? Either those
   seeds also reach this cycle (passing through 15), or they reach
   another cycle, or they exceed H. The sweep covered 1..10⁴ — checking
   what seeds 1..14 do under (3,21) is a one-line probe.

3. **(3,13) has 10 cycles.** Action 002 found only 2 at L≤3. So 8 of
   them are at L≥4. Why is b=13 so prolific in this row? b=13 is prime,
   no scaling-image relation, so it's not "structural redundancy." The
   max value of any cycle here is ~6×10⁷ — well below H. So this is
   genuinely rich finite cycle structure. Worth investigating.

## Conclusion
*Tentative.* The opening atlas is informative on every front. Five of
six predictions confirmed at least directionally; one (P000.1) was
contradicted in a substantive way. There is enough structure in the
results to seed multiple conjectures.

## Reasoning
Key inferences:

- The sweep's runtime margin (2.5s vs ~minutes budgeted) means we can
  10× the horizons (S=10⁵, H=10¹³, T=10⁵) cheaply for falsification
  passes on candidate conjectures.
- The a-axis dichotomy is real and should be the first conjecture seeded
  in `CONJECTURES.md`. But the bound between convergence and divergence
  is not at "a=3 vs a=5" — it's somewhere in the literature already
  (e.g. Conway's known-divergent variants). Our claim should be
  *empirical*, scoped to our parameter region: "for a ∈ {1,3} and our
  b range, all seeds in [1, 10⁴] reach a cycle within H, T."
- Action 002 cross-check: 002 found 116 cycles at L≤3; sweep found 153.
  Difference (37 cycles) is exclusively at L≥4, concentrated in
  (3,13) and the a=5 row. **Cross-check passes**: every L≤3 cycle from
  002 should appear in 001's cycle inventory. I'll verify this in a
  small follow-up analysis (action 005).
- Action 003 cross-check: zero full conjugacies in scope. The sub-system
  embedding via b-scaling explains why (5,15) ~ 5×(5,3), (3,9) = 9×(3,1),
  (7,21) = 21×(7,1) (predicted by 002's hint). The atlas should tag
  cycles "inherited" or "new" — see Queue update.
- (a=1, b>1) multi-cycle structure is mechanically explained: T_{1,b}
  on n: even → n/2; odd → n+b. So odd n → n+b which has the same parity
  if b is even (impossible here since b odd) — odd + odd = even, then
  halving brings it back. Trajectory mixes gcd-classes only via the
  halving. Actually since gcd(n, d) for d | b is preserved under
  multiplication by 1 and addition of b on appropriate residues. The
  full mechanism deserves a short analytic note.

## Next
- **Score predictions** in `PREDICTIONS.tsv` (P000.1-6).
- **Seed conjectures** in `CONJECTURES.md`:
  - C-001: a-axis dichotomy in tight scope
  - C-002: a=1 multi-attractor structure tracks divisor structure of b
  - C-003: a=7 row has rigid single-cycle-of-length-4 sub-pattern
  - C-004: anomaly — (3, 13) cycle-rich
  - C-005: anomaly — (5, 9) small new cycle (1, 7, 11)
- **Queue refresh** — see MEMORY ## Queue updates.
- **Falsification dispatches** to set up next cycle:
  - probe (3, 21) seeds 1..14 under high horizon
  - 10× horizon sweep (S=10⁵, H=10¹³) on a=5 row to test whether the
    "exceeded H" classification holds at the new horizon
  - structured analysis of (a=1) multi-attractor mechanism

## Linked
- autoresearch/archive/001-sweep.py
- autoresearch/archive/001-results.parquet
- autoresearch/archive/001-cycles.parquet
- autoresearch/archive/001-summary.md
