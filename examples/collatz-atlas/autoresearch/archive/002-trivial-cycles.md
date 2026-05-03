# 002 — Analytic trivial-cycle catalog

Companion script: `autoresearch/archive/002-verify.py` (re-run with
`source .venv/bin/activate && python autoresearch/archive/002-verify.py`).

## Section 1 — Setup

The family under study is `T_{a,b}` with `a, b` positive odd integers:

- if `n` is even, `T(n) = n / 2`
- if `n` is odd,  `T(n) = a·n + b`

A *shortcut step* takes an odd `n` to the next odd value: `n → (a·n + b)/2^k`,
where `k ≥ 1` is the 2-adic valuation of `a·n + b`. The *shortcut length* `L`
of a cycle is the number of odd-step applications in one period; the *period*
in raw `T`-steps is `L + Σ k_i`.

Scope: `a ∈ {1, 3, 5, 7}`, `b ∈ {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21}` — 44
variants. We enumerate every cycle of shortcut length `L ∈ {1, 2, 3}` by:

- **L=1**: solving `n·(2^k − a) = b` for positive odd `n`, swept over
  `k = 1..20`.
- **L=2**: solving `n₀·(2^{k₁+k₂} − a²) = b·(a + 2^{k₁})` for positive odd
  `n₀`, swept over `k₁, k₂ ∈ 1..12`.
- **L=3**: solving `n₀·(2^{k₁+k₂+k₃} − a³) = b·(a² + a·2^{k₁} + 2^{k₁+k₂})`
  for positive odd `n₀`, swept over `kᵢ ∈ 1..8`.

Every algebraic candidate is **verified by direct simulation**: starting at
`n₀`, apply `T_{a,b}` and confirm we return to `n₀` with the predicted
shortcut sequence and that all intermediate halvings are forced (only the
final halving in each block produces an odd value). Rotations of a cycle
share their member set; we deduplicate on member set, keeping the
shortest-period representative.

"Trivial" here means *closed-form-derivable cycles of shortcut length ≤ 3*.
A variant absent from a section may still harbour cycles at higher shortcut
length; this catalog is a **lower bound** for what the sweep should find.

Note on `a = 1`: every variant has the universal length-1 cycle `n = b` (set
`k = 1` in `n·(2 − 1) = b`). For example, `(a=1, b=11)` has the cycle
`11 → 22 → 11`. This shows up as the L1 entry with `k = 1` everywhere.

## Section 2 — Per-variant catalog

| a | b  | n_cycles | cycle_lengths | smallest_member | notes |
|---|----|----------|---------------|------------------|-------|
| 1 | 1  | 1 | 1 | 1 | trivial; only the universal n=b cycle |
| 1 | 3  | 2 | 1, 1 | 1 | n=1 (k=2) and n=3 (k=1) |
| 1 | 5  | 2 | 1, 2 | 1 | L1 n=5; L2 (1,3) k=(1,3) |
| 1 | 7  | 3 | 1, 1, 2 | 1 | L1 n=1 (k=3), n=7; L2 (3,5) k=(1,2) |
| 1 | 9  | 3 | 1, 1, 3 | 1 | L1 n=3 (k=2), n=9; L3 (1,5,7) k=(1,1,4) |
| 1 | 11 | 1 | 1 | 11 | only universal n=b cycle |
| 1 | 13 | 1 | 1 | 13 | only universal n=b cycle |
| 1 | 15 | 5 | 1, 1, 1, 2, 3 | 1 | richest a=1 case; n∈{1,5,15}; L2 (3,9); L3 (7,11,13) |
| 1 | 17 | 1 | 1 | 17 | only universal n=b cycle |
| 1 | 19 | 1 | 1 | 19 | only universal n=b cycle |
| 1 | 21 | 5 | 1, 1, 1, 2, 2 | 1 | n∈{3,7,21}; L2 (1,11) k=(1,5); L2 (9,15) k=(1,2) |
| 3 | 1  | 1 | 1 | 1 | classical Collatz fixed cycle: 1 → 4 → 2 → 1 |
| 3 | 3  | 1 | 1 | 3 | only n=3 cycle (3·1 scaling of (3,1)) |
| 3 | 5  | 4 | 1, 1, 3, 3 | 1 | known "second" Collatz-5 cycle: n=1; plus L3 cycles at (19,31,49) and (23,29,37) |
| 3 | 7  | 2 | 1, 2 | 5 | L1 n=7; L2 (5,11) k=(1,3) |
| 3 | 9  | 1 | 1 | 9 | only n=9 (3·1 scaling of (3,1) by 9) |
| 3 | 11 | 2 | 1, 2 | 1 | L1 n=11; L2 (1,7) k=(1,5) |
| 3 | 13 | 2 | 1, 1 | 1 | L1 n=1 (k=4) and n=13 |
| 3 | 15 | 4 | 1, 1, 3, 3 | 3 | L1 n=3, n=15; L3 (57,93,147), (69,87,111) |
| 3 | 17 | 2 | 1, 2 | 1 | L1 n=17; L2 (1,5) k=(2,5) |
| 3 | 19 | 1 | 1 | 19 | only n=19 |
| 3 | 21 | 2 | 1, 2 | 15 | L1 n=21; L2 (15,33) k=(1,3) |
| 5 | 1  | 3 | 2, 3, 3 | 1 | NO L1 cycle (2^k−5 = 0,−1,−3,3,11,27 hits b=1 only at k=… none integer for n>0); L2 (1,3); L3 (13,33,83), (17,27,43) |
| 5 | 3  | 7 | 1, 2, 3, 3, 3, 3, 3 | 1 | exceptionally rich; L1 n=1 (k=3); five L3 cycles |
| 5 | 5  | 3 | 2, 3, 3 | 5 | scaling of (5,1) by 5 |
| 5 | 7  | 4 | 2, 2, 3, 3 | 7 | L2 (7,21) and (9,13); L3 (91,231,581), (119,189,301) |
| 5 | 9  | 8 | 1, 2, 3, 3, 3, 3, 3, 3 | 1 | extremely rich; *small* L3 cycle (1,7,11) k=(1,2,6) |
| 5 | 11 | 4 | 1, 2, 3, 3 | 1 | L1 n=1 (k=4) |
| 5 | 13 | 4 | 2, 2, 3, 3 | 3 | L2 (3,7) k=(2,4); also L2 (13,39) |
| 5 | 15 | 7 | 1, 2, 3, 3, 3, 3, 3 | 5 | scaling of (5,3) by 5 |
| 5 | 17 | 3 | 2, 3, 3 | 17 | structurally like (5,1) scaled |
| 5 | 19 | 3 | 2, 3, 3 | 19 | structurally like (5,1) scaled |
| 5 | 21 | 8 | 1, 2, 2, 3, 3, 3, 3, 3 | 7 | scaling-of-(5,3) by 3 plus extra structure |
| 7 | 1  | 1 | 1 | 1 | only n=1, k=3: 1 → 8 → 4 → 2 → 1 |
| 7 | 3  | 1 | 1 | 3 | only n=3 (= 3·1 scaling of (7,1)) |
| 7 | 5  | 2 | 1, 2 | 3 | L1 n=5; L2 (3,13) k=(1,5) |
| 7 | 7  | 1 | 1 | 7 | only n=7 (= 7·1 scaling of (7,1)) |
| 7 | 9  | 2 | 1, 1 | 1 | L1 n=1 (k=4) and n=9 |
| 7 | 11 | 1 | 1 | 11 | only n=11 |
| 7 | 13 | 1 | 1 | 13 | only n=13 |
| 7 | 15 | 3 | 1, 2, 2 | 9 | L1 n=15; L2 (9,39) k=(1,5); L2 (11,23) k=(2,4) |
| 7 | 17 | 1 | 1 | 17 | only n=17 |
| 7 | 19 | 1 | 1 | 19 | only n=19 |
| 7 | 21 | 1 | 1 | 21 | only n=21 (= 3·7 scaling of (7,7) and 21·1 scaling of (7,1)) |

## Section 3 — Detailed cycle list

For each (a, b) with at least one cycle, all cycles of shortcut length ≤ 3
are listed below. Members are sorted ascending. `k = (k₁, …, k_L)` is the
shortcut signature; `period` is the total raw `T`-step count.

### a = 1

- **(1, 1)**: L1 k=(1,) members=(1,) period=2
- **(1, 3)**: L1 k=(1,) members=(3,) period=2; L1 k=(2,) members=(1,) period=3
- **(1, 5)**: L1 k=(1,) members=(5,) period=2; L2 k=(1, 3) members=(1, 3) period=6
- **(1, 7)**: L1 k=(1,) members=(7,) period=2; L1 k=(3,) members=(1,) period=4; L2 k=(1, 2) members=(3, 5) period=5
- **(1, 9)**: L1 k=(1,) members=(9,) period=2; L1 k=(2,) members=(3,) period=3; L3 k=(1, 1, 4) members=(1, 5, 7) period=9
- **(1, 11)**: L1 k=(1,) members=(11,) period=2
- **(1, 13)**: L1 k=(1,) members=(13,) period=2
- **(1, 15)**: L1 k=(1,) members=(15,) period=2; L1 k=(2,) members=(5,) period=3; L1 k=(4,) members=(1,) period=5; L2 k=(1, 3) members=(3, 9) period=6; L3 k=(1, 1, 2) members=(7, 11, 13) period=7
- **(1, 17)**: L1 k=(1,) members=(17,) period=2
- **(1, 19)**: L1 k=(1,) members=(19,) period=2
- **(1, 21)**: L1 k=(1,) members=(21,) period=2; L1 k=(2,) members=(7,) period=3; L1 k=(3,) members=(3,) period=4; L2 k=(1, 2) members=(9, 15) period=5; L2 k=(1, 5) members=(1, 11) period=8

### a = 3

- **(3, 1)**: L1 k=(2,) members=(1,) period=3   [classical 1→4→2→1]
- **(3, 3)**: L1 k=(2,) members=(3,) period=3
- **(3, 5)**: L1 k=(2,) members=(5,) period=3; L1 k=(3,) members=(1,) period=4; L3 k=(1, 1, 3) members=(19, 31, 49) period=8; L3 k=(1, 2, 2) members=(23, 29, 37) period=8
- **(3, 7)**: L1 k=(2,) members=(7,) period=3; L2 k=(1, 3) members=(5, 11) period=6
- **(3, 9)**: L1 k=(2,) members=(9,) period=3
- **(3, 11)**: L1 k=(2,) members=(11,) period=3; L2 k=(1, 5) members=(1, 7) period=8
- **(3, 13)**: L1 k=(2,) members=(13,) period=3; L1 k=(4,) members=(1,) period=5
- **(3, 15)**: L1 k=(2,) members=(15,) period=3; L1 k=(3,) members=(3,) period=4; L3 k=(1, 1, 3) members=(57, 93, 147) period=8; L3 k=(1, 2, 2) members=(69, 87, 111) period=8
- **(3, 17)**: L1 k=(2,) members=(17,) period=3; L2 k=(2, 5) members=(1, 5) period=9
- **(3, 19)**: L1 k=(2,) members=(19,) period=3
- **(3, 21)**: L1 k=(2,) members=(21,) period=3; L2 k=(1, 3) members=(15, 33) period=6

### a = 5

- **(5, 1)**: L2 k=(1, 4) members=(1, 3) period=7; L3 k=(1, 1, 5) members=(13, 33, 83) period=10; L3 k=(1, 3, 3) members=(17, 27, 43) period=10
- **(5, 3)**: L1 k=(3,) members=(1,) period=4; L2 k=(1, 4) members=(3, 9) period=7; L3 k=(1, 1, 5) members=(39, 99, 249) period=10; L3 k=(1, 2, 4) members=(43, 109, 137) period=10; L3 k=(1, 3, 3) members=(51, 81, 129) period=10; L3 k=(1, 4, 2) members=(53, 67, 169) period=10; L3 k=(2, 2, 3) members=(61, 77, 97) period=10
- **(5, 5)**: L2 k=(1, 4) members=(5, 15) period=7; L3 k=(1, 1, 5) members=(65, 165, 415) period=10; L3 k=(1, 3, 3) members=(85, 135, 215) period=10
- **(5, 7)**: L2 k=(1, 4) members=(7, 21) period=7; L2 k=(2, 3) members=(9, 13) period=7; L3 k=(1, 1, 5) members=(91, 231, 581) period=10; L3 k=(1, 3, 3) members=(119, 189, 301) period=10
- **(5, 9)**: L1 k=(3,) members=(3,) period=4; L2 k=(1, 4) members=(9, 27) period=7; L3 k=(1, 1, 5) members=(117, 297, 747) period=10; L3 k=(1, 2, 4) members=(129, 327, 411) period=10; **L3 k=(1, 2, 6) members=(1, 7, 11) period=12**; L3 k=(1, 3, 3) members=(153, 243, 387) period=10; L3 k=(1, 4, 2) members=(159, 201, 507) period=10; L3 k=(2, 2, 3) members=(183, 231, 291) period=10
- **(5, 11)**: L1 k=(4,) members=(1,) period=5; L2 k=(1, 4) members=(11, 33) period=7; L3 k=(1, 1, 5) members=(143, 363, 913) period=10; L3 k=(1, 3, 3) members=(187, 297, 473) period=10
- **(5, 13)**: L2 k=(1, 4) members=(13, 39) period=7; L2 k=(2, 4) members=(3, 7) period=8; L3 k=(1, 1, 5) members=(169, 429, 1079) period=10; L3 k=(1, 3, 3) members=(221, 351, 559) period=10
- **(5, 15)**: L1 k=(3,) members=(5,) period=4; L2 k=(1, 4) members=(15, 45) period=7; L3 k=(1, 1, 5) members=(195, 495, 1245) period=10; L3 k=(1, 2, 4) members=(215, 545, 685) period=10; L3 k=(1, 3, 3) members=(255, 405, 645) period=10; L3 k=(1, 4, 2) members=(265, 335, 845) period=10; L3 k=(2, 2, 3) members=(305, 385, 485) period=10
- **(5, 17)**: L2 k=(1, 4) members=(17, 51) period=7; L3 k=(1, 1, 5) members=(221, 561, 1411) period=10; L3 k=(1, 3, 3) members=(289, 459, 731) period=10
- **(5, 19)**: L2 k=(1, 4) members=(19, 57) period=7; L3 k=(1, 1, 5) members=(247, 627, 1577) period=10; L3 k=(1, 3, 3) members=(323, 513, 817) period=10
- **(5, 21)**: L1 k=(3,) members=(7,) period=4; L2 k=(1, 4) members=(21, 63) period=7; L2 k=(2, 3) members=(27, 39) period=7; L3 k=(1, 1, 5) members=(273, 693, 1743) period=10; L3 k=(1, 2, 4) members=(301, 763, 959) period=10; L3 k=(1, 3, 3) members=(357, 567, 903) period=10; L3 k=(1, 4, 2) members=(371, 469, 1183) period=10; L3 k=(2, 2, 3) members=(427, 539, 679) period=10

### a = 7

- **(7, 1)**: L1 k=(3,) members=(1,) period=4
- **(7, 3)**: L1 k=(3,) members=(3,) period=4
- **(7, 5)**: L1 k=(3,) members=(5,) period=4; L2 k=(1, 5) members=(3, 13) period=8
- **(7, 7)**: L1 k=(3,) members=(7,) period=4
- **(7, 9)**: L1 k=(3,) members=(9,) period=4; L1 k=(4,) members=(1,) period=5
- **(7, 11)**: L1 k=(3,) members=(11,) period=4
- **(7, 13)**: L1 k=(3,) members=(13,) period=4
- **(7, 15)**: L1 k=(3,) members=(15,) period=4; L2 k=(1, 5) members=(9, 39) period=8; L2 k=(2, 4) members=(11, 23) period=8
- **(7, 17)**: L1 k=(3,) members=(17,) period=4
- **(7, 19)**: L1 k=(3,) members=(19,) period=4
- **(7, 21)**: L1 k=(3,) members=(21,) period=4

## Section 4 — Variants with no length-≤-3 cycle

**None.** Every (a, b) in scope has at least one shortcut-length-≤-3 cycle.

For `a = 1`, the universal cycle `n = b` (k = 1) is always present.

For `a = 3, 7`, every (a, b) has the L1 cycle at `n = b` with `k = log₂(a+1)`
(that is, `2^k = a+1`, so `n = b/(2^k − a) = b/1 = b`). Concretely: `a=3,
k=2`; `a=7, k=3`.

For `a = 5`, `2^k − a` is never `+1` for any `k`, so there is no universal
"n = b" L1 cycle. Several `(5, b)` lack any L1 cycle entirely (`b ∈ {1, 5,
7, 13, 17, 19}`); they only have L2 and L3 cycles. This is the
"non-trivial-from-the-start" structure.

Important caveat: "no L1 cycle" or "few cycles in this catalog" does **not**
mean the variant has no cycle at all. It only constrains shortcut lengths
1, 2, 3. A variant could have its smallest cycle at L=4 or higher (or no
cycle at all and unbounded orbits — that is what the sweep is meant to
expose).

## Section 5 — Predictions for the sweep

For each (a, b), the sweep should find at least the cycles listed below
(stated as smallest member of each cycle). If the sweep finds a cycle whose
member set is not contained here and is not a higher-shortcut-length
extension, that is a **surprise** worth flagging.

| a | b  | Predicted cycle minima |
|---|----|------------------------|
| 1 | 1  | {1} |
| 1 | 3  | {1, 3} |
| 1 | 5  | {1, 5} (1 is in the L2 cycle (1,3); 5 is L1) |
| 1 | 7  | {1, 3, 7} (3 is in L2 (3,5)) |
| 1 | 9  | {1, 3, 9} (1 is in L3 (1,5,7)) |
| 1 | 11 | {11} |
| 1 | 13 | {13} |
| 1 | 15 | {1, 3, 5, 7, 15} (3 in L2 (3,9), 7 in L3 (7,11,13)) |
| 1 | 17 | {17} |
| 1 | 19 | {19} |
| 1 | 21 | {1, 3, 7, 9, 21} (1 in L2 (1,11), 9 in L2 (9,15)) |
| 3 | 1  | {1} |
| 3 | 3  | {3} |
| 3 | 5  | {1, 5, 19, 23} |
| 3 | 7  | {5, 7} (5 in L2 (5,11)) |
| 3 | 9  | {9} |
| 3 | 11 | {1, 11} (1 in L2 (1,7)) |
| 3 | 13 | {1, 13} |
| 3 | 15 | {3, 15, 57, 69} |
| 3 | 17 | {1, 17} (1 in L2 (1,5)) |
| 3 | 19 | {19} |
| 3 | 21 | {15, 21} (15 in L2 (15,33)) |
| 5 | 1  | {1, 13, 17} (1 in L2 (1,3)) |
| 5 | 3  | {1, 3, 39, 43, 51, 53, 61} |
| 5 | 5  | {5, 65, 85} |
| 5 | 7  | {7, 9, 91, 119} |
| 5 | 9  | {1, 3, 9, 117, 129, 153, 159, 183} (1 in the small L3 (1,7,11)) |
| 5 | 11 | {1, 11, 143, 187} |
| 5 | 13 | {3, 13, 169, 221} (3 in L2 (3,7)) |
| 5 | 15 | {5, 15, 195, 215, 255, 265, 305} |
| 5 | 17 | {17, 221, 289} |
| 5 | 19 | {19, 247, 323} |
| 5 | 21 | {7, 21, 27, 273, 301, 357, 371, 427} |
| 7 | 1  | {1} |
| 7 | 3  | {3} |
| 7 | 5  | {3, 5} (3 in L2 (3,13)) |
| 7 | 7  | {7} |
| 7 | 9  | {1, 9} |
| 7 | 11 | {11} |
| 7 | 13 | {13} |
| 7 | 15 | {9, 11, 15} (9 in L2 (9,39); 11 in L2 (11,23)) |
| 7 | 17 | {17} |
| 7 | 19 | {19} |
| 7 | 21 | {21} |

### Cycles small enough to be reached by small starting seeds (≤ 50)

These are the strongest tests of the sweep results — a starting seed in
`[1, 100]` should converge to one of these without having to escape to
large values:

- `(3, 5)`: cycle min 1
- `(3, 11)`: cycle min 1
- `(3, 13)`: cycle min 1
- `(3, 17)`: cycle min 1
- `(5, 1)`: cycle min 1, plus (13,33,83) and (17,27,43) — the (5,1) variant
  is the famous "5x+1" with known divergent-looking orbits
- `(5, 3)`: cycle min 1
- `(5, 9)`: small L3 cycle `(1, 7, 11)` — particularly informative because
  it sits at the very bottom of the integers
- `(5, 11)`: cycle min 1
- `(5, 13)`: L2 cycle `(3, 7)`
- `(7, 5)`: L2 cycle `(3, 13)`
- `(7, 9)`: cycle min 1
- `(7, 15)`: L2 cycles `(9, 39)` and `(11, 23)`

### Conjugacy hints flagged for action 003

Substitution `n = c·m` with `c` a positive odd divisor of `b` conjugates
`T_{a,b}` (restricted to the multiples-of-c sublattice) to `T_{a, b/c}`:
indeed `a·(c·m) + b = c·(a·m + b/c)` exactly when `c | b`. The pairs in scope
that this relation links are:

- `(a, b) ~ (a, b/c)` whenever `c` is an odd divisor of `b > 1` and `b/c`
  is one of the scope b-values. So *for every* `a ∈ {1,3,5,7}`:
  - `(a, 3) ~ (a, 1)` via `c = 3`
  - `(a, 5) ~ (a, 1)` via `c = 5`
  - `(a, 9) ~ (a, 3) ~ (a, 1)` via `c = 3, 9`
  - `(a, 15) ~ (a, 5) ~ (a, 3) ~ (a, 1)` via `c = 3, 5, 15`
  - `(a, 21) ~ (a, 7) ~ (a, 3) ~ (a, 1)` via `c = 3, 7, 21`
  - `(a, 7) ~ (a, 1)`, `(a, 11) ~ (a, 1)`, `(a, 13) ~ (a, 1)`,
    `(a, 17) ~ (a, 1)`, `(a, 19) ~ (a, 1)` via `c = b`

- Note: this conjugacy is **only on the c-multiples sublattice**. Cycles of
  `(a, b)` whose members are all divisible by `c` map 1:1 to cycles of
  `(a, b/c)`. Cycles of `(a, b)` with members coprime to `c` are *new* under
  this substitution — they have no preimage in `(a, b/c)`. Confirmed in the
  catalog: `(3, 3)` cycle `{3}` is the image of `(3, 1)` cycle `{1}` under
  `c = 3`. But `(3, 5)` has cycles `{1}, {5}, (19,31,49), (23,29,37)`; only
  `{5}` is the c=5 image of `(3,1)`'s `{1}` — the others are genuinely new
  to `(3, 5)`.

- Strong scaling pattern at `a = 5`: comparing `(5, 3)` and `(5, 15)`,
  every cycle of `(5, 3)` scales by 5 to give a cycle of `(5, 15)`:
  `{1} → {5}`, `(3, 9) → (15, 45)`, `(39, 99, 249) → (195, 495, 1245)`,
  etc. This is a clean conjugacy and (5,15) does not introduce any
  *new* L≤3 cycle beyond the scaled ones — useful negative datum for the
  conjugacy survey.

- Same scaling pattern visible at `(5, 5) = 5·(5, 1)`, `(5, 9) ⊃ 3·(5, 3)`
  but `(5, 9)` has the **extra** L3 cycle `(1, 7, 11)` which is *not* a
  scaling of any `(5, 3)` cycle (since `1, 7, 11` aren't divisible by 3).
  Same story `(5, 21) ⊃ 3·(5, 7)` plus extra structure; `(5, 21) ⊃ 7·(5, 3)`
  also (`{1} → {7}`, etc.).

- `(7, 21)` shows only the cycle `{21} = 21 · {1}` from `(7, 1)` and
  `{21} = 7 · {3}` from `(7, 3)` — no extra L≤3 structure.

- For `a = 1`, every variant has the trivial fixed-cycle `n = b`. Beyond
  that, `(1, 7)` and `(1, 9)` sit conspicuously close to `(1, 15)` and
  `(1, 21)` in cycle structure — worth checking whether there is an
  affine-not-just-scaling conjugacy at play.

These observations are inputs to action 003 (the conjugacy survey), not
conclusions. The conjugacy survey should formalize the `n = c·m` map and
identify which (a, b) pairs in scope are conjugate vs. genuinely distinct.
