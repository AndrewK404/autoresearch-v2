# Project: Generalized Collatz dynamics — a parameter atlas

## Background

The original Collatz problem is hopelessly hard, but the broader family of maps — `n → an+b` for odd n, `n → n/c` for even n, plus a few structural variants — has lots of computable behavior at small parameters and no comprehensive empirical catalog. Conway's result (that this family is Turing-complete in general) guarantees there's structure to find. Number theorists genuinely use catalogs of this shape; the autoresearch sweet spot is exactly the kind of systematic enumeration humans find tedious.

## What the work consists of

Sweep parameter sets, classify each variant empirically (all-converge to known cycles, has additional cycle, has orbit unbounded up to N), correlate classification with algebraic features (residues mod small primes, growth rate of the average map, etc.), and propose conjectures of the form "for parameters in region R, behavior B holds." Maintain an open conjecture log and try to falsify your own claims by extending search ranges.

## What success looks like

A parameter atlas with a handful of falsifiable conjectures, ideally including some that point to variants worth attacking theoretically. Even one new candidate "tractable cousin" of Collatz would be a real contribution.

## Methodology notes for the agent

This is an autoresearch-v2 run. The loop that matters: predict outcomes *before* running experiments, compare predictions to results, log the delta, and treat surprises as the primary signal. Maintain a research journal, a conjecture ledger with explicit falsification protocols, and a record of pre-registered predictions.

A few discipline points specific to this problem:

- Apparent unboundedness up to some N is not unboundedness. Be explicit about search horizons and never let "didn't find a cycle" inflate into "no cycle exists" in the writeup.
- Variants that look algebraically distinct can be conjugate via simple substitutions. Before reporting a parameter region as novel, check it isn't a relabeling of one already characterized.
- The interesting output is conjectures with scope, not exhaustive tables. A claim like "for parameters in region R with property P, all orbits converge" beats a million-row CSV.
- Negative and null results count, provided the search was thorough enough to make them informative.

## Constraints

- Laptop-scale. Arbitrary-precision integers (Python is fine; use `gmpy2` if performance demands it). No GPU.
- Reproducibility: fixed seeds, single-command regeneration of all results.

## Deliverable

A `README.md` containing a small number of falsifiable empirical claims, each with scope, evidence, and a falsification record — plus the parameter atlas itself in a form another researcher could reuse, and the research log, conjecture ledger, and prediction-vs-outcome record an autoresearch run produces.

## Begin

Read anything already in the repo, then write your opening entry in the research log: how you're framing the problem, what you'd push back on in the brief above, and what you'll do first. Then proceed.