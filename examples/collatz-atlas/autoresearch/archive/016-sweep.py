"""016 — Wider a-axis sweep: a ∈ {9, 11, 13}, b odd in [1, 21].

Family: T_{a,b}(n) = n/2 if n even else a*n + b.
Scope: a in {9, 11, 13}, b in {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21}.
Horizons (same as actions 006, 012): S = 10^5, H = 10^13, T = 10^5.

Open question: is the convergent/divergent boundary at a ≤ 3 specifically,
or does it extend to higher odd a values?

Outputs (under autoresearch/archive/, prefix 016-):
  016-results.parquet, 016-cycles.parquet, 016-summary.md.
"""

from __future__ import annotations

import json
import time
from functools import reduce
from math import gcd
from pathlib import Path

import pandas as pd

A_VALUES = [9, 11, 13]
B_VALUES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
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
                        "members_t_order": list(members),
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


def tag_inheritance(a: int, b: int, members: list[int]) -> tuple[str, int | None, int | None]:
    """Return (tag, inherited_from_b, inherited_scale)."""
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


def shortcut_L(members: list[int]) -> int:
    return sum(1 for m in members if m % 2 == 1)


def main() -> None:
    t_start = time.time()

    print(f"Starting wider-a sweep: a={A_VALUES}, b={B_VALUES}, "
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

    out_results = ARCHIVE / "016-results.parquet"
    out_cycles = ARCHIVE / "016-cycles.parquet"
    df_results.to_parquet(out_results, index=False)
    df_cycles.to_parquet(out_cycles, index=False)

    t_parquet_end = time.time()

    summary_path = ARCHIVE / "016-summary.md"
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
    L.append("# 016 — Wider a-axis sweep: a ∈ {9, 11, 13}, b odd in [1, 21]\n")
    L.append("\n## Setup\n\n")
    L.append(
        "Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. "
        f"Scope: `a ∈ {A_VALUES}`, `b ∈ {B_VALUES}` "
        f"({len(A_VALUES) * len(B_VALUES)} new variants). "
        f"Per-variant: every seed `n0 ∈ [1, {SEED_MAX}]`. "
        f"Horizons: value bound `H = {H}`, step bound `T = {T}`. "
        "Same horizons as actions 006, 012. Cycle IDs start at 0 per (a, b).\n"
    )
    L.append(
        "\nGoal: test whether the convergent/divergent boundary at a ≤ 3 "
        "(C-001) extends, or if a = 5 / a = 7 divergence persists across "
        "wider odd a values. Probe a ∈ {9, 11, 13} in the tight b range.\n"
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

    # ---------------- C-001 wider-a verdict ----------------
    L.append("\n## C-001 wider-a verdict\n\n")
    L.append("Does any (a, b) with `a ∈ {9, 11, 13}` have all seeds reach a "
             "cycle? (C-001 was confirmed only at a ∈ {1, 3}.)\n\n")
    full_converge_cells: list[tuple[int, int, int]] = []
    for a in A_VALUES:
        for b in B_VALUES:
            sub = df_results[(df_results.a == a) & (df_results.b == b)]
            total = len(sub)
            n_cycle = int((sub.outcome == "cycle").sum())
            if n_cycle == total:
                full_converge_cells.append((a, b, total))
    if not full_converge_cells:
        L.append("**No fully convergent (a, b) cells found** for "
                 f"a ∈ {A_VALUES}. Every variant has at least some seeds "
                 "exceeding H or T. C-001's full convergence does not "
                 "extend to these wider a values.\n")
    else:
        L.append(f"**{len(full_converge_cells)} cell(s) fully converge:**\n\n")
        for a, b, total in full_converge_cells:
            L.append(f"- (a={a}, b={b}): all {total} seeds reach a cycle\n")

    # ---------------- C-011 verdict ----------------
    L.append("\n## C-011 verdict (primitive cycle ⇒ b | (2^K − a^L))\n\n")
    L.append("For each `new`-tagged primitive cycle, compute K = t_period − L "
             "and check whether b divides (2^K − a^L). Theorem applies for "
             "any odd a, b — expected match rate: 100%.\n\n")
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
                tag, parent_b, scale = tag_inheritance(a, b, members)
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
                # Truncate huge integers in the table
                D_str = str(D) if abs(D) < 10**18 else f"{D:.3e}"
                L.append(f"| {a} | {b} | {ci['cycle_id']} | {ci['cycle_min']} "
                         f"| {Lv} | {K} | {D_str} | {mod} | "
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
        L.append("\n**No primitive (`new`-tagged) cycles found in the wider-a "
                 "scope.**\n")
    else:
        L.append(f"\n**Match rate: {c011_match}/{c011_total} "
                 f"({100 * c011_match / c011_total:.1f}%).**\n")
        if c011_failures:
            L.append("\n### C-011 failures\n\n")
            for a, b, cid, cmin, Lv, K, D, mod in c011_failures:
                L.append(f"- (a={a}, b={b}) cycle_id={cid} cycle_min={cmin} "
                         f"L={Lv} K={K} | 2^K−a^L = {D}, mod b = {mod}\n")

    # ---------------- a-axis dichotomy refinement ----------------
    L.append("\n## a-axis dichotomy refinement\n\n")
    L.append("Fraction of seeds reaching a cycle per (a, b):\n\n")
    L.append("| a \\ b | " + " | ".join(str(b) for b in B_VALUES) + " | mean |\n")
    L.append("|---" + "|---" * (len(B_VALUES) + 1) + "|\n")
    per_a_mean: dict[int, float] = {}
    for a in A_VALUES:
        row_fracs = []
        cells = []
        for b in B_VALUES:
            sub = df_results[(df_results.a == a) & (df_results.b == b)]
            total = len(sub)
            n_cycle = int((sub.outcome == "cycle").sum())
            frac = n_cycle / total if total > 0 else 0.0
            row_fracs.append(frac)
            cells.append(f"{frac:.3f}")
        mean_frac = sum(row_fracs) / len(row_fracs)
        per_a_mean[a] = mean_frac
        L.append(f"| **a={a}** | " + " | ".join(cells) +
                 f" | **{mean_frac:.3f}** |\n")
    L.append("\n**Per-a aggregated convergence fractions:**\n\n")
    for a in A_VALUES:
        L.append(f"- a = {a}: mean fraction of seeds reaching cycle = "
                 f"**{per_a_mean[a]:.4f}** "
                 f"(across b ∈ {B_VALUES})\n")
    L.append("\nFor reference (from action 006):\n")
    L.append("- a = 1: 1.0000 (full convergence)\n")
    L.append("- a = 3: 1.0000 (full convergence)\n")
    L.append("- a = 5: substantial divergence (most seeds escape)\n")
    L.append("- a = 7: substantial divergence (only b, 2b, 4b, 8b cycle "
             "captured)\n")

    # ---------------- Surprises ----------------
    L.append("\n## Surprises\n\n")
    surprises: list[str] = []
    # any (a, b) cell that fully converges
    if full_converge_cells:
        for a, b, total in full_converge_cells:
            surprises.append(
                f"- (a={a}, b={b}): **all {total} seeds reach a cycle** — "
                "unexpected full convergence in the divergent regime"
            )
    # high cycle counts
    for a in A_VALUES:
        per_b = []
        for b in B_VALUES:
            n_cyc = len(cycles_by_ab.get((a, b), []))
            per_b.append((b, n_cyc))
        counts = sorted(c for _, c in per_b)
        median = counts[len(counts) // 2] if counts else 0
        threshold = max(median * 3, 5)
        for b, c in per_b:
            if c >= threshold and c >= 4:
                surprises.append(
                    f"- (a={a}, b={b}): {c} distinct cycles "
                    f"(median for a={a}: {median})"
                )
    # rigid cycle structure: check whether L1 cycle {b, 2b, 4b, ...} exists
    for a in A_VALUES:
        for b in B_VALUES:
            cyc_list = cycles_by_ab.get((a, b), [])
            for ci in cyc_list:
                members = sorted(ci["members_sorted"])
                # Check if it's a pure power-of-2 chain starting from b's odd value
                # An L=1 cycle: one odd, rest even, where the odd is mapped to a*odd+b
                # which then halves. For example, members = {b * 2^i for i in [0..k]}
                # and the trajectory cycles via the odd member.
                if len(members) >= 2 and members[0] == b:
                    # check {b, 2b, 4b, ..., 2^k b}
                    is_pow2_chain = all(
                        members[i] == b * (2 ** i)
                        for i in range(len(members))
                    )
                    if is_pow2_chain:
                        # Does mapping give b -> a*b+b = (a+1)b which equals 2^k * b?
                        k = len(members) - 1
                        if (a + 1) == 2 ** k:
                            # Standard L1 trivial cycle
                            pass
    # parallel cycles: check for cycles whose member sets are gcd-scalings
    for a in A_VALUES:
        for b in B_VALUES:
            cyc_list = cycles_by_ab.get((a, b), [])
            if len(cyc_list) >= 2:
                # check for proportional cycle members
                signatures = []
                for ci in cyc_list:
                    g = list_gcd(list(ci["members_sorted"]))
                    sig = tuple(m // g for m in ci["members_sorted"])
                    signatures.append((g, sig))
                # group by signature
                from collections import defaultdict
                groups = defaultdict(list)
                for g, sig in signatures:
                    groups[sig].append(g)
                for sig, gs in groups.items():
                    if len(gs) >= 2:
                        surprises.append(
                            f"- (a={a}, b={b}): {len(gs)} parallel cycles "
                            f"with shared shape (gcd values: {sorted(gs)})"
                        )
                        break

    if not surprises:
        L.append("- No notable surprises — wider a values (9, 11, 13) behave "
                 "qualitatively like a = 5, 7: substantial divergence, "
                 "limited cycle inventory.\n")
    else:
        for line in surprises:
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

    L.append(f"\n- Total `new` (primitive) cycles found: **{len(new_cycle_inventory)}**\n")

    path.write_text("".join(L))


if __name__ == "__main__":
    main()
