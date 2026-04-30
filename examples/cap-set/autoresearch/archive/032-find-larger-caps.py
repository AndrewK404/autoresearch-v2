"""Find larger caps at n=5 (target 45) and n=6 (target 112)."""
import itertools, random, time

def cap_size(order, n):
    cap, forb = [], set()
    for e in order:
        if e in forb: continue
        for u in cap:
            c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

# n=5: try random restart greedy
print("=== n=5 (target 45) ===")
els5 = list(itertools.product(range(3), repeat=5))
best5 = 0; best_cap5 = None
t0 = time.time()
trials = 0
while time.time() - t0 < 30:
    trials += 1
    rng = random.Random(trials)
    order = els5[:]
    rng.shuffle(order)
    cap = cap_size(order, 5)
    if len(cap) > best5:
        best5 = len(cap)
        best_cap5 = cap
        print(f"  trial {trials}: NEW BEST {best5}")
        if best5 >= 45: break

print(f"Best n=5: {best5}  (after {trials} trials)")

# n=5: try with c2-prefix + random tiebreak
print("\n--- c2=2 prefix + random tiebreak ---")
t0 = time.time()
while time.time() - t0 < 30 and best5 < 45:
    trials += 1
    rng = random.Random(trials)
    order = els5[:]
    rng.shuffle(order)
    order.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2))
    cap = cap_size(order, 5)
    if len(cap) > best5:
        best5 = len(cap)
        best_cap5 = cap
        print(f"  trial {trials}: NEW BEST {best5}")
        if best5 >= 45: break

print(f"Best n=5: {best5}")

# n=5: try priorities of various forms
print("\n--- structured priorities at n=5 ---")
import numpy as np
np.random.seed(0)
for trial in range(2000):
    if best5 >= 45: break
    # random feature set
    coefs = np.random.randint(-3, 4, 6)
    def p(e, n, c=coefs):
        c0 = e.count(0); c1 = e.count(1); c2 = e.count(2)
        return c[0]*c0 + c[1]*c1 + c[2]*c2 + c[3]*c0*c1 + c[4]*c0*c2 + c[5]*c1*c2

    order = sorted(els5, key=lambda e: p(e, 5), reverse=True)
    cap = cap_size(order, 5)
    if len(cap) > best5:
        best5 = len(cap)
        best_cap5 = cap
        print(f"  trial {trial}: NEW BEST {best5}: coefs={coefs.tolist()}")

print(f"\n=== Best n=5: {best5} ===")
if best_cap5:
    with open("autoresearch/archive/032-cap-n5.txt", "w") as f:
        f.write(f"# size = {best5}\n")
        for e in best_cap5:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"saved to autoresearch/archive/032-cap-n5.txt")
