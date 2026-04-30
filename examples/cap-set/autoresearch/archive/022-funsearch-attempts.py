"""FunSearch-style attempts based on inferred priority structure."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Inspired by patterns in FunSearch evolved priorities
def p_fs_a(el, n):
    score = 0.
    el = list(el)
    for i in range(n):
        for j in range(n):
            if el[i] == 1 and el[j] == 2 and i < j:
                score += i + j
            if el[i] == 0 and el[j] == 2:
                score += (i - j) ** 2
            if el[i] == el[j] and i != j:
                score -= (i - j) ** 2
    return score

def p_fs_b(el, n):
    score = 0.
    el = list(el)
    c1 = el.count(1)
    c2 = el.count(2)
    score += abs(c1 - c2)
    for i in range(n):
        for j in range(i+1, n):
            score += abs(el[i] - el[j])
    return score

def p_fs_c(el, n):
    el = list(el)
    score = 0
    for i in range(n):
        if el[i] == 0:
            score += i
        elif el[i] == 1:
            score -= i
        else:
            score += i * 2
    return float(score)

def p_fs_d(el, n):
    el = list(el)
    score = 0
    for i in range(n):
        for j in range(i+1, n):
            score += (el[i] + 2*el[j]) % 3
    return float(score)

def p_fs_e(el, n):
    el = list(el)
    return float(sum(el[i] * (i+1) ** 2 for i in range(n)) % 3)

def p_fs_f(el, n):
    el = list(el)
    score = 0
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                score += (el[i] + el[j] + el[k]) % 3
    return -float(score)

def p_fs_g(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1000
    for i in range(n):
        for j in range(i+1, n):
            if el[i] != 2 and el[j] != 2:
                score += abs(el[i] - el[j])
    return float(score)

# A specific attempt: priority that explicitly encodes "extending" approach
def p_fs_h(el, n):
    el = list(el)
    score = 0
    counts = [el.count(0), el.count(1), el.count(2)]
    # discourage counts that lead to bad APs
    if counts[2] == 3:
        score += 1000
    elif counts[2] == 2:
        score += 800
    elif counts[2] == 4:
        score += 600

    # plus a function of the position pattern
    pos_2 = tuple(i for i, x in enumerate(el) if x == 2)
    pos_1 = tuple(i for i, x in enumerate(el) if x == 1)

    # encourage 2's to be in early positions
    if pos_2:
        score += sum(i for i in pos_2)
    if pos_1:
        score -= sum(i for i in pos_1)

    return float(score)

# Combination of c2-target + index-weighted feature
def p_fs_i(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1_000_000
    # within cluster: index-weighted
    weight = sum(el[i] * (i+1) for i in range(n))
    return float(score + weight)

def p_fs_j(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1_000_000
    # within cluster: count of "consecutive 2's"
    count = 0
    for i in range(n - 1):
        if el[i] == 2 and el[i+1] == 2:
            count += 1
    return float(score - count * 100)

# Penalty/reward for specific patterns
def p_fs_k(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1_000_000
    # count (1, 2) and (2, 1) adjacent pairs
    count_12 = 0
    for i in range(n - 1):
        if (el[i] == 1 and el[i+1] == 2) or (el[i] == 2 and el[i+1] == 1):
            count_12 += 1
    return float(score + count_12)

# Cyclic patterns
def p_fs_l(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1_000_000
    # cyclic version
    count = 0
    for i in range(n):
        if el[i] == 2 and el[(i+1) % n] != 2:
            count += 1
    return float(score + count)

# All zeros at specific positions
def p_fs_m(el, n):
    el = list(el)
    c2 = el.count(2)
    if c2 != 3:
        return -1e9 - abs(c2 - 3)
    pos_2 = sorted(i for i, x in enumerate(el) if x == 2)
    # prefer 2's spread out
    if len(pos_2) >= 3:
        gaps = [pos_2[i+1] - pos_2[i] for i in range(len(pos_2) - 1)]
        return float(min(gaps))  # max-min spread
    return 0.0

# Hash-like priority within c2=3
def p_fs_n(el, n):
    el = list(el)
    c2 = el.count(2)
    score = -abs(c2 - 3) * 1_000_000
    h = sum(el[i] * (3**i) for i in range(n))
    return float(score + h)

bench("FS pattern A", p_fs_a, n)
bench("FS pattern B", p_fs_b, n)
bench("FS pattern C", p_fs_c, n)
bench("FS pattern D", p_fs_d, n)
bench("FS pattern E", p_fs_e, n)
bench("FS pattern F", p_fs_f, n)
bench("FS pattern G", p_fs_g, n)
bench("FS pattern H", p_fs_h, n)
bench("FS pattern I (c2=3 + idx-wt)", p_fs_i, n)
bench("FS pattern J (c2=3 - adj-2)", p_fs_j, n)
bench("FS pattern K (c2=3 + (1,2) adj)", p_fs_k, n)
bench("FS pattern L (cyclic)", p_fs_l, n)
bench("FS pattern M (max-min spread)", p_fs_m, n)
bench("FS pattern N (within-c2 hash)", p_fs_n, n)
