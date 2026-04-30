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
