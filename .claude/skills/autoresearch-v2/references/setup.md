# setup.md — autoresearch configuration stages

Setup is the only phase in which `CONFIG.md`, `RESUME.md`, and the eval command can change. After a successful baseline (exp/000) the frozen contract is active and any change requires a deliberate re-setup.

Setup has three sequential stages: **Interview → Scaffold → Baseline**.

A note on the two frozen files we are about to produce:

- **`CONFIG.md`** is the **active contract** — re-read frequently by the agent whenever a decision depends on the contract (every dispatch, every diff validation, every session start).
- **`RESUME.md`** is the **accumulated context for re-setup** — what the user already told us about themselves, the environment, the bootstrap. It is also loaded on warm start, but its primary value is to make re-setup cheap if the metric, scope, or eval needs to change later.

Setup invests time in both because the contract will be frozen and any correction is expensive.

---

## Stage 1 — Interview

Goal: extract a minimally sufficient configuration from the user. Walk through `interview.md` — a question bank, not a script. Don't read it top to bottom; ask what's needed.

### What to collect

1. **Goal and metric.** What we are optimising (one sentence). Metric name. Direction (min/max). Minimum delta that counts as improvement (anything smaller is noise). For exact metrics — set noise threshold to `None`.
2. **Eval.** A single shell command that prints one scalar. Timeout. Parse method:
   - `summary_block` — grep for `<metric_name>:` in stdout;
   - `regex:<pattern>` — pattern over stdout;
   - `json_path:<path>` — path into a JSON document;
   - `file:<path>` — read the value from a file;
   - `exit_code` — 1 if exit==0, else 0.

   If eval is a multi-step pipeline (build Docker → screenshot → LLM-judge → extract), the user wraps it in `eval.sh`. The skill sees a **single** command.
3. **Scope.** Files the agent may edit (target). Files that are read-only context. Files that must not be touched at all.
4. **Anti-gaming constraints.** Specific dirty ways to inflate the metric that should be banned upfront (deleting safety checks, shortening eval, replacing real tests with mocks).
5. **Integrations.** W&B project, MLflow, Slack hooks — present this block explicitly even if the user has nothing to add (see `interview.md` Block 6).
6. **Envs.** Environment variables and keys. Keys are **not** stored directly — only references to `.env`. The user confirms each one is present.
7. **Bootstrap.** Commands to run once before the first experiment (`uv sync`, `prepare.py`, data download, tokenizer training). Recorded in `RESUME.md`.
8. **Concurrency budget.** Confirm the default `1 experiment + 3 sub-agents` or adjust.
9. **Termination criteria.** When to stop (max experiments / no-improvement window / unlimited).

### Interview principles

- **Re-ask until the answer is unambiguous.** "Performance" is not a metric. "p50 latency in ms from `pytest bench.py`" is.
- **Don't dump questions in batches.** One or two per turn.
- **Confirm phrasings.** After each block, briefly restate what was understood.
- Important answers and envs → `RESUME.md ## Important answers` and `## Envs`. Eval command + scope + constraints → `CONFIG.md`.

---

## Stage 2 — Scaffold

Create the project structure:

```
autoresearch/
├── CONFIG.md           # frozen contract
├── RESUME.md           # frozen interview answers + envs + bootstrap commands
├── MEMORY.md           # template with all fixed sections, empty
├── LESSONS.md          # empty
├── log.tsv             # header only
├── log/                # empty
├── memory/             # empty
└── archive/            # empty
```

### Steps

1. **`CONFIG.md`** — fill in from interview answers. Frozen after baseline.
2. **`RESUME.md`** — distillation of important answers + envs (with `.env` references, never raw keys) + the bootstrap command sequence. Frozen after baseline.
3. **`MEMORY.md`** — initialise from the template in `file-structure.md`. All fixed sections present, fields empty / placeholders.
4. **`LESSONS.md`** — empty (with a heading and a brief note on the entry format).
5. **`log.tsv`** — a single header line:

   ```
   NNN	timestamp	type	actor	metric	delta	status	description	linked_files
   ```

6. **`log/`, `memory/`, `archive/`** — create as empty directories (with `.gitkeep` if needed).

After scaffold, show the user the resulting tree and the final `CONFIG.md` + `RESUME.md` for confirmation. Only after an explicit "ok" — proceed to baseline.

---

## Stage 3 — Baseline

**Required.** The frozen contract is not active until baseline succeeds.

### Why

- Pin the starting metric. Without it there is nothing to compare the first experiments to.
- Verify that bootstrap and the eval command actually work as described. Better to fail here than after five experiments to discover the eval is parsed incorrectly.

### Steps

1. **Run the bootstrap commands** from `RESUME.md` (if not already done).
2. **Run the eval command without changes to the target file** → exp/000.
3. **Wait for completion**, parse the metric per `CONFIG.md ## Eval`.
4. **Record the result:**
   - `MEMORY.md ## Best`: `<metric>=<value> @ exp 000`.
   - `log.tsv`: row with status=`keep`, type=`experiment`, actor=`baseline`.
   - `log/000-experiment-baseline.md`: follows the standard `log/` entry structure (see `file-structure.md`). The `Done` section captures the baseline configuration; `Result` captures the metric value plus an environment fingerprint (GPU model, library versions if relevant); `Reasoning` confirms the contract is operable; `Next` seeds the Queue.
5. **Activate the frozen contract:** `CONFIG.md`, `RESUME.md`, and the eval command are now immutable. Any change requires re-setup.
6. **Seed `MEMORY.md ## Queue`** — 2–3 first low-hanging-fruit hypotheses, confirmed by the user (or proposed and confirmed).

### If baseline fails

- Capture the cause in `log/000-experiment-baseline.md`.
- Return to Stage 2 — fix `RESUME.md ## Bootstrap` or `CONFIG.md ## Eval`.
- Re-run baseline. The frozen contract activates **only after** a successful baseline.

---

## After setup

The skill enters steady-state coordinator mode. Further behaviour is described in `SKILL.md §2–§5`. Setup is repeated only when the user explicitly asks ("let's reconfigure" / "change the metric" / "expand scope") — that is a deliberate, one-off operation, not part of the normal cycle.

When re-setup happens, `RESUME.md` becomes the cheat-sheet: most environment questions, envs, and bootstrap details don't need to be re-asked — only the deltas (the new metric, the new scope, the new eval) are revisited and merged into the contract.
