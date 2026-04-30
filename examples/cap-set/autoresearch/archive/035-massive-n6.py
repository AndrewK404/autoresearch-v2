"""Massive priority search at n=6 to find a 112-cap."""
import itertools, random, time, math
import numpy as np

n = 6
elements = list(itertools.product(range(3), repeat=n))
TOTAL = 3 ** n  # 729

def cap_via_priority(priority):
    arr = sorted(elements, key=priority, reverse=True)
    cap, forb = [], set()
    for e in arr:
        if e in forb: continue
        for u in cap:
            c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

best = 96
best_cap = None
t0 = time.time()
budget = 600  # 10 min
trials = 0

# Family A: quadratic form x^T A x + b^T x mod 3
print("Family A: quadratic forms")
np.random.seed(42)
for trial in range(50000):
    if time.time() - t0 > budget * 0.2: break
    A = np.random.randint(0, 3, (n, n))
    A = (A + A.T) % 3
    b = np.random.randint(0, 3, n)
    c = np.random.randint(0, 3)
    target = np.random.randint(0, 3)
    def p(e, A=A, b=b, c=c, target=target):
        x = np.array(e, dtype=int)
        v = int((x @ A @ x + b @ x + c) % 3)
        return -float(abs(v - target))
    cap = cap_via_priority(p)
    trials += 1
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trials}: NEW BEST {best}")
        if best >= 112: break

# Family B: pair-feature W[a][b] for various W
print(f"\nFamily B: pair-feature priorities (best={best}, t={time.time()-t0:.0f}s)")
for trial in range(100000):
    if time.time() - t0 > budget * 0.4: break
    if best >= 112: break
    W = np.random.randint(-5, 6, (3, 3))
    W = (W + W.T) // 2  # symmetric, integer
    weight_idx = trial % 4
    def p(e, W=W, wi=weight_idx):
        s = 0
        for i in range(n):
            for j in range(i+1, n):
                if wi == 0:
                    s += W[e[i]][e[j]]
                elif wi == 1:
                    s += W[e[i]][e[j]] * (i + 1)
                elif wi == 2:
                    s += W[e[i]][e[j]] * (j - i)
                else:
                    s += W[e[i]][e[j]] * (i + j + 2)
        return float(s)
    cap = cap_via_priority(p)
    trials += 1
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trials}: NEW BEST {best}")
        if best >= 112: break

# Family C: c2-target + structural secondary
print(f"\nFamily C: c2-target + structural secondary (best={best}, t={time.time()-t0:.0f}s)")
for trial in range(100000):
    if time.time() - t0 > budget * 0.6: break
    if best >= 112: break
    primary_t = random.choice([0, 1, 2, 3, 4, 5, 6])
    coeffs = np.random.uniform(-1, 1, 8)
    def p(e, t=primary_t, c=coeffs):
        c0 = e.count(0); c1 = e.count(1); c2 = e.count(2)
        primary = -abs(c2 - t) * 1e6
        sec = (c[0]*c0 + c[1]*c1 + c[2]*c2 +
               c[3]*c0*c1 + c[4]*c1*c2 + c[5]*c0*c2 +
               c[6]*sum(e) % 3 + c[7]*(sum(x*x for x in e) % 3))
        return float(primary + sec)
    cap = cap_via_priority(p)
    trials += 1
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trials}: NEW BEST {best}")
        if best >= 112: break

# Family D: FunSearch n=8 priority adapted
print(f"\nFamily D: fs-n8-style with random parameters (best={best}, t={time.time()-t0:.0f}s)")
def make_fs_like(params):
    e0_bonus, weight_n2, refl_bonus, zero_mult = params
    def p(el):
        score = float(n)
        in_el = 0
        el_count = el.count(0)
        if el_count == 0:
            score += n ** 2 * weight_n2
            if el[1] == el[-1]: score *= refl_bonus
            if el[2] == el[-2]: score *= refl_bonus
        else:
            if el[1] == el[-1]: score *= 1.0/refl_bonus
        for e in el:
            if e == 0:
                score *= n * zero_mult ** in_el
                in_el += 1
            else:
                score += e0_bonus
        return float(score)
    return p

for trial in range(30000):
    if time.time() - t0 > budget * 0.75: break
    if best >= 112: break
    params = (random.uniform(0.1, 5),
              random.uniform(0.5, 3),
              random.uniform(0.3, 2.5),
              random.uniform(0.2, 1.5))
    p = make_fs_like(params)
    cap = cap_via_priority(p)
    trials += 1
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  trial {trials}: NEW BEST {best} params={params}")
        if best >= 112: break

# Family E: random restart greedy with many seeds
print(f"\nFamily E: random restart greedy (best={best}, t={time.time()-t0:.0f}s)")
for seed in range(50000):
    if time.time() - t0 > budget * 0.9: break
    if best >= 112: break
    rng = random.Random(seed)
    order = elements[:]
    rng.shuffle(order)
    # apply prefix bias
    if seed % 3 == 0:
        order.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2))
    elif seed % 3 == 1:
        order.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 3))
    cap = cap_via_priority(lambda e, o=order: -o.index(e))  # use given order
    # Wait this is slow; let me simplify
    pass

# Family E (simpler): random restart
print(f"\nFamily E (simpler): pure random restart (best={best}, t={time.time()-t0:.0f}s)")
for seed in range(200000):
    if time.time() - t0 > budget * 0.95: break
    if best >= 112: break
    rng = random.Random(seed * 7 + 31)
    order = elements[:]
    rng.shuffle(order)
    # greedy via order
    cap, forb = [], set()
    for e in order:
        if e in forb: continue
        for u in cap:
            c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    trials += 1
    if len(cap) > best:
        best = len(cap)
        best_cap = cap
        print(f"  seed {seed}: NEW BEST {best}")

print(f"\n=== Best at n=6: {best} ===  (trials: {trials}, time: {time.time()-t0:.0f}s)")
if best_cap:
    with open("autoresearch/archive/035-cap-n6-best.txt", "w") as f:
        f.write(f"# size = {best}\n")
        for e in best_cap:
            f.write("".join(str(x) for x in e) + "\n")
    print(f"saved to autoresearch/archive/035-cap-n6-best.txt")
