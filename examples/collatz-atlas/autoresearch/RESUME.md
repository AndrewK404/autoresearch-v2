# RESUME

## Important answers
- Mode: research-only with computational sub-tasks. The "experiments" the
  user means in TASK.md are parameter sweeps + orbit analysis written as
  scripts in `archive/`, not skill-level experiment-mode runs against a
  fixed eval command.
- Initial sweep scope: 3x+1 family, `n → (a·n+b)/2^k` for odd a, b with the
  even branch dividing by 2 fully. Opening sweep: a ∈ {1,3,5,7},
  b ∈ {1,3,5,7,9,11,13,15,17,19,21}. Wider divisor (c ∈ {2,3,4}) and
  Conway-style mod-m piecewise variants come later, after the baseline atlas
  for the tight scope is mapped.
- Initial per-orbit horizons: S=10^4 starting seeds, H=10^12 value bound,
  T=10^4 step bound. Higher horizons (10^5, 10^18, 10^5) are reserved for
  falsification of candidate conjectures in later cycles.
- Confirmation cadence: the agent runs autonomously and only pings the user
  when (a) a conjecture is candidate for promotion to `LESSONS.md`, or
  (b) escalating from L2→L3 or L3→L4 in strategy levels. Other progress is
  visible via `MEMORY.md` and `log/`.
- Hardware: laptop-scale, no GPU. CPU only. Prefer arbitrary-precision
  integers via `gmpy2` if performance demands it; default to Python `int`
  otherwise (it is already arbitrary-precision).
- Reproducibility expectation from the user: single-command regeneration of
  all results, fixed seeds, atlas in a reusable form (CSV/Parquet + loader).

## Envs
(no envs / API keys required for this research)

## Bootstrap
The command sequence to prepare the environment. Run once on first setup.
If something breaks, recreate the environment and repeat.

1. `python3 --version` — confirm Python ≥ 3.10 available.
2. `python3 -m venv .venv && source .venv/bin/activate` — create local venv.
3. `pip install gmpy2 numpy pandas pyarrow` — minimal deps. `gmpy2` is
   used only for very large integers; the opening atlas does not need it,
   but having it ready avoids a re-bootstrap when horizons expand.
4. Smoke test: `python3 -c "import gmpy2, numpy, pandas, pyarrow; print('ok')"`.

If `gmpy2` install fails on macOS without `mpfr`/`gmp`/`mpc` libraries,
fall back to:
- `brew install gmp mpfr mpc` then retry, OR
- skip `gmpy2` and use Python's built-in `int` (slower but works);
  document the fallback in `archive/000-bootstrap-notes.md`.

## Notes
- TASK.md is the source brief and is treated as read-only context.
- The output `README.md` (the user-facing deliverable) lives at the project
  root, not inside `autoresearch/`. The `autoresearch/` directory is the
  workspace; the README is the artefact.
