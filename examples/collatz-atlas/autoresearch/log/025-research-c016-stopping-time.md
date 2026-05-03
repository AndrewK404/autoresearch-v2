# res 025 — convergent regime stopping-time formula (C-016)

## What & why
While exploring divergent regime, also examined convergent regime
structure. For (3, 1) classical Collatz, tau(n) ~ O(log n) is
classical. For other (a, b) in convergent regime (a ∈ {1, 3}), is the
slope universal?

Predicted before checking: slope ≈ 1/|μ_T| where μ_T is per-T-step
drift = (log_2(a) - 2)/3.

## Done
Inline regression on `006-results.parquet` for (a, b) in convergent
regime. For each cell, regressed steps_to_outcome against log_2(n_0)
across all 10⁵ converged seeds.

## Result
n/a (research-only)

| (a, b) | mean tau | empirical slope | predicted 1/|μ_T| | match? |
|---|---|---|---|---|
| (3, 1) | 105.5 | 6.99 | 7.24 | ✓ within 4% |
| (3, 5) | 78.9 | 7.34 | 7.24 | ✓ |
| (3, 13) | 76.5 | 7.14 | 7.24 | ✓ |
| (1, 1) | 22.2 | 1.53 | 1.50 | ✓ |
| (1, 7) | 19.7 | 1.50 | 1.50 | ✓ |
| (1, 21) | 17.8 | 1.51 | 1.50 | ✓ |

## Thoughts
The match is very tight (within 4%). The intercept varies with b
(depends on cycle structure / where the trajectory ends up).

This is the convergent-regime analogue of C-015. Both follow from
the random-walk-on-log with drift μ_T:
- μ_T < 0: τ ≈ log_2(n)/|μ_T| (convergent, finite)
- μ_T > 0: f ∝ S^{-c(a)} (divergent, power-law decay)

For (1, b): μ_T = (log_2(1) - 2)/3 = -2/3 = -0.667 → 1/|μ_T| = 1.5 ✓
For (3, b): μ_T = (log_2(3) - 2)/3 ≈ -0.138 → 1/|μ_T| = 7.24 ✓

## Conclusion
*Solid.* C-016 records this as a clean empirical observation matching
the random-walk theory. Recorded in CONJECTURES.md.

## Linked
- (no archive — pure analysis)
