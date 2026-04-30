"""Try priorities with c1<->c2 symmetry and other relabeling-based priorities."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_max_c12(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -abs(max(c1, c2) - 3)

bench("max(c1,c2)=3", p_max_c12, n)

def p_min_c12(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -abs(min(c1, c2) - 3)

bench("min(c1,c2)=3", p_min_c12, n)

def p_sum_c12(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -abs((c1 + c2) - 6)

bench("c1+c2=6 (i.e. c0=2)", p_sum_c12, n)

def p_or_c12(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -min(abs(c1 - 3), abs(c2 - 3))

bench("either c1=3 or c2=3", p_or_c12, n)

def p_and_c12(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -max(abs(c1 - 3), abs(c2 - 3))

bench("both c1=3 and c2=3", p_and_c12, n)

# How does the cap size change with primary feature being multiset
print("\n--- multiset class priorities ---")
def p_c2_in_3_or_5(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 2.0
    if c2 == 5:
        return 1.0
    return -1.0

bench("c2 in {3, 5}", p_c2_in_3_or_5, n)

def p_c2_3_or_c1_3(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 2.0
    if c1 == 3:
        return 1.0
    return -1.0

bench("c2=3 first, then c1=3", p_c2_3_or_c1_3, n)

def p_min_c0_c1_c2(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float(min(c0, c1, c2))

bench("min count maximized", p_min_c0_c1_c2, n)

# Also try ELEMENT-WISE features
def p_count_zeros_pairs(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] == 0 and e[j] == 0:
                s += 1
    return -float(s)

bench("count (0,0) pairs", p_count_zeros_pairs, n)

# Boolean features in modular arith
def p_quadres(e, n):
    # x is QR mod 3 iff x ∈ {0, 1}
    qr = sum(1 for x in e if x in (0, 1))
    return float(qr)  # high for {0,1}

bench("count of {0,1}", p_quadres, n)

def p_anti_qr(e, n):
    qr = sum(1 for x in e if x in (0, 1))
    return -float(qr)

bench("count of {2}", p_anti_qr, n)

# Mod 3 sum feature
def p_modsum(e, n):
    s = sum(e) % 3
    if s == 0:
        return 1.0
    return -1.0

bench("sum mod 3 == 0", p_modsum, n)

# Number of indices where e_i ≡ a mod 3 for a fixed a (already covered by counts)

# Coordinate-pair fingerprint
def p_unique_pairs(e, n):
    pair_counts = {}
    for i in range(n):
        for j in range(i+1, n):
            pair = (e[i], e[j])
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
    # diversity score
    return float(len(pair_counts))

bench("distinct (e_i, e_j) pairs", p_unique_pairs, n)

# Trying to engineer for 512 directly
# What if priority uses a hash that mimics a known good ordering?
def p_sphericalish(e, n):
    # sum of squared values mod 3, weighted by (i+1)^2
    weights = [(i+1)**2 for i in range(n)]
    s = sum(w * (x*x) for w, x in zip(weights, e))
    return -float(s % 3)

bench("weighted sumsq mod 3", p_sphericalish, n)

# Now try priority as a continuous deformation of c2-target
def p_c2_continuous(e, n):
    c2 = sum(1 for x in e if x == 2)
    return -((c2 - 8/3.0) ** 2) - 0.5 * abs(c2 - 8/3.0)

bench("continuous c2 deformation", p_c2_continuous, n)

# Try priority based on the AP-structure with another fixed point
def p_proximity(e, n):
    # 2 - element in F_3
    e_neg = tuple((3 - x) % 3 for x in e)
    return -float(sum(1 for a, b in zip(e, e_neg) if a == b))

bench("self-symmetric distance", p_proximity, n)

# Try priority that is structured by 4+4 split
def p_44split(e, n):
    a = e[:4]
    b = e[4:]
    c2_a = sum(1 for x in a if x == 2)
    c2_b = sum(1 for x in b if x == 2)
    return -abs(c2_a - 1) * 10 - abs(c2_b - 1)

bench("4+4 split with c2=1 each", p_44split, n)

def p_44split_2(e, n):
    a = e[:4]
    b = e[4:]
    c2_a = sum(1 for x in a if x == 2)
    c2_b = sum(1 for x in b if x == 2)
    return -abs(c2_a - 2) * 10 - abs(c2_b - 1)

bench("4+4 split with c2=2,c2=1", p_44split_2, n)

# Try totally different: "inverse" priority
def p_inverse(e, n):
    # rank elements by: # of 0's minus # of 2's
    c0 = sum(1 for x in e if x == 0)
    c2 = sum(1 for x in e if x == 2)
    return float(c0 - c2)

bench("c0 - c2", p_inverse, n)

# Try priority with multi-tier
def p_multitier(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        c1 = sum(1 for x in e if x == 1)
        return 100.0 - abs(c1 - 3)  # within c2=3, prefer c1=3
    return -float(abs(c2 - 3))

bench("c2=3 with c1=3 inner", p_multitier, n)

# Try priority that combines c2-target with specific multiset preference
def p_target_multiset(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    # encourage symmetric: (3,3,2) or (3,2,3) or (2,3,3)
    valid = (c0, c1, c2) in [(3,3,2), (3,2,3), (2,3,3), (4,2,2), (2,4,2), (2,2,4)]
    return float(valid)

bench("balanced symmetric multisets", p_target_multiset, n)
