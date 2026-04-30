"""Sweep around the c2-balance discovery."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

def make_target_c2(target):
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        return -abs(c2 - target) * 1.0
    return p

def make_target_c2_sq(target):
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        return -float((c2 - target) ** 2)
    return p

def p_target_c2_2(e, n):
    c2 = sum(1 for x in e if x == 2)
    return -abs(c2 - 2) * 1.0

# Try different counts targets
for t in range(0, 9):
    bench(f"|c2-{t}|", make_target_c2(t), n)

# Also try squared distance
for t in range(0, 9):
    bench(f"(c2-{t})^2", make_target_c2_sq(t), n)

# Joint: prefer specific counts (c0, c1, c2)
def make_count_target(c0t, c1t, c2t):
    def p(e, n):
        c0 = sum(1 for x in e if x == 0)
        c1 = sum(1 for x in e if x == 1)
        c2 = sum(1 for x in e if x == 2)
        return -float(abs(c0 - c0t) + abs(c1 - c1t) + abs(c2 - c2t))
    return p

print("--- joint count targets ---")
for c0t, c1t, c2t in [(2,3,3), (3,3,2), (3,2,3), (2,2,4), (4,2,2),
                      (4,3,1), (1,3,4), (3,4,1), (1,4,3), (5,2,1),
                      (2,4,2), (4,2,2), (2,2,4)]:
    bench(f"counts=({c0t},{c1t},{c2t})", make_count_target(c0t, c1t, c2t), n)
