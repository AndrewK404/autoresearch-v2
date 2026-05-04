"""
General theorem candidate (C-019):
For any (a, K, L) with gcd(K, L) = 1, K > L·log_2(a), and b = 2^K - a^L odd,
the cell (a, b) admits EXACTLY C(K-1, L-1)/L primitive cycles via the m=1
mechanism in C-011, provided every composition yields odd n_0.

Verify across a 2D lattice of (L, K) for a=3, and spot-check a=5.
"""
from math import comb, gcd

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

def find_cycle_from(start, n_max, a, b):
    seen_local = {}
    path = []
    n = start
    steps = 0
    while steps < 200000:
        if n > n_max or n <= 0:
            return None
        if n in seen_local:
            idx = seen_local[n]
            return path[idx:]
        seen_local[n] = steps
        path.append(n)
        n = T(n, a, b)
        steps += 1
    return None

def predict_and_verify(a, L, K):
    """Verify cycle count for (a, b=2^K-a^L) with m=1."""
    b = 2**K - a**L
    if b <= 0 or b % 2 == 0:
        return None
    if gcd(K, L) != 1:
        return None  # gcd!=1 case is more complex
    expected = comb(K-1, L-1) // L
    # Sanity: divisibility
    if comb(K-1, L-1) % L != 0:
        return None  # shouldn't happen if gcd=1 by Burnside

    n0_set = set()
    for k in compositions(K, L):
        s = S_value(k, a, L)
        if s % 2 == 1:  # odd
            n0_set.add(s)
    cycles = set()
    n_max = max(b * 50, 100000)
    for n0 in n0_set:
        trace = find_cycle_from(n0, n_max, a, b)
        if trace:
            cycles.add(frozenset(trace))
    return (b, expected, len(cycles), set(len(c) for c in cycles) if cycles else set())

print("=== Lattice test for a=3 ===")
print(f"{'L':>3} {'K':>3} {'b':>12} {'pred':>6} {'actual':>6} {'len':>5} {'match':>5}")
results = []
for L in range(1, 7):
    for K in range(L+1, min(20, L*4)):
        if gcd(K, L) != 1:
            continue
        r = predict_and_verify(3, L, K)
        if r is None:
            continue
        b, exp, act, lens = r
        match = exp == act
        lenstr = str(sorted(lens)[0]) if lens else '-'
        flag = 'OK' if match else 'FAIL'
        if exp <= 5000:  # don't print giant tables, just spot-check
            print(f"{L:>3} {K:>3} {b:>12} {exp:>6} {act:>6} {lenstr:>5} {flag:>5}")
        results.append((L, K, b, exp, act, match))

n_match = sum(1 for r in results if r[5])
n_total = len(results)
print(f"\nTotal tests: {n_total}, matches: {n_match}, fails: {n_total - n_match}")

print("\n=== Spot check a=5 ===")
print(f"{'L':>3} {'K':>3} {'b':>12} {'pred':>6} {'actual':>6} {'len':>5} {'match':>5}")
for L in range(1, 5):
    for K in range(L+1, min(15, int(L*2.5)+3)):
        if gcd(K, L) != 1:
            continue
        r = predict_and_verify(5, L, K)
        if r is None:
            continue
        b, exp, act, lens = r
        match = exp == act
        lenstr = str(sorted(lens)[0]) if lens else '-'
        flag = 'OK' if match else 'FAIL'
        print(f"{L:>3} {K:>3} {b:>12} {exp:>6} {act:>6} {lenstr:>5} {flag:>5}")

print("\n=== Spot check a=7 ===")
for L in range(1, 4):
    for K in range(L+1, min(15, int(L*3.5)+3)):
        if gcd(K, L) != 1:
            continue
        r = predict_and_verify(7, L, K)
        if r is None:
            continue
        b, exp, act, lens = r
        match = exp == act
        lenstr = str(sorted(lens)[0]) if lens else '-'
        flag = 'OK' if match else 'FAIL'
        print(f"{L:>3} {K:>3} {b:>12} {exp:>6} {act:>6} {lenstr:>5} {flag:>5}")
