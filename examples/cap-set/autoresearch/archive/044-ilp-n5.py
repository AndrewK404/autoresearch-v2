"""ILP for max cap at n=5 (target 45)."""
import itertools, pulp, time

n = 5
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n  # 243

# Lines (unordered triples summing to 0)
lines = []
for i in range(TOTAL):
    for j in range(i+1, TOTAL):
        x, y = elements[i], elements[j]
        z = tuple((-xi - yi) % 3 for xi, yi in zip(x, y))
        if z == x or z == y: continue
        zi = sum(z[k] * 3**(n-1-k) for k in range(n))
        if zi <= j: continue
        lines.append((i, j, zi))
print(f"#vars={TOTAL}, #lines={len(lines)}")

prob = pulp.LpProblem("cap_n5", pulp.LpMaximize)
x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(TOTAL)]
for i, j, k in lines:
    prob += x[i] + x[j] + x[k] <= 2
prob += pulp.lpSum(x)

print("Solving...")
t0 = time.time()
solver = pulp.PULP_CBC_CMD(timeLimit=120, msg=False)
prob.solve(solver)
print(f"Time: {time.time()-t0:.0f}s, Status: {pulp.LpStatus[prob.status]}")
print(f"Cap size: {int(pulp.value(prob.objective))}")

cap = [i for i in range(TOTAL) if x[i].value() and x[i].value() > 0.5]
# Verify
sset = set(cap)
ok = True
for i, j, k in lines:
    if i in sset and j in sset and k in sset:
        ok = False; break
print(f"Valid cap: {ok}")

if len(cap) > 40 and ok:
    with open(f"autoresearch/archive/044-cap-n5-{len(cap)}.txt", "w") as f:
        for v in cap:
            f.write("".join(str(c) for c in elements[v]) + "\n")
    print(f"Saved n=5 cap of size {len(cap)}")
