"""Richer feature combinations."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_pair_eq_count(e, n):
    # pairs i<j with e_i == e_j
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] == e[j]:
                s += 1
    return -float(s)

def p_pair_eq_count_pos(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] == e[j]:
                s += 1
    return float(s)

def p_pair_zero_sum(e, n):
    # pairs i<j with e_i + e_j ≡ 0 mod 3
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if (e[i] + e[j]) % 3 == 0:
                s += 1
    return float(s)

def p_pair_zero_sum_neg(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if (e[i] + e[j]) % 3 == 0:
                s += 1
    return -float(s)

def p_triples_zero(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if (e[i] + e[j] + e[k]) % 3 == 0:
                    s += 1
    return -float(s)

def p_triples_zero_pos(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if (e[i] + e[j] + e[k]) % 3 == 0:
                    s += 1
    return float(s)

def p_c2_3_pair_eq(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] == e[j]:
                s += 1
    return primary - float(s)

def p_c2_3_pair_eq_plus(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] == e[j]:
                s += 1
    return primary + float(s)

def p_c2_3_pair_zero(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if (e[i] + e[j]) % 3 == 0:
                s += 1
    return primary - float(s)

def p_c2_3_triples_zero(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                if (e[i] + e[j] + e[k]) % 3 == 0:
                    s += 1
    return primary - float(s)

def p_pair_diff(e, n):
    # count pairs where e_i != e_j
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            if e[i] != e[j]:
                s += 1
    return float(s)

def p_norm_l2(e, n):
    return -float(sum(x*x for x in e))

def p_dot_alpha(e, n):
    # x dot (1,2,1,2,...) mod 3
    s = sum(e[i] * (1 + (i % 2)) for i in range(n)) % 3
    return -float(s)

def p_quad_form_circulant(e, n):
    # x_i * x_{i+1}
    s = sum(e[i] * e[(i+1) % n] for i in range(n))
    return -float(s % 3)

def p_quad_form_pair_idx(e, n):
    # weighted quadratic form
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            s += (i + j) * e[i] * e[j]
    return -float(s % 3)

def p_count_2_pair(e, n):
    # number of pairs (i,j) i<j s.t. e_i=2 and e_j=2
    s = 0
    for i in range(n):
        if e[i] == 2:
            for j in range(i+1, n):
                if e[j] == 2:
                    s += 1
    return -float(s)

def p_c2_3_pair_2(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    # secondary: distribute the 2's
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    if len(pos_2) >= 2:
        gaps = [pos_2[i+1]-pos_2[i] for i in range(len(pos_2)-1)]
        secondary = -float(sum(g*g for g in gaps))
    else:
        secondary = 0.0
    return primary + secondary

bench("pair_eq -", p_pair_eq_count, n)
bench("pair_eq +", p_pair_eq_count_pos, n)
bench("pair_zero_sum +", p_pair_zero_sum, n)
bench("pair_zero_sum -", p_pair_zero_sum_neg, n)
bench("triples_zero -", p_triples_zero, n)
bench("triples_zero +", p_triples_zero_pos, n)
bench("c2=3 + pair_eq -", p_c2_3_pair_eq, n)
bench("c2=3 + pair_eq +", p_c2_3_pair_eq_plus, n)
bench("c2=3 + pair_zero -", p_c2_3_pair_zero, n)
bench("c2=3 + triples_zero -", p_c2_3_triples_zero, n)
bench("pair_diff", p_pair_diff, n)
bench("-norm_l2", p_norm_l2, n)
bench("dot alpha", p_dot_alpha, n)
bench("quad_form_circulant", p_quad_form_circulant, n)
bench("quad_form_pair_idx", p_quad_form_pair_idx, n)
bench("count_2_pair -", p_count_2_pair, n)
bench("c2=3 + spread 2's", p_c2_3_pair_2, n)
