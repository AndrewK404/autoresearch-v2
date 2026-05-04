"""Action 004 — cycle inheritance tagging + C-007 verification.

Reads `autoresearch/archive/001-cycles.parquet`, tags every cycle with its
inheritance status, writes `004-inheritance-tags.parquet` and
`004-summary.md`.

Run:
    source .venv/bin/activate && python autoresearch/archive/004-tagger.py
"""

from __future__ import annotations

import json
from math import gcd
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = PROJECT_ROOT / "autoresearch" / "archive"
SRC_PARQUET = ARCHIVE / "001-cycles.parquet"
OUT_PARQUET = ARCHIVE / "004-inheritance-tags.parquet"
OUT_SUMMARY = ARCHIVE / "004-summary.md"


def step_T(n: int, a: int, b: int) -> int:
    """One raw step of T_{a,b}: halve if even, else a*n+b."""
    if n % 2 == 0:
        return n // 2
    return a * n + b


def cycle_members_from_seed(seed: int, a: int, b: int, max_steps: int = 10_000) -> list[int] | None:
    """Run T_{a,b} from `seed` for up to max_steps; if we revisit the seed,
    return the ordered members visited in one period. Otherwise None.
    """
    seen: dict[int, int] = {}
    n = seed
    path: list[int] = []
    for step in range(max_steps):
        if n in seen:
            start = seen[n]
            return path[start:]
        seen[n] = step
        path.append(n)
        n = step_T(n, a, b)
        if n <= 0:
            return None
    return None


def divisors(b: int) -> list[int]:
    out = []
    for d in range(1, b + 1):
        if b % d == 0:
            out.append(d)
    return out


def d_count(b: int) -> int:
    return len(divisors(b))


def gcd_list(xs: list[int]) -> int:
    g = 0
    for x in xs:
        g = gcd(g, x)
    return g


def member_set(members: list[int]) -> frozenset[int]:
    return frozenset(members)


def main() -> None:
    df = pd.read_parquet(SRC_PARQUET)
    rows = df.to_dict(orient="records")

    # Pre-index cycles by (a, b) -> list of (cycle_id, frozenset(members))
    by_ab: dict[tuple[int, int], list[tuple[int, frozenset[int]]]] = {}
    for r in rows:
        members = json.loads(r["cycle_members_json"])
        by_ab.setdefault((r["a"], r["b"]), []).append((r["cycle_id"], frozenset(members)))

    enriched: list[dict] = []
    for r in rows:
        a = int(r["a"])
        b = int(r["b"])
        cid = int(r["cycle_id"])
        members = json.loads(r["cycle_members_json"])
        g = gcd_list(members)

        tag = "new"
        inherited_from_b = None
        scale = None
        parent_cycle_id = None

        if g > 1 and b % g == 0:
            # candidate inheritance with λ = g
            lam = g
            parent_b = b // lam
            scaled_members = [m // lam for m in members]
            # Verify scaled_members forms a cycle of T_{a, parent_b}
            seed = scaled_members[0]
            sim = cycle_members_from_seed(seed, a, parent_b, max_steps=10_000)
            if sim is not None and frozenset(sim) == frozenset(scaled_members):
                tag = "inherited"
                inherited_from_b = parent_b
                scale = lam
                # find matching parent cycle in by_ab[(a, parent_b)]
                target = frozenset(scaled_members)
                for pcid, pset in by_ab.get((a, parent_b), []):
                    if pset == target:
                        parent_cycle_id = pcid
                        break
            else:
                tag = "gcd_match_but_not_cycle"

        enriched.append({
            **r,
            "gcd_members": int(g),
            "tag": tag,
            "inherited_from_b": inherited_from_b if inherited_from_b is not None else pd.NA,
            "inherited_scale": scale if scale is not None else pd.NA,
            "parent_cycle_id": parent_cycle_id if parent_cycle_id is not None else pd.NA,
        })

    out_df = pd.DataFrame(enriched)
    # Cast types: keep nullable int for the inheritance fields
    for col in ("inherited_from_b", "inherited_scale", "parent_cycle_id"):
        out_df[col] = out_df[col].astype("Int64")
    out_df.to_parquet(OUT_PARQUET, index=False)

    # ----- Summary -----
    # Per-(a, b) tag counts
    grp = (
        out_df.groupby(["a", "b", "tag"]).size().unstack(fill_value=0).reset_index()
    )
    for col in ("inherited", "new", "gcd_match_but_not_cycle"):
        if col not in grp.columns:
            grp[col] = 0
    grp["n_total"] = grp["inherited"] + grp["new"] + grp["gcd_match_but_not_cycle"]
    grp = grp.sort_values(["a", "b"]).reset_index(drop=True)

    # C-007 table for a=1
    a1 = grp[grp["a"] == 1].copy()
    a1["d_b"] = a1["b"].apply(d_count)
    a1["c007_strong"] = a1["inherited"] == a1["d_b"]
    a1["c007_lower"] = a1["n_total"] >= a1["d_b"]

    # New cycle catalog
    new_rows = out_df[out_df["tag"] == "new"].copy()
    new_rows = new_rows.sort_values(["a", "b", "cycle_min"]).reset_index(drop=True)

    # Unverified
    unverified = out_df[out_df["tag"] == "gcd_match_but_not_cycle"]

    lines: list[str] = []
    lines.append("# 004 — Cycle inheritance tagging + C-007 verification\n")
    lines.append(
        "Companion script: `autoresearch/archive/004-tagger.py` (re-run with "
        "`source .venv/bin/activate && python autoresearch/archive/004-tagger.py`).\n"
    )

    lines.append("## Section 1 — Setup\n")
    lines.append(
        "For each cycle in `001-cycles.parquet`, let `M` be its member set "
        "(as stored in `cycle_members_json` — includes both odd shortcut "
        "points and intermediate halvings) and `g = gcd(M)`. If `g > 1` "
        "and `g | b`, the cycle is a candidate λ-scaled image of a cycle of "
        "`T_{a, b/g}`: dividing every member by `g` should yield a cycle of "
        "`T_{a, b/g}`. We verify by direct simulation from the smallest "
        "scaled member; on success the cycle is tagged `inherited` with "
        "`inherited_scale = g`, `inherited_from_b = b/g`, and "
        "`parent_cycle_id` resolved by member-set match against the "
        "`(a, b/g)` cycle list. If verification fails the cycle is tagged "
        "`gcd_match_but_not_cycle` (would indicate a bug or unexpected "
        "structure). Otherwise (g = 1, or g > 1 but g ∤ b) the cycle is "
        "tagged `new`.\n"
    )

    lines.append("## Section 2 — Per-(a, b) tag counts\n")
    lines.append("| a | b | n_total | n_inherited | n_new | n_unverified |")
    lines.append("|---|---|---|---|---|---|")
    for _, r in grp.iterrows():
        lines.append(
            f"| {int(r['a'])} | {int(r['b'])} | {int(r['n_total'])} | "
            f"{int(r['inherited'])} | {int(r['new'])} | "
            f"{int(r['gcd_match_but_not_cycle'])} |"
        )
    lines.append("")

    lines.append("## Section 3 — C-007 verification table (a = 1)\n")
    lines.append(
        "| b | n_total | n_inherited | n_new | d(b) | "
        "C-007 strong (n_inherited == d(b)) | "
        "C-007 lower (n_total >= d(b)) |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for _, r in a1.iterrows():
        lines.append(
            f"| {int(r['b'])} | {int(r['n_total'])} | "
            f"{int(r['inherited'])} | {int(r['new'])} | "
            f"{int(r['d_b'])} | {bool(r['c007_strong'])} | "
            f"{bool(r['c007_lower'])} |"
        )
    lines.append("")

    lines.append("## Section 4 — Surprises\n")

    # 4a. unverified
    if len(unverified) == 0:
        lines.append(
            "- **`gcd_match_but_not_cycle` rows: 0.** No bug / unexpected "
            "structure detected: every cycle whose gcd divides `b` was "
            "verified to be a true λ-scaled image of an `(a, b/λ)` cycle.\n"
        )
    else:
        lines.append(
            f"- **`gcd_match_but_not_cycle` rows: {len(unverified)}** — "
            "would indicate a bug or unexpected structure. Listed below:"
        )
        for _, r in unverified.iterrows():
            lines.append(
                f"  - (a={r['a']}, b={r['b']}) cycle_id={r['cycle_id']} "
                f"members={r['cycle_members_json']} gcd={r['gcd_members']}"
            )
        lines.append("")

    # 4b. C-007 mismatches
    bad = a1[~a1["c007_strong"]]
    if len(bad) == 0:
        lines.append(
            "- **C-007 strong form (n_inherited == d(b)): holds for every "
            "(a=1, b) in scope.**\n"
        )
    else:
        lines.append(
            "- **C-007 strong form fails at:**"
        )
        for _, r in bad.iterrows():
            lines.append(
                f"  - b={int(r['b'])}: n_inherited={int(r['inherited'])}, "
                f"d(b)={int(r['d_b'])}, n_total={int(r['n_total'])}"
            )
        lines.append("")

    bad_lower = a1[~a1["c007_lower"]]
    if len(bad_lower) == 0:
        lines.append(
            "- **C-007 lower bound (n_total >= d(b)): holds for every "
            "(a=1, b) in scope.**\n"
        )
    else:
        lines.append(
            "- **C-007 LOWER BOUND FAILS — falsified — at:**"
        )
        for _, r in bad_lower.iterrows():
            lines.append(
                f"  - b={int(r['b'])}: n_total={int(r['n_total'])}, "
                f"d(b)={int(r['d_b'])}"
            )
        lines.append("")

    # 4c. high n_new flagged cells
    flagged = [(3, 13), (5, 9), (5, 21)]
    lines.append("- **High-`n_new` cells flagged in the brief:**")
    for (aa, bb) in flagged:
        sub = grp[(grp["a"] == aa) & (grp["b"] == bb)]
        if len(sub):
            r = sub.iloc[0]
            lines.append(
                f"  - (a={aa}, b={bb}): n_new={int(r['new'])}, "
                f"n_inherited={int(r['inherited'])}, "
                f"n_total={int(r['n_total'])}"
            )
    lines.append("")

    # Other (a, b) with n_new >= 5 worth highlighting
    high_new = grp[grp["new"] >= 5].sort_values("new", ascending=False)
    if len(high_new):
        lines.append("- **All cells with n_new ≥ 5 (sorted):**")
        for _, r in high_new.iterrows():
            lines.append(
                f"  - (a={int(r['a'])}, b={int(r['b'])}): "
                f"n_new={int(r['new'])}, n_inherited={int(r['inherited'])}"
            )
        lines.append("")

    lines.append("## Section 5 — `new` cycle catalog\n")
    lines.append(
        "Every cycle tagged `new` (i.e. `gcd(members) = 1`, or `gcd > 1` "
        "but `gcd ∤ b` — but the latter cannot occur in our dataset). "
        "Sorted by (a, b, cycle_min).\n"
    )
    lines.append("| a | b | cycle_min | cycle_len | members |")
    lines.append("|---|---|---|---|---|")
    for _, r in new_rows.iterrows():
        lines.append(
            f"| {int(r['a'])} | {int(r['b'])} | {int(r['cycle_min'])} | "
            f"{int(r['cycle_len'])} | {r['cycle_members_json']} |"
        )
    lines.append("")

    OUT_SUMMARY.write_text("\n".join(lines))

    # Print summary stats
    print(f"Wrote {OUT_PARQUET}")
    print(f"Wrote {OUT_SUMMARY}")
    print(f"Total cycles: {len(out_df)}")
    print(f"  inherited: {(out_df['tag'] == 'inherited').sum()}")
    print(f"  new: {(out_df['tag'] == 'new').sum()}")
    print(
        f"  gcd_match_but_not_cycle: "
        f"{(out_df['tag'] == 'gcd_match_but_not_cycle').sum()}"
    )
    print()
    print("C-007 (a=1):")
    print(a1[["b", "n_total", "inherited", "new", "d_b", "c007_strong", "c007_lower"]].to_string(index=False))


if __name__ == "__main__":
    main()
