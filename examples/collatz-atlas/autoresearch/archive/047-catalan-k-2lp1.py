"""Test second Catalan family: K = 2L+1, b = 2^{2L+1} - 3^L for a=3.

By Burnside: C(K-1, L-1)/L = C(2L, L-1)/L = C_L (Catalan).
gcd(2L+1, L) = 1, so no rotation symmetry.
"""
from math import comb

def T(n, a, b):
    return n // 2 if n % 2 == 0 else a*n + b

def compositions(K, L):
    if L == 1:
        if K >= 1:
            yield (K,)
        return
    for first in range(1, K - L + 2):
        for rest in compositions(K - first, L - 1):
            yield (first,) + rest

def S_value(k_tuple, a, L):
    s = 0
    cum = 0
    for i in range(L):
        s += a**(L-1-i) * 2**cum
        cum += k_tuple[i]
    return s

def find_cycle_from(start, S_max, a, b):
    seen_local = {}
    path = []
    n = start
    steps = 0
    while steps < 100000:
        if n > S_max * 100 or n <= 0:
            return None
        if n in seen_local:
            idx = seen_local[n]
            return path[idx:]
        seen_local[n] = steps
        path.append(n)
        n = T(n, a, b)
        steps += 1
    return None

a = 3
print(f"=== Catalan family #2: K = 2L+1, b = 2^K - 3^L, a={a} ===")
print(f"{'L':>3} {'K':>3} {'b':>10} {'C_L':>6} {'cycles':>7} {'len':>5} {'match':>5}")
for L in range(1, 8):
    K = 2*L + 1
    b = 2**K - 3**L
    if b <= 0 or b % 2 == 0:
        print(f"  L={L} skip (b={b})")
        continue
    catalan_L = comb(2*L, L) // (L+1)  # C_L
    n0_set = set()
    for k in compositions(K, L):
        s = S_value(k, a, L)
        n0_set.add(s)
    cycles = set()
    for n0 in n0_set:
        if n0 % 2 == 0:
            continue
        trace = find_cycle_from(n0, b * 100, a, b)
        if trace:
            cycles.add(frozenset(trace))
    lengths = set(len(c) for c in cycles) if cycles else {0}
    match = (len(cycles) == catalan_L)
    print(f"{L:>3} {K:>3} {b:>10} {catalan_L:>6} {len(cycles):>7} {next(iter(lengths)):>5} {'OK' if match else 'FAIL'}")
