"""
Extended search: for ALL (a, b) cells on the m=1 hypersurface up to bigger
bounds, find any case where an alternate (L', K') tuple with same T produces
additional primitive cycles via m' | S(k') for a primitive composition k'.
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

def divisors(n):
    return [d for d in range(1, n+1) if n%d==0]

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

# Sweep ranges
a_max = 25
L_max = 12
K_max = 28

cells_with_alt_tuples = 0
cells_with_extras = 0
total_cells = 0
cells_examined = []

for a in range(3, a_max+1, 2):
    for L in range(1, L_max+1):
        for K in range(L+1, K_max+1):
            tK = 2**K
            aL = a**L
            if tK <= aL: continue
            b = tK - aL
            T = K + L
            total_cells += 1
            # Find alternate (L', K') with L'+K'=T, same b satisfying b | (2^{K'} - a^{L'})
            extras_total = 0
            alt_tuples_count = 0
            for Lp in range(1, T):
                Kp = T - Lp
                if Lp == L and Kp == K: continue
                if Kp < 1: continue
                aLp = a**Lp
                tKp = 2**Kp
                if tKp <= aLp: continue
                val = tKp - aLp
                if val % b != 0: continue
                mp = val // b
                alt_tuples_count += 1
                # For this alternate tuple, count primitive compositions where mp | S
                for k in compositions(Kp, Lp):
                    if not is_primitive_composition(k): continue
                    if S_value(k, a, Lp) % mp == 0:
                        extras_total += 1
            if alt_tuples_count > 0:
                cells_with_alt_tuples += 1
                cells_examined.append((a, L, K, b, alt_tuples_count, extras_total))
                if extras_total > 0:
                    cells_with_extras += 1

print(f"Total m=1 cells tested: {total_cells}")
print(f"Cells with alternate tuples (same total length T): {cells_with_alt_tuples}")
print(f"Cells with EXTRA primitive cycles from alternate tuples: {cells_with_extras}")
print()
if cells_examined:
    print("Cells with alternate-tuple coexistence:")
    print(f"{'a':>3} {'L':>3} {'K':>3} {'b':>10} {'alt#':>5} {'extras':>7}")
    for c in cells_examined:
        print(f"{c[0]:>3} {c[1]:>3} {c[2]:>3} {c[3]:>10} {c[4]:>5} {c[5]:>7}")
print()
print("=== Extended sweep: a up to 51, K up to 35 ===")
