"""Massive priority sweep — programmatic generation of priority candidates."""
import sys, os, itertools, random, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
cap_set_size = m.cap_set_size

n = 8
elements_all = list(itertools.product(range(3), repeat=n))

t0 = time.time()
best = 448
best_desc = "baseline c2=3"
budget = 300  # seconds

# Family 1: priority(e) = -abs(c2 - target) + alpha * extra_feat
print("--- Family 1: c2=3 plus various extra features ---")
features = {
    "c0": lambda e: sum(1 for x in e if x == 0),
    "c1": lambda e: sum(1 for x in e if x == 1),
    "c2": lambda e: sum(1 for x in e if x == 2),
    "sum": lambda e: sum(e),
    "sum_mod3": lambda e: sum(e) % 3,
    "max": lambda e: max(e),
    "min": lambda e: min(e),
    "first": lambda e: e[0],
    "last": lambda e: e[-1],
    "first2": lambda e: e[0] + e[1],
    "first4_sum": lambda e: sum(e[:4]),
    "last4_sum": lambda e: sum(e[4:]),
    "even_sum": lambda e: sum(e[i] for i in range(0, n, 2)),
    "odd_sum": lambda e: sum(e[i] for i in range(1, n, 2)),
    "wt_sum": lambda e: sum(x*(i+1) for i, x in enumerate(e)),
    "wt_sum_mod3": lambda e: sum(x*(i+1) for i, x in enumerate(e)) % 3,
    "wt_sum_mod5": lambda e: sum(x*(i+1) for i, x in enumerate(e)) % 5,
    "wt_sum_mod7": lambda e: sum(x*(i+1) for i, x in enumerate(e)) % 7,
    "pair_eq": lambda e: sum(1 for i in range(n) for j in range(i+1, n) if e[i] == e[j]),
    "pair_neq": lambda e: sum(1 for i in range(n) for j in range(i+1, n) if e[i] != e[j]),
    "consec_eq": lambda e: sum(1 for i in range(n-1) if e[i] == e[i+1]),
    "ham_to_0": lambda e: sum(1 for x in e if x != 0),
    "ham_to_1": lambda e: sum(1 for x in e if x != 1),
    "ham_to_2": lambda e: sum(1 for x in e if x != 2),
    "alpha_dot": lambda e: (e[0] - e[1] + e[2] - e[3] + e[4] - e[5] + e[6] - e[7]) % 3,
}

for name, f in features.items():
    for sign in [1, -1]:
        def p(el, n, f=f, s=sign):
            c2 = sum(1 for x in el if x == 2)
            return -abs(c2 - 3) * 1000 + s * f(el)
        sz = cap_set_size(p, n)
        if sz > best:
            best = sz
            best_desc = f"c2=3 + {sign:+}*{name}"
            print(f"  NEW BEST {best}: c2=3 + {sign:+}*{name}")

# Family 2: random non-c2 polynomial in (c0, c1, c2)
print("\n--- Family 2: polynomials in counts ---")
np.random.seed(0)
for trial in range(500):
    coefs = np.random.randint(-10, 10, 6).tolist()
    def p(el, n, c=coefs):
        c0 = el.count(0)
        c1 = el.count(1)
        c2 = el.count(2)
        return c[0]*c0 + c[1]*c1 + c[2]*c2 + c[3]*c0*c1 + c[4]*c0*c2 + c[5]*c1*c2
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        best_desc = f"poly_counts {coefs}"
        print(f"  NEW BEST {best}: {coefs}")
    if time.time() - t0 > budget / 4: break

# Family 3: random pair-feature based
print("\n--- Family 3: pair-feature combinations ---")
random.seed(0)
for trial in range(300):
    # random matrix W[a][b] for pair (e_i = a, e_j = b)
    W = np.random.randint(-3, 4, (3, 3))
    weight_idx = random.choice([True, False])
    def p(el, n, W=W, wi=weight_idx):
        s = 0
        for i in range(n):
            for j in range(i+1, n):
                w = (i+1) * (j+1) if wi else 1
                s += W[el[i]][el[j]] * w
        return float(s)
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        best_desc = f"pair_W {W.tolist()} {wi}"
        print(f"  NEW BEST {best}")
    if time.time() - t0 > budget / 2: break

# Family 4: c2=3 + pair-feature
print("\n--- Family 4: c2=3 + pair-feature secondary ---")
random.seed(100)
for trial in range(300):
    W = np.random.randint(-5, 5, (3, 3))
    def p(el, n, W=W):
        c2 = sum(1 for x in el if x == 2)
        primary = -abs(c2 - 3) * 1_000_000
        s = 0
        for i in range(n):
            for j in range(i+1, n):
                s += W[el[i]][el[j]]
        return primary + float(s)
    sz = cap_set_size(p, n)
    if sz > best:
        best = sz
        best_desc = f"c2=3 + pair_W {W.tolist()}"
        print(f"  NEW BEST {best}")
    if time.time() - t0 > 3*budget/4: break

# Family 5: priority that doesn't use c2 at all
print("\n--- Family 5: pure pair-features (varied weights) ---")
for w_eq in range(-3, 4):
    for w_diff in range(-3, 4):
        if w_eq == 0 and w_diff == 0: continue
        def p(el, n, we=w_eq, wd=w_diff):
            s = 0
            for i in range(n):
                for j in range(i+1, n):
                    if el[i] == el[j]:
                        s += we
                    else:
                        s += wd
            return float(s)
        sz = cap_set_size(p, n)
        if sz > best:
            best = sz
            best_desc = f"pair_eq*{w_eq}+pair_diff*{w_diff}"
            print(f"  NEW BEST {best}")

print(f"\n=== Final best: {best} ({best_desc}) ===  [{time.time()-t0:.1f}s elapsed]")
