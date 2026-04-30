"""Local search around the 448-cap to find 449+."""
import itertools, random, time

n = 8

def get_448_cap():
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 3), reverse=True)
    cap = []
    forb = set()
    for e in elements:
        if e in forb:
            continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

cap = get_448_cap()
cap_set = set(cap)
all_elements = list(itertools.product(range(3), repeat=n))
non_cap = [e for e in all_elements if e not in cap_set]

print(f"Cap: {len(cap)}, non-cap: {len(non_cap)}")

# Compute "blockers" for each non-cap element: cap members that block its addition
def blockers(e, cap_set):
    """Pairs (a, b) in cap_set such that a+b+e ≡ 0 mod 3 (i.e. e is the 3rd of an AP)."""
    blocks = []
    cap_list = list(cap_set)
    for i in range(len(cap_list)):
        a = cap_list[i]
        # b = -a-e mod 3
        b = tuple((-a[j] - e[j]) % 3 for j in range(n))
        if b in cap_set and b != a and b != e:
            blocks.append((a, b))
    return blocks

# Try: for each non-cap element e, find what cap members must leave to add e
print("\nFor each non-cap element, count of blocking pairs:")
import collections
block_dist = collections.Counter()
for e in non_cap[:1000]:
    bs = blockers(e, cap_set)
    block_dist[len(bs)] += 1
print(f"  block count distribution (first 1000): {dict(sorted(block_dist.items())[:10])}")

# Look for non-cap elements blocked by a small number of pairs
print("\nNon-cap elements with few blockers:")
candidates_low = []
for e in non_cap:
    bs = blockers(e, cap_set)
    if len(bs) <= 4:
        candidates_low.append((len(bs), e, bs))
candidates_low.sort()
print(f"  {len(candidates_low)} elements with ≤4 blocker pairs")
if candidates_low:
    for cnt, e, bs in candidates_low[:5]:
        print(f"    e={e} blocked by {cnt} pairs (sample: {bs[:3]})")

# Try: 2-3 swap. Remove 2 cap members, add 3 non-cap members.
print("\n--- 2-out-3-in search (preserve cap property and grow) ---")
random.seed(0)
best_size = 448
t0 = time.time()
trials = 0
max_time = 30

# Find pairs that block multiple non-cap elements
from collections import defaultdict
pair_blocks = defaultdict(set)  # frozenset({a,b}) -> set of non-cap e they block (as third point)
# Build: for each pair (a, b) in cap, the third point c
for i, a in enumerate(cap):
    for j in range(i+1, len(cap)):
        b = cap[j]
        c = tuple((-a[k] - b[k]) % 3 for k in range(n))
        if c not in cap_set:
            pair_blocks[frozenset([a, b])].add(c)

print(f"  computed {len(pair_blocks)} blocker pairs")

# For each pair (a, b), removing them allows the c they block. But removing them also
# unblocks more elements via OTHER pairs they participate in.
# Let's build for each cap member the set of non-cap elements they help block.
member_blocks = defaultdict(set)
for pair_fs, c_set in pair_blocks.items():
    for m in pair_fs:
        member_blocks[m].update(c_set)

# Find pairs (a, b) that unblock the most non-cap elements when removed.
# Remove a and b: any non-cap element c whose ALL blocking pairs include a or b becomes addable.

# Build: for each non-cap e, set of pairs that block it
non_cap_blockers = defaultdict(set)
for pair_fs, c_set in pair_blocks.items():
    for c in c_set:
        non_cap_blockers[c].add(pair_fs)

# For each pair of cap members (a, b), count non-cap elements unblocked when removing both
# A non-cap element e is unblocked iff all its blockers contain a or b.
# Count: for each e, |{pairs blocking e} ∩ {pairs containing a or b}| == |all blockers of e|.

# This is expensive but doable for small samples.
# Sample pairs to remove
print("\n--- random 2-out search ---")
best_local = 448
for trial in range(2000):
    a = random.choice(cap)
    b = random.choice(cap)
    if a == b:
        continue
    # Cap minus {a, b}
    new_cap = cap_set - {a, b}
    # Find all non-cap elements that can be added
    addable = []
    for e in non_cap:
        ok = True
        for u in new_cap:
            v = tuple((-u[i] - e[i]) % 3 for i in range(n))
            if v in new_cap and v != u and v != e:
                ok = False
                break
        if ok:
            addable.append(e)
    # Greedy add as many as possible
    final_cap = set(new_cap)
    forb = set(new_cap)
    for x, y in itertools.combinations(new_cap, 2):
        z = tuple((-x[i] - y[i]) % 3 for i in range(n))
        forb.add(z)
    # Add elements in some order
    order = sorted(addable, key=lambda e: -abs(sum(1 for x in e if x == 2) - 3))
    for e in order:
        if e in forb: continue
        for u in final_cap:
            c = tuple((-u[i] - e[i]) % 3 for i in range(n))
            forb.add(c)
        final_cap.add(e)
        forb.add(e)
    if len(final_cap) > best_local:
        best_local = len(final_cap)
        print(f"  trial {trial}: NEW BEST {best_local} (removed {a}, {b})")
    if time.time() - t0 > max_time:
        print(f"  time up at trial {trial}")
        break

print(f"\nBest from 2-out search: {best_local}")
