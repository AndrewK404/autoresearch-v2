"""Action 026 — verify C-015 power law extends to b ∈ [23, 51].

C-015 uses f = fraction of seeds that converge to a cycle (i.e. outcome != 'exceeded-H').
Computes c(a, b) = log10(f(S=10^4) / f(S=10^5)) using `012-results.parquet`.
For S=10^4: n0 ≤ 10^4. For S=10^5: full data.
Compares to tight-scope c(a, b) values (from action 024 summary, which used 001/006).
Compares mean to predicted c(a) = (a-4)/(a-2).
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

ARCHIVE = Path(__file__).resolve().parent

# ----- Tight-scope c(a, b) values from action 024 (b ∈ [1, 21], a ∈ {5, 7}) -----
# Key: (a, b) -> c.  Source: 024-summary.md "Power-law verdict per (a, b)" table,
# col "c=-log10(f5/f4)".
TIGHT_C: dict[tuple[int, int], float] = {
    (5, 1): 0.379,
    (5, 3): 0.377,
    (5, 5): 0.369,
    (5, 7): 0.335,
    (5, 9): 0.329,
    (5, 11): 0.341,
    (5, 13): 0.339,
    (5, 15): 0.368,
    (5, 17): 0.341,
    (5, 19): 0.363,
    (5, 21): 0.353,
    (7, 1): 0.699,
    (7, 3): 0.713,
    (7, 5): 0.643,
    (7, 7): 0.653,
    (7, 9): 0.699,
    (7, 11): 0.593,
    (7, 13): 0.721,
    (7, 15): 0.615,
    (7, 17): 0.687,
    (7, 19): 0.676,
    (7, 21): 0.654,
}


def predicted_c(a: int) -> float:
    return (a - 4) / (a - 2)


def main() -> None:
    df = pd.read_parquet(ARCHIVE / "012-results.parquet")

    rows: list[dict] = []
    for a in [5, 7]:
        bs = sorted(b for b in df["b"].unique() if 23 <= b <= 51)
        for b in bs:
            sub = df[(df["a"] == a) & (df["b"] == b)]
            if len(sub) == 0:
                continue
            sub5 = sub
            sub4 = sub[sub["n0"] <= 10_000]
            # f = cycle-finding fraction (matches 024 convention).
            f5 = float((sub5["outcome"] != "exceeded-H").mean())
            f4 = float((sub4["outcome"] != "exceeded-H").mean())
            n5 = int(len(sub5))
            n4 = int(len(sub4))

            # c = log10(f4 / f5) = -log10(f5/f4); equivalent to action 024 sign.
            if f4 <= 0 or f5 <= 0:
                c_wider = float("nan")
            else:
                c_wider = math.log10(f4 / f5)

            c_pred = predicted_c(a)
            c_tight_mean_a = float(
                np.mean([v for (aa, _), v in TIGHT_C.items() if aa == a])
            )
            tight_for_cell = TIGHT_C.get((a, b))  # None for wider b
            rows.append(
                {
                    "a": a,
                    "b": b,
                    "f4_wider": f4,
                    "f5_wider": f5,
                    "n4": n4,
                    "n5": n5,
                    "c_wider": c_wider,
                    "c_tight_cell": tight_for_cell,  # always None for b in [23,51]
                    "c_tight_mean_a": c_tight_mean_a,
                    "c_predicted": c_pred,
                    "residual_vs_tight_mean": c_wider - c_tight_mean_a,
                    "residual_vs_predicted": c_wider - c_pred,
                }
            )

    out = pd.DataFrame(rows)
    out_path = ARCHIVE / "026-c015-wider.parquet"
    out.to_parquet(out_path, index=False)
    print(f"wrote {out_path}  shape={out.shape}")

    # ----- Summary stats -----
    summary_lines: list[str] = []
    summary_lines.append("# 026 — C-015 power-law check at wider b (b ∈ [23, 51])")
    summary_lines.append("")
    summary_lines.append("## Setup")
    summary_lines.append("")
    summary_lines.append(
        "Source: `012-results.parquet`, n0 ∈ [1, 10^5]. "
        "f = fraction of seeds that converge to a cycle (i.e. outcome ≠ 'exceeded-H'); "
        "matches the convention in action 024. "
        "S=10^4 ⟹ n0 ≤ 10^4 subsample; S=10^5 ⟹ full. "
        "c(a, b) = log10(f(10^4) / f(10^5))."
    )
    summary_lines.append("")
    summary_lines.append("Predicted c(a) = (a-4)/(a-2): c(5)=0.333, c(7)=0.600.")
    summary_lines.append(
        "Tight-scope reference (per-cell c values for b ∈ [1, 21] from action 024):"
    )
    for a in [5, 7]:
        vals = [v for (aa, _), v in TIGHT_C.items() if aa == a]
        summary_lines.append(
            f"- a={a}: tight-scope mean c = {np.mean(vals):.4f}, "
            f"std = {np.std(vals, ddof=1):.4f}, n = {len(vals)}"
        )
    summary_lines.append("")

    summary_lines.append("## Per-cell c at wider b")
    summary_lines.append("")
    summary_lines.append(
        "| a | b | f(10^4) | f(10^5) | c_wider | c_tight_mean(a) | c_pred=(a-4)/(a-2) | "
        "Δ vs tight_mean | Δ vs pred |"
    )
    summary_lines.append("|---|---|---------|---------|---------|------------------|--------------------|------------------|----------|")
    for _, r in out.iterrows():
        summary_lines.append(
            f"| {int(r['a'])} | {int(r['b'])} | {r['f4_wider']:.6f} | "
            f"{r['f5_wider']:.6f} | {r['c_wider']:.4f} | {r['c_tight_mean_a']:.4f} | "
            f"{r['c_predicted']:.4f} | {r['residual_vs_tight_mean']:+.4f} | "
            f"{r['residual_vs_predicted']:+.4f} |"
        )
    summary_lines.append("")

    summary_lines.append("## Aggregate stats per a")
    summary_lines.append("")
    summary_lines.append(
        "| a | n cells | mean c_wider | std c_wider | min c_wider | max c_wider | "
        "tight_mean | predicted | Δ(mean - tight) | Δ(mean - pred) |"
    )
    summary_lines.append(
        "|---|---------|--------------|-------------|-------------|-------------|"
        "------------|-----------|-----------------|----------------|"
    )
    agg = {}
    for a in [5, 7]:
        sub = out[out["a"] == a]
        c_vals = sub["c_wider"].values
        tight_mean = float(np.mean([v for (aa, _), v in TIGHT_C.items() if aa == a]))
        pred = predicted_c(a)
        agg[a] = {
            "mean": float(np.mean(c_vals)),
            "std": float(np.std(c_vals, ddof=1)),
            "min": float(np.min(c_vals)),
            "max": float(np.max(c_vals)),
            "tight": tight_mean,
            "pred": pred,
            "n": int(len(sub)),
        }
        summary_lines.append(
            f"| {a} | {len(sub)} | {np.mean(c_vals):.4f} | {np.std(c_vals, ddof=1):.4f} | "
            f"{np.min(c_vals):.4f} | {np.max(c_vals):.4f} | {tight_mean:.4f} | "
            f"{pred:.4f} | {np.mean(c_vals) - tight_mean:+.4f} | "
            f"{np.mean(c_vals) - pred:+.4f} |"
        )
    summary_lines.append("")

    # Pearson(c_wider, c_tight) — only meaningful if we can pair cells.
    # Wider b cells (23..51) have no tight-scope per-cell c. So we cannot do
    # a per-cell Pearson directly. We report Pearson(c_wider_a, c_tight_a) by
    # aggregating to a-level (only 2 a values — degenerate). Instead, we report:
    # 1) Pearson at the a-level (n=2): trivially perfect or undefined.
    # 2) Sanity Pearson(c_wider, b) within each a (does c trend with b?).
    summary_lines.append("## Pearson correlations")
    summary_lines.append("")
    summary_lines.append(
        "Note: tight-scope b ∈ [1, 21] and wider b ∈ [23, 51] are disjoint, so a "
        "per-cell Pearson(c_wider, c_tight) is not directly defined. We report:"
    )
    summary_lines.append("")
    summary_lines.append("- a-level Pearson(c_wider_mean, c_tight_mean): n=2 (degenerate).")
    for a in [5, 7]:
        sub = out[out["a"] == a]
        if len(sub) >= 3:
            r = float(np.corrcoef(sub["b"].astype(float), sub["c_wider"])[0, 1])
            summary_lines.append(f"- Pearson(b, c_wider) for a={a}: {r:+.4f} (n={len(sub)})")
    summary_lines.append("")

    # Extreme deviations
    summary_lines.append("## Largest |Δ vs tight_mean|")
    summary_lines.append("")
    sorted_out = out.reindex(out["residual_vs_tight_mean"].abs().sort_values(ascending=False).index)
    summary_lines.append("| a | b | c_wider | c_tight_mean(a) | Δ |")
    summary_lines.append("|---|---|---------|------------------|---|")
    for _, r in sorted_out.head(6).iterrows():
        summary_lines.append(
            f"| {int(r['a'])} | {int(r['b'])} | {r['c_wider']:.4f} | "
            f"{r['c_tight_mean_a']:.4f} | {r['residual_vs_tight_mean']:+.4f} |"
        )
    summary_lines.append("")

    summary_lines.append("## Verdict")
    summary_lines.append("")
    for a in [5, 7]:
        s = agg[a]
        summary_lines.append(
            f"- **a={a}**: mean c_wider = {s['mean']:.4f}, std = {s['std']:.4f}, "
            f"range [{s['min']:.4f}, {s['max']:.4f}]. "
            f"Tight-scope mean = {s['tight']:.4f}. Predicted = {s['pred']:.4f}. "
            f"Δ(mean − tight) = {s['mean'] - s['tight']:+.4f}; "
            f"Δ(mean − pred) = {s['mean'] - s['pred']:+.4f}."
        )
    summary_lines.append("")

    # Generalization verdict
    tol_pred = 0.10  # tolerance for matching predicted c
    tol_tight = 0.10
    pred_ok = all(abs(agg[a]["mean"] - agg[a]["pred"]) <= tol_pred for a in [5, 7])
    tight_ok = all(abs(agg[a]["mean"] - agg[a]["tight"]) <= tol_tight for a in [5, 7])
    summary_lines.append(
        f"**Match to predicted c(a) = (a-4)/(a-2) within ±{tol_pred:.2f}: "
        f"{'YES' if pred_ok else 'NO'}**"
    )
    summary_lines.append(
        f"**Match to tight-scope c(a) within ±{tol_tight:.2f}: "
        f"{'YES' if tight_ok else 'NO'}**"
    )

    out_md = ARCHIVE / "026-summary.md"
    out_md.write_text("\n".join(summary_lines) + "\n")
    print(f"wrote {out_md}")

    # Print key stats to stdout
    print()
    for a in [5, 7]:
        s = agg[a]
        print(
            f"a={a}: mean c_wider={s['mean']:.4f} std={s['std']:.4f} "
            f"range=[{s['min']:.4f}, {s['max']:.4f}] "
            f"tight={s['tight']:.4f} pred={s['pred']:.4f}"
        )


if __name__ == "__main__":
    main()
