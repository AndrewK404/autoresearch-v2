"""Priority via sub-tuple membership in known good caps."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench
cap_set_size = m.cap_set_size

n = 8

# 20-cap at n=4
CAP_20 = frozenset([
    (0,0,2,2),(0,1,2,2),(0,2,0,2),(0,2,1,2),(0,2,2,0),(0,2,2,1),
    (1,0,2,2),(1,1,2,2),(1,2,0,2),(1,2,1,2),(1,2,2,0),(1,2,2,1),
    (2,0,0,0),(2,0,0,1),(2,0,1,0),(2,0,1,1),
    (2,1,0,0),(2,1,0,1),(2,1,1,0),(2,1,1,1),
])

# 9-cap at n=3 from earlier
CAP_9 = None

# Get a good 9-cap by greedy at n=3
def get_n3_cap():
    elements = list(itertools.product(range(3), repeat=3))
    elements.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 1), reverse=True)
    cap = []
    forb = set()
    for e in elements:
        if e in forb: continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

CAP_n3 = frozenset(get_n3_cap())
print(f"n=3 cap size: {len(CAP_n3)}")

# Priority based on number of 4-tuples (out of all combinations) that land in CAP_20
def p_subset_count_4(el, n):
    s = 0
    for combo in itertools.combinations(range(n), 4):
        sub = tuple(el[i] for i in combo)
        if sub in CAP_20:
            s += 1
    return float(s)

bench("count of 4-tuples in CAP_20", p_subset_count_4, n)

def p_subset_count_4_neg(el, n):
    s = 0
    for combo in itertools.combinations(range(n), 4):
        sub = tuple(el[i] for i in combo)
        if sub in CAP_20:
            s += 1
    return -float(s)

bench("count of 4-tuples in CAP_20 (low)", p_subset_count_4_neg, n)

# Number of 3-tuples in CAP_n3
def p_subset_count_3(el, n):
    s = 0
    for combo in itertools.combinations(range(n), 3):
        sub = tuple(el[i] for i in combo)
        if sub in CAP_n3:
            s += 1
    return float(s)

bench("count of 3-tuples in CAP_n3 (high)", p_subset_count_3, n)

def p_subset_count_3_neg(el, n):
    s = 0
    for combo in itertools.combinations(range(n), 3):
        sub = tuple(el[i] for i in combo)
        if sub in CAP_n3:
            s += 1
    return -float(s)

bench("count of 3-tuples in CAP_n3 (low)", p_subset_count_3_neg, n)

# Combined
def p_combo(el, n):
    c2 = sum(1 for x in el if x == 2)
    primary = -abs(c2 - 3) * 1_000_000
    s4 = sum(1 for combo in itertools.combinations(range(n), 4)
             if tuple(el[i] for i in combo) in CAP_20)
    return primary + s4 * 1.0

bench("c2=3 + cap_n4 count", p_combo, n)

# Try: "fractal" - 8 = 4+4, encode as (CAP_20, CAP_20)
def p_fractal_44(el, n):
    a = el[:4]
    b = el[4:]
    if a in CAP_20 and b in CAP_20:
        return 100.0
    elif a in CAP_20:
        return 50.0
    elif b in CAP_20:
        return 50.0
    return 0.0

bench("fractal 4+4 over CAP_20", p_fractal_44, n)

# Try a 9 × 9 where we use F_3^3 cap (9-cap doesn't exist, only 9 for n=3? wait n=3 max is 9, so yes)
# 8 = 3 + 5, 3 + 3 + 2, etc.

# 3+5: CAP_n3 × ?
# 3+3+2: CAP_n3 × CAP_n3 × {0,1}^2

def p_335(el, n):
    a = el[:3]
    b = el[3:6]
    c = el[6:]
    if a in CAP_n3 and b in CAP_n3 and c in [(0,0),(0,1),(1,0),(1,1)]:
        return 100.0
    return 0.0

bench("3+3+2 split", p_335, n)

# Different split
def p_53(el, n):
    a = el[:5]
    b = el[5:]
    if b in CAP_n3:
        return 50.0  # but a is unconstrained
    return 0.0

bench("any first 5 + cap_n3 second", p_53, n)

# Cap at n=5 via priority
def get_n5_cap():
    elements = list(itertools.product(range(3), repeat=5))
    elements.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2), reverse=True)
    cap = []
    forb = set()
    for e in elements:
        if e in forb: continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

CAP_n5 = frozenset(get_n5_cap())
print(f"n=5 cap size: {len(CAP_n5)}")

def get_n2_cap():
    return frozenset([(0,0),(0,1),(1,0),(1,1)])

CAP_n2 = get_n2_cap()

def p_3_5(el, n):
    a = el[:3]
    b = el[3:]
    if a in CAP_n3 and b in CAP_n5:
        return 100.0
    return 0.0

bench("3+5 split (cap_n3 × cap_n5)", p_3_5, n)

def p_2_6(el, n):
    a = el[:2]
    b = el[2:]
    if a in CAP_n2 and b in [...]:
        return 100.0
    return 0.0

# Larger n=6 cap
def get_n6_cap():
    elements = list(itertools.product(range(3), repeat=6))
    elements.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2), reverse=True)
    cap = []
    forb = set()
    for e in elements:
        if e in forb: continue
        for u in cap:
            c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
            forb.add(c)
        cap.append(e)
        forb.add(e)
    return cap

CAP_n6 = frozenset(get_n6_cap())
print(f"n=6 cap size: {len(CAP_n6)}")

def p_2_6_real(el, n):
    a = el[:2]
    b = el[2:]
    if a in CAP_n2 and b in CAP_n6:
        return 100.0
    return 0.0

bench("2+6 split (cap_n2 × cap_n6)", p_2_6_real, n)

# Now layered: prioritize cap_n4 × cap_n4, then c2=3 fill
def p_layered(el, n):
    a = el[:4]
    b = el[4:]
    if a in CAP_20 and b in CAP_20:
        return 1000.0
    c2 = sum(1 for x in el if x == 2)
    return -abs(c2 - 3) * 1.0

bench("cap_n4 × cap_n4 then c2=3 fill", p_layered, n)

# And with secondary lex
def p_layered2(el, n):
    a = el[:4]
    b = el[4:]
    if a in CAP_20 and b in CAP_20:
        return 1000.0 - sum(x * 3**i for i, x in enumerate(el))
    c2 = sum(1 for x in el if x == 2)
    return -abs(c2 - 3) * 1.0
bench("layered with lex tiebreak", p_layered2, n)
