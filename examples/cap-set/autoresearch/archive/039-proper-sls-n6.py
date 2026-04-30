"""Proper SLS for cap-set at n=6 — strict cap-validity invariant."""
import itertools, random, time
import numpy as np

n = 6
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n

arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)

def greedy_fill(cap_set, order):
    """Given a valid cap_set (Python set of indices), greedily extend it
    by walking through `order`. Returns a NEW cap_set."""
    cap = list(cap_set)
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in cap: blocked[x] = True
    # mark third-points of all existing pairs
    for i in range(len(cap)):
        for j in range(i+1, len(cap)):
            blocked[THIRD[cap[i], cap[j]]] = True
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[THIRD[u, e]] = True
        cap.append(int(e))
        blocked[e] = True
    return cap

def is_cap_strict(cap_list):
    sset = set(cap_list)
    for i in range(len(cap_list)):
        for j in range(i+1, len(cap_list)):
            t = int(THIRD[cap_list[i], cap_list[j]])
            if t in sset and t != cap_list[i] and t != cap_list[j]:
                return False
    return True

# SLS: Maintain a valid cap. Move = remove K random + greedy refill with new order.
# Eval is fast — try many many trials.
best = 96
best_cap = None
t0 = time.time()
TIME_LIMIT = 360  # 6 minutes
trials = 0

# Initial good seed: c2=2 priority cap
c2_priority = -np.array([abs(sum(1 for x in elements[i] if x == 2) - 2) for i in range(TOTAL)])
order_init = list(np.argsort(-c2_priority, kind='stable'))
init_cap = greedy_fill(set(), order_init)
assert is_cap_strict(init_cap), f"init failed: {len(init_cap)}"
print(f"init c2=2 cap: {len(init_cap)}", flush=True)

# Multi-restart SLS
rng = random.Random(0)
while time.time() - t0 < TIME_LIMIT:
    trials += 1
    # random choice of starting cap
    start = list(init_cap) if best <= 96 else list(best_cap)
    # remove K random elements
    K = rng.choice([1, 2, 3, 5, 10, 15, 25, 50, 80])
    rng.shuffle(start)
    pruned = start[:-K]
    pruned_set = set(pruned)

    # random order for refill
    order = list(range(TOTAL))
    rng.shuffle(order)

    # priority bias for refill
    bias = trials % 5
    if bias == 0:
        order.sort(key=lambda e: -abs(sum(1 for x in elements[e] if x == 2) - 2))
    elif bias == 1:
        order.sort(key=lambda e: -abs(sum(1 for x in elements[e] if x == 2) - 3))
    elif bias == 2:
        order.sort(key=lambda e: rng.random())  # already shuffled
    elif bias == 3:
        order.sort(key=lambda e: -elements[e].count(0))

    # Filter order to those not in pruned_set
    cap = greedy_fill(pruned_set, order)

    if not is_cap_strict(cap):
        # bug somewhere
        print(f"  trial {trials}: INVALID after fill ({len(cap)})", flush=True)
        continue

    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trials}: NEW BEST {best} (K={K}, bias={bias})", flush=True)
        if best >= 112: break

    if trials % 1000 == 0:
        print(f"  trial {trials}: {time.time()-t0:.0f}s elapsed, best={best}", flush=True)

print(f"\n=== best at n=6: {best} ({trials} trials, {time.time()-t0:.0f}s) ===", flush=True)
if best > 96:
    with open(f"autoresearch/archive/039-cap-n6-{best}.txt", "w") as f:
        for e_idx in best_cap:
            f.write("".join(str(x) for x in elements[e_idx]) + "\n")
    print(f"Saved", flush=True)
