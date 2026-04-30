"""More desperate attempts to break 448."""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
cap_set_size = m.cap_set_size
bench = m.bench

n = 8

# Specific structured priorities
def p_sym_balanced(el, n):
    # Encourage all 3 counts non-zero
    c0, c1, c2 = el.count(0), el.count(1), el.count(2)
    if c0 > 0 and c1 > 0 and c2 > 0:
        return float(min(c0, c1, c2)) * 100 - max(abs(c0 - c1), abs(c1 - c2), abs(c0 - c2))
    return -1e6

bench("sym balanced (min count high)", p_sym_balanced, n)

def p_combo1(el, n):
    c2 = sum(1 for x in el if x == 2)
    c1 = sum(1 for x in el if x == 1)
    pair_diffs = sum(abs(el[i] - el[j]) for i in range(n) for j in range(i+1, n))
    return -abs(c2 - 3) * 1000 + pair_diffs * 0.001

bench("c2=3 + tiny pair_diffs", p_combo1, n)

def p_combo2(el, n):
    c2 = sum(1 for x in el if x == 2)
    if c2 != 3:
        return -1e6 - abs(c2 - 3)
    # within c2=3: prefer "isotropic" — same number in early/late halves
    e_first = sum(1 for x in el[:4] if x == 2)
    e_last = sum(1 for x in el[4:] if x == 2)
    return -abs(e_first - e_last) * 0.001

bench("c2=3 + balanced halves", p_combo2, n)

# What if we don't use the c2 feature but a PROJECTION
def p_proj_quad(el, n):
    # x = e[:4], y = e[4:]
    # priority based on a quadratic interaction
    x = el[:4]
    y = el[4:]
    s = 0
    for i in range(4):
        s += x[i] * y[i]
    return -float(s % 3)

bench("dot product first half · second half mod 3", p_proj_quad, n)

# Nested c2
def p_nested(el, n):
    # FIRST: c2 of first half = 1
    # SECOND: c2 of second half = 2
    # combined
    c2a = sum(1 for x in el[:4] if x == 2)
    c2b = sum(1 for x in el[4:] if x == 2)
    return -abs(c2a - 1) * 100 - abs(c2b - 2)

bench("split: c2 first=1, c2 second=2", p_nested, n)

def p_nested2(el, n):
    c2a = sum(1 for x in el[:4] if x == 2)
    c2b = sum(1 for x in el[4:] if x == 2)
    return -abs(c2a + c2b - 3) * 100

bench("c2 sum (= total c2) target 3", p_nested2, n)

# Try: priority = -((c0-c0t)^2 + ...) over many (c0t, c1t, c2t) targets
print("\n--- soft targets exhaustive ---")
best = 448
for c0t in range(1, 7):
    for c1t in range(1, 7):
        for c2t in range(1, 7):
            if c0t + c1t + c2t == 8:
                def p(e, n, t=(c0t, c1t, c2t)):
                    c0 = e.count(0)
                    c1 = e.count(1)
                    c2 = e.count(2)
                    return -((c0-t[0])**2 + (c1-t[1])**2 + (c2-t[2])**2)
                sz = cap_set_size(p, n)
                if sz > best:
                    print(f"  NEW BEST {sz}: target ({c0t},{c1t},{c2t})")
                    best = sz

# Try MIXED targets: union of multiple multisets
print("\n--- union of multiple targets ---")
multisets_ranked = [
    ((3,2,3), (2,3,3)),
    ((3,2,3), (2,3,3), (3,3,2)),
    ((3,2,3), (2,3,3), (4,1,3), (1,4,3)),
    ((3,2,3), (2,3,3), (4,2,2), (2,4,2)),
]
for s in multisets_ranked:
    def p(e, n, s=s):
        cs = (e.count(0), e.count(1), e.count(2))
        if cs in s:
            return 1.0
        return 0.0
    sz = cap_set_size(p, n)
    print(f"  union of {s}: {sz}")

# What if priority is computed via a more elaborate function
print("\n--- random matrix forms ---")
np.random.seed(99)
for trial in range(50):
    M = np.random.randint(0, 3, (n, n))
    M = (M + M.T) % 3
    v = np.random.randint(0, 3, n)
    def p(e, n, M=M, v=v):
        x = np.array(e)
        return -float((x @ M @ x + v @ x) % 3)
    sz = cap_set_size(p, n)
    if sz > 448:
        print(f"  trial {trial}: NEW BEST {sz}!!")
        best = sz

# Very different: priority = number of triples (i,j,k) with (e_i, e_j, e_k) ≠ (a, a, a)
print("\n--- count triples that are not constant ---")
def p_nonconst(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if e[i] == e[j] == e[k]:
                    s += 1
    return -float(s)

bench("count constant triples (low)", p_nonconst, n)

# Try priority = count of (e_i + e_j == 2) pairs... a triple "blocks" pattern
def p_block_triples(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] + e[j] == 4:  # both 2's? sums to 4 in integers, but mod 3 = 1
                s += 1
    return -float(s)

bench("count both-2 pairs (low)", p_block_triples, n)
