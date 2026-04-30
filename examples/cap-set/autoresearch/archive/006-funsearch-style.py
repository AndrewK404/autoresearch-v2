"""FunSearch-style priorities: products and compound features."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_product_counts(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float((c0 + 1) * (c1 + 1) * (c2 + 1))

def p_product_counts_neg(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -float((c0 + 1) * (c1 + 1) * (c2 + 1))

def p_funsearch_v1(e, n):
    el = list(e)
    o = el.count(0)
    m = el.count(1)
    d = el.count(2)
    score = (o + 1) * (m + 1) * (d + 1)
    for i in range(n):
        for j in range(i + 1, n):
            score += abs(el[i] - el[j]) * (i + 1) * (j + 1)
    return float(score)

def p_funsearch_v2(e, n):
    el = list(e)
    o = el.count(0)
    m = el.count(1)
    d = el.count(2)
    score = (o + 1) * (m + 1) * (d + 1)
    for i in range(n):
        for j in range(i + 1, n):
            score -= abs(el[i] - el[j]) * (i + 1) * (j + 1)
    return float(score)

def p_funsearch_v3(e, n):
    el = list(e)
    score = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            score += abs(el[i] - el[j])
    return score

def p_funsearch_v4(e, n):
    # primary balanced, secondary pairwise diff
    el = list(e)
    o = el.count(0)
    m = el.count(1)
    d = el.count(2)
    primary = (o + 1) * (m + 1) * (d + 1)
    secondary = 0
    for i in range(n):
        for j in range(i + 1, n):
            if el[i] == el[j]:
                secondary += 1
    return float(primary * 1000 + secondary)

def p_funsearch_v5(e, n):
    el = list(e)
    o = el.count(0)
    m = el.count(1)
    d = el.count(2)
    primary = (o + 1) * (m + 1) * (d + 1)
    secondary = 0
    for i in range(n):
        for j in range(i + 1, n):
            if el[i] == el[j]:
                secondary += 1
    return float(primary * 1000 - secondary)

def p_pair_diff_pos(e, n):
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += abs(e[i] - e[j])
    return float(s)

def p_pair_diff_neg(e, n):
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += abs(e[i] - e[j])
    return -float(s)

def p_pair_diff_pos_idx(e, n):
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += abs(e[i] - e[j]) * (i + 1) * (j + 1)
    return float(s)

def p_pair_diff_neg_idx(e, n):
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += abs(e[i] - e[j]) * (i + 1) * (j + 1)
    return -float(s)

# A smaller variant: prefer balanced AND pairwise diverse
def p_balanced_diverse(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    diff = sum(abs(e[i] - e[j]) for i in range(n) for j in range(i+1, n))
    return float(c0 * c1 * c2 + diff)

# Try more aggressive c2-target with finer continuous priority
def p_c2_pmf_tight(e, n):
    c2 = sum(1 for x in e if x == 2)
    # boltzmann-like, peaked at 3
    return -((c2 - 3) ** 2) * 1.0

def p_c2_3_or_4(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 == 3:
        return 1.0
    elif c2 == 4:
        return 0.5
    elif c2 == 2:
        return 0.5
    return -10.0

# Now try different counts of values
def p_full_balanced(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float(c0 * c1 * c2)

def p_full_balanced_2(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float((c0+1) * (c1+1) * (c2+1))

bench("product (c0+1)(c1+1)(c2+1)", p_product_counts, n)
bench("-product", p_product_counts_neg, n)
bench("funsearch v1 (product + pairs)", p_funsearch_v1, n)
bench("funsearch v2 (product - pairs)", p_funsearch_v2, n)
bench("pair_abs_diff (sum)", p_funsearch_v3, n)
bench("funsearch v4 (primary + pair_eq)", p_funsearch_v4, n)
bench("funsearch v5 (primary - pair_eq)", p_funsearch_v5, n)
bench("pair_abs_diff +", p_pair_diff_pos, n)
bench("pair_abs_diff -", p_pair_diff_neg, n)
bench("pair_abs_diff_idx +", p_pair_diff_pos_idx, n)
bench("pair_abs_diff_idx -", p_pair_diff_neg_idx, n)
bench("balanced + diverse", p_balanced_diverse, n)
bench("c2_pmf_tight", p_c2_pmf_tight, n)
bench("c2 in {2,3,4} graded", p_c2_3_or_4, n)
bench("c0*c1*c2", p_full_balanced, n)
bench("(c0+1)(c1+1)(c2+1)", p_full_balanced_2, n)
