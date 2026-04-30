"""Priority orders by 2-positions PATTERN first, then fill."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def get_pattern(e):
    return tuple(i for i, x in enumerate(e) if x == 2)

def p_c2_3_pattern_then_fill(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1_000_000
    # pattern index in lex order of 3-tuples
    pat = get_pattern(e)
    if len(pat) == 3:
        # encode pattern as a single integer
        pat_idx = pat[0] * 64 + pat[1] * 8 + pat[2]
    else:
        pat_idx = 0
    secondary = -pat_idx * 100
    # within pattern, lex of fill (the 5 non-2 coords)
    fill = tuple(x for x in e if x != 2)
    fill_idx = sum(b * 2**i for i, b in enumerate(fill))
    tertiary = -fill_idx
    return primary + secondary + tertiary

bench("c2=3, pattern-first lex", p_c2_3_pattern_then_fill, n)

def p_c2_3_fill_then_pattern(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1_000_000
    pat = get_pattern(e)
    if len(pat) == 3:
        pat_idx = pat[0] * 64 + pat[1] * 8 + pat[2]
    else:
        pat_idx = 0
    fill = tuple(x for x in e if x != 2)
    fill_idx = sum(b * 2**i for i, b in enumerate(fill))
    return primary - fill_idx * 100 - pat_idx

bench("c2=3, fill-first lex", p_c2_3_fill_then_pattern, n)

# Different pattern orderings: numerical reverse
def p_c2_3_pattern_revlex(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1_000_000
    pat = get_pattern(e)
    if len(pat) == 3:
        # reverse-lex
        pat_idx = (7 - pat[0]) * 64 + (7 - pat[1]) * 8 + (7 - pat[2])
    else:
        pat_idx = 0
    return primary - pat_idx

bench("c2=3, pattern revlex", p_c2_3_pattern_revlex, n)

# Pattern by SUM of positions
def p_c2_3_pattern_sum(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pat_sum = sum(i for i, x in enumerate(e) if x == 2)
    return primary - pat_sum

bench("c2=3, pattern sum ascending", p_c2_3_pattern_sum, n)

def p_c2_3_pattern_sum_desc(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pat_sum = sum(i for i, x in enumerate(e) if x == 2)
    return primary + pat_sum

bench("c2=3, pattern sum descending", p_c2_3_pattern_sum_desc, n)

# Pattern by min-position
def p_c2_3_pattern_minpos(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    min_pos = min(pos_2) if pos_2 else 0
    return primary - min_pos

bench("c2=3, pattern min-pos low", p_c2_3_pattern_minpos, n)

# Pattern by max-position
def p_c2_3_pattern_maxpos(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    max_pos = max(pos_2) if pos_2 else 0
    return primary - max_pos

bench("c2=3, pattern max-pos low", p_c2_3_pattern_maxpos, n)

# Pattern by spread
def p_c2_3_pattern_spread(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    if len(pos_2) >= 2:
        spread = max(pos_2) - min(pos_2)
    else:
        spread = 0
    return primary - spread

bench("c2=3, pattern small-spread first", p_c2_3_pattern_spread, n)

def p_c2_3_pattern_big_spread(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3) * 1000
    pos_2 = [i for i, x in enumerate(e) if x == 2]
    if len(pos_2) >= 2:
        spread = max(pos_2) - min(pos_2)
    else:
        spread = 0
    return primary + spread

bench("c2=3, pattern large-spread first", p_c2_3_pattern_big_spread, n)
