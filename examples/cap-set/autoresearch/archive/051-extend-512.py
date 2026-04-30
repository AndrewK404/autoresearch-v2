"""Try to extend the 512-cap at n=8 or 1082-cap at n=9."""
import itertools, sys, time, random
import numpy as np
sys.path.insert(0, "problem")
from priority import priority, _priority_n8

n = 8
elements = list(itertools.product(range(3), repeat=n))
elements.sort(key=lambda e: _priority_n8(e), reverse=True)
cap, forb = [], set()
for e in elements:
    if e in forb: continue
    for u in cap:
        c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap.append(e)
    forb.add(e)
print(f"512-cap: {len(cap)}", flush=True)

# Check maximality
cap_set = set(cap)
unforb_outside = [e for e in elements if e not in forb]
print(f"unforbidden outside: {len(unforb_outside)}")

# K-out-K+1-in: remove K random, fill greedy with random order
TOTAL = 3**n
arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)

# index in elements list
EL_TO_IDX = {tuple(elements[i]): i for i in range(TOTAL)}
cap_idx = [EL_TO_IDX[e] for e in cap]
print(f"cap as indices: {len(cap_idx)}")

best = 512; best_cap = list(cap_idx)
t0 = time.time()
TIME_LIMIT = 120

for trial in range(100000):
    if time.time() - t0 > TIME_LIMIT: break
    K = random.choice([1, 2, 3, 5, 10, 25, 100])
    rng = random.Random(trial)
    rng.shuffle(best_cap)
    pruned = best_cap[:-K]
    pruned_set = set(pruned)
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in pruned: blocked[x] = True
    cap_list = list(pruned)
    for i in range(len(cap_list)):
        for j in range(i+1, len(cap_list)):
            blocked[THIRD[cap_list[i], cap_list[j]]] = True
    order = list(range(TOTAL))
    rng.shuffle(order)
    if trial % 3 == 0:
        order.sort(key=lambda e: -_priority_n8(elements[e]))

    for e in order:
        if blocked[e]: continue
        for u in cap_list:
            blocked[THIRD[u, e]] = True
        cap_list.append(int(e))
        blocked[e] = True
    if len(cap_list) > best:
        best = len(cap_list)
        best_cap = cap_list
        print(f"  trial {trial}: NEW BEST {best}", flush=True)
    if trial % 1000 == 0:
        print(f"  trial {trial}, t={time.time()-t0:.0f}s, best={best}", flush=True)

print(f"\nFinal best n=8: {best}")
