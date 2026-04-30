"""Initial sweep of priority function families."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_const(e, n):
    return 0.0

def p_few2(e, n):
    return -float(sum(1 for x in e if x == 2))

def p_lex_rev(e, n):
    return -sum(x * 3**i for i, x in enumerate(e))

def p_more_zeros(e, n):
    return float(sum(1 for x in e if x == 0))

def p_balanced(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    target = n / 3
    return -((c0 - target) ** 2 + (c1 - target) ** 2 + (c2 - target) ** 2)

def p_hamming(e, n):
    # number of nonzeros (lower better)
    return -float(sum(1 for x in e if x != 0))

def p_quadratic_diag(e, n):
    # x^T x mod 3, then promote 0 (kernel)
    s = sum(x * x for x in e) % 3
    return -float(s)

def p_quadratic_off(e, n):
    # promote elements where sum_{i<j} e_i e_j mod 3 is 0
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += e[i] * e[j]
    return -float(s % 3)

def p_linear(e, n):
    # promote elements where sum(e) mod 3 == 0
    s = sum(e) % 3
    return -float(s)

def p_pair_count(e, n):
    # count of pairs (i,j) with i<j such that e_i = e_j
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            if e[i] == e[j]:
                s += 1
    return float(s)

def p_zero_pairs(e, n):
    # count of pairs (i,j) where e_i + e_j ≡ 0 (mod 3)
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (e[i] + e[j]) % 3 == 0:
                s += 1
    return float(s)

def p_count_2_balanced(e, n):
    # prefer more 2s with diminishing returns
    c2 = sum(1 for x in e if x == 2)
    return -abs(c2 - n // 3) * 1.0

def p_weighted_lex(e, n):
    # weighted by coord, with explicit 2-penalty
    s = 0.0
    for i, x in enumerate(e):
        if x == 0:
            s += 0
        elif x == 1:
            s += 1
        else:
            s += 100  # heavy penalty
    return -s

def p_inv_count(e, n):
    # priority by number of 1's (more 1s first)
    return float(sum(1 for x in e if x == 1))

def p_count_pattern_dist(e, n):
    # distance from all-zeros vector
    return -float(sum(1 for x in e if x != 0))

bench("p_const", p_const, n)
bench("p_few2", p_few2, n)
bench("p_lex_rev", p_lex_rev, n)
bench("p_more_zeros", p_more_zeros, n)
bench("p_balanced (counts ~ n/3)", p_balanced, n)
bench("p_hamming (low weight first)", p_hamming, n)
bench("p_quadratic_diag (kernel of x^Tx)", p_quadratic_diag, n)
bench("p_quadratic_off (kernel of off-diag)", p_quadratic_off, n)
bench("p_linear (sum=0 first)", p_linear, n)
bench("p_pair_count (more matching pairs)", p_pair_count, n)
bench("p_zero_pairs (more 0-sum pairs)", p_zero_pairs, n)
bench("p_count_2_balanced", p_count_2_balanced, n)
bench("p_weighted_lex", p_weighted_lex, n)
bench("p_inv_count (more 1s first)", p_inv_count, n)
