# res 009 — analytic proofs for C-007′ and C-006″ (replacing C-006′)

## What & why
After action 008 promoted C-008 with closed-form support, I wanted to
do the same for C-007′ and C-006′. Both looked like they should be
provable in a few lines from the family's mechanics. This log captures
the attempt.

Predicted before starting: C-007′ proves trivially via the b-scaling
embedding; C-006′ might need a residue-arithmetic argument and could
be refined.

## Done
Wrote `autoresearch/archive/009-c007-prime-and-c006-prime-proofs.md`
inline (main = sole writer). The file contains:
1. Closed-form lower-bound proof of C-007′ via the b-scaling sub-system
   embedding (action 003). Trivial: φ_d(n) = d·n is a full conjugacy
   from T_{1, b/d} to T_{1, b} on dℤ; the base cycle of T_{1, b/d}
   maps under φ_d to an inherited cycle of T_{1, b} with member-gcd
   ≥ d. Distinct d give distinct gcds, so n_inherited ≥ d(b) − 1.
2. Attempt at proof of C-006′ that **showed C-006′ is wrong as
   originally stated.** The residue r_t mod λ for an n₀ ∉ λℤ evolves
   as r → 3r (odd step) and r → r·2⁻¹ (halving step), both in
   (ℤ/λℤ)*. If gcd(3, λ) = 1, the residue stays in the units forever
   and never hits 0. Empirical check via direct query of
   `006-attractivity.parquet`: confirmed.

Then ran a one-liner across all 20 (a, b, λ) cells in
`006-attractivity.parquet` to verify the refined claim:

> forward-attractivity ⟺ gcd(a, λ) > 1

**20/20 empirical match.** Promoted to C-006″ in CONJECTURES.md.

## Result
n/a (research-only)

- C-007′ has a closed-form lower-bound proof, no caveats.
- C-006′ as originally stated is **wrong**. Its replacement C-006″
  (gcd(a, λ) > 1 ⟺ forward-attractive) holds 20/20 empirically and
  has an analytic argument for prime λ via residue arithmetic in
  (ℤ/λℤ)*.

## Thoughts
Two lessons:

1. **The action 006 sub-agent's summary was misleading.** It said "for
   a=3, max hit time ≤17" — but this applied only to λ=3 cells where
   the multiplicative factor 3 absorbs the residue immediately. For
   (a=3, λ=5, b=15) the data shows 80,000/100,000 seeds *never* enter
   5ℤ within T=10⁵. I missed this in the first integration pass and
   only caught it when my own analytic attempt produced a
   contradiction with the agent's claim.

2. **The condition `gcd(a, λ) > 1` is sharper and more elegant than
   the "a = 3 only" claim it replaces.** It connects directly to the
   residue arithmetic: a is a unit in (ℤ/λℤ)* iff gcd(a, λ) = 1, and
   in that case the orbit of a residue under multiplication-by-a
   never reaches 0. This generalizes to composite λ via rad(λ) |
   rad(a) — a strong testable conjecture for the L2 phase.

## Conclusion
*Solid.* Two conjectures advance to promotion-grade with both
empirical and analytic support: C-007′ and C-006″. Pending user
confirmation per cadence agreement.

## Reasoning
This action validates the "main never idle" principle: while
sub-agents work on the heavier dispatches (010 in flight), main can
do high-value short-form analytic work. Two conjectures graduated to
promotion-grade in 30 minutes of main's own thinking.

The C-006″ refinement is also a methodological win: my prior C-006′
was wrong, but the falsification came from my own residue argument,
not from a separate sub-agent. The autoresearch loop encourages this
self-correction: predict-then-run + try-to-prove-it surfaces
inconsistency fast.

## Next
- **MEMORY.md ## Avoid:** add "Trust sub-agent summaries only after
  cross-checking against the underlying parquet/data when promoting
  a conjecture."
- **MEMORY.md ## Recent:** record action 009.
- **MEMORY.md ## Open questions:** "what governs n_new(1, b)?" remains
  open. Add: "does C-006″ generalize to composite λ via
  rad(λ) | rad(a)?" — testable in L2.
- Wait for action 010 (C-011 enumeration) to land.

## Linked
- autoresearch/archive/009-c007-prime-and-c006-prime-proofs.md
