"""Analytic trivial-cycle catalog for T_{a,b}.

Family:
  n even -> n/2
  n odd  -> a*n + b

For each (a, b) in scope, enumerate cycles of "shortcut length" L in {1, 2, 3}.
A shortcut step takes an odd n, applies n -> a*n + b, then halves k_i times
until odd again. The cycle is a sequence (k_1, ..., k_L) of positive integers
returning to the starting odd n.

Algebra:
  L=1: n*(2^k - a) = b
  L=2: n0*(2^{k1+k2} - a^2) = b*(a + 2^{k1})
  L=3: n0*(2^{k1+k2+k3} - a^3) = b*(a^2 + a*2^{k1} + 2^{k1+k2})

We then VERIFY each candidate by simulation: starting at n0, apply T_{a,b}
period steps and confirm we return to n0, with the predicted shortcut sequence.
"""

from __future__ import annotations

from math import gcd


def T(n: int, a: int, b: int) -> int:
    if n % 2 == 0:
        return n // 2
    return a * n + b


def shortcut_step(n: int, a: int, b: int):
    """Given odd n, return (n_next, k) where n_next is the next odd value
    after one a*n+b followed by k halvings."""
    assert n % 2 == 1
    m = a * n + b
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1
    return m, k


def simulate_cycle(n0: int, a: int, b: int, length: int):
    """Run `length` shortcut steps from odd n0; return (members, ks).

    members is the list of odd nodes encountered (n0, n1, ..., n_{L-1}).
    ks is the list of halvings per step.
    Returns None if any step produces non-positive value or n0 is even.
    """
    if n0 <= 0 or n0 % 2 == 0:
        return None
    members = [n0]
    ks = []
    n = n0
    for _ in range(length):
        n, k = shortcut_step(n, a, b)
        ks.append(k)
        members.append(n)
    return members, ks


def find_length1(a: int, b: int, k_max: int = 20):
    """Solve n*(2^k - a) = b -> n = b/(2^k - a).
    For a=1 this gives many; for a>=2 only finitely many (since 2^k - a >= b
    gives n < 1).
    """
    out = []
    for k in range(1, k_max + 1):
        denom = (1 << k) - a
        if denom <= 0:
            continue
        if b % denom != 0:
            continue
        n = b // denom
        if n <= 0 or n % 2 == 0:
            continue
        # verify
        sim = simulate_cycle(n, a, b, 1)
        if sim is None:
            continue
        members, ks = sim
        if members[-1] == n and ks == [k]:
            out.append({"k": (k,), "n0": n, "members": tuple(sorted({n})), "period": 1 + k})
        if denom >= b and k > 1:
            # 2^k - a only grows; for a >= 2, denom > b means n=0, no more solutions
            # but for a=1 with b odd, denom = 2^k - 1 grows; once denom > b and b%denom != 0, no more.
            pass
    return out


def find_length2(a: int, b: int, k_max: int = 12):
    out = []
    seen_cycles = set()
    for k1 in range(1, k_max + 1):
        for k2 in range(1, k_max + 1):
            denom = (1 << (k1 + k2)) - a * a
            if denom <= 0:
                continue
            num = b * (a + (1 << k1))
            if num % denom != 0:
                continue
            n0 = num // denom
            if n0 <= 0 or n0 % 2 == 0:
                continue
            sim = simulate_cycle(n0, a, b, 2)
            if sim is None:
                continue
            members, ks = sim
            if members[-1] == n0 and ks == [k1, k2]:
                # exclude length-1 cycles (where n0 == n1)
                distinct = sorted(set(members[:-1]))
                if len(distinct) < 2:
                    continue
                key = tuple(distinct)
                if key in seen_cycles:
                    continue
                seen_cycles.add(key)
                out.append({"k": (k1, k2), "n0": n0, "members": tuple(distinct),
                            "period": 2 + k1 + k2})
    return out


def find_length3(a: int, b: int, k_max: int = 8):
    out = []
    seen_cycles = set()
    for k1 in range(1, k_max + 1):
        for k2 in range(1, k_max + 1):
            for k3 in range(1, k_max + 1):
                denom = (1 << (k1 + k2 + k3)) - a ** 3
                if denom <= 0:
                    continue
                num = b * (a * a + a * (1 << k1) + (1 << (k1 + k2)))
                if num % denom != 0:
                    continue
                n0 = num // denom
                if n0 <= 0 or n0 % 2 == 0:
                    continue
                sim = simulate_cycle(n0, a, b, 3)
                if sim is None:
                    continue
                members, ks = sim
                if members[-1] == n0 and ks == [k1, k2, k3]:
                    distinct = sorted(set(members[:-1]))
                    if len(distinct) < 3:
                        continue
                    key = tuple(distinct)
                    if key in seen_cycles:
                        continue
                    seen_cycles.add(key)
                    out.append({"k": (k1, k2, k3), "n0": n0, "members": tuple(distinct),
                                "period": 3 + k1 + k2 + k3})
    return out


def canonicalize_cycles(cycles):
    """Deduplicate cycles by their member set (rotations of (k_i) yield same cycle)."""
    seen = {}
    for c in cycles:
        key = c["members"]
        if key not in seen or c["period"] < seen[key]["period"]:
            seen[key] = c
    return list(seen.values())


def all_cycles(a: int, b: int):
    L1 = find_length1(a, b)
    L2 = find_length2(a, b)
    L3 = find_length3(a, b)
    L1 = canonicalize_cycles(L1)
    L2 = canonicalize_cycles(L2)
    L3 = canonicalize_cycles(L3)
    # filter L3 cycles that are actually L1 (period mismatch already handles)
    # also filter L2 that are actually two consecutive L1 (shouldn't happen by distinct check)
    return {"L1": L1, "L2": L2, "L3": L3}


def main():
    avals = [1, 3, 5, 7]
    bvals = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
    results = {}
    for a in avals:
        for b in bvals:
            results[(a, b)] = all_cycles(a, b)

    # Print summary
    print("a,b | L1 | L2 | L3 | smallest | cycles")
    for (a, b), r in results.items():
        n_total = len(r["L1"]) + len(r["L2"]) + len(r["L3"])
        all_members = []
        for c in r["L1"] + r["L2"] + r["L3"]:
            all_members.extend(c["members"])
        smallest = min(all_members) if all_members else None
        cycle_strs = []
        for c in r["L1"]:
            cycle_strs.append(f"L1 k={c['k']} m={c['members']}")
        for c in r["L2"]:
            cycle_strs.append(f"L2 k={c['k']} m={c['members']}")
        for c in r["L3"]:
            cycle_strs.append(f"L3 k={c['k']} m={c['members']}")
        print(f"{a},{b} | {len(r['L1'])} | {len(r['L2'])} | {len(r['L3'])} | "
              f"{smallest} | {'; '.join(cycle_strs) if cycle_strs else '(none)'}")
    return results


if __name__ == "__main__":
    main()
