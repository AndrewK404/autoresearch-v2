"""Action 005 — catalog of cycles at shortcut length L >= 4.

Inputs:
    autoresearch/archive/001-cycles.parquet

Outputs:
    autoresearch/archive/005-shortcut-lengths.parquet
    autoresearch/archive/005-l4plus-catalog.md

Re-run with:
    source .venv/bin/activate
    python autoresearch/archive/005-cataloger.py
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from math import gcd
from pathlib import Path
from functools import reduce

import pandas as pd

ARCHIVE = Path(__file__).resolve().parent
INPUT = ARCHIVE / "001-cycles.parquet"
OUT_PARQUET = ARCHIVE / "005-shortcut-lengths.parquet"
OUT_MD = ARCHIVE / "005-l4plus-catalog.md"


def t_step(n: int, a: int, b: int) -> int:
    if n % 2 == 0:
        return n // 2
    return a * n + b


def t_period(n0: int, a: int, b: int, members: set[int]) -> int:
    """Number of T-steps starting from n0 to return to n0 (must stay in members)."""
    n = t_step(n0, a, b)
    steps = 1
    while n != n0:
        if n not in members:
            raise RuntimeError(
                f"T-orbit from {n0} under (a={a}, b={b}) escaped to {n} "
                f"(not in members {members})"
            )
        n = t_step(n, a, b)
        steps += 1
        if steps > 10_000_000:
            raise RuntimeError("runaway period")
    return steps


def list_gcd(xs: list[int]) -> int:
    return reduce(gcd, xs)


def main() -> None:
    df = pd.read_parquet(INPUT)
    rows = []
    for _, row in df.iterrows():
        a = int(row["a"])
        b = int(row["b"])
        members = json.loads(row["cycle_members_json"])
        members_set = set(members)
        odd_count = sum(1 for m in members if m % 2 == 1)
        period = t_period(members[0], a, b, members_set)
        rows.append(
            {
                "a": a,
                "b": b,
                "cycle_id": int(row["cycle_id"]),
                "cycle_min": int(row["cycle_min"]),
                "cycle_len": int(row["cycle_len"]),
                "shortcut_L": odd_count,
                "t_period": period,
                "max_member": max(members),
                "members_json": json.dumps(members),
            }
        )

    out = pd.DataFrame(rows).sort_values(
        ["a", "b", "shortcut_L", "cycle_min"]
    ).reset_index(drop=True)
    out.to_parquet(OUT_PARQUET, index=False)

    # Sanity
    assert (out["shortcut_L"] >= 1).all()

    # ---- Build markdown ----
    lines: list[str] = []
    lines.append("# 005 — Catalog of cycles with shortcut length L >= 4\n")
    lines.append(
        "Companion script: `autoresearch/archive/005-cataloger.py`. "
        "Source: `autoresearch/archive/001-cycles.parquet` (153 cycles "
        "across 44 (a, b) variants).\n"
    )

    # Section 1 — Setup
    lines.append("## Section 1 — Setup\n")
    n_total = len(out)
    n_le3 = int((out["shortcut_L"] <= 3).sum())
    n_ge4 = int((out["shortcut_L"] >= 4).sum())
    lines.append(
        f"Of the {n_total} cycles in the atlas, **{n_le3}** have shortcut length "
        f"L <= 3 and **{n_ge4}** have L >= 4. The L <= 3 cycles were enumerated "
        "in closed form by action 002 because the shortcut-step equation\n"
    )
    lines.append(
        "    n0 * (2^K - a^L) = b * sum_{i=0}^{L-1} a^{L-1-i} * 2^{k_1+...+k_i}\n"
    )
    lines.append(
        "is small enough at L = 1, 2, 3 to brute-force over the halving "
        "exponents k_i. At L >= 4 the search space explodes (eight or more "
        "free integer parameters once we include k_4, k_5, ...), so the L >= 4 "
        "atlas is recovered only by direct simulation in action 001's sweep. "
        "This file catalogs that residual set.\n"
    )

    # Section 2 — L distribution
    lines.append("## Section 2 — L distribution across the atlas\n")
    lines.append("| shortcut_L | n_cycles | (a, b) variants where this L appears |")
    lines.append("|---:|---:|---|")
    for L in sorted(out["shortcut_L"].unique()):
        sub = out[out["shortcut_L"] == L]
        ab = sorted({(int(r.a), int(r.b)) for r in sub.itertuples()})
        ab_str = ", ".join(f"({a}, {b})" for a, b in ab)
        lines.append(f"| {L} | {len(sub)} | {ab_str} |")
    lines.append("")

    # Section 3 — Per (a, b) L >= 4 inventory
    lines.append("## Section 3 — Per (a, b) L >= 4 inventory\n")
    l4 = out[out["shortcut_L"] >= 4]
    lines.append(
        f"There are **{len(l4)} L >= 4 cycles** spread across "
        f"**{l4.groupby(['a','b']).ngroups} variants**.\n"
    )
    lines.append("| a | b | n_cycles_L4plus | max_L | max_t_period |")
    lines.append("|---:|---:|---:|---:|---:|")
    for (a, b), g in l4.groupby(["a", "b"]):
        lines.append(
            f"| {a} | {b} | {len(g)} | {int(g['shortcut_L'].max())} | "
            f"{int(g['t_period'].max())} |"
        )
    lines.append("")

    # Helpers for residue inspection
    def residue_summary(members: list[int], mods: list[int]) -> str:
        parts = []
        for m in mods:
            classes = sorted({x % m for x in members})
            parts.append(f"mod {m}: {{{', '.join(map(str, classes))}}}")
        return "; ".join(parts)

    def detailed_table(ab_pair: tuple[int, int]) -> list[str]:
        a, b = ab_pair
        sub = out[(out["a"] == a) & (out["b"] == b)].copy()
        sub = sub.sort_values(["t_period", "cycle_min"]).reset_index(drop=True)
        rows_md = []
        rows_md.append(
            "| cycle_min | L | t_period | max_member | gcd | members |"
        )
        rows_md.append("|---:|---:|---:|---:|---:|---|")
        for _, r in sub.iterrows():
            members = json.loads(r["members_json"])
            members_sorted = sorted(members)
            g = list_gcd(members)
            if len(members_sorted) > 8:
                disp = (
                    "["
                    + ", ".join(map(str, members_sorted[:8]))
                    + f", ... ({len(members_sorted)} total)]"
                )
            else:
                disp = "[" + ", ".join(map(str, members_sorted)) + "]"
            rows_md.append(
                f"| {r['cycle_min']} | {r['shortcut_L']} | {r['t_period']} | "
                f"{r['max_member']} | {g} | {disp} |"
            )
        return rows_md

    # Section 4 — (3, 13) detail
    lines.append("## Section 4 — Detailed listing of (a=3, b=13)\n")
    sub_313 = out[(out["a"] == 3) & (out["b"] == 13)]
    n_l4_313 = int((sub_313["shortcut_L"] >= 4).sum())
    lines.append(
        f"All {len(sub_313)} cycles, sorted by t_period. Of these, "
        f"**{n_l4_313} have L >= 4** "
        f"(action 002 catalogued 2 at L <= 3, expected 8 at L >= 4).\n"
    )
    lines.extend(detailed_table((3, 13)))
    lines.append("")

    # Residue analysis for (3, 13) L >= 4
    lines.append("### Residue-class fingerprint of the (3, 13) L >= 4 cycles\n")
    lines.append("| cycle_min | L | residues mod 3 | residues mod 13 |")
    lines.append("|---:|---:|---|---|")
    for _, r in (
        sub_313[sub_313["shortcut_L"] >= 4]
        .sort_values("t_period")
        .iterrows()
    ):
        members = json.loads(r["members_json"])
        r3 = sorted({x % 3 for x in members})
        r13 = sorted({x % 13 for x in members})
        lines.append(
            f"| {r['cycle_min']} | {r['shortcut_L']} | "
            f"{{{', '.join(map(str, r3))}}} | "
            f"{{{', '.join(map(str, r13))}}} |"
        )
    lines.append("")

    # Section 5 — Other detailed listings
    lines.append("## Section 5 — Detailed listings of (5, 21), (3, 5), (5, 9)\n")

    for ab in [(5, 21), (3, 5), (5, 9)]:
        a, b = ab
        sub = out[(out["a"] == a) & (out["b"] == b)]
        n_l4 = int((sub["shortcut_L"] >= 4).sum())
        n_total_ab = len(sub)
        lines.append(
            f"### (a={a}, b={b}) — {n_total_ab} cycles, "
            f"{n_l4} at L >= 4\n"
        )
        lines.extend(detailed_table(ab))
        lines.append("")
        # residue fingerprint for L>=4
        sub_l4 = sub[sub["shortcut_L"] >= 4]
        if len(sub_l4):
            lines.append(
                f"Residue fingerprint of the L >= 4 cycles "
                f"(mod 3, 5, 7, b={b}):\n"
            )
            lines.append("| cycle_min | L | mod 3 | mod 5 | mod 7 | mod b |")
            lines.append("|---:|---:|---|---|---|---|")
            for _, r in sub_l4.sort_values("t_period").iterrows():
                members = json.loads(r["members_json"])
                r3 = sorted({x % 3 for x in members})
                r5 = sorted({x % 5 for x in members})
                r7 = sorted({x % 7 for x in members})
                rb = sorted({x % b for x in members})
                lines.append(
                    f"| {r['cycle_min']} | {r['shortcut_L']} | "
                    f"{{{', '.join(map(str, r3))}}} | "
                    f"{{{', '.join(map(str, r5))}}} | "
                    f"{{{', '.join(map(str, r7))}}} | "
                    f"{{{', '.join(map(str, rb))}}} |"
                )
            lines.append("")
        else:
            lines.append("(No L >= 4 cycles; residue table omitted.)\n")

    # Section 6 — Patterns
    lines.append("## Section 6 — Patterns observed\n")

    # L vs t_period regression-ish
    l4_only = out[out["shortcut_L"] >= 4].copy()
    if len(l4_only):
        l4_only["ratio"] = l4_only["t_period"] / l4_only["shortcut_L"]
        ratio_min = l4_only["ratio"].min()
        ratio_max = l4_only["ratio"].max()
        ratio_mean = l4_only["ratio"].mean()
        lines.append(
            f"**L vs t_period.** Across the {len(l4_only)} L >= 4 cycles, "
            f"t_period / L ranges from {ratio_min:.2f} to {ratio_max:.2f} "
            f"(mean {ratio_mean:.2f}). For T_{{a,b}} with a = 3 the heuristic "
            f"prediction is t_period / L ~ 1 + log_2(3) ~ 2.585; for a = 5 it "
            f"is 1 + log_2(5) ~ 3.32; for a = 7 it is 1 + log_2(7) ~ 3.81. "
            "Per-a breakdown:\n"
        )
        lines.append("| a | n_L4plus | mean t_period/L | predicted 1 + log2(a) |")
        lines.append("|---:|---:|---:|---:|")
        import math
        for a_val, g in l4_only.groupby("a"):
            pred = 1 + math.log2(a_val) if a_val > 1 else 1.0
            lines.append(
                f"| {a_val} | {len(g)} | {g['ratio'].mean():.3f} | {pred:.3f} |"
            )
        lines.append("")

    # gcd inheritance check
    lines.append(
        "**gcd inheritance.** For each L >= 4 cycle we record the gcd of its "
        "members (which by action 004 equals the inherited scale). "
        "Cycles with gcd = 1 are primitive in (a, b); cycles with gcd = d > 1 "
        "are scalings of a (a, b/d) cycle by d.\n"
    )
    gcd_counts = Counter(int(list_gcd(json.loads(r["members_json"])))
                         for _, r in l4_only.iterrows())
    lines.append("| gcd of members | n_cycles |")
    lines.append("|---:|---:|")
    for g_val, c in sorted(gcd_counts.items()):
        lines.append(f"| {g_val} | {c} |")
    lines.append("")

    # max_member vs H = b/(2^k - a) heuristic - too elaborate; report simple
    # observation: gcd is constant within each cycle (sanity check). All
    # cycles are single-gcd-class by definition.
    lines.append(
        "**No L >= 4 cycle spans multiple gcd classes** (each cycle's "
        "members share a common gcd by construction — T_{a,b} preserves "
        "gcd(n, b) when gcd(a, ...) is coprime, so this is expected and "
        "consistent with action 004's inheritance tagging).\n"
    )

    # candidate conjecture text generated from data
    lines.append("### Candidate conjectures from the data\n")

    # (3, 13) L>=4: examine residues mod 13
    sub_313_l4 = out[(out["a"] == 3) & (out["b"] == 13) & (out["shortcut_L"] >= 4)]
    all_mod13 = []
    for _, r in sub_313_l4.iterrows():
        members = json.loads(r["members_json"])
        all_mod13.append(sorted({x % 13 for x in members}))
    lines.append(
        f"- **(3, 13) L >= 4 residues mod 13.** Per-cycle residue sets: "
        f"{all_mod13}. (Look for whether 0 mod 13 ever appears — if not, "
        "the cycles avoid multiples of 13, consistent with gcd(n, 13) = 1 "
        "being T-invariant when 13 | b.)\n"
    )

    # (3, 13) L>=4 residues mod 3
    all_mod3 = []
    for _, r in sub_313_l4.iterrows():
        members = json.loads(r["members_json"])
        all_mod3.append(sorted({x % 3 for x in members}))
    lines.append(
        f"- **(3, 13) L >= 4 residues mod 3.** Per-cycle: {all_mod3}.\n"
    )

    # write file
    OUT_MD.write_text("\n".join(lines))

    # Print summary to stdout
    print(f"Wrote {OUT_PARQUET}")
    print(f"Wrote {OUT_MD}")
    print(f"Total cycles: {n_total}; L<=3: {n_le3}; L>=4: {n_ge4}")
    print("L>=4 (a,b) distribution:")
    for (a, b), g in l4.groupby(["a", "b"]):
        print(
            f"  ({a:>1}, {b:>2}): {len(g):>2} cycles, "
            f"max L = {int(g['shortcut_L'].max())}, "
            f"max t_period = {int(g['t_period'].max())}"
        )
    print("\n(3,13) check:")
    sub = out[(out["a"] == 3) & (out["b"] == 13)]
    print(f"  total {len(sub)}, L<=3 {(sub['shortcut_L']<=3).sum()}, "
          f"L>=4 {(sub['shortcut_L']>=4).sum()}")
    print("(5,21) check:")
    sub = out[(out["a"] == 5) & (out["b"] == 21)]
    print(f"  total {len(sub)}, L<=3 {(sub['shortcut_L']<=3).sum()}, "
          f"L>=4 {(sub['shortcut_L']>=4).sum()}")
    print("(3,5) check:")
    sub = out[(out["a"] == 3) & (out["b"] == 5)]
    print(f"  total {len(sub)}, L<=3 {(sub['shortcut_L']<=3).sum()}, "
          f"L>=4 {(sub['shortcut_L']>=4).sum()}")
    print("(5,9) check:")
    sub = out[(out["a"] == 5) & (out["b"] == 9)]
    print(f"  total {len(sub)}, L<=3 {(sub['shortcut_L']<=3).sum()}, "
          f"L>=4 {(sub['shortcut_L']>=4).sum()}")


if __name__ == "__main__":
    main()
