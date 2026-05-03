"""atlas.py — loader for the generalized Collatz parameter atlas.

The atlas is the union of:
- per-(a, b, n0) trajectory outcomes  (001-results.parquet)
- per-(a, b, cycle_id) cycle metadata (001-cycles.parquet)
- inheritance tags                     (004-inheritance-tags.parquet)
- shortcut length / period             (005-shortcut-lengths.parquet)
- C-011 (a, b, L, K) coverage          (010-c011-tuples.parquet)

The atlas was produced by the autoresearch run documented in
`autoresearch/`. Sweep horizons: S=10⁴ initially, S=10⁵ at the
falsification pass (006-results.parquet covers the 10× horizon).

Usage:

    from atlas import load_atlas, cycles_for, trajectories_for

    atlas = load_atlas()
    print(atlas['cycles'])           # all 153 cycles with full metadata
    print(cycles_for(3, 13))         # 10 rows — the (3, 13) cycles
    print(trajectories_for(5, 9))    # 10000 rows — per-seed outcomes

Reproduce the atlas from scratch with:

    source .venv/bin/activate
    python autoresearch/archive/001-sweep.py
    python autoresearch/archive/002-verify.py
    python autoresearch/archive/003-verify.py
    python autoresearch/archive/004-tagger.py
    python autoresearch/archive/005-cataloger.py
    python autoresearch/archive/006-sweep.py        # 10× horizon
    python autoresearch/archive/008-l5-enumeration.py
    python autoresearch/archive/010-enumerate.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent
ARCHIVE = REPO_ROOT / "autoresearch" / "archive"


def load_atlas() -> dict[str, pd.DataFrame]:
    """Load the full atlas as a dict of DataFrames.

    Keys: 'cycles', 'cycles_10x', 'trajectories', 'trajectories_10x',
    'inheritance', 'shortcut_lengths', 'c011_tuples',
    'attractivity'.

    Cycles dataframe is the merged view: 001-cycles + 004-inheritance +
    005-shortcut-lengths.
    """
    cycles = pd.read_parquet(ARCHIVE / "001-cycles.parquet")
    inheritance = pd.read_parquet(ARCHIVE / "004-inheritance-tags.parquet")
    shortcut = pd.read_parquet(ARCHIVE / "005-shortcut-lengths.parquet")

    # Merged cycles view — left join to keep all 153 rows
    merged = cycles.merge(
        inheritance[["a", "b", "cycle_id", "tag",
                     "inherited_from_b", "inherited_scale"]],
        on=["a", "b", "cycle_id"], how="left",
    ).merge(
        shortcut[["a", "b", "cycle_id", "shortcut_L", "t_period"]],
        on=["a", "b", "cycle_id"], how="left",
    )

    return {
        "cycles": merged,
        "cycles_10x": pd.read_parquet(ARCHIVE / "006-cycles.parquet"),
        "trajectories": pd.read_parquet(ARCHIVE / "001-results.parquet"),
        "trajectories_10x": pd.read_parquet(ARCHIVE / "006-results.parquet"),
        "inheritance": inheritance,
        "shortcut_lengths": shortcut,
        "c011_tuples": pd.read_parquet(ARCHIVE / "010-c011-tuples.parquet"),
        "attractivity": pd.read_parquet(ARCHIVE / "006-attractivity.parquet"),
    }


def cycles_for(a: int, b: int) -> pd.DataFrame:
    """All cycles for a single (a, b) variant, with full metadata."""
    atlas = load_atlas()
    return atlas["cycles"][
        (atlas["cycles"]["a"] == a) & (atlas["cycles"]["b"] == b)
    ].sort_values("cycle_min").reset_index(drop=True)


def trajectories_for(a: int, b: int) -> pd.DataFrame:
    """Per-seed outcomes for a single (a, b) variant at S = 10⁴."""
    atlas = load_atlas()
    return atlas["trajectories"][
        (atlas["trajectories"]["a"] == a) & (atlas["trajectories"]["b"] == b)
    ].sort_values("n0").reset_index(drop=True)


def cycle_members(a: int, b: int, cycle_id: int) -> list[int]:
    """Members of a specific cycle as a sorted list of integers."""
    atlas = load_atlas()
    row = atlas["cycles"][
        (atlas["cycles"]["a"] == a)
        & (atlas["cycles"]["b"] == b)
        & (atlas["cycles"]["cycle_id"] == cycle_id)
    ]
    if len(row) == 0:
        raise KeyError(f"no cycle (a={a}, b={b}, cycle_id={cycle_id})")
    return sorted(json.loads(row.iloc[0]["cycle_members_json"]))


if __name__ == "__main__":
    atlas = load_atlas()
    print("=== atlas summary ===")
    print(f"cycles:           {len(atlas['cycles'])} rows")
    print(f"trajectories:     {len(atlas['trajectories'])} rows")
    print(f"trajectories_10x: {len(atlas['trajectories_10x'])} rows")
    print(f"c011 tuples:      {len(atlas['c011_tuples'])} rows")
    print(f"attractivity:     {len(atlas['attractivity'])} rows")
    print()
    print("=== per-variant cycle counts ===")
    counts = atlas["cycles"].groupby(["a", "b"]).size().reset_index(name="n_cycles")
    print(counts.to_string(index=False))
