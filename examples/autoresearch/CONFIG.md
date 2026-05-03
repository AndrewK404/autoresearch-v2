# CONFIG

## Mode
research-only
(no executable eval. Findings live as `Thoughts` / `Conclusion` sections in
`log/NNN-*.md`. Computational sweeps are tools the investigations use; they
write results to `archive/NNN-*` and are not the contract metric.)

## Goal
Build a parameter atlas for the generalized Collatz family `n → (a·n+b)/2^k`
(odd a, b; even branch divides by 2 fully) — classify each variant
(all-converge / has additional cycle / apparently-unbounded up to horizon),
correlate classification with algebraic features, and produce a small set of
falsifiable conjectures of the form "for parameters in region R with property
P, behavior B holds." Negative and null results count if the search is
thorough enough to make them informative.

## Done criterion
- A `README.md` at the project root with a small number of falsifiable
  empirical claims, each with: scope (parameter region it applies to),
  evidence (sweep ranges and what was observed), and falsification record
  (what was tried to break it, what survived).
- The parameter atlas itself in a reusable form (CSV / Parquet + a loader
  script).
- The research log, conjecture ledger, and prediction-vs-outcome record
  produced by the autoresearch run.
- User's confirmation criterion for promoting a finding to `LESSONS.md`:
  the user reviews the conclusion and the falsification attempts and
  explicitly says "this is solid". A conjecture that has only survived its
  initial sweep does not qualify; it must have been challenged at expanded
  horizons or against conjugacy candidates.

## Scope
- Target files: anything under `/Users/andrewkuncevich/vs_code_projects/autoresearch-eval/`
  except `TASK.md` (read-only context — the brief).
- Read-only context: `TASK.md`.
- Forbidden: none. The agent owns the rest of the project tree.

## Constraints
General research discipline (anti-gaming is N/A for research-only):
- Apparent unboundedness up to horizon H is **never** unboundedness in the
  writeup. Every classification carries the explicit (S, H, T) horizon under
  which it was observed.
- Before reporting a parameter region as novel, explicitly check it isn't a
  relabeling of an already-characterized variant via simple substitutions
  (n → λn, n → n+δ, parity-aware affine, swap of branches). The conjugacy
  check is part of the conjecture ledger entry, not optional.
- Conjectures must have stated scope. "All orbits converge" without scope
  is rejected as a deliverable; "for a in {1,3,5}, b odd in [1,21], all
  orbits ≤ 10^4 reach the trivial cycle within H=10^12 and T=10^4 steps"
  is acceptable.
- Predict-then-run: every sweep is preceded by a written prediction in
  the corresponding `log/NNN-*.md` `What & why` section. Surprises (predicted
  vs observed delta) are the primary signal.
- Reproducibility: every result regenerable by a single command. Fixed
  seeds (deterministic for integer iteration; seeds matter only for any
  randomized starting-seed sampling).

## Integrations
- W&B project: not used.
- MLflow / Tensorboard: not used.
- Slack / Discord hooks: not used.
- Status webhooks: not used.
- Notifications / email / pager: not used.
- External secrets / vaults: not used.
- Anything else: not used.

## Concurrency
- Experiments in parallel: n/a (research-only mode)
- Sub-agents in parallel: 4 (research-only default)

## Termination
Unlimited — stop only on explicit user instruction. Plateaus or exhausted
queues trigger strategy escalation (see `SKILL.md §5`), not stop.
