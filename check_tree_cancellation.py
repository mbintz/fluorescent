"""Exact, small-instance checks for the two theorems in tree-cancellation.pdf."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from random import Random


def max_path_weight(edges, weights):
    best = 0
    for selected in product((False, True), repeat=len(edges)):
        degrees = Counter()
        weight = 0
        for keep, (u, v, _), w in zip(selected, edges, weights):
            if keep:
                degrees.update((u, v))
                weight += w
        if max(degrees.values(), default=0) <= 2:
            best = max(best, weight)
    return best


def phase_histogram(modulus, period, edges, tables):
    """Count phase exponents by conditioning each subtree on its root value."""
    neighbors = [[] for _ in tables]
    for u, v, coefficient in edges:
        neighbors[u].append((v, coefficient))
        neighbors[v].append((u, coefficient))

    def subtree(vertex, parent):
        counts = [Counter({phase: 1}) for phase in tables[vertex]]
        for child, coefficient in neighbors[vertex]:
            if child == parent:
                continue
            below = subtree(child, vertex)
            for x in range(modulus):
                message = Counter()
                for y, child_counts in enumerate(below):
                    edge_phase = (period // modulus) * coefficient * x * y
                    for phase, count in child_counts.items():
                        message[(phase + edge_phase) % period] += count
                combined = Counter()
                for a, left in counts[x].items():
                    for b, right in message.items():
                        combined[(a + b) % period] += left * right
                counts[x] = combined
        return counts

    histogram = sum(subtree(0, None), Counter())
    assert histogram.total() == modulus ** len(tables)
    return histogram


def check_weighted(p, k, edges, rng):
    modulus = p**k
    period = 2 * modulus if p == 2 else modulus
    n = len(edges) + 1
    exponents = {p**s: s for s in range(k + 1)}
    weights = [exponents[modulus // gcd(a, modulus)] for _, _, a in edges]
    best = max_path_weight(edges, weights)

    def dual(shifts):
        residual = sum(max(0, w - shifts[u] - shifts[v])
                       for (u, v, _), w in zip(edges, weights))
        return 2 * sum(shifts) + residual

    shifts = min(product(range(k + 1), repeat=n), key=dual)
    assert dual(shifts) == best
    tables = [[0] * modulus for _ in range(n)]
    for u, v, a in edges:
        b = a * p ** (shifts[u] + shifts[v]) % modulus
        if b == 0:
            continue
        divisor = gcd(b, modulus)
        d = modulus // divisor
        unit = b // divisor
        chirp = (-unit * (period // (2 * d)) if p == 2
                 else -unit * pow(2, -1, d) * (period // d))
        for vertex in (u, v):
            step = p ** shifts[vertex]
            for x in range(0, modulus, step):
                tables[vertex][x] += chirp * (x // step) ** 2

    # Fill off-subgroup values independently. Equality of the mean with the
    # upper bound implies every such root-of-unity filling attains equality.
    for vertex, row in enumerate(tables):
        for x in range(modulus):
            if x % (p ** shifts[vertex]):
                row[x] = rng.randrange(period)
            row[x] %= period
    hist = phase_histogram(modulus, period, edges, tables)
    squared = [0] * period
    for a, count_a in hist.items():
        for b, count_b in hist.items():
            squared[(a - b) % period] += count_a * count_b
    squared[0] -= modulus ** (2 * n) // p**best
    # For prime-power period, divisibility by its cyclotomic polynomial
    # means all coefficients in each class modulo period/p are equal.
    stride = period // p
    assert all(len(set(squared[i::stride])) == 1 for i in range(stride))
    return best


def exhaust_prime_perturbations(p, edges):
    n = len(edges) + 1
    inputs = list(product(range(p), repeat=n))
    base = [sum(a * x[u] * x[v] for u, v, a in edges) for x in inputs]
    # Adding a constant to any vertex function preserves collisions.
    choices = [(0, *values) for values in product(range(p), repeat=p - 1)]
    largest = 0
    for functions in product(choices, repeat=n):
        counts = [0] * p
        for x, phase in zip(inputs, base):
            value = phase + sum(row[t] for row, t in zip(functions, x))
            counts[value % p] += 1
        largest = max(largest, sum(c * c for c in counts))
    r = max_path_weight(edges, [1] * len(edges))
    answer = Fraction(largest, len(inputs) ** 2)
    assert answer == Fraction(1, p) + Fraction(p - 1, p ** (r + 1))
    return answer


def main():
    rng = Random(20261120)
    for p, k in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 2)]:
        for n in range(1, 8):
            for _ in range(4):
                edges = [(rng.randrange(v), v,
                          rng.randrange(1, p**k) * p**rng.randrange(k + 1))
                         for v in range(1, n)]
                check_weighted(p, k, edges, rng)
    star = [(0, i, a) for i, a in enumerate([1, 3, 9, 9], start=1)]
    assert check_weighted(3, 3, star, rng) == 5
    print("Verified the extremizing sums on 168 small prime-power cases and the mod-27 star.")

    path = [(0, 1, 1), (1, 2, 2), (2, 3, 1)]
    claw = [(0, 1, 1), (0, 2, 2), (0, 3, 1)]
    print("Ternary four-vertex path maximum:", exhaust_prime_perturbations(3, path))
    print("Ternary three-leaf star maximum:", exhaust_prime_perturbations(3, claw))
    print("Five-element field, single edge maximum:", exhaust_prime_perturbations(5, [(0, 1, 1)]))

    edges = [(0, v, 1) for v in range(1, 5)] + [(v, v + 4, 1) for v in range(1, 5)]
    # S = {0}. In F_3 the coefficient -1/2 on each outer edge endpoint is 1.
    tables = [[0, 0, 0]] + [[0, 1, 1] for _ in range(8)]
    hist = phase_histogram(3, 3, edges, tables)
    probability = Fraction(sum(c * c for c in hist.values()), 3**18)
    assert probability == Fraction(731, 2187)
    print("Four subdivided arms, ternary quadratic extremizer:", probability)


if __name__ == "__main__":
    main()
