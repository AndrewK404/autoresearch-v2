"""
Action 052: Sharpened Diophantine criterion for alternate-tuple existence.

For primary cell (a, b = 2^K - a^L) with m=1, an alternate (L', K') with
L'+K' = L+K and L' = L - j (j ∈ {1, ..., L-1}) exists iff:

    b | ((2a)^j - 1)

When this holds, the alternate multiplier is:

    m' = 2^j + a^{L-j} * q,  where q = ((2a)^j - 1) / b.

DERIVATION:
m'*b = 2^{K+j} - a^{L-j}
     = 2^j*(2^K) - a^{L-j}
     = 2^j*b + 2^j*a^L - a^{L-j}     (since 2^K = b + a^L)
     = 2^j*b + a^{L-j}*(2^j*a^j - 1)
     = 2^j*b + a^{L-j}*((2a)^j - 1)
=> (m' - 2^j)*b = a^{L-j}*((2a)^j - 1)
=> b | a^{L-j}*((2a)^j - 1).
Since gcd(b, a) = 1 (b = 2^K - a^L, a odd, gcd(2^K, a) = 1, so
gcd(b, a) = gcd(-a^L, a) = a^L... wait but a^L | b would give b ≥ a^L, but
b = 2^K - a^L < 2^K, possibly < a^L). Actually let me recheck.

gcd(b, a): b = 2^K - a^L. b mod a = 2^K mod a (since a^L ≡ 0 mod a).
2^K mod a is nonzero (gcd(2, a) = 1). So b mod a ≠ 0, hence gcd(b, a)
divides a but doesn't equal a. Since a may be composite, gcd(b, a) could
still be > 1. Wait gcd(b, a) divides any common factor.

Actually, let p be a prime dividing both b and a. Then p | a (so p is one
of a's prime factors), and p | b = 2^K - a^L ≡ 2^K (mod p) (since p | a).
But p | a and p odd (a odd), so gcd(p, 2) = 1, so 2^K mod p ≠ 0. So p ∤ b.

Therefore gcd(b, a) = 1.

So b | ((2a)^j - 1). ∎ (criterion direction).

The converse: given b | ((2a)^j - 1), set m' = 2^j + a^{L-j} * q. Then
m'*b = 2^j*b + a^{L-j}*((2a)^j - 1) = 2^{K+j} - a^{L-j} (by reversal).
So this m' is exactly (2^{K+j} - a^{L-j})/b, an integer ≥ 2 (when q ≥ 1).
"""
from math import gcd

def criterion_check(a, L, K):
    """For primary cell (a, b=2^K-a^L), enumerate alt tuples (L'=L-j, K'=K+j)
    using the criterion b | ((2a)^j - 1).
    Returns list of (j, q, m', L', K')."""
    b = 2**K - a**L
    if b <= 0 or b % 2 == 0: return []
    alts = []
    for j in range(1, L):  # j ∈ {1, ..., L-1}
        twoa_j = (2*a)**j
        if (twoa_j - 1) % b == 0:
            q = (twoa_j - 1) // b
            m_prime = 2**j + a**(L-j) * q
            alts.append((j, q, m_prime, L - j, K + j))
    return alts

# Verify criterion: sweep cells, compare against full divisor-check
def divisor_check_alts(a, L, K):
    """Old method: enumerate (L', K') with L'+K'=L+K, check b | (2^{K'}-a^{L'})."""
    b = 2**K - a**L
    if b <= 0 or b % 2 == 0: return []
    T = K + L
    alts = []
    for Lp in range(1, L):  # only L' < L (j > 0)
        Kp = T - Lp
        if Kp <= Lp: continue
        if 2**Kp <= a**Lp: continue
        val = 2**Kp - a**Lp
        if val % b == 0:
            mp = val // b
            alts.append((L - Lp, val // ((2*a)**(L-Lp) - 1) if ((2*a)**(L-Lp)-1) > 0 and ((2*a)**(L-Lp)-1) % b == 0 else None, mp, Lp, Kp))
    return alts

# Cross-validate
print("=== Criterion verification: a≤25, L≤8, K≤20 ===")
matches = 0
mismatches = 0
for a in range(3, 26, 2):
    for L in range(2, 9):
        for K in range(L+1, 21):
            crit = criterion_check(a, L, K)
            div = divisor_check_alts(a, L, K)
            crit_set = {(a[0], a[2]) for a in crit}  # j, m'
            div_set = {(L - dv[3], dv[2]) for dv in div}  # j=L-L', m'
            if crit_set == div_set:
                matches += 1
            else:
                mismatches += 1
                if mismatches <= 5:
                    print(f"MISMATCH a={a} L={L} K={K}: criterion={crit_set} divisor={div_set}")

print(f"\nCriterion matches divisor enumeration: {matches}, mismatches: {mismatches}")

# Now sweep widely for alt-tuple cells using the fast criterion
print("\n=== Wide sweep with criterion: a≤101, L≤16, K≤45 ===")
alt_cells = []
total = 0
for a in range(3, 102, 2):
    for L in range(2, 17):
        for K in range(L+1, 46):
            tK = 2**K
            aL = a**L
            if tK <= aL: continue
            b = tK - aL
            if b % 2 == 0: continue
            total += 1
            alts = criterion_check(a, L, K)
            if alts:
                alt_cells.append((a, L, K, b, alts))

print(f"Total m=1 cells: {total}")
print(f"Cells with alt tuples: {len(alt_cells)}")
print()
print("All alt-tuple cells:")
print(f"{'a':>3} {'L':>3} {'K':>3} {'b':>10} {'alts':<70}")
for (a, L, K, b, alts) in alt_cells:
    alt_str = "; ".join(f"j={j} L'={Lp} K'={Kp} m'={mp}" for (j, q, mp, Lp, Kp) in alts)
    print(f"{a:>3} {L:>3} {K:>3} {b:>10} {alt_str}")
