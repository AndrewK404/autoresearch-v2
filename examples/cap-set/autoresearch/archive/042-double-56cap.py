"""Take the 56-cap section, check if it's projective, then double to 112."""
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

# Section: fix last two coords to (0, 1) — this gives 56 elements
section = [e[:6] for e in cap_8 if e[6] == 0 and e[7] == 1]
print(f"section size: {len(section)}")

# Check projective: no two scalar multiples
sset = set(section)
projective = True
for v in section:
    if v == (0,)*6:
        # zero vector
        continue
    v2 = tuple((2 * x) % 3 for x in v)
    if v2 in sset and v2 != v:
        projective = False
        print(f"  not projective: {v} and {v2} both in cap")
        break
print(f"Projective: {projective}")

# If projective, double via {v, 2v}
if projective:
    doubled = list(section) + [tuple((2*x)%3 for x in v) for v in section if v != (0,)*6]
    doubled = list(set(doubled))  # dedupe
    print(f"doubled cap size: {len(doubled)}")

    # Verify cap
    dset = set(doubled)
    ok = True
    bad = None
    for x, y in itertools.combinations(doubled, 2):
        z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
        if z in dset and z != x and z != y:
            ok = False
            bad = (x, y, z)
            break
    print(f"valid cap: {ok}")
    if bad:
        print(f"  e.g. AP: {bad}")
    if ok and len(doubled) > 96:
        with open(f"autoresearch/archive/042-cap-n6-{len(doubled)}.txt", "w") as f:
            for e in doubled:
                f.write("".join(str(x) for x in e) + "\n")
        print(f"saved")

# Try various sections and various doublings
print("\n--- exhaustive section + double ---")
import itertools as it
best = 96; best_cap = None
for fix_coords in it.combinations(range(8), 2):
    for vals in it.product(range(3), repeat=2):
        proj_idx = [i for i in range(8) if i not in fix_coords]
        section = [tuple(e[i] for i in proj_idx) for e in cap_8
                   if all(e[fix_coords[k]] == vals[k] for k in range(2))]
        if len(section) < 50: continue

        sset = set(section)
        # check projective (no v and 2v both in)
        proj_ok = True
        for v in section:
            if v == (0,)*6: continue
            v2 = tuple((2*x)%3 for x in v)
            if v2 in sset and v2 != v:
                proj_ok = False; break
        if not proj_ok: continue

        # Double
        doubled = list(set(list(section) + [tuple((2*x)%3 for x in v)
                            for v in section if v != (0,)*6]))
        # Verify
        dset = set(doubled)
        ok = True
        for x, y in it.combinations(doubled, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in dset and z != x and z != y:
                ok = False; break
        if ok and len(doubled) > best:
            best = len(doubled); best_cap = doubled
            print(f"  fix={fix_coords}={vals}: section={len(section)}, doubled={len(doubled)} CAP")

print(f"\nBest from section+double: {best}")
if best > 96 and best_cap:
    with open(f"autoresearch/archive/042-cap-n6-{best}.txt", "w") as f:
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"Saved.")
