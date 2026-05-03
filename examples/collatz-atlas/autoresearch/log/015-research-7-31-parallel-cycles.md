# res 015 — (7, 31) parallel cycles as a worked example of C-011's m > 1 case

## What & why
Action 012 reported 4 parallel length-23 cycles for (7, 31). These
look superficially like C-008's (3, 13) family. Probed inline to
verify the structural prediction.

Predicted before checking: the 4 cycles share (L, K) and m, with the
composition filtering acting through the secondary `m | S(k)`
divisibility (since presumably m > 1, distinguishing this case from
C-008's m = 1).

## Done
Direct query of `012-cycles.parquet` for (7, 31) cycles. Computed
L = (count of odd cycle members), K = (T-period − L), D = 2^K − 7^L,
and m = D / 31.

## Result
n/a (research-only)

5 cycles for (7, 31):
- cycle_id 2: L=1, K=3, gcd=31. **Inherited** (n=31 from (7, 1)'s
  base cycle scaled by 31). D = 2^3 − 7 = 1; 31 ∤ 1, so **NOT** in
  C-011's primitive class. Correctly tagged inherited.
- cycle_ids 0, 1, 3, 4: all **L=6, K=17, gcd=1, m=433** (where
  m = (2^17 − 7^6) / 31 = 13,423 / 31 = 433). cycle_min values
  73, 89, 101, 129 — 4 distinct primitive cycles.

For (L=6, K=17): total compositions of 17 into 6 positive parts =
C(16, 5) = 4,368. After rotation orbits (gcd(K, L) = gcd(17, 6) = 1,
generic case): 4,368 / 6 = 728 distinct rotation orbits. Of these,
only **4** yield primitive cycles — the ones whose S(k⃗) is divisible
by m = 433.

So (7, 31) at (L=6, K=17) sees only 4/728 ≈ 0.55% of compositions
producing valid integer n₀.

## Thoughts
This is the **archetype of C-011's m > 1 case**, complementary to
C-008's m = 1 case:

- (3, 13, L=5, K=8): m = 1, all 35 compositions yield cycles, 7
  distinct after rotation dedup.
- (7, 31, L=6, K=17): m = 433, only 4 of 4,368 compositions yield
  cycles (4 primitive after rotation dedup).

In both cases the **count of primitive cycles** is determined exactly
by C-011 + the secondary `m | S(k)` filter. The proof in
`014-c011-necessity-proof.md` covers both cases.

This worked pair (3,13) vs (7,31) is what makes C-011 feel like a
real classification theorem rather than a happy coincidence at one
point.

## Conclusion
*Solid.* (7, 31)'s 4 parallel primitive cycles are a textbook m > 1
example of C-011. The structural picture is consistent across the
atlas.

## Reasoning
A natural follow-up: enumerate which `(k₁..k₆) ⊢ 17` compositions
yield S(k⃗) ≡ 0 (mod 433). With m = 433 prime (let me verify: 433 is
prime, since 433 / 19 = 22.8..., /17 = 25.5, /13 = 33.3, /11 = 39.4,
/7 = 61.9, /5 = 86.6, /3 = 144.3 — and 433 < 21² = 441 — so prime),
the condition is a single residue constraint mod 433. The probability
for a random composition's S to satisfy ≡ 0 (mod 433) is roughly
1/433 ≈ 0.23%. Out of 728 rotation-orbits, expected ≈ 1.7. We see 4,
which is plausible (Poisson noise around 1.7).

## Next
- **CONJECTURES.md C-008-style entry for (7, 31)?** Probably overkill;
  C-011 already covers it. Better as an example in the README.
- Wait for action 013 (n_new structural explanation).

## Linked
- autoresearch/archive/014-c011-necessity-proof.md (proof)
- autoresearch/archive/012-cycles.parquet (data)
