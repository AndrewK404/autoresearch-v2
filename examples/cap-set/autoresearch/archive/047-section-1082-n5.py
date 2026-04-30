"""Section the 1082-cap to find caps at n=4, 5."""
import itertools, sys, time
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

def is_cap(sec):
    sset = set(sec)
    for x, y in itertools.combinations(sec, 2):
        z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
        if z in sset and z != x and z != y:
            return False
    return True

# Section to n=5 (fix 4 coords)
print("Searching sections to n=5 (fix 4 coords)...")
best5 = 40; best5_cap = None
t0 = time.time()
combos = list(itertools.combinations(range(n9), 4))
for fix_idx in combos:
    if time.time() - t0 > 60: break
    for vals in itertools.product(range(3), repeat=4):
        if time.time() - t0 > 60: break
        proj = [i for i in range(n9) if i not in fix_idx]
        sec = [tuple(e[i] for i in proj) for e in cap_9
               if all(e[fix_idx[k]] == vals[k] for k in range(4))]
        if len(sec) <= best5: continue
        if is_cap(sec):
            best5 = len(sec); best5_cap = sec
            print(f"  fix={fix_idx}={vals}: {len(sec)} CAP", flush=True)
            if best5 >= 45: break
    if best5 >= 45: break

print(f"\nBest n=5 section: {best5}")
if best5 > 40 and best5_cap:
    with open(f"autoresearch/archive/047-cap-n5-{best5}.txt", "w") as f:
        for e in best5_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print("Saved n=5 cap.")

# Section to n=4 (fix 5 coords)
print("\n--- sections to n=4 ---")
best4 = 16; best4_cap = None
t0 = time.time()
combos = list(itertools.combinations(range(n9), 5))
for fix_idx in combos:
    if time.time() - t0 > 30: break
    for vals in itertools.product(range(3), repeat=5):
        if time.time() - t0 > 30: break
        proj = [i for i in range(n9) if i not in fix_idx]
        sec = [tuple(e[i] for i in proj) for e in cap_9
               if all(e[fix_idx[k]] == vals[k] for k in range(5))]
        if len(sec) <= best4: continue
        if is_cap(sec):
            best4 = len(sec); best4_cap = sec
            print(f"  fix={fix_idx}={vals}: {len(sec)} CAP")
            if best4 >= 20: break
    if best4 >= 20: break

print(f"\nBest n=4 section: {best4}")
if best4 > 16 and best4_cap:
    with open(f"autoresearch/archive/047-cap-n4-{best4}.txt", "w") as f:
        for e in best4_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print("Saved.")
