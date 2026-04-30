"""Greedy cap set construction in F_3^n. DO NOT MODIFY."""
import itertools
from priority import priority


def solve(n: int) -> list:
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: priority(e, n), reverse=True)

    cap_set = []
    forbidden = set()

    for e in elements:
        if e in forbidden:
            continue
        for u in cap_set:
            c = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
            forbidden.add(c)
        cap_set.append(e)
        forbidden.add(e)

    return cap_set


def verify_cap_set(cap_set: list, n: int) -> tuple[bool, str]:
    s = set(cap_set)
    if len(s) != len(cap_set):
        return False, "duplicate elements"
    for x, y in itertools.combinations(cap_set, 2):
        z = tuple((3 - xi - yi) % 3 for xi, yi in zip(x, y))
        if z in s and z != x and z != y:
            return False, f"3-AP found: {x}, {y}, {z}"
    return True, "ok"
