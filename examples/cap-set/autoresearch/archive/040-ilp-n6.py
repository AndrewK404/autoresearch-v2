"""ILP search for max cap at n=6."""
import itertools
import pulp
import time

n = 6
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n

# Lines: unordered triples summing to 0
lines = []
seen = set()
for i, x in enumerate(elements):
    for j in range(i+1, TOTAL):
        y = elements[j]
        z = tuple((-xi - yi) % 3 for xi, yi in zip(x, y))
        if z == x or z == y: continue
        zi = sum(z[k] * 3**(n-1-k) for k in range(n))
        if zi <= j: continue
        lines.append((i, j, zi))
print(f"#vars = {TOTAL}, #lines = {len(lines)}")

prob = pulp.LpProblem("cap_n6", pulp.LpMaximize)
x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(TOTAL)]

for i, j, k in lines:
    prob += x[i] + x[j] + x[k] <= 2

prob += pulp.lpSum(x)

# warm start: c2=2 cap (96 elements known)
import numpy as np
arr = np.array(elements, dtype=np.int8)
c2_count = (arr == 2).sum(axis=1)
priority = -np.abs(c2_count - 2)
order = np.argsort(-priority, kind='stable')
warm_cap = []
forb = set()
for e in order:
    if e in forb: continue
    for u in warm_cap:
        c = tuple((-arr[u, k] - arr[e, k]) % 3 for k in range(n))
        ci = sum(c[k] * 3**(n-1-k) for k in range(n))
        forb.add(ci)
    warm_cap.append(int(e))
    forb.add(int(e))
print(f"warm cap: {len(warm_cap)}")
for v in warm_cap:
    x[v].setInitialValue(1)
for v in range(TOTAL):
    if v not in set(warm_cap):
        x[v].setInitialValue(0)

print("Solving...")
t0 = time.time()
solver = pulp.PULP_CBC_CMD(timeLimit=300, msg=True, warmStart=True)
prob.solve(solver)
print(f"\nSolve time: {time.time()-t0:.0f}s")
print(f"Status: {pulp.LpStatus[prob.status]}")
print(f"Objective: {pulp.value(prob.objective)}")

# Extract cap
cap_idx = [i for i in range(TOTAL) if x[i].value() and x[i].value() > 0.5]
print(f"Cap size: {len(cap_idx)}")

# Verify
sset = set(cap_idx)
ok = True
for i, j, k in lines:
    if i in sset and j in sset and k in sset:
        ok = False
        break
print(f"Valid cap: {ok}")

if len(cap_idx) > 96:
    with open(f"autoresearch/archive/040-cap-n6-{len(cap_idx)}.txt", "w") as f:
        for v in cap_idx:
            f.write("".join(str(c) for c in elements[v]) + "\n")
    print(f"Saved.")
