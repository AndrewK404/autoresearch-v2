"""
Action 052: Sharper Diophantine criterion + much wider sweep + L'=1 proof.

THEOREM (proven): For primary m=1 cell (a, b=2^K-a^L), an alternate (L', K')
with L'+K'=L+K and L'=L-j (j ∈ {1, ..., L-1}) exists iff b | ((2a)^j - 1).

Then m' = 2^j + a^{L-j} * q with q = ((2a)^j - 1)/b.

LEMMA (proven for L'=1): when L'=1, only one composition (K'), S = 1.
For m' >= 2, m' ∤ 1. So L'=1 alts NEVER contribute extras.

EMPIRICAL: across 7291 m=1 cells (action prior), only 3 admit any alt tuple
at all, ALL with 0 extras. Now extending to a≤201, L≤22, K≤60.
"""
from math import gcd, comb

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

def is_primitive(k):
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

def alts(a, L, K):
    """Returns list of (j, m', L', K') for alt tuples of primary (a, L, K)."""
    b = 2**K - a**L
    if b <= 0 or b % 2 == 0: return []
    out = []
    for j in range(1, L):
        twoaj = (2*a)**j
        if (twoaj - 1) % b == 0:
            q = (twoaj - 1) // b
            mp = 2**j + a**(L-j) * q
            out.append((j, mp, L-j, K+j))
    return out

# Wide sweep
print("=== Sweep a ≤ 201 odd, L ≤ 22, K ≤ 60 ===")
total = 0
alt_cells = []
for a in range(3, 202, 2):
    for L in range(2, 23):
        if a**L > 2**60: break  # tK cap
        for K in range(L+1, 61):
            tK = 2**K
            aL = a**L
            if tK <= aL: continue
            b = tK - aL
            if b % 2 == 0: continue
            total += 1
            al = alts(a, L, K)
            if al:
                alt_cells.append((a, L, K, b, al))

print(f"Total m=1 cells tested: {total}")
print(f"Cells with alt tuples: {len(alt_cells)}")
print()
print("All alt-tuple cells found:")
for (a, L, K, b, al) in alt_cells:
    alt_str = "; ".join(f"j={j} L'={Lp} K'={Kp} m'={mp}" for (j, mp, Lp, Kp) in al)
    print(f"  (a={a}, L={L}, K={K}), b={b}: {alt_str}")

# For each alt tuple, count extras: primitive composition k' of (L', K') with mp | S(k')
print()
print("Extras analysis (number of primitive k' with m' | S):")
total_extras = 0
for (a, L, K, b, al) in alt_cells:
    for (j, mp, Lp, Kp) in al:
        if Lp == 1:
            extras = 0  # by L'=1 lemma
        else:
            extras = 0
            for k in compositions(Kp, Lp):
                if not is_primitive(k): continue
                if S_value(k, a, Lp) % mp == 0:
                    extras += 1
        total_extras += extras
        print(f"  (a={a}, L={L}, K={K}, j={j}, L'={Lp}, K'={Kp}, m'={mp}): {extras} extras")

print(f"\nTotal extras across all alt tuples in {total} cells: {total_extras}")
