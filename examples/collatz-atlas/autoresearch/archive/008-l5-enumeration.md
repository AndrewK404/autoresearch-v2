# 008 — Algebraic enumeration of (3, 13) L=5 cycles

Companion script: `autoresearch/archive/008-l5-enumeration.py`. 
Source comparison: `autoresearch/archive/005-l4plus-catalog.md` (the 7 sweep cycles).

## Setup

For T_{a, b} with a=3, b=13, the shortcut equation at L=5, T-period=13 is

    n0 * (2^K - a^L) = b * sum_{i=0..L-1} a^{L-1-i} * 2^{k_1+...+k_i}

where K = sum(k_i) = T-period - L = 13 - 5 = 8 and each k_i >= 1.
With a=3, b=13: 2^8 - 3^5 = 256 - 243 = 13. The factor 13 cancels and

    n0 = 81 + 27*2^{k1} + 9*2^{k1+k2} + 3*2^{k1+k2+k3} + 2^{k1+k2+k3+k4}.

So *every* composition of 8 into 5 positive parts yields a positive integer n0.
A valid cycle further requires:
- n0 is **odd** (entry point of an odd step), and
- Simulation of T_{3,13} from n0 returns to n0 in exactly 13 T-steps with the
  predicted halving pattern (k1, ..., k5).

Cyclic rotations of the halving vector yield the same cycle (5 rotations per
cycle), so we deduplicate by member set.

## Per-composition table

| (k1,k2,k3,k4,k5) | n0 | n0 odd? | valid cycle? | member set (sorted, first 6) | cycle_id (sweep cycle_min) |
|---|---:|:---:|:---:|---|---|
| (1,1,1,1,4) | 211 | yes | yes | [211, 323, 422, 491, 646, 743, ...] | cycle_min=211 |
| (1,1,1,2,3) | 227 | yes | yes | [227, 347, 454, 527, 601, 694, ...] | cycle_min=227 |
| (1,1,1,3,2) | 259 | yes | yes | [259, 341, 395, 518, 599, 682, ...] | cycle_min=259 |
| (1,1,1,4,1) | 323 | yes | yes | [211, 323, 422, 491, 646, 743, ...] | cycle_min=211 |
| (1,1,2,1,3) | 251 | yes | yes | [251, 383, 439, 502, 581, 665, ...] | cycle_min=251 |
| (1,1,2,2,2) | 283 | yes | yes | [283, 373, 431, 493, 566, 653, ...] | cycle_min=283 |
| (1,1,2,3,1) | 347 | yes | yes | [227, 347, 454, 527, 601, 694, ...] | cycle_min=227 |
| (1,1,3,1,2) | 331 | yes | yes | [287, 331, 437, 503, 574, 662, ...] | cycle_min=287 |
| (1,1,3,2,1) | 395 | yes | yes | [259, 341, 395, 518, 599, 682, ...] | cycle_min=259 |
| (1,1,4,1,1) | 491 | yes | yes | [211, 323, 422, 491, 646, 743, ...] | cycle_min=211 |
| (1,2,1,1,3) | 287 | yes | yes | [287, 331, 437, 503, 574, 662, ...] | cycle_min=287 |
| (1,2,1,2,2) | 319 | yes | yes | [319, 367, 421, 485, 557, 638, ...] | cycle_min=319 |
| (1,2,1,3,1) | 383 | yes | yes | [251, 383, 439, 502, 581, 665, ...] | cycle_min=251 |
| (1,2,2,1,2) | 367 | yes | yes | [319, 367, 421, 485, 557, 638, ...] | cycle_min=319 |
| (1,2,2,2,1) | 431 | yes | yes | [283, 373, 431, 493, 566, 653, ...] | cycle_min=283 |
| (1,2,3,1,1) | 527 | yes | yes | [227, 347, 454, 527, 601, 694, ...] | cycle_min=227 |
| (1,3,1,1,2) | 439 | yes | yes | [251, 383, 439, 502, 581, 665, ...] | cycle_min=251 |
| (1,3,1,2,1) | 503 | yes | yes | [287, 331, 437, 503, 574, 662, ...] | cycle_min=287 |
| (1,3,2,1,1) | 599 | yes | yes | [259, 341, 395, 518, 599, 682, ...] | cycle_min=259 |
| (1,4,1,1,1) | 743 | yes | yes | [211, 323, 422, 491, 646, 743, ...] | cycle_min=211 |
| (2,1,1,1,3) | 341 | yes | yes | [259, 341, 395, 518, 599, 682, ...] | cycle_min=259 |
| (2,1,1,2,2) | 373 | yes | yes | [283, 373, 431, 493, 566, 653, ...] | cycle_min=283 |
| (2,1,1,3,1) | 437 | yes | yes | [287, 331, 437, 503, 574, 662, ...] | cycle_min=287 |
| (2,1,2,1,2) | 421 | yes | yes | [319, 367, 421, 485, 557, 638, ...] | cycle_min=319 |
| (2,1,2,2,1) | 485 | yes | yes | [319, 367, 421, 485, 557, 638, ...] | cycle_min=319 |
| (2,1,3,1,1) | 581 | yes | yes | [251, 383, 439, 502, 581, 665, ...] | cycle_min=251 |
| (2,2,1,1,2) | 493 | yes | yes | [283, 373, 431, 493, 566, 653, ...] | cycle_min=283 |
| (2,2,1,2,1) | 557 | yes | yes | [319, 367, 421, 485, 557, 638, ...] | cycle_min=319 |
| (2,2,2,1,1) | 653 | yes | yes | [283, 373, 431, 493, 566, 653, ...] | cycle_min=283 |
| (2,3,1,1,1) | 797 | yes | yes | [227, 347, 454, 527, 601, 694, ...] | cycle_min=227 |
| (3,1,1,1,2) | 601 | yes | yes | [227, 347, 454, 527, 601, 694, ...] | cycle_min=227 |
| (3,1,1,2,1) | 665 | yes | yes | [251, 383, 439, 502, 581, 665, ...] | cycle_min=251 |
| (3,1,2,1,1) | 761 | yes | yes | [287, 331, 437, 503, 574, 662, ...] | cycle_min=287 |
| (3,2,1,1,1) | 905 | yes | yes | [259, 341, 395, 518, 599, 682, ...] | cycle_min=259 |
| (4,1,1,1,1) | 1121 | yes | yes | [211, 323, 422, 491, 646, 743, ...] | cycle_min=211 |

## Distinct cycle count

- Total compositions: 35
- n0 odd: 35
- Valid cycles (after simulation): 35
- Distinct cycles after dedup by member set: **7**

Per-cycle multiplicity (number of compositions mapping to each cycle):

| cycle_min | rotations (compositions yielding this cycle) |
|---:|---|
| 211 | 5: (1,1,1,1,4); (1,1,1,4,1); (1,1,4,1,1); (1,4,1,1,1); (4,1,1,1,1) |
| 227 | 5: (1,1,1,2,3); (1,1,2,3,1); (1,2,3,1,1); (2,3,1,1,1); (3,1,1,1,2) |
| 251 | 5: (1,1,2,1,3); (1,2,1,3,1); (1,3,1,1,2); (2,1,3,1,1); (3,1,1,2,1) |
| 259 | 5: (1,1,1,3,2); (1,1,3,2,1); (1,3,2,1,1); (2,1,1,1,3); (3,2,1,1,1) |
| 283 | 5: (1,1,2,2,2); (1,2,2,2,1); (2,1,1,2,2); (2,2,1,1,2); (2,2,2,1,1) |
| 287 | 5: (1,1,3,1,2); (1,2,1,1,3); (1,3,1,2,1); (2,1,1,3,1); (3,1,2,1,1) |
| 319 | 5: (1,2,1,2,2); (1,2,2,1,2); (2,1,2,1,2); (2,1,2,2,1); (2,2,1,2,1) |

## Comparison vs sweep

- Sweep (action 005) reports 7 primitive L=5 cycles with cycle_min in:
  [211, 227, 251, 259, 283, 287, 319]
- Algebraic enumeration finds 7 distinct cycles with cycle_min in:
  [211, 227, 251, 259, 283, 287, 319]
- Missing from algebraic vs sweep: none
- Extras in algebraic vs sweep: none

**Match: exact.** Algebraic count equals sweep count; member sets match 1-to-1.

## Conclusion

C-008 verdict: **algebraically confirmed.** Of 35 compositions of 8 into 5
positive parts, 35 yield odd n0 and 35 yield valid L=5 cycles;
after deduplicating by member set (5 cyclic rotations per cycle), exactly **7**
distinct primitive cycles remain. They match the 7 sweep cycles 1-to-1. The
count of 7 is therefore not just empirical — it is the exact number of integer
solutions to the L=5 shortcut equation for (3, 13).
