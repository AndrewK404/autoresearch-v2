"""
Action 022 — h-autocorrelation along trajectories.

Hypothesis: the systematic ~0.6× factor between α_emp and α_theory observed in
action 019 stems from positive autocorrelation of h_t = v_2(a*n_t + b) along
the actual shortcut trajectory (versus the iid assumption used in the
random-walk derivation).

If h is positively autocorrelated, the effective variance of the log-value
random walk per N steps is σ² · N · (1 + 2·Σ ρ_t), inflating σ² and shrinking
α. Empirical ratio 0.6 = σ²/σ²_eff implies σ²_eff/σ² ≈ 1.67, so
2·Σ ρ_t ≈ 0.67.

Method:
1. For each (a, b) in the cell sample, sample n_0 from [10⁴, 10⁵].
2. Run shortcut trajectory n_{t+1} = (a*n_t + b) / 2^v_2(a*n_t + b) for up to
   200 shortcut steps, recording h_t at each step.
3. Stop early if value exceeds H_MAX or trajectory reaches a cycle.
4. Pool h_t across trajectories per cell.
5. Compute lag-t autocorrelation ρ_t = corr(h_s, h_{s+t}) for t = 1..5.
   We use the per-trajectory pairing approach (only pair within the same
   trajectory, then pool the (h_s, h_{s+t}) pairs across all trajectories
   to compute Pearson correlation).

Outputs (under autoresearch/archive/, prefix 022-):
  022-autocorrelation.parquet — per (a, b, lag): autocorrelation ρ
  022-summary.md
  022-simulate.py
"""

from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

ARCHIVE = Path("/Users/andrewkuncevich/vs_code_projects/autoresearch-eval/autoresearch/archive")
OUT_PARQUET = ARCHIVE / "022-autocorrelation.parquet"
OUT_MD = ARCHIVE / "022-summary.md"

# --- config ---
CELLS = [(5, 1), (5, 9), (5, 19), (7, 1), (7, 13), (9, 1), (11, 7), (13, 1)]
SEED_LO = 10_000
SEED_HI = 100_000
N_SEEDS_PER_CELL = 2_000  # ~200 steps each → ≤4×10^5 h values; we cap by N_H_TARGET
N_H_TARGET = 100_000      # target pooled h values per cell
MAX_STEPS = 200           # max shortcut steps per trajectory
H_VALUE_BOUND = 10**18    # bail out if value exceeds this
LAGS = [1, 2, 3, 4, 5]
EMPIRICAL_RATIO = 0.6     # action 019 finding


def v2(n: int) -> int:
    if n == 0:
        return 0
    c = 0
    while n & 1 == 0:
        n >>= 1
        c += 1
    return c


def shortcut_step(a: int, b: int, n: int) -> tuple[int, int]:
    """Compute (n_next, h) where n_next = (a*n + b)/2^h and h = v_2(a*n + b)."""
    val = a * n + b
    h = v2(val)
    return val >> h, h


def simulate_trajectory(
    a: int, b: int, n0: int, max_steps: int = MAX_STEPS,
    h_bound: int = H_VALUE_BOUND,
) -> list[int]:
    """Return list of h_t recorded along the shortcut trajectory.

    Stops on:
      - max_steps reached
      - n exceeds h_bound
      - n revisits a value already seen (cycle entered)
    Note: n is always kept odd (shortcut step divides out all 2s).
    Initial n0 may be even — apply v2 first to make odd.
    """
    # Make n odd to enter the shortcut iteration
    if n0 % 2 == 0:
        n = n0 >> v2(n0)
    else:
        n = n0
    if n == 0:
        return []
    seen = set()
    hs: list[int] = []
    for _ in range(max_steps):
        if n in seen:
            break
        seen.add(n)
        if n > h_bound:
            break
        n_next, h = shortcut_step(a, b, n)
        hs.append(h)
        n = n_next
        if n <= 0:
            break
    return hs


def lagged_pairs(trajectories: list[list[int]], lag: int) -> tuple[np.ndarray, np.ndarray]:
    """Collect (h_s, h_{s+lag}) pairs from each trajectory. Pool across all
    trajectories. Returns (xs, ys)."""
    xs_chunks: list[np.ndarray] = []
    ys_chunks: list[np.ndarray] = []
    for hs in trajectories:
        if len(hs) <= lag:
            continue
        arr = np.asarray(hs, dtype=np.int64)
        xs_chunks.append(arr[:-lag])
        ys_chunks.append(arr[lag:])
    if not xs_chunks:
        return np.array([]), np.array([])
    return np.concatenate(xs_chunks), np.concatenate(ys_chunks)


def pearson(xs: np.ndarray, ys: np.ndarray) -> float:
    if len(xs) < 2:
        return float("nan")
    sx = xs.std()
    sy = ys.std()
    if sx == 0 or sy == 0:
        return float("nan")
    return float(np.corrcoef(xs, ys)[0, 1])


def analyse_cell(a: int, b: int, rng: np.random.Generator) -> dict:
    """Run trajectories for cell (a, b), pool h values, compute autocorrelation."""
    # Sample seeds (odd preferred — but shortcut handles even by stripping 2s)
    seeds = rng.integers(SEED_LO, SEED_HI + 1, size=N_SEEDS_PER_CELL).tolist()

    trajectories: list[list[int]] = []
    pooled_count = 0
    for n0 in seeds:
        hs = simulate_trajectory(a, b, int(n0))
        if hs:
            trajectories.append(hs)
            pooled_count += len(hs)
        if pooled_count >= N_H_TARGET:
            break

    # All-pooled stats
    all_h = np.concatenate([np.asarray(t, dtype=np.int64) for t in trajectories]) if trajectories else np.array([], dtype=np.int64)
    n_traj = len(trajectories)
    n_pooled = len(all_h)
    mean_traj_len = (n_pooled / n_traj) if n_traj > 0 else float("nan")

    Eh = float(all_h.mean()) if n_pooled > 0 else float("nan")
    Vh = float(all_h.var(ddof=0)) if n_pooled > 0 else float("nan")

    rhos: dict[int, float] = {}
    n_pairs: dict[int, int] = {}
    for lag in LAGS:
        xs, ys = lagged_pairs(trajectories, lag)
        rhos[lag] = pearson(xs, ys)
        n_pairs[lag] = len(xs)

    return {
        "a": a,
        "b": b,
        "n_trajectories": n_traj,
        "n_pooled_h": n_pooled,
        "mean_traj_len": mean_traj_len,
        "Eh": Eh,
        "Vh": Vh,
        "rho_1": rhos[1],
        "rho_2": rhos[2],
        "rho_3": rhos[3],
        "rho_4": rhos[4],
        "rho_5": rhos[5],
        "n_pairs_1": n_pairs[1],
        "n_pairs_2": n_pairs[2],
        "n_pairs_3": n_pairs[3],
        "n_pairs_4": n_pairs[4],
        "n_pairs_5": n_pairs[5],
    }


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(seed=20260503)

    cell_results: list[dict] = []
    long_rows: list[dict] = []  # for parquet output: per (a, b, lag)

    for (a, b) in CELLS:
        t_cell = time.time()
        res = analyse_cell(a, b, rng)
        elapsed = time.time() - t_cell
        cell_results.append(res)

        for lag in LAGS:
            long_rows.append({
                "a": a,
                "b": b,
                "lag": lag,
                "rho": res[f"rho_{lag}"],
                "n_pairs": res[f"n_pairs_{lag}"],
                "n_trajectories": res["n_trajectories"],
                "n_pooled_h": res["n_pooled_h"],
                "mean_traj_len": res["mean_traj_len"],
                "Eh": res["Eh"],
                "Vh": res["Vh"],
            })

        print(
            f"  (a={a:2d}, b={b:2d}) {elapsed:5.1f}s  "
            f"n_traj={res['n_trajectories']:5d} n_h={res['n_pooled_h']:7d}  "
            f"mean_len={res['mean_traj_len']:.1f}  "
            f"Eh={res['Eh']:.3f}  Vh={res['Vh']:.3f}  "
            f"ρ1={res['rho_1']:+.3f} ρ2={res['rho_2']:+.3f} "
            f"ρ3={res['rho_3']:+.3f} ρ4={res['rho_4']:+.3f} "
            f"ρ5={res['rho_5']:+.3f}",
            flush=True,
        )

    df_long = pd.DataFrame(long_rows)
    df_long.to_parquet(OUT_PARQUET, index=False)

    df_cells = pd.DataFrame(cell_results)
    write_summary(df_cells)

    print(f"\nTotal runtime: {time.time() - t0:.1f}s")
    print(f"Wrote {OUT_PARQUET}")
    print(f"Wrote {OUT_MD}")


def write_summary(df: pd.DataFrame) -> None:
    md: list[str] = []
    md.append("# Action 022 — h-autocorrelation along trajectories\n")
    md.append("")
    md.append("## Setup\n")
    md.append(
        "Hypothesis: the ~0.6× systematic gap between empirical α and "
        "random-walk-predicted α (action 019) is explained by positive "
        "autocorrelation of `h_t = v_2(a·n_t + b)` along actual shortcut "
        "trajectories, which inflates the variance of the log-value walk per "
        "step:\n\n"
        "    σ²_eff = σ² · (1 + 2·Σ_{t≥1} ρ_t)\n\n"
        "Predicted α correction factor = σ²/σ²_eff = 1/(1 + 2·Σ ρ_t).\n\n"
        "If 2·Σ ρ_t ≈ 0.67, then α_emp/α_theory ≈ 1/1.67 ≈ 0.60.\n"
    )
    md.append(
        f"For each cell in the sample, we ran up to {N_SEEDS_PER_CELL} "
        f"trajectories with n_0 sampled uniformly from [{SEED_LO}, "
        f"{SEED_HI}], iterating the shortcut map "
        "`σ(n) = (a·n + b)/2^{v_2(a·n + b)}` for at most "
        f"{MAX_STEPS} steps (or until the trajectory revisits a value or "
        f"exceeds {H_VALUE_BOUND:.0e}). Recorded `h_t` at each step. "
        f"Target ~{N_H_TARGET} pooled h values per cell. "
        "Lag-t autocorrelation ρ_t was computed by collecting (h_s, h_{s+t}) "
        "pairs only within the same trajectory, pooling across trajectories, "
        "and taking Pearson correlation.\n"
    )

    md.append("## Per-cell autocorrelation\n")
    md.append("| a | b | n_traj | n_h | mean_len | E[h] | Var(h) | ρ_1 | ρ_2 | ρ_3 | ρ_4 | ρ_5 | 2·Σρ_t | corr factor 1/(1+2Σρ) |")
    md.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in df.iterrows():
        sum_rho = sum(r[f"rho_{t}"] for t in LAGS if not math.isnan(r[f"rho_{t}"]))
        two_sum = 2.0 * sum_rho
        corr_factor = 1.0 / (1.0 + two_sum) if (1.0 + two_sum) != 0 else float("nan")
        md.append(
            f"| {int(r['a'])} | {int(r['b'])} | {int(r['n_trajectories'])} | "
            f"{int(r['n_pooled_h'])} | {r['mean_traj_len']:.1f} | "
            f"{r['Eh']:.3f} | {r['Vh']:.3f} | "
            f"{r['rho_1']:+.3f} | {r['rho_2']:+.3f} | {r['rho_3']:+.3f} | "
            f"{r['rho_4']:+.3f} | {r['rho_5']:+.3f} | "
            f"{two_sum:+.3f} | {corr_factor:.3f} |"
        )
    md.append("")

    # --- Pooled stats ---
    rho_means = {t: float(df[f"rho_{t}"].mean()) for t in LAGS}
    rho_medians = {t: float(df[f"rho_{t}"].median()) for t in LAGS}

    sum_mean = sum(rho_means[t] for t in LAGS)
    sum_median = sum(rho_medians[t] for t in LAGS)
    factor_mean = 1.0 / (1.0 + 2.0 * sum_mean)
    factor_median = 1.0 / (1.0 + 2.0 * sum_median)

    md.append("## Pooled statistics across cells\n")
    md.append("| lag | mean ρ_t | median ρ_t |")
    md.append("|-----|----------|------------|")
    for t in LAGS:
        md.append(f"| {t} | {rho_means[t]:+.4f} | {rho_medians[t]:+.4f} |")
    md.append("")

    md.append(f"- mean (Σ_{{t=1..5}} ρ_t) across cells = **{sum_mean:+.4f}**")
    md.append(f"- 2·Σρ_t (mean) = **{2*sum_mean:+.4f}**  →  predicted shrinkage factor σ²/σ²_eff = "
              f"1/(1 + 2Σρ_t) = **{factor_mean:.4f}**")
    md.append(f"- median (Σ_{{t=1..5}} ρ_t) across cells = **{sum_median:+.4f}**")
    md.append(f"- 2·Σρ_t (median) = **{2*sum_median:+.4f}**  →  predicted shrinkage factor = **{factor_median:.4f}**")
    md.append("")

    md.append("## Comparison to empirical α_emp / α_theory ≈ 0.6\n")
    diff_mean = factor_mean - EMPIRICAL_RATIO
    diff_median = factor_median - EMPIRICAL_RATIO
    md.append(f"- Empirical (action 019) ratio: **{EMPIRICAL_RATIO:.3f}**")
    md.append(f"- Predicted (mean): **{factor_mean:.3f}**  (Δ = {diff_mean:+.3f})")
    md.append(f"- Predicted (median): **{factor_median:.3f}**  (Δ = {diff_median:+.3f})")
    md.append("")

    if abs(diff_mean) < 0.10:
        verdict = "**supported**: autocorrelation accounts for the bulk of the systematic shortfall."
    elif abs(diff_mean) < 0.20:
        verdict = "**partially supported**: autocorrelation explains a meaningful fraction of the gap."
    else:
        verdict = ("**weakly supported / falsified**: autocorrelation alone does not reproduce "
                   "the 0.6× factor.")

    md.append("## Conclusion\n")
    md.append(verdict + "\n")
    md.append("")

    OUT_MD.write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
