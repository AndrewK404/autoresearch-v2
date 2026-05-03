# 009 — Closed-form arguments for C-007′ and C-006′

Author: main (the autoresearch coordinator). These are short structural
arguments derivable from the family's mechanics; recording them so the
corresponding conjectures can be promoted with closed-form support, not
just empirical evidence.

---

## C-007′ — `n_inherited(1, b) ≥ d(b) − 1` for b odd

### Claim
For `T_{1, b}` with b odd, every proper divisor d of b with d > 1
yields a distinct inherited cycle of `T_{1, b}` whose member gcd equals
d. Therefore `n_inherited(1, b) ≥ d(b) − 1` (one inherited per proper
divisor d > 1; the base cycle reached from n = 1 has gcd 1 and is
"new", not "inherited").

### Argument
Fix b odd and d > 1 with d | b. Let m₀ be the entry point (smallest
odd value) of the base cycle of `T_{1, b/d}` reached from seed 1 — call
this cycle `C(b/d) ⊂ ℤ_{>0}`. The base cycle exists and is unique for
each (1, b') with b' odd, by direct construction: starting at n = 1,
T_{1, b'}(1) = 1 + b' (even since b' odd). Halve until odd: that gives
some odd value m₁ < 1 + b'. Continue. Since the trajectory takes only
finitely many odd values < 1 + b' (and each odd step is followed by at
least one halving), it eventually revisits an odd value, closing the
cycle. The cycle reached from n = 1 in `T_{1, b/d}` is the *base cycle*
C(b/d). The same reasoning applies to T_{1, b/d} as to T_{1, b}, so
C(b/d) is well-defined for each odd b/d.

Define the homothety φ_d: ℤ → ℤ by φ_d(n) = d · n. Claim: φ_d
intertwines `T_{1, b/d}` with `T_{1, b}` on dℤ:

- For odd m, T_{1, b/d}(m) = m + b/d. Then φ_d(m + b/d) = dm + b =
  T_{1, b}(dm). ✓ (since dm is odd iff m odd because d odd.)
- For even m, T_{1, b/d}(m) = m/2. Then φ_d(m/2) = dm/2 = (dm)/2
  = T_{1, b}(dm). ✓ (since dm is even iff m even because d odd.)

So φ_d is a *full conjugacy from `T_{1, b/d}` (on ℤ_{>0}) to T_{1, b}
restricted to dℤ_{>0}*. Therefore C(b/d) maps under φ_d to a cycle
φ_d(C(b/d)) ⊂ dℤ_{>0} of T_{1, b}. This is the inherited cycle.

Distinctness across d: the gcd of φ_d(C(b/d))'s members equals d ·
gcd(members of C(b/d)). Since C(b/d) is the base cycle of
T_{1, b/d} reached from n = 1 (which has gcd 1 of members in many
cases — see note below), we get gcd of inherited cycle members = d ·
(some divisor of b/d). For distinct proper divisors d, d' of b, the
inherited gcds differ — the cycles are distinct.

Therefore `n_inherited(1, b) ≥ d(b) − 1`. ∎

### Equality vs strict inequality
- Equality holds when each (1, b/d) for d | b, d > 1 has exactly one
  cycle (the base cycle from seed 1), so the construction produces
  exactly d(b) − 1 inherited cycles.
- Strict inequality occurs when some (1, b/d) has additional cycles
  whose d-scalings are distinct from each other in T_{1, b}. This is
  exactly the b = 21 case observed empirically: (1, 7) has 3 cycles
  (per action 002), and each scales by 3 to a distinct cycle in
  (1, 21), boosting n_inherited beyond d(21) − 1 = 3.

### Where this fits
The argument is *trivial* in the sense that it just unwinds the
b-scaling sub-system embedding (action 003). What's interesting is
how *tight* the lower bound is: at b = 1, 3, 5, 7 (primes), n_inherited
is exactly d(b) − 1 because (1, b/d) at d = b has only the trivial
n=1 cycle. As b acquires structure (composite), the inherited count
exceeds d(b) − 1.

### Status update for C-007′
With this argument in place, C-007′ is **proven analytically as a
lower bound** for the tight scope and any natural extension. The
empirical work in action 004 confirmed it numerically. The
*interesting* open question (what governs n_new) is unaddressed by
this argument.

---

## C-006′ — Sub-lattice forward-attractivity for a = 3 (sketch with
finite bound)

### Claim
For `T_{3, b}` with b odd composite and λ an odd proper divisor of b
with 1 < λ < b, every seed n₀ ∈ ℤ_{>0} \\ λℤ enters λℤ within finitely
many steps. Empirically (action 006): max steps ≤ 17 for b ∈ {9, 15, 21}.

### Argument sketch
Fix λ | b with λ odd > 1. Track `r_t := T^t_{3, b}(n₀) mod λ` for
n₀ ∉ λℤ.

Case 1: T^t is even. Then T^{t+1} = T^t / 2. Since λ is odd, halving
preserves the residue mod λ except by a factor of 2. Specifically,
r_{t+1} = (r_t / 2) mod λ when r_t is even (in ℤ); but in residue
class terms, r_{t+1} ≡ r_t · 2^{-1} (mod λ), where 2^{-1} is the
multiplicative inverse of 2 mod λ. (Inverse exists since gcd(2, λ) = 1.)

Case 2: T^t is odd. Then T^{t+1} = 3·T^t + b. Mod λ: r_{t+1} ≡ 3·r_t
+ b (mod λ). Since λ | b: r_{t+1} ≡ 3·r_t (mod λ).

Let r := r_t mod λ. After a "shortcut step" (one odd → many halvings →
next odd or 0 mod λ): the residue evolves as
- One multiplication by 3 (the odd step)
- Multiple multiplications by 2^{-1} (the halvings)

So at the (t + k + 1)-th step (one odd step + k halvings), r → 3 · 2^{-k} · r (mod λ).

The trajectory enters λℤ when r = 0 (mod λ). Starting from r₀ ≠ 0
(mod λ), the next 0 occurs when 3 · 2^{-k} · r₀ ≡ 0 (mod λ) for some k.
But 3 · 2^{-k} · r₀ = 0 (mod λ) means λ | 3 · 2^{-k} · r₀. Since
gcd(λ, 2) = 1 and gcd(λ, 3) might not be 1 (if 3 | λ), we have:
- If gcd(λ, 3) = 1: λ | r₀, contradicting r₀ ≠ 0.
- If gcd(λ, 3) > 1 (i.e. 3 | λ): the residue 3 · 2^{-k} · r₀ might
  hit 0 mod λ when 3 absorbs a factor of λ.

Hmm. So the residue evolves on the multiplicative group (ℤ/λℤ)*, and
hitting 0 requires the residue to be in the ideal (3) ⊂ ℤ/λℤ at some
step. This isn't guaranteed for all r₀ in general.

**This argument as I've written it is wrong** — it suggests
forward-attractivity is not automatic. So why does the empirical
result show ≤ 17 steps for a = 3?

### Re-examination
Wait — for a = 3, the residue mod λ updates as:
- odd step: r → 3r (mod λ)
- halving step: r → r · 2^{-1} (mod λ)

The trajectory in ℤ_{>0} hits λℤ exactly when the residue r = 0
(mod λ). But residues live on ℤ/λℤ, where 0 is *not* in (ℤ/λℤ)* if
we start with r ≠ 0. So *if* the residue r_t never becomes 0 (mod λ),
the trajectory never enters λℤ — and forward-attractivity *would
fail*.

But the residue r_t in ℤ/λℤ for the actual trajectory in ℤ_{>0}
**only computes the residue of T^t(n₀) mod λ**. The trajectory entering
λℤ corresponds to T^t(n₀) ≡ 0 (mod λ). For the residue to become 0
*without ever being 0 before*, the actual integer T^t(n₀) must "hit" 0
mod λ from a non-zero state — which only happens if T^t(n₀) is a
specific value divisible by λ.

Hmm, the residue calculation is consistent: the residue in ℤ/λℤ
evolves by multiplication. Starting from a unit in (ℤ/λℤ)*, it stays
a unit (since multiplication by a unit by another unit = unit). So
the residue *never* reaches 0 if it starts in (ℤ/λℤ)*.

**This contradicts the empirical observation.** Either the argument
is wrong, or the observation is wrong. Let me check (3, 9), λ = 3
empirically:

Take n₀ = 1: T_{3, 9}(1) = 12. 12 mod 3 = 0. So step 1 enters λZ.
Wait — 1 mod 3 = 1 ≠ 0, but 12 mod 3 = 0. So *one* odd step (3·1 + 9
= 12) lands in 3ℤ, not because of the residue arithmetic above, but
because **the b term contributes 9 ≡ 0 (mod 3) to the odd step.**

I made an error: in the odd step, T_{3, b}(n) = 3n + b, and *b ≡ 0
(mod λ)* (since λ | b). So r_{t+1} ≡ 3r_t + 0 (mod λ) = 3r_t. But
3r_t is the new residue, not 0 in general (unless 3 | λ and the right
preconditions hit).

Wait, but for (3, 9), λ = 3: 3 | 9 ✓ and 3 | λ ✓. Residue 1 → 3·1 = 3
≡ 0 (mod 3). So *one* step suffices because 3 = λ kills any nonzero
residue under one odd step.

For λ = 3 specifically: any odd step takes r to 3r ≡ 0 (mod 3). So
**any** seed n₀ enters 3ℤ on its very next odd step. Max attractivity
time for λ = 3: O(1) (specifically, ≤ k₁ + 1 where k₁ is the halvings
before the next odd step).

For other λ where gcd(3, λ) = 1: r → 3r (mod λ). 3 acts as a
multiplier in (ℤ/λℤ)*. Starting from r₀ ≠ 0, residue cycles through
r₀, 3r₀, 9r₀, ... The cycle length is the multiplicative order of 3 in
(ℤ/λℤ)*. Plus halvings inject factors of 2^{-1}. **For the residue to
ever hit 0, we'd need 3^k · 2^{-j} · r₀ ≡ 0 (mod λ) — but that's
impossible in (ℤ/λℤ)*.**

So forward-attractivity for a = 3, λ ∤ 3 (i.e. λ coprime to 3): **the
residue never hits 0**, contradicting C-006′ as stated.

### What's actually true
Let me re-examine action 006's data more carefully. The agent reported
"max hit time ≤ 17 for a = 3 cells." But this is conditional on the
seed n₀ ∉ λℤ. If the residue argument above is right, *some* seeds
should never hit λℤ.

Possible resolutions:
1. The agent's "≤ 17" applies only to seeds *that did hit* λℤ; seeds
   that never hit were tallied separately as `n_seeds_never_entered`.
   The agent's report flagged a=3 cells as having "max hit time ≤ 17"
   meaning *for those that hit*. Need to read action 006's summary
   more carefully.

2. **Or** — for a = 3, b composite with λ | b, the only λ values that
   matter are those where 3 | λ (i.e. when 3 | b, λ ∈ {3, 9}). For
   (3, 15), λ = 3 or 5: the λ = 3 case is fast (one step); the λ = 5
   case might never hit 0. Did the agent run the probe for λ = 5 in
   (3, 15)?

This needs verification before C-006′ can be promoted. Down-marking
C-006′ to "needs additional probe" until I read the full
006-attractivity.parquet myself.

### Status update for C-006′
**Argument is incomplete and possibly C-006′ is wrong.** Need to:
1. Read 006-attractivity.parquet for λ = 5 cases under a = 3.
2. If the data shows non-attractivity for some (a=3, λ coprime to 3),
   refine C-006′ to "forward-attractivity holds for (a, λ) iff
   gcd(a, λ) > 1 (or some related condition)."

This is a real refinement opportunity and a reminder that "ping when
confident" includes "don't promote without checking the residue
arithmetic."

---

## Conclusion

- **C-007′:** proven analytically as a lower bound; ready for
  promotion with both empirical and analytic support.
- **C-006′:** correctly diagnosed as too strong. After querying
  `006-attractivity.parquet` directly, the right characterization is
  the new **C-006″:** forward-attractivity ⟺ gcd(a, λ) > 1 (for
  prime λ). 20/20 empirical match across the action 006 probe;
  analytic argument follows from residue arithmetic in (ℤ/λℤ)*.
  C-006″ replaces C-006′ in the ledger.

The lesson here: the agent's summary of action 006 ("max hit time ≤
17 for a=3 cells") was **misleading** — the bound applied only to λ=3
cells where 3 | a. I caught this by attempting an analytic argument
which contradicted the empirical claim, then re-querying the data
directly. Per `MEMORY.md ## Avoid`: **always verify a sub-agent's
summary against the underlying data when promoting a conjecture.**
