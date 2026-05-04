"""Faster sweep for L'≥3 alts. Use direct iteration instead of factoring."""
from math import gcd

def find_L_gte_3_alts(a_max, L_max, K_max):
    found = []
    for a in range(3, a_max+1, 2):
        # Precompute (2a)^j - 1 for j up to L_max-1
        for L in range(4, L_max+1):  # L ≥ 4 needed for L' ≥ 3
            for K in range(L+1, K_max+1):
                tK = 2**K
                aL = a**L
                if tK <= aL: continue
                b = tK - aL
                if b % 2 == 0: continue
                # Check j ∈ {3, ..., L-1}: does b | (2a)^j - 1?
                for j in range(3, L):
                    if ((2*a)**j - 1) % b == 0:
                        Lp = L - j
                        q = ((2*a)**j - 1) // b
                        mp = 2**j + a**Lp * q
                        found.append((a, L, K, b, j, Lp, K+j, mp))
    return found

# Sweep
print("Sweep: a ≤ 201, L ≤ 22, K ≤ 60 — looking for L' ≥ 3 alt tuples")
found = find_L_gte_3_alts(201, 22, 60)
print(f"Found: {len(found)}")
for f in found[:30]:
    print(f"  {f}")
