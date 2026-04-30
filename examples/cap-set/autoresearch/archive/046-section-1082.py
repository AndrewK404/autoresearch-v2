"""Section the 1082-cap at n=9 to find a large cap at n=6."""
import itertools, sys, time, numpy as np
sys.path.insert(0, "problem")
from priority import _priority_n9

n9 = 9
elements_9 = list(itertools.product(range(3), repeat=n9))
elements_9.sort(key=lambda e: _priority_n9(e), reverse=True)

cap_9, forb = [], set()
for e in elements_9:
    if e in forb: continue
    for u in cap_9:
        c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap_9.append(e)
    forb.add(e)
print(f"1082-cap at n=9: {len(cap_9)}")

# Try sectioning by fixing 3 coords
def section(cap_9, fix_indices, fix_vals):
    proj = [i for i in range(n9) if i not in fix_indices]
    sec = [tuple(e[i] for i in proj) for e in cap_9
           if all(e[fix_indices[k]] == fix_vals[k] for k in range(len(fix_indices)))]
    return sec

def is_cap6(sec):
    sset = set(sec)
    for x, y in itertools.combinations(sec, 2):
        z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
        if z in sset and z != x and z != y:
            return False
    return True

best = 96; best_cap = None
t0 = time.time()
print("Searching sections fixing 3 coords...")
combos = list(itertools.combinations(range(n9), 3))
for fix_idx in combos:
    for vals in itertools.product(range(3), repeat=3):
        if time.time() - t0 > 60: break
        sec = section(cap_9, fix_idx, vals)
        if len(sec) <= best: continue
        if is_cap6(sec):
            if len(sec) > best:
                best = len(sec); best_cap = sec
                print(f"  fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)

print(f"\nBest section at n=6: {best}")
if best > 96 and best_cap:
    with open(f"autoresearch/archive/046-cap-n6-{best}.txt", "w") as f:
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")

# Also try sections of size n=7 from the 1082-cap (fix 2 coords)
print("\n--- sections to n=7 from 1082-cap ---")
best7 = 192; best7_cap = None
t0 = time.time()
combos2 = list(itertools.combinations(range(n9), 2))
for fix_idx in combos2:
    for vals in itertools.product(range(3), repeat=2):
        if time.time() - t0 > 60: break
        proj = [i for i in range(n9) if i not in fix_idx]
        sec = [tuple(e[i] for i in proj) for e in cap_9
               if all(e[fix_idx[k]] == vals[k] for k in range(2))]
        if len(sec) <= best7: continue
        sset = set(sec)
        ok = True
        for x, y in itertools.combinations(sec, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in sset and z != x and z != y:
                ok = False; break
        if ok and len(sec) > best7:
            best7 = len(sec); best7_cap = sec
            print(f"  n=7: fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)

print(f"\nBest section at n=7: {best7}")
if best7 > 192 and best7_cap:
    with open(f"autoresearch/archive/046-cap-n7-{best7}.txt", "w") as f:
        for e in best7_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print("Saved.")

# Sections to n=8 (fix 1 coord)
print("\n--- sections to n=8 from 1082-cap ---")
best8 = 0; best8_cap = None
for fix_i in range(n9):
    for v in range(3):
        proj = [i for i in range(n9) if i != fix_i]
        sec = [tuple(e[i] for i in proj) for e in cap_9 if e[fix_i] == v]
        sset = set(sec)
        ok = True
        for x, y in itertools.combinations(sec, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in sset and z != x and z != y:
                ok = False; break
        if ok and len(sec) > best8:
            best8 = len(sec); best8_cap = sec
            print(f"  n=8: fix={fix_i}={v}: {len(sec)} CAP")
print(f"\nBest section at n=8: {best8}")
