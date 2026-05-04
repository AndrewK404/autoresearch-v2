# setup.md — autoresearch configuration stages

Setup is the only phase in which `CONFIG.md` and (in experiment mode) the eval command can change. After Stage 3 the frozen contract is active and any change requires a deliberate re-setup.

Setup has three sequential stages: **Interview → Scaffold → Baseline**. The Baseline stage is **only run in experiment mode**; in research-only mode it is replaced by a lightweight contract activation step (see Stage 3 below).

`CONFIG.md` is the single frozen contract — re-read frequently by the agent whenever a decision depends on the contract (every dispatch, every diff validation, every session start). It holds everything the interview produced: goal, metric / done-criterion, eval, scope, constraints, integrations, envs, bootstrap, and any important interview answers. After setup, all new user input goes into `MEMORY.md`, never into `CONFIG.md`.

Setup invests time in `CONFIG.md` because it will be frozen and any correction is expensive.

---

## Stage 1 — Interview

Goal: extract a minimally sufficient configuration from the user **in a single `AskUserQuestion` block**. Build that block from `interview.md`, with the **mode question first**. The user answers everything in one turn; if they need to attach data that doesn't fit into a chat reply (env keys, framework configs, links, files), do **one** short follow-up data drop — not another round of questions.

### What to collect

0. **Mode (the first question).** Experiment vs research-only. Recorded as `CONFIG.md ## Mode`. In research-only mode items 2 and 4 below are skipped.
1. **Goal and metric.** What we are optimising or investigating (one sentence). *Experiment mode:* metric name, direction, noise threshold (or `None` for exact metrics). *Research-only mode:* what "done" looks like and the user's confirmation criterion for solid findings.
2. **Eval** *(experiment mode only)*. A single shell command that prints one scalar. Timeout. Parse method:
   - `summary_block` — grep for `<metric_name>:` in stdout;
   - `regex:<pattern>` — pattern over stdout;
   - `json_path:<path>` — path into a JSON document;
   - `file:<path>` — read the value from a file;
   - `exit_code` — 1 if exit==0, else 0.

   If eval is a multi-step pipeline (build Docker → screenshot → LLM-judge → extract), the user wraps it in `eval.sh`. The skill sees a **single** command.
3. **Scope.** Files the agent may edit (target). Files that are read-only context. Files that must not be touched at all.
4. **Anti-gaming constraints** *(experiment mode only)*. Specific dirty ways to inflate the metric that should be banned upfront (deleting safety checks, shortening eval, replacing real tests with mocks).
5. **Integrations.** W&B project, MLflow, Slack hooks — present this block explicitly even if the user has nothing to add (see `interview.md` Block 6).
6. **Envs.** Environment variables and keys. Keys are **not** stored directly — only references to `.env`. Missing keys are collected in the data follow-up step.
7. **Bootstrap.** Commands to run once before the first experiment / investigation (`uv sync`, `prepare.py`, data download, tokenizer training).
8. **Concurrency budget.** Confirm the default `1 experiment + 3 sub-agents` (experiment mode) or `4 sub-agents` (research-only mode), or adjust.
9. **Termination criteria.** When to stop (max experiments / no-improvement window / unlimited).

### Interview principles

- **One ask block.** Lay out every applicable question in a single `AskUserQuestion` payload, mode first. Skip experiment-only blocks in research-only mode.
- **Re-ask only on ambiguity.** "Performance" is not a metric. "p50 latency in ms from `pytest bench.py`" is. If the user's answer is genuinely unclear after the single ask, narrow the follow-up to just the unclear item.
- **Confirm at the end.** After the user answers, show the draft of `CONFIG.md` and request explicit confirmation.
- Everything from the interview lands in **one file**: `CONFIG.md` (mode, metric/done-criterion, eval, scope, constraints, integrations, envs, bootstrap, important answers).

---

## Stage 2 — Scaffold

Create the project structure:

```
autoresearch/
├── CONFIG.md           # frozen contract (single source of truth)
├── MEMORY.md           # template with all fixed sections, empty
├── LESSONS.md          # empty
├── log.tsv             # header only
├── log/                # empty
├── memory/             # empty
└── archive/            # empty
```

### Steps

1. **`CONFIG.md`** — fill in from interview answers (all of them — mode, metric/done, eval, scope, constraints, integrations, envs, bootstrap, important answers). Frozen after baseline.
2. **`MEMORY.md`** — initialise from the template in `file-structure.md`. All fixed sections present, fields empty / placeholders.
3. **`LESSONS.md`** — empty (with a heading and a brief note on the entry format).
4. **`log.tsv`** — a single header line:

   ```
   NNN	timestamp	type	actor	metric	delta	status	description	linked_files
   ```

5. **`log/`, `memory/`, `archive/`** — create as empty directories (with `.gitkeep` if needed).

After scaffold, show the user the resulting tree and the final `CONFIG.md` for confirmation. Only after an explicit "ok" — proceed to baseline.

---

## Stage 3 — Baseline (experiment mode) / Activation (research-only mode)

The frozen contract is not active until this stage completes.

### Experiment mode — required baseline

#### Why

- Pin the starting metric. Without it there is nothing to compare the first experiments to.
- Verify that bootstrap and the eval command actually work as described. Better to fail here than after five experiments to discover the eval is parsed incorrectly.

#### Steps

1. **Run the bootstrap commands** from `CONFIG.md ## Bootstrap` (if not already done).
2. **Run the eval command without changes to the target file** → exp/000.
3. **Wait for completion**, parse the metric per `CONFIG.md ## Eval`.
4. **Record the result:**
   - `MEMORY.md ## Best`: `<metric>=<value> @ exp 000`.
   - `log.tsv`: row with status=`keep`, type=`experiment`, actor=`baseline`.
   - `log/000-experiment-baseline.md`: follows the standard `log/` entry structure (see `file-structure.md`). The `Done` section captures the baseline configuration; `Result` captures the metric value plus an environment fingerprint (GPU model, library versions if relevant); `Reasoning` confirms the contract is operable; `Next` seeds the Queue.
5. **Activate the frozen contract:** `CONFIG.md` and the eval command are now immutable. Any change requires re-setup.
6. **Seed `MEMORY.md ## Queue`** — 2–3 first low-hanging-fruit hypotheses, confirmed by the user (or proposed and confirmed).

#### If baseline fails

- Capture the cause in `log/000-experiment-baseline.md`.
- Return to Stage 2 — fix `CONFIG.md ## Bootstrap` or `CONFIG.md ## Eval`.
- Re-run baseline. The frozen contract activates **only after** a successful baseline.

### Research-only mode — activation (no experiment run)

There is no eval command to validate, no metric to pin. The activation step is short:

1. **Run the bootstrap commands** from `CONFIG.md ## Bootstrap` (if any are listed — e.g., installing a doc-fetcher CLI, syncing a corpus). If there are none, skip.
2. **Write `log/000-research-kickoff.md`** with the standard structure: `What & why` restates the research question, `Done` lists what setup achieved, `Result` is `n/a (research-only mode)`, `Reasoning` confirms the contract is operable and lists the user's confirmation criterion verbatim, `Next` seeds the Queue.
3. **Append a row to `log.tsv`** with `type=research`, `actor=baseline`, `metric=-`, `delta=-`, `status=done`.
4. **Activate the frozen contract:** `CONFIG.md` is now immutable. Mode is part of the contract; switching to experiment mode later requires re-setup.
5. **Seed `MEMORY.md ## Queue`** — 2–3 first investigation hypotheses, each with a clearly stated rejection condition (the falsifier analogue for research-only mode), confirmed by the user.

---

## After setup

The skill enters steady-state coordinator mode. Further behaviour is described in `SKILL.md §2–§5`. Setup is repeated only when the user explicitly asks ("let's reconfigure" / "change the metric" / "expand scope") — that is a deliberate, one-off operation, not part of the normal cycle.

**Mid-run user input** (anything short of a contract change — "we got a second GPU", "this paper is highly relevant", "actually batch=256 is fine") is recorded in `MEMORY.md`, not `CONFIG.md`. The agent adjusts behaviour on the next dispatch.

When re-setup happens, the agent re-reads `CONFIG.md` plus `MEMORY.md` and the user's delta, then rewrites `CONFIG.md` in place. Most fields (envs, bootstrap, scope) usually carry through unchanged; only the deltas (the new metric, the new scope, the new eval) are revisited and merged into the contract.
