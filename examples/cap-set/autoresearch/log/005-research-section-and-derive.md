# res 016 + exp 017-019 — break 2164 and 4608 via sectioning

## What & why
User asked us to keep iterating until we improve our previous score. The
realistic targets:
- n=10: 2164 → 2240 (= 112 · 20, Tait 2018 lower bound)
- n=11: 4608 → 5040 (= 112 · 45, the maximum simple-product cap)
- n=8 / n=9 improvements would be world records — much harder.

Both improvements at n=10 and n=11 require an explicit 112-cap in
F_3^6 (the proven max, Potechin 2008). Earlier random / tabu / SLS
search at n=6 plateaued at 96.

## Done
1. **n=6 112-cap by sectioning** (archive/046-section-1082.py). Took
   FunSearch's 1082-cap at n=9 and tried every "fix three coordinates
   to a fixed value" section. Most are far below 112 but
   `fix={6,7,8}={1,1,0}` yields exactly 112. Verified valid.
2. **n=5 45-cap by hyperplane removal** (archive/049-derive-45cap.py).
   The 112-cap at n=6 is the doubled Hill 56-cap (each projective
   point appears as both `v` and `2v`). Iterating over the 364
   hyperplanes of PG(5,3), found 56 hyperplanes that meet Hill in
   exactly 11 points. Picked one (`a = (0,0,1,0,1,1)`); the 45 Hill
   points with `a · v = 1` form an affine 45-set on the 5-dim coset
   `{v : a·v = 1}`. Projecting away the leading nonzero coordinate of
   `a` lands these 45 in F_3^5, and they form a valid cap. This is
   Pellegrino's classical recipe.
3. **Updated priority.py**:
   - `n == 10`: `priority = 1` if `e[:6] in CAP_112` and `e[6:] in CAP_20`,
     else `-∞`. Greedy completes the full 112×20 = 2240.
   - `n == 11`: `priority = 1` if `e[:6] in CAP_112` and `e[6:] in CAP_45`,
     else `-∞`. Greedy completes 112×45 = 5040.
4. **Verified** all four caps via the official eval (which runs
   `verify_cap_set`):
   - n=8 → 512 (unchanged, FunSearch).
   - n=9 → 1082 (unchanged, FunSearch).
   - n=10 → **2240** (was 2164; +76).
   - n=11 → **5040** (was 4608; +432).
5. **Maximality** of the new caps confirmed (archive/050-...): zero
   non-forbidden elements remain after greedy completes at n=10 and n=11.
6. **Pushed n=8** with a corrected SLS using the right index-table
   (archive/053-sls-n8-fixed.py). 12k random-K-out-greedy-fill trials
   all return 512 — 512 is a genuine local max under random restart.
   No world-record improvement at n=8.

## Result
| n  | before        | after  | improvement | published landmark           |
|----|---------------|--------|-------------|------------------------------|
| 8  | 512 (FunSearch) | 512  | 0           | 512 (FunSearch 2023; tight)  |
| 9  | 1082 (FunSearch) | 1082 | 0          | 1082 (FunSearch 2023; tight) |
| 10 | 2164 (1082×2) | **2240** | +76     | 2240 (Tait 2018, 112×20)     |
| 11 | 4608 (512×9)  | **5040** | +432    | 5040 (112×45 product)        |

## Reasoning
The breakthrough was realizing that we don't need to *search* for the
112-cap at n=6 — we already had it implicitly. FunSearch's 1082-cap
at n=9 contains the 112-cap as a section. Checking all C(9,3)·3³ = 2268
possible "fix-three-coords" sections of a 1082-element cap takes a few
seconds, and one of them (only one, in fact) matches the proven max of 112
elements forming a valid cap. The 1082 is large enough that it
"captures" the n=6 max as a slice.

Once we have the 112-cap, the standard projective lifting trick
(`{v, 2v}` pairs ↔ 56 projective points = Hill cap) gives us
Pellegrino's 45-cap at n=5 by removing a hyperplane. Both are
classical recipes; the only thing computational was finding the right
section and the right hyperplane.

For n=8 and n=9, both equal the FunSearch records, and the SLS
experiment confirms 512 at n=8 is at least a local-optimum trap for
random-restart greedy. Improving them would be a real world record;
we don't have the LLM-driven search machinery to attempt that here.

## Next
- This is the new deliverable. priority.py is final.
- Open avenue if more time were available: Edel-style "extended
  product" with admissible sets — could potentially push n=10 above
  2240 toward the Tyrrell asymptotic (~2515 at n=10).

## Linked
- archive/046-section-1082.py + archive/046-cap-n6-112.txt
- archive/049-derive-45cap.py + archive/049-cap-n5-45.txt
- archive/050-extend-2240-5040.py (maximality check)
- archive/053-sls-n8-fixed.py (n=8 cannot be improved by random restart)
- problem/priority.py (final, contains all explicit caps as literals)
