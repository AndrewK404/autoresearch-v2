# RESUME

## Important answers
- Problem: cap set construction in F_3^n via greedy with priority function.
- Skeleton: `problem/solve.py` and `problem/eval.py` are immutable. Only
  `problem/priority.py` evolves.
- Primary n=8. Targets: 496 = validation; 512 = match FunSearch; >512 = world
  record. Then sweep n=10, n=11.
- Baseline (priority returns 0.0): cap_set_size=256 at n=8 (lex-order greedy
  recovers {0,1}^n, which is a 2^n cap set since there are no 3-collinear
  points with entries in {0,1}).
- Eval is fast (<1s for n=8), so experiment cycles are cheap.

## Envs
(none required)

## Bootstrap
1. (no setup needed — Python 3 with stdlib + numpy)

## Notes
- `priority(element, n)` may use `math`, `itertools`, `functools`, `numpy` only.
- Sort is stable; ties break in `itertools.product(range(3), repeat=n)` order.
- `solve.py` line 54: `elements.sort(key=lambda e: priority(e, n), reverse=True)`.
- `solve.py` line 63: forbidden update uses `(3 - ui - ei) % 3` per coord (the
  unique third point of the line through u and e).
- For n=8, |F_3^8| = 6561, so priority is called 6561 times per eval.
