"""Find an explicit 9-cap in F_3^3 (max cap size at n=3)."""
import itertools

n = 3
elements = list(itertools.product(range(3), repeat=n))

def is_cap(s):
    sset = set(s)
    for x, y in itertools.combinations(s, 2):
        z = tuple((-xi - yi) % 3 for xi, yi in zip(x, y))
        if z in sset and z != x and z != y:
            return False
    return True

# Brute search: try all 9-subsets
from itertools import combinations
print("Searching for a 9-cap in F_3^3...")
found = None
for s in combinations(elements, 9):
    if is_cap(s):
        found = s
        break

if found:
    print(f"Found 9-cap:")
    for e in found:
        print(f"  {e}")
    # Verify
    print(f"Is cap: {is_cap(found)}")
else:
    print("No 9-cap found??")
