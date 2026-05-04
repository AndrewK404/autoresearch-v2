# res 002 — analytic trivial-cycle catalog

## What & why
Queue #2 — derive cycles of shortcut length L ≤ 3 in closed form for each
(a, b) in scope, before the sweep returns. Goal: ground truth for the
sweep cross-check, and pre-flag (a, b) where the sweep should find
specific cycles by member-set.

The hypothesis being tested in this action: "a closed-form derivation at
L ≤ 3 captures most of the cycle structure visible in the sweep at
S = 10⁴." Rejection condition: if the sweep finds many cycles not
predicted at L ≤ 3, the analytic catalog is too shallow and we should
extend to L = 4, 5.

## Done
Sub-agent solved the standard recurrences:
- L1: n·(2^k − a) = b
- L2: n₀·(2^{k₁+k₂} − a²) = b·(a + 2^{k₁})
- L3: n₀·(2^{k₁+k₂+k₃} − a³) = b·(a² + a·2^{k₁} + 2^{k₁+k₂})

over k bounded ranges, deduplicated cycles by member set, verified each
algebraic candidate by direct simulation under T_{a,b}. No discrepancy
found between algebra and simulation.

Outputs:
- `autoresearch/archive/002-trivial-cycles.md` — full per-variant
  catalog, predictions for the sweep, conjugacy hints
- `autoresearch/archive/002-verify.py` — verification script

## Result
n/a (research-only)

Headline:
- 116 cycles total at L ≤ 3 across the 44 variants
- L1: 49, L2: 26, L3: 41
- All 44 variants have at least one cycle at this depth
- Richest: (5, 9) with 8; (5, 3), (5, 21) with 7+; (5, 15) with 7
  (5-scaled image of (5, 3))
- Sparsest: 12 variants have only the universal n=b cycle (e.g.
  (1, 11), (1, 13), (1, 17), (1, 19); (3, 9), (3, 19); a=7 mostly)
- a=5 has *no* universal n=b L1 cycle (since 2^k − 5 ≠ 1 for any k);
  this is a structural difference from a ∈ {1, 3, 7}

## Thoughts
- The non-existence of a universal `n = b` cycle at a = 5 is striking.
  It's a tight number-theoretic constraint: `2^k − 5 = 1` has no
  solution. This *might* be a clue to why a=5 dynamics are more
  divergent — there's no "easy" L1 attractor that catches every b·m for
  m a power of 2.
- Conjugacy hints from the algebra (later confirmed by action 003):
  - `n = c·m` with `c | b` embeds `T_{a, b/c}` into `T_{a, b}` on cZ.
  - Therefore (5, 15) is a 5-scaled (5, 3); (3, 9) is a 9-scaled (3, 1).
- (5, 9) is *not* a scaling: the cycle (1, 7, 11) is genuinely new at
  this row. b=9 has divisors {1, 3, 9}; (5, 1) and (5, 3) have specific
  cycle structures, and (5, 9) introduces a cycle whose members are
  coprime to 3. So scaling cannot explain it.

## Conclusion
*Tentative.* Lower-bound prediction: every (a, b) cycle list in the
sweep contains at least the L ≤ 3 cycles from this catalog. After cross-
check (see Reasoning), the catalog appears tight as a lower bound but
incomplete: the sweep finds 153 cycles, of which 116 match this catalog
at L ≤ 3 and 37 are at L ≥ 4, concentrated in (3, 13) and the a=5 row.

## Reasoning
Cross-check against sweep (action 001):
- 153 distinct cycles in sweep − 116 closed-form cycles at L ≤ 3
  = 37 cycles at L ≥ 4 visible in the sweep
- (3, 13) sweep finds 10 cycles; analytic catalog finds 2 at L ≤ 3.
  So 8 cycles at L ≥ 4. **This is the headline cross-check anomaly.**
  Why does (3, 13) carry so much L ≥ 4 structure? b = 13 is a prime,
  no scaling parents in the (3, ·) row. Worth deeper investigation.
- (3, 5): sweep finds 6 cycles; catalog finds 4. Two cycles at L ≥ 4.
  Smaller anomaly.
- (5, 21): sweep finds 12 cycles; catalog finds 8. Four cycles at
  L ≥ 4 — but (5, 21) is a scaling of (5, 3) plus extras, so the L ≥ 4
  cycles may decompose into "(5, 3)-inherited" vs "new at b=21". Worth
  separating.

The catalog was correct as far as it went; the gap is honest about the
limit of L ≤ 3. We should NOT extend to L = 4, 5 algebraically right
now — that's diminishing returns. Instead, use the sweep's
`001-cycles.parquet` to *list* the L ≥ 4 cycles directly and pair them
with their structure (members, period). That's a quick analyst dispatch.

The conjugacy hints from this action seeded action 003's b-scaling
section directly, so the analytic and substitution arms came out
consistent.

## Next
- Schedule analyst dispatch (action 005 or so): "list every L ≥ 4 cycle
  found in 001-cycles.parquet, group by (a, b), report period
  distribution, member-coprimality structure" → `archive/005-l4plus.md`.
- Action 003's normal form table will be cross-multiplied with the
  catalog to tag each cycle as "inherited from (a, b/λ)" or "new."

## Linked
- autoresearch/archive/002-trivial-cycles.md
- autoresearch/archive/002-verify.py
