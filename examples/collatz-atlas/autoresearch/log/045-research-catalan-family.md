# res 045 — the Catalan family of cycle-rich (3, b) cells

## What & why
While exploring the (3, 269) cell (which I identified as having a single m=1
tuple at (L=5, K=9) per C-011 prediction), I noticed Burnside's count
C(K-1, L-1)/L for K = 2L-1 simplifies to C(2L-2, L-1)/L = **Catalan
number C_{L-1}**. This suggested an infinite family of cells with
Catalan-many cycles.

## Done
1. Identified the K = 2L-1 family algebraically.
2. Computed b = 2^{2L-1} - 3^L for L = 3, 4, 5, 6, 7, 8.
3. Predicted cycle counts via Catalan numbers C_{L-1}.
4. Verified empirically for L = 3, 4, 5, 6.

## Result

**The Catalan family** of "exceptionally cycle-rich" (3, b) cells:

| L | K=2L-1 | b = 2^K − 3^L | Catalan C_{L-1} | Empirical |
|---|---|---|---|---|
| 3 | 5 | **5** | 2 | 2 ✓ (atlas: (3, 5) has 6 cycles total, 2 at L=3 K=5) |
| 4 | 7 | **47** | 5 | 5 ✓ (atlas: (3, 47) has 8 cycles, 5 at len=11) |
| 5 | 9 | **269** | 14 | **14 ✓** (verified: 14 cycles at length 14) |
| 6 | 11 | **1319** | 42 | **42 ✓** (verified: 42 cycles at length 17) |
| 7 | 13 | 6005 | 132 | predicted |
| 8 | 15 | 26207 | 429 | predicted |
| 9 | 17 | 113213 | 1430 | predicted |

For L = 5: convergence verified at S=10⁵, 14 cycles at length 14
exactly match the prediction.

For L = 6: convergence verified at S=10⁵, 42 cycles at length 17
exactly match the prediction. 1319 is prime, so all 42 are primitive.

**Why Catalan?** Compositions of K = 2L-1 into L positive parts are in
bijection with subsets of {1, ..., 2L-2} of size L-1, totaling
C(2L-2, L-1). With gcd(K, L) = gcd(2L-1, L) = 1, no composition is
rotation-symmetric, so Burnside gives:

  C(2L-2, L-1) / L = (2L-2)! / (L! · (L-1)!) = C_{L-1} (Catalan).

## Thoughts
This is a clean structural connection between THREE pieces:

1. **Pillai equation specific form**: b = 2^{2L-1} − 3^L picks out a
   specific exponent ratio K/L = 2 - 1/L.
2. **C-011 cycle classification**: the m=1 case (b | 2^K - a^L
   exactly) gives generic-composition cycles.
3. **Catalan combinatorics**: K = 2L-1, gcd=1 specializes Burnside
   to Catalan numbers.

The family is INFINITE (one cell per L ≥ 3), with cycle counts
following the Catalan sequence 2, 5, 14, 42, 132, 429, 1430, ...

## Conclusion
*Solid empirical finding.* Verified for L = 3, 4, 5, 6 with
predictions for L ≥ 7 testable via small sweep at the corresponding
b values.

This is the cleanest "new structural observation" of the run. It
produces an INFINITE family of "tractable cousins" with exact
cycle counts, not just sporadic examples.

## Reasoning
Whether this specific connection (Pillai + C-011 + Catalan via
K = 2L-1) is in the literature — uncertain. The component pieces
(cycle equation, Burnside on compositions, Catalan via central
binomial) are standard. The connection in the Collatz-family context
may be novel — at least, it doesn't appear in the standard surveys
I've seen for generalized Collatz.

The cells in the family:
- (3, 5) at L=3 (which is also our double-m=1 cell with extra (1, 3) tuple)
- (3, 47) at L=4
- (3, 269) at L=5 (newly identified as cycle-rich)
- (3, 1319) at L=6 (newly identified, 42 cycles)
- (3, 6005) at L=7 (predicted 132 cycles)
- ...

These are concrete "tractable cousins of Collatz" with explicit cycle
counts.

## Next
- Verify L = 7: (3, 6005) should have 132 cycles. Computational test.
- Check if other a values admit similar Catalan families (a=1 trivial; a=5, 7, ... K=2L-1 doesn't satisfy 2^K > a^L).
- Try to PROVE this structurally (the Burnside-Catalan connection
  is straightforward; the Pillai m=1 condition is by construction).
- Document in CONJECTURES.md as C-018.

## Linked
- (no archive yet — analysis is computational)
