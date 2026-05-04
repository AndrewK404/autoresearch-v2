"""
For each of the 5 candidate cells, check whether the alternate (L', K') tuple
actually produces additional primitive cycles of length K+L beyond the m=1
prediction L_{K,L}.

For an m'>1 tuple (L', K'), we need:
  - Primitive composition k' of K' into L' positive parts (Lyndon word).
  - m' | S(k') where S(k') = sum a^{L'-1-i} * 2^{k_1+...+k_i}.

If any such k' exists, the cell has EXTRA primitive cycles of length T=K+L.
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

candidates = [
    # (a, L, K, b, Lp, Kp, mp)
    (3, 3, 5, 5, 1, 7, 25),
    (3, 3, 5, 5, 2, 6, 11),
    (5, 3, 7, 3, 1, 9, 169),
    (5, 3, 7, 3, 2, 8, 77),
    (11, 2, 7, 7, 1, 8, 35),
]

print(f"{'a':>3} {'(L,K)':>7} {'b':>5} {'(Lp,Kp)':>9} {'mp':>5} {'extras?':>8} {'note':>30}")
print("-" * 80)

for (a, L, K, b, Lp, Kp, mp) in candidates:
    extras = 0
    found_compositions = []
    for k in compositions(Kp, Lp):
        if not is_primitive_composition(k): continue
        S = S_value(k, a, Lp)
        if S % mp == 0:
            extras += 1
            found_compositions.append((k, S, S // mp))
    note = f"extras={extras}"
    if found_compositions:
        # note: rotation-equivalent compositions give same cycle; count orbits
        note += f" (n0={found_compositions[0][2]})"
    primary_count = lyndon_count(K, L)
    print(f"{a:>3} ({L},{K}):>7 {b:>5} ({Lp},{Kp}):>9 {mp:>5} {extras:>8} primary L_K,L={primary_count}, k'={[c[0] for c in found_compositions[:3]]}")
