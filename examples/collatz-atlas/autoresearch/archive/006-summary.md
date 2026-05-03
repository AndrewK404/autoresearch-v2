# 006 — 10x horizon falsification sweep + sub-lattice attractivity

## Setup

Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. Scope: `a ∈ {1,3,5,7}`, `b ∈ {1,3,5,7,9,11,13,15,17,19,21}` (44 variants). Per-variant: every seed `n0 ∈ [1, 10^5]`. Horizons: value bound `H = 10^13`, step bound `T = 10^5`. Outcomes: `cycle` (revisit), `exceeded-H`, `exceeded-T`.

Cycle IDs reuse 001's IDs where the same member set appears; new cycles get new IDs (column `new_in_006 = True`).

## Diff vs action 001

| a | b | n_cycles_001 | n_cycles_006 | new_cycles |
|---|---|--------------|--------------|------------|
| 1 | 1 | 1 | 1 | 0 |
| 1 | 3 | 2 | 2 | 0 |
| 1 | 5 | 2 | 2 | 0 |
| 1 | 7 | 3 | 3 | 0 |
| 1 | 9 | 3 | 3 | 0 |
| 1 | 11 | 2 | 2 | 0 |
| 1 | 13 | 2 | 2 | 0 |
| 1 | 15 | 5 | 5 | 0 |
| 1 | 17 | 3 | 3 | 0 |
| 1 | 19 | 2 | 2 | 0 |
| 1 | 21 | 6 | 6 | 0 |
| 3 | 1 | 1 | 1 | 0 |
| 3 | 3 | 1 | 1 | 0 |
| 3 | 5 | 6 | 6 | 0 |
| 3 | 7 | 2 | 2 | 0 |
| 3 | 9 | 1 | 1 | 0 |
| 3 | 11 | 3 | 3 | 0 |
| 3 | 13 | 10 | 10 | 0 |
| 3 | 15 | 6 | 6 | 0 |
| 3 | 17 | 3 | 3 | 0 |
| 3 | 19 | 2 | 2 | 0 |
| 3 | 21 | 2 | 2 | 0 |
| 5 | 1 | 3 | 3 | 0 |
| 5 | 3 | 7 | 7 | 0 |
| 5 | 5 | 3 | 3 | 0 |
| 5 | 7 | 6 | 6 | 0 |
| 5 | 9 | 10 | 10 | 0 |
| 5 | 11 | 5 | 5 | 0 |
| 5 | 13 | 5 | 5 | 0 |
| 5 | 15 | 7 | 7 | 0 |
| 5 | 17 | 4 | 4 | 0 |
| 5 | 19 | 4 | 4 | 0 |
| 5 | 21 | 12 | 12 | 0 |
| 7 | 1 | 1 | 1 | 0 |
| 7 | 3 | 1 | 1 | 0 |
| 7 | 5 | 3 | 3 | 0 |
| 7 | 7 | 1 | 1 | 0 |
| 7 | 9 | 2 | 2 | 0 |
| 7 | 11 | 2 | 2 | 0 |
| 7 | 13 | 1 | 1 | 0 |
| 7 | 15 | 4 | 4 | 0 |
| 7 | 17 | 1 | 1 | 0 |
| 7 | 19 | 2 | 2 | 0 |
| 7 | 21 | 1 | 1 | 0 |

### Variants with new cycles (members, len)

- No new cycles found in any variant.

## C-001 verdict (a ∈ {1,3}, b odd in [1,21])

**CONFIRMED at 10× horizon.** All 2200000 trajectories (a∈{1,3}) reached a cycle within T=10^5 steps without exceeding H=10^13.

## C-003 verdict (a=7, b ∈ {1,3,7,13,17,21}: only L1 cycle {b,2b,4b,8b})

**CONFIRMED at 10× horizon.** For every b ∈ {1,3,7,13,17,21}, the only cycles reached by seeds in [1,10^5] are the L1 cycles {b, 2b, 4b, 8b}.

## C-004 verdict ((3, 13) cycle richness at 10× horizon)

- Cycle count (a=3, b=13) at 001 horizon: **10**.
- Cycle count at 10× horizon: **10**.
- New cycles at 10× horizon: **0**.

## Sub-lattice attractivity (C-006) per (a, b, λ)

| a | b | λ | fraction_ever_entered_λZ | max_hit_time_among_entered | n_never_among_non_H | n_counterexamples_to_attractivity |
|---|---|---|--------------------------|----------------------------|---------------------|-----------------------------------|
| 1 | 9 | 3 | 0.0000 | 0 | 66667 | 0 |
| 3 | 9 | 3 | 1.0000 | 17 | 0 | 0 |
| 5 | 9 | 3 | 0.0000 | 0 | 11023 | 55644 |
| 7 | 9 | 3 | 0.0000 | 0 | 69 | 66598 |
| 1 | 15 | 3 | 0.0000 | 0 | 66667 | 0 |
| 1 | 15 | 5 | 0.0000 | 0 | 80000 | 0 |
| 3 | 15 | 3 | 1.0000 | 17 | 0 | 0 |
| 3 | 15 | 5 | 0.0000 | 0 | 80000 | 0 |
| 5 | 15 | 3 | 0.0000 | 0 | 2204 | 64463 |
| 5 | 15 | 5 | 1.0000 | 17 | 0 | 0 |
| 7 | 15 | 3 | 0.0000 | 0 | 539 | 66128 |
| 7 | 15 | 5 | 0.0000 | 0 | 1246 | 78754 |
| 1 | 21 | 3 | 0.0000 | 0 | 66667 | 0 |
| 1 | 21 | 7 | 0.0000 | 0 | 85715 | 0 |
| 3 | 21 | 3 | 1.0000 | 17 | 0 | 0 |
| 3 | 21 | 7 | 0.0000 | 0 | 85715 | 0 |
| 5 | 21 | 3 | 0.0000 | 0 | 1588 | 65079 |
| 5 | 21 | 7 | 0.0000 | 0 | 5534 | 80181 |
| 7 | 21 | 3 | 0.0000 | 0 | 0 | 66667 |
| 7 | 21 | 7 | 1.0000 | 17 | 0 | 0 |

**Total counterexamples to forward-attractivity (n0 ∉ λZ exceeding H without entering λZ):** 543514

## Runtime

- Total wall-clock: **46.4s**
- Sweep + sanity: **16.9s**
- Parquet + summary: 29.46s
- Per-variant timings (top 10 slowest):
    - (a=5, b=21): 1.23s
    - (a=7, b=15): 1.14s
    - (a=5, b=9): 1.13s
    - (a=7, b=9): 1.00s
    - (a=5, b=15): 0.66s
    - (a=7, b=21): 0.63s
    - (a=5, b=1): 0.56s
    - (a=5, b=19): 0.54s
    - (a=5, b=11): 0.54s
    - (a=5, b=7): 0.54s
