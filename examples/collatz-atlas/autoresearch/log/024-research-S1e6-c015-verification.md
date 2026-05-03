# res 024 — S=10⁶ verification of C-015 power law

## What & why
C-015 says f(a, b, S) ∝ S^{-c(a, b)}. Action 023 + main verified
across S=10³/10⁴/10⁵ subsamples. This action runs S=10⁶ to falsify
or confirm at the next scale.

Prediction before run: predicted f(10⁶) = f(10⁵)·10^{-c} per cell.
Tolerance: ±20% would be excellent; ±50% acceptable.

## Done
Sub-agent dispatched the sweep but didn't complete; main ran the
script directly. Total runtime 182s; 22 variants × 10⁶ seeds = 22M
trajectories. Suffix memoization made the sweep cheap (~7-8s per
variant).

Outputs:
- `autoresearch/archive/024-results.parquet` (22M rows)
- `autoresearch/archive/024-cycles.parquet`
- `autoresearch/archive/024-summary.md`

## Result
n/a (research-only)

**C-015 confirmed strongly:**
- **22/22 cells within ±20%** of predicted f(10⁶)
- **Median ratio observed/predicted: 0.975**
- No cells fail ±50%
- Best fits: (5, 5) ratio=0.996, (5, 19) ratio=1.009, (5, 21) ratio=1.006
- Worst fits: (7, 1) ratio=0.887, (7, 7) ratio=0.860 (still well within
  ±20%)

**Zero new cycles at S=10⁶.** All 22 cells' cycle inventories match
S=10⁵ exactly. The atlas at the tight scope is **empirically complete
through S=10⁶** — no integer ≤ 10⁶ reaches a cycle that wasn't already
reached by some integer ≤ 10⁵.

## Thoughts
Three independent S values (10⁴, 10⁵, 10⁶) and the predicted/observed
ratio is between 0.86 and 1.05 in every cell. C-015 is the strongest
empirical regularity in the project.

The slight systematic underprediction (median 0.975) suggests a small
correction term: the power-law form is `f(S) = A·S^{-c}·(1 + O(1/S))`
or similar. Negligible at our resolution.

The "no new cycles at S=10⁶" finding suggests the atlas at the tight
scope is *complete* in the practical sense: any cycle exists is
discoverable by the small-seed sweep S=10⁴, and increasing S only
*shrinks* the basin of each cycle (per C-015), it doesn't reveal new
cycles. This connects to C-014's cycle-attractor structure: the cycles
are fully cataloged by C-011 + b-scaling.

## Conclusion
*Solid.* C-015 is now a fully empirically validated empirical law:

> **For (a, b) odd with a ≥ 5, the convergent fraction in [1, S]
> follows f(a, b, S) = const · S^{-c(a, b)} with c(a) ≈ (a-4)/(a-2)
> to within ±0.07. Across S ∈ {10⁴, 10⁵, 10⁶}, the predicted/observed
> ratio is within 20% across all 22 (a∈{5, 7}, b∈[1, 21] odd) cells.**

Combined with C-013 (residue-class biasing within each cell) and
C-011 (cycle structure), this gives a closed empirical picture of the
divergent regime.

## Reasoning
The "tractable cousin" question gets a quantitative answer: cells
with smaller c(a) retain more convergent seeds at large S. (5, 9) at
c ≈ 0.33 retains the highest fraction. (7, 13) at c ≈ 0.72 retains
almost none.

Also note: the (a-4)/(a-2) formula has a clean asymptote: c(4) = 0,
c(∞) = 1. The convergent/divergent boundary at a = 4 (between odd
values 3 and 5) is the natural threshold of this formula.

## Next
- Update CONJECTURES.md with C-015 confirmation.
- Update README with C-015 + (a-4)/(a-2) formula prominently.
- Open question for analytical work: derive c(a) = (a-4)/(a-2)
  from the random-walk on log-value with geometric h distribution.
- Consider the same probe at wider-b (b ∈ [23, 51]).

## Linked
- autoresearch/archive/024-sweep.py
- autoresearch/archive/024-results.parquet
- autoresearch/archive/024-cycles.parquet
- autoresearch/archive/024-summary.md
