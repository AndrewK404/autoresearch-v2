# Cap set optimization in F₃ⁿ via autoresearch

Set up the cap set construction problem and run autoresearch on it.

## Phase 1 — Scaffold

Create this structure:

```
./
├── problem/
│   ├── priority.py        ← the target file (autoresearch edits this)
│   ├── solve.py           ← read-only, fixed greedy skeleton
│   └── eval.py            ← read-only, runs solve and prints metric
└── BACKGROUND.md
```

### `problem/priority.py`

```python
"""Priority function for cap set greedy construction.

solve(n) enumerates all 3^n vectors in F_3^n, sorts them by
priority(element, n) descending, then greedily adds each one,
skipping any that would form a 3-term arithmetic progression
with two existing members.

Higher priority = considered earlier.

This is the ONLY file the autoresearch loop may modify.
"""


def priority(element: tuple, n: int) -> float:
    """Return priority for adding `element` to the cap set.

    element: tuple of length n, entries in {0, 1, 2}.
    n: dimension.
    Returns: real-valued score, higher = added earlier.
    """
    return 0.0
```

### `problem/solve.py` (immutable)

```python
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
```

### `problem/eval.py` (immutable)

```python
"""Cap set evaluation. DO NOT MODIFY.

Reads CAP_SET_N from environment (default 8). Runs solve, verifies,
prints a parseable summary block. Metric: cap_set_size.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solve import solve, verify_cap_set


def main():
    n = int(os.environ.get("CAP_SET_N", "8"))
    t0 = time.time()
    cap_set = solve(n)
    elapsed = time.time() - t0

    ok, reason = verify_cap_set(cap_set, n)
    if not ok:
        print(f"STATUS: incorrect")
        print(f"REASON: {reason}")
        sys.exit(1)

    print(f"STATUS: correct")
    print(f"n: {n}")
    print(f"cap_set_size: {len(cap_set)}")
    print(f"eval_seconds: {elapsed:.2f}")


if __name__ == "__main__":
    main()
```

### `BACKGROUND.md`

```markdown
# Cap Set Problem

A cap set in F_3^n is a subset with no three distinct elements
x, y, z satisfying x + y + z ≡ 0 (mod 3). Find the largest one.

## Known landmarks

- n=8: best known 512 (FunSearch, Nature 2023). Pre-FunSearch best
  496 (Edel, ~2004).
- n=9: best known 1082 (FunSearch).
- n≥10: less published; meaningful headroom.
- Asymptotic lower bound: ≥ 2.2202^n (Tyrrell 2022 + FunSearch
  follow-up).

## Skeleton

solve(n) is fixed. It sorts all 3^n vectors by priority(element, n)
descending, then greedily adds while maintaining the no-3-AP
invariant. Only priority.py evolves.

## Construction techniques worth exploring (hypotheses, not gospel)

- Edel-style product / extendable-collection constructions.
- Symmetry handling: coordinate permutations, sign flips, affine
  group — priority should respect or deliberately break these.
- Weight-based heuristics: priority by Hamming weight, by entry
  pattern, by lex order on (weight, position).
- Quadratic forms: priority via x^T A x mod 3 for chosen A.
- Tensor / direct product seeded by smaller n.
```

## Phase 2 — Sanity check

Run `CAP_SET_N=8 python problem/eval.py` manually. Expect
`STATUS: correct` and a baseline `cap_set_size` somewhere around
35–50 for the trivial priority function. Fix scaffolding if not.

## Phase 3 — Hand off to autoresearch

Use autoresearch.

When the setup interview asks, the answers are:

- **Goal**: discover a `priority(element, n)` function that, used by
  the fixed greedy in `problem/solve.py`, yields the largest cap set
  in F₃ⁿ. Primary target n=8 (≥496 = validation, ≥512 = match
  FunSearch, >512 = world record). Then sweep n=10, n=11.
- **Target file**: `problem/priority.py`
- **Read-only context**: `problem/solve.py`, `problem/eval.py`,
  `BACKGROUND.md`
- **Eval command**: `CAP_SET_N=8 python problem/eval.py`
- **Eval timeout**: 120 seconds
- **Metric**: `cap_set_size`, maximize, parsed from the
  `cap_set_size: N` line
- **Constraints**: priority must be deterministic, side-effect-free,
  return a finite real for every input. Imports limited to `math`,
  `itertools`, `functools`, `numpy`. No file I/O. No network.
  `solve.py` and `eval.py` are immutable.
- **Success threshold**: 512 at n=8.
- **Stop condition**: plateau-stop after 50 experiments without
  improvement, or manual interrupt.

Run until interrupted. Do not narrate progress in chat — the
autoresearch logs are the record.