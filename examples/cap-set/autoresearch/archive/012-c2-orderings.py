"""Different orderings over c2 values."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def make_c2_order(order):
    """order is a list of c2 values, earlier => higher priority."""
    rank = {v: -i for i, v in enumerate(order)}
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        return float(rank.get(c2, -1000))
    return p

# Try every permutation of {0..8} - 9! = 362880, too many.
# Just try interesting ones.
orders = [
    [3, 2, 4, 1, 5, 0, 6, 7, 8],  # near 3 ascending then descending
    [3, 4, 2, 5, 1, 6, 0, 7, 8],
    [3, 0, 2, 1, 4, 5, 6, 7, 8],  # c2=3 then {0,1} sets
    [3, 2, 1, 0, 4, 5, 6, 7, 8],
    [3, 2, 0, 1, 4, 5, 6, 7, 8],
    [3],  # only c2=3 (then by itertools)
    [2, 3, 4, 1, 5, 0, 6, 7, 8],  # c2=2 first
    [3, 4, 5, 2, 1, 0, 6, 7, 8],
    [2, 3, 1, 4, 0, 5, 6, 7, 8],
    [3, 2, 4],  # only those, rest at default
    [3, 4],
    [3, 2],
    [2, 3],
    [4, 3, 2, 5, 1, 6, 0, 7, 8],
    [4, 3, 5, 2, 6, 1, 7, 0, 8],
    [2, 3, 1],
]

for order in orders:
    sz = bench(f"order {order}", make_c2_order(order), n)

# Now: c2 priority + multiset bias
print("\n--- c2 with multiset priority ---")
# Within each c2 cluster, prefer certain (c0, c1) splits
def p_c2_3_balanced_multi(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 100
    # within cluster: prefer (c0, c1) close to balanced
    secondary = -abs(c0 - c1) * 0.1
    return primary + secondary

bench("c2=3 + |c0-c1| balance", p_c2_3_balanced_multi, n)

# Try priority that promotes c2=3 elements with specific 2-positions
def p_c2_3_pos_specific(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    # positions of 2's
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    # specific patterns - prefer 2's at non-adjacent positions
    secondary = 0
    if len(pos_2) >= 2:
        for i in range(len(pos_2) - 1):
            if pos_2[i+1] - pos_2[i] == 1:
                secondary -= 0.1
    return primary + secondary

bench("c2=3 + non-adjacent 2's", p_c2_3_pos_specific, n)

# Combine c2 cluster with c0-c1 balance subdued
def p_funny(e, n):
    c2 = sum(1 for x in e if x == 2)
    pos_2 = sum(i for i, x in enumerate(e) if x == 2)
    return -abs(c2 - 3) * 1000.0 + (pos_2 % 7) * 0.001

bench("c2=3 + pos_2 mod 7 tiny", p_funny, n)

# A two-stage greedy in priority: first c2=3, then c2=0
def p_c2_3_then_0(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 100.0
    if c2 == 0:
        return 50.0
    if c2 == 2:
        return 30.0
    return -float(abs(c2 - 3))

bench("c2 in [3, 0, 2, ...]", p_c2_3_then_0, n)

def p_c2_3_then_0_v2(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 100.0
    if c2 == 0:
        return 99.0
    if c2 == 2:
        return 50.0
    return -float(abs(c2 - 3))

bench("c2 [3>0>2]", p_c2_3_then_0_v2, n)

def p_c2_3_then_2_then_4(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 100.0
    if c2 == 2:
        return 99.0
    if c2 == 4:
        return 98.0
    return -float(abs(c2 - 3))

bench("c2 [3>2>4]", p_c2_3_then_2_then_4, n)

def p_c2_3_then_4_then_2(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 100.0
    if c2 == 4:
        return 99.0
    if c2 == 2:
        return 98.0
    return -float(abs(c2 - 3))

bench("c2 [3>4>2]", p_c2_3_then_4_then_2, n)
