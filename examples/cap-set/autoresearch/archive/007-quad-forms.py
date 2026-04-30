"""Quadratic forms and matrix-based priorities."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Try priority = x^T A x mod 3 for various A
def make_quad(A, mode="zero"):
    A = np.array(A, dtype=int)
    def p(e, n):
        x = np.array(e, dtype=int)
        v = int(x @ A @ x % 3)
        if mode == "zero":
            return -float(v)
        elif mode == "max":
            return float(v)
        else:
            return float(v == 0)
    return p

# Identity
A_id = np.eye(n, dtype=int)
# Off-diagonal all ones
A_off = np.ones((n, n), dtype=int) - np.eye(n, dtype=int)
# Cyclic
A_cyc = np.zeros((n, n), dtype=int)
for i in range(n):
    A_cyc[i, (i+1) % n] = 1
# Random-ish but deterministic
A_rand = np.array([[(i * j + i + j) % 3 for j in range(n)] for i in range(n)])

bench("quad x^T I x ==0", make_quad(A_id, "kernel"), n)
bench("quad x^T I x mod3 -", make_quad(A_id, "zero"), n)
bench("quad x^T off x ==0", make_quad(A_off, "kernel"), n)
bench("quad x^T off x mod3 -", make_quad(A_off, "zero"), n)
bench("quad x^T cyc x ==0", make_quad(A_cyc, "kernel"), n)
bench("quad x^T rand x ==0", make_quad(A_rand, "kernel"), n)

# Combined with c2=3
def make_c2_then_quad(A):
    A = np.array(A, dtype=int)
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 10000
        x = np.array(e, dtype=int)
        v = int((x @ A @ x) % 3)
        return primary - float(v)
    return p

bench("c2=3 + quad I -", make_c2_then_quad(A_id), n)
bench("c2=3 + quad off -", make_c2_then_quad(A_off), n)
bench("c2=3 + quad cyc -", make_c2_then_quad(A_cyc), n)
bench("c2=3 + quad rand -", make_c2_then_quad(A_rand), n)

# Linear forms
def make_lin(a, mode="zero"):
    a = np.array(a, dtype=int)
    def p(e, n):
        x = np.array(e, dtype=int)
        v = int((x @ a) % 3)
        if mode == "zero":
            return -float(v)
        return float(v == 0)
    return p

bench("lin (1,1,1,1,1,1,1,1) ==0", make_lin([1]*n, "kernel"), n)
bench("lin (1,2,1,2,1,2,1,2) ==0", make_lin([1,2]*4, "kernel"), n)
bench("lin (1,2,0,1,2,0,1,2) ==0", make_lin([1,2,0,1,2,0,1,2], "kernel"), n)
bench("lin (0,1,2,0,1,2,0,1) ==0", make_lin([0,1,2,0,1,2,0,1], "kernel"), n)

# Combined: c2=3 within lin=0
def p_c2_lin0(e, n):
    c2 = sum(1 for x in e if x == 2)
    s = sum(e) % 3
    primary = -abs(c2 - 3) * 100
    if s == 0:
        return primary + 50
    return primary

bench("c2=3 AND sum==0", p_c2_lin0, n)

# Stacked priority: hierarchical
def p_layered_1(e, n):
    c2 = sum(1 for x in e if x == 2)
    s = sum(e) % 3
    return float(-(c2 - 3)**2 * 100 - s * 1)

bench("layered(c2,sum)", p_layered_1, n)

# Bilinear with index weights
def p_bilinear_idx(e, n):
    s = 0
    for i in range(n):
        for j in range(i+1, n):
            s += (e[i] * e[j]) * (i + 1) * (j + 1)
    return -float(s % 3)

bench("bilinear with index weights", p_bilinear_idx, n)

# Many random linear/quadratic forms
np.random.seed(42)
for trial in range(20):
    A = np.random.randint(0, 3, (n, n))
    A = (A + A.T)  # symmetric
    def p(e, n, A=A):
        x = np.array(e, dtype=int)
        v = int((x @ A @ x) % 3)
        return -float(v)
    bench(f"random quad {trial}", p, n)
