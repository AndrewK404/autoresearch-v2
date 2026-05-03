# res 004 — cycle inheritance tagging + C-007 verification

## What & why
Queue #1 — tag every cycle in `001-cycles.parquet` as `inherited` /
`new` / `gcd_match_but_not_cycle`, then check whether the C-007 lower
bound `n_total ≥ d(b)` and the implicit equality `n_inherited == d(b)`
hold for the a=1 row.

Predicted before dispatch: `n_total ≥ d(b)` would hold (this was C-007's
weaker form). The strong inheritance-equality form was untested.

## Done
Sub-agent built `autoresearch/archive/004-tagger.py`. Algorithm:
1. For each cycle row, compute g = gcd of members.
2. If g > 1 and g | b: divide all members by g, simulate under T_{a, b/g}
   from the resulting smallest member, confirm it's a cycle of (a, b/g)
   with the same shape. Tag `inherited` with `inherited_from_b = b/g`,
   `inherited_scale = g`.
3. Otherwise (g = 1 or g ∤ b) — tag `new`.
4. Sanity row: `gcd_match_but_not_cycle` if step 2 fails (would indicate
   a bug or weird structure).

Outputs:
- `autoresearch/archive/004-inheritance-tags.parquet` — 153 rows with
  added columns
- `autoresearch/archive/004-summary.md` — full per-(a, b) breakdown
- `autoresearch/archive/004-tagger.py`

## Result
n/a (research-only)

Headline:
- **C-007 strong form (n_inherited == d(b)) fails at 10 of 11 (a=1, b)
  cells.** Only b=21 satisfies it.
- **C-007 lower bound (n_total ≥ d(b)) holds at all 11 cells.** Slack
  range 0..2.
- **0 `gcd_match_but_not_cycle` rows** — clean. Every gcd-detected
  inheritance candidate verifies as a true scaled image. Action 003's
  conjugacy framework is internally consistent.
- **64 `new` cycles** across the whole atlas of 153.
- (3, 13) carries 9 new — the bulk of its 10-cycle richness.
- (5, 21) has 2 new + 10 inherited (mostly 3- and 7-scaled images of
  (5, 7) and (5, 3)).
- (5, 9) has 3 new — the agent flags this against my a-priori "small
  L3 cycle is the only new thing" thinking.

## Thoughts
The mismatch in the strong form has a clean reason that I should have
seen up front: under the gcd-based tagging rule, the **base cycle of
(1, b) reachable from seed n=1 has gcd = 1 of members and gets tagged
`new`, not `inherited`.** It's a genuine cycle of (1, b), not a scaling
of anything. So:

- For each divisor d | b with d > 1, there's a d-scaling of (1, b/d)'s
  base cycle, contributing one `inherited` cycle.
- For d = 1, there's no scaling parent — the cycle is "self".
- Therefore n_inherited ≥ d(b) − 1 in general (one inherited per proper
  divisor d > 1).
- And n_total ≥ d(b) since the base cycle adds at least 1.

This is a refinement, not a falsification of the *weak* form. It's a
falsification of the *strong* form I'd written.

The case b=21 is a coincidence: 21 has more inherited cycles than
d(21) − 1 = 3 because (1, 7) and (1, 3) themselves each have multiple
cycles, all of which get scaled into (1, 21).

## Conclusion
*Tentative.* C-007 weak form survives. The strong form is dead and
should be marked falsified. A refined statement should replace it:
**"n_inherited(1, b) ≥ d(b) − 1 with equality when (1, b/d) has exactly
one cycle for each d | b, d > 1."** That's still empirically falsifiable
and structurally interesting — but it doesn't say much beyond
mechanical bookkeeping.

The more interesting question the data raises: **what governs n_new for
(1, b)?** That's the count of base-level non-inherited cycles, which is
where novelty lives. From action 004:

| b | n_new(a=1) |
|---|---|
| 1 | 1 |
| 3 | 1 |
| 5 | 1 |
| 7 | 2 |
| 9 | 1 |
| 11 | 1 |
| 13 | 1 |
| 15 | 2 |
| 17 | 2 |
| 19 | 1 |
| 21 | 2 |

The 1-vs-2 pattern looks like it tracks something — maybe
*the existence of at least one L ≥ 2 cycle of (1, b) on integers
coprime to b*. Worth a dedicated probe.

## Reasoning
- Cross-check vs action 003's conjugacy survey: 0 `gcd_match_but_not_cycle`
  rows confirms that the b-scaling embedding *is* the only nontrivial
  inheritance mechanism in our scope. If there were a hidden conjugacy
  the agents missed, we'd expect to see cycles whose gcd divides b but
  whose scaled image is NOT a cycle of the parent — and we don't.
- (5, 9)'s 3 new cycles (rather than 1) revises C-005: the (1, 7, 11)
  L3 cycle is one of three "new" cycles for (5, 9), not the only one.
  C-005 should be tightened to specifically about (1, 7, 11) and the
  others should be added as separate "new" entries in a new conjecture
  if they're structurally distinct.
- (3, 13)'s 9 new cycles is the headline. Combined with action 005's
  finding that 8 of those have shortcut length 5 with t_period 13, the
  (3, 13) anomaly is starting to look like a **structured family**
  parametrized by halving-vector (k₁..k₅) summing to a constant. C-004
  upgrades to "structured" rather than "anomalous".

## Next
- **CONJECTURES.md updates:**
  - C-007 strong form: status falsified.
  - C-007 weak form: status probed (one falsification attempt run, lower
    bound held).
  - Refined statement C-007′: n_inherited(1, b) ≥ d(b) − 1.
  - C-004: upgrade from "anomaly" to "structured family" pending
    action 005's analysis.
  - C-005: tighten to specifically about the (1, 7, 11) cycle.
- **PREDICTIONS.tsv:** no new prediction needed; this was a conjecture
  scoring, not a registered prediction.
- **MEMORY.md ## Open questions:** add "what governs n_new(1, b)?"
- Wait for action 006 (10× horizon sweep) before making bigger
  decisions; it tests C-001 directly.

## Linked
- autoresearch/archive/004-inheritance-tags.parquet
- autoresearch/archive/004-summary.md
- autoresearch/archive/004-tagger.py
