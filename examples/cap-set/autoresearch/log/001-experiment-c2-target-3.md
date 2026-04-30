# exp 001 — c2-target = 3 priority

## What & why
First non-trivial priority. Hypothesis: prefer elements with count_of_2 = 3
(because n/3 ≈ 2.67, and balancing the multiset puts elements in a "rich"
zone that can pack densely without 3-APs). Falsifier: if cap_set_size is
not strictly > 256, reject.

## Done
Tested across hundreds of priority candidates via batch tester
(autoresearch/archive/000-batch-tester.py, called from 001-..023-..py).
Wrote priority.py = -|c2 - 3| and ran the official eval.

## Result
- STATUS: correct
- cap_set_size: **448**
- Delta vs best (256): **+192** → keep
- eval_seconds: 0.11

This is robust:
- `-abs(c2-3)` and `-(c2-3)^2` both give 448.
- Cap composition: 320 elements with c2=3, 128 with c2=2 (no c2=4).
- Multiset distribution favours symmetric splits like (3,2,3), (2,3,3),
  (4,1,3), (1,4,3), (5,0,3), (0,5,3) for the c2=3 bucket and (3,3,2),
  (4,2,2), (2,4,2), (5,1,2), (1,5,2), (6,0,2), (0,6,2) for the c2=2 bucket.
- No tiebreaker (random or structural) ever beats 448 — the natural
  itertools.product lex order is the unique strong attractor.

## Reasoning
Massive jump from baseline. The c2-target encodes a combinatorial
"balanced count" hint: the cap should have elements where the number of 2's
matches n/3, which biases the picks towards multiset shapes that minimise
cross-element AP completions.

The 448-cap is **maximal** — exhaustive check (archive/018-extend-448.py)
showed there are zero non-forbidden, non-cap elements after greedy
completes. Random restart greedies (200 trials with shuffled orders) max
out at 272; with c2=3 prefix + random tiebreak at 287. So the natural lex
order *within* c2=3 is structurally critical, not interchangeable.

This is a strong local maximum. Beating 448 will require a fundamentally
different priority structure (non-c2 dominant, or an explicitly-encoded
construction).

## Next
- Add to LESSONS pending: "c2 ≈ n/3 target with natural lex tiebreak gives
  a cap-set local maximum that beats baseline by ~75%." Need a second keep
  with the same falsifier to promote.
- Strategy escalation: move to L3 (structural changes) and L4 (radical
  rethinking) — try hardcoded known caps, tensor products, code-based
  constructions.
- Open question: which priority structure breaks the 448 ceiling?

## Linked
- archive/000-batch-tester.py
- archive/001-sweep-basic.py
- archive/002-sweep-c2.py through archive/023-funsearch-pub.py
- archive/011-cap-448.txt — the 448 cap elements
- archive/018-extend-448.py — maximality check
