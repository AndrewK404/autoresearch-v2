"""Search for >96-cap at n=6 by priority space exploration."""
import sys, os, itertools, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 6

def cap_size(priority_fn, n=6):
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: priority_fn(e, n), reverse=True)
    cap = []
    forb = set()
    for e in elements:
        if e in forb: continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return len(cap), cap

# Baseline at n=6
bench("baseline 0", lambda e, n: 0., n)
bench("c2=2", lambda e, n: -abs(sum(1 for x in e if x == 2) - 2), n)
bench("c2=3", lambda e, n: -abs(sum(1 for x in e if x == 2) - 3), n)
bench("c1=2", lambda e, n: -abs(sum(1 for x in e if x == 1) - 2), n)

# Tensor 9 × 9 cap — find 9-cap at n=3 via brute force
elements3 = list(itertools.product(range(3), repeat=3))

best_n3 = 0
best_n3_cap = None
for seed in range(200):
    rng = random.Random(seed)
    order = elements3[:]
    rng.shuffle(order)
    cap = []
    forb = set()
    for e in order:
        if e in forb: continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    if len(cap) > best_n3:
        best_n3 = len(cap)
        best_n3_cap = cap
print(f"\nBest cap at n=3: {best_n3}")
CAP_9 = frozenset(best_n3_cap)

# Tensor: priority for (a, b) with a, b ∈ CAP_9 → high
def p_tensor(e, n):
    a = e[:3]
    b = e[3:]
    if a in CAP_9 and b in CAP_9:
        return 1.0
    return 0.0

bench(f"tensor 9-cap × 9-cap", p_tensor, n)

# Many random priorities at n=6
print("\n--- random priorities at n=6 ---")
best_n6 = 96
for seed in range(2000):
    rng = random.Random(seed)
    coeffs = rng.uniform(-10, 10, n+1) if False else [rng.uniform(-10, 10) for _ in range(n+1)]
    # For each element, score = sum of (e_i * coeffs[i]) + nonlinear
    def p(e, n, c=coeffs):
        return sum(e[i] * c[i] for i in range(n)) + c[n] * sum(1 for x in e if x == 2)
    sz, _ = cap_size(p, n)
    if sz > best_n6:
        best_n6 = sz
        print(f"  seed {seed}: NEW BEST {best_n6}")

print(f"\nBest from random linear+c2: {best_n6}")

# Priority families
print("\n--- structural priorities at n=6 ---")
for k in range(0, 7):
    def p(e, n, k=k):
        c2 = sum(1 for x in e if x == 2)
        return -abs(c2 - k)
    sz, _ = cap_size(p, n)
    print(f"  c2={k}: {sz}")

# Combined
def p_n6_special(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 2) * 1000
    # Edel's known construction at n=6 uses specific structure
    # Try: prefer sum mod 3 == 0
    s = sum(e) % 3
    return primary - float(s)

bench("n6 c2=2 + sum mod 3", p_n6_special, n)
