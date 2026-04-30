"""Find a 20-cap in F_3^4 by exhaustive priority search."""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
cap_set_size = m.cap_set_size

n = 4

def cap_set_with(priority_fn, n):
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: priority_fn(e, n), reverse=True)
    cap_set = []
    forbidden = set()
    for e in elements:
        if e in forbidden:
            continue
        for u in cap_set:
            c = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
            forbidden.add(c)
        cap_set.append(e)
        forbidden.add(e)
    return cap_set

best_cap = None
best_size = 0
best_desc = None

# Test many priorities at n=4
candidates = []

def add(name, fn):
    candidates.append((name, fn))

add("const", lambda e, n: 0.0)
add("c2=1", lambda e, n: -abs(sum(1 for x in e if x == 2) - 1))
add("c2=0", lambda e, n: -abs(sum(1 for x in e if x == 2) - 0))
add("c2=2", lambda e, n: -abs(sum(1 for x in e if x == 2) - 2))
add("c1=1", lambda e, n: -abs(sum(1 for x in e if x == 1) - 1))
add("c0*c1*c2", lambda e, n: float((sum(1 for x in e if x == 0)+1) * (sum(1 for x in e if x == 1)+1) * (sum(1 for x in e if x == 2)+1)))

# Quadratic form check: x_0*x_1 + x_2*x_3 mod 3
add("quad x0x1+x2x3", lambda e, n: -float((e[0]*e[1] + e[2]*e[3]) % 3))

# Pellegrino-like: x^2 + y^2 + z^2 + w^2 ≡ c mod 3
for c in range(3):
    add(f"sumsq=={c}", lambda e, n, c=c: -float((sum(x*x for x in e) - c) % 3 != 0))

# All possible (target, mod) combinations
add("c2=1, c1=2", lambda e, n: -abs(sum(1 for x in e if x == 2) - 1) * 10 - abs(sum(1 for x in e if x == 1) - 2))

# Random quadratic forms
np.random.seed(0)
for trial in range(30):
    A = np.random.randint(0, 3, (n, n))
    A = (A + A.T) % 3
    b = np.random.randint(0, 3, n)
    c = np.random.randint(0, 3)
    def fn(e, n, A=A, b=b, c=c):
        x = np.array(e)
        v = int((x @ A @ x + b @ x + c) % 3)
        return -float(v)
    add(f"randq{trial}", fn)

for name, fn in candidates:
    cap = cap_set_with(fn, n)
    sz = len(cap)
    if sz > best_size:
        best_size = sz
        best_cap = cap
        best_desc = name
        print(f"  NEW BEST: {sz} via {name}")

print(f"\nBest at n=4: {best_size} via {best_desc}")
if best_cap:
    print(f"  Cap (first 10): {best_cap[:10]}")
    # Save
    with open("autoresearch/archive/016-cap-n4.txt", "w") as f:
        f.write(f"# size = {best_size}\n# desc = {best_desc}\n")
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")
