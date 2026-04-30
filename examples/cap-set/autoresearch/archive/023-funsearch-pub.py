"""More aggressive variants inspired by FunSearch's structure."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Many index-weighted feature combinations
def p_v1(el, n):
    score = 0.
    for i in range(n):
        if el[i] != 0:
            score += i + el[i] * (n - i)
        for j in range(i + 1, n):
            if el[i] == el[j] and el[i] != 0:
                score += i + j + el[i] * el[j]
            else:
                score -= max(el[i], el[j]) * (i + j)
    return score

def p_v2(el, n):
    score = 0.
    for i in range(n):
        for j in range(i + 1, n):
            if el[i] == el[j]:
                score += (el[i] + 1) * (i + j + 2)
            else:
                score -= abs(el[i] - el[j]) * (i + j + 2)
    return score

def p_v3(el, n):
    score = 0.
    for i in range(n):
        for j in range(i + 1, n):
            score += el[i] * el[j] * (i + 1) * (j + 1)
    return -score % 23.0

def p_v4(el, n):
    n2 = el.count(2)
    score = -abs(n2 - 3) * 100.
    for i in range(n):
        for j in range(i + 1, n):
            if el[i] == 2 and el[j] == 2:
                score -= (i + j) * 0.01
    return score

def p_v5(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # within c2=3, prefer specific 2-position patterns
    pos2 = tuple(i for i, x in enumerate(el) if x == 2)
    if len(pos2) == 3:
        # encourage spread out 2's
        spread = pos2[2] - pos2[0]
        return primary - spread
    return primary

def p_v6(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # use position weighted sum mod 7
    h = sum(el[i] * (i + 1) for i in range(n)) % 7
    return primary - h

def p_v7(el, n):
    # Inspired by lattice point distance to a non-trivial center
    center = (1, 0, 1, 0, 1, 0, 1, 0)
    return -float(sum((el[i] - center[i])**2 for i in range(n)))

def p_v8(el, n):
    # Nonlinear combination
    n0 = el.count(0)
    n1 = el.count(1)
    n2 = el.count(2)
    # Asymmetric reward
    if n0 + n2 == 5 and n1 == 3 and n2 == 3:
        return 100.
    return float((n0 + 1) * (n1 + 1) * (n2 + 1))

def p_v9(el, n):
    # specific multiset list
    cs = (el.count(0), el.count(1), el.count(2))
    target_set = {(2, 3, 3), (3, 2, 3)}
    if cs in target_set:
        return 100.
    return -float(abs(cs[2] - 3))

def p_v10(el, n):
    # primary by c2 distance, secondary stratified by specific permutation invariant
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1000
    # parity of sum of 1-positions
    pos1_parity = sum(i for i, x in enumerate(el) if x == 1) % 2
    return primary + pos1_parity * 0.5

def p_v11(el, n):
    n2 = el.count(2)
    n1 = el.count(1)
    primary = -abs(n2 - 3) * 1e9
    # secondary: ensure 1 and 2 positions are interlaced
    pos1 = sorted(i for i, x in enumerate(el) if x == 1)
    pos2 = sorted(i for i, x in enumerate(el) if x == 2)
    if not pos1 or not pos2:
        secondary = 0
    else:
        # distance from interlaced
        all_pos = sorted([(p, 1) for p in pos1] + [(p, 2) for p in pos2])
        # count sign changes
        signs = [v for _, v in all_pos]
        flips = sum(1 for i in range(1, len(signs)) if signs[i] != signs[i-1])
        secondary = flips
    return primary + secondary

def p_v12(el, n):
    # Pure positional encoding
    val = 0
    for i, x in enumerate(el):
        val += x * (i + 1)
    return -float(val % 7)

def p_v13(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # secondary: number of (e_i = 0, e_j = 1) inversions (i<j)
    s = 0
    for i in range(n):
        if el[i] == 0:
            for j in range(i+1, n):
                if el[j] == 1:
                    s += 1
    return primary + s

def p_v14(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # secondary: alternating sum of positions of 2's
    pos = sorted(i for i, x in enumerate(el) if x == 2)
    if not pos:
        return primary
    alt = sum((-1)**i * p for i, p in enumerate(pos))
    return primary + alt

def p_v15(el, n):
    # priority based on number of identical adjacent pairs
    s = 0
    for i in range(n - 1):
        if el[i] == el[i+1]:
            s += 1
    return -float(s)

def p_v16(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # secondary: -count of identical adjacent pairs
    s = 0
    for i in range(n - 1):
        if el[i] == el[i+1]:
            s += 1
    return primary - s

def p_v17(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # secondary: sum(el[i]*el[(i+1)%n])
    s = sum(el[i] * el[(i+1) % n] for i in range(n))
    return primary - s

def p_v18(el, n):
    n2 = el.count(2)
    primary = -abs(n2 - 3) * 1e6
    # secondary: sum(el[i]*(i+1)*el[(i+1)%n])
    s = sum(el[i] * el[(i+1) % n] * (i+1) for i in range(n))
    return primary + s

# Test all
for name, fn in [
    ("v1", p_v1), ("v2", p_v2), ("v3", p_v3), ("v4", p_v4),
    ("v5", p_v5), ("v6", p_v6), ("v7", p_v7), ("v8", p_v8),
    ("v9", p_v9), ("v10", p_v10), ("v11", p_v11), ("v12", p_v12),
    ("v13", p_v13), ("v14", p_v14), ("v15", p_v15), ("v16", p_v16),
    ("v17", p_v17), ("v18", p_v18),
]:
    bench(name, fn, n)
