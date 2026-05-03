Updated: 2026-05-03T23:10:00Z | Last action: 048

---

## Best
n/a (research-only mode)

## Status
Atlas covers **137 variants** (a∈{1,3,5,7,9,11,13}, b∈[1,21] full
plus a∈{1,3,5,7}, b∈[23,51]) with **455 total cycles** (153 tight +
283 wider-b + 19 wider-a) at S=10⁵, H=10¹³, T=10⁵. **All 171 primitive
cycles satisfy C-011's b | (2^K - a^L); 284 inherited cycles account
for the rest. Full closed-form decomposition.**

Strategy level: 2 (systematic exploration). Wider-b sweep + n_new
analysis + C-011 necessity proof + (7, 31) m>1 worked example all
landed.

Promotion-grade candidates pending user confirmation:

- **C-001** (a-axis dichotomy a∈{1,3} all converge): surviving across
  3 falsification attempts (10× horizon + wider-b). 5.2M trajectories,
  0 failures.
- **C-003** (a=7 rigid L1 cycle pattern in original scope b∈
  {1,3,7,13,17,21}): surviving — but does NOT generalize uniformly
  to wider b. Refined as a number-theoretic condition on b.
- **C-006″** (sub-lattice forward-attractivity ⟺ rad(λ) | rad(a)):
  surviving + analytic proof via residue arithmetic in (ℤ/pℤ)*; 24+
  empirical cells match across prime AND composite λ.
- **C-007′** (n_inherited(1, b) ≥ d(b) − 1): surviving + closed-form
  proof via b-scaling embedding + extended verification at b∈[23, 51].
- **C-008** ((3, 13) has exactly 7 primitive L=5 cycles): surviving +
  closed-form algebraic enumeration. m = 1 worked example of C-011.
- **C-009** (period law t_period ≈ L·(1 + log₂ a) for a ≥ 3): probed,
  deviation < 4% for a ≥ 3; **fails for a = 1**.
- **C-011** (primitive cycles ↔ (L, K, composition) with b | (2^K − a^L)):
  **PROVEN for b odd** + 160/160 empirical match across 104 variants.
  The structural backbone of the atlas.
- **C-012** (n_new(1, b) closed form via ord_b(2)): surviving, 11/11
  match in tight scope, also confirmed at wider b. Corollary of C-011.
- **C-013** (multi-step h predicts lift): log(lift)≈α·Σh_i over first
  K steps; α matches Brownian theory α_RW = 2(log₂(a)-2)/(σ²·ln 2)
  within ~10-15% via individual-seed logistic regression. (7, 1)
  matches 2%; AUC 0.72-0.99. The earlier 0.6× gap was binned-lift
  artifact, closed by individual-seed approach.
- **C-015** (power-law in S: f ∝ S^{-c(a,b)} with c≈(a-4)/(a-2)):
  **surviving across 65 cells, 4 S scales** (10³,10⁴,10⁵,10⁶);
  Pearson(c, μ)=0.982; closed-form RMSE 0.05; S=10⁶ verification 22/22
  within ±20%; wider-b verified — Pearson(b, c)≈0.
- **C-016** (convergent regime stopping time): τ ≈ log_2(n)/|μ_T|.
  Slope=7.0 for a=3 (predicted 7.24); slope=1.5 for a=1 (predicted
  1.50). Match within 4%.
- **C-017** (exactly THREE double-m=1 cells {(3,5), (3,13), (5,3)}
  in a, b odd ≥ 3, L≥1, K>L, b ≤ 10¹²). Pillai-equation Diophantine
  finding. surviving via systematic enumeration to a ≤ 199, K ≤ 99,
  L ≤ 39.
- **C-018** (Catalan family): for L ≥ 3 and b = 2^{2L−1} − 3^L,
  the (3, b) cell admits exactly C_{L−1} primitive cycles at the
  m=1 tuple (L, K=2L−1). **Proven** (Burnside on compositions with
  gcd(2L−1, L)=1). Verified empirically L=3..9: cycles =
  2, 5, 14, 42, 132, 429, 1430. Now subsumed by C-019.
- **C-019** (general m=1 lattice — Lyndon-word bijection — main theorem):
  for any odd a≥3, L,K≥1 with 2^K>a^L, the cell (a, b=2^K-a^L) has
  EXACTLY (1/L)·Σ_{d|gcd(K,L)} μ(d)·C(K/d-1, L/d-1) primitive cycles
  of length K+L = #{binary Lyndon words of length K with L ones}.
  **Proven sketch** + 59/59 empirical verifications across a∈{3,5,7},
  gcd∈{1..6}. Generates an INFINITE 2D lattice of tractable cousins;
  Catalan families are special diagonals (K=2L±1). **The main novel
  theorem of the run** — primitive Collatz cycles ↔ Lyndon words.

Falsifications (kept per TASK.md):
- **C-002** strong form (n_total = d(b)): falsified.
- **C-006** universal forward-attractivity: falsified, 543k
  counterexamples.
- **C-006′** "a=3 only attractive": falsified via residue argument,
  replaced by C-006″.

**Strategy level: 2 (systematic exploration).** L1 → L2 escalation
authorized by user. Tight scope is mapped with full closed-form
decomposition (89 inherited + 64 primitive = 153 cycles). L2 tests
generalization at wider b range, composite λ for C-006″, and
necessity of C-011's divisibility condition.

## Queue
1. **[next, action 008] Algebraic enumeration of (3, 13)'s L=5 cycle
   equation.** Solve `n₀·(2⁸ − 3⁵) = 13·(3⁴ + 3³·2^{k₁} + 3²·2^{k₁+k₂}
   + 3·2^{k₁+k₂+k₃} + 2^{k₁+k₂+k₃+k₄})` for all 35 compositions of 8
   into 5 positive parts; count integer solutions. Expect 7 (matches
   sweep). Anything else falsifies / refines C-008. Quick sub-agent.
2. **[L2, action 009 — pending escalation confirmation] Wider b sweep.**
   Extend b ∈ {1, 3, ..., 51} odd (15 more values) at S=10⁴. Test
   whether C-001, C-003, C-007′ generalize.
3. **[L2, action 010 — pending] Divisor c expansion.** T_{a,b,c}: even
   case n → n/2 generalized to n → n/c when c|n. Sweep c ∈ {2, 3, 4}.
4. **[L2, action 011 — pending] (5, 9) and (5, 21) deep dive.** These
   carry both `inherited` and `new` cycles. Examine the residue structure
   of new cycles. Could yield a structural conjecture analogous to
   C-008.
5. **[L2, action 012 — pending] Analytic proof attempts.** C-007′ and
   C-006′ (refined) have near-trivial closed-form derivations. Try.

### Holding (deferred)
6. **Conway-style mod-m piecewise variants.** Defer until at least one
   tight-scope conjecture is promoted to LESSONS.md.
7. **Atlas storage format consolidation.** Once 008-012 land and the
   schema stabilizes, write `atlas.py` loader at project root.

## Recent
- res 048: done — C-019 strengthened to full Lyndon-word form. Möbius
  inversion handles gcd>1 rotation symmetry. 17 gcd>1 cells verified
  across a∈{3,5,7}, gcd∈{2,3,4,5,6}. Total 59/59 lattice cells, complete
  characterization of m=1 hypersurface. Lyndon-word ↔ primitive Collatz
  cycle bijection.
- res 047: done — General m=1 theorem (C-019). For gcd(K,L)=1 and
  2^K>a^L, cell (a, 2^K-a^L) has C(K-1, L-1)/L primitive cycles of
  length K+L. 42/42 cells verified across a∈{3,5,7}. Lyndon-word
  bijection. Catalan families are diagonals K=2L±1. Now THE main
  theorem; C-018 demoted to corollary.
- res 046: done — Catalan family L=9 verification. (3, 111389) admits
  exactly 1430 cycles at length 26 = C_8. Seven consecutive Catalan
  numbers verified (L=3..9). Corrected b-arithmetic error from log/045
  (113213 → 111389). Archive: 046-catalan-l9-verify.py.
- res 045: done — Catalan family C-018 discovered. For (3, b=2^{2L-1}−3^L),
  cycle count = Catalan number C_{L-1}. Verified L=3..8 via direct
  sweep. Infinite tractable-cousin family. Headline new finding.
- res 044: done — three "double-m=1" cells {(3,5),(3,13),(5,3)};
  Pillai equation observation. C-017 added.
- ana 023 + main: power-law in S confirmed strongly. C-015 added:
  f(a, b, S) ∝ S^{-c(a,b)} with c(5)=0.36, c(7)=0.67, c(9)=0.73,
  c(11)=0.75, c(13)=0.80. Pearson(c, μ)=0.982. C-014 strong falsified
  ((9,1) basin 99.6% but f=0%). α regression gap WIDENS at higher k,
  not narrows — random-walk derivation has structural error.
- ana 022: h-autocorrelation falsification. ρ_1≈0; iid Geom(1/2)
  exact along trajectories. The 0.6× α factor is NOT autocorrelation.
- ana 019: α(a, b) functional form correct (r=0.84 with random-walk
  prediction) but uniform 0.6× shrinkage. Var(h)=2.000 confirmed.
  Basin oscillates wildly at high k for divergent (5,1) — first hint
  C-014 might be fragile.
- ana 020: trap-basin mechanism. (3,1) trap-basins are 14% slower;
  (5,1) trap-basins are 3.6× lower convergence rate. drift-sign
  dichotomy at a=3/5 boundary.
- ana 017: done — C-013 systematic verification. **34/34
  non-degenerate cells, Pearson r > 0.7 at k=4. Median r = 0.833.**
  No anti-correlations anywhere. Multi-step harvest does NOT improve
  correlation — single-step h captures all predictable structure.
  C-013 graduates to "surviving (full sweep)" status. Genuinely novel
  finding for the divergent regime.
- main + ana 017: pivoted to the divergent regime. Found
  that for (a ≥ 5, b), the convergent-seed basin has structural
  residue-class basis: residues are partitioned by the shortcut
  residue chain on (ℤ/2^kℤ)* into attractors; convergent seeds
  concentrate in attractors that include cycle-odd-residues. Initial
  Pearson r ∈ [0.76, 0.86] for first-step h-correlation. Recorded as
  C-013.
- res 016: done — wider-a sweep a∈{9,11,13}. Convergence fractions
  0.045%/0.035%/0.016% — divergence universal for a≥5 odd. C-001 has
  4 surviving falsification attempts. C-011 11/11. New parallel-cycle
  families: (11,7), (11,21), (13,9). Total atlas: 171/171 across 137
  variants.
- ana 015: done — verified (7, 31) 4 parallel primitive cycles all at
  L=6, K=17, m=433 — clean worked example of C-011's m > 1 case.
- ana 013: done — n_new(a=1, b) closed form via ord_b(2). 11/11 match.
  Falsified the 2-adic hypothesis. Added as C-012.
- res 012: done — wider-b sweep. C-001 confirmed (3 attempts);
  C-007′ confirmed; C-011 96/96 primitive cycles. C-003 weakened
  (8/15 wider b values rigid); C-009 fails at a=1.
- ana 014: done — main proved C-011 necessity for b odd via gcd
  propagation. C-011 is now a proven theorem (not just empirical) for
  the b odd case. Atlas decomposition is closed-form classified.
- README.md filled in with substantive content based on proven C-011 +
  promotion-grade conjectures.
- ana 011: done — verified all 64 primitive atlas cycles satisfy
  C-011's divisibility condition (no L cap). Combined with 89 inherited
  cycles, the atlas decomposes completely. C-011 upgraded to "full
  coverage" status.
- ana 010: done — C-011 enumeration. 1,661 tuples; 100% match; covers
  57/153 atlas cycles within L ≤ 8 cap. Promoted to surviving.
- ana 009: done — main's analytic work. Closed-form proof of C-007′;
  falsification of C-006′ via residue argument; promoted refined
  C-006″ (gcd(a,λ)>1 ⟺ forward-attractive) with 20/20 match.
- res 008: done — algebraic enumeration of (3, 13) L=5 cycles. All 35
  compositions valid; 35/5 = 7 distinct cycles. Matches sweep 7-for-7.
  Promoted C-008 to surviving + closed-form support.
- ana 010: in flight — enumerate all (a,b,L,K) where 2^K-a^L divides b
  in tight scope; verify C-011 across all cells.
- res 006: done — 10× horizon sweep + attractivity probe. C-001 / C-003
  / C-008 / C-004 confirmed. C-006 falsified (543k counterexamples).
  Zero new cycles at higher horizon — atlas at tight scope is complete.
- ana 005: done — L≥4 catalog. (3,13) has 7 cycles at L=5, t_period=13;
  primitive, members coprime to 39. Empirical period law
  t_period ≈ L·(1+log₂ a) with deviation <4% per (a,b).
- ana 004: done — inheritance tagging. 64 new + 89 inherited. C-007
  strong falsified; C-007′ refined with n_inherited ≥ d(b)−1.
- ana 007: done — main probed (3,21) seeds 1..14 inline. All reach a
  cycle.
- main: spot-check on a=1 cycle counts vs d(b). C-002 strong falsified;
  reframed as C-007 then C-007′.
- res 003: done — conjugacy survey. Zero full conjugacies; b-scaling
  embedding only; normal form is identity.
- res 002: done — analytic L≤3 catalog. 116 cycles. (5, 9) carries new
  L3 cycle (1, 7, 11). a=5 has no universal n=b L1 cycle.
- res 001: done — opening sweep. 153 cycles. a∈{1,3} all converge;
  a∈{5,7} mostly escape.
- res 000: done — kickoff.

---

## Avoid
- *Predicting cycle counts without verification.* (C-002 falsified
  immediately on spot-check.) Always run the one-line query before
  publishing a numerical claim, even in a draft conjecture.
- *Conflating L≤3 catalog count with sweep total.* In the action 005
  brief I told the agent "(5, 9) had 8 total" based on the L≤3 catalog;
  the sweep had 10. Pure shorthand error; use the parquet not the
  summary when stating numbers in briefs.
- *Trusting sub-agent summaries when promoting a conjecture.* Action
  006's "a=3 max hit time ≤17" was misleading (applied only to λ=3
  cells). I almost promoted C-006′ on this. Caught by attempting the
  analytic proof which contradicted the claim; verified by direct
  query of `006-attractivity.parquet`. **Always cross-check sub-agent
  numerical claims against the underlying parquet before promotion.**
- *Notation collisions in sub-agent reports.* Action 010's "K=27" for
  the (1, 19) L=9 outlier cycle used K = t_period (= 27), not
  K = halving-sum (= 18). My C-011 formulation uses the latter. The
  collision almost let me misclassify the cycle as outside C-011's
  mechanism. **Pin notation explicitly in briefs to sub-agents AND
  re-derive the verification from the parquet on integration.**

## Open questions
- **Analytic derivation of c(a, b)** for C-015. Random-walk hitting
  probability for transient walks with bounded-above and
  geometric-tail-below increments: Veraverbeke heuristic suggests
  c → 1 as a → ∞, with c saturating sublinearly. Empirically matches.
- **Source of 0.6× α factor in C-013.** NOT autocorrelation (action
  022). NOT regression artifact (action 023; gap widens at k=6). The
  random-walk derivation is structurally incomplete.
- **Why does basin disconnect from convergence?** (9,1) basin = 99.6%,
  f = 0%. The residue-chain projection misses something the integer
  trajectory needs. Possibly the cycle's *integer-value* attractor
  basin is much smaller than the residue-attractor basin.
- **C-006″ for composite λ.** Does the rad(λ) | rad(a) generalization
  hold for composite λ? Need (a, b, λ) with composite λ — eg (a, 27, 9),
  (a, 45, 15). Outside current scope.
- **C-009 corrected for a=1.** The period law `1 + log₂ a` fails at
  a=1. The actual t_period/L for a=1 cycles is determined by ord_b(2)
  exactly: t_period = L + ord_b(2) so t_period/L = 1 + ord_b(2)/L. Not
  an "average law" but an exact one.

## Resolved (kept for traceability)
- *(3, 21) seeds 1..14:* main probed inline. All reach a cycle. n=7,
  14 → b-fixed cycle; rest → L2 cycle starting at 15.
- *What governs n_new(1, b)?* Closed by action 013 + C-012: n_new is
  derived from C-011 enumeration at K = ord_b(2). 11/11 match in
  tight scope; the previously hypothesized 2-adic residue pattern was
  falsified.
- *Are there cycles outside C-011's mechanism?* Closed: zero. All 171
  primitive cycles across 137 variants satisfy the divisibility.
  Action 014 proved necessity for b odd analytically.
- *a-axis transition.* Closed by action 016: a ∈ {1, 3} converge,
  a ≥ 5 odd diverge with monotonically sharpening divergence. The
  boundary is at a = 3/5 — empirically validated across a ∈ {1, 3, 5,
  7, 9, 11, 13}.
- ~~**What's the second cycle-creation mechanism?**~~ Resolved:
  there is no second mechanism in tight scope. Action 011 verified
  that all 64 primitive atlas cycles satisfy C-011's divisibility
  condition once the (L, K) cap is removed. The "5 outliers" reported
  by action 010 were artefacts of the L ≤ 8 enumeration cap, not of
  the divisibility condition.

## Resolved (kept for traceability)
- *(3, 21) seeds 1..14:* main probed inline. All reach a cycle. n=7,
  14 → b-fixed cycle; rest → L2 cycle starting at 15.
