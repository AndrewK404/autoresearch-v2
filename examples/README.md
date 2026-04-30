# Examples

Successful runs of `autoresearch` where meaningful results were achieved.
Each subdirectory holds the complete skill working tree (`autoresearch/`)
plus a top-level `report.md` summarising the achievement and the trace.
The original problem scaffolding (the read-only `problem/`, the
`BACKGROUND.md`, the prompt that started the run) is preserved alongside
so the run is reproducible end-to-end.

## Index

| Example | Domain | Headline result |
|---|---|---|
| [cap-set/](cap-set/) | extremal combinatorics — cap sets in F₃ⁿ | matched the published records at n=8 (**512**) and n=9 (**1082**); reached **2240** at n=10 (the classical 112 × 20 product) and **5040** at n=11 (112 × 45) by combining FunSearch's published priorities with sectioning + Pellegrino's hyperplane-removal recipe |

## Per-example layout

```
<example-name>/
├── autoresearch/      # skill working tree (CONFIG, MEMORY, LESSONS, log/, archive/, ...)
├── report.md          # what was achieved + brief trace summary
└── problem/           # the original scaffold:
    ├── PROMPT.md      #   the prompt that launched the run
    ├── BACKGROUND.md  #   read-only context handed to the skill
    ├── priority.py    #   the target file (the one autoresearch evolves)
    ├── solve.py       #   read-only skeleton
    └── eval.py        #   read-only eval that prints the metric
```
