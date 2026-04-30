---
name: autoresearch-v2
description: Turns the Claude Code main thread into an event-driven coordinator for autonomous optimization. Use when the user asks to autonomously improve something measurable: optimize a file by a metric, run experiments on code, iteratively reduce loss / latency / bundle size, raise pass rate, improve a prompt eval score, "run experiments on this", "make this faster/smaller/better autonomously", "find a better version", "keep iterating until I stop you". Works for ML training (val_loss, val_bpb), API performance (p50_ms), bundle size, prompt pass-rate, LLM-judged quality — for ANY metric that reduces to a single shell command printing one parseable scalar. Also triggers on phrases like "run autoresearch", "start the experiment loop", "optimize X by metric Y", "iterate on this autonomously".
---

# autoresearch

A skill that turns the Claude Code main thread into an event-driven coordinator for autonomous optimization. You point it at a target file (or scope) and one scalar metric with a direction (min/max). The agent iterates: hypothesize → edit → eval → keep/discard → learn → repeat, until you stop it.

## 1. Core principles

1. **Single target, single scalar** *(experiment mode)*. Drift is impossible; keep/discard is just `<` or `>`. In **research-only mode** (no executable experiment) there is no scalar — the loop is hypothesis → investigation → conclusion logged to `log/` (see §1a).
2. **Frozen contract.** `CONFIG.md`, `RESUME.md`, and (in experiment mode) the eval command are immutable after baseline. Changes require an explicit re-setup.
3. **Experiments = ground truth, research = advisory.** Only ≥ 2 confirming keep experiments promote a claim into `LESSONS.md`. *(In research-only mode, `LESSONS.md` is populated from the user's own confirmed conclusions instead — see §1a.)*
4. **Async, event-driven.** Sub-agent returns arrive asynchronously. No cycle pairing, no fixed cadence.
5. **Falsification over confirmation.** Every hypothesis carries a numeric falsifier *(experiment mode)* or a clearly stated rejection condition *(research-only mode)*. Investigations are designed to risk being wrong.
6. **Main never idle.** While sub-agents work, main keeps going: sharpening the next brief, pruning the Queue, compressing MEMORY, dispatching new work. Idle is acceptable only when capacity is full AND the Queue is empty.
7. **Expensive resources never sit idle.** Experiments (especially GPU) must not wait while we do detailed analysis that could run in the background. Thinking to formulate a sharper hypothesis is fine; lengthy investigation is not.
8. **Never gives up.** A plateau, an exhausted Queue, a streak of discards — these are signals to **escalate the strategy level** (see §5), not to stop. Stopping is allowed only on explicit conditions in `CONFIG.md ## Termination` or by user command. If every idea "obviously won't work", we move to the next level: systematic → structural → radical rethinking. The metric, scope, or problem framing may be wrong — but that conclusion is reached *through* experiments, not by refusing to run them.

## 1a. Operating modes

The **first question of the interview** (see `references/interview.md`) determines the mode:

- **Experiment mode** *(default)* — research that involves a direct, executable experiment (a shell command that prints one scalar). The full loop applies: hypothesize → edit → eval → keep/discard → learn. All sections of this document apply as written.
- **Research-only mode** — the work is investigative (literature surveys, analysis, comparison studies, design exploration) without an executable experiment. The Stage 0 baseline (exp/000) is **skipped**, the eval block in `CONFIG.md` is **omitted**, and the cycle becomes: hypothesize → investigate (research/analysis sub-agents, optional manual experimentation) → record thoughts and conclusions in `log/NNN-<type>-<info>.md`. The user — not an automated metric — decides whether a finding is solid; once they confirm, it can be promoted to `LESSONS.md`.

Mode is recorded in `CONFIG.md ## Mode` and is part of the frozen contract. Switching modes requires a re-setup.

## 2. End-to-end flow

**Stage 0 — Setup (one-time).** After the interview the project has an `autoresearch/` directory at the **project root** containing: `CONFIG.md`, `RESUME.md`, `MEMORY.md`, `LESSONS.md`, `log/`, `memory/`, `archive/`, `log.tsv`. *In experiment mode* a baseline (exp/000) has been run and the starting metric is fixed. *In research-only mode* the baseline is skipped and the contract is activated as soon as the user confirms `CONFIG.md` and `RESUME.md`. Either way, the frozen contract becomes active at the end of Stage 0.

**Stage 1 — Kick-off.**
- The user states the task.
- *Experiment mode:* form a hypothesis and launch an experiment in the background (`uv run ...` or similar).
- *Research-only mode:* form a hypothesis and dispatch the first investigation (research / analysis sub-agent, doc digest, profiler, etc.). No background eval command runs.

**Stage 2 — Parallel work (THE CORE).** While the experiment runs:
- identify topics where knowledge is thin;
- spawn sub-agents (research / analysis / any other useful task) through the general agent built into Claude Code;
- every dispatch (experiment or sub-agent) is appended to `log.tsv`.

**Stage 3 — Result integration** (from a sub-agent OR from an experiment — the sequence is the same):

1. think
2. analyse the return carefully
3. write `log/NNN-<type>-<info>.md` (e.g. `054-research-lr-scheduler.md`) — in **research-only mode** this is also where the user's own thoughts and conclusions are saved (free-form `Thoughts` / `Conclusion` sections inside the same file)
4. update the corresponding row in `log.tsv`
5. update `MEMORY.md`
6. *Experiment mode:* if a lesson is now confirmed (≥ 2 keep) — update `LESSONS.md`. *Research-only mode:* if the user has explicitly confirmed a conclusion as solid, promote it to `LESSONS.md` with references to the supporting `log/` entries.
7. think
8. decide the next direction and dispatch the next sub-agent (analysis / research / scripted task / whatever fits)

The cycle continues until the user interrupts.

## 3. Coordination pattern

```
think → dispatch → integrate → think
```

Returns arrive asynchronously. No cycle pairing, no fixed cadence. Main does not synchronously wait for all sub-agents — it integrates each return the moment it arrives and moves on.

**Concurrency (default):** 1 experiment + 3 sub-agents in parallel (sub-agents run in the background).

**Experiment isolation:** experiments run in isolated git worktrees. On keep — merge into the main HEAD; on discard — the worktree is deleted.

## 4. Hypotheses and the Queue

`MEMORY.md ## Queue` holds a ranked backlog of hypotheses. Each one carries a **numeric falsifier**: "if X fails to reach Y under condition Z — reject".

Default flow: `Queue → researcher (optional, if theory needs preparation) → experiment (background shell command, not a sub-agent — see §8)`. Direct dispatch without a researcher is a valid judgement call, not a violation.

**A hypothesis can be rejected without an experiment** — based on a sub-agent's return. A researcher / analyst / falsifier can: show that the falsifier already contradicts data in `archive/`; produce a theoretical counterexample; find that the literature has systematically failed this approach in similar setups. In those cases the hypothesis is removed from the Queue with a note in `log/NNN-research-<info>.md` (or `log/NNN-analysis-<info>.md`) and a one-line entry in `MEMORY.md ## Avoid` — without spending experiment budget. The experiment remains the **final** arbiter (§1, principle 3); a sub-agent can only reject a hypothesis before it runs, not confirm it.

## 5. Strategy escalation by experiment count ⚠️ CRITICAL

The strategy level depends on the number of experiments run so far:

- **1–5 experiments:** low-hanging fruit (hyperparameters, obvious fixes).
- **6–15:** systematic exploration (architecture variations, optimizer changes).
- **16–30:** structural changes (new components, different approach).
- **30+:** radical rethinking (is the metric right? is the problem framed correctly?).

**Escalate one level early** when a plateau is detected (the last N experiments improved the metric by less than the threshold).

The current level lives in `MEMORY.md ## Status`. On a level change — record it in `log.tsv` and a one-line motivation in `MEMORY.md`.

## 6. Memory and state

### MEMORY.md — live dashboard

Hard cap: **400 lines**. Cold-startable: a fresh session needs only `CONFIG.md + RESUME.md + MEMORY.md + LESSONS.md` to understand the state and continue.

**Structure — fixed header + fixed sections + optional sections.** Full template example:

```markdown
Updated: 2026-04-28T10:14:00Z | Last action: 023

---

## Best
val_loss=2.314 @ exp 019
(added 200-step warmup, learning rate 3e-4 → 5e-4)

## Status
Focus: stabilise training at higher LR. Strategy level: 2 (systematic exploration).
Escalated one level early after plateau on L1 (4 experiments in a row, delta < 0.005).

## Queue
1. Replace AdamW → Lion at the current LR. Falsifier: if val_loss does not drop
   below 2.30 within 5 experiments, reject.
2. Cosine schedule with warmdown_ratio=0.7. Falsifier: val_loss < 2.305 with
   training_seconds within ±5% — otherwise reject.
3. <...>

## Recent
- exp 023: discard, +0.012 — raised batch to 256, MFU dropped
- res 022: done — digest of Lion paper (Chen et al., 2023), artefacts in archive/022-*
- exp 021: keep, -0.008 — warmdown_ratio 0.5 → 0.6
- ana 020: done — post-mortem of runs 015–019, found warmup pattern
- exp 019: keep, -0.018 — warmup steps 100 → 200

---

## Avoid
- Batch > 256 — exhausted, MFU degrades (exp 008, 014, 023)
- Dropout > 0.1 — exhausted, systematically worsens val_loss (exp 005, 011, 017)

## Open questions
- Why does warmdown with ratio > 0.7 cause a dip in the last 5% of training?
```

**Header** is the status line. **Best, Status, Queue, Recent** are fixed and always present. **Avoid, Open questions, Active threads**, and any other sections are added by the agent as the current goal demands.

**MEMORY.md also captures genuinely important user input mid-run.** After setup, if the user shares context that changes strategy, scope perception, or constraints — examples: "we just got a second GPU", "this paper is highly relevant to what you're doing", "actually, batch size 256 is fine if you accept the MFU drop" — the agent updates `MEMORY.md` (typically as a line in `Status`, an entry under `Open questions`, or a fresh optional section). Trivial chitchat does not go here. Anything that would change the contract itself (metric, scope, eval) is **not** a MEMORY update — it triggers a re-setup (see §7).

**At 400 lines (compression):**
1. Copy current `MEMORY.md` → `memory/NNN-memory.md` (zero-padded next id).
2. Rewrite `MEMORY.md` in place: keep fixed sections + still-relevant optional sections, compress the rest.

`memory/` is a read-only archive of historical snapshots. Useful for cold-start with deep context and for traceability — "when exactly did we start avoiding X?".

### LESSONS.md

Confirmed lessons grounded in **own experience**. Writes are allowed only after **≥ 2 keep experiments confirm the same falsifier statement** (i.e. the same falsifier from `MEMORY.md ## Queue` is satisfied twice — not just two keeps that loosely point in the same direction). Research-only insights do not go here (their place is `log/NNN-research-<info>.md`).

### log/

Per-action notes named `log/NNN-<type>-<info>.md`, where `<type>` is the action type (`experiment`, `research`, `analysis`, `compression`, `escalation`, …) and `<info>` is a short kebab-case slug describing the specific action. Examples: `054-research-lr-scheduler.md`, `023-experiment-batch-256.md`, `040-analysis-warmup-postmortem.md`. The detailed report for an action — everything that does not fit in a single `log.tsv` row.

**Hard requirement for `log/` entries: explicit reasoning and conclusions from the agent.** Each `log/NNN-*.md` records not just facts ("hypothesis was X, metric was Y, status keep") but also **what main was thinking before the dispatch, what it noticed along the way, what it concludes, and what it changes in Queue / MEMORY / LESSONS as a result.** This is the "thinking layer" between experiments that would otherwise be lost. If the experiment delivered a straightforward keep/discard with nothing to think about — say so explicitly, in one line ("expected, no surprises; next hypothesis from Queue unchanged"). Silence in `Reasoning` = lost context.

The exact structure is in `references/file-structure.md`.

### archive/

Auxiliary artefacts: paper PDFs, `.py` / `.ipynb` scripts from researchers, intermediate data, screenshots, profiles. **All agents — including sub-agents — write here.** Collisions are extremely unlikely.

### log.tsv

A single append-only log of every action by main and sub-agents. Columns:

```
NNN  timestamp  type  actor  metric  delta  status  description  linked_files
```

`type` ∈ {experiment, research, analysis, ...}. `linked_files` are paths in `log/` and `archive/` — but **not** the top-level files (`MEMORY.md`, `LESSONS.md`, `CONFIG.md` — those don't go here).

### Warm start (steady state)

Every new session (after the first setup) loads:

```
SKILL.md + CONFIG.md + RESUME.md + MEMORY.md + LESSONS.md
```

`references/*` are loaded on-demand when needed.

## 7. Files and write ownership

### CONFIG.md vs RESUME.md — different roles, both frozen

Both files are immutable after baseline, but they serve different purposes:

- **`CONFIG.md`** is the **active contract**: goal, metric, eval, scope, constraints, integrations. The agent re-reads it any time decisions depend on the contract — at session start, before each dispatch, when validating a diff.
- **`RESUME.md`** is the **accumulated context for re-setup**: which questions the user already answered, which envs exist, which bootstrap commands worked. It is also loaded on warm start so the agent knows the environment, but its primary job is to make re-setup cheap when the user wants to change scope, the metric, or the eval — we don't ask everything from scratch.

Re-setup happens when the **contract** must change ("let's also optimise memory, not just speed"; "you can now edit `utils.py`"; "the eval command should now use the held-out split"). User input that does **not** change the contract goes into `MEMORY.md`, not into a re-setup.

### Ownership table

| File | Purpose | Writer |
|---|---|---|
| `CONFIG.md` | Active frozen contract: goal, metric+direction, eval command, scope, anti-gaming constraints, integrations | Setup only |
| `RESUME.md` | Frozen accumulated context for re-setup: important interview answers + envs (refs to `.env`, never raw keys) + bootstrap commands | Setup only |
| `MEMORY.md` | Live dashboard (see §6), 400-line cap, also captures important mid-run user input | Main |
| `LESSONS.md` | Confirmed lessons (≥ 2 keep) | Main |
| `log/NNN-*.md` | Per-action detailed notes with explicit reasoning | Main (on integration of returns) |
| `memory/NNN-memory.md` | Frozen MEMORY.md snapshots from compression | Main (on compression) |
| `log.tsv` | Single append-only action log | Main |
| `archive/` | PDFs, scripts, notebooks, intermediate data | All agents, including sub-agents |
| `references/{setup,interview,file-structure}.md` | Skill-internal docs | Skill author |

## 8. Sub-agents

Spawned through the **general agent** built into Claude Code. **There are no separate system-prompt files in this skill.** Main writes the brief inline at dispatch.

The minimum set is researcher + analyst. **The list below is examples, not exhaustive — main is free to spawn any sub-agent type that fits the current knowledge gap, including ones not listed here (e.g. a `computer-use` sub-agent for browser/desktop automation, a `data-fetcher` for hitting external APIs, etc.).** Common types:

- **Researcher** — source digest, literature sweep, tool/library evaluation, surfacing numerically falsifiable hypotheses.
- **Analyst** — post-mortem of an experiment series on existing data, ablations over logs without new runs, checking correlations between hyperparameters and the metric.
- **Critic / sanity-check** — review a fresh keep critically: any metric gaming (removed asserts, shortened eval, hard-coded answers for known cases)?
- **Falsifier** — attempt to reject a Queue hypothesis **before** running an experiment, via theory / `archive/` data / literature (see §4).
- **Profiler** — find bottlenecks from logs or quick runs, rank candidates for optimisation.
- **Doc digest** — summarise library/API/SDK documentation on a specific question.
- **Reflection** — meta-review of the last N actions to surface a pattern main may have missed under focus.

**Researcher output:** numerically falsifiable hypotheses (or motivated rejection of an existing one — see §4) + artefacts in `archive/`.

**Experiment** is just a background launch of the command from `CONFIG.md` (**in the vast majority of cases this is NOT a separate agent** — it's a shell command Claude Code runs in the background; main queues the task, awaits the return asynchronously, and integrates the result). A sub-agent for an experiment is needed only in rare cases where the run itself requires meaningful decisions in flight (transient failure recovery, dynamic logging).

**Every sub-agent writes only to `archive/`.** Main is responsible for integrating the return into `MEMORY.md` / `log/NNN-*.md` / `log.tsv` / `LESSONS.md`.

## 9. Setup flow (3 stages)

Details in `references/setup.md`.

1. **Interview** — a single consolidated `AskUserQuestion` block (see `references/interview.md`). The **first question** of that block decides the operating mode (experiment vs research-only). The user answers all questions in one turn and may attach additional data (env keys, framework configs, links) in a follow-up message if asked. Important answers and envs → `RESUME.md`. Mode + (optionally) eval command + scope + constraints → `CONFIG.md`.
2. **Scaffold** — create the file tree, initialise empty `MEMORY.md`, `LESSONS.md`, `log.tsv` (header only), and empty `log/`, `memory/`, `archive/` directories.
3. **Baseline** — required **only in experiment mode**. Run exp/000 to fix the starting metric; without a successful baseline the frozen contract is not active. *In research-only mode this stage is skipped*; the contract activates as soon as the user confirms `CONFIG.md` and `RESUME.md`.

### Cold start (read order at first setup)

```
SKILL.md
  → references/setup.md
  → references/interview.md
  → references/file-structure.md
  → interview the user (single ask block; first question = mode)
  → scaffold
  → baseline (exp/000)        # experiment mode only
  → enter steady state
```

Warm start (subsequent sessions) — see §6.

## 10. Known limitations

- Single-node by default; remote compute lives behind the eval command.
- Linear keep/discard against the current best; no branching / tournament search.
- LLM-judged metrics are noisy — trust trends, not single comparisons.
- Metric gaming is possible — encode hard rules in `CONFIG.md ## Constraints`.