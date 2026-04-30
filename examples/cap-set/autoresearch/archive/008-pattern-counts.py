"""Pattern-count priorities (triples, structural counts)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_triples_all_diff(e, n):
    # number of (i,j,k), i<j<k, with {e_i,e_j,e_k} = {0,1,2}
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if {e[i], e[j], e[k]} == {0, 1, 2}:
                    s += 1
    return float(s)

def p_triples_all_diff_neg(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if {e[i], e[j], e[k]} == {0, 1, 2}:
                    s += 1
    return -float(s)

def p_triples_all_eq(e, n):
    # number of (i,j,k) with e_i=e_j=e_k
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if e[i] == e[j] == e[k]:
                    s += 1
    return float(s)

def p_triples_all_eq_neg(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if e[i] == e[j] == e[k]:
                    s += 1
    return -float(s)

def p_triples_zero_sum(e, n):
    # already from earlier; here mid-range as comparison
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if (e[i] + e[j] + e[k]) % 3 == 0:
                    s += 1
    return -float(s)

def p_combo_c2_triples_diff_pos(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if {e[i], e[j], e[k]} == {0, 1, 2}:
                    s += 1
    return primary + float(s)

def p_combo_c2_triples_diff_neg(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if {e[i], e[j], e[k]} == {0, 1, 2}:
                    s += 1
    return primary - float(s)

def p_combo_c2_triples_eq_neg(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if e[i] == e[j] == e[k]:
                    s += 1
    return primary - float(s)

def p_combo_c2_triples_eq_pos(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if e[i] == e[j] == e[k]:
                    s += 1
    return primary + float(s)

def p_combo_c2_triples_zero_neg(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if (e[i] + e[j] + e[k]) % 3 == 0:
                    s += 1
    return primary - float(s)

bench("triples_all_diff +", p_triples_all_diff, n)
bench("triples_all_diff -", p_triples_all_diff_neg, n)
bench("triples_all_eq +", p_triples_all_eq, n)
bench("triples_all_eq -", p_triples_all_eq_neg, n)
bench("triples_zero_sum -", p_triples_zero_sum, n)
bench("c2=3 + triples_diff +", p_combo_c2_triples_diff_pos, n)
bench("c2=3 + triples_diff -", p_combo_c2_triples_diff_neg, n)
bench("c2=3 + triples_eq -", p_combo_c2_triples_eq_neg, n)
bench("c2=3 + triples_eq +", p_combo_c2_triples_eq_pos, n)
bench("c2=3 + triples_zero -", p_combo_c2_triples_zero_neg, n)

# 4-tuples
def p_4tuples_all_diff(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    if {e[i], e[j], e[k], e[l]} == {0, 1, 2}:
                        s += 1
    return float(s)

bench("4tuples covering all diff +", p_4tuples_all_diff, n)

# Check: what if we score by total number of "valid" partitions
def p_partition_score(e, n):
    # Count nonzero entries split between values 1 and 2 ideally
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -abs(c1 - c2)

bench("|c1 - c2| balance", p_partition_score, n)

def p_c2_3_c1_c2_diff(e, n):
    c2 = sum(1 for x in e if x == 2)
    c1 = sum(1 for x in e if x == 1)
    primary = -abs(c2 - 3) * 1000
    secondary = -abs(c1 - c2)
    return primary + secondary

bench("c2=3 + |c1-c2| balance", p_c2_3_c1_c2_diff, n)

# Many variations of c2 target with flat plateau
def p_c2_in_set(e, n):
    c2 = sum(1 for x in e if x == 2)
    if c2 in (2, 3, 4):
        return 1.0
    return -float(abs(c2 - 3))

bench("c2 in {2,3,4} flat", p_c2_in_set, n)

# Permutation-invariant: only multiset counts
def p_multiset_pmf(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    # gaussian-like centered at (3,3,2) / (3,2,3) / (2,3,3)
    centers = [(3,3,2), (3,2,3), (2,3,3)]
    return max(-((c0-c0t)**2 + (c1-c1t)**2 + (c2-c2t)**2) for c0t,c1t,c2t in centers)

bench("multiset pmf at balanced", p_multiset_pmf, n)
