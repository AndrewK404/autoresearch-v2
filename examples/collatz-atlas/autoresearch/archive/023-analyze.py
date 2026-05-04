"""
Action 023 — high-k basin probe (C-014) + α regression diagnostic.

Goal A: For selected (a, b) cells, compute basin fraction of attractor
containing residue 1 at k = 10..22. Vectorized BFS over functional graph.

Goal B: Re-run α regression at k=6 with weighted-OLS, Theil–Sen, and
high-h-only OLS. Compare to k=4 OLS to see whether the 0.6× factor is a
methodology artifact.

Outputs:
  023-basin-highk.parquet
  023-alpha-diagnostics.parquet
  023-summary.md
"""

from __future__ import annotations

import math
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ARCHIVE = Path("/Users/andrewkuncevich/vs_code_projects/autoresearch-eval/autoresearch/archive")
OUT_BASIN = ARCHIVE / "023-basin-highk.parquet"
OUT_ALPHA = ARCHIVE / "023-alpha-diagnostics.parquet"
OUT_MD = ARCHIVE / "023-summary.md"

LN2 = math.log(2.0)

# ---------------------------------------------------------------------------
# Goal A — basin fraction of attractor containing residue 1
# ---------------------------------------------------------------------------

def basin_fraction_containing_1(a: int, b: int, k: int) -> tuple[float, int, int]:
    """
    Build the residue-chain functional graph on odd residues mod 2^k.
    Find the cycle that contains residue 1, then BFS over reverse edges
    to count the basin size. Vectorized.

    Returns (basin_fraction, cycle_length, basin_size).
    """
    mod = 1 << k
    n_odd = mod // 2
    # index i <-> residue 2*i + 1
    idx = np.arange(n_odd, dtype=np.int64)
    odd = 2 * idx + 1
    val = a * odd + b
    lowbit = val & -val
    h = np.log2(lowbit.astype(np.float64)).astype(np.int64)
    nxt_residue = (val >> h) & (mod - 1)
    nxt_idx = ((nxt_residue - 1) >> 1).astype(np.int64)

    # Floyd's: find a cycle node reachable from index 0 (residue 1)
    slow = 0
    fast = 0
    while True:
        slow = int(nxt_idx[slow])
        fast = int(nxt_idx[int(nxt_idx[fast])])
        if slow == fast:
            break
    # canonical cycle entry
    slow = 0
    while slow != fast:
        slow = int(nxt_idx[slow])
        fast = int(nxt_idx[fast])
    # cycle length
    lam = 1
    cur = int(nxt_idx[slow])
    while cur != slow:
        cur = int(nxt_idx[cur])
        lam += 1
    # collect cycle members
    cycle_members = np.empty(lam, dtype=np.int64)
    cur = slow
    for i in range(lam):
        cycle_members[i] = cur
        cur = int(nxt_idx[cur])

    # CSR reverse adjacency
    in_count = np.bincount(nxt_idx, minlength=n_odd)
    indptr = np.zeros(n_odd + 1, dtype=np.int64)
    indptr[1:] = np.cumsum(in_count)
    children = np.argsort(nxt_idx, kind="stable").astype(np.int64)

    basin = np.zeros(n_odd, dtype=bool)
    basin[cycle_members] = True
    frontier = cycle_members.copy()
    while frontier.size > 0:
        starts = indptr[frontier]
        ends = indptr[frontier + 1]
        sizes = ends - starts
        total = int(sizes.sum())
        if total == 0:
            break
        new_parents = np.empty(total, dtype=np.int64)
        pos = 0
        for s, e in zip(starts.tolist(), ends.tolist()):
            n = e - s
            if n:
                new_parents[pos:pos + n] = children[s:e]
                pos += n
        # filter
        keep = ~basin[new_parents]
        new_parents = new_parents[keep]
        if new_parents.size == 0:
            break
        new_parents = np.unique(new_parents)
        basin[new_parents] = True
        frontier = new_parents

    basin_size = int(basin.sum())
    return basin_size / n_odd, int(lam), basin_size


def goal_a() -> pd.DataFrame:
    cells = [(3, 1), (5, 1), (7, 1), (5, 9), (5, 19), (9, 1)]
    ks = [10, 12, 14, 16, 18, 20, 22]
    rows = []
    for (a, b) in cells:
        for k in ks:
            t0 = time.time()
            bf, lam, bs = basin_fraction_containing_1(a, b, k)
            dt = time.time() - t0
            print(f"a={a:2d} b={b:2d} k={k:2d}: basin={bf:.6f} cycle={lam:5d} "
                  f"basin_size={bs:,} time={dt:.2f}s")
            rows.append({
                "a": a,
                "b": b,
                "k": k,
                "basin_fraction": bf,
                "cycle_length": lam,
                "basin_size": bs,
                "n_odd_total": (1 << k) // 2,
                "compute_seconds": dt,
            })
    df = pd.DataFrame(rows)
    df.to_parquet(OUT_BASIN, index=False)
    return df


# ---------------------------------------------------------------------------
# Goal B — α regression diagnostic
# ---------------------------------------------------------------------------

def theoretical_alpha(a: int, b: int, K: int = 16) -> float:
    odd_r = np.arange(1, 1 << K, 2, dtype=np.int64)
    vals = a * odd_r + b
    lowbit = vals & -vals
    h = np.log2(lowbit.astype(np.float64)).astype(np.int64)
    Eh = float(h.mean())
    Vh = float(h.var(ddof=0))
    mu = math.log2(a) - Eh
    if Vh <= 0:
        return float("nan")
    return 2.0 * mu / (Vh * LN2)


def ols_fit(h: np.ndarray, ll: np.ndarray, w: np.ndarray | None = None) -> tuple[float, float, float]:
    """OLS (or weighted) fit of ll = alpha*h + beta. Returns (alpha, beta, R²)."""
    if h.size < 3 or h.std() == 0:
        return float("nan"), float("nan"), float("nan")
    if w is None:
        alpha, beta = np.polyfit(h, ll, 1)
        pred = alpha * h + beta
        ss_res = float(np.sum((ll - pred) ** 2))
        ss_tot = float(np.sum((ll - ll.mean()) ** 2))
    else:
        # weighted OLS: minimize sum w_i (ll_i - a h_i - b)^2
        W = w.sum()
        h_w = (w * h).sum() / W
        ll_w = (w * ll).sum() / W
        cov = (w * (h - h_w) * (ll - ll_w)).sum() / W
        var = (w * (h - h_w) ** 2).sum() / W
        if var <= 0:
            return float("nan"), float("nan"), float("nan")
        alpha = cov / var
        beta = ll_w - alpha * h_w
        pred = alpha * h + beta
        ss_res = float((w * (ll - pred) ** 2).sum())
        ss_tot = float((w * (ll - ll_w) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(alpha), float(beta), float(r2)


def theil_sen(h: np.ndarray, ll: np.ndarray) -> tuple[float, float]:
    """Theil–Sen slope = median pairwise slope; intercept = median(ll - α h)."""
    n = h.size
    if n < 3:
        return float("nan"), float("nan")
    slopes = []
    for i, j in combinations(range(n), 2):
        if h[j] != h[i]:
            slopes.append((ll[j] - ll[i]) / (h[j] - h[i]))
    if not slopes:
        return float("nan"), float("nan")
    alpha = float(np.median(slopes))
    beta = float(np.median(ll - alpha * h))
    return alpha, beta


def fit_for_cell(sub: pd.DataFrame, k: int) -> dict:
    """Run multiple regressions on one (a, b) at residue mod 2^k."""
    s = sub[(sub["k"] == k) & (sub["lift"] > 0)].copy()
    n = len(s)
    if n < 3:
        return {
            "n_residues": n,
            "alpha_ols": float("nan"),
            "alpha_weighted": float("nan"),
            "alpha_theilsen": float("nan"),
            "alpha_highh_only": float("nan"),
            "r2_ols": float("nan"),
            "n_highh": 0,
        }
    h = s["h_first_step"].to_numpy(dtype=float)
    ll = np.log(s["lift"].to_numpy(dtype=float))
    w = s["n_total"].to_numpy(dtype=float)

    a_ols, _, r2 = ols_fit(h, ll)
    a_w, _, _ = ols_fit(h, ll, w=w)
    a_ts, _ = theil_sen(h, ll)

    # high-h only: residues with h >= 2 AND lift > 1
    mask_high = (s["h_first_step"] >= 2) & (s["lift"] > 1.0)
    if mask_high.sum() >= 2:
        sh = s[mask_high]
        h2 = sh["h_first_step"].to_numpy(dtype=float)
        l2 = np.log(sh["lift"].to_numpy(dtype=float))
        if h2.std() > 0:
            a_high, _, _ = ols_fit(h2, l2)
        else:
            a_high = float("nan")
    else:
        a_high = float("nan")

    return {
        "n_residues": n,
        "alpha_ols": a_ols,
        "alpha_weighted": a_w,
        "alpha_theilsen": a_ts,
        "alpha_highh_only": a_high,
        "r2_ols": r2,
        "n_highh": int(mask_high.sum()),
    }


def goal_b() -> pd.DataFrame:
    df = pd.read_parquet(ARCHIVE / "017-residue-lift.parquet")
    cells = sorted({(int(a), int(b)) for a, b in zip(df["a"], df["b"])})
    rows = []
    for (a, b) in cells:
        sub = df[(df["a"] == a) & (df["b"] == b)]
        alpha_th = theoretical_alpha(a, b)
        rec_k4 = fit_for_cell(sub, k=4)
        rec_k6 = fit_for_cell(sub, k=6)
        rows.append({
            "a": a,
            "b": b,
            "alpha_theory": alpha_th,
            "alpha_k4_ols": rec_k4["alpha_ols"],
            "alpha_k4_weighted": rec_k4["alpha_weighted"],
            "alpha_k4_theilsen": rec_k4["alpha_theilsen"],
            "alpha_k4_highh": rec_k4["alpha_highh_only"],
            "n_residues_k4": rec_k4["n_residues"],
            "n_highh_k4": rec_k4["n_highh"],
            "r2_k4": rec_k4["r2_ols"],
            "alpha_k6_ols": rec_k6["alpha_ols"],
            "alpha_k6_weighted": rec_k6["alpha_weighted"],
            "alpha_k6_theilsen": rec_k6["alpha_theilsen"],
            "alpha_k6_highh": rec_k6["alpha_highh_only"],
            "n_residues_k6": rec_k6["n_residues"],
            "n_highh_k6": rec_k6["n_highh"],
            "r2_k6": rec_k6["r2_ols"],
        })
    out = pd.DataFrame(rows)
    # ratios
    for col in ["alpha_k4_ols", "alpha_k4_weighted", "alpha_k4_theilsen", "alpha_k4_highh",
                "alpha_k6_ols", "alpha_k6_weighted", "alpha_k6_theilsen", "alpha_k6_highh"]:
        out[col + "_ratio"] = out[col] / out["alpha_theory"]
    out.to_parquet(OUT_ALPHA, index=False)
    return out


# ---------------------------------------------------------------------------
# Markdown summary
# ---------------------------------------------------------------------------

def write_summary(basin_df: pd.DataFrame, alpha_df: pd.DataFrame) -> None:
    md: list[str] = []
    md.append("# Action 023 — High-k basin probe + α regression diagnostic\n")

    md.append("## Goal A — Basin trends for attractor containing residue 1\n")
    md.append("For each (a, b) cell, basin fraction at k = 10..22. The basin "
              "is the set of odd residues mod 2^k whose iterated residue-chain "
              "trajectory reaches the cycle that contains residue 1.\n")

    md.append("### Per-cell basin fraction by k\n")
    pivot = basin_df.pivot_table(index=["a", "b"], columns="k",
                                  values="basin_fraction", aggfunc="first")
    md.append("| (a, b) | " + " | ".join(f"k={k}" for k in pivot.columns) + " |")
    md.append("|---|" + "|".join(["---"] * len(pivot.columns)) + "|")
    for (a, b), row in pivot.iterrows():
        cells_str = " | ".join(f"{v:.6f}" if not pd.isna(v) else "—" for v in row)
        md.append(f"| ({int(a)}, {int(b)}) | {cells_str} |")
    md.append("")

    md.append("### Cycle length by k\n")
    cyc = basin_df.pivot_table(index=["a", "b"], columns="k",
                                values="cycle_length", aggfunc="first")
    md.append("| (a, b) | " + " | ".join(f"k={k}" for k in cyc.columns) + " |")
    md.append("|---|" + "|".join(["---"] * len(cyc.columns)) + "|")
    for (a, b), row in cyc.iterrows():
        cells_str = " | ".join(f"{int(v)}" if not pd.isna(v) else "—" for v in row)
        md.append(f"| ({int(a)}, {int(b)}) | {cells_str} |")
    md.append("")

    md.append("### Trend interpretation\n")
    # Examine each cell
    for (a, b), row in pivot.iterrows():
        vals = [row[k] for k in pivot.columns if not pd.isna(row[k])]
        first = vals[0]; last = vals[-1]
        trend = "→ 1" if last > 0.95 else ("→ 0" if last < 0.05 else "non-monotone / oscillating")
        md.append(f"- ({int(a)}, {int(b)}): {first:.4f} (k=10) → {last:.4f} (k=22). Trend: **{trend}**.")
    md.append("")

    md.append("## Goal B — α regression methodology comparison\n")
    md.append("All cells from `017-residue-lift.parquet`. We compare:\n"
              "- α_k4_ols: OLS at k=4 (action 019 method).\n"
              "- α_k6_ols: OLS at k=6 (~32 odd residues per cell).\n"
              "- α_k6_weighted: weighted OLS at k=6, weights = n_total per residue.\n"
              "- α_k6_theilsen: Theil–Sen at k=6 (robust median-of-pairwise-slopes).\n"
              "- α_k4_highh: OLS at k=4 restricted to residues with h ≥ 2 and lift > 1.\n"
              "Compared to α_theory from action 019.\n")

    headline = alpha_df.dropna(subset=["alpha_theory"])
    headline = headline[headline["alpha_theory"] > 0]

    def med(col):
        v = headline[col + "_ratio"].dropna()
        return float(v.median()) if len(v) > 0 else float("nan"), len(v)

    md.append("### Median α/α_theory by method\n")
    md.append("| method | median ratio | n cells |")
    md.append("|---|---|---|")
    for col in ["alpha_k4_ols", "alpha_k4_highh",
                "alpha_k6_ols", "alpha_k6_weighted", "alpha_k6_theilsen", "alpha_k6_highh"]:
        m, n = med(col)
        md.append(f"| {col} | {m:.3f} | {n} |")
    md.append("")

    md.append("### Per-cell table (subset, a ≥ 5)\n")
    md.append("| a | b | α_th | k4_OLS | k4_highh | k6_OLS | k6_W | k6_TS | k6_highh |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for _, r in alpha_df.sort_values(["a", "b"]).iterrows():
        def fmt(x): return f"{x:.3f}" if not pd.isna(x) else "—"
        md.append(
            f"| {int(r['a'])} | {int(r['b'])} | {fmt(r['alpha_theory'])} | "
            f"{fmt(r['alpha_k4_ols'])} | {fmt(r['alpha_k4_highh'])} | "
            f"{fmt(r['alpha_k6_ols'])} | {fmt(r['alpha_k6_weighted'])} | "
            f"{fmt(r['alpha_k6_theilsen'])} | {fmt(r['alpha_k6_highh'])} |"
        )
    md.append("")

    md.append("## Closure or open?\n")
    m_k4, _ = med("alpha_k4_ols")
    m_k6, _ = med("alpha_k6_ols")
    m_k6w, _ = med("alpha_k6_weighted")
    m_k6ts, _ = med("alpha_k6_theilsen")
    m_k4h, _ = med("alpha_k4_highh")
    m_k6h, _ = med("alpha_k6_highh")

    md.append(f"- α_k4_OLS / α_theory ≈ **{m_k4:.3f}** (action 019 baseline; ≈ 0.6×).")
    md.append(f"- α_k6_OLS / α_theory ≈ **{m_k6:.3f}**.")
    md.append(f"- α_k6_weighted / α_theory ≈ **{m_k6w:.3f}**.")
    md.append(f"- α_k6_theilsen / α_theory ≈ **{m_k6ts:.3f}**.")
    md.append(f"- α_k4_high-h-only / α_theory ≈ **{m_k4h:.3f}**.")
    md.append(f"- α_k6_high-h-only / α_theory ≈ **{m_k6h:.3f}**.")
    md.append("")

    best = max([m_k6, m_k6w, m_k6ts, m_k4h, m_k6h])
    if best > 0.85:
        verdict = ("The 0.6× factor **largely closes** under best methodology. "
                   "Action 019's gap is mostly a regression artifact from k=4 small bucket count "
                   "and bounded/saturating lift values.")
    elif best > 0.7:
        verdict = ("The 0.6× factor **partially closes** — better methodology raises the ratio, "
                   "but a residual structural bias remains.")
    else:
        verdict = ("The 0.6× factor **does not close** under any method tried. "
                   "The systematic bias is structural, not a regression artifact.")
    md.append(f"**Verdict:** {verdict}")
    md.append("")

    OUT_MD.write_text("\n".join(md) + "\n")


def main() -> None:
    print("=== Goal A — basin probe ===")
    basin_df = goal_a()
    print()
    print("=== Goal B — α diagnostics ===")
    alpha_df = goal_b()
    print()
    write_summary(basin_df, alpha_df)
    print(f"Wrote {OUT_BASIN}")
    print(f"Wrote {OUT_ALPHA}")
    print(f"Wrote {OUT_MD}")
    # print quick summary
    print()
    print("Median ratio summary:")
    for col in ["alpha_k4_ols", "alpha_k4_highh",
                "alpha_k6_ols", "alpha_k6_weighted", "alpha_k6_theilsen", "alpha_k6_highh"]:
        v = alpha_df[col + "_ratio"].dropna()
        print(f"  {col}: median = {v.median():.4f} (n={len(v)})")


if __name__ == "__main__":
    main()
