"""Try projecting/sectioning the FunSearch 512-cap at n=8 down to n=6."""
import itertools
import sys
sys.path.insert(0, "problem")
from priority import _priority_n8

n = 8
elements_8 = list(itertools.product(range(3), repeat=n))
elements_8.sort(key=lambda e: _priority_n8(e), reverse=True)

cap_8 = []
forb = set()
for e in elements_8:
    if e in forb: continue
    for u in cap_8:
        c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap_8.append(e)
    forb.add(e)
print(f"512-cap at n=8: {len(cap_8)}")

# Project: fix last 2 coords to (a, b), look at the 6-tuple slice
# A "section" of cap_8 fixing last 2 coords = (a, b) is a cap at n=6.
print("\n--- sections (fix last 2 coords) ---")
import collections
best_sec = 0; best_sec_cap = None
for a in range(3):
    for b in range(3):
        section = [e[:6] for e in cap_8 if e[6] == a and e[7] == b]
        # Verify cap
        sset = set(section)
        ok = True
        for x, y in itertools.combinations(section, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in sset and z != x and z != y:
                ok = False
                break
        print(f"  fix=(  {a},{b}): {len(section)} elements, cap={ok}")
        if ok and len(section) > best_sec:
            best_sec = len(section)
            best_sec_cap = section

# Section by other coord pairs
print("\n--- sections (fix various 2 coords) ---")
best = best_sec
best_cap = best_sec_cap
for fix_coords in [(0, 1), (0, 4), (3, 7), (2, 5), (1, 6), (0, 7)]:
    for vals in itertools.product(range(3), repeat=2):
        section = []
        proj_indices = [i for i in range(8) if i not in fix_coords]
        for e in cap_8:
            if all(e[fix_coords[k]] == vals[k] for k in range(2)):
                section.append(tuple(e[i] for i in proj_indices))
        sset = set(section)
        ok = True
        for x, y in itertools.combinations(section, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in sset and z != x and z != y:
                ok = False; break
        if ok and len(section) > best:
            best = len(section); best_cap = section
            print(f"  fix={fix_coords} = {vals}: {len(section)} CAP", flush=True)
        elif ok:
            pass  # silent
print(f"\nBest section cap at n=6: {best}")

# Try sections fixing 1 coord (n=8 -> n=7)
print("\n--- sections at n=7 (fix 1 coord) ---")
best7 = 0; best7_cap = None
for fc in range(8):
    for v in range(3):
        section = [tuple(e[i] for i in range(8) if i != fc) for e in cap_8 if e[fc] == v]
        sset = set(section)
        ok = all((tuple((-xi-yi)%3 for xi, yi in zip(x, y)) not in sset or
                  tuple((-xi-yi)%3 for xi, yi in zip(x, y)) == x or
                  tuple((-xi-yi)%3 for xi, yi in zip(x, y)) == y)
                 for x, y in itertools.combinations(section, 2))
        if ok and len(section) > best7:
            best7 = len(section); best7_cap = section
print(f"Best section at n=7: {best7}")

if best > 96:
    with open(f"autoresearch/archive/041-cap-n6-{best}.txt", "w") as f:
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"Saved n=6 cap of size {best}")

if best7 > 192:
    with open(f"autoresearch/archive/041-cap-n7-{best7}.txt", "w") as f:
        for e in best7_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"Saved n=7 cap of size {best7}")
