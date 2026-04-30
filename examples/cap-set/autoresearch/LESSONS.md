# LESSONS

Confirmed lessons grounded in own experience. A lesson lands here only after
≥ 2 keep experiments confirm the same falsifier statement.

## `-|count_of_2 - 3|` is the strongest simple priority across n ∈ [8, 11]

For the fixed greedy in `problem/solve.py`, promoting elements with exactly
three 2's beats every other count-based or pair-based priority we tested
(more than 700 candidates), at every `n` we measured:

- exp 001 — n=8 → 448 (vs. baseline 256, +75%)
- exp 005 — n=9 → 896 (vs. baseline 512, +75%)
- exp 006 — n=10 → 2048 (vs. baseline 1024, +100%)
- exp 007 — n=11 → 4096 (vs. baseline 2048, +100%)

The *constant* target 3 — not `n // 3` — wins for all `n` in this range.
The natural `itertools.product` lex order acts as the intra-cluster
tiebreak; replacing it with any random or structural tiebreak strictly
underperforms (max 287 from 200 random trials).

Context: this lesson applies to the cap-set construction skeleton in
`problem/solve.py` (greedy with priority-based ordering, no rejection
sampling, no backtracking). It does NOT claim that 448 is the maximum
cap at n=8 — known caps reach 480+ via Edel-style constructions and 512
via FunSearch's discovered priority. Only that within the space of
simple, hand-articulable priorities, `-|c2 - 3|` is the local maximum.

## The 448-cap at n=8 is maximal under greedy completion

Two confirming directions:

- exp 001 — after greedy completes with priority `-|c2 - 3|`, zero
  non-forbidden, non-cap elements remain (`archive/018-extend-448.py`).
- ana 004 — random 2-element-removal + re-greedy fill, 200+ trials, all
  return to size 448 (`archive/024-local-search.py`).

Implication: to break 448 with this skeleton, a priority must induce a
**different basin** — most plausibly via LLM-driven program search
(FunSearch) or by hardcoding an explicit construction.

## Sections of larger caps are an effective shortcut to small-n caps

Two confirming directions:

- res 016 — fixing 3 coordinates of the FunSearch 1082-cap at n=9 to
  `{6,7,8}={1,1,0}` yields a 112-cap at n=6 — the proven Potechin max.
  Random / tabu / SLS / ILP at n=6 alone stayed at 96
  (`archive/035-...`, `039-...`, `040-...`).
- exp 017 — using that 112-cap in a 112×20 tensor for n=10 jumped the
  cap from 2164 to 2240, matching the published Tait 2018 lower bound.

Why: the FunSearch n=9 priority encodes structural information that no
pure n=6 priority shape captured. Sectioning is "free" — it costs
nothing once the larger cap is computed — and it pulls a tighter cap
out of the bigger one. Useful pattern: **whenever you need a max cap at
small n and direct priority search is stuck, section a known good cap
at higher n through every fix-k-coords slice.**

## Pellegrino's hyperplane-removal lifts a 112-cap at n=6 to a 45-cap at n=5

Two confirming directions:

- res 018 — taking the 112-cap, viewed as the doubled Hill 56-cap,
  iterating over all PG(5,3) hyperplanes finds 56 with intersection
  size 11 with Hill, and `Hill ∖ hyperplane = 45` projective points
  that lift to a 45-cap in `AG(5,3) = F_3^5`.
- exp 019 — using that 45-cap in a 112×45 tensor for n=11 jumped the
  cap from 4608 to 5040.

Implication: classical projective↔affine constructions scale **down**
just as recursively as the product construction scales up, given an
explicit cap at one good dimension as a seed.

## SLS index discipline: do not cross sorted-list indices with itertools-canonical THIRD tables

Recorded after the false 550-cap result at n=8 (archive/052-...). The
fix is in `archive/053-sls-n8-fixed.py`: keep `elements` in itertools
order when computing the THIRD lookup table; do priority sorting only
inside the priority itself, not by reordering the array. After the fix,
SLS at n=8 cleanly plateaus at 512.

**Why:** `THIRD[i, j] = ((-elements[i] - elements[j]) % 3) @ powers`
canonicalizes to itertools index. If you sort `elements` first and
then use this formula, the value of `THIRD[i, j]` no longer matches
the index of any element in the sorted array, so `blocked[THIRD[i, j]]`
silently flips the wrong bit and the greedy reports caps that don't
verify.

**How to apply:** when memoising third-points, keep the canonical
order. Use a separate `priority_for(idx)` array if you want to walk
elements in priority order — but never index `cap_list` /
`elements_sorted` with `THIRD[…]` directly.
