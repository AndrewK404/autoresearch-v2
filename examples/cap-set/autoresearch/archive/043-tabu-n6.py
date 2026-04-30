"""Tabu search / better local search for cap at n=6."""
import itertools, random, time
import numpy as np

n = 6
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n

arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)

# Move = swap one cap-out for one cap-in (or remove K, add K+1).
# Maintain conflict structure: each non-cap element e has a set of "blocking pairs"
# (a, b) ⊂ cap with THIRD[a, b] = e. e is addable iff blocking pairs == empty.
# Each cap element a has a set of "conflict elements" e (non-cap) such that adding e
# would conflict.

# We want to find a sequence of swaps that eventually grow.

def initial_cap():
    """c2=2 priority cap (96)"""
    pri = -np.array([abs((arr[i] == 2).sum() - 2) for i in range(TOTAL)], dtype=float)
    order = np.argsort(-pri, kind='stable')
    cap, blocked = [], np.zeros(TOTAL, dtype=bool)
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[THIRD[u, e]] = True
        cap.append(int(e))
        blocked[e] = True
    return cap

def cap_blockers(cap):
    """For each non-cap e, set of blocking pairs (a, b) where a, b in cap, THIRD[a,b]=e."""
    cap_set = set(cap)
    block_pairs = {e: [] for e in range(TOTAL) if e not in cap_set}
    for i in range(len(cap)):
        for j in range(i+1, len(cap)):
            t = int(THIRD[cap[i], cap[j]])
            if t not in cap_set:
                block_pairs[t].append((cap[i], cap[j]))
    return block_pairs

def cap_max_extend(cap):
    cap_set = set(cap)
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in cap_set: blocked[x] = True
    cap_list = list(cap)
    for i in range(len(cap_list)):
        for j in range(i+1, len(cap_list)):
            blocked[THIRD[cap_list[i], cap_list[j]]] = True
    return cap_list, blocked

# k-out-(k+1)-in search
def k_swap_search(initial, time_limit=180, target=112):
    cap = list(initial)
    best = len(cap)
    best_cap = list(cap)
    t0 = time.time()
    rng = random.Random(0)

    while time.time() - t0 < time_limit:
        # Random k
        k = rng.choice([1, 2, 3, 4, 5])
        # Remove k random
        rng.shuffle(cap)
        removed = cap[:k]
        kept = cap[k:]
        kept_set = set(kept)

        # Compute blockers for each non-kept element
        blocked = np.zeros(TOTAL, dtype=bool)
        for x in kept_set: blocked[x] = True
        for i in range(len(kept)):
            for j in range(i+1, len(kept)):
                blocked[THIRD[kept[i], kept[j]]] = True

        # Greedy refill using random order with priority bias
        order = list(range(TOTAL))
        if rng.random() < 0.3:
            order.sort(key=lambda e: -abs((arr[e] == 2).sum() - 2))
        elif rng.random() < 0.3:
            rng.shuffle(order)
            order.sort(key=lambda e: -abs((arr[e] == 2).sum() - 3))
        else:
            rng.shuffle(order)

        new_cap = list(kept)
        for e in order:
            if blocked[e]: continue
            for u in new_cap:
                blocked[THIRD[u, e]] = True
            new_cap.append(int(e))
            blocked[e] = True

        if len(new_cap) > best:
            best = len(new_cap)
            best_cap = new_cap
            print(f"  [{time.time()-t0:.0f}s] NEW BEST {best}", flush=True)
            cap = list(new_cap)
            if best >= target: return best_cap
        else:
            # Sometimes accept worse to escape
            if len(new_cap) >= len(cap) - 1 and rng.random() < 0.05:
                cap = list(new_cap)

    return best_cap

print("Initial...", flush=True)
cap = initial_cap()
print(f"init: {len(cap)}", flush=True)

# Multi-start
best = len(cap)
best_cap = list(cap)
for restart in range(10):
    res = k_swap_search(cap if restart == 0 else best_cap, time_limit=60, target=112)
    if len(res) > best:
        best = len(res)
        best_cap = res
        print(f"--- restart {restart}: best now {best}", flush=True)
    if best >= 112: break

print(f"\nFinal: {best}", flush=True)
if best > 96:
    with open(f"autoresearch/archive/043-cap-n6-{best}.txt", "w") as f:
        for e_idx in best_cap:
            f.write("".join(str(x) for x in elements[e_idx]) + "\n")
    print("Saved.", flush=True)
