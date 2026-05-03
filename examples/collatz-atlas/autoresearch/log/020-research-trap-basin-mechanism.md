# res 020 — trap-basin mechanism: refining C-013

## What & why
After C-013's first-step-h correlation was established, probed the
deeper mechanism. Specifically: the "trap attractor" framing of the
residue chain mod 2^k — does it correspond to slow convergence
(if a ∈ {1, 3}), divergence (if a ≥ 5), or both?

Predicted before checking: trap basins correspond to (a) slow
convergence in convergent regimes, (b) divergence in divergent regimes.

## Done
Inline check using `006-results.parquet` (S = 10⁵).

For (3, 1) — fully convergent — at k = 10:
- Residue chain has 2 attractors: {1} (basin size 325) and a trap of
  size 187.
- Seeds in good basin (~63% of odd seeds): mean steps = 106.
- Seeds in trap basin (~37%): mean steps = 121 — **14% slower**.
- Both ultimately converge — trap is transient.

For (5, 1) — divergent — at k = 10:
- Residue chain has 4 attractors. Good basin (containing residue 1)
  size 27 of 512 odd residues.
- Seeds in good basin: 6.75% converge (n=2637).
- Seeds in trap basins: 1.88% converge (n=47363) — **3.6× lower
  rate**.

## Result
n/a (research-only)

The residue-chain attractor structure mod 2^k is a *projection* of the
true integer dynamics. Trap attractors are residues that cycle in the
mod-2^k dynamics — but whether the integer trajectory actually
*stays* in the trap basin depends on:
- **Random-walk drift in log-value space**: per shortcut step,
  Δlog_2(value) = log_2(a) − h. Mean drift μ = log_2(a) − E[h] ≈
  log_2(a) − 2.
- For μ < 0 (a ∈ {1, 3}): drift pulls value down, trajectories
  eventually leak out of trap basins via higher-bit shifts. Trap
  basins manifest as *slower-but-still-eventual* convergence.
- For μ > 0 (a ≥ 5): drift pulls value up, trajectories stay trapped
  in their residue basin and grow. Trap basins manifest as
  *suppressed convergence rate*.

So the trap-basin structure is universal, but its empirical
manifestation depends on the drift sign.

## Thoughts
This unifies C-001 (a-axis dichotomy) with C-013 (residue basin
structure). The dichotomy at a = 3/5 is exactly the drift-sign
boundary:
- a = 3: μ = log_2(3) − 2 = −0.415 → trap basins leaky.
- a = 5: μ = log_2(5) − 2 = +0.32 → trap basins absorbing.

So **C-001 is a corollary** of C-013 + the drift formula:
- For a ∈ {1, 3} (μ < 0): all residues eventually converge regardless
  of basin (just slower in trap basins). Hence full convergence.
- For a ≥ 5 (μ > 0): trap-basin residues mostly diverge. Hence
  partial convergence.

Refined claim:

> **C-013″:** For (a, b) odd with a ≥ 5, the residue chain at mod 2^k
> partitions odd residues into attractor basins. Seeds whose starting
> residue lies in the basin of an attractor *containing a cycle-odd-
> residue* converge with significantly higher rate than seeds in
> other (trap) basins. The suppression factor for trap basins reflects
> the drift sign in log-value space; for μ > 0, trap basins are
> nearly absorbing and convergence is rare. For μ < 0 (a ∈ {1, 3}),
> trap basins are merely transiently slow.

Open question for analytic derivation: is the trap-basin convergence
rate quantitatively predictable from μ, σ², and basin size?

## Conclusion
*Solid (extends C-013).* The trap-basin / drift-sign unification is
clean and explains both the C-001 dichotomy and the C-013 lift
correlation. Adds quantitative structure beyond first-step h alone.

## Next
- Wait for action 019 (analytic α + basin volumes) to refine.
- Open question for the post-019 follow-up: jointly regress
  convergence on (basin membership, first-step h) — are they
  independent contributors?
- Consider a higher-k limit study (k = 16, 20) to see if basin sizes
  converge to a natural density.

## Linked
- (no archive artefacts; analysis was inline)
