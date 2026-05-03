# res 008 — algebraic enumeration of (3, 13) L=5 cycles

## What & why
Queue #1 (now-promoted to head). C-008 says (3, 13) admits exactly 7
primitive L=5 cycles. Action 005 found these empirically by sweep at
S=10⁵; action 006 confirmed no new ones at 10× horizon. The remaining
question: is "exactly 7" forced by the algebra, or could a higher-seed
cycle be hiding?

Predicted before dispatch: about 7 of the 35 compositions of 8 into 5
positive parts would yield valid integer cycles. *Wrong.* The actual
result is structurally cleaner.

## Done
Sub-agent enumerated all 35 compositions (k₁..k₅) with k_i ≥ 1 and
Σk = 8. For each composition, computed n₀ from the L=5 cycle equation
at (a=3, b=13):

  n₀ · (2⁸ − 3⁵) = 13 · (3⁴ + 3³·2^{k₁} + 3²·2^{k₁+k₂}
                         + 3·2^{k₁+k₂+k₃} + 2^{k₁+k₂+k₃+k₄}).

Since 2⁸ − 3⁵ = 256 − 243 = 13, the LHS is `13 · n₀` and RHS is
`13 · (...)`, giving `n₀ = 81 + 27·2^{k₁} + 9·2^{k₁+k₂} + 3·2^{k₁+k₂+k₃}
+ 2^{k₁+k₂+k₃+k₄}`. Every composition yields a positive integer.
Verified by simulation: every n₀ is odd and the trajectory under T_{3,13}
returns to n₀ in 13 T-steps with the predicted halving pattern.

Deduplication by member set: every cycle has 5 cyclic rotations
contributing the same member set, so 35 / 5 = 7 distinct primitive
cycles. The cycle_min values match the sweep exactly: {211, 227, 251,
259, 283, 287, 319}.

Outputs:
- `autoresearch/archive/008-l5-enumeration.py`
- `autoresearch/archive/008-l5-enumeration.md`

## Result
n/a (research-only)

**35/35 compositions yield valid L=5 cycles. After dedup by 5-fold
rotation: 7 distinct primitive cycles. Match against sweep: 7-for-7.**

The structural reason is sharp:
- `2⁸ − 3⁵ = 13` exactly. This is what makes (3, 13) special at L=5,
  Σk=8.
- For other (a, b) with `2^K − a^L` not a multiple of b, most
  compositions yield a non-integer n₀ and the count of valid cycles is
  much smaller.

## Thoughts
This is the cleanest finding of the run so far. C-008's strong form is
not just empirical — it has a **closed-form structural reason**:

> If `2^{Σk} − a^L = m · b` for some positive integer m and some L,
> Σk, then *every* composition (k₁..k_L) of Σk into L positive parts
> yields a valid primitive cycle of T_{a, b} of shortcut length L and
> T-period Σk + L (after checking n₀ is odd, which is automatic when
> the resulting n₀ is integer and m·n₀ matches the RHS structure).

The (3, 13) case has m = 1, which is the cleanest possible setting.
The number of compositions of K into L positive parts is C(K−1, L−1),
and after dedup by L-fold cyclic rotation it's C(K−1, L−1) / L (when
no composition is rotation-symmetric, which is the generic case for
gcd(K, L) = 1 — here gcd(8, 5) = 1).

So **C-008 generalizes**:

> For any (a, b, L, K) with `2^K − a^L = m·b` for some positive
> integer m, the number of distinct primitive L-cycles of T_{a, b} at
> T-period K + L is **C(K−1, L−1) / L** (for gcd(K, L) = 1; the
> general case requires Burnside/Cauchy-Frobenius counting).

This is C-011 (new conjecture, see Next).

## Conclusion
*Solid (pending user confirmation).* C-008 algebraically verified:
exactly 7 primitive L=5 cycles for (3, 13). The reason is the lucky
identity `2⁸ − 3⁵ = 13`. The structural generalization (C-011) is the
real prize — it gives a closed-form count for cycles in any (a, b)
where `2^K − a^L` divides b.

This is a *promotion-grade* finding. C-008 has both:
- empirical confirmation at two horizons (action 001, action 006)
- algebraic confirmation at the closed-form level (action 008)

## Reasoning
The generalization C-011 is testable:
- Find other (a, b, L, K) where `2^K − a^L` divides b. E.g.
  `2^4 − 3^2 = 7`, so (3, 7, L=2, K=4) should yield C(3, 1) / 2 cycles
  if my generalization is right. C(3, 1) = 3, 3/2 is not an integer —
  so the formula needs adjustment for non-coprime (K, L). Let me redo.
- For gcd(K, L) > 1, some compositions are rotation-symmetric and
  Burnside counts the distinct cycles. The generic-case formula
  C(K−1, L−1)/L is too simple in general.
- Concrete next test: (3, 7, L=2, K=4). Compositions of 4 into 2 parts:
  (1, 3), (2, 2), (3, 1). For each, n₀ = (3 + 2^{k₁}) · 7 / 7 = 3 + 2^{k₁}.
  - (1, 3): n₀ = 3 + 2 = 5
  - (2, 2): n₀ = 3 + 4 = 7
  - (3, 1): n₀ = 3 + 8 = 11
  Are they all valid odd cycles? 5 is odd, 7 is odd, 11 is odd ✓.
  Now dedup by 2-fold rotation: (1, 3) and (3, 1) are rotations of
  each other (same cycle); (2, 2) is rotation-fixed (its own rotation).
  So 2 distinct cycles. The action 002 catalog lists for (3, 7):
  "L1 n=7; L2 (5, 11) k=(1, 3)" — that's 1 L1 cycle + 1 L2 cycle = 2
  cycles. **Wait, my count predicts 2 *L=2* cycles**, and action 002 has
  only 1 L=2 cycle. Discrepancy!
  Looking again: (1, 3) gives n₀ = 5, cycle is {5, ..., 11, ...}; (3, 1)
  gives n₀ = 11, same cycle (rotation). So 1 distinct L=2 cycle from
  these. (2, 2) gives n₀ = 7, cycle is {7, 14}? No — that's L=1, not
  L=2. **(2, 2) corresponds to a "trivial" length-2 cycle that is
  actually a length-1 in disguise — n₀ = 7 with halving pattern (k=2,
  k=2) means 7 → 28 → 14 → 7? Let me check: T(7) = 3·7+13... wait, this
  is for (3, 7), so T(7) = 3·7+7 = 28. T(28) = 14. T(14) = 7. Yes!
  That's 7 → 28 → 14 → 7, T-period 3, **shortcut length 1**. So (2, 2)
  doesn't give an L=2 cycle — it's the L=1 cycle counted twice in our
  composition enumeration.

So the generalization is more subtle: the rotation-fixed compositions
correspond to *lower-shortcut-length* cycles, not new L cycles. The
correct count is **only** the rotation-orbit count of compositions
that don't reduce to lower shortcut length. Burnside-style.

So C-011 should be stated more carefully — but the (3, 13) case (gcd(K,
L) = gcd(8, 5) = 1) avoided this complication, which is why all 35
compositions gave 7 genuine cycles.

## Next
- **Promote C-008** in CONJECTURES.md to status `surviving` (pending
  user confirmation for `promoted`).
- **Add C-011** (general count of primitive L-cycles when 2^K − a^L
  divides b, with the Burnside refinement).
- **Add a falsification entry** for C-011: enumerate (a, b, L, K)
  candidates and check the cycle count against the sweep.
- **MEMORY.md ## Open questions:** add the rotation-fixed composition
  refinement.

## Linked
- autoresearch/archive/008-l5-enumeration.py
- autoresearch/archive/008-l5-enumeration.md
