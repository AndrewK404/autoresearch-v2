# examples

Worked autoresearch-v2 runs. One subdirectory per run, each containing
the working tree (`autoresearch/`) and a publication-style `report.md`.

## Index

| Task | Mode | Headline result |
|---|---|---|
| [`collatz-atlas/`](collatz-atlas/) | research-only | Lyndon-word bijection for primitive cycles of the generalized Collatz family on the m=1 hypersurface — an infinite 2D family of "tractable cousins" of Collatz with explicit cycle counts. 59/59 cells verified. |

## Per-task layout

Each task directory contains exactly two things:

```
examples/<task-name>/
├── autoresearch/   # full working tree from the run
│   ├── CONFIG.md, RESUME.md         # frozen contract + interview answers
│   ├── MEMORY.md, LESSONS.md        # live dashboard + confirmed lessons
│   ├── CONJECTURES.md               # claims ledger (research-only mode)
│   ├── log.tsv, log/                # action log + per-action notes
│   ├── archive/                     # scripts, sub-agent summaries, data
│   └── memory/                      # archived MEMORY.md snapshots
└── report.md       # task / main conclusion / evidence / agent's steps
```

Open `report.md` first. It states the task, the headline result in one
paragraph, the evidence, and the trace of decisions the agent made.
The full ledger of claims and falsifications is in
`autoresearch/CONJECTURES.md`; the run's chronology is in
`autoresearch/log.tsv` + `autoresearch/log/`.

---

# Lessons from these runs — proposed changes to autoresearch

These are observations from running autoresearch-v2 on tasks that
stretch the canonical single-scalar framing — primarily research-heavy,
no-executable-metric tasks. They are *proposals*, not changes already
merged.

## 1. Promote `CONJECTURES.md` to a first-class file in research-only mode

Research-only mode currently uses `LESSONS.md` for anything the user
confirms. But research outputs are *falsifiable claims*, not lessons —
they have scope, evidence, falsification protocol, and a status that
evolves (open → surviving → proven / falsified). In the Collatz run
the agent created `CONJECTURES.md` ad-hoc and it became load-bearing:
every meaningful result was added there, and the conjecture status was
the de-facto progress metric.

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

## 2. Strategy escalation for research-only mode

`SKILL.md §5` keys strategy levels (low-hanging fruit → systematic →
structural → radical) to **experiment count**. Research-only mode has
no experiments; the spec is silent on when to escalate.

**Proposal.** In research-only mode, escalate by **claim productivity per
N sub-agent dispatches**:

- L1 (1–5 dispatches): canvass obvious hypotheses.
- L2 (6–15): systematic exploration (sweeps, lattice tests).
- L3 (16–30): structural claims — look for theorems, not just
  observations.
- L4 (30+): radical reframing — is the metric of "novelty" right? is
  this just re-deriving known material?

Plateau signal: N consecutive sub-agent returns produce no new entries
in `CONJECTURES.md` and no falsifications.

## 3. Honesty audit as a first-class sub-agent type

A user prompt mid-Collatz-run was load-bearing: *"have you actually
discovered something new?"*. It forced the agent to deflate over-hyped
framings. **The bias of an autonomous loop is to celebrate; an external
skeptical voice is required.**

**Proposal.** Add an `honesty-audit` sub-agent type to the menu in
`SKILL.md §8` (alongside researcher / analyst / falsifier). Its brief:
read the last N entries of `CONJECTURES.md` and challenge each — is
the claim genuinely novel, or a re-derivation of standard material?
is the formula classical? has the agent confused empirical correlation
with theorem? Dispatch automatically every K dispatches (default
K = 10) and on every promotion to "proven".

## 4. Memory snapshots on major pivots, not just at 400 lines

`MEMORY.md` compaction triggers on a 400-line cap. But the natural
snapshot moments in research are *pivots* — when a working hypothesis
is generalized (C-018 → C-019 in this run), abandoned (C-006′ → C-006″),
or reframed (C-013 multistep → individual-seed). These are precisely
when future-you will want to read the pre-pivot state.

**Proposal.** Allow main to take a manual snapshot
(`memory/NNN-pivot-<info>.md`) on a recognized pivot. Keep the 400-line
trigger as a fallback.

## 5. Replace single `Best:` with `Top findings` in research-only mode

Several places in `SKILL.md` rest on *one* metric (best, keep/discard,
strategy escalation). Research-only loosens this informally but doesn't
replace it. A research run can produce multiple unrelated discoveries
(Catalan family + Lyndon bijection + falsified strong-form claims here);
the single `## Best` slot in `MEMORY.md` becomes ambiguous.

**Proposal.** In research-only mode, replace `## Best` with `## Top
findings`, listing all *promoted* claims (≥ user-confirmed) in
significance order, with a one-line headline for each. Keep `## Status`
focused on the current frontier.

---

# Evaluation metric (research and engineering, unified)

The single-scalar metric of canonical autoresearch fits engineering
tasks (LLM training, kernel optimization, prompt iteration); research
tasks need a richer object. Below is a unified evaluation that reduces
to the canonical metric on engineering tasks and to a claims-ledger
score on research tasks.

## The unified score

For a completed autoresearch run, define:

  **V := Σ_i  significance_i × status_weight_i  −  λ · cost**

where the sum is over all promoted findings i (research: entries in
`CONJECTURES.md`; engineering: validated metric deltas), and:

| Term | Engineering task | Research-only task |
|---|---|---|
| `significance_i` | Relative metric improvement vs. baseline (e.g. `(loss_baseline − loss_i) / loss_baseline`), capped at 1. | Subjective scope-and-novelty score, 0–10 (rubric below). |
| `status_weight_i` | 0 (claimed) → 1 (≥ 2 confirming keep) → 2 (held under independent rerun + falsification stress test). | 0 (open) → 1 (surviving) → 2 (proven) → −1 (falsified, kept on purpose). |
| `cost` | wall-clock GPU hours × $/h (or token spend for prompt-tasks). | sub-agent dispatches + main-loop wall time. |
| `λ` | configured in `CONFIG.md`; default 1 unit per dollar (engineering) or 0.01 unit per dispatch (research). |  |

**On engineering tasks** the formula reduces to *cumulative validated
metric improvement minus cost* — what canonical autoresearch already
optimizes, just integrated over the run rather than read off the final
`Best`.

**On research-only tasks** it rewards: (a) producing claims, (b)
hardening them through falsification attempts, (c) proving them, and
*penalizes* trivial re-derivations through the significance score
(which can be 0 or negative for a known result re-discovered).

## Significance rubric (research)

| Score | Description | Example |
|---|---|---|
| 0 | Re-derivation or restatement of a textbook result. | "Σ 1/n diverges." |
| 1–2 | Specific empirical observation with narrow scope. | "(3, 7) has 2 primitive cycles." |
| 3–4 | Closed-form characterization within a small region. | C-008 ((3,13) has exactly 7 cycles). |
| 5–6 | New structural connection between two known frameworks. | C-019 (Lyndon-word bijection). |
| 7–8 | Novel theorem changing how a sub-field is organized. | (Stanford-PhD-thesis-tier.) |
| 9–10 | Field-changing — new language or proven hard problem. | (Galois theory; Fermat.) |

The rubric is deliberately blunt: it forces both agent and reviewer to
place each claim on a calibrated scale, preventing the loop's natural
tendency to celebrate.

## Why `status_weight` matters

A run that produces 50 claims but never tries to break them is worth
less than a run that produces 5 claims and falsifies 2 of them. The
weight encodes this: open claims contribute zero, falsified claims
(kept on purpose, per `SKILL.md §1` principle 5) contribute −1 to the
*original* claim but in practice are accompanied by a *new* refined
claim that earns positive credit. Net effect: the loop is rewarded for
hardness, not throughput.

## When the canonical single-scalar metric breaks down

Canonical autoresearch optimizes one metric monotonically with
keep/discard against the current best. That works perfectly when:

- the metric exists and reduces to one shell command (engineering);
- the edit space is structurally homogeneous (e.g., all hyperparameter
  changes affect the same model);
- "best" is unambiguous (lower loss = better).

It fits poorly when:

- there is no executable metric (research-only);
- a run can produce *multiple* unrelated valuable findings (Catalan
  family + Lyndon bijection here are independent);
- some "discoveries" are re-derivations that shouldn't score (the
  Lyndon-word formula itself is classical; only the bijection with
  Collatz cycles is new).

The unified score collapses to canonical autoresearch on the first case
and extends it cleanly on the rest.

## Worked example: the Collatz run

Applying the rubric to `collatz-atlas/`:

| Finding | significance | status | weight | contribution |
|---|---:|---|---:|---:|
| C-011 cycle classification (proven) | 5 | proven | 2 | 10 |
| C-019 m=1 Lyndon-word bijection | 5 | proven sketch | 2 | 10 |
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

The headline number on its own says little; the point is that the same
formula yields a comparable scalar across runs and across modes,
allowing engineering and research runs to be compared on the same axis.
