"""Batch tester for cap-set priority candidates. NOT the eval.

Reproduces problem/solve.py's logic exactly so we can score many priority
functions per round without thrashing problem/priority.py. The official
score is still produced by `CAP_SET_N=N python problem/eval.py`.
"""
import itertools
import time
from typing import Callable


def cap_set_size(priority_fn: Callable, n: int) -> int:
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: priority_fn(e, n), reverse=True)
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
    # quick verify
    s = set(cap_set)
    for x, y in itertools.combinations(cap_set, 2):
        z = tuple((3 - xi - yi) % 3 for xi, yi in zip(x, y))
        if z in s and z != x and z != y:
            raise AssertionError(f"3-AP: {x},{y},{z}")
    return len(cap_set)


def bench(name, fn, n=8):
    t0 = time.time()
    sz = cap_set_size(fn, n)
    dt = time.time() - t0
    print(f"  {name:50s}  size={sz:5d}   ({dt:.2f}s)")
    return sz


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print(f"n={n}, |F_3^n|={3**n}")
    bench("baseline (constant 0)", lambda e, n: 0.0, n)
