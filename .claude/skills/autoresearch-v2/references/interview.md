# interview.md — question bank for setup

Don't read top to bottom. Ask as needed, one or two questions per turn, re-ask until the answer is unambiguous. After each thematic block, briefly summarise what was understood and ask for confirmation.

The goal is to populate `CONFIG.md` and `RESUME.md` (see `setup.md` Stage 1).

---

## Block 1 — Goal and metric

- What exactly are we optimising? In one sentence.
- What is the metric called? How does it appear in the output (a number with units, a percentage, dimensionless)?
- Direction: **minimise** or **maximise**?
- What is the smallest delta you consider a real improvement, not noise? For example, for val_loss: < 0.005 is noise; for p50 latency: < 1ms is noise. If the metric is exact (loss in ML training, exit code, integer counts) — set noise threshold to `None`.
- Is this metric stable across runs on the same data, or does it carry built-in jitter (LLM-judge, sampling, etc.)? If yes — how much?

---

## Block 2 — Eval

- What command runs the eval? (one shell command that prints one scalar)
- Roughly how long is one run? What timeout should we set (with margin)?
- How does the metric appear in the output?
  - a `metric_name: 0.123` summary block in stdout?
  - a regex over stdout?
  - a JSON file?
  - a plain file with a single value?
  - exit code (success/fail)?
- Is eval one step or a pipeline? If a pipeline (build → run → judge → extract) — wrap it in `eval.sh`. Where does it live, or does it need to be written?
- Is eval idempotent (same code → same metric value)? If not — what introduces the variance?

---

## Block 3 — Scope

- Which files may the agent edit? (exact paths)
- Which files should the agent **read** but **not edit**? (read-only context)
- What must not be touched under any circumstances?
- Roughly how many lines are in the target file? (to gauge how large edits can realistically be)

---

## Block 4 — Anti-gaming constraints

- Which "dirty" ways to inflate the metric should be banned upfront? Be specific:
  - deleting safety checks?
  - replacing real tests with mocks?
  - shortening eval (fewer samples, smaller batch, shorter sequence)?
  - changing ground-truth labels?
  - hard-coding answers for known test cases?
- Are there tests or validators that **must** pass on every keep? (If eval does not run them itself — they need to be stated explicitly under `## Constraints`.)

---

## Block 5 — Environment and bootstrap

- What needs to happen **once** before the first run? Specific commands:
  - install dependencies (`uv sync`, `pip install -r ...`)?
  - data download / preprocessing?
  - tokenizer / index training?
  - anything else?
- Is there a smoke test that confirms the environment is ready? If not — what cheap one could be added?
- Which envs / API keys are needed? **Variable names, not values.** Are they already in `.env`? If not — ask the user to add them and confirm.

---

## Block 6 — Integrations

**Always present this block**, even if it seems no integrations are needed. The user can answer "none" to every question — but the fact that we asked about typical integrations upfront matters: after baseline these answers join the frozen contract and changing them requires a re-setup.

- W&B project / entity? (if used)
- MLflow / Tensorboard / another tracking system?
- Slack / Discord / other hooks on keep experiments?
- Status webhooks (e.g., on crash or plateau)?
- Notifications / email / pager?
- External secrets / vaults?
- Anything else specific to the project?

If no integration is needed — record `not used` against each, so a future re-setup shows the question was asked and the answer was deliberate.

---

## Block 7 — Concurrency and termination

- Confirm the default: 1 experiment + 3 sub-agents in parallel (sub-agents run in the background)? Or adjust based on available resources (GPU memory, API rate limits)?
- When to stop?
  - max N experiments?
  - K experiments in a row without improvement (plateau)?
  - unlimited — stop only manually?
- Should I stop and report on reaching a target metric value? (target threshold)

---

## Block 8 — Final confirmation

After collecting all answers, show the user the **drafts of `CONFIG.md` and `RESUME.md`** and ask for explicit confirmation before scaffolding and running the baseline.

If the user edits anything — update, show the diff, re-confirm. Move to Stage 2 only after an explicit "ok".
