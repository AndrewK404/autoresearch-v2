# autoresearch

**A principles-first Claude Code skill for autonomous optimization.** Point the
agent at a target file (or scope) and one scalar metric with a direction
(min/max). The Claude Code main thread becomes an event-driven coordinator that
iterates: hypothesize → edit → eval → keep/discard → learn → repeat, until you
stop it.

Works for ML training (`val_loss`, `val_bpb`), API performance (`p50_ms`),
bundle size, prompt pass-rate, LLM-judged quality — for **any** metric that
reduces to one shell command printing one parseable scalar.

## Install & run

```bash
git clone https://github.com/AndrewK404/autoresearch-v2 ~/.claude/skills/autoresearch-v2
```

Then in any project, tell Claude Code: `run autoresearch`.

Or via the plugin marketplace:

```
/plugin marketplace add AndrewK404/autoresearch-v2
/plugin install autoresearch-v2@autoresearch-v2
```

## Architecture

After setup, the Claude Code main thread is an event-driven coordinator. It
dispatches sub-agents in the background and integrates returns as they arrive:

- **experiment** — a background launch of the eval command.
- **researcher / analyst / falsifier / ...** — sub-agents spawned through the
  general agent built into Claude Code: source digest, literature sweep, light
  EDA, post-mortem, falsification before run.

Concurrency: **1 experiment + 3 sub-agents in parallel** (sub-agents run in
the background).

```
       ┌──────────────────────────────────────┐
       │              setup                   │
       │  (interview → scaffold → baseline)   │
       └──────────────────┬───────────────────┘
                          ▼
   ┌──────────────────────▼───────────────────┐
   │           main coordinator               │ ◄──── async returns
   │   think → dispatch → integrate → think   │
   └──┬────────────────────────────────┬──────┘
      │                                │
      ▼                                ▼
  experiment                       sub-agents
  (background run                  (researcher, analyst,
   of eval command)                 falsifier, ...)
```

## File layout in the user's project

After setup, the project gets:

```
autoresearch/
├── CONFIG.md           # frozen: goal, metric, eval, scope, constraints
├── RESUME.md           # frozen: important interview answers + envs + bootstrap
├── MEMORY.md           # live dashboard, 400-line cap
├── LESSONS.md          # confirmed lessons (≥ 2 keep)
├── log.tsv             # single action log
├── log/                # detailed NNN-<type>-<info>.md (e.g. 023-experiment-batch-256.md)
├── memory/             # archived MEMORY.md snapshots (NNN-memory.md)
└── archive/            # PDFs, scripts, notebooks, intermediate data
                        #   (the only path for sub-agents)
```

## Why it works

1. **Single target, single scalar.** Drift is impossible; keep/discard is just
   `<` or `>`.
2. **Frozen contract.** `CONFIG.md`, `RESUME.md`, and the eval command are
   immutable after baseline.
3. **Experiments = ground truth, research = advisory.** Only ≥ 2 keep
   experiments promote a claim into `LESSONS.md`.
4. **Falsification over confirmation.** Every hypothesis carries a numeric
   falsifier.
5. **Async, event-driven.** Main is idle only when capacity is full AND the
   Queue is empty.
6. **Strategy escalation by experiment count.** 1–5 / 6–15 / 16–30 / 30+ — the
   strategy level is explicit and escalates one level early on plateau.
7. **Expensive resources never sit idle.** While an experiment runs, main
   works in parallel — research, pruning, sharpening.
8. **Never gives up.** Plateau is a signal to escalate, not to stop.

## Known limitations

- Single-node by default; remote compute lives behind the eval command.
- Linear keep/discard against the current best; no branching / tournament
  search.
- LLM-judged metrics are noisy — trust trends, not single comparisons.
- Metric gaming is possible — encode hard rules in `CONFIG.md ## Constraints`.


## Inspiration

- [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) —
  the original minimal single-file / single-metric autonomous loop.
- [Anthropic's multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) —
  sub-agent architecture, task-briefing.
- [Popper](https://arxiv.org/abs/2502.09858), [AIGS](https://agent-force.github.io/AIGS/) —
  falsification-first hypothesis validation.
- [Sakana AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) —
  progressive experimentation.
- MemGPT / [Letta](https://www.letta.com/blog/agent-memory),
  [Generative Agents](https://arxiv.org/abs/2304.03442) — long-term memory
  patterns.
