"""Search for 112-cap at n=6 via random-restart + FunSearch-style priorities."""
import itertools, random, time
import numpy as np

n = 6
elements = list(itertools.product(range(3), repeat=n))

def cap_via_order(order):
    cap, forb = [], set()
    for e in order:
        if e in forb: continue
        for u in cap:
            c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

# Try FunSearch n=8 priority adapted
def fs_n8(el):
    n = len(el)
    if n < 4: return 0
    score = n
    in_el = 0
    el_count = el.count(0)
    if el_count == 0:
        score += n ** 2
        if el[1] == el[-1]: score *= 1.5
        if n > 3 and el[2] == el[-2]: score *= 1.5
    else:
        if el[1] == el[-1]: score *= 0.5
        if n > 3 and el[2] == el[-2]: score *= 0.5
    for e in el:
        if e == 0:
            if in_el == 0:
                score *= n * 0.5
            elif in_el == el_count - 1:
                score *= 0.5
            else:
                score *= n * 0.5 ** in_el
            in_el += 1
        else:
            score += 1
    if el[1] == el[-1]: score *= 1.5
    if n > 3 and el[2] == el[-2]: score *= 1.5
    return float(score)

print(f"FunSearch-n8 adapted at n=6: {len(cap_via_order(sorted(elements, key=fs_n8, reverse=True)))}")

# c2 targets
for t in range(7):
    p = lambda e, t=t: -abs(sum(1 for x in e if x == 2) - t)
    print(f"c2={t}: {len(cap_via_order(sorted(elements, key=p, reverse=True)))}")

# Quadratic forms with all symmetric A
print("\n--- random quadratic forms ---")
best = 96
np.random.seed(0)
for trial in range(2000):
    A = np.random.randint(0, 3, (n, n))
    A = (A + A.T) % 3
    b = np.random.randint(0, 3, n)
    def p(e, A=A, b=b):
        x = np.array(e)
        return -float((x @ A @ x + b @ x) % 3)
    sz = len(cap_via_order(sorted(elements, key=p, reverse=True)))
    if sz > best:
        best = sz
        print(f"  trial {trial}: NEW BEST {sz}")

# Pair-feature priorities
print("\n--- pair-feature priorities ---")
for trial in range(2000):
    W = np.random.randint(-5, 6, (3, 3))
    def p(e, W=W):
        s = 0
        for i in range(n):
            for j in range(i+1, n):
                s += W[e[i]][e[j]]
        return float(s)
    sz = len(cap_via_order(sorted(elements, key=p, reverse=True)))
    if sz > best:
        best = sz
        print(f"  trial {trial}: W={W.tolist()} NEW BEST {sz}")

print(f"\nBest at n=6: {best}")
