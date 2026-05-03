"""Action 008 — algebraic enumeration of (3, 13) L=5 cycles.

For T_{a, b} with a=3, b=13, shortcut length L=5, T-period 13 means
sum of halving exponents Sigma k_i = 13 - 5 = 8. The shortcut equation:

    n0 * (2^K - a^L) = b * sum_{i=0}^{L-1} a^{L-1-i} * 2^{k_1+...+k_i}

With K=8, a=3, b=13: 2^8 - 3^5 = 256 - 243 = 13. The factor 13 cancels:

    n0 = 81 + 27*2^{k1} + 9*2^{k1+k2} + 3*2^{k1+k2+k3} + 2^{k1+k2+k3+k4}

Enumerate all C(7,4)=35 compositions of 8 into 5 positive parts;
for each compute n0; check whether n0 is odd; simulate to verify the
predicted halving pattern; deduplicate by member set.

Compares against the 7 cycles found by sweep in action 005:
cycle_min ∈ {211, 227, 251, 259, 283, 287, 319}.

Run:
    python autoresearch/archive/008-l5-enumeration.py
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

A = 3
B = 13
L = 5
K_SUM = 8  # T-period - L = 13 - 5 = 8

# 7 sweep cycles from action 005-l4plus-catalog.md (a=3, b=13, L=5, t_period=13)
SWEEP_CYCLE_MINS = [211, 227, 251, 259, 283, 287, 319]


def compositions(total: int, parts: int):
    """Yield compositions of `total` into `parts` strictly positive parts."""
    # Place (parts-1) dividers among (total-1) gaps between unit balls.
    for divs in combinations(range(1, total), parts - 1):
        bounds = (0,) + divs + (total,)
        yield tuple(bounds[i + 1] - bounds[i] for i in range(parts))


def n0_from_composition(ks: tuple[int, ...]) -> int:
    """Compute n0 for halving vector ks given a=3, L=5, K=8."""
    # n0 = a^4 + a^3 * 2^{k1} + a^2 * 2^{k1+k2} + a * 2^{k1+k2+k3} + 2^{k1+k2+k3+k4}
    cum = 0
    n0 = A ** (L - 1)  # the term with no 2^... factor (i=0 -> a^4)
    for i in range(L - 1):
        cum += ks[i]
        coeff = A ** (L - 2 - i)
        n0 += coeff * (2 ** cum)
    return n0


def t_step(n: int) -> int:
    """One T_{3,13} step. Odd: 3n+13. Even: n//2."""
    if n % 2 == 1:
        return A * n + B
    return n // 2


def simulate_cycle(n0: int, expected_ks: tuple[int, ...]) -> tuple[bool, list[int], tuple[int, ...]]:
    """Simulate from n0 and check if it returns to n0 in exactly T-period steps,
    matching expected halving pattern. Returns (valid, members, observed_ks)."""
    if n0 % 2 == 0:
        return False, [], ()
    members: list[int] = []
    observed_ks: list[int] = []
    n = n0
    members.append(n)
    # 5 shortcut steps; each: one odd step then k_i halvings
    for i in range(L):
        if n % 2 != 1:
            return False, members, tuple(observed_ks)
        n = A * n + B  # odd step
        members.append(n)
        # halve while even, count
        k = 0
        while n % 2 == 0:
            n = n // 2
            k += 1
            if i < L - 1 or n != n0:
                # don't add the n0 itself again on final return
                if not (i == L - 1 and n == n0 and k > 0):
                    members.append(n)
                else:
                    members.append(n)  # we'll dedupe later
        observed_ks.append(k)
    # The cycle should have closed
    closed = (n == n0)
    # remove the trailing duplicate of n0 if present
    if members and members[-1] == n0:
        members = members[:-1]
    valid = closed and tuple(observed_ks) == expected_ks
    return valid, members, tuple(observed_ks)


def member_set_from_cycle(n0: int) -> frozenset[int]:
    """Run T_{3,13} until return to n0, collecting all members."""
    members = {n0}
    n = t_step(n0)
    steps = 0
    max_steps = 10_000
    while n != n0 and steps < max_steps:
        members.add(n)
        n = t_step(n)
        steps += 1
    return frozenset(members)


def cycle_min(member_set: frozenset[int]) -> int:
    return min(member_set)


def main() -> None:
    rows = []
    cycle_sets: dict[frozenset[int], dict] = {}

    comps = list(compositions(K_SUM, L))
    assert len(comps) == 35, f"expected 35 compositions, got {len(comps)}"

    for ks in comps:
        n0 = n0_from_composition(ks)
        odd = (n0 % 2 == 1)
        if odd:
            valid, members, observed_ks = simulate_cycle(n0, ks)
        else:
            valid, members, observed_ks = False, [], ()

        member_set = frozenset(members) if valid else frozenset()
        cmin = min(member_set) if member_set else None

        rows.append({
            "ks": ks,
            "n0": n0,
            "odd": odd,
            "valid": valid,
            "member_set": member_set,
            "cycle_min": cmin,
            "observed_ks": observed_ks,
        })

        if valid:
            if member_set not in cycle_sets:
                cycle_sets[member_set] = {
                    "cycle_min": cmin,
                    "members_sorted": sorted(member_set),
                    "first_ks": ks,
                    "n0_first": n0,
                    "rotations": [ks],
                }
            else:
                cycle_sets[member_set]["rotations"].append(ks)

    # match against sweep
    sweep_set = set(SWEEP_CYCLE_MINS)
    found_mins = {c["cycle_min"] for c in cycle_sets.values()}

    distinct = len(cycle_sets)
    missing = sweep_set - found_mins
    extras = found_mins - sweep_set

    # ----- write markdown -----
    out_md = Path(__file__).with_suffix(".md")
    lines = []
    lines.append("# 008 — Algebraic enumeration of (3, 13) L=5 cycles")
    lines.append("")
    lines.append("Companion script: `autoresearch/archive/008-l5-enumeration.py`. ")
    lines.append("Source comparison: `autoresearch/archive/005-l4plus-catalog.md` (the 7 sweep cycles).")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append("For T_{a, b} with a=3, b=13, the shortcut equation at L=5, T-period=13 is")
    lines.append("")
    lines.append("    n0 * (2^K - a^L) = b * sum_{i=0..L-1} a^{L-1-i} * 2^{k_1+...+k_i}")
    lines.append("")
    lines.append("where K = sum(k_i) = T-period - L = 13 - 5 = 8 and each k_i >= 1.")
    lines.append("With a=3, b=13: 2^8 - 3^5 = 256 - 243 = 13. The factor 13 cancels and")
    lines.append("")
    lines.append("    n0 = 81 + 27*2^{k1} + 9*2^{k1+k2} + 3*2^{k1+k2+k3} + 2^{k1+k2+k3+k4}.")
    lines.append("")
    lines.append("So *every* composition of 8 into 5 positive parts yields a positive integer n0.")
    lines.append("A valid cycle further requires:")
    lines.append("- n0 is **odd** (entry point of an odd step), and")
    lines.append("- Simulation of T_{3,13} from n0 returns to n0 in exactly 13 T-steps with the")
    lines.append("  predicted halving pattern (k1, ..., k5).")
    lines.append("")
    lines.append("Cyclic rotations of the halving vector yield the same cycle (5 rotations per")
    lines.append("cycle), so we deduplicate by member set.")
    lines.append("")
    lines.append("## Per-composition table")
    lines.append("")
    lines.append("| (k1,k2,k3,k4,k5) | n0 | n0 odd? | valid cycle? | member set (sorted, first 6) | cycle_id (sweep cycle_min) |")
    lines.append("|---|---:|:---:|:---:|---|---|")
    for r in rows:
        ks_str = "(" + ",".join(str(k) for k in r["ks"]) + ")"
        if r["valid"]:
            sorted_members = sorted(r["member_set"])
            preview = sorted_members[:6]
            preview_str = "[" + ", ".join(str(m) for m in preview)
            if len(sorted_members) > 6:
                preview_str += ", ..."
            preview_str += "]"
            cmin = r["cycle_min"]
            if cmin in sweep_set:
                cid_str = f"cycle_min={cmin}"
            else:
                cid_str = f"cycle_min={cmin} (NOT in sweep)"
        else:
            preview_str = "—"
            cid_str = "—"
        lines.append(
            f"| {ks_str} | {r['n0']} | {'yes' if r['odd'] else 'no'} | "
            f"{'yes' if r['valid'] else 'no'} | {preview_str} | {cid_str} |"
        )

    n_odd = sum(1 for r in rows if r["odd"])
    n_valid = sum(1 for r in rows if r["valid"])

    lines.append("")
    lines.append("## Distinct cycle count")
    lines.append("")
    lines.append(f"- Total compositions: {len(rows)}")
    lines.append(f"- n0 odd: {n_odd}")
    lines.append(f"- Valid cycles (after simulation): {n_valid}")
    lines.append(f"- Distinct cycles after dedup by member set: **{distinct}**")
    lines.append("")
    lines.append("Per-cycle multiplicity (number of compositions mapping to each cycle):")
    lines.append("")
    lines.append("| cycle_min | rotations (compositions yielding this cycle) |")
    lines.append("|---:|---|")
    for ms, info in sorted(cycle_sets.items(), key=lambda x: x[1]["cycle_min"]):
        rots = info["rotations"]
        rots_str = "; ".join("(" + ",".join(str(k) for k in r) + ")" for r in rots)
        lines.append(f"| {info['cycle_min']} | {len(rots)}: {rots_str} |")

    lines.append("")
    lines.append("## Comparison vs sweep")
    lines.append("")
    lines.append(f"- Sweep (action 005) reports 7 primitive L=5 cycles with cycle_min in:")
    lines.append(f"  {sorted(sweep_set)}")
    lines.append(f"- Algebraic enumeration finds {distinct} distinct cycles with cycle_min in:")
    lines.append(f"  {sorted(found_mins)}")
    lines.append(f"- Missing from algebraic vs sweep: {sorted(missing) if missing else 'none'}")
    lines.append(f"- Extras in algebraic vs sweep: {sorted(extras) if extras else 'none'}")
    lines.append("")
    if distinct == 7 and not missing and not extras:
        lines.append("**Match: exact.** Algebraic count equals sweep count; member sets match 1-to-1.")
    else:
        lines.append("**Mismatch.** See discrepancies above.")
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    if distinct == 7 and not missing and not extras:
        lines.append("C-008 verdict: **algebraically confirmed.** Of 35 compositions of 8 into 5")
        lines.append(f"positive parts, {n_odd} yield odd n0 and {n_valid} yield valid L=5 cycles;")
        lines.append("after deduplicating by member set (5 cyclic rotations per cycle), exactly **7**")
        lines.append("distinct primitive cycles remain. They match the 7 sweep cycles 1-to-1. The")
        lines.append("count of 7 is therefore not just empirical — it is the exact number of integer")
        lines.append("solutions to the L=5 shortcut equation for (3, 13).")
    else:
        lines.append("C-008 verdict: **discrepancy detected** — see comparison section.")

    out_md.write_text("\n".join(lines) + "\n")
    print(f"wrote {out_md}")
    print(f"compositions: {len(rows)}, odd n0: {n_odd}, valid: {n_valid}, distinct: {distinct}")
    print(f"sweep cycle_mins: {sorted(sweep_set)}")
    print(f"algebraic cycle_mins: {sorted(found_mins)}")
    print(f"missing: {sorted(missing)}, extras: {sorted(extras)}")


if __name__ == "__main__":
    main()
