"""Local-search style for 112-cap at n=6."""
import itertools, random, time
import numpy as np
import sys

n = 6
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n

# Precompute third-point table
arr = np.array(elements, dtype=np.int8)
all_third = (-arr[:, None, :] - arr[None, :, :]) % 3
powers = 3 ** np.arange(n - 1, -1, -1, dtype=np.int64)
THIRD = (all_third * powers).sum(axis=2).astype(np.int32)
print(f"Precomputed THIRD: {THIRD.shape}", flush=True)

def build_cap_from_priority(priority_arr):
    """priority_arr: 1D array of priorities for each element index."""
    order = np.argsort(-priority_arr, kind='stable')
    cap = []
    blocked = np.zeros(TOTAL, dtype=bool)
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[THIRD[u, e]] = True
        cap.append(int(e))
        blocked[e] = True
    return cap

def is_cap(s):
    sset = set(s)
    s_list = list(s)
    for i in range(len(s_list)):
        for j in range(i+1, len(s_list)):
            if THIRD[s_list[i], s_list[j]] in sset:
                return False
    return True

# SLS: start with 96-cap, then iteratively do: pick random "non-cap" element,
# add it, compute conflicts, remove all conflicted elements, repeat.
def sls(initial_cap, time_limit=60, target=112):
    cap_set = set(initial_cap)
    best = len(cap_set)
    best_cap = list(cap_set)
    rng = random.Random(time.time())
    t0 = time.time()
    iters = 0
    while time.time() - t0 < time_limit:
        iters += 1
        if len(cap_set) >= target:
            return list(cap_set), iters
        # pick a non-cap element
        non_cap = [e for e in range(TOTAL) if e not in cap_set]
        if not non_cap:
            break
        new = rng.choice(non_cap)
        # find conflicts: cap members u, v such that THIRD[u, v] = new (form 3-AP through new)
        cap_list = list(cap_set)
        conflicts = []  # cap members involved in any conflict
        for i in range(len(cap_list)):
            u = cap_list[i]
            # for each v, if THIRD[u, v] = new and v in cap, conflict
            # equivalently: v = THIRD[u, new] (since THIRD is symmetric/algebraic)
            v = THIRD[u, new]
            if v in cap_set and v != u and v != new:
                conflicts.append(u)
                # don't break — but we need only need ONE conflict pair
                # actually: a 3-AP is (u, v, new) — adding new creates 3-AP iff
                # there exist u, v in cap with THIRD[u, v] = new
                break
        if not conflicts:
            # no conflict — add!
            cap_set.add(new)
        else:
            # remove conflicting cap member, add new
            cap_set.discard(conflicts[0])
            cap_set.add(new)
        # Sometimes also try to expand greedily
        if iters % 50 == 0:
            cap_list = list(cap_set)
            # check if cap is valid; also greedy-fill
            blocked = np.zeros(TOTAL, dtype=bool)
            for x in cap_list:
                blocked[x] = True
            for i in range(len(cap_list)):
                for j in range(i+1, len(cap_list)):
                    blocked[THIRD[cap_list[i], cap_list[j]]] = True
            order = list(range(TOTAL))
            rng.shuffle(order)
            for e in order:
                if blocked[e]: continue
                for u in cap_list:
                    blocked[THIRD[u, e]] = True
                cap_list.append(e)
                blocked[e] = True
            if len(cap_list) > best and is_cap(cap_list):
                best = len(cap_list)
                best_cap = list(cap_list)
                print(f"  [SLS iter {iters}] NEW BEST {best}", flush=True)
                if best >= target:
                    return cap_list, iters
            cap_set = set(cap_list)
    return best_cap, iters

# Build initial 96-cap
def cap_c2(t):
    arr = np.array([abs(sum(1 for x in elements[e] if x == 2) - t) for e in range(TOTAL)])
    return build_cap_from_priority(-arr.astype(np.float64))

cap_init = cap_c2(2)
print(f"Initial cap (c2=2): {len(cap_init)}", flush=True)
assert is_cap(cap_init)

# Run SLS
print("Running SLS...", flush=True)
best_cap, iters = sls(cap_init, time_limit=60)
print(f"SLS best: {len(best_cap)} in {iters} iters", flush=True)

# More attempts: random restart greedy
print("\nMassive random restart greedy...", flush=True)
best = len(best_cap)
t0 = time.time()
seed = 0
while time.time() - t0 < 120:
    seed += 1
    rng = random.Random(seed)
    order = list(range(TOTAL))
    rng.shuffle(order)
    cap = []
    blocked = np.zeros(TOTAL, dtype=bool)
    for e in order:
        if blocked[e]: continue
        for u in cap:
            blocked[THIRD[u, e]] = True
        cap.append(int(e))
        blocked[e] = True
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  seed {seed}: NEW BEST {best}", flush=True)
        if best >= 112:
            break

print(f"\nFinal best: {best}", flush=True)
if best > 96:
    with open(f"autoresearch/archive/037-cap-n6-{best}.txt", "w") as f:
        for e_idx in best_cap:
            f.write("".join(str(x) for x in elements[e_idx]) + "\n")
    print(f"Saved", flush=True)
