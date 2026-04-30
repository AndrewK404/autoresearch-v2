"""More diverse priority functions: combinations and patterns."""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def p_c2_3_strict(e, n):
    c2 = sum(1 for x in e if x == 2)
    return 1.0 if c2 == 3 else 0.0

def p_c2_pmf(e, n):
    # Use proxy: priority is high near c2=3 with smooth fall-off
    c2 = sum(1 for x in e if x == 2)
    return -float((c2 - 8/3) ** 2)

def p_c2_with_secondary_count(e, n):
    # only ties matter; explore which secondary helps
    c2 = sum(1 for x in e if x == 2)
    if c2 != 3:
        return -1000.0 - abs(c2 - 3)
    # within c2=3: try various secondaries
    return 0.0

def make_secondary_within_c2_3(secondary):
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        if c2 != 3:
            return -1000.0 - abs(c2 - 3)
        return float(secondary(e, n))
    return p

# secondary by c1
sec_c1_3 = lambda e, n: -abs(sum(1 for x in e if x == 1) - 3)
sec_c0_3 = lambda e, n: -abs(sum(1 for x in e if x == 0) - 3)
sec_c1_2 = lambda e, n: -abs(sum(1 for x in e if x == 1) - 2)
sec_lex = lambda e, n: -sum(x * 3**i for i, x in enumerate(e))
sec_lex_neg = lambda e, n: sum(x * 3**i for i, x in enumerate(e))
sec_norm = lambda e, n: -sum(x*x for x in e)
sec_pair_eq_neg = lambda e, n: -sum(1 for i in range(n) for j in range(i+1,n) if e[i]==e[j])
sec_pair_eq_pos = lambda e, n: sum(1 for i in range(n) for j in range(i+1,n) if e[i]==e[j])
sec_pair_zero_neg = lambda e, n: -sum(1 for i in range(n) for j in range(i+1,n) if (e[i]+e[j])%3==0)
sec_diag = lambda e, n: -(sum(x*x for x in e) % 3)

# Let's test secondaries on c2=3 cluster
bench("c2=3 strict (binary)", p_c2_3_strict, n)
bench("c2 ~ 8/3 squared", p_c2_pmf, n)
bench("c2=3 only, sec c1=3", make_secondary_within_c2_3(sec_c1_3), n)
bench("c2=3 only, sec c0=3", make_secondary_within_c2_3(sec_c0_3), n)
bench("c2=3 only, sec c1=2", make_secondary_within_c2_3(sec_c1_2), n)
bench("c2=3 only, sec lex", make_secondary_within_c2_3(sec_lex), n)
bench("c2=3 only, sec lex_neg", make_secondary_within_c2_3(sec_lex_neg), n)
bench("c2=3 only, sec norm", make_secondary_within_c2_3(sec_norm), n)
bench("c2=3 only, sec pair_eq -", make_secondary_within_c2_3(sec_pair_eq_neg), n)
bench("c2=3 only, sec pair_eq +", make_secondary_within_c2_3(sec_pair_eq_pos), n)
bench("c2=3 only, sec pair_zero -", make_secondary_within_c2_3(sec_pair_zero_neg), n)
bench("c2=3 only, sec diag", make_secondary_within_c2_3(sec_diag), n)

# Now reverse: c2 != 3 elements still searched, but lower priority
def p_c2_lex_combined(e, n):
    c2 = sum(1 for x in e if x == 2)
    primary = -abs(c2 - 3)  # stable sort acts as natural tiebreak
    return primary

bench("base reaffirm", p_c2_lex_combined, n)

# Try also targeting different counts
for k in [2, 3, 4]:
    for j in [2, 3, 4]:
        def p(e, n, k=k, j=j):
            c2 = sum(1 for x in e if x == 2)
            c1 = sum(1 for x in e if x == 1)
            return -float(abs(c2 - k) * 1000 + abs(c1 - j))
        bench(f"c2={k}, c1={j} (weighted)", p, n)

# Bilinear combinations
def p_c2_minus_c1(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float(c2 - c1)

def p_c1_minus_c2(e, n):
    c1 = sum(1 for x in e if x == 1)
    c2 = sum(1 for x in e if x == 2)
    return float(c1 - c2)

bench("c2 - c1", p_c2_minus_c1, n)
bench("c1 - c2", p_c1_minus_c2, n)

# Functions of multiset only (permutation invariant)
# Encoded by (c0, c1, c2) tuple directly
# Try every (c0,c1,c2) target with c0+c1+c2=8
results = []
for c2t in range(9):
    for c1t in range(9 - c2t):
        c0t = 8 - c1t - c2t
        def p(e, n, c0t=c0t, c1t=c1t, c2t=c2t):
            c0 = sum(1 for x in e if x == 0)
            c1 = sum(1 for x in e if x == 1)
            c2 = sum(1 for x in e if x == 2)
            return -float(abs(c0-c0t) + abs(c1-c1t) + abs(c2-c2t))
        sz = bench(f"target c=({c0t},{c1t},{c2t})", p, n)
        results.append((sz, (c0t, c1t, c2t)))

best = max(results)
print(f"\nbest count target: {best}")
