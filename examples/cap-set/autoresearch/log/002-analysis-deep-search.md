# ana 002 — deep priority search around 448

## What & why
Many priority families had been tried with no lift past 448. Goal: do one
broad, programmatic sweep across the priority landscape so we can claim
the ceiling robustly before escalating.

## Done
Across archive/001–029-*.py, evaluated **on the order of 700+** distinct
priority candidates spanning:
- single-feature targets (c0, c1, c2 alone, weighted/non-weighted)
- multiset-class indicators (every `(c0, c1, c2)` partition of 8)
- pair-feature priorities (`pair_eq`, `pair_zero_sum`, `pair_diff_idx`,
  with positive and negative weights)
- triple-feature priorities (counts of zero-sum, all-equal, all-distinct
  triples)
- quadratic forms `x^T A x mod 3` for fixed and random `A`
- linear forms `a^T x mod 3` for many `a`
- index-weighted polynomials in coordinates
- sub-cap counts (number of 3-tuples in a 9-cap at n=3 / 4-tuples in the
  20-cap at n=4)
- product / tensor encodings (`cap_n4 × cap_n4 = 400` at n=8, etc.)
- 200 random-restart greedies (no priority bias) → max 272
- 200 random-tiebreak greedies inside the c2=3 cluster → max 287

## Result
- No priority candidate exceeded 448.
- Several cluster-class priorities reproduce 448 exactly: `-abs(c2-3)`,
  `-(c2-3)^2`, "c2 in {2,3,4} graded", `c2-target with c2=3 prefix`.
- Several priorities reach 384 (e.g. `c2 ∈ {2,3,4}` flat) or 400
  (cap_n4 tensor).
- The natural itertools.product lex order *within* the c2=3 cluster is
  a strong attractor: every random tiebreak inside that cluster
  underperforms it (max 287 vs 448).

## Reasoning
The 448-cap sits at a deep local maximum of the cap-set landscape under
this skeleton. Random restarts can't reach it (too many wrong local
minima below). Local moves around it can't grow it (we exhaustively
checked: zero non-forbidden, non-cap elements remain after greedy
completes — the cap is **maximal** in the strong sense). 2-out swaps with
re-greedy fill all return to 448.

To get past 448 with this skeleton, we'd need a priority that **encodes
a different basin** — most plausibly a hand-derived FunSearch-style
priority discovered by an LLM-driven program search loop, or a
hardcoded explicit construction (e.g. an Edel 480/496-cap embedded as
a precomputed lookup). Without an LLM in the loop and without an
explicit closed-form 480+ construction memorized, none of the priority
*shapes* we can articulate from theory beats 448.

This is consistent with the framing in BACKGROUND.md: pre-FunSearch the
explicit best at n=8 was 480/496 (Edel-Bierbrauer), and the 512 came
specifically from FunSearch's discovered priority — a non-obvious,
non-standard function.

## Next
- Mark 448 as our final keep at n=8 and update priority.py with the
  best priority found.
- Sweep n=10 and n=11 with the same priority (per PROMPT) to see how the
  c2-target shape scales.
- Document the gap (-48 vs Edel, -64 vs FunSearch) honestly.

## Linked
- archive/000-batch-tester.py (re-used by all sweeps)
- archive/001-sweep-basic.py, 002-sweep-c2.py, 003-sweep-combine.py,
  004-sweep-rich.py, 005-sweep-multi.py, 006-funsearch-style.py,
  007-quad-forms.py, 008-pattern-counts.py, 009-product-structure.py,
  010-random-perturb.py, 012-c2-orderings.py, 013-pattern-first.py,
  014-novel-features.py, 015-exotic.py, 020-orthogonal.py,
  021-symmetric.py, 022-funsearch-attempts.py, 023-funsearch-pub.py,
  024-local-search.py, 025-search-n6.py, 026-massive-sweep.py,
  027-final-attempt.py, 028-subcap-priority.py, 029-deep-search.py
- archive/011-cap-448.txt — the actual 448-cap
- archive/018-extend-448.py — proof of cap maximality
- archive/019-random-restart.py — random restart distribution
