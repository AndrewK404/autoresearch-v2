"""006 — 10x horizon falsification sweep + sub-lattice attractivity probe.

Family: T_{a,b}(n) = n/2 if n even else a*n + b.
Scope: a in {1,3,5,7}, b odd in [1,21].
Horizons: S = 10^5, H = 10^13, T = 10^5.

Falsification targets:
  - C-001: a in {1,3} -> all seeds in [1, S] cycle within (H, T).
  - C-003: a=7, b in {1,3,7,13,17,21} -> only L1 cycle {b,2b,4b,8b}.
  - C-004: (3,13) cycle count at higher horizon.

Job B: For each (a,b) with b composite (b in {9,15,21}, all 4 a-values), and
each odd lambda > 1 with lambda | b and lambda < b, log first_lambda_hit time
per seed not in lambda Z. If a seed not in lambda Z exceeds H without entering
lambda Z, that's a counterexample to forward-attractivity (C-006).

Outputs (all under autoresearch/archive/, prefix 006-):
  006-results.parquet, 006-cycles.parquet, 006-attractivity.parquet,
  006-summary.md.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import pandas as pd

A_VALUES = [1, 3, 5, 7]
B_VALUES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
SEED_MAX = 100_000
H = 10**13
T = 100_000

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = REPO_ROOT / "archive"

ATTR_BS = [9, 15, 21]  # composite b
ATTR_BIN_EDGES = [0, 10, 100, 1_000, 10_000, 100_001]  # bins: [low, high) up to 1e5+1
# Bin labels: 0-10, 10-100, 100-1000, 1000-10000, 10000-100000, never


def odd_proper_divisors_gt1(b: int):
    """Odd divisors lambda of b with 1 < lambda < b."""
    out = []
    for d in range(3, b, 2):
        if b % d == 0:
            out.append(d)
    return out


def step(n: int, a: int, b: int) -> int:
    if n % 2 == 0:
        return n // 2
    return a * n + b


def run_variant(a: int, b: int, lambdas: list[int], prior_cycles: dict):
    """Sweep all seeds in [1, SEED_MAX] under T_{a,b}.

    prior_cycles: dict members_sorted_tuple -> cycle_id (from 001).
    lambdas: list of odd divisors of b in (1, b). Empty if b prime.

    Per-variant memo cache:
      cache[v] = (outcome, cycle_id, suffix_max, suffix_steps)
    where outcome is 'cycle' or 'exceeded-H'. exceeded-T is never cached.

    Additionally, we track lambda-hit info per cached value:
      lambda_cache[v][lambda] = first_steps_to_hit (int) or -1 (never hits before
                                terminal -- terminal here means cycle entry or H).
      The convention is: if v itself in lambda Z, value is 0.
      If terminal is cycle and no member of cycle is in lambda Z, never reaches.
      If terminal is exceeded-H, never (within H).

    For each seed, we compute first_lambda_hit per lambda, which is the first
    t >= 1 with T^t(n0) in lambda Z. If n0 already in lambda Z, we still want
    smallest t >= 1; we treat n0 in lambda Z separately.

    Per task spec: log first_lambda_hit only for seeds NOT in lambda Z.
    Per (a,b,lambda): histogram of bins, plus counterexample tally
    (n0 not in lambda Z that exceeded H without entering lambda Z).

    Returns: results, cycles_list, attractivity_data
    """
    cache = {}  # value -> (outcome, cid, suffix_max, suffix_steps)
    # lambda_cache[v] = dict lambda -> first_steps_to_lambdaZ from v (>=0), or math.inf
    lambda_cache: dict[int, dict[int, float]] = {}

    cycles_by_members: dict[tuple, int] = {}
    cycles_list = []  # per-variant list

    # Pre-populate with prior cycles? Actually we only assign IDs once we discover
    # a cycle. We'll resolve final ID at the end. For simplicity, assign new IDs
    # internally then map to prior IDs after.

    results = []

    has_lams = bool(lambdas)

    for n0 in range(1, SEED_MAX + 1):
        n = n0
        prefix_path = []
        prefix_index = {}
        prefix_max = n0
        prefix_steps = 0

        # For lambda tracking: compute per-step which lambdas hit.
        # We want, for each lambda, the smallest t >= 1 with T^t(n0) in lambda Z.
        # Initialize first-hit per lambda to None (unknown / not yet hit).
        first_hit: dict[int, int | None] = {lam: None for lam in lambdas} if has_lams else {}

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
                # lambda: combine prefix-hits with cache's lambda info from n
                if has_lams:
                    lam_info = lambda_cache.get(n, {})
                    for lam in lambdas:
                        if first_hit[lam] is not None:
                            continue
                        cached_d = lam_info.get(lam, math.inf)
                        if cached_d == math.inf:
                            continue  # never within suffix
                        # cached_d is steps from n to first lambda Z hit (>=0).
                        # If cached_d == 0 then n itself is in lambda Z, and
                        # the absolute step from n0 is prefix_steps + 0.
                        # But we also want t >= 1: if prefix_steps + cached_d == 0
                        # (i.e. n0 == n and n0 in lambda Z), we ignore (handled later).
                        t_abs = prefix_steps + int(cached_d)
                        if t_abs >= 1:
                            first_hit[lam] = t_abs
                break

            if n > H:
                terminal = "exceeded-H"
                cache[n] = ("exceeded-H", -1, n, 0)
                if has_lams:
                    # n itself: if n in lambda Z, suffix dist is 0; else inf.
                    # But we cap by H — n exceeds H, so we don't actually go into
                    # lambda Z from n's POV. Convention: at this terminal, no
                    # further lambda hits are possible. Mark as inf for all
                    # lambdas (n exceeded H — game over). But if n itself IS
                    # in lambda Z, that's still a hit from the perspective of
                    # absolute steps. Capture that.
                    lam_info = {}
                    for lam in lambdas:
                        if n % lam == 0:
                            lam_info[lam] = 0
                        else:
                            lam_info[lam] = math.inf
                    lambda_cache[n] = lam_info
                    for lam in lambdas:
                        if first_hit[lam] is not None:
                            continue
                        if lam_info[lam] == 0:
                            t_abs = prefix_steps  # n was reached via prefix_steps
                            if t_abs >= 1:
                                first_hit[lam] = t_abs
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
                # Cache cycle members. Compute per-cycle lambda-hit:
                # within a cycle, distance from each member to nearest lambda-Z
                # member (in forward direction). If no member in lambda Z, inf.
                # Compute by walking once around the cycle in T-order from each member?
                # Simpler: gather lambda Z members and their positions in
                # the cycle (in T-order), then dist[i] = (pos_lz - i) mod L.
                # We need cycle in T-order, not sorted. members (the prefix slice)
                # is already in T-order.
                cycle_order = list(members)  # T-order, len L (no repeats)
                L_cyc = len(cycle_order)
                cyc_pos = {v: i for i, v in enumerate(cycle_order)}
                if has_lams:
                    cyc_lambda_info = {}
                    for lam in lambdas:
                        lz_positions = [i for i, v in enumerate(cycle_order) if v % lam == 0]
                        if not lz_positions:
                            for v in cycle_order:
                                cyc_lambda_info.setdefault(v, {})[lam] = math.inf
                        else:
                            for i, v in enumerate(cycle_order):
                                # distance forward to nearest lz position
                                best = min((p - i) % L_cyc for p in lz_positions)
                                cyc_lambda_info.setdefault(v, {})[lam] = best
                else:
                    cyc_lambda_info = {v: {} for v in cycle_order}
                for v in cycle_order:
                    if v not in cache:
                        cache[v] = ("cycle", cid, cyc_max, 0)
                        if has_lams:
                            lambda_cache[v] = cyc_lambda_info[v]

                # combine prefix with terminal node n's lambda info
                if has_lams:
                    lam_info = lambda_cache[n]
                    for lam in lambdas:
                        if first_hit[lam] is not None:
                            continue
                        d = lam_info.get(lam, math.inf)
                        if d == math.inf:
                            continue
                        t_abs = prefix_steps + int(d)
                        if t_abs >= 1:
                            first_hit[lam] = t_abs
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

            # Check lambda hits at this step (n is at absolute step prefix_steps)
            if has_lams:
                if prefix_steps >= 1:
                    for lam in lambdas:
                        if first_hit[lam] is None and n % lam == 0:
                            first_hit[lam] = prefix_steps

            n_next = n // 2 if n % 2 == 0 else a * n + b
            n = n_next
            prefix_steps += 1

        # After loop: also check final n value at step prefix_steps if no terminal-reached lambda hit
        # Not needed: we've handled cache hit / cycle / H.

        # Compute totals
        if terminal == "exceeded-T":
            total_max = prefix_max
            if n > total_max:
                total_max = n
            total_steps = prefix_steps
        else:
            total_max = max(prefix_max, suf_max)
            total_steps = prefix_steps + suf_steps

        # Memoize prefix nodes (only for cycle / exceeded-H)
        if terminal in ("cycle", "exceeded-H"):
            running_max = suf_max
            running_steps = suf_steps
            # For lambda info on prefix nodes, we propagate distances backward.
            # For each prefix node v at index i, distance to lambda Z =
            #   if v in lambda Z: 0
            #   else: 1 + dist(next_node)
            # We can rebuild from suffix.
            # Get suffix lambda info from terminal node n.
            if has_lams:
                # Start from n's lambda info
                if n in lambda_cache:
                    suffix_lam = dict(lambda_cache[n])
                else:
                    suffix_lam = {lam: math.inf for lam in lambdas}
            for i in range(len(prefix_path) - 1, -1, -1):
                v = prefix_path[i]
                running_steps += 1
                if v > running_max:
                    running_max = v
                if v not in cache:
                    cache[v] = (terminal, suf_cid, running_max, running_steps)
                    if has_lams:
                        v_lam = {}
                        for lam in lambdas:
                            if v % lam == 0:
                                v_lam[lam] = 0
                            else:
                                d = suffix_lam.get(lam, math.inf)
                                v_lam[lam] = (d + 1) if d != math.inf else math.inf
                        lambda_cache[v] = v_lam
                        suffix_lam = v_lam
                else:
                    if has_lams:
                        # Use existing cached info for downstream propagation
                        suffix_lam = lambda_cache.get(v, suffix_lam)

        if terminal == "cycle":
            cycles_list[cycle_id]["n_seeds_reaching"] += 1

        # Build first_lambda_hit dict for this seed (only for lambda where n0 NOT in lambda Z)
        flh_dict = {}
        for lam in lambdas:
            if n0 % lam == 0:
                # n0 already in lambda Z — task says "for seeds not in lambda Z";
                # we still record but mark as 0? Actually task says:
                # "first_lambda_hit (JSON dict mapping each odd-lambda-divisor of
                # b to either an int or 'never')". For seeds in lambda Z, the
                # smallest t >= 1 with T^t(n0) in lambda Z — could be 1 if next
                # step is in lambda Z, else more. We'll still record it.
                # But for the attractivity probe, we exclude n0 in lambda Z.
                # Compute: smallest t >= 1 with T^t in lambda Z.
                pass  # fall through to compute below
            if first_hit[lam] is not None:
                flh_dict[lam] = first_hit[lam]
            else:
                flh_dict[lam] = "never"

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
            "first_lambda_hit": json.dumps(flh_dict) if flh_dict else None,
        })

    return results, cycles_list


def bin_index(t: int) -> int:
    """Map t to bin index. ATTR_BIN_EDGES = [0, 10, 100, 1000, 10000, 100001].
    Bins:
      0: [0, 10)
      1: [10, 100)
      2: [100, 1000)
      3: [1000, 10000)
      4: [10000, 100001)
    """
    for i in range(len(ATTR_BIN_EDGES) - 1):
        if ATTR_BIN_EDGES[i] <= t < ATTR_BIN_EDGES[i + 1]:
            return i
    return len(ATTR_BIN_EDGES) - 1  # shouldn't happen


def main():
    t_start = time.time()

    # Sanity check
    print("Sanity check: (a=3, b=1) at S=10^5, H=10^13, T=10^5...", flush=True)
    sanity_results, sanity_cycles = run_variant(3, 1, [], {})
    n_cycle = sum(1 for r in sanity_results if r["outcome"] == "cycle")
    cycle_members = set()
    for ci in sanity_cycles:
        cycle_members.update(ci["members_sorted"])
    expected = {1, 2, 4}
    if n_cycle != SEED_MAX or cycle_members != expected:
        raise RuntimeError(
            f"Sanity check FAILED: n_cycle={n_cycle}/{SEED_MAX}, "
            f"cycle_members={cycle_members}, expected={expected}"
        )
    print(f"  Sanity OK: all {SEED_MAX} seeds reach {{1,2,4}}.", flush=True)
    t_sanity = time.time()
    print(f"  Sanity time: {t_sanity - t_start:.1f}s", flush=True)

    # Load 001 cycles for ID re-use
    df_cycles_001 = pd.read_parquet(ARCHIVE / "001-cycles.parquet")
    prior_id_map: dict[tuple[int, int], dict[tuple, int]] = {}
    for _, row in df_cycles_001.iterrows():
        members = tuple(sorted(json.loads(row["cycle_members_json"])))
        prior_id_map.setdefault((int(row["a"]), int(row["b"])), {})[members] = int(row["cycle_id"])

    all_results = []
    all_cycles = []
    per_variant_runtime: dict[tuple[int, int], float] = {}

    for a in A_VALUES:
        for b in B_VALUES:
            t0 = time.time()
            if a == 3 and b == 1:
                # already ran in sanity, but re-run to capture full data with lambdas (none here)
                results = sanity_results
                cycles_info = sanity_cycles
                lams = []
            else:
                lams = odd_proper_divisors_gt1(b)
                results, cycles_info = run_variant(a, b, lams, {})
            t1 = time.time()
            per_variant_runtime[(a, b)] = t1 - t0
            all_results.extend(results)

            # Re-map cycle IDs to 001 IDs where matching, else assign new IDs
            # starting from max(prior_id) + 1.
            prior_for_ab = prior_id_map.get((a, b), {})
            next_new_id = (max(prior_for_ab.values()) + 1) if prior_for_ab else 0
            new_id_map = {}  # internal_id -> final_id
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
                    "new_in_006": is_new,
                })

            # Update results' cycle_id to final mapped IDs
            for r in results:
                if r["outcome"] == "cycle":
                    r["cycle_id"] = new_id_map[r["cycle_id"]][0]

            n_cycle = sum(1 for r in results if r["outcome"] == "cycle")
            n_h = sum(1 for r in results if r["outcome"] == "exceeded-H")
            n_t = sum(1 for r in results if r["outcome"] == "exceeded-T")
            n_new = sum(1 for ci in cycles_info if new_id_map[ci["cycle_id"]][1])
            print(f"  (a={a}, b={b}) {t1-t0:6.2f}s | cycles={len(cycles_info)} (new={n_new}) "
                  f"| reached={n_cycle} H={n_h} T={n_t}", flush=True)

    t_sweep_end = time.time()

    # Build attractivity table for (a, b) with b in ATTR_BS, all lambdas with 1 < lam < b odd lam | b.
    attr_rows = []
    counterexamples: dict[tuple[int, int, int], int] = {}

    df_results_tmp = pd.DataFrame(all_results)
    for b in ATTR_BS:
        lams = odd_proper_divisors_gt1(b)
        for a in A_VALUES:
            sub = df_results_tmp[(df_results_tmp.a == a) & (df_results_tmp.b == b)]
            for lam in lams:
                # bins of first_lambda_hit time for seeds NOT in lam Z
                bin_counts = [0] * (len(ATTR_BIN_EDGES) - 1)
                never_count = 0
                ce_count = 0  # n0 not in lam Z that exceeded H without entering lam Z
                ever_count = 0
                total_not_in_lamZ = 0
                max_hit_among_entered = 0
                never_among_not_exceeded_H = 0
                for _, row in sub.iterrows():
                    n0 = row["n0"]
                    if n0 % lam == 0:
                        continue
                    total_not_in_lamZ += 1
                    flh_str = row["first_lambda_hit"]
                    if flh_str is None:
                        # shouldn't happen for composite b
                        continue
                    flh = json.loads(flh_str)
                    val = flh.get(str(lam))
                    if val is None or val == "never":
                        never_count += 1
                        if row["outcome"] == "exceeded-H":
                            ce_count += 1
                        else:
                            # not exceeded-H and never entered: count for the col
                            never_among_not_exceeded_H += 1
                    else:
                        ever_count += 1
                        bi = bin_index(int(val))
                        bin_counts[bi] += 1
                        if int(val) > max_hit_among_entered:
                            max_hit_among_entered = int(val)

                # rows: per bin
                for bi in range(len(ATTR_BIN_EDGES) - 1):
                    attr_rows.append({
                        "a": a,
                        "b": b,
                        "lambda": lam,
                        "bin_low": ATTR_BIN_EDGES[bi],
                        "bin_high": ATTR_BIN_EDGES[bi + 1],
                        "n_seeds_in_bin": bin_counts[bi],
                    })
                # special "never" row
                attr_rows.append({
                    "a": a,
                    "b": b,
                    "lambda": lam,
                    "bin_low": -1,
                    "bin_high": -1,
                    "n_seeds_in_bin": never_count,
                })
                counterexamples[(a, b, lam)] = ce_count

    df_attr = pd.DataFrame(attr_rows)

    df_results = pd.DataFrame(all_results)
    df_cycles = pd.DataFrame(all_cycles)

    for col in ["a", "b", "n0", "cycle_id", "cycle_min", "cycle_len", "max_value", "steps_to_outcome"]:
        df_results[col] = df_results[col].astype("int64")
    for col in ["a", "b", "cycle_id", "cycle_len", "cycle_min", "n_seeds_reaching"]:
        df_cycles[col] = df_cycles[col].astype("int64")
    for col in ["a", "b", "lambda", "bin_low", "bin_high", "n_seeds_in_bin"]:
        df_attr[col] = df_attr[col].astype("int64")

    out_results = ARCHIVE / "006-results.parquet"
    out_cycles = ARCHIVE / "006-cycles.parquet"
    out_attr = ARCHIVE / "006-attractivity.parquet"
    df_results.to_parquet(out_results, index=False)
    df_cycles.to_parquet(out_cycles, index=False)
    df_attr.to_parquet(out_attr, index=False)

    t_parquet_end = time.time()

    summary_path = ARCHIVE / "006-summary.md"
    write_summary(
        summary_path,
        df_results,
        df_cycles,
        df_attr,
        df_cycles_001,
        per_variant_runtime,
        counterexamples,
        t_sweep_total=t_sweep_end - t_start,
        t_parquet=t_parquet_end - t_sweep_end,
        t_total=t_parquet_end - t_start,
    )

    print(f"\nTotal runtime: {time.time()-t_start:.1f}s")
    print(f"Wrote: {out_results}")
    print(f"Wrote: {out_cycles}")
    print(f"Wrote: {out_attr}")
    print(f"Wrote: {summary_path}")


def write_summary(path, df_results, df_cycles, df_attr, df_cycles_001,
                  per_variant_runtime, counterexamples,
                  t_sweep_total, t_parquet, t_total):
    L = []
    L.append("# 006 — 10x horizon falsification sweep + sub-lattice attractivity\n")
    L.append("\n## Setup\n\n")
    L.append(
        "Family: `T_{a,b}(n) = n/2` if n even, else `a*n + b`. "
        "Scope: `a ∈ {1,3,5,7}`, `b ∈ {1,3,5,7,9,11,13,15,17,19,21}` (44 variants). "
        "Per-variant: every seed `n0 ∈ [1, 10^5]`. "
        "Horizons: value bound `H = 10^13`, step bound `T = 10^5`. "
        "Outcomes: `cycle` (revisit), `exceeded-H`, `exceeded-T`.\n\n"
        "Cycle IDs reuse 001's IDs where the same member set appears; "
        "new cycles get new IDs (column `new_in_006 = True`).\n"
    )

    # Diff vs 001
    L.append("\n## Diff vs action 001\n\n")
    L.append("| a | b | n_cycles_001 | n_cycles_006 | new_cycles |\n")
    L.append("|---|---|--------------|--------------|------------|\n")
    new_by_ab = {}
    for a in A_VALUES:
        for b in B_VALUES:
            n001 = int(((df_cycles_001.a == a) & (df_cycles_001.b == b)).sum())
            cyc_006 = df_cycles[(df_cycles.a == a) & (df_cycles.b == b)]
            n006 = len(cyc_006)
            new_rows = cyc_006[cyc_006.new_in_006]
            new_count = len(new_rows)
            new_by_ab[(a, b)] = list(new_rows.itertuples(index=False))
            L.append(f"| {a} | {b} | {n001} | {n006} | {new_count} |\n")

    L.append("\n### Variants with new cycles (members, len)\n\n")
    any_new = False
    for (a, b), rows in new_by_ab.items():
        if not rows:
            continue
        any_new = True
        L.append(f"- **(a={a}, b={b})** — {len(rows)} new cycle(s):\n")
        for r in rows:
            members = json.loads(r.cycle_members_json)
            show = ", ".join(str(m) for m in members[:8])
            if len(members) > 8:
                show += f", ... ({len(members)} total)"
            L.append(
                f"    - cycle_id={r.cycle_id} | min={r.cycle_min} | len={r.cycle_len} | "
                f"members={{{show}}} | seeds_reaching={r.n_seeds_reaching}\n"
            )
    if not any_new:
        L.append("- No new cycles found in any variant.\n")

    # C-001 verdict
    L.append("\n## C-001 verdict (a ∈ {1,3}, b odd in [1,21])\n\n")
    sub = df_results[(df_results.a.isin([1, 3]))]
    n_total = len(sub)
    n_cycle = int((sub.outcome == "cycle").sum())
    n_h = int((sub.outcome == "exceeded-H").sum())
    n_t = int((sub.outcome == "exceeded-T").sum())
    if n_cycle == n_total:
        L.append(f"**CONFIRMED at 10× horizon.** All {n_total} trajectories (a∈{{1,3}}) reached a cycle within T=10^5 steps without exceeding H=10^13.\n")
    else:
        L.append(f"**FALSIFIED at 10× horizon.** Out of {n_total}: cycle={n_cycle}, exceeded-H={n_h}, exceeded-T={n_t}.\n")
        bad = sub[sub.outcome != "cycle"]
        first_bad = bad.head(20)
        L.append("\nFirst falsifiers:\n\n")
        for _, r in first_bad.iterrows():
            L.append(f"- (a={r.a}, b={r.b}, n0={r.n0}): outcome={r.outcome}, max_value={r.max_value}, steps={r.steps_to_outcome}\n")

    # C-003 verdict
    L.append("\n## C-003 verdict (a=7, b ∈ {1,3,7,13,17,21}: only L1 cycle {b,2b,4b,8b})\n\n")
    c003_bs = [1, 3, 7, 13, 17, 21]
    c003_falsifiers = []
    for b in c003_bs:
        cyc = df_cycles[(df_cycles.a == 7) & (df_cycles.b == b)]
        expected = sorted([b, 2 * b, 4 * b, 8 * b])
        for _, r in cyc.iterrows():
            members = sorted(json.loads(r.cycle_members_json))
            if members != expected:
                c003_falsifiers.append((b, r.cycle_id, members, r.cycle_len, int(r.n_seeds_reaching)))
    if not c003_falsifiers:
        L.append("**CONFIRMED at 10× horizon.** For every b ∈ {1,3,7,13,17,21}, the only cycles reached by seeds in [1,10^5] are the L1 cycles {b, 2b, 4b, 8b}.\n")
    else:
        L.append(f"**FALSIFIED at 10× horizon.** {len(c003_falsifiers)} cycle(s) other than the L1 cycle:\n\n")
        for b, cid, members, L_, nsr in c003_falsifiers:
            show = ", ".join(str(m) for m in members[:8])
            if len(members) > 8:
                show += f", ... ({len(members)} total)"
            L.append(f"- (a=7, b={b}) cycle_id={cid} | len={L_} | members={{{show}}} | seeds_reaching={nsr}\n")

    # C-004 verdict
    L.append("\n## C-004 verdict ((3, 13) cycle richness at 10× horizon)\n\n")
    cyc_313 = df_cycles[(df_cycles.a == 3) & (df_cycles.b == 13)]
    n_313 = len(cyc_313)
    n_313_001 = int(((df_cycles_001.a == 3) & (df_cycles_001.b == 13)).sum())
    new_313 = cyc_313[cyc_313.new_in_006]
    L.append(f"- Cycle count (a=3, b=13) at 001 horizon: **{n_313_001}**.\n")
    L.append(f"- Cycle count at 10× horizon: **{n_313}**.\n")
    L.append(f"- New cycles at 10× horizon: **{len(new_313)}**.\n")
    if len(new_313):
        L.append("\nNew cycles:\n\n")
        for _, r in new_313.iterrows():
            members = json.loads(r.cycle_members_json)
            show = ", ".join(str(m) for m in members[:8])
            if len(members) > 8:
                show += f", ... ({len(members)} total)"
            L.append(
                f"- cycle_id={r.cycle_id} | min={r.cycle_min} | len={r.cycle_len} | "
                f"members={{{show}}} | seeds_reaching={r.n_seeds_reaching}\n"
            )

    # Sub-lattice attractivity (C-006)
    L.append("\n## Sub-lattice attractivity (C-006) per (a, b, λ)\n\n")
    L.append("| a | b | λ | fraction_ever_entered_λZ | max_hit_time_among_entered | n_never_among_non_H | n_counterexamples_to_attractivity |\n")
    L.append("|---|---|---|--------------------------|----------------------------|---------------------|-----------------------------------|\n")
    for b in ATTR_BS:
        lams = odd_proper_divisors_gt1(b)
        for a in A_VALUES:
            for lam in lams:
                # compute from df_attr and df_results
                sub_attr = df_attr[(df_attr.a == a) & (df_attr.b == b) & (df_attr["lambda"] == lam)]
                ever_rows = sub_attr[sub_attr.bin_low >= 0]
                never_row = sub_attr[sub_attr.bin_low == -1]
                ever = int(ever_rows.n_seeds_in_bin.sum())
                never = int(never_row.n_seeds_in_bin.sum())
                total = ever + never
                frac = ever / total if total > 0 else float("nan")

                # max hit time among entered: scan results for this (a,b)
                sub_res = df_results[(df_results.a == a) & (df_results.b == b)]
                max_hit = 0
                never_not_H = 0
                ce = counterexamples.get((a, b, lam), 0)
                for _, r in sub_res.iterrows():
                    n0 = r.n0
                    if n0 % lam == 0:
                        continue
                    flh_str = r.first_lambda_hit
                    if flh_str is None:
                        continue
                    flh = json.loads(flh_str)
                    v = flh.get(str(lam))
                    if v is None or v == "never":
                        if r.outcome != "exceeded-H":
                            never_not_H += 1
                    else:
                        if int(v) > max_hit:
                            max_hit = int(v)
                L.append(
                    f"| {a} | {b} | {lam} | {frac:.4f} | {max_hit} | {never_not_H} | {ce} |\n"
                )

    total_ce = sum(counterexamples.values())
    L.append(f"\n**Total counterexamples to forward-attractivity (n0 ∉ λZ exceeding H without entering λZ):** {total_ce}\n")

    # Runtime
    L.append("\n## Runtime\n\n")
    L.append(f"- Total wall-clock: **{t_total:.1f}s**\n")
    L.append(f"- Sweep + sanity: **{t_sweep_total:.1f}s**\n")
    L.append(f"- Parquet + summary: {t_parquet:.2f}s\n")
    L.append("- Per-variant timings (top 10 slowest):\n")
    items = sorted(per_variant_runtime.items(), key=lambda kv: -kv[1])[:10]
    for (a, b), t in items:
        L.append(f"    - (a={a}, b={b}): {t:.2f}s\n")

    path.write_text("".join(L))


if __name__ == "__main__":
    main()
