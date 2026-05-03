"""001 — Opening sweep over the tight 3x+1 family.

For each (a, b) with a in {1,3,5,7} and b in {1,3,5,...,21}:
  T_{a,b}(n) = n/2 if n even else a*n + b.
For each starting seed n0 in [1, 10^4], iterate until:
  - exceeds value bound H=10^12  -> "exceeded-H"
  - exceeds step bound T=10^4    -> "exceeded-T"
  - revisits a value             -> "cycle"

Outputs (script writes alongside itself):
  autoresearch/archive/001-results.parquet
  autoresearch/archive/001-cycles.parquet
  autoresearch/archive/001-summary.md
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

# --- config ---
A_VALUES = [1, 3, 5, 7]
B_VALUES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
SEED_MAX = 10_000
H = 10**12
T = 10_000

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "archive"


def run_variant(a: int, b: int):
    """Sweep all seeds in [1, SEED_MAX] under T_{a,b}.

    Per-variant memo cache: value -> (outcome, cycle_id, suffix_max, suffix_steps)
    where suffix_max is max value seen from this node through end-of-trajectory
    inclusive of this node, and suffix_steps is number of transitions from this
    node to the terminal event (cycle revisit, or H exceedance).

    Cache only stores 'cycle' and 'exceeded-H' outcomes (these depend only on
    the value, not on absolute step count). 'exceeded-T' depends on absolute
    step count from the seed and is NOT cached for prefix nodes.

    Returns (results_list, cycles_list).
    """
    cache = {}  # value -> (outcome, cycle_id, suffix_max, suffix_steps)

    cycles_by_members = {}  # sorted tuple -> cycle_id
    cycles_list = []  # list of dicts: {cycle_id, cycle_len, cycle_min, members_sorted, n_seeds_reaching}

    results = []

    for n0 in range(1, SEED_MAX + 1):
        n = n0
        prefix_path = []         # ordered list of values visited in this seed's walk
        prefix_index = {}        # value -> index in prefix_path
        prefix_max = n0
        prefix_steps = 0

        terminal = None  # "cycle" / "exceeded-H" / "exceeded-T"
        cycle_id = -1
        cycle_members = None
        cycle_len = -1
        # suffix info from terminal node n
        suf_outcome = None
        suf_cid = -1
        suf_max = 0
        suf_steps = 0

        while True:
            # 1) cache hit?
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

            # 2) value bound?
            if n > H:
                terminal = "exceeded-H"
                # cache n itself
                cache[n] = ("exceeded-H", -1, n, 0)
                suf_outcome = "exceeded-H"
                suf_cid = -1
                suf_max = n
                suf_steps = 0
                break

            # 3) step bound?
            if prefix_steps >= T:
                terminal = "exceeded-T"
                # don't cache (depends on absolute step count)
                suf_outcome = "exceeded-T"
                suf_cid = -1
                suf_max = n
                suf_steps = 0
                break

            # 4) cycle in current walk?
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
                        "n_seeds_reaching": 0,
                    })
                terminal = "cycle"
                cycle_id = cid
                cycle_members = members_sorted
                # cache the entire cycle
                cyc_max = max(members_sorted)
                for v in members_sorted:
                    if v not in cache:
                        cache[v] = ("cycle", cid, cyc_max, 0)
                suf_outcome = "cycle"
                suf_cid = cid
                suf_max = cyc_max
                suf_steps = 0
                break

            # 5) extend the walk
            prefix_index[n] = len(prefix_path)
            prefix_path.append(n)
            if n > prefix_max:
                prefix_max = n

            if n % 2 == 0:
                n = n // 2
            else:
                n = a * n + b
            prefix_steps += 1

        # Compute totals
        if terminal == "exceeded-T":
            total_max = prefix_max  # n is current value (not in prefix), suf_max == n already
            if n > total_max:
                total_max = n
            total_steps = prefix_steps
        else:
            total_max = max(prefix_max, suf_max)
            total_steps = prefix_steps + suf_steps

        # Memoize prefix nodes (only for cycle / exceeded-H terminations)
        if terminal in ("cycle", "exceeded-H"):
            running_max = suf_max
            running_steps = suf_steps
            # walk prefix backwards
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


def main():
    t_start = time.time()
    all_results = []
    all_cycles = []
    per_variant_runtime = {}

    for a in A_VALUES:
        for b in B_VALUES:
            t0 = time.time()
            results, cycles_info = run_variant(a, b)
            t1 = time.time()
            per_variant_runtime[(a, b)] = t1 - t0
            all_results.extend(results)
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
            n_cycle = sum(1 for r in results if r["outcome"] == "cycle")
            n_h = sum(1 for r in results if r["outcome"] == "exceeded-H")
            n_t = sum(1 for r in results if r["outcome"] == "exceeded-T")
            print(f"  (a={a}, b={b}) {t1-t0:6.2f}s | cycles={len(cycles_info)} "
                  f"| reached={n_cycle} H={n_h} T={n_t}", flush=True)

    t_sweep_end = time.time()

    df_results = pd.DataFrame(all_results)
    df_cycles = pd.DataFrame(all_cycles)

    for col in ["a", "b", "n0", "cycle_id", "cycle_min", "cycle_len", "max_value", "steps_to_outcome"]:
        df_results[col] = df_results[col].astype("int64")
    for col in ["a", "b", "cycle_id", "cycle_len", "cycle_min", "n_seeds_reaching"]:
        df_cycles[col] = df_cycles[col].astype("int64")

    out_results = ARCHIVE / "001-results.parquet"
    out_cycles = ARCHIVE / "001-cycles.parquet"
    df_results.to_parquet(out_results, index=False)
    df_cycles.to_parquet(out_cycles, index=False)

    t_parquet_end = time.time()

    summary_path = ARCHIVE / "001-summary.md"
    write_summary(summary_path, df_results, df_cycles, per_variant_runtime,
                  t_sweep_total=t_sweep_end - t_start,
                  t_parquet=t_parquet_end - t_sweep_end,
                  t_total=t_parquet_end - t_start)

    print(f"\nTotal runtime: {time.time()-t_start:.1f}s")
    print(f"Wrote: {out_results}")
    print(f"Wrote: {out_cycles}")
    print(f"Wrote: {summary_path}")


def write_summary(path: Path, df_results: pd.DataFrame, df_cycles: pd.DataFrame,
                  per_variant_runtime: dict, t_sweep_total: float,
                  t_parquet: float, t_total: float):
    L = []
    L.append("# 001 — Opening sweep summary\n")
    L.append("\n## Setup\n")
    L.append(
        "Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. "
        "Scope: `a ∈ {1,3,5,7}`, `b ∈ {1,3,5,7,9,11,13,15,17,19,21}` (44 variants). "
        "Per-variant: every seed `n0 ∈ [1, 10^4]`. "
        "Horizons: value bound `H = 10^12`, step bound `T = 10^4`. "
        "Outcomes: `cycle` (revisit), `exceeded-H`, `exceeded-T`.\n"
    )

    # Per-variant table
    L.append("\n## Per-variant table\n\n")
    L.append("| a | b | total_seeds | reached_cycle | exceeded_H | exceeded_T | n_distinct_cycles | smallest_cycle_min | largest_cycle_len | max_value_seen |\n")
    L.append("|---|---|-------------|---------------|------------|------------|-------------------|--------------------|-------------------|----------------|\n")

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
            largest_len = int(cyc_sub.cycle_len.max()) if n_distinct > 0 else -1
            max_val = int(sub.max_value.max())
            L.append(f"| {a} | {b} | {total} | {n_cycle} | {n_h} | {n_t} | {n_distinct} | {smallest_cm} | {largest_len} | {max_val} |\n")

    # Cycle inventory
    L.append("\n## Cycle inventory\n\n")
    for a in A_VALUES:
        for b in B_VALUES:
            cyc_sub = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)].sort_values("cycle_min")
            if len(cyc_sub) == 0:
                L.append(f"- **(a={a}, b={b})**: no cycles found (all trajectories exceeded H or T).\n")
                continue
            L.append(f"- **(a={a}, b={b})** — {len(cyc_sub)} distinct cycle(s):\n")
            for _, row in cyc_sub.iterrows():
                members = json.loads(row["cycle_members_json"])
                if len(members) > 6:
                    show = ", ".join(str(m) for m in members[:6]) + f", ... ({len(members)} total)"
                else:
                    show = ", ".join(str(m) for m in members)
                L.append(
                    f"    - cycle_id={row['cycle_id']} | min={row['cycle_min']} | len={row['cycle_len']} | "
                    f"members={{{show}}} | seeds_reaching={row['n_seeds_reaching']}\n"
                )

    # Predictions vs outcomes
    L.append("\n## Surprises against the predictions\n\n")
    L.append(
        "Predictions from `autoresearch/log/000-research-kickoff.md`:\n\n"
        "1. **a=1: trivial. All seeds reach the b-fixed-cycle quickly. No surprises.**\n"
        "2. **a=3, b=1 (classical Collatz): all seeds in [1, 10^4] reach 1.**\n"
        "3. **a=3, b=3: equivalent to classical via n→n/3 substitution if 3|n; otherwise diverges from {n: 3∤n}. (Possibly conjugate — flag.)**\n"
        "4. **a=3, b=5: classical literature suggests at least one extra cycle. Expect: not all seeds reach the trivial cycle.**\n"
        "5. **a=5, b=1: known empirically to have orbits unbounded up to large N for some seeds. Expect: at least one seed hits the H bound or T bound.**\n"
        "6. **a=5,b=3 / ... / a=7,b=*: less tabulated. Expect ≥ 2 (a,b) pairs to show \"additional cycle\" classification.**\n\n"
    )

    def variant_summary(a, b):
        sub = df_results[(df_results.a == a) & (df_results.b == b)]
        cyc_sub = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
        return {
            "n_cycle": int((sub.outcome == "cycle").sum()),
            "n_h": int((sub.outcome == "exceeded-H").sum()),
            "n_t": int((sub.outcome == "exceeded-T").sum()),
            "n_distinct": len(cyc_sub),
            "cycles": cyc_sub,
            "sub": sub,
        }

    L.append("### Verdicts\n\n")

    # P1
    a1_results = [(b, variant_summary(1, b)) for b in B_VALUES]
    a1_all_one_cycle = all(s["n_distinct"] == 1 and s["n_cycle"] == SEED_MAX for _, s in a1_results)
    if a1_all_one_cycle:
        L.append("- **P1 (a=1 trivial): CONFIRMED.** Every (a=1, b) variant has exactly one cycle reached by all 10000 seeds.\n")
    else:
        L.append("- **P1 (a=1 trivial): MIXED/CONTRADICTED.**\n")
        for b, s in a1_results:
            L.append(f"    - a=1, b={b}: distinct_cycles={s['n_distinct']}, reached={s['n_cycle']}, exceeded_H={s['n_h']}, exceeded_T={s['n_t']}.\n")

    # P2
    s = variant_summary(3, 1)
    cyc31 = s["cycles"]
    if len(cyc31) == 1:
        members = sorted(json.loads(cyc31.iloc[0]["cycle_members_json"]))
        if members == [1, 2, 4] and s["n_cycle"] == SEED_MAX:
            L.append("- **P2 (a=3, b=1 classical Collatz → {1,2,4}): CONFIRMED.** All 10000 seeds reach the cycle {1,2,4}. (Sanity check passed.)\n")
        else:
            L.append(f"- **P2 (a=3, b=1 classical Collatz): CONTRADICTED.** Cycle members={members}, n_reached={s['n_cycle']}/{SEED_MAX}.\n")
    else:
        L.append(f"- **P2 (a=3, b=1 classical Collatz): CONTRADICTED.** Found {len(cyc31)} distinct cycles.\n")

    # P3: a=3, b=3
    s = variant_summary(3, 3)
    sub33 = s["sub"]
    nm = sub33[sub33.n0 % 3 != 0]
    mm = sub33[sub33.n0 % 3 == 0]
    nm_c = int((nm.outcome == "cycle").sum())
    nm_h = int((nm.outcome == "exceeded-H").sum())
    m_c = int((mm.outcome == "cycle").sum())
    m_h = int((mm.outcome == "exceeded-H").sum())
    L.append(
        f"- **P3 (a=3, b=3 conjugacy):** distinct_cycles={s['n_distinct']}, "
        f"reached={s['n_cycle']}, H={s['n_h']}, T={s['n_t']}. "
        f"Among 3∤n0: cycle={nm_c}, H={nm_h}. Among 3|n0: cycle={m_c}, H={m_h}. "
        "Note: the iteration `n→3n+3` always produces multiples of 3, and division by 2 preserves the 3-divisibility class once we reach an odd multiple of 3 (n is odd, 3|n → 3n+3=3(n+1) and division by 2 doesn't disturb the 3-factor since 3∤2). "
        "So the long-run dynamics partition by `n0 mod 3` exactly as the prediction suggests; verdict here depends on whether non-multiples-of-3 escape or join a separate cycle.\n"
    )

    # P4
    s = variant_summary(3, 5)
    L.append(
        f"- **P4 (a=3, b=5 extra cycle):** distinct_cycles={s['n_distinct']}, "
        f"reached={s['n_cycle']}/{SEED_MAX}, H={s['n_h']}, T={s['n_t']}. "
    )
    if s["n_distinct"] >= 2:
        L.append("**CONFIRMED** — multiple cycles found.\n")
    elif s["n_h"] > 0 or s["n_t"] > 0:
        L.append("**PARTIAL** — single cycle but some seeds escaped to horizon.\n")
    else:
        L.append("**CONTRADICTED** — only one cycle and all seeds reach it.\n")

    # P5
    s = variant_summary(5, 1)
    L.append(
        f"- **P5 (a=5, b=1 horizon escape):** reached={s['n_cycle']}, "
        f"H={s['n_h']}, T={s['n_t']}, distinct_cycles={s['n_distinct']}. "
    )
    if s["n_h"] > 0 or s["n_t"] > 0:
        L.append("**CONFIRMED** — at least one seed hits horizon.\n")
    else:
        L.append("**CONTRADICTED** — all seeds reach a cycle within horizon.\n")

    # P6
    extra = []
    for a in [5, 7]:
        for b in B_VALUES:
            cyc_sub = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
            if len(cyc_sub) >= 2:
                extra.append((a, b, len(cyc_sub)))
    L.append(f"- **P6 (a∈{{5,7}}, ≥2 variants with additional cycle):** {len(extra)} variant(s) with ≥2 distinct cycles. ")
    if extra:
        L.append("Variants: " + ", ".join(f"(a={a},b={b},nc={n})" for a, b, n in extra) + ". ")
    if len(extra) >= 2:
        L.append("**CONFIRMED**.\n")
    else:
        L.append("**CONTRADICTED or WEAKER**.\n")

    # Anomalies
    L.append("\n## Anomalies and standouts\n\n")
    single_cycle_all = []
    multi_cycle = []
    horizon_escapes = []
    big_max = []
    for a in A_VALUES:
        for b in B_VALUES:
            sub = df_results[(df_results.a == a) & (df_results.b == b)]
            cyc_sub = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
            n_cycle = int((sub.outcome == "cycle").sum())
            n_h = int((sub.outcome == "exceeded-H").sum())
            n_t = int((sub.outcome == "exceeded-T").sum())
            n_dist = len(cyc_sub)
            mv = int(sub.max_value.max())
            if n_dist == 1 and n_cycle == SEED_MAX:
                single_cycle_all.append((a, b))
            if n_dist >= 2:
                multi_cycle.append((a, b, n_dist))
            if n_h + n_t > 0:
                horizon_escapes.append((a, b, n_h, n_t))
            big_max.append((a, b, mv))

    big_max.sort(key=lambda t: -t[2])

    L.append(f"- **Single-cycle, all-seeds-reach** ({len(single_cycle_all)} variants): "
             + ", ".join(f"(a={a},b={b})" for a, b in single_cycle_all) + "\n")
    if multi_cycle:
        L.append("- **Multiple distinct cycles**: "
                 + ", ".join(f"(a={a},b={b},nc={n})" for a, b, n in multi_cycle) + "\n")
    else:
        L.append("- **Multiple distinct cycles**: none.\n")
    if horizon_escapes:
        L.append("- **Variants with ≥1 horizon escape**: "
                 + ", ".join(f"(a={a},b={b},H={h},T={t})" for a, b, h, t in horizon_escapes) + "\n")
    else:
        L.append("- **Variants with ≥1 horizon escape**: none.\n")
    L.append("- **Top 10 variants by max value reached**:\n")
    for a, b, mv in big_max[:10]:
        L.append(f"    - (a={a}, b={b}): max_value = {mv}\n")

    # Runtime
    L.append("\n## Runtime\n\n")
    L.append(f"- Total wall-clock: **{t_total:.1f}s**\n")
    L.append(f"- Sweep loop (44 variants): **{t_sweep_total:.1f}s**\n")
    L.append(f"- Parquet write: {t_parquet:.2f}s\n")
    L.append("- Per-variant timings (top 10 slowest):\n")
    items = sorted(per_variant_runtime.items(), key=lambda kv: -kv[1])[:10]
    for (a, b), t in items:
        L.append(f"    - (a={a}, b={b}): {t:.2f}s\n")

    path.write_text("".join(L))


if __name__ == "__main__":
    main()
