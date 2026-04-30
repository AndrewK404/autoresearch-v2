"""Cap set evaluation. DO NOT MODIFY.

Reads CAP_SET_N from environment (default 8). Runs solve, verifies,
prints a parseable summary block. Metric: cap_set_size.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solve import solve, verify_cap_set


def main():
    n = int(os.environ.get("CAP_SET_N", "8"))
    t0 = time.time()
    cap_set = solve(n)
    elapsed = time.time() - t0

    ok, reason = verify_cap_set(cap_set, n)
    if not ok:
        print(f"STATUS: incorrect")
        print(f"REASON: {reason}")
        sys.exit(1)

    print(f"STATUS: correct")
    print(f"n: {n}")
    print(f"cap_set_size: {len(cap_set)}")
    print(f"eval_seconds: {elapsed:.2f}")


if __name__ == "__main__":
    main()
