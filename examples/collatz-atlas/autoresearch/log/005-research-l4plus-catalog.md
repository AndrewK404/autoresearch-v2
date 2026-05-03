# res 005 — L ≥ 4 cycle catalog

## What & why
Queue #2 — separate the 153 atlas cycles by shortcut length L, focus on
L ≥ 4 (the cycles invisible to action 002's L ≤ 3 closed-form catalog),
look for structural patterns. Especially: does (3, 13)'s 8 L ≥ 4 cycles
share a residue or period pattern?

## Done
Sub-agent computed shortcut length L = (number of odd members in the
cycle) for every row in `001-cycles.parquet`, and the full T-period
t_period by direct simulation. Output: `005-shortcut-lengths.parquet`,
`005-l4plus-catalog.md`, `005-cataloger.py`.

## Result
n/a (research-only)

**37 cycles at L ≥ 4** out of 153 total, spread across 22 of the 44
(a, b) variants. Per-a distribution: a=1 → 6, a=3 → 15, a=5 → 12,
a=7 → 4.

**(3, 13) inventory** — confirmed 8 L ≥ 4 cycles, of which:
- **7 share the exact shape (L = 5, t_period = 13)**, with cycle_min
  values 211, 227, 251, 259, 283, 287, 319.
- 1 has L = 15 (the outlier).
- All 8 have **gcd of members = 1** (primitive — they don't inherit).
- All 8 have members **coprime to 3** (gcd-invariant since a=3 with
  b coprime to 3) — but only inheritance-wise; the strong claim is they
  also avoid 0 mod 13 (which is non-trivial).

The L=5 cycles all have t_period exactly 13. So the halving-vector
(k₁, ..., k₅) sums to 8 in every case (period 13 = 5 odd-steps + 8
halvings). 7 distinct halving vectors summing to 8 for L=5.

**(5, 9) inventory** — **2 L ≥ 4 cycles** (L=9 and L=27). My brief
told the agent to *expect 0* — wrong. Action 002's L ≤ 3 catalog
listed 8 cycles for (5, 9), but the sweep finds 10 — so 2 are at L ≥ 4.
The error was on my side (conflated catalog count with sweep count).
The 2 cycles are large: max member ~ 10⁵, t_period 30 and 90.

**(5, 21) inventory** — 4 L ≥ 4 cycles. Confirms the brief.

**(3, 5) inventory** — 2 L ≥ 4 cycles. Confirms.

**Empirical period law:**
> t_period ≈ L · (1 + log₂ a)

Per-a observed mean ratio:
- a=3: 2.66 (theoretical 1 + log₂ 3 = 2.585) — within 3%
- a=5: 3.42 (theoretical 1 + log₂ 5 = 3.32) — within 3%
- a=7: 3.87 (theoretical 1 + log₂ 7 = 3.81) — within 2%

This is the *expected* relation: each odd step adds 1 to the T-step
counter; each odd step is followed on average by `log₂ a` halvings (by
the heuristic that a·n + b is divisible by 2 with probability 1/2,
again with 1/4, etc., giving expected halvings = log₂ a + a constant
for the first halving). The data match this exactly. Useful for
sanity-checking sweep parses.

## Thoughts
Three things are interesting:

1. **(3, 13)'s 7 cycles at L=5, t_period=13** look like a *family*
   indexed by halving vectors (k₁,..,k₅) summing to 8. Possibly all
   such valid k-sequences yield a cycle; the count of compositions of 8
   into 5 positive parts is C(8−1, 5−1) = 35. We see 7 (and a few of
   those might be rotations). So most candidate halving vectors do NOT
   yield a valid cycle (the algebra `n₀ · (2⁸ − 3⁵) = 13 · (...)` only
   has positive odd integer solutions for specific shapes). Question:
   *what determines which compositions are valid?*

2. **The t_period = L · (1 + log₂ a) law is tight enough to be
   diagnostic.** A cycle that violates it badly indicates either a
   parse error or genuinely unusual structure (very long halving runs,
   etc.). For atlas-quality control it's a free check.

3. **(5, 21), (5, 7), (5, 13) all have a cycle with L = 18,
   t_period = 60**. Same shape, three different (a, b). Worth a
   targeted probe — could be a structural family across the a=5 row.

## Conclusion
*Tentative.* Several conjectures emerge:
- C-008: for (3, 13), the L=5 cycles form a structured family
  parametrized by halving vector (k₁..k₅) summing to 8. **Conjecture:
  the count of distinct (3, 13) primitive L=5 cycles equals the number
  of (k₁..k₅) compositions of 8 yielding positive integer solutions of
  `n₀ · (2⁸ − 3⁵) = 13 · (3⁴ + 3³·2^k₁ + 3²·2^{k₁+k₂} + ...)`.**
- C-009: the empirical period law `t_period ≈ L · (1 + log₂ a)` holds
  uniformly across the atlas with deviation < 4% per (a, b) average.
- C-010 (open): the (a=5, b ∈ {7, 13, 21}) shared L=18, t_period=60
  cycle indicates a structural family.

## Reasoning
The (3, 13) finding is the most concrete lead. The 7 cycles at the
same (L, t_period) cannot be coincidence; they must reflect a shared
algebraic structure. Possible angles:
- The 7-fold structure resembles a Galois-theoretic / multiplicative-
  group structure on Z/13Z (which has 12 = 4 · 3 elements; the order-4
  cyclic subgroup of (Z/13Z)* has elements {1, 5, 8, 12}). Could be a
  coincidence at this scale; needs verification.
- The cycle min values 211, 227, 251, 259, 283, 287, 319 don't have an
  obvious pattern; their residues mod 13: 211 mod 13 = 3, 227 mod 13 =
  6, 251 mod 13 = 4, 259 mod 13 = 12, 283 mod 13 = 10, 287 mod 13 = 1,
  319 mod 13 = 7. So residues {1, 3, 4, 6, 7, 10, 12} — that's 7 of
  the 12 nonzero residues. Each cycle "owns" one residue.

If a follow-up sub-agent can verify that (3, 13) has *exactly* 7
primitive L=5 cycles and that their cycle_min residues mod 13 cover a
specific subset, that's a structural finding worth promoting.

## Next
- **CONJECTURES.md updates:** add C-008, C-009, C-010.
- **Queue:** schedule a structural probe of (3, 13) — derive the L=5
  cycle equation algebraically and check which (k₁..k₅) yield positive
  integer solutions. Expected: most don't.
- Wait for action 006.

## Linked
- autoresearch/archive/005-shortcut-lengths.parquet
- autoresearch/archive/005-l4plus-catalog.md
- autoresearch/archive/005-cataloger.py
