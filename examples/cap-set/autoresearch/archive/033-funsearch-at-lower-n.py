"""Try FunSearch n=8 / n=9 priorities at lower n."""
import itertools
import numpy as np
import time

def cap_size(priority, n):
    elements = list(itertools.product(range(3), repeat=n))
    elements.sort(key=lambda e: priority(e), reverse=True)
    cap, forb = [], set()
    for e in elements:
        if e in forb: continue
        for u in cap:
            c = tuple((-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

def fs_n8(el):
    n = len(el)
    score = n
    in_el = 0
    el_count = el.count(0)
    if el_count == 0:
        score += n ** 2
        if len(el) > 1 and el[1] == el[-1]: score *= 1.5
        if len(el) > 3 and el[2] == el[-2]: score *= 1.5
        if len(el) > 5 and el[3] == el[-3]: score *= 1.5
    else:
        if len(el) > 1 and el[1] == el[-1]: score *= 0.5
        if len(el) > 3 and el[2] == el[-2]: score *= 0.5
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
    if len(el) > 1 and el[1] == el[-1]: score *= 1.5
    if len(el) > 3 and el[2] == el[-2]: score *= 1.5
    return float(score)

def fs_n9(el):
    n = len(el)
    arr = np.array(el, dtype=np.float32)
    weight = (arr @ arr) % 3
    a = max(1, n // 3)
    b = max(a + 1, n - n // 3)
    if b >= n: b = n - 1
    if a >= b: a = b - 1
    s_1 = (arr[:b] @ arr[:b]) % 3
    s_3 = (2 * (arr[:a] @ arr[:a])) % 3
    s_4 = (arr[:a] @ arr[a:b]) % 3 if a < b else 0
    s_5 = np.sum(arr[:a] == arr[-1]) % 3
    return float(-3**3 * s_1 + 3**2 * weight + 3**3 * s_3 + 3**2 * s_4 + s_5)

def c2_target(t):
    def p(el):
        c2 = sum(1 for x in el if x == 2)
        return -abs(c2 - t)
    return p

for n in [3, 4, 5, 6, 7]:
    print(f"=== n={n} (max known: {[None,None,None,9,20,45,112,236][n]}) ===")
    print(f"  fs_n8 priority: {len(cap_size(fs_n8, n))}")
    print(f"  fs_n9 priority: {len(cap_size(fs_n9, n))}")
    for t in range(n+1):
        sz = len(cap_size(c2_target(t), n))
        print(f"  c2={t}: {sz}")
