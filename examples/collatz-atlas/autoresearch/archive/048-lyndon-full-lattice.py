"""
FULL m=1 theorem (C-019 extended): for any (a, K, L) with 2^K > a^L,
b = 2^K - a^L odd, the (a, b) cell admits exactly

  L_k(K, L) := (1/L) * sum_{d | gcd(K, L)} mu(d) * C(K/d - 1, L/d - 1)

primitive cycles of length K + L (the binary Lyndon-word count).
For gcd=1 this reduces to C(K-1, L-1)/L. For gcd>1 the Möbius
correction excludes imprimitive (rotation-symmetric) cycles.

Verify across cells with gcd > 1.
"""
from math import comb, gcd

def mobius(n):
    if n == 1: return 1
    r, p = 1, 2
    nn = n
    while p * p <= nn:
        if nn % p == 0:
            nn //= p
            if nn % p == 0: return 0
            r = -r
        p += 1
    if nn > 1: r = -r
    return r

def divisors(n):
    return [d for d in range(1, n+1) if n % d == 0]

def lyndon_count(K, L):
    g = gcd(K, L)
    s = sum(mobius(d) * comb(K//d - 1, L//d - 1) for d in divisors(g))
    return s // L

def T(n, a, b):
    return n // 2 if n % 2 == 0 else a*n + b

def compositions(K, L):
    if L == 1:
        if K >= 1: yield (K,)
        return
    for first in range(1, K - L + 2):
        for rest in compositions(K - first, L - 1):
            yield (first,) + rest

def S_value(k_tuple, a, L):
    s, cum = 0, 0
    for i in range(L):
        s += a**(L-1-i) * 2**cum
        cum += k_tuple[i]
    return s

def is_primitive_composition(k):
    L = len(k)
    for d in range(1, L):
        if L % d == 0 and tuple(k[:d]) * (L//d) == k:
            return False
    return True

def find_cycle_from(start, n_max, a, b):
    seen_local = {}
    path = []
    n = start
    steps = 0
    while steps < 200000:
        if n > n_max or n <= 0: return None
        if n in seen_local:
            return path[seen_local[n]:]
        seen_local[n] = steps
        path.append(n)
        n = T(n, a, b)
        steps += 1
    return None

def verify_cell(a, L, K):
    b = 2**K - a**L
    if b <= 0 or b % 2 == 0: return None
    pred = lyndon_count(K, L)
    if pred <= 0: return None
    
    # Count distinct primitive cycles of length K+L from primitive compositions
    primitive_n0 = set()
    for k in compositions(K, L):
        if is_primitive_composition(k):
            n0 = S_value(k, a, L)
            if n0 % 2 == 1:
                primitive_n0.add(n0)
    
    cycles = set()
    n_max = max(b * 50, 100000)
    for n0 in primitive_n0:
        trace = find_cycle_from(n0, n_max, a, b)
        if trace and len(trace) == K + L:
            cycles.add(frozenset(trace))
    return (b, pred, len(cycles), gcd(K, L))

print("=== Möbius/Lyndon test: cells with gcd(K, L) > 1 ===")
print(f"{'a':>3} {'L':>3} {'K':>3} {'gcd':>4} {'b':>10} {'pred':>5} {'actual':>6} {'match':>6}")
test_cells = [
    (3, 2, 4), (3, 2, 6), (3, 2, 8), (3, 3, 6), (3, 3, 9),
    (3, 4, 8), (3, 4, 10), (3, 4, 12),
    (3, 5, 10), (3, 5, 15),
    (3, 6, 12), (3, 6, 14),
    (5, 2, 4), (5, 2, 6), (5, 3, 9), (5, 4, 10),
    (7, 2, 6), (7, 3, 9),
]
n_match = 0
n_total = 0
for (a, L, K) in test_cells:
    r = verify_cell(a, L, K)
    if r is None:
        continue
    b, pred, act, g = r
    n_total += 1
    match = pred == act
    if match: n_match += 1
    flag = 'OK' if match else 'FAIL'
    print(f"{a:>3} {L:>3} {K:>3} {g:>4} {b:>10} {pred:>5} {act:>6} {flag:>6}")

print(f"\nTotal: {n_match}/{n_total} matches")
