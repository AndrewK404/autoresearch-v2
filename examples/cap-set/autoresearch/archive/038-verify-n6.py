"""Carefully verify the alleged 114-cap at n=6."""
import itertools

n = 6

with open("autoresearch/archive/037-cap-n6-114.txt") as f:
    cap = [tuple(int(c) for c in line.strip()) for line in f if line.strip()]

print(f"Cap size: {len(cap)}")
print(f"Distinct: {len(set(cap))}")

# Robust check
sset = set(cap)
violations = []
for x, y in itertools.combinations(cap, 2):
    z = tuple((-xi - yi) % 3 for xi, yi in zip(x, y))
    if z in sset and z != x and z != y:
        violations.append((x, y, z))

print(f"Violations: {len(violations)}")
if violations:
    print(f"First 3:")
    for v in violations[:3]:
        print(f"  {v}")
        # double-check: x + y + z mod 3 should be 0
        x, y, z = v
        s = tuple((xi + yi + zi) % 3 for xi, yi, zi in zip(x, y, z))
        print(f"    sum mod 3 = {s}")
