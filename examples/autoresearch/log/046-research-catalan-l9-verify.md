# res 046 — Catalan family L=9 verification (and L=9 b-value correction)

## What & why
Per "DON'T STOP" directive, push the Catalan-family empirical evidence
one more rung. Predicted: (3, b=2^{17}−3^9) admits exactly C_8 = 1430
primitive cycles at L=9, K=17 via the construction in C-018.

## Done
1. Computed correct b: 2^17 − 3^9 = 131072 − 19683 = **111389**
   (the table in log/045 had an arithmetic error: 113213 was wrong;
   fixed in README.md and CONJECTURES.md).
2. Enumerated all C(16, 8) = 12870 compositions of K=17 into L=9
   positive parts.
3. Computed n_0 = S(k_⃗) for each; verified n_0 is odd in every case
   (consistent with the C-018 proof, step 3).
4. Traced trajectories from each n_0; collected distinct cycle
   member-sets.
5. Counted distinct cycles.

Script: `archive/046-catalan-l9-verify.py`.

## Result
- Distinct n_0 values from compositions: **12870** (= C(16, 8))
- Distinct primitive cycles: **1430** = C_8 (Catalan)
- All cycles have iteration-length 26 = K + L = 17 + 9 ✓
- 12870 / 9 = 1430 confirms each cycle is hit by exactly L=9
  rotation-equivalent compositions, as predicted by Burnside (no
  rotation symmetry since gcd(2L-1, L) = 1).

**Seven consecutive Catalan numbers now empirically verified:**
2, 5, 14, 42, 132, 429, 1430 for L = 3, 4, 5, 6, 7, 8, 9.

## Thoughts
The verification is mechanical now — the proof is solid and each
additional L is just a confirming data point. The interesting questions
have shifted to:

1. **Are these cycles trap-attractive or trap-repulsive?** I.e., for
   (3, 111389), what fraction of orbits from random starting points
   eventually enter one of the 1430 primary cycles vs. diverge or
   enter higher-K cycles? With 1430 primary cycles in a single cell,
   the basin geometry is plausibly very different from (3, 1) where
   only the trivial cycle exists.

2. **Generalization to a > 3.** The construction requires
   2^K > a^L with K = 2L-1, i.e. 2^{2L-1} > a^L, i.e. a < 2^{2 - 1/L}.
   For L → ∞, the bound is a < 4. So a ∈ {1, 3} is exhaustive among
   odd a. For a=1 the construction degenerates (3·n+b becomes n+b).
   So a=3 is the unique non-trivial Catalan family in this exact form.

3. **Are there other (a, b) families with composition count = a
   classical sequence (Motzkin, Schröder, Fibonacci)?** Different
   gcd(K, L) values would dedup differently, possibly producing
   other combinatorial sequences. Worth a dedicated sweep.

4. **The L=10 prediction (4862 cycles for (3, 465239))** is a
   straightforward extension; not pursued here because it offers no
   new structural information beyond confirming the same proof.

## Conclusion
*Verified, no surprises.* The Catalan family C-018 stands at seven
consecutive verifications. The mathematical content is the proof;
empirical verification beyond L=9 is decorative.

The immediate "did we discover something new" question (per user's
directive) is firmly answered: **yes** — an infinite family of
"tractable cousins" of Collatz with explicit cycle counts following
the Catalan sequence, connecting Pillai-form Diophantine constraint,
C-011 cycle classification, and Burnside-Catalan combinatorics.

## Reasoning
The minor b-value correction is worth recording because it would
otherwise propagate as "we predicted a value for L=9 and verified it"
when in fact the predicted b was wrong. With the corrected b, the
verification is clean and exact.

## Next
- Investigate basin geometry for (3, 111389): with 1430 primitive
  cycles, do "most" trajectories from random starts converge to one
  of them, or are most trajectories apparently unbounded? A short
  random-start sweep at S = 10^4 should distinguish.
- Explore non-(2L-1) K values for cycle-rich dedup variants.

## Linked
- archive/046-catalan-l9-verify.py
