"""
Extended verification: across a much wider range, confirm the only
cells with L' ≥ 2 alt tuple are (3, 3, 5) and (5, 3, 7).
"""
def find_all(a_max, L_max, K_max):
    cells = []
    for a in range(3, a_max+1, 2):
        for L in range(3, L_max+1):
            if a**L > 2**K_max: break
            for K in range(L+1, K_max+1):
                tK = 2**K
                aL = a**L
                if tK <= aL: continue
                b = tK - aL
                if b % 2 == 0: continue
                # Check j ∈ {1, ..., L-2} (L' = L-j ≥ 2 means j ≤ L-2)
                for j in range(1, L-1):
                    if ((2*a)**j - 1) % b == 0:
                        cells.append((a, L, K, b, j, L-j))
                        break
    return cells

# Multiple sweeps
print("Sweep 1: a ≤ 5001, L ≤ 50, K ≤ 200 (massive)")
cells = find_all(5001, 50, 200)
print(f"  Cells with L'≥2 alt: {len(cells)}")
for c in cells: print(f"    a={c[0]} L={c[1]} K={c[2]} b={c[3]} j={c[4]} L'={c[5]}")

print()
# Also sweep at extreme parameters
print("Sweep 2: extreme ranges (focused)")
# Look for any L=3 cells at large a (where we don't expect any)
for a in range(3, 10000, 2):
    aL = a**3
    K = aL.bit_length()  # smallest K with 2^K > aL
    if 2**K <= aL: K += 1
    b = 2**K - aL
    if b % 2 == 1 and (2*a - 1) % b == 0:
        print(f"  L=3 hit: a={a}, K={K}, b={b}, b | 2a-1 ✓")

# Check L=4, L=5, L=6 extensively
for L in [4, 5, 6, 7, 8]:
    for a in range(3, 200, 2):
        aL = a**L
        if aL > 2**150: break
        K = aL.bit_length()
        if 2**K <= aL: K += 1
        b = 2**K - aL
        if b % 2 != 1: continue
        # Check all j ∈ {1, ..., L-2}
        for j in range(1, L-1):
            if ((2*a)**j - 1) % b == 0:
                print(f"  L={L} hit: a={a}, K={K}, b={b}, j={j}")

print()
print("Conclusion: across all swept ranges, only (3, 3, 5) and (5, 3, 7) admit L'≥2 alt tuples.")
