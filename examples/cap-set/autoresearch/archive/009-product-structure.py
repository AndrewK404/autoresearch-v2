"""Product-structured priorities."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench

n = 8

# Try at smaller n first to confirm c2-target works
print("--- baseline c2-target across n ---")
for ni in [3, 4, 5, 6, 7, 8]:
    def p(e, n, ni=ni):
        c2 = sum(1 for x in e if x == 2)
        target = ni // 3 if ni % 3 != 2 else ni // 3 + 1
        return -abs(c2 - target)
    bench(f"c2=~n/3 at n={ni}", p, ni)

# c2 = 2 vs 3 at n=7
print("\n--- finer c2 targets at n=7 ---")
for t in range(8):
    def p(e, n, t=t):
        c2 = sum(1 for x in e if x == 2)
        return -abs(c2 - t)
    bench(f"c2={t} @ n=7", p, 7)

# Try product structure: split coords [0:k] {0,1} only (no 2's), [k:n] use c2-balance
print("\n--- product structure (binary head + c2-balanced tail) ---")
for k in range(1, n):
    def p(e, n, k=k):
        head = e[:k]
        tail = e[k:]
        if any(x == 2 for x in head):
            return -1e9 - sum(1 for x in head if x == 2)
        c2 = sum(1 for x in tail if x == 2)
        target_tail = (n - k) // 3 + (1 if (n - k) % 3 == 2 else 0)
        # default to (n-k)/3 rounded
        return -abs(c2 - target_tail)
    bench(f"binary head k={k}, c2-balanced tail", p, 8)

# Reverse: tail as binary, head as c2-balanced
print("\n--- product structure (c2-balanced head + binary tail) ---")
for k in range(1, n):
    def p(e, n, k=k):
        tail = e[n-k:]
        head = e[:n-k]
        if any(x == 2 for x in tail):
            return -1e9 - sum(1 for x in tail if x == 2)
        c2 = sum(1 for x in head if x == 2)
        target_head = (n - k) // 3 + (1 if (n - k) % 3 == 2 else 0)
        return -abs(c2 - target_head)
    bench(f"c2-balanced head, binary tail k={k}", p, 8)

# Strict {0,1} on subsets of coords
print("\n--- strict 2-pos restrictions ---")
for fixed_coord in range(n):
    def p(e, n, fc=fixed_coord):
        c2 = sum(1 for x in e if x == 2)
        primary = -abs(c2 - 3) * 1000
        # bonus if fixed coord is not 2
        secondary = -10 if e[fc] == 2 else 0
        return primary + secondary
    bench(f"c2=3 + coord {fixed_coord} != 2", p, n)
