# 003 — Conjugacy survey and normal form

Companion code: `autoresearch/archive/003-verify.py` (run with `source .venv/bin/activate
&& python autoresearch/archive/003-verify.py`). Every PASS/FAIL claim below corresponds
to a printed line from that script.

---

## Section 1 — Setup

### Family

For positive odd integers `a, b`, define `T_{a,b}: Z>0 -> Z>0` by

    n even:  T_{a,b}(n) = n / 2
    n odd:   T_{a,b}(n) = a*n + b.

Note this is the **un-accelerated** map (single halving step), matching the
phrasing in the action brief. The accelerated form `n -> (a*n+b) / 2^k`
discussed elsewhere in the project is the iterate of this map until the
result is odd; conjugacies of one form lift to the other because they are
exactly the same orbit, observed at different stride.

In-scope grid (per `RESUME.md`): `a ∈ {1, 3, 5, 7}`, `b` odd in `[1, 21]`,
i.e. 4 × 11 = 44 variants.

### What "conjugacy" means here

Two variants `T_{a,b}` and `T_{a',b'}` are **fully conjugate** on `Z>0` iff
there is a bijection `phi: Z>0 -> Z>0` with

    T_{a',b'} ∘ phi  =  phi ∘ T_{a,b}     on all of Z>0.

The image of `phi` must be all of `Z>0` (otherwise it cannot be a
bijection). Under a full conjugacy, the entire dynamical picture (cycles,
basins, divergence) transports from one variant to the other.

The weaker notion that actually shows up in this family is a **sub-system
embedding**: an injection `phi: Z>0 -> Z>0` whose image `phi(Z>0)` is a
**forward-invariant** subset of `Z>0` under `T_{a',b'}`, with

    T_{a',b'} ∘ phi  =  phi ∘ T_{a,b}     on all of Z>0.

This says: "the dynamics of `T_{a,b}` on `Z>0` reappears verbatim inside
the dynamics of `T_{a',b'}` restricted to `phi(Z>0)`." It says **nothing**
about the dynamics of `T_{a',b'}` on `Z>0 \ phi(Z>0)`. In particular,
sub-system embedding **does not** transport convergence claims from
`(a', b')` to `(a, b)` (because the embedded copy is only one stratum of
the larger map), nor from `(a, b)` to `(a', b')` (because the complement
of the image is dynamically independent).

This distinction is load-bearing for the atlas: conflating it would let
us "re-use" the (3, 1) classification for (3, 3), (3, 5), (3, 7), …, but
those variants have additional orbits on integers coprime to the scaling
factor, and those orbits are exactly where novelty lives.

---

## Section 2 — Substitutions surveyed

Throughout this section `lambda` (or `alpha`) denotes a positive odd
integer, and `phi(n) = lambda * n` means the substitution that multiplies
state by `lambda`.

### 2.1  Trivial b-scaling: `phi(n) = lambda * n`

**Algebra.** For even `n` (so `lambda * n` is also even since `lambda` is
odd):

    T_{a, lambda*b}(lambda * n)  =  (lambda * n) / 2  =  lambda * (n/2)
                                 =  lambda * T_{a,b}(n).

For odd `n` (so `lambda * n` is odd):

    T_{a, lambda*b}(lambda * n)  =  a * (lambda * n) + lambda * b
                                 =  lambda * (a*n + b)
                                 =  lambda * T_{a,b}(n).

So `phi` intertwines `T_{a, b}` and `T_{a, lambda*b}` on all of `Z>0`.

**But it is not a bijection of `Z>0`** — its image is `lambda * Z>0`,
which is a proper subset for `lambda > 1`. This is a sub-system embedding:
`(a, lambda*b)`'s dynamics on multiples of `lambda` is a faithful copy of
`(a, b)`'s dynamics on all of `Z>0`.

**Forward-invariance check.** Is `lambda * Z>0` forward-invariant under
`T_{a, lambda*b}`? Yes:

  - even multiple of `lambda`: dividing by 2 keeps the factor `lambda`
    (since `lambda` is odd, `lambda * n` even means `n` even).
  - odd multiple of `lambda`: `a * (lambda*n) + lambda*b = lambda*(a*n+b)`,
    a multiple of `lambda`.

So once an orbit enters `lambda * Z>0`, it stays there, and on that fiber
it is a copy of `T_{a, b}`.

**Status:** sub-system embedding (one-way). Not a full conjugacy —
`T_{a, lambda*b}` has dynamics on `Z>0 \ lambda * Z>0` that is wholly
absent from `T_{a, b}`.

**In-scope pairs produced:**

| (a, b) parent | embeds into (a, lambda*b) for lambda = | producing children in scope |
|---|---|---|
| (1, 1) | 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 | (1, 3) … (1, 21) |
| (3, 1) | 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 | (3, 3) … (3, 21) |
| (5, 1) | 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 | (5, 3) … (5, 21) |
| (7, 1) | 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 | (7, 3) … (7, 21) |
| (3, 3) | 3, 5, 7 | (3, 9), (3, 15), (3, 21) |
| (3, 5) | 3 | (3, 15) |
| (3, 7) | 3 | (3, 21) |
| (5, 3) | 3, 5, 7 | (5, 9), (5, 15), (5, 21) |
| (5, 5) | 3 | (5, 15) |
| (5, 7) | 3 | (5, 21) |
| (7, 3) | 3, 5, 7 | (7, 9), (7, 15), (7, 21) |
| (7, 5) | 3 | (7, 15) |
| (7, 7) | 3 | (7, 21) |

Symmetric rows for `a = 1, 5, 7`. Note: `(3, 9)` is reached from both
`(3, 1)` (via `lambda=9`) and `(3, 3)` (via `lambda=3`); the embeddings
compose. So `(3, 9)`'s `9*Z` fiber mirrors `(3, 1)` on `Z`, while its
`3*Z` fiber (a strictly larger set) mirrors `(3, 3)` on `Z`.

**Simulation verification.** From `003-verify.py` § 1 / § 2b:

  - `(3, 1) -> (3, 3)` via `n -> 3n`, seeds `{1, 2, 3, 5, 7, 11}`,
    80 steps: PASS.
  - `(3, 1) -> (3, 5)` via `n -> 5n`, seeds `{1, 2, 4, 7, 9}`, 80 steps:
    PASS.
  - `(5, 1) -> (5, 3)` via `n -> 3n`, seeds `{1, 2, 3, 4, 7}`, 80 steps:
    PASS.
  - `(7, 1) -> (7, 3)` via `n -> 3n`, seeds `{1, 2, 4, 5}`, 80 steps:
    PASS.
  - `(3, 3) -> (3, 9)` via `n -> 3n`, seeds `{1, 2, 3, 5, 7}`, 80 steps:
    PASS.

### 2.2  GCD reduction near `(a=3, b=3)`

The user's hint: on odd multiples of 3, `T_{3,3}(n) = 3n + 3 = 3(n+1)`.
Does this give a conjugacy to `(3, 1)` on `Z`?

**Answer: sub-system embedding only**, and it's exactly the `lambda = 3`
case of § 2.1. Let `phi(n) = 3n`. Then `T_{3,3}(phi(n)) = phi(T_{3,1}(n))`
for all `n` (verified, 120 steps, seeds `{1, 2, 3, 5, 7, 11, 27}`: PASS).

The crucial check is whether `3 * Z>0` is forward-invariant under
`T_{3,3}` on the **whole** `Z>0` — i.e. whether starting from a non-multiple
of 3 you can avoid entering `3Z` forever, or you must enter it. Either
direction tells us something:

  - if `3Z` is forward-invariant *from non-3Z too*, then `T_{3,3}` would
    just be `T_{3,1}` in disguise plus an irrelevant fiber;
  - if non-3Z is *also* forward-invariant, the two halves are independent
    sub-systems;
  - in between (orbits cross fibers) there is genuine novelty.

Trace from `003-verify.py` § 2:

    n0=1 (1 mod 3): [1, 6, 3, 12, 6, 3, 12, 6, 3, ...]
    n0=5 (2 mod 3): [5, 18, 9, 30, 15, 48, 24, 12, 6, ...]
    n0=7 (1 mod 3): [7, 24, 12, 6, 3, 12, 6, 3, 12, ...]

Every non-3Z seed in this sample falls into 3Z within a few steps and
stays there. So `3Z` is **forward-attracting** for `T_{3,3}`, but it is
not forward-invariant in the strict sense (initial points outside 3Z
*enter* 3Z, but they were never in `phi(Z>0)`'s image so this does not
threaten the embedding — it just means non-3Z points are *transient*).

Empirically `T_{3,3}` looks like "a transient pre-period for non-3Z
seeds, then `T_{3,1}` dynamics on 3Z." If that observation generalizes
to all of `Z>0` (a sweep question, not a substitution question), then in
fact `T_{3,3}` would be **dynamically equivalent to `T_{3,1}`** in the
sense of asymptotic classification (cycles and divergence on 3Z determine
all eventual behavior), even though it is not strictly conjugate.

This is exactly the kind of statement the conjecture ledger should hold:
"For `(3, b)` with `b = 3*b0`, every orbit eventually enters `3Z` and from
there obeys `(3, b0)` dynamics." The substitution proves it on `3Z`; a
**sweep** is required to certify that all non-3Z seeds are transient.
**Open question — see § 5.**

### 2.3  Periodicity `(a, b) <-> (a, b + 2*a*m)`

**Claim under test:** `phi(n) = n` (identity) intertwines `T_{a,b}` and
`T_{a, b+2*a*m}`.

**Algebra.** Even branch: identical. Odd branch: `a*n + b` versus
`a*n + b + 2*a*m`. They differ by `2*a*m`, which is non-zero for `m ≠ 0`.
Identity does not work.

Could a non-identity `phi` save it? An odd-branch shift of `2*a*m`
followed by the same number of even halvings would give a state shift of
`2*a*m / 2^j = a*m / 2^{j-1}`, which is not generally an integer, so no
clean periodicity emerges. Numerically:

    (3, 1) from 1: [1, 4, 2, 1, 4, 2, 1, ...]
    (3, 7) from 1: [1, 10, 5, 22, 11, 40, 20, 10, ...]

The two trajectories diverge on the first odd step. (`003-verify.py` § 3
FAIL, as expected — it was a counterexample probe.)

**Status:** no conjugacy via `b`-shifts. Different `b mod 2*a` classes
are dynamically distinct in general.

### 2.4  Branch-swap / parity reflection

**`phi(n) = -n` on `Z`.** With Python `//` rounding toward `-∞`, parity
is preserved under negation (`-odd` is odd, `-even` is even). For odd
`n`:

    T_{a, b'}(-n) = a*(-n) + b' = -a*n + b'
    -T_{a, b}(n) = -(a*n + b) = -a*n - b

so we need `b' = -b`. For even `n`: `(-n)/2 = -(n/2)`, fine. So on `Z`,
`phi(n) = -n` is a full conjugacy `T_{a,b} <-> T_{a,-b}`. Verified
numerically in `003-verify.py` § 4 (PASS).

**In-scope implication: none.** Our family has `b > 0` by stipulation;
sign-flip leaves the family. Worth recording for the broader phase
diagram (it equates the b > 0 atlas with a hypothetical b < 0 atlas) but
contributes zero in-scope identifications.

**`phi(n) = c - n` on `Z>0`.** This requires `c - n > 0` for relevant
`n`, so it is a bijection at most on `[1, c-1]`. For it to intertwine the
maps: even `n` goes to `c - n/2` and we need parity of `c - n` to match
parity of `n` — i.e. `c` even. Then on even `n`, `T_{a,b'}(c - n) =
(c - n)/2`, while `phi(T_{a,b}(n)) = c - n/2`. Setting equal:
`(c - n)/2 = c - n/2`, i.e. `c/2 = c`, i.e. `c = 0`. So `phi(n) = -n`,
already covered.

**Status:** no in-scope identifications from parity reflection.

### 2.5  Affine substitution `phi(n) = alpha*n + beta`

Take `phi: Z>0 -> Z>0` with `alpha, beta` integer, `alpha > 0`. To
intertwine the two-branch map you must match parities branch-by-branch.

**Even branch.** `T_{a,b}(n) = n/2` on even `n`. Need `phi(n)` to be
even (so `T_{a',b'}` takes its even branch on `phi(n)`):

    parity(alpha*n + beta) == parity(n)   for all n
    ⟹  alpha odd  AND  beta even.

Then `T_{a',b'}(phi(n)) = (alpha*n + beta) / 2` and `phi(T_{a,b}(n)) =
phi(n/2) = alpha*n/2 + beta`. Setting equal:

    (alpha*n + beta)/2 = alpha*n/2 + beta
    ⟹  beta/2 = beta
    ⟹  beta = 0.

**Odd branch.** Now `phi(n) = alpha*n` with `alpha` odd. For odd `n`:

    T_{a',b'}(alpha*n) = a' * alpha * n + b'
    phi(T_{a,b}(n))    = alpha * (a*n + b) = alpha*a*n + alpha*b
    ⟹  a' = a,  b' = alpha * b.

**Conclusion.** The complete classification of integer affine
substitutions `phi(n) = alpha*n + beta` with `alpha, beta in Z`,
`alpha > 0`, that intertwine `T_{a,b}` with `T_{a',b'}` is:

    beta = 0,  alpha odd ≥ 1,  a' = a,  b' = alpha * b.

`alpha = 1` is the trivial identity. `alpha ≥ 3` is the b-scaling
sub-system embedding from § 2.1. **There is no integer affine
substitution that changes `a`, and no integer affine substitution that
gives a bona fide full conjugacy of `Z>0` for `alpha > 1`.**

Verified in `003-verify.py` § 5: all `alpha`-odd, `beta=0` cases PASS;
the `phi(n) = n + 2` probe FAILs, confirming `beta ≠ 0` breaks parity.

### 2.6  Summary table

| substitution | algebra | status | in-scope effect |
|---|---|---|---|
| `phi(n) = lambda*n`, lambda odd ≥ 1 | (a,b) ↔ (a, lambda*b) | sub-system embedding (lambda > 1); identity (lambda = 1) | each `(a, lambda*b)` in scope embeds `(a, b0)` for each odd `b0 = b/lambda` it divides |
| `phi(n) = n + 2*a*m` (identity) | none | fails | no identifications |
| `phi(n) = -n` on Z | (a,b) ↔ (a,-b) | full conjugacy on `Z` | leaves `b > 0` family; no in-scope effect |
| `phi(n) = c - n` on Z>0 | reduces to `phi(n) = -n` after solving constraints | none | no in-scope effect |
| `phi(n) = alpha*n + beta`, integer affine | forces `beta = 0`, `alpha` odd, gives § 2.1 | sub-system embedding | same as § 2.1 |

---

## Section 3 — Normal form

### Finding

**There are no nontrivial full conjugacies of `T_{a,b}` on `Z>0` within
this family for `a ∈ {1, 3, 5, 7}`, `b` odd in `[1, 21]`.** Every
substitution we identified is either trivial (identity), out-of-domain
(sign-flip), or a strict sub-system embedding (`b`-scaling).

This is a real finding, not a punt. It means: the 44-cell atlas grid is
**not** quotiented by any full conjugacy. Each `(a, b)` is its own
dynamical equivalence class on the level of "do all orbits converge / is
there an extra cycle / is some orbit unbounded up to horizon."

### Proposed `normal_form(a, b)`

Given the above, the strict-conjugacy normal form is the identity:

    def normal_form(a, b):
        return (a, b)        # no nontrivial full conjugacies in scope

Every cell in the in-scope grid is its own canonical representative.

### Proposed `subsystem_parent(a, b)`

The useful structural info is the sub-system parent: for each `(a, b)`
with `b > 1`, the smallest odd `b0` such that `b = lambda * b0` for some
odd `lambda > 1` (so that `(a, b)` on `lambda*Z` mirrors `(a, b0)` on
`Z`). When `b = 1`, no parent.

    def subsystem_parent(a, b):
        # smallest b0 < b such that b = lambda*b0 with odd lambda > 1
        best = None
        for lam in range(3, b+1, 2):
            if b % lam == 0:
                b0 = b // lam
                if b0 % 2 == 1 and (best is None or b0 < best[1]):
                    best = (a, b0)
        return best          # or None

(Code: `archive/003-verify.py`.)

### Canonical-representative table

44 cells. `normal_form(a, b) = (a, b)` always. The third column lists
the smallest `(a, b0)` whose dynamics is embedded inside `(a, b)` via
`n -> (b/b0) * n` (`subsystem_parent`); an em-dash means none in scope.

| a | b | normal_form | sub-system parent | reason |
|--:|--:|--:|---|---|
| 1 | 1 | (1, 1) | — | base |
| 1 | 3 | (1, 3) | (1, 1) | n -> 3n |
| 1 | 5 | (1, 5) | (1, 1) | n -> 5n |
| 1 | 7 | (1, 7) | (1, 1) | n -> 7n |
| 1 | 9 | (1, 9) | (1, 1) | n -> 9n; also (1,3) via n -> 3n |
| 1 | 11 | (1, 11) | (1, 1) | n -> 11n |
| 1 | 13 | (1, 13) | (1, 1) | n -> 13n |
| 1 | 15 | (1, 15) | (1, 1) | n -> 15n; also (1,3) via 5n, (1,5) via 3n |
| 1 | 17 | (1, 17) | (1, 1) | n -> 17n |
| 1 | 19 | (1, 19) | (1, 1) | n -> 19n |
| 1 | 21 | (1, 21) | (1, 1) | n -> 21n; also (1,3) via 7n, (1,7) via 3n |
| 3 | 1 | (3, 1) | — | classical Collatz; base |
| 3 | 3 | (3, 3) | (3, 1) | n -> 3n |
| 3 | 5 | (3, 5) | (3, 1) | n -> 5n |
| 3 | 7 | (3, 7) | (3, 1) | n -> 7n |
| 3 | 9 | (3, 9) | (3, 1) | n -> 9n; also (3,3) via 3n |
| 3 | 11 | (3, 11) | (3, 1) | n -> 11n |
| 3 | 13 | (3, 13) | (3, 1) | n -> 13n |
| 3 | 15 | (3, 15) | (3, 1) | also (3,3) via 5n, (3,5) via 3n |
| 3 | 17 | (3, 17) | (3, 1) | n -> 17n |
| 3 | 19 | (3, 19) | (3, 1) | n -> 19n |
| 3 | 21 | (3, 21) | (3, 1) | also (3,3) via 7n, (3,7) via 3n |
| 5 | 1 | (5, 1) | — | base; known wild |
| 5 | 3 | (5, 3) | (5, 1) | n -> 3n |
| 5 | 5 | (5, 5) | (5, 1) | n -> 5n |
| 5 | 7 | (5, 7) | (5, 1) | n -> 7n |
| 5 | 9 | (5, 9) | (5, 1) | also (5,3) via 3n |
| 5 | 11 | (5, 11) | (5, 1) | n -> 11n |
| 5 | 13 | (5, 13) | (5, 1) | n -> 13n |
| 5 | 15 | (5, 15) | (5, 1) | also (5,3) via 5n, (5,5) via 3n |
| 5 | 17 | (5, 17) | (5, 1) | n -> 17n |
| 5 | 19 | (5, 19) | (5, 1) | n -> 19n |
| 5 | 21 | (5, 21) | (5, 1) | also (5,3) via 7n, (5,7) via 3n |
| 7 | 1 | (7, 1) | — | base |
| 7 | 3 | (7, 3) | (7, 1) | n -> 3n |
| 7 | 5 | (7, 5) | (7, 1) | n -> 5n |
| 7 | 7 | (7, 7) | (7, 1) | n -> 7n |
| 7 | 9 | (7, 9) | (7, 1) | also (7,3) via 3n |
| 7 | 11 | (7, 11) | (7, 1) | n -> 11n |
| 7 | 13 | (7, 13) | (7, 1) | n -> 13n |
| 7 | 15 | (7, 15) | (7, 1) | also (7,3) via 5n, (7,5) via 3n |
| 7 | 17 | (7, 17) | (7, 1) | n -> 17n |
| 7 | 19 | (7, 19) | (7, 1) | n -> 19n |
| 7 | 21 | (7, 21) | (7, 1) | also (7,3) via 7n, (7,7) via 3n |

The four "base" representatives (`b = 1` row) are the only cells with no
sub-system parent in scope.

---

## Section 4 — Implications for the atlas

### 4.1  Which pairs reduce under the normal form?

**None** — `normal_form` is the identity. The 44-cell grid does not
collapse under full conjugacy.

### 4.2  Sub-system relationships and how to state them

The sub-system embedding `(a, b) ↪ (a, lambda*b)` lets us transport
**lower bounds** on the structure of `(a, lambda*b)` from `(a, b)`, but
not upper bounds. Concretely:

- **Cycles:** every cycle of `T_{a,b}` lifts (via `n -> lambda*n`) to a
  cycle of `T_{a, lambda*b}` on `lambda*Z`. So if the cycle inventory of
  `(3, 1)` is `{the 1->4->2->1 cycle}`, then `(3, lambda)` has at least
  `{the lambda -> 4*lambda -> 2*lambda -> lambda cycle}` for every odd
  `lambda`. **The converse is false:** `(3, lambda)` may have additional
  cycles on integers coprime to `lambda` that don't come from `(3, 1)`.

- **Divergence:** if `(a, b)` has an unbounded orbit from some seed `n0`,
  then `(a, lambda*b)` has an unbounded orbit from `lambda*n0`. The
  converse is again false.

- **Universal convergence:** "all `Z>0` orbits of `(a, b)` reach the
  trivial cycle" does **not** imply the same for `(a, lambda*b)` —
  because `(a, lambda*b)` has dynamics on `Z>0 \ lambda*Z` that the
  embedding tells us nothing about. (Exception in spirit, not in proof:
  if a sweep observes that all non-`lambda*Z` seeds of `(a, lambda*b)`
  fall into `lambda*Z` within finitely many steps, then atlas-level
  classification *can* be transported. That's the (3, 3) story above —
  but it is a sweep result, not a substitution result.)

**Recommended atlas phrasing**, using `(3, 3)` as exemplar:

> "The map `T_{3,3}` restricted to multiples of 3 is conjugate to
> `T_{3,1}` via `n -> 3n`, so its dynamics on `3*Z` mirrors classical
> Collatz exactly. Its dynamics on integers coprime to 3 is a separate
> question: empirically [from sweep 001] every coprime seed up to S=10⁴
> enters `3*Z` within T=___ steps and never returns. Subject to that
> sweep observation, `T_{3,3}`'s asymptotic behavior on `Z>0` reduces to
> `T_{3,1}`'s. The reduction is not a conjugacy."

### 4.3  Conjecture-ledger guidance

When reporting results from the opening sweep:

1. Each of the 44 cells is reported on its own. None is suppressed as
   "covered by another cell."
2. For each cell `(a, b)` with `b > 1`, the report includes an explicit
   "sub-system parent" annotation if one exists in scope (per the
   table above). This is bookkeeping — it warns the reader that some
   of `(a, b)`'s cycles are inherited.
3. Any cycle discovered in `(a, b)` is checked against
   `lambda * cycles_of((a, b/lambda))` for every odd `lambda > 1`
   dividing `b`. Cycles that appear in this lifted set are tagged
   "inherited from `(a, b/lambda)`"; cycles that don't are tagged "new".
   **The 'new' tag is the atlas's primary novelty signal for cycles.**
4. Apparent divergence in `(a, b)` is checked likewise: if the divergent
   seed is `lambda * n0` and `(a, b/lambda)` is also classified
   apparently-divergent from `n0`, the divergence is inherited; else
   genuinely new.

---

## Section 5 — Open questions

1. **Forward-attractivity of `lambda*Z` under `T_{a, lambda*b}`.** The
   substitution argument shows `lambda*Z` is forward-invariant. The
   numerical experiments in § 2.2 suggest `lambda*Z` is also
   forward-attracting (every non-`lambda*Z` seed enters `lambda*Z`
   within a few steps and stays). If true universally, the asymptotic
   classification of `(a, lambda*b)` reduces to that of `(a, b)`. But
   this is a **sweep claim**, not a substitution claim, and needs
   action 001's data to settle. Suggested check: in the sweep, log for
   each seed `n0` and each cell `(a, b)` the smallest `t` with
   `T_{a,b}^t(n0) ∈ lambda*Z` for each odd `lambda | b`. If finite for
   every seed up to S, the reduction holds within sweep horizon.

2. **Higher-degree substitutions.** We restricted to integer affine
   `phi`. Quadratic or piecewise-affine `phi` (e.g. `phi` depending on
   `n mod 4`) could in principle give exotic conjugacies, especially
   ones that swap the parity branches. Worth exploring if the atlas
   surfaces unexplained dynamical similarities between cells that the
   `b`-scaling embedding does not connect.

3. **Acceleration-aware conjugacy.** The accelerated map
   `n -> (a*n+b) / 2^{nu_2(a*n+b)}` (CONFIG's preferred form) admits the
   same conjugacies as the un-accelerated map, since the orbits coincide
   pointwise. But the accelerated map may admit additional
   conjugacies that re-stride odd-step indices. This is a subtle point
   not pursued here. If sweep 001 shows the accelerated and
   un-accelerated atlases agree cell-for-cell on classification, this is
   moot; if not, revisit.

4. **Cross-`a` identifications.** The affine analysis proves no integer
   affine `phi` changes `a`. But are there `a`-dependent changes of
   variable across the **family** (e.g. via 2-adic conjugacy as in
   Lagarias' work) that would equate `(3, b)` and `(5, b')` dynamics in
   some abstract sense? Outside the scope of the integer-substitution
   survey, but worth flagging for the broader literature review.

5. **Treatment of `a = 1`.** `T_{1, b}` is `n/2` on even, `n + b` on
   odd. The orbit of any odd `n` is `n -> n+b -> ... ` and `n+b` is
   even (sum of two odds), so the next step halves. So one full odd
   step gives `(n+b)/2` (or further halvings). Convergence/cycle
   behavior of this much simpler map is presumably well-understood; the
   conjugacies above all apply trivially. Action 002 (analytic cycle
   catalog) should cover this.

---

## Appendix — Code map

`archive/003-verify.py` has six labelled sections matching § 2.1–2.5
and § 3:

  - § 1: b-scaling sub-system embedding (PASS for 5 cases, 80 steps each)
  - § 2: GCD reduction (3, 3) on 3Z (PASS, 120 steps; plus trajectory
    trace from non-3Z showing transient entry into 3Z)
  - § 2b: chained b-scaling (3, 3) -> (3, 9) (PASS, 80 steps)
  - § 3: identity attempt for (3, 1) vs (3, 7) (FAIL, expected)
  - § 4: sign reflection on Z (PASS, 40 steps signed)
  - § 5: affine cases — odd alpha, beta=0 (5 PASS); beta=2 probe (FAIL)
  - normal-form table (44 rows)
