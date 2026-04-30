"""Analyze the 448-cap produced by c2=3 priority."""
import itertools
from collections import Counter

n = 8

def priority(e, n):
    c2 = sum(1 for x in e if x == 2)
    return -abs(c2 - 3)

elements = list(itertools.product(range(3), repeat=n))
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

print(f"Cap size: {len(cap_set)}")

# Distribution of c2 in the cap
c2_dist = Counter(sum(1 for x in e if x == 2) for e in cap_set)
print(f"c2 distribution: {dict(sorted(c2_dist.items()))}")

# Distribution of multiset
mult_dist = Counter((sum(1 for x in e if x == 0),
                     sum(1 for x in e if x == 1),
                     sum(1 for x in e if x == 2)) for e in cap_set)
print(f"\nmultiset distribution:")
for ms, cnt in sorted(mult_dist.items(), key=lambda x: -x[1]):
    print(f"  {ms}: {cnt}")

# Save the cap
with open("autoresearch/archive/011-cap-448.txt", "w") as f:
    for e in cap_set:
        f.write("".join(str(x) for x in e) + "\n")
print(f"\nSaved to autoresearch/archive/011-cap-448.txt")
