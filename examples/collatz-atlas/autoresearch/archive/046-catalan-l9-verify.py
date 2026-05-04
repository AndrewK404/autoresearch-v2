"""Verify L=9 in Catalan family: (3, 113213) should have 1430 cycles at length 26."""
import sys

a = 3
L = 9
K = 2*L - 1  # = 17
b = 2**K - 3**L  # = 131072 - 19683 = 111389... let me compute
print(f"L={L}, K={K}")
print(f"2^{K} = {2**K}")
print(f"3^{L} = {3**L}")
print(f"b = 2^K - 3^L = {2**K - 3**L}")

b = 2**K - 3**L
print(f"b={b}")

# Catalan number C_{L-1} = C_8 = 1430
from math import comb
catalan = comb(2*L-2, L-1) // L
print(f"Predicted: C_{L-1} = {catalan} cycles at length K={K}")

# Now verify by sweep up to S
def T(n, a, b):
    return n // 2 if n % 2 == 0 else a*n + b

# We expect cycles of length 17 only (the primary family).
# To find them: enumerate all compositions of K=17 into L=9 positive parts (k_1,...,k_L).
# n_0 = S(k) where S is the cycle-equation sum.
# But more simply: just simulate and find cycles up to bound.

# Use suffix memoization
S_max = 200000
print(f"Sweep S={S_max}...")

seen = {}  # n -> trajectory_id when we last saw it
cycle_id_of = {}
cycles_found = []  # list of (length, members frozen set)
trajectory_visited = {}

def find_cycle_from(start, S_max, a, b):
    """Run trajectory; if it cycles, return the cycle list."""
    path = []
    seen_local = {}
    n = start
    steps = 0
    while steps < 100000:
        if n > S_max * 100:  # too big
            return None
        if n in seen_local:
            idx = seen_local[n]
            return path[idx:]
        seen_local[n] = steps
        path.append(n)
        n = T(n, a, b)
        steps += 1
    return None

# Find unique cycles by trying many starting points
unique_cycles = set()  # frozensets

# Start with small odd numbers and divisors
# Actually, easier: enumerate compositions and compute n_0
from itertools import product

# Compositions of K=17 into L=9 positive parts
# k_1 + k_2 + ... + k_9 = 17, each k_i >= 1
# Equivalent: j_i = k_i - 1 >= 0, sum j_i = 17 - 9 = 8

# Number = C(17-1, 9-1) = C(16, 8) = 12870 compositions

# For each, compute S(k) = sum_{i=1}^{L} a^{L-i} * 2^{k_i + k_{i+1} + ... + k_{i-1} but that's the cycle sum}
# Per C-011: n_0 * (2^K - a^L) = b * S(k)
# With m=1: n_0 = S(k)
# S(k) for cycle (k_1,...,k_L): start at n_0, apply a*n+b, then divide by 2^{k_1}, then a*n+b, etc.
# After unrolling: n_0 * 2^K = a^L * n_0 + b*S(k)
# where S(k) = sum_{i=0}^{L-1} a^{L-1-i} * 2^{k_1 + ... + k_i}
# (with k_0 = 0 so first term is a^{L-1} * 2^0 = a^{L-1})

def compositions(K, L):
    """All compositions of K into L positive parts."""
    if L == 1:
        if K >= 1:
            yield (K,)
        return
    for first in range(1, K - L + 2):
        for rest in compositions(K - first, L - 1):
            yield (first,) + rest

def S_value(k_tuple, a, L):
    s = 0
    cum = 0  # cumulative k
    for i in range(L):
        s += a**(L-1-i) * 2**cum
        cum += k_tuple[i]
    return s

n0_values = set()
for k in compositions(K, L):
    s = S_value(k, a, L)
    # n_0 = s when m=1
    # Verify it's odd
    if s % 2 == 0:
        continue  # shouldn't happen
    n0_values.add(s)

print(f"Distinct n_0 values from compositions: {len(n0_values)}")

# Now, each cycle is represented L times (once per starting position in the cycle).
# So distinct cycles = len(n0_values) / L (when no rotation symmetry, gcd(K,L)=1)
# But actually, n_0 values that belong to the SAME cycle are exactly the L members.
# Let's verify by tracing.

cycle_reps = set()  # frozenset of cycle members
for n0 in sorted(n0_values):
    trace = find_cycle_from(n0, b * 100, a, b)
    if trace is None:
        continue
    fs = frozenset(trace)
    cycle_reps.add(fs)

print(f"Distinct cycles: {len(cycle_reps)}")
# Each should have length K=17
lengths = set(len(c) for c in cycle_reps)
print(f"Cycle lengths: {lengths}")
print(f"Predicted Catalan {catalan} matches actual {len(cycle_reps)}: {catalan == len(cycle_reps)}")
