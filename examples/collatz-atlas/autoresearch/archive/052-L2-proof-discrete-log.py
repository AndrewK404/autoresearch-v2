"""
L'=2 case proof attempt.

For an alt tuple (L'=2, K'=K+j with j=L-2≥1) of primary (a, L≥3, K, b):
- m' = 2^{L-2} + a^2 · q with q = ((2a)^{L-2} - 1)/b.
- 2^{K'} ≡ a^2 (mod m'), i.e., (2^{K'/2})^2 ≡ a^2 (mod m').

So 2^{K'/2} is a square root of a^2 mod m'. We want: no primitive k_1
∈ [1, K'-1] \ {K'/2 if K' even} satisfies 2^{k_1} ≡ -a (mod m').

Sub-claim: ord_{m'}(2) > K' - 2 in our setup, so the discrete log
(if it exists) has at most ONE solution in [1, K'-1].

Verification: for each alt tuple in our 22731-cell sweep, check
ord_{m'}(2) and its relationship to K'.
"""
from math import gcd

def ord_mod(g, m):
    """Multiplicative order of g modulo m, or None if gcd(g, m) ≠ 1."""
    if gcd(g, m) != 1: return None
    o = 1
    cur = g % m
    while cur != 1:
        cur = (cur * g) % m
        o += 1
        if o > m * 2: return None
    return o

# Alt tuple cases (from 22731-cell sweep; only 3 cells)
cases = [
    # (a, L, K, b, j, m', L', K')
    (3, 3, 5, 5, 1, 11, 2, 6),
    (5, 3, 7, 3, 1, 77, 2, 8),
    # L'=1 cases (already handled in closed form):
    (3, 3, 5, 5, 2, 25, 1, 7),
    (5, 3, 7, 3, 2, 169, 1, 9),
    (11, 2, 7, 7, 1, 35, 1, 8),
]

print(f"{'cell':>10} {'L,K':>5} {'j':>2} {'Lp,Kp':>6} {'mp':>5} {'ord_2':>6} {'Kp-1':>5} {'solns':>20}")
print("-" * 80)
for (a, L, K, b, j, mp, Lp, Kp) in cases:
    o = ord_mod(2, mp)
    target = (-a) % mp  # need 2^k ≡ -a (mod m')
    # Find k in [1, K'-1] with 2^k ≡ target (mod mp)
    solns = []
    cur = 2 % mp
    for k in range(1, Kp):
        if cur == target:
            solns.append(k)
        cur = (cur * 2) % mp
    # Filter primitive (k ≠ K'/2 if K' even)
    primitive_solns = [k for k in solns if not (Kp % 2 == 0 and k == Kp // 2)]
    note = f"all={solns}, primitive={primitive_solns}"
    if Lp != 2:
        note = "(L'=1, S=1, m'∤1 trivially)"
    print(f"({a},{b})    {L},{K}  {j:>2}  {Lp},{Kp}  {mp:>5}  {str(o):>10}  {Kp-1:>5}  {note}")
