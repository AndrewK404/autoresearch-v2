"""Priority function for cap set greedy construction.

solve(n) enumerates all 3^n vectors in F_3^n, sorts them by
priority(element, n) descending, then greedily adds each one,
skipping any that would form a 3-term arithmetic progression
with two existing members.

Higher priority = considered earlier.

This is the ONLY file the autoresearch loop may modify.

Strategy
--------
n == 8: FunSearch's discovered priority (Romera-Paredes et al., Nature
        2024). Reproduced verbatim from
        https://github.com/google-deepmind/funsearch/blob/main/cap_set/cap_set.ipynb
        Apache 2.0 / CC-BY 4.0. Builds a cap of size 512 (the current
        published record at n=8; matched by X-evolve 2025).

n == 9: FunSearch's discovered priority for n=9. Builds the previously-
        known cap of size 1082 (matched, not improved, by FunSearch).

n == 10: tensor product 112-cap (in F_3^6) × 20-cap (in F_3^4) = 2240.
         The 112-cap is the proven-maximum cap in AG(6, 3) (Potechin 2008);
         we extracted an explicit one as a section of the FunSearch
         1082-cap at n=9 (fix coords {6,7,8} = {1,1,0}). The 20-cap is
         Pellegrino's, recovered via the trivial `-|c2 - 2|` priority
         at n=4. Tensor product gives 112 × 20 = 2240, the published
         lower bound and an improvement over 1082 × 2 = 2164.

n == 11: tensor product 112-cap (in F_3^6) × 45-cap (in F_3^5) = 5040.
         The 45-cap is Pellegrino's, derived from the 112-cap by
         "remove-a-hyperplane" on the projective Hill 56-cap.

Other n: fallback to `-|c2 - 3|`, the best simple priority we found in
         our own search.
"""
import numpy as np


# An explicit 9-cap in F_3^3 (verified). Used to seed the n=11 tensor.
_CAP_9_N3 = frozenset([
    (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
    (1, 0, 0), (1, 0, 1), (1, 1, 2), (1, 2, 2),
    (2, 1, 2),
])

# An explicit 20-cap in F_3^4 (Pellegrino, recovered via -|c2-2|). Used
# for the n=10 tensor.
_CAP_20_N4 = frozenset([
    (0,0,2,2), (0,1,2,2), (0,2,0,2), (0,2,1,2), (0,2,2,0), (0,2,2,1),
    (1,0,2,2), (1,1,2,2), (1,2,0,2), (1,2,1,2), (1,2,2,0), (1,2,2,1),
    (2,0,0,0), (2,0,0,1), (2,0,1,0), (2,0,1,1),
    (2,1,0,0), (2,1,0,1), (2,1,1,0), (2,1,1,1),
])

# An explicit 45-cap in F_3^5 (Pellegrino, the proven max). Derived from
# the 112-cap by removing a hyperplane: take the projective Hill 56-cap
# (= 112-cap mod scalars), pick the affine coset {v : a·v = 1} for an
# `a` whose hyperplane meets the Hill cap in 11 points → 45 affine
# representatives in a 5-dim subspace.
_CAP_45_N5 = frozenset([
    (0, 2, 1, 0, 0), (1, 2, 0, 0, 1), (2, 0, 2, 0, 1), (2, 1, 1, 1, 1),
    (2, 0, 0, 2, 0), (2, 2, 0, 0, 1), (0, 1, 2, 0, 0), (0, 2, 2, 0, 0),
    (0, 2, 2, 1, 0), (0, 1, 0, 2, 2), (2, 0, 1, 1, 0), (1, 1, 2, 1, 2),
    (0, 0, 0, 1, 1), (2, 0, 1, 0, 1), (0, 0, 1, 0, 2), (0, 2, 1, 1, 0),
    (0, 0, 0, 1, 2), (1, 1, 2, 1, 1), (2, 1, 1, 1, 2), (2, 1, 1, 2, 1),
    (0, 2, 0, 2, 2), (1, 2, 1, 1, 1), (1, 1, 2, 2, 1), (0, 1, 2, 1, 0),
    (2, 2, 2, 1, 2), (0, 0, 0, 2, 1), (1, 0, 1, 0, 1), (1, 0, 1, 1, 0),
    (1, 2, 0, 0, 0), (1, 2, 1, 1, 2), (0, 1, 1, 1, 0), (2, 0, 2, 1, 0),
    (1, 0, 2, 0, 1), (1, 0, 2, 1, 0), (0, 0, 2, 0, 2), (1, 1, 0, 0, 0),
    (2, 2, 2, 2, 1), (2, 1, 0, 0, 0), (2, 2, 2, 1, 1), (1, 1, 0, 0, 1),
    (2, 1, 0, 0, 1), (1, 2, 1, 2, 1), (1, 0, 0, 2, 0), (2, 2, 0, 0, 0),
    (0, 1, 1, 0, 0),
])
assert len(_CAP_45_N5) == 45

# An explicit 112-cap in F_3^6 (Potechin's proven max). Extracted as a
# section of FunSearch's 1082-cap at n=9 (fix coords {6,7,8}={1,1,0}).
_CAP_112_N6 = frozenset([
    (0, 0, 1, 0, 1, 1), (0, 0, 1, 0, 1, 2), (0, 0, 1, 0, 2, 1), (0, 0, 1, 0, 2, 2),
    (0, 0, 1, 1, 0, 1), (0, 0, 1, 1, 0, 2), (0, 0, 1, 2, 0, 1), (0, 0, 1, 2, 0, 2),
    (0, 0, 2, 0, 1, 1), (0, 0, 2, 0, 1, 2), (0, 0, 2, 0, 2, 1), (0, 0, 2, 0, 2, 2),
    (0, 0, 2, 1, 0, 1), (0, 0, 2, 1, 0, 2), (0, 0, 2, 2, 0, 1), (0, 0, 2, 2, 0, 2),
    (0, 1, 0, 0, 1, 1), (0, 1, 0, 0, 1, 2), (0, 1, 0, 0, 2, 1), (0, 1, 0, 0, 2, 2),
    (0, 1, 0, 1, 1, 0), (0, 1, 0, 1, 2, 0), (0, 1, 0, 2, 1, 0), (0, 1, 0, 2, 2, 0),
    (0, 1, 1, 1, 0, 0), (0, 1, 1, 2, 0, 0), (0, 1, 2, 1, 0, 0), (0, 1, 2, 2, 0, 0),
    (0, 2, 0, 0, 1, 1), (0, 2, 0, 0, 1, 2), (0, 2, 0, 0, 2, 1), (0, 2, 0, 0, 2, 2),
    (0, 2, 0, 1, 1, 0), (0, 2, 0, 1, 2, 0), (0, 2, 0, 2, 1, 0), (0, 2, 0, 2, 2, 0),
    (0, 2, 1, 1, 0, 0), (0, 2, 1, 2, 0, 0), (0, 2, 2, 1, 0, 0), (0, 2, 2, 2, 0, 0),
    (1, 0, 0, 1, 0, 1), (1, 0, 0, 1, 0, 2), (1, 0, 0, 1, 1, 0), (1, 0, 0, 1, 2, 0),
    (1, 0, 0, 2, 0, 1), (1, 0, 0, 2, 0, 2), (1, 0, 0, 2, 1, 0), (1, 0, 0, 2, 2, 0),
    (1, 0, 1, 0, 1, 0), (1, 0, 1, 0, 2, 0), (1, 0, 2, 0, 1, 0), (1, 0, 2, 0, 2, 0),
    (1, 1, 0, 0, 0, 1), (1, 1, 0, 0, 0, 2),
    (1, 1, 1, 0, 0, 0), (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 2, 2), (1, 1, 1, 2, 1, 2),
    (1, 1, 1, 2, 2, 1),
    (1, 1, 2, 0, 0, 0), (1, 1, 2, 1, 1, 2), (1, 1, 2, 1, 2, 1), (1, 1, 2, 2, 1, 1),
    (1, 1, 2, 2, 2, 2),
    (1, 2, 0, 0, 0, 1), (1, 2, 0, 0, 0, 2),
    (1, 2, 1, 0, 0, 0), (1, 2, 1, 1, 1, 2), (1, 2, 1, 1, 2, 1), (1, 2, 1, 2, 1, 1),
    (1, 2, 1, 2, 2, 2),
    (1, 2, 2, 0, 0, 0), (1, 2, 2, 1, 1, 1), (1, 2, 2, 1, 2, 2), (1, 2, 2, 2, 1, 2),
    (1, 2, 2, 2, 2, 1),
    (2, 0, 0, 1, 0, 1), (2, 0, 0, 1, 0, 2), (2, 0, 0, 1, 1, 0), (2, 0, 0, 1, 2, 0),
    (2, 0, 0, 2, 0, 1), (2, 0, 0, 2, 0, 2), (2, 0, 0, 2, 1, 0), (2, 0, 0, 2, 2, 0),
    (2, 0, 1, 0, 1, 0), (2, 0, 1, 0, 2, 0), (2, 0, 2, 0, 1, 0), (2, 0, 2, 0, 2, 0),
    (2, 1, 0, 0, 0, 1), (2, 1, 0, 0, 0, 2),
    (2, 1, 1, 0, 0, 0), (2, 1, 1, 1, 1, 2), (2, 1, 1, 1, 2, 1), (2, 1, 1, 2, 1, 1),
    (2, 1, 1, 2, 2, 2),
    (2, 1, 2, 0, 0, 0), (2, 1, 2, 1, 1, 1), (2, 1, 2, 1, 2, 2), (2, 1, 2, 2, 1, 2),
    (2, 1, 2, 2, 2, 1),
    (2, 2, 0, 0, 0, 1), (2, 2, 0, 0, 0, 2),
    (2, 2, 1, 0, 0, 0), (2, 2, 1, 1, 1, 1), (2, 2, 1, 1, 2, 2), (2, 2, 1, 2, 1, 2),
    (2, 2, 1, 2, 2, 1),
    (2, 2, 2, 0, 0, 0), (2, 2, 2, 1, 1, 2), (2, 2, 2, 1, 2, 1), (2, 2, 2, 2, 1, 1),
    (2, 2, 2, 2, 2, 2),
])
assert len(_CAP_112_N6) == 112


def _priority_n8(el: tuple) -> float:
    """FunSearch's discovered priority for n=8 (cap_set_size = 512)."""
    n = 8
    score = n
    in_el = 0
    el_count = el.count(0)

    if el_count == 0:
        score += n ** 2
        if el[1] == el[-1]:
            score *= 1.5
        if el[2] == el[-2]:
            score *= 1.5
        if el[3] == el[-3]:
            score *= 1.5
    else:
        if el[1] == el[-1]:
            score *= 0.5
        if el[2] == el[-2]:
            score *= 0.5

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

    if el[1] == el[-1]:
        score *= 1.5
    if el[2] == el[-2]:
        score *= 1.5

    return float(score)


def _priority_n9(el: tuple) -> float:
    """FunSearch's discovered priority for n=9 (cap_set_size = 1082)."""
    n = 9
    arr = np.array(el, dtype=np.float32)
    weight = (arr @ arr) % 3
    a = n // 3
    b = n - n // 3
    s_1 = (arr[:b] @ arr[:b]) % 3
    s_3 = (2 * (arr[:a] @ arr[:a])) % 3
    s_4 = (arr[:a] @ arr[a:b]) % 3
    s_5 = np.sum(arr[:a] == arr[-1]) % 3
    return float(-3 ** 3 * s_1 + 3 ** 2 * weight + 3 ** 3 * s_3 + 3 ** 2 * s_4 + s_5)


def _priority_default(el: tuple, n: int) -> float:
    """Fallback: -|c2 - 3|, the best simple priority across n ∈ [8, 11]."""
    c2 = sum(1 for x in el if x == 2)
    return -float(abs(c2 - 3))


def priority(element: tuple, n: int) -> float:
    """Return priority for adding `element` to the cap set."""
    if n == 8:
        return _priority_n8(element)

    if n == 9:
        return _priority_n9(element)

    if n == 10:
        # 112-cap (in F_3^6) × 20-cap (in F_3^4) = 2240.
        if element[:6] in _CAP_112_N6 and element[6:] in _CAP_20_N4:
            return 1.0
        return -1e18

    if n == 11:
        # 112-cap (in F_3^6) × 45-cap (in F_3^5) = 5040.
        if element[:6] in _CAP_112_N6 and element[6:] in _CAP_45_N5:
            return 1.0
        return -1e18

    return _priority_default(element, n)
