# file-structure.md — autoresearch file layout

For each file: one or two sentences on its purpose + a sample layout. **Fields are illustrative** — the exact set depends on the task. Fixed sections are marked explicitly; everything else is optional and added by the agent as needed.

---

## CONFIG.md

**Role:** the **active frozen contract**. Goal, metric, eval, scope, constraints, integrations. Re-read frequently — at session start and before decisions that depend on the contract. Immutable after baseline.

**Sample layout:**

```markdown
# CONFIG

## Mode
<experiment | research-only>
(experiment: a single shell command prints one scalar; research-only: no
executable eval — findings are recorded as thoughts/conclusions in log/)

## Goal
<One sentence: what we are optimising or investigating, and why.>

## Metric
(experiment mode only — omit this whole section in research-only mode)
- Name: <metric_name>
- Direction: <minimize | maximize>
- Noise threshold: <value below which a change is treated as noise; `None` if
  the metric is exact — e.g. val_loss in ML training, exit_code, integer counts>
- Notes: <any jitter / instability>

## Done criterion
(research-only mode only — omit in experiment mode)
- Definition of done: <e.g. "a written recommendation comparing 3 frameworks">
- User's confirmation criterion for promoting a finding to LESSONS.md:
  <e.g. "I review the conclusion and explicitly say it's solid">

## Eval
(experiment mode only — omit this whole section in research-only mode)
- Command: `<single shell command>`
- Timeout: <seconds>
- Parse: <summary_block | regex:<...> | json_path:<...> | file:<path> | exit_code>
- Idempotent: <yes | no — explain if no>

> If eval is a multi-step pipeline (build → run → judge → extract), wrap it in
> a single `eval.sh` (lives next to the target, e.g. `./eval.sh` or
> `autoresearch/eval.sh`). The skill always sees one command.

## Scope
- Target files: <paths the agent may edit>
- Read-only context: <paths the agent should understand>
- Forbidden: <files/areas never to touch>

## Constraints
(experiment mode only — anti-gaming rules; in research-only mode this section
is typically empty or holds general scope rules)
- <Constraint 1: e.g. "do not remove asserts in tests/">
- <Constraint 2>
- <...>

## Integrations
- W&B project: <name | not used>
- <Other integrations as needed; "not used" entries are intentional, not omissions>

## Concurrency
- Experiments in parallel: <N>  (experiment mode only; default 1; n/a in research-only)
- Sub-agents in parallel: <M>  (default 3 in experiment mode, 4 in research-only mode)

## Termination
- <max experiments | plateau window | target threshold | unlimited>

## Important answers
<Interview answers that frame the agent's context but didn't fit cleanly into
the sections above. Examples: "user prefers conservative edits", "target
hardware: a single A100 40GB", "data is refreshed quarterly, not in real
time".>

## Envs
- WANDB_API_KEY — in `.env`
- HF_TOKEN — in `.env`
- <...>

(Raw keys are never stored here. If a key is missing from `.env` — re-ask the
user before running baseline.)

## Bootstrap
The command sequence to prepare the environment. Run once on first setup.
If something breaks, recreate the environment and repeat.

1. `uv sync`
2. `uv run prepare.py`
3. `<...>`

## Notes
<Optional: one-off remarks about the environment that matter for
reproducibility.>
```

The full contract — goal, metric/done-criterion, eval, scope, constraints,
envs, bootstrap, important answers — lives in this one file. Frozen after
baseline; any change requires explicit re-setup.

---

## MEMORY.md

**Role:** live state dashboard, **and the single home for everything the user
tells the agent after setup**. Cold-startable — `MEMORY.md` plus `CONFIG / LESSONS` is enough to resume work. Hard cap: **400 lines**.

After setup, **all** new user input goes here, not into `CONFIG.md` (which is
frozen). The two flavours:

- **Trajectory-changing context** ("we just got a second GPU", "this paper
  is highly relevant", "actually, batch size 256 is fine if you accept the
  MFU drop") — recorded in `Status`, under `Open questions`, or in a fresh
  optional section. The agent's behaviour adjusts on the next dispatch.
- **Genuine contract changes** (new metric, new scope, new eval) do NOT go
  here — they trigger a re-setup that updates `CONFIG.md`. Anything else
  the user says, even if it sounds important, lives in `MEMORY.md`.

Trivia is not recorded.

### Fixed sections (always present)

```markdown
Updated: <ISO timestamp> | Last action: NNN

## Best
<metric_name>=<value> @ exp NNN
(short phrase: what change brought it)

## Status
<1–2 sentences: current focus>
Strategy level: <1: low-hanging | 2: systematic | 3: structural | 4: radical>
(if escalated early due to plateau — note the reason in one phrase)

## Queue
Ranked backlog of hypotheses. Each one with a numeric falsifier.

1. <Hypothesis>. Falsifier: <if X fails to reach Y under condition Z — reject>.
2. <...>

## Recent
Last 5–10 actions, brief.

- exp NNN: <delta> — <one phrase>
- res NNN: <one phrase about the return>
- <...>
```

### Optional sections (added by the agent as needed)

```markdown
## Avoid
- <Approach X> — exhausted, reason: <ref to exp NNN, MMM>
- <...>

## Open questions
- <Unresolved but important>

## Active threads
- <Research direction in progress, status>
```

Any other section is allowed if it serves the current goal.

### Compression

When the file approaches 400 lines:
1. Copy `MEMORY.md` → `memory/NNN-memory.md` (zero-padded next id).
2. Rewrite `MEMORY.md` in place: keep fixed sections + still-relevant optional sections; tighten `Recent`, aggregate exhausted entries in `Avoid`, promote resolved `Open questions` to `LESSONS.md` (if they qualify under the ≥ 2 keep rule) or to the archived snapshot.

---

## LESSONS.md

**Role:** confirmed lessons grounded in **own experience**.

- *Experiment mode:* writes are allowed only after **≥ 2 keep experiments confirm the same falsifier statement** (i.e. the same falsifier from `MEMORY.md ## Queue` is satisfied twice — not just two keeps that loosely point in the same direction). Sub-agent research insights alone do not qualify (their place is `log/NNN-research-<info>.md`).
- *Research-only mode:* a finding is promoted here once **the user explicitly confirms it as solid** (per `CONFIG.md ## Done criterion`). The lesson must still cite the supporting `log/NNN-*.md` entries that contain the underlying thoughts and conclusions.

**Format — free-form.** Each lesson is written however lands naturally: a single sentence, a paragraph, a paragraph with a quoted experiment, a small list of caveats. There is no rigid schema. What must come through: **what** is claimed, **on what evidence** (at least two `exp NNN` references), and **in what context** it applies.

**Short example:**

```markdown
## Warmup is critical for LR > 3e-4
At learning rates above 3e-4 without warmup, loss explodes in the first 100–200
steps (exp 008, 014). With a 200-step linear warmup it is stable
(exp 019, 021). Context: current architecture and data scale; not verified for
smaller batch.
```

**Longer example:**

```markdown
## Batch > 256 does not scale on our hardware
Tested three times (exp 008, 014, 023): MFU degrades from 42% to 28% when
moving from 256 to 512, effective throughput drops, val_loss is worse for the
same wall-clock. Looks like we hit memory bandwidth, not compute. This is not
a universal claim about large-batch training — it is specifically about a
single A100 40GB and our model. On H100 / multi-GPU it may not reproduce.
```

**Anti-patterns (do not record here):**

- "Researcher thinks X is important" — that belongs in `log/NNN-research-<info>.md`.
- A single keep is not enough; wait for confirmation.
- Vague phrases ("optimisation matters") — be concrete.
- A lesson without at least two `exp NNN` anchors — there is no own-experience basis yet.

---

## log/NNN-<type>-<info>.md

**Role:** detailed per-action notes for anything more involved than a single `log.tsv` row. This covers experiments, research sessions, analyses, compressions, escalations, and any other action types main chooses to record.

**Naming:** `NNN-<type>-<info>.md`, where `<type>` is the action type (`experiment`, `research`, `analysis`, `compression`, `escalation`, …) and `<info>` is a short kebab-case slug. Examples: `054-research-lr-scheduler.md`, `023-experiment-batch-256.md`, `040-analysis-warmup-postmortem.md`, `048-compression-snapshot-001.md`, `036-escalation-l2-to-l3.md`.

**Hard requirement:** every `log/NNN-*.md` contains **explicit reasoning and conclusions from the agent** — what main was thinking before the dispatch, what it noticed along the way, what it concludes, what it changes in Queue / MEMORY / LESSONS as a result. This is the "thinking layer" between experiments that would otherwise vanish. Without it the log becomes a chronology of facts with no explanation of why the agent went a particular way.

If the experiment was a straightforward keep/discard with nothing to think about — say so explicitly ("expected, no surprises; next hypothesis from Queue unchanged"). Silence is loss.

### Common structure

```markdown
# <type-prefix> NNN — <slug>

## What & why
<What this action targeted and why precisely it: hypothesis for an experiment,
brief for research, question for analysis. Main's thinking before the dispatch.>

## Done
<What was actually performed / data collected / diff applied.>

## Result
<Numbers, statuses, findings. For experiments — metric, delta, status. For
research / analysis — distilled findings; full artefacts in archive/.>

## Reasoning
<Explicit conclusions. What follows from this? What does it say about the
current strategy? Does it confirm / contradict anything in MEMORY / LESSONS?
Which new hypotheses arise, which existing ones drop out?>

## Next
<What changes as a result: Queue updates, additions to Avoid, strategy-level
escalation, the next dispatch.>

## Linked
- archive/<files>
- (for experiments) git commit: <hash>
```

The sections are guidance. If an action has no diff (a research session) — skip `Done` or rephrase it. The one section that is **always** present is `Reasoning`.

### Research-only mode — `Thoughts` and `Conclusion` sections

In research-only mode there is no scalar metric to populate `Result`. Instead, two free-form sections are added:

- **`## Thoughts`** — the user's own running notes during the investigation: hunches, half-formed ideas, observations from reading. Free-form prose, bullets, or quoted snippets — whatever fits.
- **`## Conclusion`** — the user's distilled answer to the hypothesis from `What & why`. Marked as `tentative` (most cycles) or `confirmed` (when the user has stamped it per `CONFIG.md ## Done criterion`). Only `confirmed` conclusions are eligible for promotion to `LESSONS.md`.

`Result` is set to `n/a (research-only)`. Everything else (`What & why`, `Done`, `Reasoning`, `Next`, `Linked`) keeps its meaning. A short example for research-only mode is appended to the Examples section below.

### Example: experiment

```markdown
# exp 023 — bigger batch

## What & why
Hypothesis: batch 128 → 256 will give better val_loss for the same wall-clock
via more stable gradients. Falsifier: if val_loss does not drop below 2.30
within 5K steps OR training_seconds rises by more than 5%, reject.

## Done
In `train.py`: `batch_size = 128` → `256`. Nothing else changed. Commit 3a2c91d.

## Result
- Metric: val_loss=2.326
- Delta vs best (2.314): +0.012 → discard
- Eval duration: 1847s (was 1781s, +3.7%)

## Reasoning
Hypothesis rejected on both arms of the falsifier: metric is worse and time is
up. This is the third attempt at a larger batch (008, 014, 023) — the pattern
reproduces. Looks like memory bandwidth, not compute. Reinforces the hunch from
ana 020 that batch > 256 is hopeless on our hardware. Candidate for LESSONS if
we get one more confirmation from a slightly different angle.

## Next
- Add to Avoid: "Batch > 128 — exhausted, MFU degrades (008, 014, 023)".
- Drop remaining large-batch entries from Queue.
- Next dispatch: Lion optimizer (Queue #1).

## Linked
- archive/023-mfu-trace.png
- git commit: 3a2c91d
```

### Example: research

```markdown
# res 022 — Lion optimizer digest

## What & why
Brief: digest Chen et al. 2023 (Lion). Need to gauge whether we expect a win in
our LR regime and whether to test it before other Queue items.

## Done
Read the paper, saved to archive/022-lion-paper.pdf. Authors' benchmarks at
similar scale captured in archive/022-bench-summary.md.

## Result
Lion delivers a steady +1–3% over AdamW at multi-billion scale, at LR 3–10×
smaller. Optimizer memory is half of AdamW. At small scale (< 100M params) the
win is weaker and inconsistent.

## Reasoning
Our scale sits at the lower edge of the zone where Lion clearly wins. But the
optimizer memory drop is a separate plus, potentially opening batch 256 within
the same memory envelope. This re-frames exp 023: the loss could have been
masked by AdamW memory pressure, not the batch size itself. Worth checking.

## Next
- Add to Queue, high priority: Lion with LR ÷ 5 at the current batch.
- Add lower in Queue: Lion + batch 256 (re-attempt — exp 023's rejection is
  weakened).
- Open question for MEMORY: "memory pressure from AdamW vs Lion in our setup".

## Linked
- archive/022-lion-paper.pdf
- archive/022-bench-summary.md
```

### Example: analysis

```markdown
# ana 020 — post-mortem of runs 015–019

## What & why
A series of five experiments with warmup variations (015–019) gave mixed
results: 2 keep, 3 discard. Want to understand what the keeps share before
moving on.

## Done
Reviewed `log.tsv` for NNN ∈ [015, 019], pulled train curves from archive/,
made a quick scatter (warmup_steps × delta_val_loss) →
archive/020-warmup-scatter.png.

## Result
All three discards were at warmup_steps < 100. Both keeps were at 200. Nothing
between 100 and 200 was tried.

## Reasoning
Looks like a monotone zone: below ~100 warmup is insufficient, above 200 it is
already enough; the in-between is unknown. This is not "warmup helps" in the
abstract — it is "for our LR=5e-4, ≥ 100 warmup steps are needed for
stability". One more confirming keep at 150 would qualify this for LESSONS.

## Next
- Queue: warmup_steps=150 as a cheap probe (medium priority).
- MEMORY ## Open questions: "minimum warmup for stability at LR=5e-4".
- No strategy-level escalation; we are still on L2.

## Linked
- archive/020-warmup-scatter.png
```

### Example: research-only mode entry (with Thoughts and Conclusion)

```markdown
# res 014 — vector store comparison: pgvector vs Qdrant vs Weaviate

## What & why
Hypothesis: for our 5M-document corpus with hybrid filtering needs, pgvector
is good enough and avoids adding a new system. Rejection condition (per
CONFIG.md ## Done criterion): if pgvector falls short on filtered ANN latency
at p95 by >2× compared to a dedicated store at the same recall, we drop it.

## Done
Read three benchmark posts (archive/014-pgvector-bench.md,
archive/014-qdrant-bench.md, archive/014-weaviate-bench.md). Sketched a small
table of operational properties (archive/014-ops-matrix.md). No code run.

## Result
n/a (research-only)

## Thoughts
- pgvector benchmarks all use HNSW now; the old IVFFlat numbers people quote
  are misleading.
- Filtering story is the real differentiator. Qdrant's filter-then-search
  path stays sub-100ms even with selective filters; pgvector with HNSW drops
  to brute-force on tight filters.
- We almost always have a tight filter (tenant_id, doc_type). That's the
  case where pgvector hurts.

## Conclusion
*Tentative.* For our specific filtering pattern (always-on tenant_id +
frequent doc_type), pgvector is likely to be the slow path, not the
"good enough" baseline I assumed. Qdrant looks like the right default; need
to validate on our corpus before committing.

## Reasoning
Hypothesis is leaning toward rejection but not yet there — I haven't measured
on our own corpus. Want to run a small filtered-ANN probe before promoting
this to LESSONS.

## Next
- Queue: small filtered-ANN probe on a 100k-doc sample (one-off script,
  still research-only — record numbers as Thoughts in the next log entry).
- Once user confirms the conclusion stands after the probe → promote to
  LESSONS.md.

## Linked
- archive/014-pgvector-bench.md
- archive/014-qdrant-bench.md
- archive/014-weaviate-bench.md
- archive/014-ops-matrix.md
```

### Example: compression

```markdown
# compression 048 — snapshot 001

## What & why
MEMORY.md hit 392 lines after a long run on warmup/optimizer experiments. Cap is 400; rewrite before the next dispatch.

## Done
Copied current MEMORY.md → memory/001-memory.md. Rewrote MEMORY.md in place: kept fixed sections; collapsed `Recent` from 18 entries to last 8; merged six exhausted approaches into two `Avoid` lines; promoted resolved warmup question to LESSONS.

## Result
- Before: 392 lines. After: 184 lines.
- Snapshot saved at memory/001-memory.md.

## Reasoning
Routine compression, no surprises. Rewrite preserved all load-bearing context; older `Recent` entries are recoverable from log.tsv if needed.

## Next
- Continue from Queue head.

## Linked
- memory/001-memory.md
```

### Example: escalation

```markdown
# escalation 036 — L2 → L3

## What & why
Last 6 experiments at strategy level 2 (systematic exploration) returned deltas < 0.003 — below the noise threshold. Plateau detected; escalating one level early per §5.

## Done
Updated `MEMORY.md ## Status`: strategy level 2 → 3 (structural changes). Pruned remaining L2-flavoured items from Queue; added two L3 candidates (replace attention block, swap optimizer family).

## Result
- New strategy level: 3.
- Queue rebalanced: 4 items (was 7).

## Reasoning
Plateau is a signal to escalate, not stop (§1, principle 8). L2 hyperparameter sweeps have stopped paying out; L3 structural changes are the next bet.

## Next
- Dispatch first L3 candidate (Queue #1: replace attention block with grouped-query attention).

## Linked
- (no archive artefacts — pure state change)
```

---

## memory/NNN-memory.md

**Role:** a frozen `MEMORY.md` snapshot taken at compression time. Read-only to the rest of the system. Used for:

- cold-start with deep context (when one needs to understand *why* we arrived at the current state);
- traceability — "when exactly did we start avoiding X?".

The content is a verbatim copy of `MEMORY.md` at the moment of compression. The file is not edited after creation.

---

## log.tsv

**Role:** a single append-only log of every action by main and sub-agents.

**Header:**

```
NNN	timestamp	type	actor	metric	delta	status	description	linked_files
```

**Columns:**

| Column | Meaning |
|---|---|
| `NNN` | Zero-padded id, monotonic across all action types |
| `timestamp` | ISO 8601 |
| `type` | `experiment` \| `research` \| `analysis` \| `compression` \| `escalation` \| **any other** type main introduces (e.g., `critique`, `profile`, `reflection`) |
| `actor` | `main` \| `experiment` \| `researcher` \| `baseline` \| **any other** briefed sub-agent role |
| `metric` | metric value (for `experiment` in experiment mode) or `-` (always `-` in research-only mode) |
| `delta` | signed delta vs best (for `experiment` in experiment mode) or `-` (always `-` in research-only mode) |
| `status` | `running` (in flight) \| `keep` \| `discard` \| `crash` \| `done` (for non-experiments) |
| `description` | one phrase |
| `linked_files` | comma-separated paths in `log/` and `archive/`. **Never** include `MEMORY.md`, `LESSONS.md`, `CONFIG.md` |

Append-only for new actions, but the row of an in-flight action may be updated in place when it completes (e.g. `status: running → keep/discard/crash`, fill in `metric` and `delta`). Other cells are not rewritten retroactively; if a final status was recorded by mistake, append a correction row with `type=analysis` and the explanation in `description`.

---

## archive/

**Role:** free-form bin for auxiliary artefacts: paper PDFs, `.py` / `.ipynb` scripts from researchers, intermediate data, screenshots, profiles, traces.

**Writers:** all agents, including sub-agents. This is the only path through which sub-agents leave artefacts.

**Naming convention:** prefix with `NNN-` matching the action id, to preserve traceability. Examples:

- `archive/003-attention-paper.pdf`
- `archive/003-eda.ipynb`
- `archive/007-bench-output.txt`
- `archive/012-mfu-trace.png`
- `archive/015-train-curves.csv`
- `archive/018-profile.json`
- `archive/022-bench-summary.md`
- `archive/025-ablation.py`
- ... (anything else useful — `.log`, `.svg`, `.tar.gz`, whatever helps)

Collisions are extremely unlikely with the default concurrency (1 experiment + 3 sub-agents) and meaningful prefixing.
