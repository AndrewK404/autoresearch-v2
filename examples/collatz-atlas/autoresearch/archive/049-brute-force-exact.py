"""Hybrid: predicted-n_0 verification (counts what scripts in action 048 do)
PLUS independent brute-force on smaller cells to confirm the predicted count
isn't missing anything from m>1 alternate tuples.

The predicted-n_0 approach: enumerate primitive compositions of (L, K),
compute n_0 = S(k)/m for primary (m=1, so n_0 = S(k)), trace cycles, count
distinct cycles of length T = K+L. This is what the Möbius formula counts.

For independent brute-force we use much wider bounds.
"""
from math import comb, gcd
import sys

def mobius(n):
    if n == 1: return 1
    r, p, nn = 1, 2, n
    while p*p <= nn:
        if nn%p==0:
            nn //= p
            if nn%p==0: return 0
            r = -r
        p += 1
    if nn > 1: r = -r
    return r

def divisors(n): return [d for d in range(1, n+1) if n%d==0]

def lyndon_count(K, L):
    g = gcd(K, L)
    s = sum(mobius(d) * comb(K//d - 1, L//d - 1) for d in divisors(g))
    return s // L

def compositions(K, L):
    if L == 1:
        if K >= 1: yield (K,)
        return
    for first in range(1, K - L + 2):
        for rest in compositions(K - first, L - 1):
            yield (first,) + rest

def is_primitive_composition(k):
    L = len(k)
    for d in range(1, L):
        if L % d == 0 and tuple(k[:d]) * (L//d) == k:
            return False
    return True

def S_value(k_tuple, a, L):
    s, cum = 0, 0
    for i in range(L):
        s += a**(L-1-i) * 2**cum
        cum += k_tuple[i]
    return s

def T(n, a, b):
    return n // 2 if n % 2 == 0 else a*n + b

def trace(start, a, b, n_bound, max_steps):
    seen = {}
    path = []
    n = start
    steps = 0
    while steps < max_steps:
        if n > n_bound or n <= 0: return None
        if n in seen:
            return path[seen[n]:]
        seen[n] = steps
        path.append(n)
        n = T(n, a, b)
        steps += 1
    return None

def composition_traced_count(a, L, K):
    """Count primitive cycles of length L+K via composition n_0 enumeration."""
    b = 2**K - a**L
    cycles = set()
    n_bound = 100 * b * a**L
    for k in compositions(K, L):
        S = S_value(k, a, L)
        # n_0 = S (m=1)
        if S % 2 == 0: continue
        cyc = trace(S, a, b, n_bound, 1000000)
        if cyc and len(cyc) == K + L:
            cycles.add(frozenset(cyc))
    return len(cycles)

def brute_force_count(a, L, K, seed_factor=20, n_factor=200):
    """Brute-force: try every odd seed up to bound, count cycles of length L+K."""
    b = 2**K - a**L
    target_T = K + L
    seed_bound = seed_factor * a**L + 100
    n_bound = n_factor * a**L * b
    found_cycles = set()
    seen_starts = set()
    for n0 in range(1, seed_bound, 2):
        if n0 in seen_starts: continue
        cyc = trace(n0, a, b, n_bound, 1000000)
        if cyc is None:
            seen_starts.add(n0)
            continue
        if len(cyc) == target_T:
            found_cycles.add(frozenset(cyc))
        seen_starts.update(cyc)
    return len(found_cycles), seed_bound

test_cells = [
    (3, 1, 3),
    (3, 2, 4),
    (3, 3, 5),
    (3, 4, 7),
    (3, 5, 8),
    (3, 5, 9),    # was failing — bigger bounds
    (3, 4, 8),    # gcd=4 — was failing
    (5, 2, 5),
    (5, 3, 7),
    (7, 2, 7),
]

print(f"{'a':>3} {'b':>5} {'L':>3} {'K':>3} {'T':>3} {'gcd':>4} {'L_KL':>5} {'comp':>5} {'brute':>6} {'match':>6}")
for (a, L, K) in test_cells:
    b = 2**K - a**L
    g = gcd(K, L)
    pred = lyndon_count(K, L)
    comp_count = composition_traced_count(a, L, K)
    brute_count, _ = brute_force_count(a, L, K)
    match_all = (pred == comp_count == brute_count)
    flag = 'OK' if match_all else f'pred={pred} comp={comp_count} brute={brute_count}'
    print(f"{a:>3} {b:>5} {L:>3} {K:>3} {K+L:>3} {g:>4} {pred:>5} {comp_count:>5} {brute_count:>6} {flag:>6}")
