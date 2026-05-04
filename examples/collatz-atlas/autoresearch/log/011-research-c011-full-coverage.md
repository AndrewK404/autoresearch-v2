# res 011 — full C-011 coverage at unbounded (L, K)

## What & why
After integrating action 010, I noticed the agent reported "5 cycles
outside C-011's mechanism" with notation "(a, b) L=X K=Y" where Y was
the *T-period* (cycle length), not the sum of halvings. This made me
question whether those 5 cycles were genuinely outside C-011 or just
outside the enumeration cap (L ≤ 8 in my brief).

Predicted before checking: at most a couple of the 5 are genuinely
outside the divisibility; the rest are within the cap with corrected K.

## Done
Pulled all 64 `new`-tagged cycles from the merged atlas via `atlas.py`.
For each, computed K_halvings = t_period − shortcut_L. Checked whether
`b | (2^{K_halvings} − a^{shortcut_L})`.

## Result
n/a (research-only)

**64 of 64 primitive cycles satisfy C-011's divisibility.** Zero genuine
outliers. The 5 "outliers" reported by action 010 were artefacts of
the L ≤ 8 cap, not of the divisibility condition.

Combined with action 003's mechanism (89 inherited cycles via
b-scaling), the atlas decomposes completely:

- **89 inherited cycles** — for each (a, b) with b > 1, every odd
  divisor d > 1 of b yields a d-scaled image of an (a, b/d) cycle.
  Mechanism: b-scaling embedding (action 003).
- **64 primitive cycles** — every primitive cycle satisfies
  `b | (2^K − a^L)` for the cycle's (L, K). Mechanism: C-011's
  divisibility condition.

**Total: 153 = 89 + 64. Full coverage.**

## Thoughts
This is a stronger statement than C-011's original "sufficient
condition" framing. Empirically, in our tight scope:

> Every primitive cycle of T_{a, b} corresponds to a triple (L, K) with
> b | (2^K − a^L), with K = number of halvings = t_period − L.

Two reasons this might generalize:

1. **The cycle equation** for L, K = (k₁..k_L) is
   n₀ · (2^K − a^L) = b · S(k_⃗) where S is a positive integer
   depending on the composition. For primitive n₀ to be a positive
   integer, (2^K − a^L) must divide b · S(k_⃗). C-011's strong
   divisibility (b | 2^K − a^L) is ONE way for this to happen — every
   composition then yields a valid n₀. But the weaker
   "(2^K − a^L) divides b · S(k_⃗) for some composition" could also
   produce primitive cycles.
2. The empirical observation is that, in our tight scope, the weaker
   condition didn't add anything beyond the strong one. Either:
   - The tight scope is too small for the weaker mechanism to surface
     (would emerge at b > 21 or larger L).
   - OR the strong condition is in fact the only mechanism — there's
     a hidden number-theoretic reason gcd(2^K − a^L, S(k_⃗)) cannot
     exceed b in the absence of `b | 2^K − a^L`.

Either way, **C-011 strengthens to a near-classification theorem** in
tight scope: it accounts for *every* primitive cycle.

## Conclusion
*Solid (pending user confirmation).* C-011 is now empirically
necessary and sufficient for primitive cycle existence in tight scope.
The atlas at S = 10⁵, H = 10¹³ admits a complete closed-form
decomposition:

- 89 cycles inherited via b-scaling
- 64 cycles primitive via 2^K − a^L | b

This is the strongest deliverable of the run.

## Reasoning
Methodologically: the action 010 agent's notation collision (using K
for t_period instead of K = halving sum) almost cost us this finding.
Caught by main on the integration pass after questioning the "5
outliers" report. **Always re-derive numerical claims from the parquet,
not from the summary's notation.** This adds to the Avoid list.

## Next
- **CONJECTURES.md C-011:** upgrade evidence to "all 64 primitive
  cycles in atlas satisfy the condition (64/64)". Status remains
  surviving — promotion-grade.
- **MEMORY.md:** update Status to highlight full coverage. Remove "5
  outliers, second mechanism" from Open questions.
- **README.md:** the C-011 + inheritance dual decomposition is the
  headline result. Worth foregrounding.

## Linked
- atlas.py (project root) — loader used for the verification.
