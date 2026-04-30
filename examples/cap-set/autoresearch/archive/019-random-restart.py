"""Random restart greedy: shuffle elements, run greedy, track best."""
import itertools
import random
import time

n = 8
elements_all = list(itertools.product(range(3), repeat=n))
print(f"Total elements: {len(elements_all)}")

def greedy_cap(order):
    cap = []
    forb = set()
    for e in order:
        if e in forb:
            continue
        for u in cap:
            c = tuple((3 - ui - ei) % 3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

best = 0
best_cap = None
t0 = time.time()
trials = 200
for trial in range(trials):
    rng = random.Random(trial)
    order = elements_all[:]
    rng.shuffle(order)
    cap = greedy_cap(order)
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trial}: NEW BEST {best}")

print(f"\n[Pure random] Best after {trials} trials: {best}  ({time.time()-t0:.1f}s)")

# Save best
if best_cap is not None:
    with open("autoresearch/archive/019-best-cap.txt", "w") as f:
        f.write(f"# size = {best}\n")
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")

# Random + c2-bias: prefer c2=3 with random secondary
print("\n--- c2=3 prefer + random tiebreak ---")
best_c2 = 0
for trial in range(200):
    rng = random.Random(10000 + trial)
    perm = elements_all[:]
    rng.shuffle(perm)
    perm.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 3))
    cap = greedy_cap(perm)
    if len(cap) > best_c2:
        best_c2 = len(cap)
        print(f"  trial {trial}: NEW BEST {best_c2}")

print(f"\nBest c2=3 + random tiebreak: {best_c2}")
