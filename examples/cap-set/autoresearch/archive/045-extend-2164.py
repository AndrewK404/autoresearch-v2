"""Check whether the 2164-cap at n=10 is maximal — can it be extended?"""
import itertools, sys, time
sys.path.insert(0, "problem")
from priority import priority

n = 10
print("Building 2164-cap...", flush=True)
elements = list(itertools.product(range(3), repeat=n))
elements.sort(key=lambda e: priority(e, n), reverse=True)

cap, forb = [], set()
for e in elements:
    if e in forb: continue
    for u in cap:
        c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap.append(e)
    forb.add(e)
print(f"cap size: {len(cap)}", flush=True)

cap_set = set(cap)
# How many elements are non-forbidden, non-cap?
non_cap = [e for e in itertools.product(range(3), repeat=n) if e not in cap_set]
unforbidden_outside = [e for e in non_cap if e not in forb]
print(f"non-cap: {len(non_cap)}, unforbidden outside cap: {len(unforbidden_outside)}", flush=True)

# Check addable
addable = []
t0 = time.time()
for ei, e in enumerate(unforbidden_outside):
    if time.time() - t0 > 60: break
    ok = True
    for u in cap:
        v = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        if v in cap_set and v != u and v != e:
            ok = False
            break
    if ok:
        addable.append(e)

print(f"checked {ei+1} elements in {time.time()-t0:.0f}s, addable: {len(addable)}", flush=True)
if addable:
    print(f"  e.g. {addable[:5]}")
