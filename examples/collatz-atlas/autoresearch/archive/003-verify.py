"""
003-verify.py — empirical verification of conjugacy/sub-system claims for the
generalized Collatz family

  n even: T_{a,b}(n) = n / 2
  n odd:  T_{a,b}(n) = a*n + b

with a, b positive odd integers.

Run with the project venv:
    source .venv/bin/activate
    python archive/003-verify.py

This is a verification harness, not a sweep. Each check prints PASS/FAIL.
"""

from __future__ import annotations
from typing import Callable, Iterable

# ---------------------------------------------------------------------------
# Core map
# ---------------------------------------------------------------------------

def T(a: int, b: int, n: int) -> int:
    """One step of T_{a,b}.  n must be a positive integer."""
    if n % 2 == 0:
        return n // 2
    return a * n + b


def trajectory(a: int, b: int, n0: int, steps: int) -> list[int]:
    """First `steps` iterates of T_{a,b} starting from n0 (length steps+1)."""
    out = [n0]
    n = n0
    for _ in range(steps):
        n = T(a, b, n)
        out.append(n)
    return out


# ---------------------------------------------------------------------------
# Substitution helpers
# ---------------------------------------------------------------------------

def commutes(
    phi: Callable[[int], int],
    a: int, b: int,
    a2: int, b2: int,
    seeds: Iterable[int],
    steps: int = 60,
) -> tuple[bool, str]:
    """
    Check whether T_{a2,b2}(phi(n)) == phi(T_{a,b}(n)) for `steps` iterations
    starting from each seed n in seeds.  Returns (all_ok, message).
    """
    for n0 in seeds:
        n = n0
        for k in range(steps):
            lhs = T(a2, b2, phi(n))
            rhs = phi(T(a, b, n))
            if lhs != rhs:
                return (
                    False,
                    f"  FAIL seed={n0} step={k} n={n}: "
                    f"T_{{{a2},{b2}}}(phi(n))={lhs}  phi(T_{{{a},{b}}}(n))={rhs}",
                )
            n = T(a, b, n)
    return True, f"  ok on seeds {list(seeds)} for {steps} steps"


def report(label: str, ok: bool, msg: str) -> None:
    flag = "PASS" if ok else "FAIL"
    print(f"[{flag}] {label}\n{msg}")


# ---------------------------------------------------------------------------
# 1.  Trivial b-scaling:   phi(n) = lambda * n,   maps T_{a,b} -> T_{a, lambda*b}
#     This is a sub-system embedding: phi sends Z>0 into lambda*Z>0, and the
#     dynamics of T_{a, lambda*b} restricted to multiples of lambda is a copy
#     of T_{a,b} on all of Z>0.
# ---------------------------------------------------------------------------

def check_b_scaling():
    print("\n=== 1. b-scaling sub-system embedding ===")
    print("Claim: phi(n) = lambda*n satisfies T_{a, lambda*b}(phi(n)) = phi(T_{a,b}(n))")
    print("       i.e. (a, b) embeds into (a, lambda*b) on the multiples-of-lambda fiber.")
    cases = [
        # (a, b, lam, seeds)
        (3, 1, 3, [1, 2, 3, 5, 7, 11]),    # 3n+1 -> 3n+3 on 3Z
        (3, 1, 5, [1, 2, 4, 7, 9]),        # 3n+1 -> 3n+5 on 5Z
        (5, 1, 3, [1, 2, 3, 4, 7]),        # 5n+1 -> 5n+3 on 3Z
        (3, 3, 3, [1, 2, 3, 5, 7]),        # 3n+3 -> 3n+9 on 3Z
        (7, 1, 3, [1, 2, 4, 5]),
    ]
    for a, b, lam, seeds in cases:
        phi = lambda n, L=lam: L * n
        ok, msg = commutes(phi, a, b, a, lam * b, seeds, steps=80)
        report(f"(a={a}, b={b}) -> (a={a}, b={lam*b}) via n -> {lam}n", ok, msg)


# ---------------------------------------------------------------------------
# 2.  GCD reduction near (a=3, b=3)
#     On odd multiples of 3, T_{3,3}(n) = 3n+3 = 3(n+1); halving preserves the
#     factor of 3 only if n+1 is odd, i.e. n=...something.  Trace this carefully.
#     Specifically, T_{3,3} on 3Z is conjugate to T_{3,1} on Z via phi(n)=3n.
#     But T_{3,3} on integers is NOT conjugate to T_{3,1} on integers, because
#     {3Z} is not preserved by T_{3,3}: e.g. T_{3,3}(1)=6, T_{3,3}(6)=3, so
#     non-multiples of 3 enter the multiples-of-3 fiber.  Once inside 3Z, the
#     orbit obeys T_{3,1} dynamics under phi^{-1}.
# ---------------------------------------------------------------------------

def check_gcd_reduction():
    print("\n=== 2. GCD reduction:  (3, 3) on 3Z mirrors (3, 1) on Z ===")
    phi = lambda n: 3 * n
    ok, msg = commutes(phi, 3, 1, 3, 3, [1, 2, 3, 5, 7, 11, 27], steps=120)
    report("(3, 1) -> (3, 3) via n -> 3n  [sub-system on 3Z]", ok, msg)

    # Show that 3Z is NOT invariant under T_{3,3} on Z>0:
    print("  Note: 3Z is not forward-invariant under T_{3,3} starting from non-3Z.")
    for n0 in [1, 5, 7]:
        traj = trajectory(3, 3, n0, 8)
        print(f"    n0={n0} (mod 3 = {n0%3}): {traj}")

    # And (3, 9) on 3Z mirrors (3, 3) on Z:
    print("\n=== 2b. (3, 9) on 3Z mirrors (3, 3) on Z (chained b-scaling) ===")
    ok, msg = commutes(phi, 3, 3, 3, 9, [1, 2, 3, 5, 7], steps=80)
    report("(3, 3) -> (3, 9) via n -> 3n", ok, msg)


# ---------------------------------------------------------------------------
# 3.  (a, b) vs (a, b + 2*a*m): no, this does not give a conjugacy.
#     Halving is the same regardless of b, but the odd branch a*n + b vs
#     a*n + b' differs by (b - b') for every odd-step.  The discrepancy
#     accumulates.  Confirm by counterexample.
# ---------------------------------------------------------------------------

def check_b_shift():
    print("\n=== 3. Periodicity-style b shift  (a, b) vs (a, b + 2a*m) ===")
    print("Claim under test: identity phi(n) = n.  Expected: FAIL — no conjugacy.")
    phi = lambda n: n
    a, b, m = 3, 1, 1                # (3, 1) vs (3, 7)
    ok, msg = commutes(phi, a, b, a, b + 2 * a * m, [1, 3, 5], steps=10)
    report(f"(a=3, b=1) =?= (a=3, b=7) via identity", ok, msg)
    # Explicit comparison of trajectories
    print("  trajectories diverge:")
    print(f"    (3,1) from 1: {trajectory(3, 1, 1, 8)}")
    print(f"    (3,7) from 1: {trajectory(3, 7, 1, 8)}")


# ---------------------------------------------------------------------------
# 4.  Branch-swap / parity reflection:  phi(n) = c - n  or phi(n) = -n.
#     With positive odd a, b and the map confined to positive integers, n -> -n
#     leaves the positive-integer domain.  Even on Z, the parity of -n equals
#     parity of n only when n is even (since -odd is odd, -even is even — both
#     parities are preserved).  Then T_{a,b}(-n) on odd -n:
#         a*(-n) + b = -a*n + b
#     which equals -(a*n - b) = -T_{a,-b}(n).  So phi(n) = -n conjugates
#     T_{a,b} (on Z) to T_{a,-b} (on Z).  Within our scope b > 0, this leaves
#     the positive-b family.  Not useful for in-scope identifications, but
#     worth recording.
# ---------------------------------------------------------------------------

def check_branch_swap():
    print("\n=== 4. Sign reflection phi(n) = -n :  T_{a,b} on Z conjugate to T_{a,-b} on Z ===")
    # Verify on Z (allowing negative integers):
    def T_signed(a, b, n):
        if n % 2 == 0:        # Python //: -3 % 2 == 1, -4 % 2 == 0 — OK
            return n // 2
        return a * n + b

    a, b = 3, 1
    phi = lambda n: -n
    seeds = [1, 2, 3, 5, 7, 11]
    ok = True
    msg = "  ok on signed integers"
    for n0 in seeds:
        n = n0
        for k in range(40):
            lhs = T_signed(a, -b, phi(n))
            rhs = phi(T_signed(a, b, n))
            if lhs != rhs:
                ok = False
                msg = f"  FAIL seed={n0} step={k} n={n} lhs={lhs} rhs={rhs}"
                break
            n = T_signed(a, b, n)
        if not ok:
            break
    report(f"(a={a}, b={b}) on Z -> (a={a}, b={-b}) on Z via n -> -n", ok, msg)
    print("  In-scope (b>0) implication: none — sign flip leaves the b>0 family.")


# ---------------------------------------------------------------------------
# 5.  Affine substitution phi(n) = alpha*n + beta.
#     Algebra:
#       Even n: T_{a,b}(n) = n/2.  phi(n/2) = alpha*n/2 + beta.
#       For T_{a',b'} on phi(n): we need parity of phi(n) = parity of n
#         (so that the "even" branch on phi(n) coincides with even on n).
#         alpha*n + beta has parity = (alpha*n + beta) mod 2.  For this to
#         equal n mod 2 for all n, we need alpha odd and beta even.
#       Even n, phi(n) even: T_{a',b'}(phi(n)) = phi(n)/2 = (alpha*n + beta)/2.
#         Want = phi(n/2) = alpha*n/2 + beta.  So beta/2 = beta -> beta = 0.
#       Therefore beta = 0, alpha odd.
#       Odd n: T_{a,b}(n) = a*n + b.  phi(T_{a,b}(n)) = alpha*(a*n+b).
#         Odd n, phi(n)=alpha*n odd: T_{a',b'}(phi(n)) = a'*alpha*n + b'.
#         Match: a'*alpha*n + b' = alpha*a*n + alpha*b
#                -> a' = a, b' = alpha*b.
#     Conclusion: the only orientation-preserving affine integer conjugacies
#     are phi(n) = alpha*n with alpha odd, giving (a, b) ~ (a, alpha*b) as a
#     SUB-SYSTEM (image is alpha*Z), not a full conjugacy of N>0.
#
#     Allowing beta != 0: would require parity-twisting, but parity of
#     alpha*n + beta with beta odd flips parity, sending the even branch to
#     the odd branch — that's a different (branch-swapped) variant, not in
#     our family.
# ---------------------------------------------------------------------------

def check_affine():
    print("\n=== 5. Affine substitution phi(n) = alpha*n + beta ===")
    print("Derivation forces beta = 0 and alpha odd, giving (a, b) -> (a, alpha*b).")
    print("Confirm the alpha=odd, beta=0 case (already covered in #1):")
    cases = [(3, 1, 3), (3, 1, 5), (3, 1, 7), (5, 3, 3), (7, 1, 3)]
    for a, b, alpha in cases:
        phi = lambda n, A=alpha: A * n
        ok, msg = commutes(phi, a, b, a, alpha * b, [1, 2, 5, 9, 11, 17], steps=60)
        report(f"alpha={alpha}, beta=0: (a={a}, b={b}) -> (a={a}, b={alpha*b})", ok, msg)

    print("\nNow show that beta != 0 fails parity-matching:")
    a, b, alpha, beta = 3, 1, 1, 2
    a2, b2 = 3, 1
    phi = lambda n, A=alpha, B=beta: A * n + B
    ok, msg = commutes(phi, a, b, a2, b2, [1, 2, 3], steps=5)
    print(f"  attempt: phi(n)=n+2, (3,1) -> (3,1):  ok={ok}")
    if not ok:
        print(msg)


# ---------------------------------------------------------------------------
# Bonus.  a-scaling?  Try phi(n) = alpha*n, mapping (a, b) -> (?, ?).
#   Already shown above: only (a, b) -> (a, alpha*b).  a is preserved.
#   So there is no integer affine substitution that changes a.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Normal form for the in-scope grid a in {1,3,5,7}, b odd in [1,21].
# ---------------------------------------------------------------------------

from math import gcd

def normal_form(a: int, b: int) -> tuple[int, int]:
    """
    Return the canonical (a*, b*) in the sub-system equivalence class.

    Convention:
      Two pairs (a, b) and (a, b') are 'sub-system equivalent' when there
      exists an odd integer alpha such that b' = alpha * b OR b = alpha * b'.
      Equivalently they share the same odd squarefree-or-not divisor structure
      relative to b's "primitive" part.

    Concretely the orbit of (a, b) on multiples of d = gcd(?, b) will contain
    a copy of (a, b/lambda) for each odd lambda | b.  The minimal-b
    representative under sub-system embedding is therefore (a, 1) — but ONLY
    on the lambda-fiber.  Since the embedding is one-way (sub-system, not
    full conjugacy), the canonical choice for the atlas is to keep b as-is
    UNLESS we are explicitly studying the lambda-fiber of (a, lambda*b).

    For atlas bookkeeping we adopt the strict-conjugacy normal form:
      normal_form(a, b) = (a, b)         # no nontrivial full conjugacy
    and separately tag which (a, b) pairs are sub-system-related.
    """
    return (a, b)


def subsystem_parent(a: int, b: int) -> tuple[int, int] | None:
    """
    If (a, b) = (a, lambda * b0) with b0 < b odd and lambda > 1 odd, return
    the smallest such (a, b0); otherwise None.  This is the (a, b0) variant
    whose dynamics appear inside (a, b)'s orbit on multiples of lambda.
    """
    best = None
    for lam in range(3, b + 1, 2):           # odd lam > 1
        if b % lam == 0:
            b0 = b // lam
            if b0 % 2 == 1 and b0 >= 1:
                cand = (a, b0)
                if best is None or cand[1] < best[1]:
                    best = cand
    return best


def show_atlas_table():
    print("\n=== Normal-form / sub-system table for in-scope grid ===")
    print(f"{'a':>3} {'b':>3}  {'normal_form':>12}  {'sub-system parent':>18}")
    for a in (1, 3, 5, 7):
        for b in range(1, 22, 2):
            nf = normal_form(a, b)
            sp = subsystem_parent(a, b)
            sp_str = "—" if sp is None else f"{sp}"
            print(f"{a:>3} {b:>3}  {str(nf):>12}  {sp_str:>18}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    check_b_scaling()
    check_gcd_reduction()
    check_b_shift()
    check_branch_swap()
    check_affine()
    show_atlas_table()
