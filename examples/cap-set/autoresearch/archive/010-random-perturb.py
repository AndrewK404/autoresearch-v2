"""Random perturbations on top of c2-target — see if a particular tiebreak helps."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Random tiebreaks within c2=3 cluster
best = 448
best_seed = None
for seed in range(50):
    rng = np.random.default_rng(seed)
    # Generate a random map from element tuple to a small perturbation
    # We can't store all 6561 -> use a deterministic hash-like
    coeffs = rng.integers(-100, 100, size=n).tolist()
    coeffs2 = rng.integers(-100, 100, size=(n, n)).tolist()
    def p(e, n, c=coeffs, c2_=coeffs2):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 1_000_000
        sec = sum(c[i] * e[i] for i in range(n))
        for i in range(n):
            for j in range(i+1, n):
                sec += c2_[i][j] * e[i] * e[j]
        return primary + float(sec)
    sz = bench(f"seed {seed}", p, n)
    if sz > best:
        best = sz
        best_seed = seed
        print(f"  >>> NEW BEST: {sz} at seed {seed}")

print(f"\nBest: {best} at seed {best_seed}")
