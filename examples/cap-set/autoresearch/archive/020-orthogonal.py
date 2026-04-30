"""Orthogonal priority structures: try non-c2 dominant features."""
import sys, os, itertools, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Symmetric-difference based: priority based on relation to a fixed pattern
patterns = [
    (0,)*8,
    (1,)*8,
    (2,)*8,
    (0,1)*4,
    (0,2)*4,
    (1,2)*4,
    (0,1,2,0,1,2,0,1),
    (2,1,0,2,1,0,2,1),
    (0,0,1,1,2,2,0,1),
    (1,2,0,1,2,0,1,2),
]
for pat in patterns:
    # Hamming distance (number of mismatched coords)
    def p(e, n, pat=pat):
        return -float(sum(1 for a, b in zip(e, pat) if a != b))
    bench(f"hamming-dist to {pat}", p, n)

# Now negation: pick FAR from pattern
print("\n--- far from pattern ---")
for pat in patterns[:3]:
    def p(e, n, pat=pat):
        return float(sum(1 for a, b in zip(e, pat) if a != b))
    bench(f"hamming-dist FROM {pat} max", p, n)

# Quadratic distance in F_3
print("\n--- F_3-distance from pattern ---")
for pat in patterns[:5]:
    def p(e, n, pat=pat):
        d = sum(((a - b) % 3) ** 2 for a, b in zip(e, pat))
        return -float(d)
    bench(f"f3 dist (squared) from {pat}", p, n)

# Combined: c2=3 + hamming distance
print("\n--- c2=3 + hamming dist secondary ---")
for pat in patterns[:5]:
    def p(e, n, pat=pat):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 1000
        secondary = -float(sum(1 for a, b in zip(e, pat) if a != b))
        return primary + secondary
    bench(f"c2=3 + dist from {pat}", p, n)

# Bit-reverse-based ordering
print("\n--- bit-reverse priority ---")
def p_bitrev(e, n):
    # interpret e as base-3 number, reverse digits
    rev = 0
    for x in e:
        rev = rev * 3 + x
    return float(rev)

bench("base3 reverse number", p_bitrev, n)

def p_bitrev_neg(e, n):
    rev = 0
    for x in e:
        rev = rev * 3 + x
    return -float(rev)

bench("base3 forward number", p_bitrev_neg, n)

def p_bitrev_c2(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 100000
    rev = 0
    for x in reversed(e):
        rev = rev * 3 + x
    return primary + float(rev)

bench("c2=3 + reverse base3", p_bitrev_c2, n)

# Different scaling of c2-target
print("\n--- c2-target with varying primary scale ---")
def make_c2(primary_scale, secondary_fn):
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * primary_scale
        return primary + secondary_fn(e, n)
    return p

def s_lex(e, n):
    return -sum(x * 3**i for i, x in enumerate(e))

def s_revlex(e, n):
    return sum(x * 3**i for i, x in enumerate(e))

def s_aff(e, n):
    return -float((e[0] + e[1]) % 3)

for ps in [10, 100, 1000, 10000, 100000]:
    bench(f"c2=3 (scale {ps}) + lex", make_c2(ps, s_lex), n)
    bench(f"c2=3 (scale {ps}) + revlex", make_c2(ps, s_revlex), n)

# Now WITH a sub-priority that has wider range than the inter-cluster gap
print("\n--- c2=3 with SECONDARY large enough to interleave clusters ---")
def p_c2_3_then_pattern(e, n):
    # Within each cluster of c2=k, sort by pattern_idx
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 100
    # secondary based on positional structure
    secondary = -sum(i * (1 if e[i] == 2 else 0) for i in range(n))
    return primary + secondary

bench("c2=3 (small primary) + 2-pos sum", p_c2_3_then_pattern, n)
