"""Deep search across many priority families."""
import sys, os, itertools, random, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
cap_set_size = m.cap_set_size

n = 8
budget = 240
t0 = time.time()
best = 448

# Family A: c2=3 + (linear_form mod 3) + (random subset of features)
print("--- A: c2=3 + linear forms ---")
np.random.seed(0)
for trial in range(500):
    if time.time() - t0 > budget * 0.3: break
    a = np.random.randint(0, 3, n)
    a_target = np.random.randint(0, 3)
    def p(e, n, a=a, t=a_target):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 1_000_000
        v = sum(a[i] * e[i] for i in range(n)) % 3
        return primary - abs(v - t) * 100
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        print(f"  trial {trial}: NEW BEST {sz}")

# Family B: weighted feature sums
print("--- B: weighted feature sums ---")
np.random.seed(1)
for trial in range(500):
    if time.time() - t0 > budget * 0.5: break
    w = np.random.uniform(-1, 1, 10)
    def p(e, n, w=w):
        c0 = e.count(0)
        c1 = e.count(1)
        c2 = e.count(2)
        s = w[0]*c0 + w[1]*c1 + w[2]*c2 + w[3]*(c2-3)**2 + w[4]*c0*c1 + w[5]*c1*c2 + w[6]*c0*c2
        s += w[7]*sum(e[i]*e[(i+1)%n] for i in range(n)) % 3
        s += w[8]*sum(1 for i in range(n) for j in range(i+1, n) if e[i]==e[j])
        s += w[9]*sum(e)
        return float(s)
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        print(f"  trial {trial}: NEW BEST {sz}")

# Family C: c2 and c1 joint
print("--- C: c2 and c1 joint targets ---")
for c2t in range(0, 9):
    for c1t in range(0, 9):
        if time.time() - t0 > budget * 0.7: break
        def p(e, n, c2t=c2t, c1t=c1t):
            c2 = e.count(2)
            c1 = e.count(1)
            return -abs(c2 - c2t) * 100 - abs(c1 - c1t) * 90
        sz = cap_set_size(p, n)
        if sz > best:
            best = sz
            print(f"  c2={c2t}, c1={c1t}: NEW BEST {sz}")

# Family D: more elaborate combinations
print("--- D: sin-cos / nonlinear-feature combinations ---")
np.random.seed(2)
import math
for trial in range(200):
    if time.time() - t0 > budget * 0.85: break
    seeds = np.random.uniform(-3, 3, 12)
    def p(e, n, s=seeds):
        c2 = e.count(2)
        c1 = e.count(1)
        c0 = e.count(0)
        v = (s[0]*math.sin(c2*s[1]) + s[2]*math.cos(c1*s[3]) +
             s[4]*c0 + s[5]*(c2 - 3)**2 + s[6]*c1*c2)
        return float(v)
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        print(f"  trial {trial}: NEW BEST {sz}")

# Family E: double-target
print("--- E: double-cluster priority ---")
clusters = [
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c2 == 3},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c2 in (2, 3)},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c2 in (3, 4)},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c2 in (1, 3, 5)},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c1 == c2},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if c0 == c2},
    {(c0, c1, c2) for c0 in range(9) for c1 in range(9-c0) for c2 in [9-c0-c1] if abs(c1-c2) <= 1},
]
for cs in clusters:
    def p(e, n, cs=cs):
        cs_e = (e.count(0), e.count(1), e.count(2))
        return float(cs_e in cs)
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        print(f"  cluster {cs}: NEW BEST {sz}")
    else:
        print(f"  cluster size {len(cs)}: {sz}")

print(f"\n=== Final best: {best} ===  [{time.time()-t0:.1f}s]")
