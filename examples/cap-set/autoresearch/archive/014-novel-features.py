"""Novel feature explorations."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Permutation-symmetric in groups of coords
def p_pair_grouped(e, n):
    # group coords into 4 pairs
    pairs = [(e[0], e[1]), (e[2], e[3]), (e[4], e[5]), (e[6], e[7])]
    # count how many pairs are (1,2) or (2,1)
    s = sum(1 for p in pairs if (p == (1, 2) or p == (2, 1)))
    return float(s)

def p_triplets_grouped(e, n):
    return 0.0

def p_pair_count_per_value(e, n):
    # count of pairs that are (a,b) for various (a,b)
    pairs = [(e[i], e[j]) for i in range(n) for j in range(i+1, n)]
    return float(sum(1 for p in pairs if p in [(1,2), (2,1), (0,2), (2,0)]))

def p_count_balanced_pairs(e, n):
    # count pairs (i,j) with e_i + e_j = 1 mod 3 (most "balanced")
    s = sum(1 for i in range(n) for j in range(i+1, n) if (e[i] + e[j]) % 3 == 1)
    return float(s)

def p_count_pair_sum_1(e, n):
    s = sum(1 for i in range(n) for j in range(i+1, n) if (e[i] + e[j]) % 3 == 1)
    return float(s)

def p_count_pair_sum_2(e, n):
    s = sum(1 for i in range(n) for j in range(i+1, n) if (e[i] + e[j]) % 3 == 2)
    return float(s)

bench("count pairs (1,2) or (2,1) or (0,2) or (2,0)", p_pair_count_per_value, n)
bench("count pairs e_i+e_j ≡ 1 mod 3", p_count_pair_sum_1, n)
bench("count pairs e_i+e_j ≡ 2 mod 3", p_count_pair_sum_2, n)

# Try priority that encourages "diversity":
def p_distinct_values(e, n):
    return float(len(set(e)))  # 1, 2, or 3

bench("distinct values", p_distinct_values, n)

def p_distinct_neg(e, n):
    return -float(len(set(e)))

bench("distinct values neg", p_distinct_neg, n)

# Linear weight
def p_pos_weighted_2(e, n):
    return -float(sum(i for i, x in enumerate(e) if x == 2))

bench("sum of 2-positions ascending", p_pos_weighted_2, n)

def p_pos_weighted_2_desc(e, n):
    return float(sum(i for i, x in enumerate(e) if x == 2))

bench("sum of 2-positions descending", p_pos_weighted_2_desc, n)

# Positional index of 2's modular
def p_modpos_2(e, n):
    s = sum(i for i, x in enumerate(e) if x == 2) % 3
    return -float(s)

bench("sum of 2-positions mod 3 == 0", p_modpos_2, n)

# Number of 2's at even positions
def p_even_2(e, n):
    s = sum(1 for i in range(0, n, 2) if e[i] == 2)
    return -abs(s - 1) * 1.0

bench("2's at even pos == 1", p_even_2, n)

# Combined c2-target with separate even/odd
def p_c2_3_even_2(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    even_2 = sum(1 for i in range(0, n, 2) if e[i] == 2)
    return primary - abs(even_2 - 1) * 1.0

bench("c2=3 + even-2's-count==1", p_c2_3_even_2, n)

# Custom: based on a specific code structure (Hamming-like)
def p_hamming_code(e, n):
    # Imagine a [8,4] linear code, prefer codewords mod 3
    # Use generator matrix [I_4 | M] where M is fixed
    M = np.array([[1,1,1,0],
                  [1,1,0,1],
                  [1,0,1,1],
                  [0,1,1,1]])
    x = np.array(e[:4])
    expected_parity = (x @ M) % 3
    actual_parity = np.array(e[4:]) % 3
    diff = sum(int(a != b) for a, b in zip(expected_parity, actual_parity))
    return -float(diff)

bench("Hamming-code parity check", p_hamming_code, n)

# Reed-Muller / RM(1,3) like code
def p_rm_like(e, n):
    # parity coords 4..7 = e_0+e_1, e_0+e_2, e_0+e_3, e_1+e_2 mod 3
    pairs = [(e[0]+e[1])%3, (e[0]+e[2])%3, (e[0]+e[3])%3, (e[1]+e[2])%3]
    actual = [e[4], e[5], e[6], e[7]]
    diff = sum(1 for a, b in zip(pairs, actual) if a != b)
    return -float(diff)

bench("RM-like code parity", p_rm_like, n)

# Many random linear codes
np.random.seed(7)
best = 448
for trial in range(20):
    M = np.random.randint(0, 3, (4, 4))
    def p(e, n, M=M):
        x = np.array(e[:4])
        expected = (x @ M) % 3
        actual = np.array(e[4:]) % 3
        return -float(np.sum(expected != actual))
    sz = bench(f"random [8,4] code {trial}", p, n)
    if sz > best:
        best = sz
        print(f"  >>> NEW BEST: {sz}")

# Random with c2=3 primary
print("\n--- c2=3 + random codes ---")
np.random.seed(13)
for trial in range(20):
    M = np.random.randint(0, 3, (4, 4))
    def p(e, n, M=M):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 1000
        x = np.array(e[:4])
        expected = (x @ M) % 3
        actual = np.array(e[4:]) % 3
        secondary = -float(np.sum(expected != actual))
        return primary + secondary
    sz = bench(f"c2=3 + rand code {trial}", p, n)
    if sz > best:
        best = sz
        print(f"  >>> NEW BEST: {sz}")
