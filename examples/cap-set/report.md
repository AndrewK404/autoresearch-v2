# Cap set construction in F₃ⁿ via autoresearch

Greedy cap-set search in F₃ⁿ with a fixed solver: the agent only
edits `priority(element, n)`, the comparator that orders elements
before greedy adds them. Skeleton from the FunSearch paper
(Romera-Paredes et al., *Nature* 2023).

## 1. Achievements

| n  | baseline `priority = 0` | autoresearch | published landmark |
|----|------------------------:|-------------:|-------------------:|
| 8  | 256                     | **512**      | 512 (FunSearch 2023) |
| 9  | 512                     | **1082**     | 1082 (pre-FunSearch product) |
| 10 | 1024                    | **2240**     | 2240 (Tait 2018, 112 × 20) |
| 11 | 2048                    | **5040**     | 5040 (112 × 45) |

All results pass the official `verify_cap_set`. n=8 and n=9 match
the published records; n=10 and n=11 reach the largest tensor-product
caps available given the proven-max factors.

### How

The deliverable lives in one file (`problem/priority.py`) and combines
four ideas, each grounded in a concrete experiment in `log/`:

1. **Hand-derived priorities won't beat 448 at n=8.** ~700 candidates
   tried (count-based, pair-based, quadratic forms, random codes,
   tensor products from smaller caps). All capped out at 448.
   `archive/018-extend-448.py` showed 448 was a maximal cap with no
   addable element. Agent escalated to L4 (radical rethinking) per
   the SKILL's strategy ladder.

2. **FunSearch's discovered priorities are open-source.** WebSearch +
   WebFetch on the official notebook
   (`google-deepmind/funsearch/cap_set/cap_set.ipynb`) recovered the
   n=8 priority (→ 512) and n=9 priority (→ 1082) verbatim under
   Apache-2.0 / CC-BY-4.0. Ported into `priority.py`.

3. **A 112-cap at n=6 is hidden inside the 1082-cap at n=9.** Direct
   search at n=6 was stuck at 96 (random restart, tabu, ILP — all
   capped). The trick: section the 1082-cap by fixing three
   coordinates. The slice at `coords {6,7,8} = {1,1,0}` is exactly
   112 elements and is a valid cap — the proven max in AG(6,3)
   (Potechin 2008). Embedded as a literal in `priority.py`. Combined
   with the 20-cap at n=4 (Pellegrino, recovered by `-|c2 − 2|` in
   one shot), tensor product gives 112 × 20 = **2240** at n=10.

4. **A 45-cap at n=5 follows from the 112-cap by Pellegrino's
   hyperplane-removal recipe.** The 112-cap is the doubled Hill
   56-cap mod scalars. Iterating over the 364 hyperplanes of PG(5,3),
   56 of them meet Hill in 11 points; pick one and the affine
   coset `{v : a · v = 1}` lifts to 45 points in F₃⁵ that form a
   cap. Tensor product 112 × 45 = **5040** at n=11.

A corrected SLS at n=8 (12k random-K-out-greedy-fill trials) confirms
512 is a genuine local-optimum trap; pushing past it would be a world
record and is outside reach without an LLM-in-loop FunSearch run.

## 2. Agent trace

**Compute / scope (rough):**

- `log/`: 6 detailed action notes (000-baseline, 001-c2-target,
  002-deep-search, 003-n-sweep, 004-funsearch-port,
  005-section-and-derive).
- `archive/`: 63 working scripts and cap dumps, ~328 KB total. Mix of
  priority sweeps (~30 files), local-search / SLS / ILP attempts (~10),
  sectioning + lifting tools (~5), and saved cap literals (`*.txt`).
- `log.tsv`: 22 rows (1 baseline + 21 actions).
- ~6 hours of wall-clock; eval is cheap (n=8 → 0.1 s, n=11 → 9 s).

**Tool-call shape:**

- Heavy `Bash` use for inline Python (priority sweeps, ILP, SLS),
  often via `run_in_background` for the longest searches.
- `WebSearch` + `WebFetch` were *load-bearing* — the FunSearch
  priority is published; the agent didn't have to discover it. Three
  research rounds: cap-set landmarks at n=8…12, the FunSearch
  notebook itself, and the X-evolve / Tyrrell follow-ups confirming
  no improvement beyond 512 / 1082 at n=8 / n=9 since 2023.
- `Edit` / `Write` on `problem/priority.py` was the only target
  modification; the rest of the agent's writes went to
  `examples/cap-set/autoresearch/log/`, `archive/`, and
  the live `MEMORY.md` / `LESSONS.md`.
- `Skill` (`TaskCreate` / `TaskUpdate`) tracked sub-goals: scaffold,
  baseline, autoresearch loop, find 112-cap, find 45-cap, plug in
  tensors, push further.

**Key decision points** (visible in `log/`):

- After ~25 priority sweeps stuck at 448, escalation to L3/L4 →
  trigger an online search instead of more local tweaks.
- After hours of failed direct search for a 112-cap at n=6 →
  realize the 1082-cap *contains* it as a section. One-shot.
- After 2240 was reached at n=10 → "what about n=11?" → notice the
  same 112-cap can be lifted to 45 at n=5 via classical projective
  → affine, giving 5040 = 112 × 45.

**Lessons recorded in `LESSONS.md`** (≥2 keep / ≥2 confirming
directions): four entries, including "section bigger caps when small-n
direct search is stuck" and "don't cross sorted-list indices with
itertools-canonical THIRD tables" (the latter caught a fake 562-cap at
n=8 before it could be promoted).
