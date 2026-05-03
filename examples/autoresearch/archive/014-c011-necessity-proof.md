# 014 — Closed-form proof of C-011's necessity (for b odd)

Author: main.

## Claim
For the family `T_{a, b}` with **a, b positive odd integers**, every
primitive cycle of T_{a, b} of shortcut length L corresponds to a
triple (L, K) with **b | (2^K − a^L)**, where K is the sum of halving
counts in one period of the cycle.

(The complementary direction — that the divisibility condition yields
cycles — was already addressed in C-011's sufficient form: every
composition of K into L positive parts produces an integer n₀ via the
cycle equation when b | (2^K − a^L).)

## Setup
A cycle of T_{a, b} of shortcut length L visits L odd values
m₀, m₁, ..., m_{L−1} in cyclic order, with the i-th odd step taking
m_i to m_{i+1 mod L} via:

    m_i → a·m_i + b → /2 (k_{i+1} times) → m_{i+1}

i.e. `a·m_i + b = m_{i+1} · 2^{k_{i+1}}` with k_{i+1} ≥ 1.

Telescoping over one full period (L odd steps, K = Σ k_i halvings):

    m₀ · 2^K = a^L · m₀ + b · S(k⃗)

where S(k⃗) is a positive integer sum of products of powers of 2 and
powers of a, depending on the composition (k₁, ..., k_L). Equivalently:

    m₀ · (2^K − a^L) = b · S(k⃗).      (*)

For a primitive cycle, **gcd of all members equals 1**.

## Proof
Suppose m₀, m₁, ..., m_{L−1} is a primitive cycle. Let
g := gcd(m₀, b). Since b is odd, every prime divisor of g is odd.

We claim g divides every member m_i. Induction on i:
- Base: g | m₀ by definition.
- Step: assume g | m_i. Then g | a·m_i (since a is integer) and we
  need g | b for the next step. **Since g | b by definition, g |
  a·m_i + b.** Therefore g | m_{i+1} · 2^{k_{i+1}}. Since g is odd
  (every prime divisor odd, and g divides odd number m_i which is
  odd), gcd(g, 2^{k_{i+1}}) = 1, so **g | m_{i+1}**.

Therefore g divides every cycle member m_i. By primitivity, gcd of
members = 1, so g = 1.

Hence **gcd(m₀, b) = 1**.

From (*): `b · S(k⃗) = m₀ · (2^K − a^L)`. Since gcd(m₀, b) = 1:

    b | m₀ · (2^K − a^L)  AND  gcd(b, m₀) = 1
    ⟹ b | (2^K − a^L).    ∎

## Where this leaves C-011

With the proof, write `m := (2^K − a^L) / b`. The cycle equation (*)
becomes:

    m · n₀ = S(k⃗).      (**)

**Necessity** (proven above for b odd): every primitive cycle's (L, K)
satisfies b | (2^K − a^L), i.e. m is a positive integer.

**Sufficiency conditions for a given (L, K, composition):**

- *Strong case (m = 1):* every composition yields integer n₀ = S(k⃗)
  for free. Whether the resulting n₀ is the entry point of a
  *primitive* cycle depends only on rotation-orbit non-degeneracy
  (Burnside applies). C-008's (3, 13, L=5, K=8) is exactly this: m =
  13/13 = 1, so all 35 compositions give cycles, deduping to 7.
- *Weak case (m > 1):* additional constraint **m | S(k⃗)**. Only those
  compositions whose S-value is divisible by m yield integer n₀;
  among those, primitivity is again a rotation-orbit condition.

Concrete example of the weak case: (a=3, b=19, L=2, K=8). m =
(2⁸ − 3²)/19 = 247/19 = 13. The cycle equation requires 13 | S(k₁)
= 3 + 2^{k₁}. So 2^{k₁} ≡ −3 ≡ 10 (mod 13). The order of 2 mod 13 is
12, and 2^k mod 13 takes the values {2, 4, 8, 3, 6, 12, 11, 9, 5,
10, 7, 1}. So 2^{k₁} ≡ 10 at k₁ = 10 — outside the K = 8 budget.
Therefore (3, 19, L=2, K=8) yields **no** primitive cycles, consistent
with the sweep finding only the L=1 cycle for (3, 19).

**Bijection (refined):**

> For odd a, b: primitive cycles of T_{a, b} of shortcut length L are
> in bijection with rotation orbits of compositions
> `(k₁, ..., k_L) ⊢ K` such that:
> 1. `b | (2^K − a^L)` (so `m = (2^K − a^L)/b` is a positive integer),
> 2. `m | S(k⃗)` where `S(k⃗) = a^{L−1} + a^{L−2}·2^{k_{L-1}} + ... +
>    2^{k_{L-1}+...+k_1}`,
> 3. the composition is primitive (not rotation-symmetric to shorter L).

When m = 1, condition (2) is vacuous and conditions (1) + (3) suffice.
Empirically, all 64 primitive cycles in our 153-cycle atlas are in the
m = 1 case.

This is the **closed-form classification of primitive cycles** for any
positive odd (a, b).

## Combined with b-scaling inheritance
Action 003's b-scaling embedding gives: every odd divisor d of b yields
inherited cycles via φ_d: ℤ → ℤ, n → d·n. Specifically, every
*primitive* cycle of T_{a, b/d} maps under φ_d to a *non-primitive*
(gcd ≥ d) cycle of T_{a, b} on dℤ.

Therefore, the **full** cycle inventory of T_{a, b} for odd a, b is:

> **Primitive cycles**: corresponding to (L, K, composition) triples
> with b | (2^K − a^L) and the primitivity condition.
>
> **Inherited cycles**: for each odd d > 1 with d | b, the d-scaled
> images of primitive cycles of T_{a, b/d}.

This recursively decomposes every cycle in the atlas into closed-form
pieces, recovering the full empirical decomposition observed in tight
scope.

## Implications

1. **The cycle problem reduces to number theory** — specifically, to
   characterizing the divisibility relation b | (2^K − a^L). For each
   (a, b) with b odd, the primitive (L, K) tuples are determined by
   the multiplicative orders of 2 and a in (ℤ/bℤ)*.

2. **For a = 1**: 2^K ≡ 1 (mod b) iff K is a multiple of ord_b(2). So
   primitive (L, K) for (1, b) are at K ∈ {ord_b(2), 2·ord_b(2), ...}.
   Connects directly to action 013's investigation of n_new(1, b).

3. **For prime b**: by Fermat's Little Theorem, a^{b-1} ≡ 1 (mod b)
   when gcd(a, b) = 1. So 2^K ≡ a^L (mod b) is solvable iff there
   exist K, L with 2^K · a^{-L} ≡ 1 (mod b), i.e. (2 · a^{-1})^?
   structure. For primes b coprime to 2a, the (L, K) lattice is dense
   modulo (b-1).

4. **Tractable cousins.** The divisibility condition is what makes a
   variant "tractable" in the sense the brief asks for. (a, b) where
   ord_b(2) is small gives few (L, K) tuples and possibly a small
   finite cycle set. The condition `2^K = a^L + b` has small-solution
   instances (like (3, 5, L=1, K=3): 2³ − 3 = 5 ✓ — wait that's
   2^K = a^L + b at K=3, L=1: 8 = 3 + 5 ✓ — yes; and indeed (3, 5)
   has the L1 cycle n=1 since 1·(2^3 − 3) = 5·1, m₀ = 1.)

This is the structural backbone of the atlas.
