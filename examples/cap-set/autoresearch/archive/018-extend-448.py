"""Check whether the 448-cap is maximal."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load 448 cap
n = 8
def get_448_cap():
    elements = list(itertools.product(range(3), repeat=n))
    def priority(e, n):
        c2 = sum(1 for x in e if x == 2)
        return -abs(c2 - 3)
    elements.sort(key=lambda e: priority(e, n), reverse=True)
    cap_set = []
    forbidden = set()
    for e in elements:
        if e in forbidden:
            continue
        for u in cap_set:
            c = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
            forbidden.add(c)
        cap_set.append(e)
        forbidden.add(e)
    return cap_set

cap = get_448_cap()
cap_set = set(cap)
print(f"Initial cap size: {len(cap)}")

# Check forbidden set: for each non-cap element, can it extend?
forbidden = set()
for x, y in itertools.combinations(cap, 2):
    z = tuple((3 - xi - yi) % 3 for xi, yi in zip(x, y))
    forbidden.add(z)
forbidden |= cap_set

remaining = [e for e in itertools.product(range(3), repeat=n) if e not in forbidden]
print(f"Non-forbidden, non-cap elements: {len(remaining)}")

# If any of these are addable
addable = []
for e in remaining:
    ok = True
    for u in cap:
        v = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
        if v in cap_set:
            ok = False
            break
    if ok:
        addable.append(e)

print(f"Addable elements: {len(addable)}")
if addable:
    print(f"  e.g.: {addable[:5]}")

# How many distinct caps of size > 448 can be built starting from any prefix of cap?
# Try: drop k elements from cap, see if more elements become addable
import random
random.seed(0)
print(f"\n--- removing elements from 448-cap and re-greedy ---")
for k in [1, 5, 10, 20, 50]:
    best_after = 0
    for trial in range(5):
        c0 = cap[:]
        random.shuffle(c0)
        kept = c0[:-k]
        kset = set(kept)
        forb = set(kept)
        for x, y in itertools.combinations(kept, 2):
            z = tuple((3 - xi - yi) % 3 for xi, yi in zip(x, y))
            forb.add(z)
        # Try every element to extend
        elements = list(itertools.product(range(3), repeat=n))
        random.shuffle(elements)
        cap_new = list(kept)
        forb_new = set(forb)
        for e in elements:
            if e in forb_new:
                continue
            for u in cap_new:
                c = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
                forb_new.add(c)
            cap_new.append(e)
            forb_new.add(e)
        best_after = max(best_after, len(cap_new))
    print(f"  k={k} dropped, best after re-greedy: {best_after}")
