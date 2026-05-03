# examples — generalized Collatz parameter atlas

A worked autoresearch-v2 run (research-only mode) on the generalized
Collatz family `T_{a,b}(n) = n/2 if even, a·n+b if odd`. Outcome:
one new structural theorem (C-019: a Lyndon-word bijection for
primitive cycles on the m=1 hypersurface) and an infinite 2D family
of "tractable cousins" of Collatz with explicit cycle counts.

## Contents

| Path | What it is |
|---|---|
| `report.md` | Publication-style report: task statement, main conclusion (one paragraph), evidence, comparison with prior results, and the agent's step-by-step trace. **Start here.** |
| `TASK.md` | The original brief handed to the agent at session start. |
| `atlas.py` | Loader script for the atlas data (`load_atlas`, `cycles_for(a, b)`, `trajectories_for(a, b)`, `cycle_members(a, b, cycle_id)`). |
| `autoresearch/CONFIG.md` | Frozen contract: mode (research-only), goal, scope, constraints. |
| `autoresearch/RESUME.md` | Frozen interview answers + envs + bootstrap commands (for warm starts and re-setup). |
| `autoresearch/MEMORY.md` | Live dashboard at end of run: best findings, queue, recent actions, status. |
| `autoresearch/LESSONS.md` | Confirmed lessons (only entries the user explicitly promoted). |
| `autoresearch/CONJECTURES.md` | The conjecture ledger — 19 entries with status, scope, evidence, falsification protocol. C-011 (proven), C-019 (main novel theorem, proven sketch + 59/59), C-018 (corollary, Catalan family), C-001/003/006″/007′/008/012/013/015/016/017 (surviving), four documented falsifications. |
| `autoresearch/log.tsv` | Single append-only action log: NNN, timestamp, type, actor, metric, delta, status, description, linked files. |
| `autoresearch/log/NNN-<type>-<info>.md` | Detailed per-action notes (30 entries). Each contains: hypothesis, what was done, results, agent's reasoning, conclusion, next step. |
| `autoresearch/archive/*.py` | Verification scripts (one per action that needed code). Reproducible: fixed parameters, no randomness in cycle enumeration. |
| `autoresearch/archive/*-summary.md` | Sub-agent summaries (research / analysis returns). |
| `autoresearch/archive/*.parquet` | Atlas data (primitive cycles, results, attractivity). Large data files (>1 MB) excluded from this PR; regeneratable from the corresponding `*-sweep.py`. |
| `autoresearch/memory/.gitkeep` | Memory snapshot directory (no compaction occurred — MEMORY.md stayed under the 400-line cap). |

Open `report.md` for the headline result. Open `autoresearch/CONJECTURES.md`
to read the full conjecture ledger. Open
`autoresearch/log/047-research-general-mequal1-theorem.md` and
`autoresearch/log/048-research-lyndon-full-theorem.md` for the moments
where C-019 took its final shape.

## Headline result

For any odd `a ≥ 3` and `L, K ≥ 1` with `2^K > a^L`, the cell
`(a, b = 2^K − a^L)` has *exactly*

  L_{K,L} := (1/L) · Σ_{d | gcd(K, L)} μ(d) · C(K/d − 1, L/d − 1)

primitive cycles of length K + L, in **bijection with binary Lyndon
words of length K with L ones**. Verified across **59 cells** (a ∈
{3, 5, 7}, gcd(K, L) ∈ {1..6}); zero failures. Two diagonals (K = 2L±1)
yield Catalan-many cycles per cell — concrete infinite families of
tractable cousins.

## Reproducing the run

```bash
# Inside this examples/ directory:
python autoresearch/archive/048-lyndon-full-lattice.py    # 17/17 gcd>1 cells
python autoresearch/archive/047-general-lattice.py        # 42/42 gcd=1 cells
python autoresearch/archive/046-catalan-l9-verify.py      # L=9 Catalan
python autoresearch/archive/<NNN>-sweep.py                # regenerate atlas parquets
```

To re-run the full autoresearch loop from scratch: clear `autoresearch/`
back to its empty scaffolds, point Claude Code at this directory, and run
`autoresearch`. The loop is research-only mode (no executable scalar
metric); the run itself is the source of truth.

---

# Changes proposed for autoresearch (lessons from this run)

These are observations from running autoresearch-v2 on a research-heavy,
no-scalar task. They are *proposals*, not changes already merged.

## 1. Promote `CONJECTURES.md` to a first-class file in research-only mode

Research-only mode currently uses `LESSONS.md` for anything the user
confirms. But research outputs are *falsifiable claims*, not lessons —
they have scope, evidence, falsification protocol, and a status that
evolves (open → surviving → proven / falsified). During this run the
agent created `CONJECTURES.md` ad-hoc. It became the load-bearing
artefact: every meaningful result was added there, and the conjecture
status (proven, surviving, falsified) was the de-facto progress metric.

**Proposal.** In research-only mode, scaffold `CONJECTURES.md` at setup
alongside `LESSONS.md`, with a fixed schema:

```
### C-NNN — short title (status flag)

**Status:** open | surviving | proven | falsified
**First proposed:** action NNN
**Scope:** ...
**Statement:** ...
**Evidence:** ...
**Falsification protocol:** ...
**Linked:** log/NNN-*.md, archive/...
```

`LESSONS.md` then becomes what it should be: cross-cutting *meta*-lessons
about how to attack this kind of problem, not findings about the problem
itself.

## 2. Strategy escalation, but for research-only mode

`SKILL.md §5` keys strategy levels (low-hanging fruit → systematic →
structural → radical) to **experiment count**. Research-only mode has
no experiments. The current spec is silent on when to escalate.

**Proposal.** In research-only mode, escalate by **claim productivity per
N sub-agent dispatches**:

- L1 (1–5 dispatches): canvass obvious hypotheses.
- L2 (6–15): systematic exploration (sweeps, lattice tests).
- L3 (16–30): structural claims (look for theorems, not just
  observations).
- L4 (30+): radical reframing (is the metric of "novelty" right? is
  this just re-deriving known material?).

Plateau signal in research-only: N consecutive sub-agent returns produce
no new entries in `CONJECTURES.md` and no falsifications.

## 3. Honesty audit as a first-class sub-agent type

A user prompt mid-run was load-bearing: *"have you actually discovered
something new?"*. It forced the agent to deflate over-hyped framings
(an empirical correlation `c ≈ (a-4)/(a-2)` was mistaken for a
meaningful law before the prompt). **The bias of an autonomous loop
is to celebrate; an external skeptical voice is required.**

**Proposal.** Add a `honesty-audit` sub-agent type to the menu in
`SKILL.md §8` (alongside researcher / analyst / falsifier). Its brief:
read the last N entries of `CONJECTURES.md` and challenge each — is
the claim genuinely novel, or a re-derivation of standard material?
is the formula classical? has the agent confused empirical correlation
with theorem? Dispatch automatically every K dispatches (default
K = 10) and on every claim promotion to "proven".

## 4. Memory snapshots on major pivots, not just at 400 lines

`MEMORY.md` compaction triggers on a 400-line cap. But the natural
snapshot moments in research are *pivots* — when a working hypothesis
is generalized (C-018 → C-019), abandoned (C-006′ → C-006″),
or reframed (C-013 multistep → individual-seed). These are precisely
when future-you will want to read the pre-pivot state.

**Proposal.** Allow main to take a manual snapshot
(`memory/NNN-pivot-<info>.md`) on a recognized pivot, with a one-line
trigger ("**Pivot:** ..." line in `MEMORY.md`). Keep the 400-line
trigger as a fallback.

## 5. Single-scalar-metric framing is too tight for research-only

Several places in `SKILL.md` rest on *one* metric (best, keep/discard,
strategy escalation). Research-only mode loosens this informally but
doesn't replace it. A research run can produce multiple unrelated
discoveries (here: Catalan family + Lyndon bijection + falsified
strong-form claims). The single-`Best:` slot in `MEMORY.md` becomes
ambiguous.

**Proposal.** In research-only mode, replace `## Best` with `## Top
findings`, listing all *promoted* claims (≥ user-confirmed) in
significance order, with a one-line headline for each. Keep `## Status`
focused on the current frontier.

---

# Evaluation metric (research and engineering, unified)

The brief specifically asked for an evaluation metric covering not only
research but also engineering tasks (LLM training, kernel optimization,
prompt iteration). The single-scalar metric of canonical autoresearch
fits engineering tasks; research tasks need a richer object. Below is
a unified evaluation that reduces to the canonical metric on engineering
tasks and to a claims-ledger score on research tasks.

## The unified score

For a completed autoresearch run, define:

  **Run value V := Σ_i  significance_i × status_weight_i  −  λ · cost**

where the sum is over all promoted findings i (research: entries in
`CONJECTURES.md` or equivalent; engineering: validated metric deltas),
and:

| Term | Engineering task (e.g. LLM training) | Research-only task |
|---|---|---|
| `significance_i` | Relative metric improvement vs. baseline (e.g., `(loss_baseline − loss_i) / loss_baseline`), capped at 1. | Subjective scope-and-novelty score on a 0–10 scale (proven theorem with broad scope > sporadic example > re-derivation of textbook result < 0). |
| `status_weight_i` | 0 (claimed but unverified) → 1 (≥ 2 confirming keep) → 2 (held under independent rerun + falsification stress test). | 0 (open) → 1 (surviving falsification N times) → 2 (proven) → −1 (falsified, kept on purpose). |
| `cost` | wall-clock GPU hours × $/h (or token spend for prompt-tasks). | sub-agent dispatches + main-loop wall time. |
| `λ` | configured in `CONFIG.md`; default 1 unit per dollar for engineering, 0.01 unit per dispatch for research. | (same) |

**On engineering tasks** the formula reduces to *cumulative validated
metric improvement minus cost* — i.e., what canonical autoresearch
already optimizes, just integrated over the run rather than read off
the final `Best`.

**On research-only tasks** the formula rewards: (a) producing claims,
(b) hardening them through falsification attempts, (c) proving them,
and *penalizes* trivial re-derivations through the significance score
(which can be 0 or negative for a known result re-discovered).

## Practical scoring rubric for `significance_i` (research)

| Score | Description | Example |
|---|---|---|
| 0 | Re-derivation or restatement of a textbook result. | "Σ 1/n diverges." |
| 1–2 | Specific empirical observation with narrow scope. | "(3, 7) has 2 primitive cycles." |
| 3–4 | Closed-form characterization within a small region. | C-008 ((3,13) has exactly 7 cycles). |
| 5–6 | New structural connection between two known frameworks. | C-019 — Lyndon-word bijection. |
| 7–8 | Novel theorem changing how a sub-field is organized. | (Stanford-PhD-thesis-tier.) |
| 9–10 | Field-changing — new language or proven hard problem. | (Galois theory; Fermat.) |

The rubric is deliberately blunt. The point is to make the agent (and
the user reviewing the run) place each claim on a calibrated scale,
preventing the loop's natural tendency to celebrate.

## Why `status_weight` matters

A run that produces 50 claims but never tries to break them is worth
less than a run that produces 5 claims and falsifies 2 of them. The
status weight encodes this: open claims contribute zero, falsified
claims (kept on purpose, per `SKILL.md §1` principle 5) contribute −1
to *the original claim* but in practice are accompanied by a *new*
refined claim that earns positive credit. Net effect: the loop gets
credit for hardness, not just throughput.

## Comparison to the canonical single-scalar metric

Canonical autoresearch optimizes one metric, monotonically, with
keep/discard against the current best. That works perfectly when:

- The metric exists and reduces to one shell command (engineering).
- The space of edits is large but structurally homogeneous (e.g., all
  hyperparameter changes affect the same model).
- The "best" notion is unambiguous (lower loss = better).

It fits poorly when:

- There is no executable metric (research-only).
- A run can produce *multiple* unrelated valuable findings (this run:
  Catalan family + Lyndon bijection are independent, neither subsumes
  the other).
- Some "discoveries" are re-derivations that should not score (the
  Lyndon-word formula itself is classical; only the bijection with
  Collatz cycles is new).

The unified score collapses to canonical autoresearch on the first
case and extends it cleanly on the rest.

## Headline benchmark for this run

Applying the rubric to this run:

| Finding | significance | status | weight | contribution |
|---|---|---|---|---|
| C-011 cycle classification (proven) | 5 | proven | 2 | 10 |
| C-019 m=1 Lyndon-word bijection (main novel theorem) | 5 | proven sketch | 2 | 10 |
| C-018 Catalan family (corollary of C-019) | 4 | proven | 2 | 8 |
| C-017 three double-m=1 cells | 3 | surviving | 1 | 3 |
| C-013 lift–halving correlation | 3 | surviving | 1 | 3 |
| C-015 power-law decay c ≈ (a−4)/(a−2) | 3 | surviving | 1 | 3 |
| C-016 stopping time | 3 | surviving | 1 | 3 |
| C-001 a-axis convergence | 2 | surviving | 1 | 2 |
| C-002 strong, C-006, C-006′, C-014 strong | (falsifications) | falsified | −1 each | −4 |
| Sub-total |  |  |  | **38** |
| Cost: ~50 sub-agent dispatches × 0.01 |  |  |  | −0.5 |
| **Total V** |  |  |  | **≈ 37.5** |

The headline number (~38) on its own says little; the point is that
the same formula yields a comparable scalar across runs and across
modes, allowing engineering and research runs to be compared on the
same axis.
