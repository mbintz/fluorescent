"""Collision thresholds for trapped, Jastrow-dressed SU(2)_3 spin-1 blocks.

Run python3 fibonacci_collision.py. The table uses exact rational arithmetic.
Pass --max-n N to extend it, or --witness N {1,tau} for a maximizing tree.
"""

import argparse
import cmath
import math
from fractions import Fraction as Q
from functools import cache
from itertools import combinations, product


VAC, TAU = "1", "tau"
WEIGHT = {VAC: Q(0), TAU: Q(2, 5)}


def fuse(left, right):
    if left == VAC:
        return (right,)
    if right == VAC:
        return (left,)
    return (VAC, TAU)


def charges(particles):
    if particles == 0:
        return (VAC,)
    if particles == 1:
        return (TAU,)
    return (VAC, TAU)


def margin(size, charge, alpha):
    return size - 1 + WEIGHT[charge] - size * WEIGHT[TAU] - math.comb(size, 2) * alpha


def threshold(size, charge):
    return margin(size, charge, 0) / math.comb(size, 2)


def critical_coupling(particles, total):
    """A cluster of charge c must fuse with the complement to the given total."""
    return min(
        threshold(size, charge)
        for size in range(2, particles + 1)
        for charge in charges(size)
        if any(total in fuse(charge, rest) for rest in charges(particles - size))
    )


@cache
def critical_tree(size, total, alpha):
    """Maximize the number of simultaneous critical scales in a fusion tree."""
    if size == 1:
        return 0, "t"
    critical = int(margin(size, total, alpha) == 0)
    best_score, best_tree = -1, None
    for left_size in range(1, size // 2 + 1):
        right_size = size - left_size
        for left, right in product(charges(left_size), charges(right_size)):
            if total not in fuse(left, right):
                continue
            l_score, l_tree = critical_tree(left_size, left, alpha)
            r_score, r_tree = critical_tree(right_size, right, alpha)
            score = l_score + r_score + critical
            if score > best_score:
                mark = "*" if critical else ""
                best_score, best_tree = score, f"({l_tree} {r_tree})[{total}{mark}]"
    return best_score, best_tree


def check_small_trees():
    # Enumerate all ordered binary fusions, carrying the smallest threshold and
    # its multiplicity. This independently checks the complement test and the
    # maximization at fixed alpha. Particle permutations give the same weights.
    @cache
    def enumerate_trees(size):
        if size == 1:
            return [(TAU, None, 0)]
        records = []
        for left_size in range(1, size):
            for left, la, lp in enumerate_trees(left_size):
                for right, ra, rp in enumerate_trees(size - left_size):
                    for charge in fuse(left, right):
                        a = threshold(size, charge)
                        entries = [(x, p) for x, p in ((la, lp), (ra, rp), (a, 1)) if x is not None]
                        first = min(x for x, p in entries)
                        records.append((charge, first, sum(p for x, p in entries if x == first)))
        return records

    for size in range(2, 9):
        for total in charges(size):
            candidates = [(a, p) for c, a, p in enumerate_trees(size) if c == total]
            first = min(a for a, p in candidates)
            order = max(p for a, p in candidates if a == first)
            assert first == critical_coupling(size, total)
            assert order == critical_tree(size, total, first)[0]
    enumerate_trees.cache_clear()


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return 0
    return 1 if (b - a) % 3 == 1 else -1


def check_five_spin_projections():
    """Contract two singlet pairs on the invariant five-vector tensors δ ε."""
    for i, j in combinations(range(5), 2):
        rest = [p for p in range(5) if p not in (i, j)]

        def tensor(indices):
            if indices[i] != indices[j]:
                return 0
            return epsilon(*(indices[p] for p in rest))

        for e in range(3):
            amplitude = sum(tensor((a, a, b, b, e)) for a, b in product(range(3), repeat=2))
            assert amplitude == 0
        if (i, j) == (0, 1):
            assert sum(tensor((a, a, 0, 1, 2)) for a in range(3)) == 3


def check_six_spin_kz_residue():
    """Act with 2 sum S_i.S_j on six actual spin-one tensor factors.

    In the Cartesian vector representation, S_i.S_j exchanges indices and
    subtracts their trace. Dividing the result by k+2 gives the KZ residue.
    """
    for total in (VAC, TAU):
        def tensor(indices):
            a, b, c, d, e, f = indices
            if a != b or c != d:
                return 0
            return int(e == f) if total == VAC else epsilon(e, f, 2)

        eigenvalue = 5 * (WEIGHT[total] - 6 * WEIGHT[TAU])
        for state in product(range(3), repeat=6):
            action = 0
            for i, j in combinations(range(6), 2):
                indices = list(state)
                indices[i], indices[j] = state[j], state[i]
                action += tensor(indices)
                if state[i] == state[j]:
                    for spatial_index in range(3):
                        indices[i] = indices[j] = spatial_index
                        action -= tensor(indices)
            assert 2 * action == eigenvalue * tensor(state)


def numerical_radius(moment, nu):
    """Integrate R^moment times the unnormalized law, with ell = 1, in log R."""
    low, high, steps = -160.0, 3.0, 12000
    step = (high - low) / steps
    terms = []
    for i in range(steps + 1):
        y = low + i * step
        weight = 1 if i in (0, steps) else (4 if i % 2 else 2)
        terms.append(weight * math.exp((2 * nu + moment) * y - math.exp(2 * y) / 2))
    return math.fsum(terms) * step / 3


def check_braided_pair():
    """Return the vacuum-channel weight after one full winding of particles 2,3."""
    phi = (1 + math.sqrt(5)) / 2
    a, b = 1 / phi, 1 / math.sqrt(phi)
    recouple = ((a, b), (b, -a))
    phases = (cmath.exp(-4j * math.pi / 5), cmath.exp(3j * math.pi / 5))

    def change_basis(vector):
        return tuple(sum(x * y for x, y in zip(row, vector)) for row in recouple)

    in_23_basis = change_basis((0, 1))
    wound = tuple(phase ** 2 * entry for phase, entry in zip(phases, in_23_basis))
    in_12_basis = change_basis(wound)
    probability = abs(in_12_basis[0]) ** 2
    assert abs(probability - (3 * phi - 4)) < 1e-14
    assert abs(sum(abs(x) ** 2 for x in in_12_basis) - 1) < 1e-14
    assert margin(2, VAC, Q(1, 5)) == 0 and margin(2, TAU, Q(1, 5)) == Q(2, 5)
    return probability


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=10)
    parser.add_argument("--witness", nargs=2, metavar=("N", "CHARGE"))
    args = parser.parse_args()
    if args.max_n < 2:
        parser.error("--max-n must be at least 2")
    if args.witness:
        size_string, total = args.witness
        try:
            size = int(size_string)
        except ValueError:
            parser.error("witness N must be an integer")
        if size < 2 or total not in (VAC, TAU):
            parser.error("a witness needs N >= 2 and charge 1 or tau")
        alpha = critical_coupling(size, total)
        order, tree = critical_tree(size, total, alpha)
        print(f"alpha_c = {alpha}, order = {order}; * marks a critical scale\n{tree}")
        return

    print(" N     vacuum   order      tau   order")
    for size in range(2, args.max_n + 1):
        rows = []
        for total in (VAC, TAU):
            alpha = critical_coupling(size, total)
            order, _ = critical_tree(size, total, alpha)
            rows.extend((str(alpha), order))
        print(f"{size:2} {rows[0]:>10} {rows[1]:7} {rows[2]:>8} {rows[3]:7}")

    check_small_trees()
    check_five_spin_projections()
    check_six_spin_kz_residue()
    for size in range(6, max(31, args.max_n + 1)):
        vacuum = critical_coupling(size, VAC)
        tau = critical_coupling(size, TAU)
        assert vacuum == Q(6 * size - 10, 5 * size * (size - 1))
        assert tau == Q(6, 5 * size)
        midpoint = (vacuum + tau) / 2
        assert margin(size, TAU, midpoint) == Q(1, 5)
        assert margin(size, VAC, midpoint) == -Q(1, 5)
    radius_sq = numerical_radius(2, 0.2) / numerical_radius(0, 0.2)
    assert abs(radius_sq - 0.4) < 1e-11
    print("All ordered fusion trees through N=8 and five-spin contractions passed.")
    print("Six-spin KZ dilation residues verified on all 729 tensor components in both sectors.")
    print(f"Midpoint radius quadrature: <R^2>/ell^2 = {radius_sq:.12f}")
    print(f"Full winding: pair-contact log coefficient / vacuum control = {check_braided_pair():.12f}")


if __name__ == "__main__":
    main()
