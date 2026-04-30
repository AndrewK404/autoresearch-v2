"""Check whether 2240-cap and 5040-cap can be extended."""
import itertools, sys, time
sys.path.insert(0, "problem")
from priority import priority

def build_and_extend(n):
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
    print(f"n={n}: cap size={len(cap)}", flush=True)
    cap_set = set(cap)

    # Number of unforbidden non-cap elements
    unforb_outside = [e for e in elements if e not in forb]
    print(f"  unforbidden outside cap: {len(unforb_outside)}", flush=True)

    # Check addable
    t0 = time.time()
    addable = []
    for ei, e in enumerate(unforb_outside):
        if time.time() - t0 > 60:
            print(f"  checked {ei}/{len(unforb_outside)} in 60s", flush=True)
            break
        ok = True
        for u in cap:
            v = tuple((-ui - ei2) % 3 for ui, ei2 in zip(u, e))
            if v in cap_set and v != u and v != e:
                ok = False; break
        if ok:
            addable.append(e)
            if len(addable) >= 5: break
    print(f"  addable: {len(addable)}", flush=True)
    return cap, addable

print("=== n=10 ===")
build_and_extend(10)
print("\n=== n=11 ===")
build_and_extend(11)
