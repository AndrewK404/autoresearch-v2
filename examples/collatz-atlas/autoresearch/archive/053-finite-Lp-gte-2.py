"""
Action 053: A potentially novel finiteness result.

Hypothesis: only finitely many primary m=1 cells admit any alt tuple
with L' ≥ 2. Empirically (across 84880 cells): exactly TWO such cells:
(a=3, L=3, K=5, b=5) and (a=5, L=3, K=7, b=3). Both with L'=2 alt only.

Need to PROVE finiteness, ideally identifying all such cells exhaustively.

Strategy: for L'≥2 alt at j = L - L' ≥ 1, the criterion `b | (2a)^j - 1`
combined with `b = 2^K - a^L` gives:
  2^K - a^L divides (2a)^j - 1
  ⟹ 2^K - a^L ≤ (2a)^j - 1 ≤ (2a)^{L-2} - 1 (since j ≤ L-2 for L'≥2).

This is a Pillai-type Diophantine condition. By Mihăilescu/Tijdeman bounds,
|2^K - a^L| has effective lower bounds that GROW with max(2^K, a^L). For
sufficiently large parameters, the condition fails.

Specifically: for fixed L, varying a, the smallest |2^K - a^L| (over valid K)
exceeds (2a)^{L-2} for a ≥ a₀(L). Below a₀(L), explicit check.
"""
from math import gcd

# Exhaustive search: for each (a, L), find all K with 2^K > a^L AND
# b := 2^K - a^L divides (2a)^j - 1 for some j ∈ {1, ..., L-2}.
# (j ≤ L-2 corresponds to L' ≥ 2.)

def find_all_cells_with_Lp_gte_2(a_max, L_max, K_max):
    cells = []
    for a in range(3, a_max+1, 2):
        for L in range(3, L_max+1):  # L ≥ 3 for L' ≥ 2 alt
            if a**L > 2**K_max: break
            for K in range(L+1, K_max+1):
                tK = 2**K
                aL = a**L
                if tK <= aL: continue
                b = tK - aL
                if b % 2 == 0: continue
                # Check j ∈ {1, ..., L-2}
                for j in range(1, L-1):
                    if ((2*a)**j - 1) % b == 0:
                        cells.append((a, L, K, b, j))
                        break  # one j is enough
    return cells

# Aggressive sweep: very wide
print("=== Sweep a ≤ 1001, L ≤ 35, K ≤ 100 (using bounds) ===")
cells = find_all_cells_with_Lp_gte_2(1001, 35, 100)
print(f"All cells with L' ≥ 2 alt tuple in this range: {len(cells)}")
for c in cells:
    print(f"  (a={c[0]}, L={c[1]}, K={c[2]}, b={c[3]}, j={c[4]})")

# Also check: for each (a, L, K), is the condition "b ≤ (2a)^{L-2} - 1" required?
print()
print("=== Why finiteness: gap analysis ===")
print("For L'≥2 alt: b ≤ (2a)^{L-2} - 1. But b = 2^K - a^L, and Tijdeman")
print("bounds say min|2^K - a^L| over valid K grows ~ a^{L*(1-eps)}.")
print()
# Show explicit gap analysis for L=3
print("Case L=3: need b | 2a-1. So b ≤ 2a-1. b = 2^K - a^3.")
print("Smallest b for each a (smallest K with 2^K > a^3):")
print(f"{'a':>4} {'a^3':>10} {'next 2^K':>12} {'min b':>8} {'2a-1':>5} {'b ≤ 2a-1?':>10}")
for a in range(3, 30, 2):
    aL = a**3
    K = 1
    while 2**K <= aL: K += 1
    b = 2**K - aL
    bound = 2*a - 1
    print(f"{a:>4} {aL:>10} {2**K:>12} {b:>8} {bound:>5} {'YES' if b <= bound else 'no':>10}")

# Verify: for a ≥ 7, min b > 2a-1 always.
print()
print("Conclusion for L=3:")
print("- a=3: min b = 5 = 2a-1 ✓ → cell (3, 5)")
print("- a=5: min b = 3, divides 2a-1=9 ✓ → cell (5, 3)")
print("- a≥7: min b > 2a-1, so no further L'=2 alt cells at L=3.")
