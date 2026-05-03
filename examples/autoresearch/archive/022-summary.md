# Action 022 — h-autocorrelation along trajectories


## Setup

Hypothesis: the ~0.6× systematic gap between empirical α and random-walk-predicted α (action 019) is explained by positive autocorrelation of `h_t = v_2(a·n_t + b)` along actual shortcut trajectories, which inflates the variance of the log-value walk per step:

    σ²_eff = σ² · (1 + 2·Σ_{t≥1} ρ_t)

Predicted α correction factor = σ²/σ²_eff = 1/(1 + 2·Σ ρ_t).

If 2·Σ ρ_t ≈ 0.67, then α_emp/α_theory ≈ 1/1.67 ≈ 0.60.

For each cell in the sample, we ran up to 2000 trajectories with n_0 sampled uniformly from [10000, 100000], iterating the shortcut map `σ(n) = (a·n + b)/2^{v_2(a·n + b)}` for at most 200 steps (or until the trajectory revisits a value or exceeds 1e+18). Recorded `h_t` at each step. Target ~100000 pooled h values per cell. Lag-t autocorrelation ρ_t was computed by collecting (h_s, h_{s+t}) pairs only within the same trajectory, pooling across trajectories, and taking Pearson correlation.

## Per-cell autocorrelation

| a | b | n_traj | n_h | mean_len | E[h] | Var(h) | ρ_1 | ρ_2 | ρ_3 | ρ_4 | ρ_5 | 2·Σρ_t | corr factor 1/(1+2Σρ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 1 | 730 | 100048 | 137.1 | 2.014 | 2.030 | +0.007 | -0.004 | +0.003 | -0.006 | +0.007 | +0.013 | 0.987 |
| 5 | 9 | 822 | 100052 | 121.7 | 2.007 | 2.043 | +0.007 | +0.000 | -0.008 | -0.003 | +0.004 | -0.001 | 1.001 |
| 5 | 19 | 703 | 100003 | 142.3 | 2.022 | 2.103 | +0.001 | +0.011 | +0.006 | -0.013 | -0.006 | -0.004 | 1.004 |
| 7 | 1 | 1762 | 100013 | 56.8 | 1.996 | 1.975 | +0.001 | -0.003 | -0.002 | +0.009 | +0.004 | +0.017 | 0.983 |
| 7 | 13 | 1764 | 100045 | 56.7 | 1.996 | 1.991 | -0.001 | +0.001 | -0.002 | -0.001 | -0.004 | -0.016 | 1.016 |
| 9 | 1 | 2000 | 79376 | 39.7 | 2.006 | 1.994 | -0.006 | +0.002 | -0.001 | -0.006 | +0.004 | -0.015 | 1.016 |
| 11 | 7 | 2000 | 63210 | 31.6 | 1.996 | 2.003 | -0.006 | -0.002 | +0.003 | +0.012 | -0.000 | +0.014 | 0.987 |
| 13 | 1 | 2000 | 54708 | 27.4 | 2.004 | 2.001 | +0.003 | -0.000 | +0.010 | +0.007 | +0.008 | +0.055 | 0.948 |

## Pooled statistics across cells

| lag | mean ρ_t | median ρ_t |
|-----|----------|------------|
| 1 | +0.0005 | +0.0006 |
| 2 | +0.0008 | +0.0000 |
| 3 | +0.0011 | +0.0010 |
| 4 | -0.0003 | -0.0022 |
| 5 | +0.0019 | +0.0036 |

- mean (Σ_{t=1..5} ρ_t) across cells = **+0.0040**
- 2·Σρ_t (mean) = **+0.0079**  →  predicted shrinkage factor σ²/σ²_eff = 1/(1 + 2Σρ_t) = **0.9921**
- median (Σ_{t=1..5} ρ_t) across cells = **+0.0031**
- 2·Σρ_t (median) = **+0.0062**  →  predicted shrinkage factor = **0.9939**

## Comparison to empirical α_emp / α_theory ≈ 0.6

- Empirical (action 019) ratio: **0.600**
- Predicted (mean): **0.992**  (Δ = +0.392)
- Predicted (median): **0.994**  (Δ = +0.394)

## Conclusion

**weakly supported / falsified**: autocorrelation alone does not reproduce the 0.6× factor.


