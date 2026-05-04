"""
Structural analysis of L'=2 case: m' | S(k') ⟺ m' | (a + 2^{k_1})
⟺ 2^{k_1} ≡ -a (mod m').

For each cell with alternate L'=2 tuple, compute the discrete log (if it
exists) and check whether it lies in the valid primitive range
{1, ..., K'-1} \ {K'/2}.
"""
from math import gcd

def ord_mod(g, m):
    """Multiplicative order of g modulo m."""
    if gcd(g, m) != 1: return None
    o = 1
    cur = g % m
    while cur != 1:
        cur = (cur * g) % m
        o += 1
        if o > m: return None
    return o

def discrete_log(g, h, m):
    """Find smallest k >= 1 with g^k ≡ h (mod m), or None."""
    cur = g % m
    h = h % m
    for k in range(1, m + 2):
        if cur == h: return k
        cur = (cur * g) % m
        if k > 2 * m: return None
    return None

# For each cell with alt L'=2 tuple, compute the discrete log
# and check if it falls in primitive range.
# (a, primary L, primary K, b, alt L'=2, alt K', m')
cases = [
    (3, 3, 5, 5, 2, 6, 11),
    (5, 3, 7, 3, 2, 8, 77),
]

print("L'=2 case analysis: 2^{k_1} ≡ -a (mod m'); k_1 must be in [1, K'-1] \\ {K'/2}")
print()
for (a, L, K, b, Lp, Kp, mp) in cases:
    target = (-a) % mp
    o = ord_mod(2, mp)
    k1 = discrete_log(2, target, mp)
    primitive_range = [k for k in range(1, Kp) if k != Kp // 2 or Kp % 2 != 0]
    in_range = k1 in primitive_range if k1 else False
    print(f"  Cell (a={a}, b={b}), primary (L={L}, K={K}); alt (L'=2, K'={Kp}), m'={mp}")
    print(f"    Need: 2^k ≡ {target} (mod {mp}). Order of 2 mod {mp}: {o}.")
    print(f"    Smallest k: {k1}. Primitive range: {primitive_range}.")
    print(f"    In range? {in_range}.")
    if k1 is not None and o is not None:
        # All solutions: k1, k1+o, k1+2o, ...
        # Check any falls in primitive range
        all_solutions_in_range = [k for k in primitive_range if (k - k1) % o == 0]
        print(f"    All k in primitive range satisfying eq: {all_solutions_in_range}")
        # Check imprimitive (k = K'/2)
        if Kp % 2 == 0 and (Kp//2 - k1) % o == 0:
            print(f"    Imprimitive k=K'/2={Kp//2} satisfies eq (gives shorter cycle).")
    print()
