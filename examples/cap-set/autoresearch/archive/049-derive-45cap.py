"""From the 112-cap in F_3^6, derive a 45-cap at n=5 by:
1. Project to PG(5, 3): pairs (v, 2v) → 56 projective points (Hill cap).
2. For each affine hyperplane H of PG(5, 3), compute |Hill ∩ H|.
3. Take Hill cap minus a hyperplane intersection of size 11 to get 45 points.
4. These 45 points lift to 45 affine points in F_3^5 by deleting the
   hyperplane-defining coordinate.
"""
import itertools, sys
sys.path.insert(0, "problem")
from priority import _CAP_112_N6

cap = list(_CAP_112_N6)
print(f"112-cap size: {len(cap)}")

# Step 1: Find pairs (v, 2v). Verify cap is symmetric (closed under x -> 2x).
sset = set(cap)
pairs = []
seen = set()
for v in cap:
    if v in seen: continue
    v2 = tuple((2*x) % 3 for x in v)
    if v2 == v:
        # zero vector? In F_3^6: only (0,0,0,0,0,0) maps to itself. Check.
        if v != (0,0,0,0,0,0):
            print(f"  weird: {v} == 2*{v}")
        continue
    if v2 in sset:
        pairs.append((v, v2))
        seen.add(v); seen.add(v2)
    else:
        # not a "doubled" pair; v alone
        pairs.append((v,))
        seen.add(v)

print(f"pairs+singletons: {len(pairs)}")
# Verify
proj_count = sum(2 if len(p)==2 else 1 for p in pairs)
print(f"total elements: {proj_count}")

# So the 112-cap is 56 pairs. Each pair = 1 projective point.
hill_proj_points = [pair[0] for pair in pairs if len(pair) == 2]  # representatives
hill_proj_singles = [pair[0] for pair in pairs if len(pair) == 1]
print(f"Doubled pairs (projective points): {len(hill_proj_points)}")
print(f"Singletons: {len(hill_proj_singles)}")

# Each "projective point" corresponds to (v, 2v) pair. Hill cap = 56 such points.
if len(hill_proj_points) == 56:
    print("Confirmed: 112-cap = doubled Hill 56-cap")

# Step 2: For each hyperplane in PG(5, 3) defined by linear form l(x) = 0,
# count how many Hill points lie on it. We want a hyperplane with 11 Hill points.
# Affine hyperplanes in F_3^6 are {x : a · x = c} for nonzero a ∈ F_3^6, c ∈ F_3.
# For projective: hyperplane is {projective point [v] : a · v = 0}.
# So we want |{[v] ∈ Hill : a · v = 0}| = 11 for the right a.

n = 6
# Iterate over all nonzero a ∈ F_3^6 mod scalar (i.e. distinct projective hyperplanes)
seen_a = set()
hyperplanes_with_11 = []
for a_full in itertools.product(range(3), repeat=n):
    if all(x == 0 for x in a_full): continue
    # canonicalize: first nonzero entry = 1
    first_nz = next(i for i, x in enumerate(a_full) if x != 0)
    if a_full[first_nz] != 1:
        continue  # canonical form
    seen_a.add(a_full)
    cnt = sum(1 for v in cap if sum(a_full[i] * v[i] for i in range(n)) % 3 == 0)
    # cnt counts AFFINE Hill points (112-cap) with a·v = 0, but since cap is doubled,
    # this is 2 × (projective points satisfying a·v = 0).
    proj_cnt = cnt // 2
    if proj_cnt == 11:
        hyperplanes_with_11.append(a_full)

print(f"\nhyperplanes a with |Hill ∩ {{a·v=0}}| = 11: {len(hyperplanes_with_11)}")
if hyperplanes_with_11:
    a = hyperplanes_with_11[0]
    print(f"using a = {a}")
    # The 45 = 56 - 11 affine points: take Hill - hyperplane = projective points where a·v ≠ 0.
    # In affine F_3^6: cap minus {v : a·v = 0} → 112 - 22 = 90 points (since 11 proj × 2 affine).
    # We want a 45-cap in F_3^5 by deleting the hyperplane direction.
    # When a·v = 0: v lies in the hyperplane (subspace of dim 5).
    # When a·v ≠ 0: v lies in one of two affine cosets.
    # For each of the 56 - 11 = 45 projective Hill points NOT on the hyperplane,
    # there's exactly one affine representative with a·v = 1 (and another with a·v = 2).
    # Pick the a·v = 1 representatives → 45 points in the affine coset {v : a·v = 1}.
    # This affine coset is parametrizable as F_3^5 (5-dim affine subspace).

    # Find the 45 Hill points (out of 112) with a·v = 1
    cap_45_lifted = [v for v in cap if sum(a[i] * v[i] for i in range(n)) % 3 == 1]
    print(f"Hill points with a·v=1: {len(cap_45_lifted)}")

    # Project these to F_3^5 by deleting one coordinate where a is nonzero
    nz_idx = first_nz = next(i for i, x in enumerate(a) if x != 0)
    proj_idx = [i for i in range(n) if i != nz_idx]
    cap_45 = [tuple(v[i] for i in proj_idx) for v in cap_45_lifted]
    print(f"45-cap candidate at n=5: {len(set(cap_45))}")  # should be 45 distinct

    # Verify cap
    sset = set(cap_45)
    if len(sset) != len(cap_45):
        print("  ERROR: duplicates after projection")
    else:
        violations = 0
        for x, y in itertools.combinations(cap_45, 2):
            z = tuple((-xi-yi)%3 for xi, yi in zip(x, y))
            if z in sset and z != x and z != y:
                violations += 1
        print(f"  violations: {violations}")
        if violations == 0:
            print(f"  ✓ valid {len(cap_45)}-cap at n=5")
            with open(f"autoresearch/archive/049-cap-n5-{len(cap_45)}.txt", "w") as f:
                for e in cap_45:
                    f.write("".join(str(x) for x in e) + "\n")
            print(f"  Saved.")
