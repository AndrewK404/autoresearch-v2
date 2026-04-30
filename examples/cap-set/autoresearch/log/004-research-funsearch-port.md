# res 008 + exp 009-012 + res 013-014 — port FunSearch and tensor up

## What & why
After hitting 448 with `-|c2-3|`, we plateaued. The user prompted us to
look online for better results. Hypothesis: FunSearch's 2023 published
priority for n=8 (which produces 512) is open-source on GitHub, and its
priority for n=9 (which produces 1082) is too. If so, we can port them
verbatim and get exact records at n=8, n=9.

For n=10 and n=11 the same source doesn't ship priorities, but the
classical "product of caps" theorem (Edel) says cap_a × cap_b is a cap
in F_3^{a+b} of size |cap_a| · |cap_b|. So:

- n=10 = 9 + 1: 1082 × 2 = **2164**.
- n=11 = 8 + 3: 512 × 9 = **4608** (using a hand-found 9-cap in F_3^3).

## Done
- WebSearch + WebFetch: located
  `github.com/google-deepmind/funsearch/blob/main/cap_set/cap_set.ipynb`
  and extracted the two discovered priorities and the explicit
  `build_512_cap()` construction.
- Ported `_priority_n8` and `_priority_n9` verbatim into
  `problem/priority.py` (Apache-2.0 / CC-BY-4.0 license preserved).
- Ran `archive/031-find-9cap-n3.py` to brute-force one explicit 9-cap
  in F_3^3 (`{(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1),
  (1,1,2), (1,2,2), (2,1,2)}`).
- Implemented n=10 dispatch: push e[9]=2 to -∞ and use the n=9 priority
  on e[:9]. Implemented n=11 dispatch: restrict e[8:] to the 9-cap and
  use the n=8 priority on e[:8].
- Verified all four eval runs end with `STATUS: correct`.

## Result
| n  | priority           | cap_set_size | prior best in our search | published landmark         |
|----|--------------------|--------------|--------------------------|----------------------------|
| 8  | FunSearch n=8      | **512**      | 448 (`-|c2-3|`)          | 512 (FunSearch 2023; X-evolve 2025 matched) |
| 9  | FunSearch n=9      | **1082**     | 896 (`-|c2-3|`)          | 1082 (known pre-FunSearch via product) |
| 10 | 1082 × {0,1}       | **2164**     | 2048 (`-|c2-3|`)         | 2240 (Tait 2018 table, via 112 × 20) |
| 11 | 512 × 9-cap        | **4608**     | 4096 (`-|c2-3|`)         | (no widely-cited specific value; ≥ 2.218^11 ≈ 5800 asymptotic) |

## Reasoning
After the search confirmed the priorities are published verbatim, it
was a port not a discovery. We hit the n=8 and n=9 records exactly.

The PROMPT's success threshold (≥ 512 at n=8) is **achieved**.

For n=10 and n=11 the FunSearch repo doesn't ship priorities, but
tensor product caps are a textbook construction (Edel) and easy to
encode as a priority: restrict one factor coordinate-block to a known
cap and apply the existing priority to the other factor. Mechanism:

- n=10: priority returns `-∞` for any vector with a 2 in coord 9, and
  otherwise `_priority_n9(e[:9])`. The greedy then picks every element
  of `cap_n9 × {0}` and `cap_n9 × {1}` (order-independent because all
  AP completions across the {0,1} factor land in the {2}-block which
  is excluded).
- n=11: priority returns `-∞` unless `e[8:] ∈ CAP_9_N3`, otherwise
  `_priority_n8(e[:8])`. Same logic: `cap_n8 × cap_9_n3` is a cap of
  size 512·9 = 4608.

For n=10, the published lower bound 2240 = 112·20 (a 112-cap in F_3^6
times a 20-cap in F_3^4) is **strictly better** than our 2164. We
attempted to find a 112-cap in F_3^6 by random-restart greedy and
~4000 quadratic-form / pair-feature priorities — the ceiling stayed at
96 (archive/034-search-n6-112.py). Without an explicit 112-cap (the
proven max is 112; Edel's website only ships the projective version),
we cannot replicate the 2240 record. This is the same kind of barrier
we hit at n=8 with `-|c2-3|` ≤ 448 before porting FunSearch's
priority — finding the cap requires an LLM-driven program search
loop or a hand-derived construction we don't have to hand.

For n=11, no widely-cited specific record stands out in the
literature; the asymptotic Tyrrell bound ≥ 2.218^n ≈ 5800 at n=11 is
implied by recursive constructions on much larger admissible sets,
not by a single explicit cap of that size. Our 4608 is the
straightforward tensor product 512·9 and is the largest we can build
from the explicit caps we have.

## Online research summary
- **OEIS A090245**: known exact values are 1, 2, 4, 9, 20, 45, 112 (for
  n=1..7); the entry has not been extended for n=8 because the exact
  max remains open.
- **FunSearch (DeepMind, Nature 2023)**: introduced the n=8 record of
  512 (improving Edel's 480/496). Their n=9 priority matches the
  pre-existing 1082 product construction.
- **X-evolve (arXiv 2508.07932, Aug 2025)**: matched FunSearch's 512
  at n=8 (found three distinct 512-caps), improved the asymptotic
  lower bound on the cap-set capacity from 2.2202 to 2.2203 via
  larger admissible sets at n=24, 27 — but **did not** improve the
  explicit cap size at n=8 or n=9.
- **Generative Modeling for Mathematical Discovery (arXiv 2503.11061,
  Mar 2025)**: ran 8 LLMs through FunSearch on cap set; max achieved
  was 448, none reached 512 — confirming the difficulty.
- **Tyrrell, "New Lower Bounds for Cap Sets" (Discrete Analysis 2023)**:
  improves the asymptotic bound to ≥ 2.218^n via admissible-set
  recursion; doesn't ship explicit small-n caps.
- **Edel's tables**: list lower bounds for projective caps PG(k-1,3),
  not for affine; the proven max in AG(6,3) is 112 (Potechin 2008)
  but the explicit 112-set is not published in plain-text form on
  Edel's site.

So: as of late 2025, **no public source has a cap larger than 512 at
n=8 or larger than 1082 at n=9**. Our priority.py now matches both.

## Next
- This is the deliverable. Set priority.py as final.
- If we ever get an explicit 112-cap in F_3^6, we could push n=10
  from 2164 to 2240. Lighter open question; not on the critical
  path of the PROMPT.

## Linked
- archive/cap_set.ipynb (FunSearch official notebook contents)
- archive/031-find-9cap-n3.py (explicit 9-cap in F_3^3)
- archive/034-search-n6-112.py (failed search for 112-cap at n=6)
- problem/priority.py (final priority)
