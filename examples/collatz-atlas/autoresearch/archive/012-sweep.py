"""012 — Wider-b sweep + atlas extension.

Family: T_{a,b}(n) = n/2 if n even else a*n + b.
Scope: a in {1,3,5,7}, b in {23,25,27,29,31,33,35,37,39,41,43,45,47,49,51}.
Horizons (same as action 006): S = 10^5, H = 10^13, T = 10^5.

Goal: test whether C-001, C-003, C-007', C-009, C-011 generalize to wider b.

Outputs (under autoresearch/archive/, prefix 012-):
  012-results.parquet, 012-cycles.parquet, 012-summary.md.
"""

from __future__ import annotations

import json
import math
import time
from functools import reduce
from itertools import combinations
from math import gcd
from pathlib import Path

import pandas as pd

A_VALUES = [1, 3, 5, 7]
B_VALUES = [23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
SEED_MAX = 100_000
H = 10**13
T = 100_000

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "archive"


def step(n: int, a: int, b: int) -> int:
    if n % 2 == 0:
        return n // 2
    return a * n + b


def run_variant(a: int, b: int):
    """Sweep all seeds in [1, SEED_MAX] under T_{a,b} with suffix memo.

    Cache: value -> (outcome, cycle_id, suffix_max, suffix_steps). Caches only
    'cycle' / 'exceeded-H' (suffix-deterministic). 'exceeded-T' is per-seed
    (depends on absolute step count) and is not cached.
    """
    cache = {}  # value -> (outcome, cycle_id, suffix_max, suffix_steps)
    cycles_by_members: dict[tuple, int] = {}
    cycles_list: list[dict] = []
    results: list[dict] = []

    for n0 in range(1, SEED_MAX + 1):
        n = n0
        prefix_path: list[int] = []
        prefix_index: dict[int, int] = {}
        prefix_max = n0
        prefix_steps = 0

        terminal = None
        cycle_id = -1
        cycle_members = None
        cycle_len = -1
        suf_outcome = None
        suf_cid = -1
        suf_max = 0
        suf_steps = 0

        while True:
            if n in cache:
                c_outcome, c_cid, c_smax, c_ssteps = cache[n]
                terminal = c_outcome
                cycle_id = c_cid
                suf_outcome = c_outcome
                suf_cid = c_cid
                suf_max = c_smax
                suf_steps = c_ssteps
                if c_outcome == "cycle":
                    info = cycles_list[c_cid]
                    cycle_members = info["members_sorted"]
                    cycle_len = info["cycle_len"]
                break

            if n > H:
                terminal = "exceeded-H"
                cache[n] = ("exceeded-H", -1, n, 0)
                suf_outcome = "exceeded-H"
                suf_cid = -1
                suf_max = n
                suf_steps = 0
                break

            if prefix_steps >= T:
                terminal = "exceeded-T"
                suf_outcome = "exceeded-T"
                suf_cid = -1
                suf_max = n
                suf_steps = 0
                break

            if n in prefix_index:
                first_idx = prefix_index[n]
                members = prefix_path[first_idx:]
                members_sorted = tuple(sorted(set(members)))
                cycle_len = len(members_sorted)
                if members_sorted in cycles_by_members:
                    cid = cycles_by_members[members_sorted]
                else:
                    cid = len(cycles_list)
                    cycles_by_members[members_sorted] = cid
                    cycles_list.append({
                        "cycle_id": cid,
                        "cycle_len": cycle_len,
                        "cycle_min": min(members_sorted),
                        "members_sorted": members_sorted,
                        "members_t_order": list(members),  # T-order for t_period
                        "n_seeds_reaching": 0,
                    })
                terminal = "cycle"
                cycle_id = cid
                cycle_members = members_sorted
                cyc_max = max(members_sorted)
                for v in members_sorted:
                    if v not in cache:
                        cache[v] = ("cycle", cid, cyc_max, 0)
                suf_outcome = "cycle"
                suf_cid = cid
                suf_max = cyc_max
                suf_steps = 0
                break

            # Extend
            prefix_index[n] = len(prefix_path)
            prefix_path.append(n)
            if n > prefix_max:
                prefix_max = n
            n = n // 2 if n % 2 == 0 else a * n + b
            prefix_steps += 1

        if terminal == "exceeded-T":
            total_max = prefix_max
            if n > total_max:
                total_max = n
            total_steps = prefix_steps
        else:
            total_max = max(prefix_max, suf_max)
            total_steps = prefix_steps + suf_steps

        if terminal in ("cycle", "exceeded-H"):
            running_max = suf_max
            running_steps = suf_steps
            for i in range(len(prefix_path) - 1, -1, -1):
                v = prefix_path[i]
                running_steps += 1
                if v > running_max:
                    running_max = v
                if v not in cache:
                    cache[v] = (terminal, suf_cid, running_max, running_steps)

        if terminal == "cycle":
            cycles_list[cycle_id]["n_seeds_reaching"] += 1

        results.append({
            "a": a,
            "b": b,
            "n0": n0,
            "outcome": terminal,
            "cycle_id": cycle_id if terminal == "cycle" else -1,
            "cycle_min": min(cycle_members) if cycle_members is not None else -1,
            "cycle_len": cycle_len if terminal == "cycle" else -1,
            "max_value": total_max,
            "steps_to_outcome": total_steps,
        })

    return results, cycles_list


def list_gcd(xs) -> int:
    return reduce(gcd, xs)


def divisors(b: int) -> list[int]:
    return [d for d in range(1, b + 1) if b % d == 0]


def d_count(b: int) -> int:
    return len(divisors(b))


def cycle_members_from_seed(seed: int, a: int, b: int, max_steps: int = 100_000):
    seen: dict[int, int] = {}
    n = seed
    path: list[int] = []
    for s in range(max_steps):
        if n in seen:
            start = seen[n]
            return path[start:]
        seen[n] = s
        path.append(n)
        n = step(n, a, b)
        if n <= 0:
            return None
    return None


def tag_inheritance(a: int, b: int, members: list[int],
                    parent_cycles: dict[int, list[frozenset[int]]]) -> tuple[str, int | None, int | None]:
    """Return (tag, inherited_from_b, inherited_scale).

    tag: 'inherited' if gcd(members) > 1 and divides b and verified to be
    the lambda-scaled image of a cycle of T_{a, b/lambda}; else 'new'.

    parent_cycles: dict parent_b -> list of frozenset(members) of cycles in
    that variant (for membership lookup if available); otherwise we simulate.
    """
    g = list_gcd(members)
    if g <= 1 or b % g != 0:
        return "new", None, None
    lam = g
    parent_b = b // lam
    scaled = [m // lam for m in members]
    sim = cycle_members_from_seed(scaled[0], a, parent_b, max_steps=100_000)
    if sim is None:
        return "new", None, None
    if frozenset(sim) == frozenset(scaled):
        return "inherited", parent_b, lam
    return "new", None, None


# ----------------- C-009 t_period helper -----------------

def t_period_of_cycle(members_t_order: list[int]) -> int:
    """t_period = number of T-steps to return to start = len of T-orbit."""
    return len(members_t_order)


def shortcut_L(members: list[int]) -> int:
    return sum(1 for m in members if m % 2 == 1)


# ----------------- C-011 helper -----------------

def c011_check(a: int, b: int, members: list[int]) -> tuple[bool, int, int]:
    """For a primitive cycle, compute K = t_period - L and check b | (2^K - a^L).

    Returns (matches, K, L).
    """
    L = shortcut_L(members)
    K = len(members) - L
    if L == 0:
        return False, K, L
    D = 2 ** K - a ** L
    if D == 0:
        return False, K, L
    matches = (D % b == 0)
    return matches, K, L


def main() -> None:
    t_start = time.time()

    # Sanity: the sanity case from action 006 used (3, 1) which isn't in our
    # new b range. Use (3, 23) — should still cycle for all seeds.
    print(f"Starting wider-b sweep: a={A_VALUES}, b={B_VALUES}, "
          f"S={SEED_MAX}, H={H}, T={T}", flush=True)

    all_results: list[dict] = []
    all_cycles: list[dict] = []
    per_variant_runtime: dict[tuple[int, int], float] = {}
    cycles_by_ab: dict[tuple[int, int], list[dict]] = {}

    for a in A_VALUES:
        for b in B_VALUES:
            t0 = time.time()
            results, cycles_info = run_variant(a, b)
            t1 = time.time()
            per_variant_runtime[(a, b)] = t1 - t0

            # Renumber cycle_id starting from 0 per (a, b) (independent
            # numbering per task spec).
            # cycles_info already uses local IDs starting at 0.
            cycles_by_ab[(a, b)] = cycles_info

            for ci in cycles_info:
                all_cycles.append({
                    "a": a,
                    "b": b,
                    "cycle_id": ci["cycle_id"],
                    "cycle_len": ci["cycle_len"],
                    "cycle_min": ci["cycle_min"],
                    "cycle_members_json": json.dumps(list(ci["members_sorted"])),
                    "n_seeds_reaching": ci["n_seeds_reaching"],
                })

            all_results.extend(results)

            n_cycle = sum(1 for r in results if r["outcome"] == "cycle")
            n_h = sum(1 for r in results if r["outcome"] == "exceeded-H")
            n_t = sum(1 for r in results if r["outcome"] == "exceeded-T")
            print(f"  (a={a}, b={b}) {t1-t0:6.2f}s | cycles={len(cycles_info)} "
                  f"| reached={n_cycle} H={n_h} T={n_t}", flush=True)

    t_sweep_end = time.time()

    df_results = pd.DataFrame(all_results)
    df_cycles = pd.DataFrame(all_cycles)

    for col in ["a", "b", "n0", "cycle_id", "cycle_min", "cycle_len",
                "max_value", "steps_to_outcome"]:
        df_results[col] = df_results[col].astype("int64")
    for col in ["a", "b", "cycle_id", "cycle_len", "cycle_min", "n_seeds_reaching"]:
        df_cycles[col] = df_cycles[col].astype("int64")

    out_results = ARCHIVE / "012-results.parquet"
    out_cycles = ARCHIVE / "012-cycles.parquet"
    df_results.to_parquet(out_results, index=False)
    df_cycles.to_parquet(out_cycles, index=False)

    t_parquet_end = time.time()

    summary_path = ARCHIVE / "012-summary.md"
    write_summary(
        summary_path,
        df_results,
        df_cycles,
        cycles_by_ab,
        per_variant_runtime,
        t_sweep_total=t_sweep_end - t_start,
        t_parquet=t_parquet_end - t_sweep_end,
        t_total=t_parquet_end - t_start,
    )

    print(f"\nTotal runtime: {time.time()-t_start:.1f}s")
    print(f"Wrote: {out_results}")
    print(f"Wrote: {out_cycles}")
    print(f"Wrote: {summary_path}")


def write_summary(path: Path, df_results: pd.DataFrame, df_cycles: pd.DataFrame,
                  cycles_by_ab: dict[tuple[int, int], list[dict]],
                  per_variant_runtime: dict[tuple[int, int], float],
                  t_sweep_total: float, t_parquet: float, t_total: float):
    L: list[str] = []
    L.append("# 012 — Wider-b sweep + atlas extension\n")
    L.append("\n## Setup\n\n")
    L.append(
        "Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. "
        f"Scope: `a ∈ {{1,3,5,7}}`, `b ∈ {B_VALUES}` "
        f"({len(A_VALUES) * len(B_VALUES)} new variants). "
        f"Per-variant: every seed `n0 ∈ [1, {SEED_MAX}]`. "
        f"Horizons: value bound `H = {H}`, step bound `T = {T}`. "
        "Same horizons as action 006. Cycle IDs start at 0 per (a, b) "
        "(independent of action 001 numbering).\n"
    )

    # ---------------- Per-variant table ----------------
    L.append("\n## Per-variant table\n\n")
    L.append("| a | b | total_seeds | reached_cycle | exceeded_H | exceeded_T "
             "| n_distinct_cycles | smallest_cycle_min |\n")
    L.append("|---|---|-------------|---------------|------------|------------"
             "|-------------------|--------------------|\n")
    for a in A_VALUES:
        for b in B_VALUES:
            sub = df_results[(df_results.a == a) & (df_results.b == b)]
            cyc_sub = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
            total = len(sub)
            n_cycle = int((sub.outcome == "cycle").sum())
            n_h = int((sub.outcome == "exceeded-H").sum())
            n_t = int((sub.outcome == "exceeded-T").sum())
            n_distinct = len(cyc_sub)
            smallest_cm = int(cyc_sub.cycle_min.min()) if n_distinct > 0 else -1
            L.append(f"| {a} | {b} | {total} | {n_cycle} | {n_h} | {n_t} "
                     f"| {n_distinct} | {smallest_cm} |\n")

    # ---------------- C-001 verdict ----------------
    L.append("\n## C-001 verdict (a ∈ {1, 3} at wider b)\n\n")
    sub = df_results[df_results.a.isin([1, 3])]
    n_total = len(sub)
    n_cycle = int((sub.outcome == "cycle").sum())
    n_h = int((sub.outcome == "exceeded-H").sum())
    n_t = int((sub.outcome == "exceeded-T").sum())
    if n_cycle == n_total:
        L.append(
            f"**CONFIRMED at wider b.** All {n_total} trajectories "
            f"(a ∈ {{1, 3}}, b ∈ {B_VALUES}) reached a cycle within "
            f"T = {T} steps without exceeding H = {H}.\n"
        )
    else:
        L.append(
            f"**FALSIFIED at wider b.** Out of {n_total}: cycle={n_cycle}, "
            f"exceeded-H={n_h}, exceeded-T={n_t}.\n\nFirst falsifiers:\n\n"
        )
        bad = sub[sub.outcome != "cycle"].head(20)
        for _, r in bad.iterrows():
            L.append(f"- (a={r.a}, b={r.b}, n0={r.n0}): outcome={r.outcome}, "
                     f"max_value={r.max_value}, steps={r.steps_to_outcome}\n")

    # ---------------- C-003 verdict ----------------
    L.append("\n## C-003 verdict (a = 7 at wider b — single L1 cycle?)\n\n")
    c003_extra = []  # cycles other than {b, 2b, 4b, 8b}
    c003_l1_only_bs = []
    for b in B_VALUES:
        cyc = df_cycles[(df_cycles.a == 7) & (df_cycles.b == b)]
        expected = sorted([b, 2 * b, 4 * b, 8 * b])
        is_only_l1 = True
        for _, r in cyc.iterrows():
            members = sorted(json.loads(r.cycle_members_json))
            if members != expected:
                is_only_l1 = False
                c003_extra.append((b, int(r.cycle_id), members,
                                   int(r.cycle_len), int(r.n_seeds_reaching)))
        if is_only_l1 and len(cyc) >= 1:
            c003_l1_only_bs.append(b)

    L.append(f"- Variants where the only cycle reached is the L1 cycle "
             f"`{{b, 2b, 4b, 8b}}`: **{len(c003_l1_only_bs)}** out of "
             f"{len(B_VALUES)} ({c003_l1_only_bs}).\n")
    if not c003_extra:
        L.append("- **No additional cycles** outside the L1 cycle were found "
                 "for any (a=7, b) variant in the new range.\n")
    else:
        L.append(f"- **{len(c003_extra)} additional cycle(s)** beyond the L1 "
                 "cycle:\n")
        for b, cid, members, cyc_len, nsr in c003_extra:
            show = ", ".join(str(m) for m in members[:8])
            if len(members) > 8:
                show += f", ... ({len(members)} total)"
            L.append(f"    - (a=7, b={b}) cycle_id={cid} | len={cyc_len} | "
                     f"members={{{show}}} | seeds_reaching={nsr}\n")

    # ---------------- C-007' verdict (a=1) ----------------
    L.append("\n## C-007' verdict (a = 1 at wider b)\n\n")
    L.append("Tag each cycle as `inherited` if gcd(members) > 1 and divides b "
             "AND the gcd-scaled image is a verified cycle of T_{a, b/gcd}; "
             "else `new`.\n\n")
    L.append("| b | d(b) | n_total | n_inherited | n_new | "
             "lower_holds (n_total ≥ d(b)−1) | strong_inherited (n_inh ≥ d(b)−1) |\n")
    L.append("|---|------|---------|-------------|-------|"
             "------------------------------|---------------------------------|\n")
    a1_summary_rows = []
    for b in B_VALUES:
        cyc_list = cycles_by_ab.get((1, b), [])
        n_total_cyc = len(cyc_list)
        n_inh = 0
        n_new = 0
        for ci in cyc_list:
            members = list(ci["members_sorted"])
            tag, _, _ = tag_inheritance(1, b, members, {})
            if tag == "inherited":
                n_inh += 1
            else:
                n_new += 1
        d_b = d_count(b)
        # C-007' lower bound: n_inherited >= d(b) - 1 (proper divisors > 1
        # plus trivial cycle from b=1; in the wider-b literature the
        # n_inherited count tracks d(b) - 1 if we count all proper-divisor
        # parent cycles excluding self).
        # Following action 004's strong form: n_inherited == d(b) for a=1 in
        # tight scope. C-007' is stated as a lower bound. We report both
        # matches.
        lower_holds = n_total_cyc >= (d_b - 1)
        strong_inh = n_inh >= (d_b - 1)
        a1_summary_rows.append((b, d_b, n_total_cyc, n_inh, n_new,
                                lower_holds, strong_inh))
        L.append(f"| {b} | {d_b} | {n_total_cyc} | {n_inh} | {n_new} | "
                 f"{lower_holds} | {strong_inh} |\n")

    n_lower_fail = sum(1 for row in a1_summary_rows if not row[5])
    if n_lower_fail == 0:
        L.append(f"\n**Lower bound n_total ≥ d(b)−1 holds for all {len(B_VALUES)} "
                 "wider-b variants at a=1.**\n")
    else:
        L.append(f"\n**Lower bound fails on {n_lower_fail} variants.**\n")

    # ---------------- C-009 verdict ----------------
    L.append("\n## C-009 verdict (period law t_period ≈ L · (1 + log₂ a))\n\n")
    L.append("For each cycle: t_period = total cycle length, L = #odd "
             "members. Per-(a, b) we report mean t_period/L. Predicted: "
             "1 + log₂(a) (= 1 for a=1, ≈2.585 for a=3, ≈3.322 for a=5, "
             "≈3.807 for a=7).\n\n")
    L.append("| a | b | n_cycles | mean t_period/L | predicted | abs deviation |\n")
    L.append("|---|---|----------|-----------------|-----------|---------------|\n")
    c009_rows = []
    for a in A_VALUES:
        predicted = 1.0 + math.log2(a) if a > 1 else 1.0
        for b in B_VALUES:
            cyc_list = cycles_by_ab.get((a, b), [])
            ratios = []
            for ci in cyc_list:
                members = list(ci["members_sorted"])
                tp = len(ci["members_t_order"])  # = cycle_len
                Lv = shortcut_L(members)
                if Lv == 0:
                    continue
                ratios.append(tp / Lv)
            if not ratios:
                continue
            mean_r = sum(ratios) / len(ratios)
            dev = abs(mean_r - predicted)
            c009_rows.append((a, b, len(ratios), mean_r, predicted, dev))
            L.append(f"| {a} | {b} | {len(ratios)} | {mean_r:.3f} | "
                     f"{predicted:.3f} | {dev:.3f} |\n")
    if c009_rows:
        max_dev = max(row[5] for row in c009_rows)
        L.append(f"\nMax absolute deviation across all (a, b): **{max_dev:.4f}**.\n")

    # ---------------- C-011 verdict ----------------
    L.append("\n## C-011 verdict (primitive cycle ⇒ b | (2^K − a^L))\n\n")
    L.append("For each `new`-tagged cycle, compute K = t_period − L and check "
             "whether b divides (2^K − a^L).\n\n")
    L.append("| a | b | cycle_id | cycle_min | L | K | 2^K − a^L | "
             "(2^K − a^L) mod b | matches |\n")
    L.append("|---|---|----------|-----------|---|---|-----------|"
             "-------------------|---------|\n")
    c011_total = 0
    c011_match = 0
    c011_failures = []
    new_cycle_inventory = []
    for a in A_VALUES:
        for b in B_VALUES:
            cyc_list = cycles_by_ab.get((a, b), [])
            for ci in cyc_list:
                members = list(ci["members_sorted"])
                tag, parent_b, scale = tag_inheritance(a, b, members, {})
                if tag != "new":
                    continue
                Lv = shortcut_L(members)
                tp = len(ci["members_t_order"])
                K = tp - Lv
                D = 2 ** K - a ** Lv
                mod = D % b if b != 0 else None
                matches = (D != 0 and mod == 0)
                c011_total += 1
                if matches:
                    c011_match += 1
                else:
                    c011_failures.append((a, b, ci["cycle_id"],
                                          ci["cycle_min"], Lv, K, D, mod))
                L.append(f"| {a} | {b} | {ci['cycle_id']} | {ci['cycle_min']} "
                         f"| {Lv} | {K} | {D} | {mod} | "
                         f"{'yes' if matches else 'NO'} |\n")
                new_cycle_inventory.append({
                    "a": a, "b": b, "cycle_id": ci["cycle_id"],
                    "cycle_min": ci["cycle_min"], "cycle_len": tp,
                    "L": Lv, "K": K,
                    "members": list(ci["members_sorted"]),
                    "n_seeds_reaching": ci["n_seeds_reaching"],
                    "c011_match": matches,
                })

    if c011_total == 0:
        L.append("\n**No primitive (`new`-tagged) cycles found in the wider-b "
                 "scope.** C-011 has no new cycles to test.\n")
    else:
        L.append(f"\n**Match rate: {c011_match}/{c011_total} "
                 f"({100 * c011_match / c011_total:.1f}%).**\n")
        if c011_failures:
            L.append("\n### C-011 failures\n\n")
            for a, b, cid, cmin, Lv, K, D, mod in c011_failures:
                L.append(f"- (a={a}, b={b}) cycle_id={cid} cycle_min={cmin} "
                         f"L={Lv} K={K} | 2^K−a^L = {D}, mod b = {mod}\n")

    # ---------------- New `new`-cycle inventory ----------------
    L.append("\n## New `new`-cycle inventory\n\n")
    if not new_cycle_inventory:
        L.append("- No primitive (non-inherited) cycles found.\n")
    else:
        L.append(f"- **Total `new` cycles in the wider-b sweep: "
                 f"{len(new_cycle_inventory)}**\n\n")
        # group by (a, b)
        by_ab: dict[tuple[int, int], list] = {}
        for c in new_cycle_inventory:
            by_ab.setdefault((c["a"], c["b"]), []).append(c)
        for (a, b) in sorted(by_ab.keys()):
            cs = by_ab[(a, b)]
            L.append(f"- **(a={a}, b={b})** — {len(cs)} new cycle(s):\n")
            for c in cs:
                members = c["members"]
                show = ", ".join(str(m) for m in members[:8])
                if len(members) > 8:
                    show += f", ... ({len(members)} total)"
                L.append(f"    - cycle_id={c['cycle_id']} | min={c['cycle_min']} "
                         f"| L={c['L']} | K={c['K']} | t_period={c['cycle_len']} "
                         f"| seeds={c['n_seeds_reaching']} | "
                         f"members={{{show}}}\n")

    # ---------------- Anomalies ----------------
    L.append("\n## Anomalies\n\n")
    anomalies: list[str] = []
    # cycle counts: for each (a, b), report if exceptionally high vs other (a, *)
    for a in A_VALUES:
        per_b = []
        for b in B_VALUES:
            n_cyc = len(cycles_by_ab.get((a, b), []))
            per_b.append((b, n_cyc))
        # find outliers: 3x median or > 5
        counts = sorted(c for _, c in per_b)
        if not counts:
            continue
        median = counts[len(counts) // 2]
        threshold = max(median * 3, 5)
        for b, c in per_b:
            if c >= threshold and c >= 4:
                anomalies.append(
                    f"- (a={a}, b={b}): {c} distinct cycles "
                    f"(median for a={a} across new range: {median})"
                )
    # any (a, b) with exceeded-H or exceeded-T > 0
    for a in A_VALUES:
        for b in B_VALUES:
            sub = df_results[(df_results.a == a) & (df_results.b == b)]
            n_h = int((sub.outcome == "exceeded-H").sum())
            n_t = int((sub.outcome == "exceeded-T").sum())
            if n_h > 0 or n_t > 0:
                anomalies.append(
                    f"- (a={a}, b={b}): {n_h} seeds exceeded H, {n_t} exceeded T"
                )
    if not anomalies:
        L.append("- No notable anomalies (all variants behave like their "
                 "tight-scope analogues; no cycle-count outliers).\n")
    else:
        for line in anomalies:
            L.append(line + "\n")

    # ---------------- Runtime ----------------
    L.append("\n## Runtime\n\n")
    L.append(f"- Total wall-clock: **{t_total:.1f}s**\n")
    L.append(f"- Sweep: **{t_sweep_total:.1f}s**\n")
    L.append(f"- Parquet + summary: {t_parquet:.2f}s\n")
    L.append("- Per-variant timings (top 10 slowest):\n")
    items = sorted(per_variant_runtime.items(), key=lambda kv: -kv[1])[:10]
    for (a, b), t in items:
        L.append(f"    - (a={a}, b={b}): {t:.2f}s\n")

    path.write_text("".join(L))


if __name__ == "__main__":
    main()
