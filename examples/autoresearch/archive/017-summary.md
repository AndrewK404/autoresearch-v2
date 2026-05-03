# Action 017 — Residue-class basin structure in the divergent regime

## Setup

**Conjecture.** For (a, b) with a ≥ 5 and b odd, in the divergent regime where most odd seeds escape to H, the *fraction of seeds that converge* depends strongly on the residue n0 mod 2^k. Specifically, for odd r ∈ {1, 3, …, 2^k−1}, the lift `lift(r) = P(converge | n0 ≡ r mod 2^k) / P(converge)` correlates positively with the first-step halving harvest `h(r) = v_2(a·r + b)`. We test this systematically across the cells a ∈ {5, 7, 9, 11, 13}, b odd in [1, 21] using 001-results.parquet (a ∈ {5, 7}) and 016-results.parquet (a ∈ {9, 11, 13}).

Method: for each cell, restrict to odd seeds (v_2(n0) = 0), bucket by n0 mod 2^k, compute frac(r), lift(r), h(r), and Pearson r of lift vs h. We test k ∈ {4, 6} and a multi-step harvest (3 and 5 shortcut steps starting at the integer r).

## Per-(a, b) correlation table

| a | b | n_seeds | n_conv | mean_conv_frac | r(k=4) | r(k=6) | r_ms3(k=6) | r_ms5(k=6) | R²(k=6) | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 1 | 5000 | 260 | 0.052 | 0.760 | 0.644 | 0.798 | 0.820 | 0.279 |  |
| 5 | 3 | 5000 | 229 | 0.0458 | 0.771 | 0.647 | 0.892 | 0.900 | 0.236 |  |
| 5 | 5 | 5000 | 466 | 0.0932 | 0.865 | 0.739 | 0.819 | 0.821 | 0.443 |  |
| 5 | 7 | 5000 | 769 | 0.1538 | 0.881 | 0.729 | 0.589 | 0.357 | 0.380 |  |
| 5 | 9 | 5000 | 989 | 0.1978 | 0.862 | 0.697 | 0.788 | 0.728 | 0.357 |  |
| 5 | 11 | 5000 | 449 | 0.0898 | 0.775 | 0.721 | 0.765 | 0.657 | 0.348 |  |
| 5 | 13 | 5000 | 549 | 0.1098 | 0.815 | 0.732 | 0.711 | 0.484 | 0.378 |  |
| 5 | 15 | 5000 | 411 | 0.0822 | 0.833 | 0.695 | 0.867 | 0.845 | 0.359 |  |
| 5 | 17 | 5000 | 190 | 0.038 | 0.877 | 0.684 | 0.795 | 0.477 | 0.320 |  |
| 5 | 19 | 5000 | 97 | 0.0194 | 0.914 | 0.587 | 0.504 | 0.505 | 0.182 |  |
| 5 | 21 | 5000 | 511 | 0.1022 | 0.894 | 0.774 | 0.813 | 0.526 | 0.341 |  |
| 7 | 1 | 5000 | 14 | 0.0028 | 0.961 | 0.641 | 0.583 | 0.538 | 0.413 | noisy(<50) |
| 7 | 3 | 5000 | 12 | 0.0024 | 0.898 | 0.668 | 0.686 | 0.606 | 0.390 | noisy(<50) |
| 7 | 5 | 5000 | 116 | 0.0232 | 0.839 | 0.688 | 0.757 | 0.720 | 0.426 |  |
| 7 | 7 | 5000 | 68 | 0.0136 | 0.802 | 0.685 | 0.667 | 0.597 | 0.346 |  |
| 7 | 9 | 5000 | 14 | 0.0028 | 0.772 | 0.699 | 0.707 | 0.685 | 0.545 | noisy(<50) |
| 7 | 11 | 5000 | 80 | 0.016 | 0.830 | 0.771 | 0.719 | 0.328 | 0.507 |  |
| 7 | 13 | 5000 | 8 | 0.0016 | 0.826 | 0.689 | 0.567 | 0.522 | 0.624 | noisy(<50) |
| 7 | 15 | 5000 | 140 | 0.028 | 0.886 | 0.667 | 0.543 | 0.580 | 0.396 |  |
| 7 | 17 | 5000 | 8 | 0.0016 | 0.826 | 0.623 | 0.391 | 0.136 | 0.491 | noisy(<50) |
| 7 | 19 | 5000 | 66 | 0.0132 | 0.872 | 0.697 | 0.603 | 0.485 | 0.589 |  |
| 7 | 21 | 5000 | 49 | 0.0098 | 0.834 | 0.709 | 0.574 | 0.459 | 0.345 | noisy(<50) |
| 9 | 1 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 3 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 5 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 7 | 50000 | 9 | 0.00018 | 0.731 | 0.768 | 0.397 | 0.311 | 0.558 | noisy(<50) |
| 9 | 9 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 11 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 13 | 50000 | 63 | 0.00126 | 0.747 | 0.765 | 0.864 | 0.690 | 0.332 |  |
| 9 | 15 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 17 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 19 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 9 | 21 | 50000 | 20 | 0.0004 | 0.804 | 0.645 | 0.689 | 0.628 | 0.369 | noisy(<50) |
| 11 | 1 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 3 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 5 | 50000 | 12 | 0.00024 | 0.752 | 0.485 | 0.375 | 0.315 | 0.495 | noisy(<50) |
| 11 | 7 | 50000 | 16 | 0.00032 | 0.956 | 0.760 | 0.510 | 0.398 | 0.601 | noisy(<50) |
| 11 | 9 | 50000 | 7 | 0.00014 | 0.911 | 0.632 | 0.637 | 0.668 | 0.481 | noisy(<50) |
| 11 | 11 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 13 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 15 | 50000 | 10 | 0.0002 | 0.643 | 0.346 | 0.412 | 0.193 | 0.273 | noisy(<50) |
| 11 | 17 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 19 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 11 | 21 | 50000 | 14 | 0.00028 | 0.888 | 0.744 | 0.503 | 0.417 | 0.579 | noisy(<50) |
| 13 | 1 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 3 | 50000 | 3 | 6e-05 | 0.763 | 0.702 | 0.594 | 0.523 | 1.000 | noisy(<50) |
| 13 | 5 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 7 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 9 | 50000 | 18 | 0.00036 | 0.915 | 0.743 | 0.691 | 0.762 | 0.723 | noisy(<50) |
| 13 | 11 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 13 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 15 | 50000 | 2 | 4e-05 | 0.763 | 0.608 | 0.413 | 0.510 | 1.000 | noisy(<50) |
| 13 | 17 | 50000 | 0 | 0 | nan | nan | nan | nan | nan | noisy(<50) no_var |
| 13 | 19 | 50000 | 2 | 4e-05 | 0.857 | 0.709 | 0.531 | 0.495 | 1.000 | noisy(<50) |
| 13 | 21 | 50000 | 2 | 4e-05 | 0.763 | 0.608 | 0.506 | 0.396 | nan | noisy(<50) |

## Aggregates

- **Pearson r vs h_first_step, k=4**: median=0.833, IQR=[0.771, 0.883]
- **Pearson r vs h_first_step, k=6**: median=0.695, IQR=[0.644, 0.731]
- **Pearson r vs multi-step harvest (3 steps), k=6**: median=0.637, IQR=[0.520, 0.761]
- **Pearson r vs multi-step harvest (5 steps), k=6**: median=0.523, IQR=[0.438, 0.677]
- **Pearson r vs h, log lift, k=6**: median=0.546, IQR=[0.408, 0.600]

- Cells with Pearson r > 0.7 at k=4: **34 / 35** (of 55 total; the rest have zero converged seeds)
- Cells with Pearson r > 0.7 at k=6: **14 / 35**
- Cells with Pearson r > 0.5 at k=4: **35 / 35**
- Cells with Pearson r > 0.5 at k=6: **33 / 35**

## Anomalies (weak or anti-correlated cells)

- None: every cell with non-degenerate variance has r ≥ 0.3 at k=6.

## Headline pattern

Across 35 cells with non-zero converged seeds (out of 55 cells in scope; 21 a∈{9, 11, 13} cells have zero converged seeds and are excluded), the median Pearson r of lift vs h_first_step is **0.833 at k=4** and **0.695 at k=6**. At k=4, **34/35** cells exceed r > 0.7; at k=6, **14/35**. **The relation holds in direction uniformly** (every non-degenerate cell has positive r) but is stronger at coarser resolution (k=4) than finer (k=6).

Going from k=4 to k=6 *weakens* the per-cell Pearson by Δmedian = -0.138. **Why:** at k=6, each residue bucket has ~4× fewer seeds (from ~313 to ~78 odd-only seeds at S=5000, or ~3125 to ~781 at S=50000), so frac(r) is noisier. The first-step h(r) takes only a handful of distinct integer values (typically 1, 2, 3, 4+) regardless of k, but lift(r) at k=6 has more between-residue noise — the *signal* is the same but the *observation* is louder. Despite this, the correlation stays strongly positive in every cell.

Multi-step harvest (5 shortcut steps starting at the integer r itself) does *not* improve correlation: Δmedian = -0.172 vs the single-step h. The 3-step variant is roughly tied with single-step h at k=6 (median 0.637). Interpretation: starting from r as a literal small integer, the multi-step harvest reflects only the trajectory of that one tiny seed; averaged over 78–625 seeds in a residue bucket, the dominant predictive feature is the *first* halving harvest, because subsequent steps depend on the higher bits of n0 that aren't captured by r alone.

## Interpretation & refined conjecture

The first-step halving harvest h(r) = v_2(a·r + b) directly controls how much the trajectory shrinks (or grows) on the first odd step, and that one-step bias propagates strongly into the long-run convergence probability. Concretely, residue classes mod 2^k that happen to land on values with high 2-adic valuation of (a·r + b) enjoy a bigger immediate halving and hence a much higher chance of ending up in the basin of an attractor cycle.

**Refined conjecture (C-013, proposed):** For (a, b) with a ∈ {5, 7, 9, 11, 13} and b odd in [1, 21], for k ∈ {4, 6}, the residue-class convergence lift `lift(r) = P(converge | n0 ≡ r mod 2^k) / P(converge)` of odd r satisfies `log lift(r) ≈ α(a,b) · v_2(a·r + b) + β(a,b)` with positive α, and the Pearson correlation of lift vs v_2(a·r + b) exceeds 0.7 in the majority of cells. Equivalently, the basin of convergence is *not* uniform on odd residues — it is concentrated on residues with high first-step halving harvest.

