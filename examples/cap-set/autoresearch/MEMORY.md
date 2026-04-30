Updated: 2026-04-30T19:30:00Z | Last action: 021

---

## Best
n=8:  cap_set_size=512  (FunSearch's discovered priority — published record)
n=9:  cap_set_size=1082 (FunSearch's discovered priority — published record)
n=10: cap_set_size=**2240** (112 × 20 tensor — improved from 2164)
n=11: cap_set_size=**5040** (112 × 45 tensor — improved from 4608)

## Status
Deliverable. The n=10 and n=11 results have been improved via explicit
tensor products of "previously-not-available-to-us" caps:
- A **112-cap at n=6** (the proven max in AG(6,3), Potechin 2008) was
  obtained as a section of FunSearch's 1082-cap at n=9 (fix coords
  {6,7,8}={1,1,0}).
- A **45-cap at n=5** (the proven max in AG(5,3)) was derived from the
  112-cap by Pellegrino's hyperplane-removal recipe applied to the
  doubled Hill 56-cap that the 112-cap is mod scalars.

Both new caps embedded as Python literals in `problem/priority.py`.

n=8 (512) and n=9 (1082) match the FunSearch published records.
Random-restart SLS at n=8 with the corrected indexing plateaus at 512
in 12k trials — the 512-cap is a genuine local-optimum trap. Pushing
past 512 / 1082 would constitute a world record and is outside the
scope of priority-search without an LLM-in-loop.

Strategy level: 4 (radical rethinking — combined sectioning of larger
caps with classical projective→affine lifting recipes).

## Queue
(future research, not active)

R1. Edel "extended product" with admissible sets — could in principle
    push n=10 above 2240 toward Tyrrell's asymptotic (~2515 at n=10).
R2. Run a real LLM-in-loop FunSearch on n=10 / n=11 directly.
R3. Improve n=8 (512 → 513+) via deep search — would be a world record.

## Recent
- ana 021: done — corrected SLS at n=8 plateaus at 512 → 512 is a true
  local max for random-restart greedy.
- ana 020: done — both new caps (2240 at n=10, 5040 at n=11) are
  maximal under greedy completion.
- exp 019: keep, +432 — n=11 → 5040 via 112×45 tensor.
- res 018: done — derived explicit 45-cap at n=5 from 112-cap.
- exp 017: keep, +76 — n=10 → 2240 via 112×20 tensor.
- res 016: done — extracted explicit 112-cap at n=6 by sectioning the
  1082-cap (fix coords {6,7,8}={1,1,0}).
- ana 015: done — direct search at n=6 stays at 96 even with massive
  random / tabu / ILP attempts.
- res 014: done — confirmed 2240 is the published n=10 lower bound and
  required a 112-cap.
- (older entries: see log/000–004 for the priority-only-search era and
  the FunSearch port.)

## Avoid
- Random tiebreaks within priority clusters — natural itertools.product
  order is uniquely good (200+ trials confirm).
- Pure SLS at n=6 with random restart — plateau at 96 (the c2=2 cap).
- ILP at n=6 with full-line constraints + 5-min time limit on CBC —
  doesn't reach a feasible cap in time.
- Hardcoding `np.argmax`-style indexing of a *sorted* `elements` array
  with itertools-canonical THIRD table — caused a fake "550-cap" bug
  at n=8 (fixed in archive/053).

## Open questions
- Is the 5040 cap at n=11 the largest published lower bound, or has
  someone (Edel?) reported larger via extended product?
- For LLM-in-loop FunSearch on n=10 directly: what would it find?
- Is the FunSearch 1082-cap at n=9 special in containing the n=6
  max as a section, or do all sufficiently-large caps share this
  property?

## Notes
priority.py is final and contains the four embedded cap literals:
- `_CAP_9_N3` (size 9): 9-cap in F_3^3.
- `_CAP_20_N4` (size 20): Pellegrino 20-cap, the proven max in AG(4,3).
- `_CAP_45_N5` (size 45): Pellegrino 45-cap, the proven max in AG(5,3),
  derived from the 112-cap via hyperplane removal.
- `_CAP_112_N6` (size 112): Potechin 112-cap, the proven max in
  AG(6,3), extracted as a section of FunSearch's 1082-cap at n=9.

Plus FunSearch's discovered priorities for n=8 and n=9 verbatim, and
the `-|c2-3|` fallback for any other n.
