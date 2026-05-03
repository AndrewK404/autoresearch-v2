"""Action 029 — systematic multi-step C-013 verification.

For each (a, b) with a ∈ {5, 7} and b odd in [1, 21], using
`001-results.parquet` (S=10⁴) and `006-results.parquet` (S=10⁵):

  1. For each ODD seed n0, simulate first 4 shortcut steps and
     record h_1, h_2, h_3, h_4.
  2. Compute cumulative sum H_K = Σ h_i for K = 1, 2, 3, 4.
  3. For each K, group seeds by H_K, compute lift per group.
  4. Pearson(log lift, H_K) per K.
  5. Linear fit log(lift) vs H_K → slope α_K (in log_2 units, i.e.
     divide natural-log slope by ln 2).
  6. Report per (a, b, K).

Outputs:
  029-multistep.parquet
  029-summary.md
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

ARCHIVE = Path("/Users/andrewkuncevich/vs_code_projects/autoresearch-eval/autoresearch/archive")
OUT_PARQUET = ARCHIVE / "029-multistep.parquet"
OUT_MD = ARCHIVE / "029-summary.md"

LN2 = math.log(2.0)


# ---------------------------------------------------------------------------
# Shortcut simulation
# ---------------------------------------------------------------------------

def v2(n: int) -> int:
    """2-adic valuation of n. Returns 0 for n=0 (sentinel)."""
    if n == 0:
        return 0
    c = 0
    while (n & 1) == 0:
        n >>= 1
        c += 1
    return c


def shortcut_h_sequence(a: int, b: int, n0: int, K: int = 4) -> list[int]:
    """Simulate the shortcut chain starting at odd integer n0 and return
    the first K halving-harvest values h_1, ..., h_K.

    Map: odd n -> (a*n + b) / 2^{v2(a*n+b)}.
    If the integer grows pathologically, abort (returns shorter list — but
    in practice we stop at K=4 which is fine even for large b).
    """
    n = n0
    hs: list[int] = []
    for _ in range(K):
        if n <= 0:
            break
        val = a * n + b
        h = v2(val)
        hs.append(h)
        n = val >> h
        # safety cap (very generous; not expected to trigger for K=4)
        if n.bit_length() > 4096:
            break
    return hs


# ---------------------------------------------------------------------------
# Theory
# ---------------------------------------------------------------------------

def predicted_alpha_rw(a: int, b: int, K: int = 16) -> float:
    """α_RW = 2 μ / (σ² · ln 2), with
    μ = log2(a) - E[h], σ² = Var[h], h = v_2(a·r + b) over odd r ∈ [1, 2^K-1].
    """
    odd_r = np.arange(1, 1 << K, 2, dtype=np.int64)
    vals = a * odd_r + b
    lowbit = vals & -vals
    h = np.log2(lowbit.astype(np.float64))
    Eh = float(h.mean())
    Vh = float(h.var(ddof=0))
    mu = math.log2(a) - Eh
    if Vh <= 0:
        return float("nan")
    return 2.0 * mu / (Vh * LN2)


# ---------------------------------------------------------------------------
# Per-cell analysis
# ---------------------------------------------------------------------------

def analyze_cell(df_cell: pd.DataFrame, a: int, b: int, S: int) -> list[dict]:
    """For one (a, b, S) and a precomputed odd-seed dataframe, compute α_K
    for K = 1..4. Returns up to 4 rows.
    """
    odd = df_cell[df_cell["n0"] % 2 == 1].copy()
    if len(odd) == 0:
        return []
    odd["converged"] = (odd["outcome"] == "cycle").astype(int)
    n_seeds = int(len(odd))
    n_conv = int(odd["converged"].sum())
    cell_mean_frac = float(odd["converged"].mean())
    if cell_mean_frac <= 0:
        return []

    # Simulate first 4 h values for each odd seed.
    # Vectorize where possible: hs is a list of 4 ints per seed.
    n0_arr = odd["n0"].to_numpy(dtype=np.int64)
    h_mat = np.zeros((len(n0_arr), 4), dtype=np.int64)
    for i, n0 in enumerate(n0_arr):
        seq = shortcut_h_sequence(a, b, int(n0), K=4)
        for j, hv in enumerate(seq):
            h_mat[i, j] = hv

    converged_arr = odd["converged"].to_numpy(dtype=np.int64)

    rows: list[dict] = []
    for K in (1, 2, 3, 4):
        # H_K = sum of first K h's
        HK = h_mat[:, :K].sum(axis=1)
        # Group by H_K
        df_seeds = pd.DataFrame({"H": HK, "conv": converged_arr})
        grp = df_seeds.groupby("H").agg(n_total=("conv", "size"), n_conv=("conv", "sum")).reset_index()
        grp["frac"] = grp["n_conv"] / grp["n_total"]
        grp["lift"] = grp["frac"] / cell_mean_frac
        # only groups with at least one converged seed (lift > 0) for log
        valid = grp[grp["lift"] > 0].copy()
        n_groups_valid = len(valid)

        if n_groups_valid >= 3 and valid["H"].std() > 0:
            HH = valid["H"].to_numpy(dtype=float)
            ll_nat = np.log(valid["lift"].to_numpy(dtype=float))
            # Pearson r
            mx, my = HH.mean(), ll_nat.mean()
            num = float(np.sum((HH - mx) * (ll_nat - my)))
            dx = float(np.sqrt(np.sum((HH - mx) ** 2)))
            dy = float(np.sqrt(np.sum((ll_nat - my) ** 2)))
            R = num / (dx * dy) if dx > 0 and dy > 0 else float("nan")
            # OLS fit (natural log domain), then convert slope to log2 units
            # so α_K is in "per unit h" but expressed as log2(lift) per h.
            slope_nat, intercept_nat = np.polyfit(HH, ll_nat, 1)
            alpha_K = float(slope_nat / LN2)
            intercept = float(intercept_nat / LN2)
        else:
            R = float("nan")
            alpha_K = float("nan")
            intercept = float("nan")

        rows.append({
            "a": a,
            "b": b,
            "S": S,
            "K": K,
            "n_seeds": n_seeds,
            "n_conv": n_conv,
            "n_groups": int(len(grp)),
            "n_groups_valid": int(n_groups_valid),
            "alpha_K": alpha_K,
            "R": float(R) if R == R else float("nan"),
            "intercept": intercept,
            "mean_conv_frac": cell_mean_frac,
        })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    df1 = pd.read_parquet(ARCHIVE / "001-results.parquet")
    df6 = pd.read_parquet(ARCHIVE / "006-results.parquet")

    bs = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    aas = [5, 7]

    rows: list[dict] = []
    for (S, df_src) in [(10_000, df1), (100_000, df6)]:
        for a in aas:
            for b in bs:
                sub = df_src[(df_src["a"] == a) & (df_src["b"] == b)]
                if len(sub) == 0:
                    continue
                cell_rows = analyze_cell(sub, a, b, S)
                rows.extend(cell_rows)
                # Progress print
                if cell_rows:
                    last = cell_rows[-1]
                    print(
                        f"S={S:>6d} a={a} b={b:2d}: n_seeds={last['n_seeds']:5d} "
                        f"n_conv={last['n_conv']:5d} "
                        f"α_K1={cell_rows[0]['alpha_K']:.3f} "
                        f"α_K4={cell_rows[-1]['alpha_K']:.3f} "
                        f"R_K4={cell_rows[-1]['R']:.3f}"
                    )
                else:
                    print(f"S={S} a={a} b={b}: skipped (no converged seeds)")

    out = pd.DataFrame(rows)
    # Add theoretical α_RW per (a, b)
    th = {(a, b): predicted_alpha_rw(a, b) for a in aas for b in bs}
    out["alpha_theory_rw"] = out.apply(lambda r: th[(int(r["a"]), int(r["b"]))], axis=1)
    out.to_parquet(OUT_PARQUET, index=False)
    print(f"\nwrote {OUT_PARQUET}  shape={out.shape}")

    write_summary(out)


def write_summary(out: pd.DataFrame) -> None:
    md: list[str] = []
    md.append("# Action 029 — Systematic multi-step C-013 verification\n")
    md.append("## Setup\n")
    md.append(
        "For each (a, b) with a ∈ {5, 7} and b odd in [1, 21], using\n"
        "`001-results.parquet` (S=10⁴, odd seeds n0 ∈ [1, 10⁴]) and\n"
        "`006-results.parquet` (S=10⁵, odd seeds n0 ∈ [1, 10⁵]):\n\n"
        "1. Simulate first 4 shortcut steps for each odd seed → h_1..h_4.\n"
        "2. H_K = Σ_{i=1..K} h_i.\n"
        "3. Group seeds by H_K; compute lift(H_K) = frac_conv(H_K) / mean_frac.\n"
        "4. Pearson R of (log lift, H_K), plus OLS slope α_K (log_2 units, "
        "so α_K = (natural-log slope) / ln 2).\n\n"
        "Random-walk prediction: α_RW = 2μ / (σ² · ln 2) with "
        "μ = log_2(a) − E[h], σ² = Var[h], "
        "h = v_2(a·r + b) over odd r ∈ [1, 2^16 − 1]. "
        "For a=5: α_RW ≈ 0.46. For a=7: α_RW ≈ 1.16.\n"
    )

    # Per (a, S, K) median table
    md.append("## Median α_K by (a, S, K)\n")
    md.append("| a | S | K | median α_K | median R | n cells |")
    md.append("|---|---|---|---|---|---|")
    for a in (5, 7):
        for S in (10_000, 100_000):
            for K in (1, 2, 3, 4):
                sub = out[(out["a"] == a) & (out["S"] == S) & (out["K"] == K)]
                v = sub["alpha_K"].dropna()
                rs = sub["R"].dropna()
                if len(v) == 0:
                    continue
                md.append(
                    f"| {a} | {S} | {K} | {v.median():.3f} | "
                    f"{rs.median():.3f} | {len(v)} |"
                )
    md.append("")

    # Theory comparison
    md.append("## Comparison vs random-walk theory α_RW = 2μ / (σ² ln 2)\n")
    md.append("| a | α_RW (theory) | median α_4 (S=10⁴) | median α_4 (S=10⁵) |")
    md.append("|---|---|---|---|")
    for a in (5, 7):
        th = out[out["a"] == a]["alpha_theory_rw"].iloc[0] if len(out[out["a"] == a]) else float("nan")
        v4 = out[(out["a"] == a) & (out["S"] == 10_000) & (out["K"] == 4)]["alpha_K"].dropna()
        v5 = out[(out["a"] == a) & (out["S"] == 100_000) & (out["K"] == 4)]["alpha_K"].dropna()
        md.append(
            f"| {a} | {th:.3f} | "
            f"{v4.median():.3f} (n={len(v4)}) | "
            f"{v5.median():.3f} (n={len(v5)}) |"
        )
    md.append("")

    # Stability of α_K vs K
    md.append("## Stability of α_K across K (per cell)\n")
    md.append(
        "For each (a, b, S), compute std(α_1, α_2, α_3, α_4) and "
        "α_4 − α_1.\n"
    )
    md.append("| a | S | median std(α_K) | median(α_4 − α_1) |")
    md.append("|---|---|---|---|")
    for a in (5, 7):
        for S in (10_000, 100_000):
            sub = out[(out["a"] == a) & (out["S"] == S)]
            piv = sub.pivot_table(index="b", columns="K", values="alpha_K")
            piv = piv.dropna()
            if len(piv) == 0:
                continue
            stds = piv.std(axis=1)
            d = piv[4] - piv[1]
            md.append(
                f"| {a} | {S} | {stds.median():.3f} | {d.median():+.3f} |"
            )
    md.append("")

    # Per-cell α at K=4 (full table)
    md.append("## Per (a, b) α_K at all K (S=10⁵)\n")
    md.append("| a | b | α_1 | α_2 | α_3 | α_4 | R_4 | α_RW |")
    md.append("|---|---|---|---|---|---|---|---|")
    sub = out[out["S"] == 100_000].sort_values(["a", "b", "K"])
    for (a, b), grp in sub.groupby(["a", "b"]):
        d = {int(r["K"]): r for _, r in grp.iterrows()}
        def fmt(x):
            return f"{x:.3f}" if x == x else "—"
        a1 = fmt(d.get(1, {}).get("alpha_K", float("nan")))
        a2 = fmt(d.get(2, {}).get("alpha_K", float("nan")))
        a3 = fmt(d.get(3, {}).get("alpha_K", float("nan")))
        a4 = fmt(d.get(4, {}).get("alpha_K", float("nan")))
        r4 = fmt(d.get(4, {}).get("R", float("nan")))
        ath = fmt(grp["alpha_theory_rw"].iloc[0])
        md.append(f"| {int(a)} | {int(b)} | {a1} | {a2} | {a3} | {a4} | {r4} | {ath} |")
    md.append("")

    md.append("## Per (a, b) α_K at all K (S=10⁴)\n")
    md.append("| a | b | α_1 | α_2 | α_3 | α_4 | R_4 |")
    md.append("|---|---|---|---|---|---|---|")
    sub = out[out["S"] == 10_000].sort_values(["a", "b", "K"])
    for (a, b), grp in sub.groupby(["a", "b"]):
        d = {int(r["K"]): r for _, r in grp.iterrows()}
        def fmt(x):
            return f"{x:.3f}" if x == x else "—"
        a1 = fmt(d.get(1, {}).get("alpha_K", float("nan")))
        a2 = fmt(d.get(2, {}).get("alpha_K", float("nan")))
        a3 = fmt(d.get(3, {}).get("alpha_K", float("nan")))
        a4 = fmt(d.get(4, {}).get("alpha_K", float("nan")))
        r4 = fmt(d.get(4, {}).get("R", float("nan")))
        md.append(f"| {int(a)} | {int(b)} | {a1} | {a2} | {a3} | {a4} | {r4} |")
    md.append("")

    # S=10⁴ vs S=10⁵
    md.append("## S=10⁴ vs S=10⁵ comparison (α_4)\n")
    md.append("| a | median α_4 (S=10⁴) | median α_4 (S=10⁵) | Δ |")
    md.append("|---|---|---|---|")
    for a in (5, 7):
        v4 = out[(out["a"] == a) & (out["S"] == 10_000) & (out["K"] == 4)]["alpha_K"].dropna()
        v5 = out[(out["a"] == a) & (out["S"] == 100_000) & (out["K"] == 4)]["alpha_K"].dropna()
        if len(v4) and len(v5):
            md.append(
                f"| {a} | {v4.median():.3f} | {v5.median():.3f} | "
                f"{v5.median() - v4.median():+.3f} |"
            )
    md.append("")

    md.append("## Verdict\n")
    # auto verdict
    for a in (5, 7):
        th = out[out["a"] == a]["alpha_theory_rw"].iloc[0]
        v5 = out[(out["a"] == a) & (out["S"] == 100_000) & (out["K"] == 4)]["alpha_K"].dropna()
        v4 = out[(out["a"] == a) & (out["S"] == 10_000) & (out["K"] == 4)]["alpha_K"].dropna()
        ratio = v5.median() / th if th != 0 else float("nan")
        md.append(
            f"- **a={a}**: median α_4(S=10⁵) = {v5.median():.3f}, "
            f"α_RW = {th:.3f}, ratio = {ratio:.3f}. "
            f"Median α_4(S=10⁴) = {v4.median():.3f}."
        )
    md.append("")
    md.append(
        "**Per-step α stable across K?** See std(α_K) table above. "
        "Small std relative to the median means α is approximately "
        "constant per shortcut step, validating the additive form "
        "log lift ≈ α · Σ h_i + const.\n"
    )

    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
