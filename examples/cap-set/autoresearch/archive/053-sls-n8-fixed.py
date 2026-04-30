"""SLS at n=8 with FIXED indexing — try to break 512."""
import itertools, sys, time, random
import numpy as np
sys.path.insert(0, "problem")
from priority import _priority_n8

n = 8
# Use itertools order WITHOUT sorting
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3**n
arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
# Now THIRD[i, j] = canonical itertools index of -elements[i] - elements[j]
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)

# Build initial 512-cap using FunSearch priority on itertools-ordered elements
priorities = np.array([_priority_n8(e) for e in elements])
order = np.argsort(-priorities, kind='stable')
cap_idx = []
blocked = np.zeros(TOTAL, dtype=bool)
for e in order:
    if blocked[e]: continue
    for u in cap_idx:
        blocked[THIRD[u, e]] = True
    cap_idx.append(int(e))
    blocked[e] = True
print(f"512-cap (via THIRD): {len(cap_idx)}")
assert len(cap_idx) == 512

# Verify
def verify(cap_idx):
    sset = set(cap_idx)
    for i in range(len(cap_idx)):
        for j in range(i+1, len(cap_idx)):
            t = int(THIRD[cap_idx[i], cap_idx[j]])
            if t in sset and t != cap_idx[i] and t != cap_idx[j]:
                return False
    return True

assert verify(cap_idx), "init invalid"
print("init verified", flush=True)

best = 512; best_cap = list(cap_idx)
t0 = time.time()
TIME_LIMIT = 240

for trial in range(100000):
    if time.time() - t0 > TIME_LIMIT: break
    K = random.choice([1, 2, 3, 5, 10, 25, 100, 200])
    rng = random.Random(trial)
    pool = list(best_cap)
    rng.shuffle(pool)
    pruned = pool[:-K]
    blocked = np.zeros(TOTAL, dtype=bool)
    for x in pruned: blocked[x] = True
    cap_list = list(pruned)
    for i in range(len(cap_list)):
        for j in range(i+1, len(cap_list)):
            blocked[THIRD[cap_list[i], cap_list[j]]] = True

    fill_order = list(range(TOTAL))
    rng.shuffle(fill_order)
    if trial % 4 == 0:
        fill_order.sort(key=lambda e: -priorities[e])

    for e in fill_order:
        if blocked[e]: continue
        for u in cap_list:
            blocked[THIRD[u, e]] = True
        cap_list.append(int(e))
        blocked[e] = True

    if len(cap_list) > best:
        if verify(cap_list):
            best = len(cap_list)
            best_cap = cap_list
            print(f"  trial {trial}: NEW BEST {best} (verified)", flush=True)
        else:
            print(f"  trial {trial}: {len(cap_list)} but FAILED verify", flush=True)
    if trial % 500 == 0:
        print(f"  trial {trial}, t={time.time()-t0:.0f}s, best={best}", flush=True)

print(f"\nfinal n=8 best: {best}")
if best > 512:
    print(f"!!! WORLD RECORD POTENTIAL !!!")
    with open(f"autoresearch/archive/053-cap-n8-{best}.txt", "w") as f:
        for i in best_cap:
            f.write("".join(str(x) for x in elements[i]) + "\n")
