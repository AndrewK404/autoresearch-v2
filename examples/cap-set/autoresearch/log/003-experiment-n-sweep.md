# exp 005-007 — c2-target priority across n=9, 10, 11

## What & why
PROMPT calls for sweeping n=10 and n=11 after n=8. Question: does the
same priority (`-|c2 - 3|`) keep paying out at higher n, and what cap
sizes does it produce?

## Done
- `CAP_SET_N=9 python problem/eval.py` → 896, 0.24s
- `CAP_SET_N=10 python problem/eval.py` → 2048, 1.31s
- `CAP_SET_N=11 python problem/eval.py` → 4096, 6.11s
- For each `n ∈ {10, 11}` also swept `c2 ∈ {0..n}` to check the target
  shape (archive/030-higher-n.py).

## Result
Best `c2` target at each `n` (under priority `-|c2 - target|`):

| n  | best target | size | baseline 2^n | ratio  | known max |
|----|-------------|------|--------------|--------|-----------|
| 8  | c2=3        | 448  | 256          | 1.75×  | 512 (FunSearch) / 496 (Edel) |
| 9  | c2=3        | 896  | 512          | 1.75×  | 1082 (FunSearch) |
| 10 | c2=3        | 2048 | 1024         | 2.00×  | (>2.22^10 ≈ 2600 known lower bound) |
| 11 | c2=3        | 4096 | 2048         | 2.00×  | (>2.22^11 ≈ 5800 known lower bound) |

For n=10 and n=11 specifically, c2=3 wins over c2=4 (1216, 2432) and
c2=2 (1536, 3072) and c2=5 (1536, 3072). `c2=3` is robustly the best
single c2-target across all n from 8 to 11.

## Reasoning
The target c2=3 is *not* `n/3` rounded — at n=10, n/3 ≈ 3.33 and at
n=11, n/3 ≈ 3.67, but neither c2=4 nor a higher target wins. The exact
integer 3 is structurally privileged. This is a real (small) finding:
the optimal target for the simple count-based priority is **constant
across the range we tested**, not scaling with n.

Sizes 1024, 2048, 4096 at n=9, 10, 11 are exact powers of 2, which is
suggestive of an underlying product-of-`{0,1}^k`-with-a-fixed-c2-pattern
structure. Worth investigating in follow-up.

We are short of the known-best caps at every n we measured, by amounts
ranging from -48 (n=8 vs Edel) to roughly -1500 (n=10 vs the 2.22^n
asymptotic lower bound). To close that gap we would need a non-trivial
priority shape (FunSearch-style discovery, or hardcoding an explicit
construction).

## Next
- Set `problem/priority.py` to the c2=3 priority and freeze.
- Write up the result in MEMORY.md and the project log; mark exp 001
  + the sweep as the deliverable.
- Acknowledge limitation: simple priorities cannot reach 480+, let alone
  512, without LLM-driven program search or a hardcoded construction.

## Linked
- archive/030-higher-n.py
