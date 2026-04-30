"""Combine c2-target with secondary features."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def base_c2(e, n):
    c2 = sum(1 for x in e if x == 2)
    return -abs(c2 - 3) * 1.0

def p_c2_then_lex(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    secondary = -sum(x * 3**i for i, x in enumerate(e))
    return primary + secondary

def p_c2_then_quad(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            s += e[i] * e[j]
    secondary = -float(s % 3)
    return primary + secondary

def p_c2_then_diag(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    s = sum(x * x for x in e) % 3
    secondary = -float(s)
    return primary + secondary

def p_c2_squared(e, n):
    c2 = sum(1 for x in e if x == 2)
    return -float((c2 - 3) ** 2)

def p_c2_floor_ceil(e, n):
    # both 2 and 3 are good
    c2 = sum(1 for x in e if x == 2)
    if c2 == 2 or c2 == 3:
        return 1.0
    return -abs(c2 - 2.5)

def p_c2_target_3_w_c1(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    secondary = -abs(c1 - 3) * 100
    return primary + secondary

def p_c2_target_3_w_c0(e, n):
    c0 = sum(1 for x in e if x == 0)
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    secondary = -abs(c0 - 3) * 100
    return primary + secondary

def p_pos_c2_pattern(e, n):
    # Where are the 2's? Prefer specific patterns of positions
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    secondary = sum(pos_2)  # later positions for 2's
    return primary + secondary

def p_pos_c2_pattern_neg(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    secondary = -sum(pos_2)  # earlier positions
    return primary + secondary

def p_count_balance_full(e, n):
    c0 = sum(1 for x in e if x == 0)
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    # all close to n/3
    return -float(abs(c0 - 3) + abs(c1 - 3) + abs(c2 - 2)) * 1.0

def p_quad_diag(e, n):
    s = sum(x * x for x in e) % 3
    return -float(s)

def p_c2_3_c1_3(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return -float(abs(c2 - 3) * 10 + abs(c1 - 3))

bench("base c2=3 (sanity)", base_c2, n)
bench("c2=3 + lex tiebreak", p_c2_then_lex, n)
bench("c2=3 + quad-off mod 3 tiebreak", p_c2_then_quad, n)
bench("c2=3 + quad-diag mod 3 tiebreak", p_c2_then_diag, n)
bench("(c2-3)^2", p_c2_squared, n)
bench("c2 in {2,3} flat", p_c2_floor_ceil, n)
bench("c2=3 + c1=3 tiebreak", p_c2_target_3_w_c1, n)
bench("c2=3 + c0=3 tiebreak", p_c2_target_3_w_c0, n)
bench("c2=3 + late 2's", p_pos_c2_pattern, n)
bench("c2=3 + early 2's", p_pos_c2_pattern_neg, n)
bench("count balance full", p_count_balance_full, n)
bench("c2=3 c1=3 weighted", p_c2_3_c1_3, n)
