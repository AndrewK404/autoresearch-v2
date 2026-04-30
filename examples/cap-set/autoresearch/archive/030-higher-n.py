"""Sweep c2 targets at higher n to find best priority for n=10, 11."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
cap_set_size = m.cap_set_size

def make(t):
    def p(e, n):
        c2 = sum(1 for x in e if x == 2)
        return -abs(c2 - t)
    return p

# n=10
print("=== n=10 ===")
print(f"  |F_3^10| = {3**10}")
for t in range(11):
    t0 = time.time()
    sz = cap_set_size(make(t), 10)
    dt = time.time() - t0
    print(f"  c2={t}: {sz}  ({dt:.1f}s)")

# n=11
print("\n=== n=11 ===")
print(f"  |F_3^11| = {3**11}")
for t in range(12):
    t0 = time.time()
    sz = cap_set_size(make(t), 11)
    dt = time.time() - t0
    print(f"  c2={t}: {sz}  ({dt:.1f}s)")
