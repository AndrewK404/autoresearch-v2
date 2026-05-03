"""024 — S=10^6 verification of C-015 power law.

C-015: f(a, b, S) ∝ S^{-c(a, b)}, where f(a, b, S) is the fraction of seeds
n0 ∈ [1, S] whose T_{a,b} trajectory reaches a cycle within (H, T) horizons.

Empirical c values (from S=10^4 in action 001 vs S=10^5 in action 006):
  (5,1): c≈0.379, predicts f(10^6) ≈ 0.01266
  (5,9): c≈0.329, predicts f(10^6) ≈ 0.05814
  (5,19): c≈0.363, predicts f(10^6) ≈ 0.00549
  (7,1): c≈0.699, predicts f(10^6) ≈ 0.000328
  (7,13): c≈0.721, predicts f(10^6) ≈ 0.000144

This action runs T_{a,b} on a ∈ {5, 7}, b odd in [1, 21] at horizon S = 10^6,
H = 10^14, T = 10^5, with aggressive suffix memoization. Predicted vs observed
f(10^6) is computed per cell.

Outputs (under autoresearch/archive/, prefix 024-):
  024-results.parquet, 024-cycles.parquet, 024-summary.md.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import pandas as pd

A_VALUES = [5, 7]
B_VALUES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
SEED_MAX = 1_000_000
H = 10**14
T = 100_000

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "archive"


def run_variant(a: int, b: int):
    """Sweep all seeds in [1, SEED_MAX] under T_{a,b} with suffix memo.

    Cache: value -> (outcome, cycle_id, suffix_max, suffix_steps). Caches only
    'cycle' / 'exceeded-H' (suffix-deterministic). 'exceeded-T' is per-seed
    (depends on absolute step count) and is not cached.
    """
    cache: dict[int, tuple[str, int, int, int]] = {}
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


def main() -> None:
    t_start = time.time()

    print(f"024 sweep: a={A_VALUES}, b={B_VALUES}, "
          f"S={SEED_MAX}, H={H}, T={T}", flush=True)

    # Load prior cycle-id maps (001 + 006) for ID re-use.
    prior_id_map: dict[tuple[int, int], dict[tuple, int]] = {}
    next_id_map: dict[tuple[int, int], int] = {}
    for src in ("001-cycles.parquet", "006-cycles.parquet"):
        p = ARCHIVE / src
        if not p.exists():
            continue
        df = pd.read_parquet(p)
        for _, row in df.iterrows():
            members = tuple(sorted(json.loads(row["cycle_members_json"])))
            key = (int(row["a"]), int(row["b"]))
            cid = int(row["cycle_id"])
            sub = prior_id_map.setdefault(key, {})
            if members not in sub:
                sub[members] = cid
            cur = next_id_map.get(key, -1)
            if cid > cur:
                next_id_map[key] = cid

    # Load f(S=10^5) per (a, b) from 006-results for prediction comparison.
    df_006 = pd.read_parquet(ARCHIVE / "006-results.parquet")
    df_001 = pd.read_parquet(ARCHIVE / "001-results.parquet")
    f5: dict[tuple[int, int], float] = {}
    f4: dict[tuple[int, int], float] = {}
    for a in A_VALUES:
        for b in B_VALUES:
            sub5 = df_006[(df_006.a == a) & (df_006.b == b)]
            sub4 = df_001[(df_001.a == a) & (df_001.b == b)]
            if len(sub5) > 0:
                f5[(a, b)] = float((sub5.outcome == "cycle").sum()) / len(sub5)
            if len(sub4) > 0:
                f4[(a, b)] = float((sub4.outcome == "cycle").sum()) / len(sub4)

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

            # Re-map cycle IDs to prior IDs where matching, else assign new IDs.
            prior_for_ab = prior_id_map.get((a, b), {})
            next_new_id = next_id_map.get((a, b), -1) + 1
            new_id_map: dict[int, tuple[int, bool]] = {}
            for ci in cycles_info:
                members = ci["members_sorted"]
                if members in prior_for_ab:
                    final_id = prior_for_ab[members]
                    is_new = False
                else:
                    final_id = next_new_id
                    next_new_id += 1
                    is_new = True
                new_id_map[ci["cycle_id"]] = (final_id, is_new)

            for ci in cycles_info:
                final_id, is_new = new_id_map[ci["cycle_id"]]
                all_cycles.append({
                    "a": a,
                    "b": b,
                    "cycle_id": final_id,
                    "cycle_len": ci["cycle_len"],
                    "cycle_min": ci["cycle_min"],
                    "cycle_members_json": json.dumps(list(ci["members_sorted"])),
                    "n_seeds_reaching": ci["n_seeds_reaching"],
                    "new_in_024": is_new,
                })

            for r in results:
                if r["outcome"] == "cycle":
                    r["cycle_id"] = new_id_map[r["cycle_id"]][0]

            all_results.extend(results)

            n_cycle = sum(1 for r in results if r["outcome"] == "cycle")
            n_h = sum(1 for r in results if r["outcome"] == "exceeded-H")
            n_t = sum(1 for r in results if r["outcome"] == "exceeded-T")
            n_new = sum(1 for ci in cycles_info if new_id_map[ci["cycle_id"]][1])
            f6_obs = n_cycle / SEED_MAX
            print(f"  (a={a}, b={b}) {t1-t0:7.2f}s | cycles={len(cycles_info)} "
                  f"(new={n_new}) | reached={n_cycle} H={n_h} T={n_t} "
                  f"| f(10^6)={f6_obs:.6f}", flush=True)

    t_sweep_end = time.time()

    df_results = pd.DataFrame(all_results)
    df_cycles = pd.DataFrame(all_cycles)

    for col in ["a", "b", "n0", "cycle_id", "cycle_min", "cycle_len",
                "max_value", "steps_to_outcome"]:
        df_results[col] = df_results[col].astype("int64")
    for col in ["a", "b", "cycle_id", "cycle_len", "cycle_min", "n_seeds_reaching"]:
        df_cycles[col] = df_cycles[col].astype("int64")

    out_results = ARCHIVE / "024-results.parquet"
    out_cycles = ARCHIVE / "024-cycles.parquet"
    df_results.to_parquet(out_results, index=False)
    df_cycles.to_parquet(out_cycles, index=False)

    t_parquet_end = time.time()

    summary_path = ARCHIVE / "024-summary.md"
    write_summary(
        summary_path,
        df_results,
        df_cycles,
        f4,
        f5,
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
                  f4: dict, f5: dict,
                  per_variant_runtime: dict[tuple[int, int], float],
                  t_sweep_total: float, t_parquet: float, t_total: float) -> None:
    L: list[str] = []
    L.append("# 024 — S=10^6 verification of C-015 power law\n")
    L.append("\n## Setup\n\n")
    L.append(
        "Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. "
        f"Scope: `a ∈ {A_VALUES}`, `b ∈ {B_VALUES}` "
        f"({len(A_VALUES) * len(B_VALUES)} variants). "
        f"Per-variant: every seed `n0 ∈ [1, {SEED_MAX:,}]`. "
        f"Horizons: value bound `H = 10^{int(math.log10(H))}`, step bound `T = {T:,}`.\n\n"
        "C-015 (proposed): `f(a, b, S) ∝ S^{-c(a, b)}`. "
        "We compute `c(a, b)` from the empirical S=10^4 → S=10^5 ratio "
        "(actions 001 → 006), predict `f(10^6) = f(10^5) · 10^{-c}`, "
        "then compare against observed `f(10^6)` from this sweep.\n\n"
        "Cycle IDs reuse 001/006 IDs where the same member set appears; new "
        "cycles get fresh IDs (column `new_in_024 = True`).\n"
    )

    L.append("\n## Power-law verdict per (a, b)\n\n")
    L.append(
        "| a | b | f(10^4) | f(10^5) | c=-log10(f5/f4) | predicted f(10^6) "
        "| observed f(10^6) | ratio obs/pred | fit error |\n"
    )
    L.append(
        "|---|---|---------|---------|------------------|-------------------"
        "|------------------|----------------|-----------|\n"
    )
    rows: list[dict] = []
    for a in A_VALUES:
        for b in B_VALUES:
            sub6 = df_results[(df_results.a == a) & (df_results.b == b)]
            n6 = len(sub6)
            f6_obs = float((sub6.outcome == "cycle").sum()) / n6 if n6 else float("nan")
            f4v = f4.get((a, b), float("nan"))
            f5v = f5.get((a, b), float("nan"))
            if (
                not math.isnan(f4v) and not math.isnan(f5v)
                and f4v > 0 and f5v > 0
            ):
                c = -math.log10(f5v / f4v)
                pred6 = f5v * (10 ** (-c))
            else:
                c = float("nan")
                pred6 = float("nan")
            ratio = (f6_obs / pred6) if (pred6 and not math.isnan(pred6) and pred6 > 0) else float("nan")
            fit_err = abs(ratio - 1.0) if not math.isnan(ratio) else float("nan")
            rows.append({
                "a": a, "b": b, "f4": f4v, "f5": f5v, "c": c,
                "pred6": pred6, "obs6": f6_obs, "ratio": ratio, "fit_err": fit_err,
            })
            L.append(
                f"| {a} | {b} | {f4v:.6f} | {f5v:.6f} | {c:.3f} "
                f"| {pred6:.6f} | {f6_obs:.6f} | {ratio:.3f} | {fit_err:.3f} |\n"
            )

    valid_ratios = [r["ratio"] for r in rows if not math.isnan(r["ratio"])]
    valid_ratios_sorted = sorted(valid_ratios)
    n_valid = len(valid_ratios_sorted)
    if n_valid:
        median_ratio = (
            valid_ratios_sorted[n_valid // 2]
            if n_valid % 2 == 1
            else 0.5 * (valid_ratios_sorted[n_valid // 2 - 1] + valid_ratios_sorted[n_valid // 2])
        )
    else:
        median_ratio = float("nan")
    n_within_20 = sum(1 for r in valid_ratios if 0.8 <= r <= 1.2)
    n_within_50 = sum(1 for r in valid_ratios if 0.5 <= r <= 1.5)
    fail_50 = [r for r in rows if not math.isnan(r["ratio"]) and (r["ratio"] < 0.5 or r["ratio"] > 1.5)]

    L.append("\n## C-015 verdict\n\n")
    L.append(f"- Cells with valid prediction: **{n_valid}** of {len(rows)}.\n")
    L.append(f"- **Median ratio observed/predicted: {median_ratio:.3f}**\n")
    L.append(f"- Cells within ±20% of 1.0: **{n_within_20}/{n_valid}**\n")
    L.append(f"- Cells within ±50% of 1.0: **{n_within_50}/{n_valid}**\n")
    if fail_50:
        L.append(f"- Cells failing ±50% (|ratio-1|>0.5): **{len(fail_50)}**\n\n")
        for r in fail_50:
            L.append(
                f"    - (a={r['a']}, b={r['b']}): obs={r['obs6']:.6f}, "
                f"pred={r['pred6']:.6f}, ratio={r['ratio']:.3f}\n"
            )
    else:
        L.append("- No cells fail ±50%.\n")

    if n_within_20 == n_valid and n_valid > 0:
        L.append("\n**C-015 power law CONFIRMED within ±20% across all cells.**\n")
    elif n_within_50 == n_valid and n_valid > 0:
        L.append("\n**C-015 power law APPROXIMATELY HOLDS (all cells within ±50%, not all within ±20%).**\n")
    else:
        L.append("\n**C-015 power law NOT confirmed (some cells outside ±50%).**\n")

    # Cycle inventory diff vs 006.
    L.append("\n## Cycle inventory diff vs S=10^5 (action 006)\n\n")
    L.append("| a | b | n_cycles_006 | n_cycles_024 | new_in_024 |\n")
    L.append("|---|---|--------------|--------------|------------|\n")
    df_006_cyc = pd.read_parquet(ARCHIVE / "006-cycles.parquet")
    new_total = 0
    new_by_ab: dict[tuple[int, int], list] = {}
    for a in A_VALUES:
        for b in B_VALUES:
            n006 = int(((df_006_cyc.a == a) & (df_006_cyc.b == b)).sum())
            cyc024 = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
            n024 = len(cyc024)
            new_rows = cyc024[cyc024.new_in_024]
            new_count = len(new_rows)
            new_total += new_count
            new_by_ab[(a, b)] = list(new_rows.itertuples(index=False))
            L.append(f"| {a} | {b} | {n006} | {n024} | {new_count} |\n")

    L.append(f"\n**Total new cycles found at S=10^6: {new_total}.**\n")
    if new_total:
        L.append("\n### New-cycle details\n\n")
        for (a, b), rows_list in new_by_ab.items():
            if not rows_list:
                continue
            L.append(f"- **(a={a}, b={b})** — {len(rows_list)} new cycle(s):\n")
            for r in rows_list:
                members = json.loads(r.cycle_members_json)
                show = ", ".join(str(m) for m in members[:8])
                if len(members) > 8:
                    show += f", ... ({len(members)} total)"
                L.append(
                    f"    - cycle_id={r.cycle_id} | min={r.cycle_min} | "
                    f"len={r.cycle_len} | members={{{show}}} | "
                    f"seeds_reaching={r.n_seeds_reaching}\n"
                )

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
