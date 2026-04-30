"""Section the 2240-cap and 4608-cap to find caps at n=5, 6, 7."""
import itertools, sys, time
sys.path.insert(0, "problem")
from priority import _priority_n8, _CAP_112_N6, _CAP_20_N4, _CAP_9_N3

# Build 2240-cap (n=10, 112 × 20 tensor)
cap_2240 = [(*a, *b) for a in _CAP_112_N6 for b in _CAP_20_N4]
print(f"2240-cap: {len(cap_2240)}")

# Build 4608-cap (n=11, 512 × 9 tensor)
n8_elements = list(itertools.product(range(3), repeat=8))
n8_elements.sort(key=_priority_n8, reverse=True)
cap_512, forb = [], set()
for e in n8_elements:
    if e in forb: continue
    for u in cap_512:
        c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap_512.append(e)
    forb.add(e)
print(f"512-cap: {len(cap_512)}")
cap_4608 = [(*a, *b) for a in cap_512 for b in _CAP_9_N3]
print(f"4608-cap: {len(cap_4608)}")

def is_cap(s):
    sset = set(s)
    for x, y in itertools.combinations(s, 2):
        z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
        if z in sset and z != x and z != y:
            return False
    return True

# Section 2240 to n=5 (fix 5 coords)
print("\n--- 2240-cap → n=5 (fix 5 coords) ---")
n = 10
best5 = 40; best5_cap = None
t0 = time.time()
combos = list(itertools.combinations(range(n), 5))
for fix_idx in combos:
    if time.time() - t0 > 30: break
    proj = [i for i in range(n) if i not in fix_idx]
    for vals in itertools.product(range(3), repeat=5):
        if time.time() - t0 > 30: break
        sec = [tuple(e[i] for i in proj) for e in cap_2240
               if all(e[fix_idx[k]] == vals[k] for k in range(5))]
        if len(sec) <= best5: continue
        if is_cap(sec):
            best5 = len(sec); best5_cap = sec
            print(f"  fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)
            if best5 >= 45: break
    if best5 >= 45: break

print(f"Best 2240→n=5: {best5}")

# Section 4608 to n=5 (fix 6 coords)
print("\n--- 4608-cap → n=5 (fix 6 coords) ---")
n = 11
t0 = time.time()
combos = list(itertools.combinations(range(n), 6))
for fix_idx in combos:
    if time.time() - t0 > 60: break
    proj = [i for i in range(n) if i not in fix_idx]
    for vals in itertools.product(range(3), repeat=6):
        if time.time() - t0 > 60: break
        sec = [tuple(e[i] for i in proj) for e in cap_4608
               if all(e[fix_idx[k]] == vals[k] for k in range(6))]
        if len(sec) <= best5: continue
        if is_cap(sec):
            best5 = len(sec); best5_cap = sec
            print(f"  4608: fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)
            if best5 >= 45: break
    if best5 >= 45: break

print(f"Best n=5: {best5}")

# Section 4608 to n=6 (fix 5 coords) and n=7 (fix 4)
print("\n--- 4608-cap → n=6 (fix 5 coords) ---")
n = 11
best6 = 112; best6_cap = None
t0 = time.time()
combos = list(itertools.combinations(range(n), 5))
for fix_idx in combos:
    if time.time() - t0 > 30: break
    proj = [i for i in range(n) if i not in fix_idx]
    for vals in itertools.product(range(3), repeat=5):
        if time.time() - t0 > 30: break
        sec = [tuple(e[i] for i in proj) for e in cap_4608
               if all(e[fix_idx[k]] == vals[k] for k in range(5))]
        if len(sec) <= best6: continue
        if is_cap(sec):
            best6 = len(sec); best6_cap = sec
            print(f"  fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)
            if best6 >= 200: break
    if best6 >= 200: break

print(f"Best n=6 from 4608: {best6}")

if best5 > 40 and best5_cap:
    with open(f"autoresearch/archive/048-cap-n5-{best5}.txt", "w") as f:
        for e in best5_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"Saved n=5 cap.")
