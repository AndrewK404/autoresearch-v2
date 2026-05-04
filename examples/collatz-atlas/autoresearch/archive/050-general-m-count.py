"""
Action 050: Generalize C-019 to arbitrary m ≥ 1.

For any (a, L, K) with 2^K > a^L, set N_a = 2^K - a^L. Each odd divisor
b of N_a defines a cell (a, b) with m = N_a/b. The number of primitive
cycles of length L+K in cell (a, b) is:

  N(a, b, L, K) := |{ k primitive composition of (L, K) : m | S(k, a, L) }| / L

(with cyclic-rotation orbits, Möbius-corrected).

For m=1, this is L_{K,L}.

Question: as b ranges over divisors of N_a, how does N distribute?

Equivalent reformulation: for each primitive composition k, S(k) is a
positive integer. The cycle (k, n_0 = S(k)/m) exists in cell
(a, b = N_a/m) iff m | gcd(N_a, S(k)). So summing over primitive k:

  sum_{b | N_a, odd} N(a, b, L, K) · L
    = sum over primitive k, summed over orbit reps:
      |{ d : d | gcd(N_a, S(k)), d odd }|

But careful: the orbit dedup is per b, not per k.

Verify: for fixed (a, L, K), sum over all divisors b of N_a of L·N(a,b,L,K)
should equal sum over primitive compositions k of #{odd divisors of
gcd(N_a, S(k))}.
"""
from math import comb, gcd

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

def odd_divisors(n): return [d for d in divisors(n) if d % 2 == 1]

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

# Test: for (a, L, K), compute N_a, then for each primitive composition k,
# count #{ b odd | b divides N_a, and m = N_a/b divides S(k) } 
# (equivalently: # odd divisors of gcd(N_a, S(k)))
# Sum over primitive k, divide by L (rotation orbits).
# Should equal: sum over odd b | N_a of N(a, b, L, K).

def total_cycle_count_distribution(a, L, K):
    N_a = 2**K - a**L
    # Sum over primitive compositions of (L, K), counting odd divisors of
    # gcd(N_a, S(k)). Each contributes one cycle in cell (a, b=N_a/m).
    # We then group by m=N_a/b.
    cycles_by_m = {}
    for k in compositions(K, L):
        if not is_primitive_composition(k): continue
        S = S_value(k, a, L)
        g = gcd(N_a, S)
        for d in odd_divisors(g):
            # d divides N_a and d divides S, so b = N_a/d, m = d.
            # Wait: m = N_a/b and we want m | S, so m | g. Iterate over odd divisors of g.
            # But we want m, and b = N_a/m must be odd too.
            b = N_a // d
            # b must be odd
            if b % 2 != 0:
                cycles_by_m.setdefault(d, []).append((k, S, b))
    return N_a, cycles_by_m

def primitive_cycles_in_cell(a, b, L, K):
    """Direct count: # primitive cycles of (L, K) in cell (a, b)."""
    if (2**K - a**L) % b != 0: return 0
    m = (2**K - a**L) // b
    cycles = set()
    for k in compositions(K, L):
        if not is_primitive_composition(k): continue
        S = S_value(k, a, L)
        if S % m != 0: continue
        # Rotation-orbit dedup: take canonical (lex smallest) rotation
        rotations = [tuple(k[i:] + k[:i]) for i in range(L)]
        canon = min(rotations)
        cycles.add(canon)
    return len(cycles)

# Test on a few (a, L, K) and confirm:
# sum over odd b | N_a of N(a, b, L, K) ≈ sum over primitive k of #odd divisors of gcd(N_a, S(k)) / L
print("=== Distribution of primitive cycles across divisor cells ===")
print()
for (a, L, K) in [(3, 3, 5), (3, 4, 7), (3, 5, 8), (5, 3, 7), (3, 5, 9)]:
    N_a = 2**K - a**L
    print(f"(a={a}, L={L}, K={K}): N_a = 2^{K} - {a}^{L} = {N_a}")
    print(f"  Odd divisors of N_a: {odd_divisors(N_a)}")
    L_KL = lyndon_count(K, L)
    print(f"  L_{{{K},{L}}} = {L_KL}")
    
    for b in odd_divisors(N_a):
        m = N_a // b
        n_cycles = primitive_cycles_in_cell(a, b, L, K)
        marker = " (m=1, primary)" if m == 1 else f" (m={m})"
        print(f"    cell (a={a}, b={b}): {n_cycles} primitive cycles{marker}")
    print()
