# res 003 — conjugacy survey and normal form

## What & why
Queue #3 — enumerate substitutions n ↔ φ(n) that conjugate (a, b)
variants of T_{a,b}, decide what counts as full conjugacy vs sub-system
embedding, propose a normal form so the atlas does not double-count
"novel" regions.

The hypothesis being tested: "the tight scope contains nontrivial full
conjugacies, and the atlas size collapses by ~30–50% under the normal
form." Rejection condition: if the survey produces only sub-system
embeddings (no full conjugacies), document the negative result and
adjust the atlas to track parents instead of equivalence classes.

## Done
Sub-agent surveyed five substitution families:
1. Trivial b-scaling φ(n) = λn (λ odd ≥ 1)
2. GCD reduction near (3, 3)
3. Periodicity shift (a, b) vs (a, b + 2am)
4. Branch-swap / parity reflection φ(n) = ±n, φ(n) = c − n
5. General integer affine φ(n) = αn + β

For each: derived the algebraic relation, checked positive cases on a
handful of starting seeds, confirmed FAIL probes also fail. All checks
pass. Output: `autoresearch/archive/003-conjugacy-survey.md` with the
worked algebra; `autoresearch/archive/003-verify.py` runs the
PASS/FAIL tests.

## Result
n/a (research-only)

**Zero full conjugacies in the b > 0 scope.** Affine analysis forces
β = 0 and α odd, giving exactly the b-scaling embedding (a, b) → (a, αb).
φ(n) = −n is a full conjugacy on ℤ from (a, b) to (a, −b), which lies
outside our positive-b family.

**Sub-system parents:** every (a, b) with b > 1 admits the parent
(a, 1) via n → bn embedding into bℤ. Composite-b cells admit
intermediate parents: (a, 9) → (a, 3) → (a, 1); (a, 15) → (a, 5),
(a, 3) → (a, 1); (a, 21) → (a, 7), (a, 3) → (a, 1).

**Normal form:** identity. The 44-cell grid does not collapse.
Sub-system parents tracked as separate metadata.

## Thoughts
- I half-expected the affine substitution to recover something
  nontrivial. It didn't. The constraint "must map odd integers to odd
  integers and respect both branches of T" is *very* restrictive.
- The sub-system embedding direction is one-way: (a, 1)'s dynamics
  inject into (a, b)'s dynamics on bℤ — but (a, b)'s dynamics on the
  *complement* (integers not divisible by b) is independent and can
  carry novel cycles. (5, 9)'s (1, 7, 11) cycle is exactly such an
  example: it lives on integers coprime to 3 (and to 9), so no parent
  contains it.
- The open question the survey raises: is bℤ *forward-attracting* under
  T_{a,b} from the rest of ℤ_{>0}? If yes, then asymptotic classification
  reduces. The agent's spot checks suggest yes for (3, 3), but this is
  a sweep-strength question, not a substitution question — flag it.

## Conclusion
*Tentative.* The atlas does not collapse under conjugacy; every (a, b)
in scope is its own equivalence class. Sub-system embeddings *do*
constrain how cycles are inherited: every cycle of (a, 1) gives a
b-scaled cycle of (a, b) on bℤ, and the catalog (action 002) confirms
this structurally. New cycles in (a, b) must live partially or wholly
off bℤ.

## Reasoning
This finding shapes the atlas presentation:
- We do **not** quotient the 44-cell grid. Every (a, b) reports its own
  classification.
- For each cycle in `001-cycles.parquet`, we tag it as either
  **inherited** (members all ≡ 0 mod some odd λ | b, with λ > 1, so the
  cycle is the λ-scaled image of a (a, b/λ) cycle) or **new** (members
  not all in any nontrivial sublattice).
- The "novelty" claim for any region in the atlas requires the cycle to
  be tagged "new" under this scheme — otherwise we're double-counting.

The forward-attractive-sublattice question is a *real* open question
that affects how strongly we can claim "(a, λb) reduces to (a, b)
asymptotically." If λZ is forward-attracting under T_{a, λb}, the claim
is strong. If not, λZ and its complement are independent dynamical
systems and reduction is local-only. The sweep can answer this directly:
for each seed n0 not divisible by λ, log the first time T^t(n0) lands
in λZ, or report it never does.

## Next
- Add to Queue: "Sub-lattice attractivity probe — for each (a, b) with
  composite b, modify the sweep to log first hit time into bZ from non-bZ
  seeds. Output: per-(a,b) histogram of hit times. Falsifier: if any
  fraction > 0 of non-bZ seeds reach the H bound *without* ever hitting
  bZ, the sublattice is not forward-attractive at this horizon."
- Add to Queue: "Cycle inheritance tagging — cross 001-cycles.parquet
  with the parent table. Each cycle gets `inherited_from: (a, b') | new`
  metadata."
- Update CONJECTURES.md format hint: every conjecture about a region
  with composite b must say whether it includes/excludes inherited
  structure.

## Linked
- autoresearch/archive/003-conjugacy-survey.md
- autoresearch/archive/003-verify.py
