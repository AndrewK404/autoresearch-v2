"""Backtracking search for a 112-cap at n=6 with strong heuristics."""
import itertools, random, time
import numpy as np

n = 6
elements = list(itertools.product(range(3), repeat=n))
EL_TO_IDX = {e: i for i, e in enumerate(elements)}
IDX_TO_EL = elements
TOTAL = 3 ** n

# Precompute "third point" table: for each pair (i, j) with i < j, the index of the 3rd point on the line.
import numpy as np
arr = np.array(elements, dtype=np.int8)
# third(i,j) = (-elements[i] - elements[j]) % 3 → index
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3  # [N, N, n]
powers = 3 ** np.arange(n - 1, -1, -1)
all_third_idx = (all_third * powers).sum(axis=2)  # [N, N]
print(f"precomputed third-point table: {all_third_idx.shape}, dtype={all_third_idx.dtype}")

def find_extension_greedy(start_cap_idx, target):
    """Try to extend start_cap to a cap of size >= target."""
    cap = list(start_cap_idx)
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in cap:
        blocked[x] = True
    for i in range(len(cap)):
        for j in range(i + 1, len(cap)):
            blocked[all_third_idx[cap[i], cap[j]]] = True
    # Now greedily add
    order = list(range(TOTAL))
    order.sort(key=lambda e: -abs(sum(1 for x in IDX_TO_EL[e] if x == 2) - 2))
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[all_third_idx[u, e]] = True
        cap.append(e)
        blocked[e] = True
        if len(cap) >= target:
            break
    return cap

# Try restart with various seeds
print("Running 'shrink-then-greedy' with priority-based initial seed...")
# Start from c2=2 priority cap (96)
best = 96
best_cap_idx = None
seed_order = list(range(TOTAL))
seed_order.sort(key=lambda e: -abs(sum(1 for x in IDX_TO_EL[e] if x == 2) - 2))
cap_init = []
blocked = np.zeros(TOTAL, dtype=bool)
for e in seed_order:
    if blocked[e]: continue
    for u in cap_init:
        blocked[all_third_idx[u, e]] = True
    cap_init.append(e)
    blocked[e] = True
print(f"baseline c2=2 cap: {len(cap_init)}")

# Now try removing K elements and re-greedying with different orders
import random
random.seed(0)
t0 = time.time()
for trial in range(2000):
    if time.time() - t0 > 120: break
    K = random.choice([1, 2, 3, 5, 10, 20])
    pruned = cap_init[:]
    random.shuffle(pruned)
    pruned = pruned[:-K]
    # Re-greedy with shuffled order on the rest
    cap = pruned[:]
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in cap:
        blocked[x] = True
    for i in range(len(cap)):
        for j in range(i + 1, len(cap)):
            blocked[all_third_idx[cap[i], cap[j]]] = True
    rng = random.Random(trial)
    order = list(range(TOTAL))
    rng.shuffle(order)
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[all_third_idx[u, e]] = True
        cap.append(e)
        blocked[e] = True
    if len(cap) > best:
        best = len(cap)
        best_cap_idx = cap
        print(f"  trial {trial}, K={K}: NEW BEST {best}")
        if best >= 112: break

print(f"\nBest after shrink-then-greedy: {best}  (time {time.time()-t0:.0f}s)")

# Now try BACKTRACKING with branch-and-bound
print("\n=== Backtracking search ===")
# Order elements by priority (c2=2 ish) first
order = list(range(TOTAL))
order.sort(key=lambda e: -abs(sum(1 for x in IDX_TO_EL[e] if x == 2) - 2))

best_bt = 96
import sys
sys.setrecursionlimit(200000)

t0 = time.time()
TIME_LIMIT = 300

def backtrack(cap_idx, blocked, candidates, depth=0):
    global best_bt
    if time.time() - t0 > TIME_LIMIT:
        return
    sz = len(cap_idx)
    if sz > best_bt:
        best_bt = sz
        print(f"  depth {depth}, NEW BEST {sz}")
    # Upper bound: sz + |unblocked candidates|
    free = [c for c in candidates if not blocked[c]]
    if sz + len(free) <= best_bt:
        return
    if not free:
        return
    # Pick first 3 candidates and branch
    for i, e in enumerate(free[:3]):
        new_cap = cap_idx + [e]
        new_blocked = blocked.copy()
        for u in cap_idx:
            new_blocked[all_third_idx[u, e]] = True
        new_blocked[e] = True
        new_candidates = free[i+1:]
        backtrack(new_cap, new_blocked, new_candidates, depth + 1)
        if time.time() - t0 > TIME_LIMIT: break
        if best_bt >= 112: break
    # Also try not picking
    if time.time() - t0 < TIME_LIMIT and best_bt < 112:
        backtrack(cap_idx, blocked, [c for c in candidates if c != free[0]], depth + 1)

# Don't run backtracking — too expensive. Just report best from priorities.
print(f"\nFinal best: {best}")
