"""Try tensor product of 20-cap-in-F3^4 with itself."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
m = import_module("000-batch-tester")
bench = m.bench
cap_set_size = m.cap_set_size

n = 8

# 20-cap in F_3^4 from prior experiment
CAP_20 = frozenset([
    (0,0,2,2),(0,1,2,2),(0,2,0,2),(0,2,1,2),(0,2,2,0),(0,2,2,1),
    (1,0,2,2),(1,1,2,2),(1,2,0,2),(1,2,1,2),(1,2,2,0),(1,2,2,1),
    (2,0,0,0),(2,0,0,1),(2,0,1,0),(2,0,1,1),
    (2,1,0,0),(2,1,0,1),(2,1,1,0),(2,1,1,1),
])

def p_tensor_cap20(e, n):
    a = e[:4]
    b = e[4:]
    if a in CAP_20 and b in CAP_20:
        return 1.0
    return 0.0

def p_tensor_cap20_within(e, n):
    a = e[:4]
    b = e[4:]
    if a in CAP_20 and b in CAP_20:
        return 100.0
    elif a in CAP_20 or b in CAP_20:
        return 50.0
    return 0.0

bench("tensor 20×20 (high vs rest)", p_tensor_cap20, n)
bench("tensor 20×20 graded", p_tensor_cap20_within, n)

# Try with tensor + c2-balance for tiebreak
def p_tensor_then_c2(e, n):
    a = e[:4]
    b = e[4:]
    if a in CAP_20 and b in CAP_20:
        return 1000.0
    c2 = sum(1 for x in e if x == 2)
    return -abs(c2 - 3) * 1.0

bench("tensor 20×20 then c2=3", p_tensor_then_c2, n)

# What if we use 9-cap × cap-something?
# 9-cap in F_3^3: known one
CAP_9_n3 = []
# Try priority 1 to find 9-cap at n=3
elements3 = list(itertools.product(range(3), repeat=3))
elements3.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 1), reverse=True)
cap = []
forb = set()
for e in elements3:
    if e in forb: continue
    for u in cap:
        c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap.append(e)
    forb.add(e)
print(f"\nFound cap at n=3 via c2=1: size {len(cap)}")
CAP_9_n3 = frozenset(cap)
print(f"  cap: {sorted(CAP_9_n3)}")

# Larger cap at n=5
elements5 = list(itertools.product(range(3), repeat=5))
elements5.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2), reverse=True)
cap5 = []
forb = set()
for e in elements5:
    if e in forb: continue
    for u in cap5:
        c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap5.append(e)
    forb.add(e)
print(f"\nFound cap at n=5 via c2=2: size {len(cap5)}")
CAP_n5 = frozenset(cap5)

# n=3 ⊗ n=5
def p_tensor_3x5(e, n):
    a = e[:3]
    b = e[3:]
    if a in CAP_9_n3 and b in CAP_n5:
        return 100.0
    return 0.0

bench(f"tensor n3({len(CAP_9_n3)}) × n5({len(CAP_n5)})", p_tensor_3x5, n)

# n=2 ⊗ n=6
elements2 = list(itertools.product(range(3), repeat=2))
elements2.sort(key=lambda e: 0)
cap2 = []
forb = set()
for e in elements2:
    if e in forb: continue
    for u in cap2:
        c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap2.append(e)
    forb.add(e)
print(f"\nFound cap at n=2 const: size {len(cap2)}")
CAP_n2 = frozenset(cap2)

elements6 = list(itertools.product(range(3), repeat=6))
elements6.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2), reverse=True)
cap6 = []
forb = set()
for e in elements6:
    if e in forb: continue
    for u in cap6:
        c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap6.append(e)
    forb.add(e)
print(f"\nFound cap at n=6 via c2=2: size {len(cap6)}")
CAP_n6 = frozenset(cap6)

def p_tensor_2x6(e, n):
    a = e[:2]
    b = e[2:]
    if a in CAP_n2 and b in CAP_n6:
        return 100.0
    return 0.0

bench(f"tensor n2({len(CAP_n2)}) × n6({len(CAP_n6)})", p_tensor_2x6, n)

# n=1 ⊗ n=7 (binary first coord, n=7 cap)
elements7 = list(itertools.product(range(3), repeat=7))
elements7.sort(key=lambda e: -abs(sum(1 for x in e if x == 2) - 2), reverse=True)
cap7 = []
forb = set()
for e in elements7:
    if e in forb: continue
    for u in cap7:
        c = tuple((3-ui-ei)%3 for ui, ei in zip(u, e))
        forb.add(c)
    cap7.append(e)
    forb.add(e)
print(f"\nFound cap at n=7: size {len(cap7)}")
CAP_n7 = frozenset(cap7)

def p_binary_n7(e, n):
    if e[0] == 2:
        return -1000.0
    if e[1:] in CAP_n7:
        return 100.0
    return 0.0

bench(f"binary first × n7({len(CAP_n7)})", p_binary_n7, n)

# Tensor n4 × n4
def p_tensor_4x4(e, n):
    a = e[:4]
    b = e[4:]
    if a in CAP_20 and b in CAP_20:
        return 100.0
    return 0.0

bench("tensor n4(20) × n4(20)", p_tensor_4x4, n)
