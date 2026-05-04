"""
Action 051: Cycles of T_{a, 1}(n) = n/2 if even, a*n+1 if odd, for odd a.

By C-020, primitive cycles of (a, 1) at (L, K) ⟺ (2^K - a^L) | S(k, a, L)
for some primitive composition k. Trivial cycle: (L=1, K=k_trivial), 
N_a = 2^{k_trivial} - a = 1, so 2^{k_trivial} = a + 1.

For a+1 = 2^{k_trivial}: a = 2^{k_trivial} - 1. So a ∈ {1, 3, 7, 15, 31, 63, ...}
admit a trivial cycle directly. For a = 5, 9, 11, 13, ..., a+1 is not a
power of 2, so the trivial L=1 K=2 cycle is at N_a = 2^2 - a < 0 (no cycle)
or N_a ≥ 2.

Sweep: for each odd a ∈ {3, 5, 7, 9, 11, 13, 15}, find all (L, K) with
2^K > a^L and any primitive composition k satisfying (2^K - a^L) | S(k).
"""
from math import gcd

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

def find_a_b_1_cycles(a, L_max=12, K_max=22):
    """Find all primitive cycles of cell (a, 1) at any (L, K) within bounds."""
    cycles = []  # list of (L, K, orbit, n_0)
    for L in range(1, L_max+1):
        for K in range(L, K_max+1):
            tK = 2**K
            aL = a**L
            if tK <= aL: continue
            N_a = tK - aL
            seen_orbits = set()
            for k in compositions(K, L):
                if not is_primitive_composition(k): continue
                rot = [tuple(k[i:] + k[:i]) for i in range(L)]
                canon = min(rot)
                if canon in seen_orbits: continue
                seen_orbits.add(canon)
                S = S_value(canon, a, L)
                if S % N_a == 0:
                    n_0 = S // N_a
                    cycles.append((L, K, canon, n_0))
    return cycles

print(f"=== Cycles of (a, 1): a*n+1 dynamics ===")
print(f"{'a':>3} {'(L,K)':>9} {'orbit (k)':<25} {'n_0':>10} {'note':<30}")
for a in [3, 5, 7, 9, 11, 13, 15, 17, 25, 27]:
    cycles = find_a_b_1_cycles(a)
    if not cycles:
        print(f"{a:>3} (none in bound L≤12, K≤22)")
        continue
    for (L, K, orbit, n_0) in cycles[:6]:
        # Verify by tracing
        def T(n, a, b): return n//2 if n%2==0 else a*n+b
        n = n_0
        seen = set()
        chain = []
        steps = 0
        while n not in seen and steps < 200:
            seen.add(n)
            chain.append(n)
            n = T(n, a, 1)
            steps += 1
        cycle_len = len(chain) - chain.index(n) if n in chain else None
        note = f"len={cycle_len} chain[:5]={chain[:5]}"
        print(f"{a:>3} ({L},{K}):>9 {str(orbit):<25} {n_0:>10} {note:<30}")
    if len(cycles) > 6:
        print(f"    ... and {len(cycles) - 6} more")
    print()
