"""Extended sweep: a up to 501, L up to 30, K up to 80. Confirm that
all alt-tuple cells in this expanded range still have L' ∈ {1, 2}, so
Theorems A/B/C/D apply and "no extras" is proven (not just empirical)."""
from math import gcd

def alts(a, L, K):
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

total = 0
alt_cells = []
for a in range(3, 502, 2):
    for L in range(2, 31):
        if a**L > 2**80: break
        for K in range(L+1, 81):
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
print("All alt-tuple cells:")
for (a, L, K, b, al) in alt_cells:
    alt_str = "; ".join(f"j={j} L'={Lp} K'={Kp} m'={mp}" for (j, mp, Lp, Kp) in al)
    print(f"  (a={a}, L={L}, K={K}), b={b}: {alt_str}")

# Check: are all alts L' ∈ {1, 2}?
all_lp = set()
for (a, L, K, b, al) in alt_cells:
    for (j, mp, Lp, Kp) in al:
        all_lp.add(Lp)
print(f"\nAll L' values found in alt tuples: {sorted(all_lp)}")
print(f"All L' ≤ 2 (Theorem D fully covers): {max(all_lp) <= 2 if all_lp else True}")
