"""Re-run SLS at n=8 and dump+verify the cap."""
import itertools, sys, time, random
import numpy as np
sys.path.insert(0, "problem")
from priority import _priority_n8

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

TOTAL = 3**n
arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)
EL_TO_IDX = {elements[i]: i for i in range(TOTAL)}
cap_idx = [EL_TO_IDX[e] for e in cap]

best = 512; best_cap = list(cap_idx)
t0 = time.time()

for trial in range(20000):
    if time.time() - t0 > 60: break
    K = random.choice([1, 2, 3, 5, 10, 25, 100])
    rng = random.Random(trial)
    pool = list(best_cap)
    rng.shuffle(pool)
    pruned = pool[:-K]
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

print(f"\nfound size: {best}")
print("\nVERIFY:", flush=True)
# Convert to elements
cap_elements = [elements[i] for i in best_cap]
sset = set(cap_elements)
print(f"distinct: {len(sset)}, total: {len(cap_elements)}")
viol = 0
for x, y in itertools.combinations(cap_elements, 2):
    z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
    if z in sset and z != x and z != y:
        viol += 1
        if viol <= 3:
            print(f"  AP: {x}, {y}, {z}")
print(f"violations: {viol}")

# Manual verify with the official solve.py logic
print("\n--- official-style verify ---")
# Run the official verify
def verify_cap_set(cap_set, n):
    s = set(cap_set)
    if len(s) != len(cap_set):
        return False, "duplicate"
    for x, y in itertools.combinations(cap_set, 2):
        z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
        if z in s and z != x and z != y:
            return False, f"AP {x}, {y}, {z}"
    return True, "ok"

ok, msg = verify_cap_set(cap_elements, n)
print(f"verify: {ok}, msg: {msg}")
