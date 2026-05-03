# res 000 — kickoff

## What & why
Activate the research-only contract for the generalized Collatz parameter
atlas. The brief (TASK.md) is concrete: sweep parameter sets of the family
`n → (a·n+b)/2^k` (and structural variants), classify each variant
empirically (all-converge / has additional cycle / apparently-unbounded up
to horizon), correlate classification with algebraic features, and produce
a small set of falsifiable conjectures with explicit scope. The autoresearch
loop is the right shape for this: predict → run → compare → log delta →
escalate, with surprises as the primary signal.

## Done
- Interview consolidated to 4 questions; user picked the recommended option
  on each.
- `autoresearch/` directory scaffolded with all required files.
- `CONFIG.md` written: research-only mode, goal stated, done criterion in
  terms of `README.md` + reusable atlas + falsification record, constraints
  including the predict-then-run rule and the conjugacy-check-before-novelty
  rule.
- `RESUME.md` written: initial sweep scope (a ∈ {1,3,5,7},
  b ∈ {1,3,...,21}), horizons (S=10⁴, H=10¹², T=10⁴), bootstrap commands.
- `MEMORY.md` seeded with 3 Queue items: opening atlas, analytic
  trivial-cycle catalog, conjugacy survey.
- Bootstrap executed: Python 3.12.7 venv, `numpy pandas pyarrow gmpy2`
  installed. `gmpy2 2.3.0` works (no fallback needed).
- User confirmed contract with "ok". Contract is now frozen.

## Result
n/a (research-only)

## Thoughts
Pushback I'd record on the brief itself, framing the work:

- *"Apparent unboundedness up to N is not unboundedness."* Agreed and
  enforced in CONFIG. But the more subtle failure mode is the inverse:
  *apparent convergence up to N is not convergence either.* A sweep that
  shows all seeds in [1, 10⁴] reach the trivial cycle within H=10¹² is
  evidence of a pattern, not of a theorem. The atlas should report both
  arms with equal honesty.
- *Conjugacy is load-bearing.* The 3x+1 family has obvious symmetries
  (multiply b by an odd unit, etc.) that will create spurious "novelty" if
  we're not careful. I want a normal form *before* claiming any region is
  new — that's why the conjugacy survey is Queue #3, not deferred.
- *The deliverable is conjectures with scope, not tables.* I'd add: and
  the predictions logged *before* each sweep are the signal that
  distinguishes "we found a pattern" from "we noticed the pattern after
  the fact." The latter is cheap; the former is what makes the conjecture
  ledger worth anything.
- *"Even one new candidate tractable cousin of Collatz would be a real
  contribution."* This is the right ambition level. It also tells me that
  *anomalies* (a (a,b) pair where the dynamics look unusually well-behaved
  or unusually wild) deserve more effort than the bulk of the atlas. The
  atlas exists to surface them; the conjectures exist to characterize
  them.

What I'll do first:

1. Dispatch a sub-agent to build the opening sweep tool
   (`archive/001-sweep.py`) and run it on the tight scope. Output: a tidy
   classification table + per-variant cycle inventory + per-variant
   max-value histograms. Takes a single agent run.
2. In parallel, dispatch a researcher for the analytic trivial-cycle
   catalog (Queue #2): for each (a,b) in scope, derive the fixed-point
   cycle of `(a·n+b)/2^k = n` (and short cycles of length 2, 3) by hand
   so we know what "trivial" looks like before sweep results land.
3. In parallel, dispatch a researcher for the conjugacy survey (Queue
   #3): enumerate substitutions that map (a,b)-variants to each other,
   build a normal form.
4. When sweep results return, integrate against the analytic catalog. Any
   (a,b) where the sweep finds a cycle the catalog does not predict is a
   surprise — exactly the signal we're looking for.

Predictions before the first sweep (so we can score surprise after):

- a=1: trivial. All seeds reach the b-fixed-cycle quickly. No surprises.
- a=3, b=1 (classical Collatz): all seeds in [1, 10⁴] reach 1.
- a=3, b=3: equivalent to classical via n → n/3 substitution if n
  divisible by 3; otherwise diverges from {n: 3 ∤ n}. *(Possibly conjugate
  — flag for survey.)*
- a=3, b=5: classical literature suggests at least one extra cycle exists.
  Expect: not all seeds reach the trivial cycle.
- a=5, b=1: known empirically to have orbits unbounded up to large N for
  some seeds. Expect: at least one seed hits the H bound or T bound.
- a=5, b=3, a=5, b=5, ..., a=7, b=*: less tabulated. Expect ≥ 2 (a,b)
  pairs to show "additional cycle" classification.

These are written *before* running. After the sweep returns, the delta
between predictions and observation goes into
`log/00X-experiment-opening-sweep.md ## Reasoning`.

## Conclusion
*Tentative.* Setup is correct; the framing is sound. The work to come is
mechanical for the opening atlas and judgement-heavy for the conjugacy and
conjecture phases. The autoresearch loop is well-matched.

## Reasoning
The contract is operable: research-only mode + 4 sub-agent concurrency +
unlimited termination matches the open-ended nature of an empirical atlas.
The constraint about predict-then-run is the discipline that makes this
distinguishable from "running a lot of code and looking at the output."

## Next
- Dispatch sub-agent #1 (general-purpose): build `archive/001-sweep.py`,
  run the opening sweep, report classification table + cycle inventory.
- Dispatch sub-agent #2 (general-purpose): write the analytic trivial-cycle
  catalog to `archive/002-trivial-cycles.md`.
- Dispatch sub-agent #3 (general-purpose): conjugacy survey to
  `archive/003-conjugacy-survey.md`.
- Main keeps thinking on Queue #4-onwards (atlas storage format,
  divisor-c expansion, prediction-vs-outcome ledger structure).

## Linked
- (no archive artefacts yet — kickoff is a state change only)
