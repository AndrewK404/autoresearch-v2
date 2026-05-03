# 016 — Wider a-axis sweep: a ∈ {9, 11, 13}, b odd in [1, 21]

## Setup

Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. Scope: `a ∈ [9, 11, 13]`, `b ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]` (33 new variants). Per-variant: every seed `n0 ∈ [1, 100000]`. Horizons: value bound `H = 10000000000000`, step bound `T = 100000`. Same horizons as actions 006, 012. Cycle IDs start at 0 per (a, b).

Goal: test whether the convergent/divergent boundary at a ≤ 3 (C-001) extends, or if a = 5 / a = 7 divergence persists across wider odd a values. Probe a ∈ {9, 11, 13} in the tight b range.

## Per-variant table

| a | b | total_seeds | reached_cycle | exceeded_H | exceeded_T | n_distinct_cycles | smallest_cycle_min |
|---|---|-------------|---------------|------------|------------|-------------------|--------------------|
| 9 | 1 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 3 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 5 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 7 | 100000 | 52 | 99948 | 0 | 1 | 1 |
| 9 | 9 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 11 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 13 | 100000 | 311 | 99689 | 0 | 1 | 23 |
| 9 | 15 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 17 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 19 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 9 | 21 | 100000 | 127 | 99873 | 0 | 1 | 3 |
| 11 | 1 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 3 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 5 | 100000 | 76 | 99924 | 0 | 1 | 1 |
| 11 | 7 | 100000 | 96 | 99904 | 0 | 3 | 13 |
| 11 | 9 | 100000 | 51 | 99949 | 0 | 1 | 1 |
| 11 | 11 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 13 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 15 | 100000 | 59 | 99941 | 0 | 1 | 3 |
| 11 | 17 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 19 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 11 | 21 | 100000 | 98 | 99902 | 0 | 4 | 1 |
| 13 | 1 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 3 | 100000 | 25 | 99975 | 0 | 1 | 1 |
| 13 | 5 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 7 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 9 | 100000 | 92 | 99908 | 0 | 2 | 1 |
| 13 | 11 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 13 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 15 | 100000 | 17 | 99983 | 0 | 1 | 5 |
| 13 | 17 | 100000 | 0 | 100000 | 0 | 0 | -1 |
| 13 | 19 | 100000 | 21 | 99979 | 0 | 1 | 1 |
| 13 | 21 | 100000 | 16 | 99984 | 0 | 1 | 7 |

## C-001 wider-a verdict

Does any (a, b) with `a ∈ {9, 11, 13}` have all seeds reach a cycle? (C-001 was confirmed only at a ∈ {1, 3}.)

**No fully convergent (a, b) cells found** for a ∈ [9, 11, 13]. Every variant has at least some seeds exceeding H or T. C-001's full convergence does not extend to these wider a values.

## C-011 verdict (primitive cycle ⇒ b | (2^K − a^L))

For each `new`-tagged primitive cycle, compute K = t_period − L and check whether b divides (2^K − a^L). Theorem applies for any odd a, b — expected match rate: 100%.

| a | b | cycle_id | cycle_min | L | K | 2^K − a^L | (2^K − a^L) mod b | matches |
|---|---|----------|-----------|---|---|-----------|-------------------|---------|
| 9 | 7 | 0 | 1 | 1 | 4 | 7 | 0 | yes |
| 9 | 13 | 0 | 23 | 5 | 16 | 6487 | 0 | yes |
| 11 | 5 | 0 | 1 | 1 | 4 | 5 | 0 | yes |
| 11 | 7 | 0 | 13 | 2 | 7 | 7 | 0 | yes |
| 11 | 7 | 1 | 15 | 2 | 7 | 7 | 0 | yes |
| 11 | 7 | 2 | 19 | 2 | 7 | 7 | 0 | yes |
| 11 | 9 | 0 | 1 | 2 | 8 | 135 | 0 | yes |
| 11 | 21 | 0 | 1 | 1 | 5 | 21 | 0 | yes |
| 13 | 3 | 0 | 1 | 1 | 4 | 3 | 0 | yes |
| 13 | 9 | 0 | 1 | 3 | 12 | 1899 | 0 | yes |
| 13 | 19 | 0 | 1 | 1 | 5 | 19 | 0 | yes |

**Match rate: 11/11 (100.0%).**

## a-axis dichotomy refinement

Fraction of seeds reaching a cycle per (a, b):

| a \ b | 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 | 17 | 19 | 21 | mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **a=9** | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 | 0.000 | 0.003 | 0.000 | 0.000 | 0.000 | 0.001 | **0.000** |
| **a=11** | 0.000 | 0.000 | 0.001 | 0.001 | 0.001 | 0.000 | 0.000 | 0.001 | 0.000 | 0.000 | 0.001 | **0.000** |
| **a=13** | 0.000 | 0.000 | 0.000 | 0.000 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | **0.000** |

**Per-a aggregated convergence fractions:**

- a = 9: mean fraction of seeds reaching cycle = **0.0004** (across b ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21])
- a = 11: mean fraction of seeds reaching cycle = **0.0003** (across b ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21])
- a = 13: mean fraction of seeds reaching cycle = **0.0002** (across b ∈ [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21])

For reference (from action 006):
- a = 1: 1.0000 (full convergence)
- a = 3: 1.0000 (full convergence)
- a = 5: substantial divergence (most seeds escape)
- a = 7: substantial divergence (only b, 2b, 4b, 8b cycle captured)

## Surprises

- No notable surprises — wider a values (9, 11, 13) behave qualitatively like a = 5, 7: substantial divergence, limited cycle inventory.

## Runtime

- Total wall-clock: **17.3s**
- Sweep: **14.0s**
- Parquet + summary: 3.30s
- Per-variant timings (top 10 slowest):
    - (a=13, b=17): 0.51s
    - (a=9, b=1): 0.49s
    - (a=13, b=21): 0.48s
    - (a=11, b=1): 0.46s
    - (a=9, b=5): 0.46s
    - (a=11, b=13): 0.46s
    - (a=11, b=19): 0.45s
    - (a=11, b=3): 0.45s
    - (a=9, b=17): 0.45s
    - (a=9, b=13): 0.45s

- Total `new` (primitive) cycles found: **11**
