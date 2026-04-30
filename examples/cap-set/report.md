# Cap-set construction in F₃ⁿ via autoresearch

The greedy skeleton is fixed: `solve(n)` enumerates all 3ⁿ vectors in
F₃ⁿ, sorts them by `priority(element, n)` descending, and adds each one
that does not complete a 3-AP with two already-picked vectors. The
agent edits only `priority(element, n)`. Skeleton from FunSearch
(Romera-Paredes et al., *Nature* 625, 468–475, 2023).

## 1. Achievements

All four results pass the official `verify_cap_set`.

| n  | autoresearch | how                                  | published landscape                                        |
|----|-------------:|--------------------------------------|------------------------------------------------------------|
| 8  | **512**      | FunSearch's discovered priority      | 512 is the largest cap known (FunSearch 2023; X-evolve 2025 found three different 512-caps but did not exceed). Upper bound 771 (Tait 2018). |
| 9  | **1082**     | FunSearch's discovered priority      | 1082 is the largest cap known (Edel-style product, found pre-FunSearch; FunSearch's evolved program rediscovered the same value). Upper bound 2070. |
| 10 | **2240**     | 112-cap (n=6) × 20-cap (n=4)         | 2240 is the long-standing classical lower bound (Versluis 2017; product of Potechin's 112-cap and Pellegrino's 20-cap). The exact maximum is open: 2240 ≤ max ≤ 5619. |
| 11 | **5040**     | 112-cap (n=6) × 45-cap (n=5)         | 5040 = product of two proven-max caps (Potechin 2008 at n=6; Pellegrino-style at n=5). No widely-cited tighter explicit cap at n=11 in the literature we surveyed. |

We did **not** beat any published record. The contribution is the
mechanical assembly of four published constructions that no single
priority function on its own gives:

1. **Port** FunSearch's discovered priorities for n=8 and n=9 verbatim
   from the [official notebook](https://github.com/google-deepmind/funsearch/blob/main/cap_set/cap_set.ipynb)
   (Apache-2.0 / CC-BY-4.0). These give 512 and 1082 directly.
2. **Section** FunSearch's 1082-cap at n=9 to recover an explicit
   112-cap at n=6: fixing coordinates {6,7,8} = {1,1,0} cuts a slice
   of exactly 112 elements that forms a valid cap — the proven max
   in AG(6,3) (Potechin 2008). Hours of direct search at n=6 (random
   restart, tabu, ILP) had stayed at 96.
3. **Lift** the 112-cap to a 45-cap at n=5 by Pellegrino's
   hyperplane-removal recipe: the 112-cap mod scalars is the Hill
   56-cap in PG(5,3) (Hill 1973); 56 of the 364 hyperplanes of
   PG(5,3) meet Hill in 11 points; pick one and the affine coset
   `{v : a·v = 1}` lifts to 45 points in F₃⁵.
4. **Tensor** to lift 112 × 20 → 2240 at n=10 and 112 × 45 → 5040 at
   n=11. Both new caps are maximal under greedy completion (zero
   addable elements remain after the greedy finishes).

The crisp lesson, recorded in `autoresearch/LESSONS.md`: **when direct
priority search at small n is stuck, section a known good cap at
larger n through every fix-k-coords slice.** A 112-cap at n=6 lives
inside the 1082-cap at n=9; the agent had been hunting for it locally
for hours.

## 2. Agent trace

A single Claude Code session over roughly **6 hours of wall clock**
across two prompts: an initial run that capped at 448 / 896 / 2048 /
4096 with the simple priority `-|c2 − 3|`, then a second pass after
the user pointed at the FunSearch source. Eval is cheap (n=8 ≈ 0.1 s,
n=11 ≈ 9 s) so iteration was rapid.

**File outputs** (in `autoresearch/`):

- `log.tsv`: 22 actions (1 baseline + 21).
- `log/`: 6 detailed action notes, one per "thinking unit"
  (000-baseline, 001-c2-target, 002-deep-search, 003-n-sweep,
  004-funsearch-port, 005-section-and-derive).
- `archive/`: **63 entries** — 54 Python scripts (priority sweeps,
  ILP attempts, SLS, sectioning tools) and 9 cap dumps. Total 328 KB.
- `MEMORY.md` and `LESSONS.md` were rewritten end-to-end three times
  as the strategy level escalated.

**Tool-call shape**:

- `Bash` was the workhorse — inline Python for priority sweeps and
  local search; `run_in_background` for the longest searches (random
  restart at n=6 for ~3 min; CBC ILP for ~6 min).
- `WebSearch` + `WebFetch` were load-bearing twice. First, to
  discover that FunSearch's priorities are open-source (this is
  what jumped n=8 from 448 to 512). Second, to verify the
  literature landscape after the user asked whether anything beats
  512 / 1082 (X-evolve 2025 only matched; Tyrrell 2023 improves
  asymptotic bounds, not specific small n).
- `Edit` / `Write` on `problem/priority.py` — the only file modified
  in `problem/`. The skeleton (`solve.py`, `eval.py`,
  `BACKGROUND.md`) was never touched.
- `TaskCreate` / `TaskUpdate` for sub-goals: scaffold, baseline,
  autoresearch loop, find 112-cap, find 45-cap, push further.

**Two key decision points**, visible in `log/` reasoning sections:

- After ~25 hand-shaped priorities all plateaued at 448 at n=8, the
  agent escalated to strategy level 4 (the SKILL's "is the metric
  right? is the problem framed correctly?" tier) and pivoted to a
  literature search instead of more local tweaks. WebFetch on the
  FunSearch GitHub was the unlock.
- After hours of failed direct-search for the 112-cap at n=6, the
  realisation that the 1082-cap at n=9 *contains* it as a section
  was a single-shot win — 2268 candidate slices of the 1082-cap
  enumerated in seconds, exactly one yields the 112-cap.

**One bug worth recording** (now in `LESSONS.md`): an early SLS at
n=8 reported a 562-cap that didn't `verify_cap_set`. Cause:
sorting `elements` by priority and then indexing the
itertools-canonical THIRD lookup table with sorted-array indices —
the indices stop matching, the wrong bits flip, the greedy reports
a non-cap as a cap. Fixed by keeping `elements` in itertools order
and walking it in priority order via a separate priority array.
After the fix, SLS at n=8 cleanly plateaus at 512 — confirming 512
is a genuine local-optimum trap for random-restart greedy.
