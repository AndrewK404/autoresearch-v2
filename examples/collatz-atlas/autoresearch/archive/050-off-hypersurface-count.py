"""
Action 050: cycle count formula for general (a, b, L, K) — off the m=1
hypersurface. For each primitive composition k of (L, K), the cycle exists
in cell (a, b = N_a/m) iff m | S(k).

Group primitive compositions by their "m-set": M(k) := odd divisors of
gcd(N_a, S(k)). Then cell (a, b = N_a/m) hosts cycles from k iff m ∈ M(k).
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

def odd_divisors(n):
    return [d for d in divisors(n) if d % 2 == 1]

# For each (a, L, K), partition primitive compositions by orbit, then
# count cycles per cell (a, b=N_a/m) for each odd divisor m of N_a.
def cell_cycle_breakdown(a, L, K):
    N_a = 2**K - a**L
    if N_a <= 0: return None
    # primitive compositions, grouped into rotation orbits
    seen_orbits = set()
    orbits = []
    for k in compositions(K, L):
        if not is_primitive_composition(k): continue
        rotations = [tuple(k[i:] + k[:i]) for i in range(L)]
        canon = min(rotations)
        if canon in seen_orbits: continue
        seen_orbits.add(canon)
        S = S_value(canon, a, L)
        orbits.append((canon, S))
    # For each odd divisor m of N_a, count orbits with m | S
    cells = {}
    for m in odd_divisors(N_a):
        b = N_a // m
        if b % 2 == 0: continue  # need b odd
        n_cycles = sum(1 for (k, S) in orbits if S % m == 0)
        cells[m] = (b, n_cycles)
    return N_a, len(orbits), cells

# Sweep cells with composite N_a (where multiple m values produce cycles)
print("=== Off-hypersurface cycle counts ===")
print("Looking for (a, L, K) where N_a is composite, so multiple cells get cycles.")
print()

interesting = []
for a in [3, 5, 7, 9, 11]:
    for L in range(2, 9):
        for K in range(L+1, 18):
            res = cell_cycle_breakdown(a, L, K)
            if not res: continue
            N_a, n_orbits, cells = res
            # If more than one m gives non-zero cycles, it's interesting
            non_trivial = [(m, b, c) for m, (b, c) in cells.items() if c > 0 and m > 1]
            if non_trivial:
                interesting.append((a, L, K, N_a, n_orbits, cells))

# Print first 20 interesting cases
print(f"Found {len(interesting)} (a, L, K) cells with off-hypersurface cycles")
print()
for (a, L, K, N_a, n_orbits, cells) in interesting[:25]:
    L_KL = lyndon_count(K, L)
    print(f"(a={a}, L={L}, K={K}): N_a = 2^{K} - {a}^{L} = {N_a}; L_{{K,L}} = {L_KL}")
    print(f"  Primitive orbits: {n_orbits} (= L_{{K,L}})")
    for m, (b, n) in sorted(cells.items()):
        marker = " ← m=1 primary" if m == 1 else ""
        if n > 0:
            print(f"    cell (a={a}, b={b}): {n} cycles via m={m}{marker}")
    print()
