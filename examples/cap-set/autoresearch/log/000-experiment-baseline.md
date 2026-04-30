# exp 000 — baseline (priority returns 0.0)

## What & why
Pin the starting metric for the cap-set greedy with the trivial priority
(constant 0.0). Verify the eval pipeline works end-to-end and the verifier
accepts the produced set.

## Done
Ran `CAP_SET_N=8 python problem/eval.py` against the scaffolded
`problem/priority.py` returning `0.0` for every element.

## Result
- STATUS: correct
- n: 8
- cap_set_size: 256
- eval_seconds: 0.02
- Environment fingerprint: macOS Darwin 24.5.0, Python 3 + stdlib (numpy
  available but not imported by baseline).

## Reasoning
With a constant priority, Python's stable sort preserves the
`itertools.product(range(3), repeat=8)` lex order. Greedy then walks
elements lex order; the chosen set turns out to coincide with `{0,1}^8`,
which is a valid cap because three distinct points x,y,z ∈ {0,1}^n cannot
satisfy x+y+z ≡ 0 (mod 3) coord-wise without all three coinciding (in each
coord {0,1} sums to 0 only if all three are 0; sums to 3 only if all three
are 1 — both force x=y=z). Size = 2^n = 256.

The PROMPT predicted 35–50; the actual baseline is 256. The eval pipeline
is verified and the contract is operable. Strategy level 1 starts with
heuristics that should at least preserve this {0,1}^n structure and ideally
push above it toward 496+ (Edel) and 512 (FunSearch).

## Next
- Activate frozen contract.
- First dispatch: Queue #1 — Hamming-weight-based priority that suppresses
  elements with many 2's, expected to reproduce ~256 as a cleanliness check
  before more interesting priorities.

## Linked
- (no archive artefacts; baseline is config-only)
