# CONFIG

## Mode
experiment

## Goal
Discover a `priority(element, n)` function that, used by the fixed greedy in
`problem/solve.py`, yields the largest cap set in F_3^n. Primary target n=8
(≥496 = validation, ≥512 = match FunSearch, >512 = world record). Then sweep
n=10, n=11.

## Metric
- Name: cap_set_size
- Direction: maximize
- Noise threshold: None (deterministic; integer count)
- Notes: deterministic given a fixed `priority` function and fixed `n`.

## Eval
- Command: `CAP_SET_N=8 python problem/eval.py`
- Timeout: 120 seconds
- Parse: summary_block (grep for `cap_set_size:` in stdout)
- Idempotent: yes (priority must be deterministic)

## Scope
- Target files: `problem/priority.py`
- Read-only context: `problem/solve.py`, `problem/eval.py`, `BACKGROUND.md`
- Forbidden: `problem/solve.py`, `problem/eval.py` (immutable)

## Constraints
- `priority` must be deterministic and side-effect-free.
- `priority` must return a finite real for every input (no NaN, no inf).
- Imports limited to: `math`, `itertools`, `functools`, `numpy`.
- No file I/O, no network, no subprocesses.
- `solve.py` and `eval.py` are immutable — no edits.
- Must not modify the verifier or eval logic.
- Returned cap set must pass `verify_cap_set` (the eval already enforces this).

## Integrations
- W&B: not used
- MLflow: not used
- Slack/Discord: not used
- Webhooks/email: not used
- External secrets: not used

## Concurrency
- Experiments in parallel: 1
- Sub-agents in parallel: 3

## Termination
- Plateau-stop: 50 experiments without improvement
- Target threshold: cap_set_size ≥ 512 at n=8 (success threshold; do not stop —
  continue toward >512 and then sweep n=10, 11)
- Manual interrupt allowed at any time
