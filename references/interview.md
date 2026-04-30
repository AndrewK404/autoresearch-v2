# interview.md — single-block interview for setup

The interview is **one consolidated `AskUserQuestion` call**, not a multi-turn drill. Lay out every question the user can plausibly answer up front so they can fill in the whole picture in a single turn. Then, *only if the user signals they need to attach additional data* (env keys, framework config snippets, internal links, file uploads, etc.), follow up with a short data-collection message — that is the only acceptable second touch before scaffolding.

The goal is to populate `CONFIG.md` and `RESUME.md` (see `setup.md` Stage 1).

---

## The first question — operating mode

**This question must come first** in the ask block. It governs which of the later questions are even relevant.

> **Does this research involve a direct, executable experiment** (a single shell command that prints one scalar metric — `val_loss`, `p50_ms`, `bundle_kb`, pass-rate, LLM-judge score, etc.), **or is it research-only** (literature surveys, comparative analysis, design exploration, where there is no automated metric and you'll save your own thoughts and conclusions instead)?

- **Experiment mode** → all blocks below apply.
- **Research-only mode** → skip Block 2 (Eval), Block 4 (Anti-gaming), and the baseline run in Stage 3 of setup. The "experiments" steps are removed entirely; instead, the user's thoughts and conclusions are recorded in the `Thoughts` / `Conclusion` sections of `log/NNN-<type>-<info>.md` (free-form), and a finding can be promoted to `LESSONS.md` once the user explicitly confirms it as solid.

Record the chosen mode in `CONFIG.md ## Mode`. It becomes part of the frozen contract.

---

## The single ask block

Build one `AskUserQuestion` payload that includes the mode question above plus every applicable item below, grouped by heading. Skip the experiment-specific sections in research-only mode. Phrase questions as bullets the user can answer inline.

### Block 1 — Goal and metric

- What exactly are we optimising / investigating? In one sentence.
- *Experiment mode only:*
  - What is the metric called? How does it appear in the output (a number with units, a percentage, dimensionless)?
  - Direction: **minimise** or **maximise**?
  - Smallest delta you consider a real improvement (anything smaller is noise). For exact metrics (loss, exit code, integer counts) — `None`.
  - Is the metric stable across runs on the same data, or does it carry built-in jitter (LLM-judge, sampling, etc.)? If yes — how much?
- *Research-only mode only:*
  - What does "done" look like? E.g., "a written recommendation", "a comparison table across 5 frameworks", "a decision between approaches A/B/C with rationale".
  - What signals will the user use to call a conclusion solid (their own confirmation criterion replaces the ≥ 2 keep rule)?

### Block 2 — Eval *(experiment mode only — skip in research-only)*

- What command runs the eval? (one shell command that prints one scalar)
- Roughly how long is one run? What timeout should we set (with margin)?
- How does the metric appear in the output? (`summary_block` / `regex:<pattern>` / `json_path:<path>` / `file:<path>` / `exit_code`)
- Is eval one step or a pipeline? If a pipeline (build → run → judge → extract) — wrap it in `eval.sh`. Where does it live, or does it need to be written?
- Is eval idempotent (same code → same metric value)? If not — what introduces the variance?

### Block 3 — Scope

- Which files may the agent edit? (exact paths)
- Which files should the agent **read** but **not edit**? (read-only context)
- What must not be touched under any circumstances?
- *Experiment mode:* roughly how many lines are in the target file? (to gauge how large edits can realistically be)

### Block 4 — Anti-gaming constraints *(experiment mode only — skip in research-only)*

- Which "dirty" ways to inflate the metric should be banned upfront? Be specific:
  - deleting safety checks?
  - replacing real tests with mocks?
  - shortening eval (fewer samples, smaller batch, shorter sequence)?
  - changing ground-truth labels?
  - hard-coding answers for known test cases?
- Are there tests or validators that **must** pass on every keep? (If eval does not run them itself — they need to be stated explicitly under `## Constraints`.)

### Block 5 — Environment and bootstrap

- What needs to happen **once** before the first run? Specific commands:
  - install dependencies (`uv sync`, `pip install -r ...`)?
  - data download / preprocessing?
  - tokenizer / index training?
  - anything else?
- Is there a smoke test that confirms the environment is ready? If not — what cheap one could be added?
- Which envs / API keys are needed? **Variable names, not values.** Are they already in `.env`? If not — note which ones still need to be added; the user attaches them in the data follow-up step (see "Data the user attaches" below).

### Block 6 — Integrations

Always include this section, even if the user is likely to answer "none" to everything. After baseline these answers join the frozen contract and changing them requires re-setup.

- W&B project / entity? (if used)
- MLflow / Tensorboard / another tracking system?
- Slack / Discord / other hooks on keep experiments?
- Status webhooks (e.g., on crash or plateau)?
- Notifications / email / pager?
- External secrets / vaults?
- Anything else specific to the project?

If no integration is needed — record `not used` against each, so a future re-setup shows the question was asked and the answer was deliberate.

### Block 7 — Concurrency and termination

- Confirm the default: 1 experiment + 3 sub-agents in parallel (sub-agents run in the background)? Or adjust based on available resources (GPU memory, API rate limits)? *In research-only mode the experiment slot is unused; default becomes 4 sub-agents in parallel unless the user specifies otherwise.*
- When to stop?
  - max N experiments / investigations?
  - K cycles in a row without a new finding (plateau)?
  - unlimited — stop only manually?
- *Experiment mode:* should I stop and report on reaching a target metric value? (target threshold)

---

## Data the user attaches (only if needed)

If — and only if — the answers above reveal that the user must hand over additional material that does not fit into a chat reply (env keys to write into `.env`, a framework config file to read, a paper PDF, a sample dataset, internal documentation links), follow up with **one** short message asking for those specific items by name. Do not turn this into a second round of questions; it is a data drop, not an interview.

---

## After the ask block

1. Parse the user's response into draft `CONFIG.md` (including `## Mode`) and `RESUME.md`.
2. Show the drafts back to the user and ask for explicit confirmation.
3. If the user edits anything — update, re-show the diff, re-confirm.
4. Move to Stage 2 (Scaffold) only after an explicit "ok".
