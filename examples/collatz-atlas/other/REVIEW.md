# Independent Math Review of report.md

Reviewer: independent agent, fresh-eyes pass, no prior conversation context.
Date: 2026-05-04.

## 1. Overall verdict

**Publishable with revisions** as a short note (e.g., INTEGERS, Journal of
Integer Sequences, or arXiv preprint). The core mathematical content of
Theorem A and Theorem C is correct, novel-enough, and tightly argued;
Theorem 053's global classification is sound modulo making the Baker step
fully effective. **Not a duplicate** of Belaga–Mignotte 1998 or Gupta 2020,
but the bijective-count component (C-019) is closer to a "natural
strengthening" of Gupta than the report acknowledges in its headlines.

## 2. Mathematical correctness (proof-by-proof)

**Theorem A.** Substitution `2^K = b + a^L` into `m'·b = 2^{K+j} − a^{L-j}`
cleanly yields `(m' − 2^j)·b = a^{L−j}·((2a)^j − 1)`. Coprimality
`gcd(b, a) = 1` is justified (any odd prime dividing both would divide
`2^K`, contradicting oddness). Forward direction `b | (2a)^j − 1` and
converse-by-substitution are both valid. Numerically verified the
closed-form `m' = 2^j + a^{L−j}·((2a)^j−1)/b` on the two exceptional cells
(m'=11 for (3,3,5,j=1) and m'=77 for (5,3,7,j=1)). **Sound.**

**Theorem B (L'=1).** Trivially correct: S=1, m'≥2 ⇒ no integer solution.
**Sound.**

**Theorem C (L'=2).** The most delicate step. Correct:
- Step 1: bound `m' ≥ 2^{L-2} + a²·q ≥ a² + 2` is correct given `q ≥ 1` and
  `L ≥ 3`. The `a²−2 < m'` inequality and the contradiction with `a` odd
  integer are valid.
- Step 2-3: squaring/discrete-log argument forcing `2k₁ ≡ K' (mod ord_{m'}(2))`
  and then `2k₁ = K'` from the order bound is correct; the imprimitivity
  conclusion `(K'/2, K'/2)` follows.

**Small gap to flag:** the proof shows the unique solution `2^{k₁} ≡ −a (mod m')`
in `[1, K'−1]`, but the cycle equation actually requires `m' | S(k')` where
`S(k') = a + 2^{k₁}` for `L'=2`. A referee would want it spelled out that
`S(k_1, k_2) = a + 2^{k_1}` only depends on `k_1` (since `k_2 = K' − k_1`).
Implicit in the algebra; should be made explicit.

**Theorem 053 / Step 3-6.** Reduction `b ≤ (2a)^{L−2}` is correct (since
`b | (2a)^j − 1` ⇒ `b ≤ (2a)^j − 1 ≤ (2a)^{L-2} − 1`). Combined with the
Baker/Tijdeman lower bound `b ≥ a^{L−ε(a,L)}`, one gets
`a^{2−ε} ≤ 2^{L-2}` ⇒ `a ≤ 2^{(L-2)/(2-ε)}`. **Structure is sound** — this
is exactly how one applies linear forms in logs to a Pillai-type problem.
However:

- **Real gap:** The report does not actually compute the effective Baker
  constant. The empirical sweep (a ≤ 5001, L ≤ 50, K ≤ 200) is large but
  does not by itself rule out cells with very large `a` and small `L`, or
  `L` slightly above 50. To make Step 6 fully rigorous, one needs a
  published explicit Baker bound (Laurent–Mignotte–Nesterenko 1995, or
  Mignotte's 2002 sharpened constants) and then verify that
  `2^{(L-2)/(2-ε(a,L))}` is dominated by 5001 for all L≥3. The headline
  **"global / unconditional" should be downgraded** to "conditional on
  standard explicit Baker constants" until computed.
- The ad-hoc "for a ≥ 7, the smallest 2^K exceeds a³ by more than 2a−1"
  claim is correct for a=7 onward by direct check (the table is right),
  but the justification "By Baker, this holds for all a ≥ 7 (effectively)"
  hand-waves. Cannot stand as a formal proof without computation.

## 3. Novelty assessment

| Component | Rating | Justification |
|---|---|---|
| **Theorem A** (`b ∣ (2a)^j − 1`) | **6/10** | The substitution is elementary (one line) but the explicit reformulation of alt-tuple existence as a Pillai-type divisibility on `(2a)^j − 1` is, to my knowledge, not stated in Belaga–Mignotte, Gupta, or Lagarias's surveys. Could plausibly appear as an exercise but I have not seen it. |
| **Theorem C** (L'=2 closed form via order bound) | **6/10** | Substantive: discrete-log uniqueness combined with the imprimitivity payoff is a genuine argument, not a routine corollary. Similar arguments appear in cycle nonexistence proofs (Steiner 1977, Simons & de Weger 2005) but the specific application to alt-tuple coexistence on the m=1 hypersurface is new. |
| **Theorem 053** (global finite classification {(3,5),(5,3)}) | **5/10** | Once Theorem A is in hand, an expert with Baker bounds would produce this in a day. The combination is novel and the explicit identification of these two cells is a nice concrete result, but the "size-2 set" outcome is not surprising given Tijdeman/Pillai finiteness. |
| **Catalan families K = 2L±1 at a = 3** | **3-4/10** | Not found in Lagarias's surveys (1985, 2010, 2012) or Conway/Tao/Kontorovich. However, the general fact that compositions of K into L parts give cycles via the m=1 mechanism, combined with binomial counts, is present in Belaga–Mignotte and is a few-line computation from there. The Catalan reading is cute and might be new in print, but is not deep. **"First infinite tractable subfamily" overstates novelty.** |
| **C-019 = exact Lyndon-word count** | **4-5/10** | Closest call. Gupta 2020 Theorem 10 establishes existence with Hardy-Ramanujan asymptotics; Möbius/Lyndon-word counting on cyclic compositions is utterly standard (OEIS A001037, Reutenauer's *Free Lie Algebras*). Combining the two gives the exact count by inspection — *if you know Gupta gives a primitive composition for each Lyndon word and that no extras arise*. The "no extras" half is genuinely Theorems A+C+053. The bijection statement is 3-4/10, the *exactness* is what gives it 4-5/10. |

**Prior art search.** **No exact duplicate found.** Closest neighbors:
- Belaga–Mignotte 1998 ("Embedding the dynamics of a Collatz-like ...") — cycle equation.
- Simons–de Weger 2005 — nonexistence bounds for non-trivial Collatz cycles via Baker (relevant methodologically, not on m=1 enumeration).
- Steiner 1977 — Collatz cycle-nonexistence proof using a similar discrete-log + order-bound template.

None of these state Theorem A or the explicit Lyndon-bijection / global classification.

## 4. Empirical evidence

**Sufficient.** Verification scripts run and confirm:
- `048-lyndon-full-lattice.py`: 17/17 gcd>1 cells match the Möbius count exactly.
- `053-massive-finite-check.py`: across (a ≤ 5001, L ≤ 50, K ≤ 200), exactly two cells satisfy `b | (2a)^j − 1` for some `j ∈ {1,...,L−2}`: (3,3,5) and (5,3,7). Confirmed.
- Combined gcd=1 verification (action 047) of 42 cells plus 17 gcd>1 = 59 — correct.

**Minor:** the "5×10⁷ cell-tuple sweep" headline is order-of-magnitude
correct (the actual count is roughly 2-3×10⁷ (a, L, K) triples plus
j-iterations); calling it "2-5×10⁷" or just "tens of millions" would be
more honest.

## 5. Gaps and follow-ups

1. **Effective Baker constants for Step 6.** The single largest gap. The
   report acknowledges it but the headline should not say "unconditional."
   A weekend's work with Laurent–Mignotte–Nesterenko 1995 would close this.
2. **L' ≥ 3 alt tuples.** The proof relies on Theorem 053 ruling them out
   globally via Baker rather than proving a Theorem-C analog. Correct
   strategy, but the exposition should make crystal clear that the
   "no extras for L' ≥ 3" half is *only* established because no such alt
   tuples exist at all (per Theorem 053). If a future version of the Baker
   step found a missed cell at L=3, the C-019 strict-equality claim would
   be re-opened.
3. **m > 1 primary tuples.** Report explicitly excludes these (§2.6). For
   completeness, a published version should state precisely what is *not*
   claimed: cells with the same total length T = K+L but different primary
   (L, K) pairs and m > 1 could in principle add cycles not counted by
   L_{K,L}. C-017 handles one piece; the general statement is open.
4. **Bijection direction in C-019.** The proof sketch relies on `n_0` being
   odd (proven), positive, and the cycle landing back on `n_0` after K+L
   steps. Injectivity follows from Belaga–Mignotte; surjectivity is what
   Theorem 053 effectively secures. **This logical chain should be drawn
   explicitly** in a publication-grade write-up.

## 6. Final calibrated rating

**5/10** on the integral=10 / standard-PhD=7 scale.

The report's self-rating of 5–6/10 is roughly honest; I land at the lower
end (5/10).

- Theorem A is a clean and genuinely new identity.
- Theorem C is a substantive (not routine) discrete-log argument.
- Theorem 053 is the right global statement; empirical evidence is solid.
- Together they form a coherent ~10-page paper that would publish in a
  specialty venue (INTEGERS, J. Integer Seq., or as a section of a longer
  Collatz-family survey).

**What keeps it from 6-7/10:** (i) the Baker step is not made effective;
(ii) the Lyndon bijection on m=1 cells is morally close to "Gupta +
standard Möbius counting" — the genuinely-new insight is the no-extras
half, not the count itself; (iii) the result is firmly *within* the
existing Belaga–Mignotte framework rather than introducing new machinery.

**What lifts it above 3-4/10** (the reviewer-pivot rating at action 049):
the Diophantine criterion of Theorem A *is* a new identity, the L'=2
discrete-log argument is non-trivial, and the explicit two-cell
classification is a concrete falsifiable end-state. The Catalan-family
corollary is a nice expository hook but does not add mathematical weight.

## Recommendation

Revise the manuscript to:
- (a) compute the explicit Baker constants;
- (b) demote the "unconditional / global" claim slightly until (a) is done;
- (c) compress the C-019 / Lyndon-word framing as "Gupta's Theorem 10
  strengthened to an exact count via Theorems A+C+053" rather than as a
  fresh discovery;
- (d) lead with Theorem A as the cleanest standalone novel statement.
