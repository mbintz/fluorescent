"""Check the cubic matrix product and its finite-field entanglement formula."""

from itertools import combinations, product
from math import factorial, gcd, isqrt


I = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
PAIRS = tuple(combinations(range(3), 2))


def multiply(a, b):
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in zip(*b))
                 for row in a)


def shift(a, k):
    return tuple(tuple(x + k * I[i][j] for j, x in enumerate(row))
                 for i, row in enumerate(a))


def quotient_invariants(a, q):
    """Invariant factors of the image of a modulo q, for nonsingular a."""
    first = gcd(*(x for row in a for x in row))
    second = gcd(*(a[i][k] * a[j][l] - a[i][l] * a[j][k]
                   for i, j in PAIRS for k, l in PAIRS))
    u, v, w = a
    det = abs(sum(u[i] * (v[(i + 1) % 3] * w[(i + 2) % 3]
                          - w[(i + 1) % 3] * v[(i + 2) % 3]) for i in range(3)))
    factors = (first, second // first, det // second)
    return tuple(q // gcd(q, t) for t in reversed(factors))


def good_part(n, discriminant):
    common = gcd(n, discriminant)
    while common > 1:
        n //= common
        common = gcd(n, discriminant)
    return n


def power_mod(a, exponent, p):
    result = I
    while exponent:
        if exponent % 2:
            result = tuple(tuple(x % p for x in row) for row in multiply(result, a))
        exponent //= 2
        a = tuple(tuple(x % p for x in row) for row in multiply(a, a))
    return result


def rank_mod(rows, p):
    rows = [list(row) for row in rows]
    rank = 0
    for col in range(3):
        pivot = next((i for i in range(rank, 3) if rows[i][col] % p), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][col] % p, -1, p)
        for i in range(rank + 1, 3):
            scale = rows[i][col] * inverse % p
            rows[i] = [(x - scale * y) % p for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def check(a, b, disc, limit=193):
    # Companion of x^3 + a*x + b, in the basis 1, x, x^2.
    m = ((0, 0, -b), (1, 0, -a), (0, 1, 0))
    primes = [p for p in range(2, limit + 1) if disc % p and
              all(p % d for d in range(2, isqrt(p) + 1))]
    degrees = {}
    for p in primes:
        roots = sum((x**3 + a*x + b) % p == 0 for x in range(p))
        degrees[p] = {0: (3,), 1: (1, 2), 3: (1, 1, 1)}[roots]

    for offset in (0, 5):
        numerator = I
        expected = [1, 1, 1]
        for n in range(1, limit + 1):
            numerator = multiply(numerator, shift(m, offset - (n - 1)))
            for p, cycle in degrees.items():
                power = 1
                while n % (power * p) == 0:
                    power *= p
                for i in range(cycle.count(1), 3):
                    expected[i] *= power
            actual = tuple(good_part(s, disc) for s in
                           quotient_invariants(numerator, factorial(n)))
            assert actual == tuple(expected), (disc, offset, n, actual, expected)

    for p, cycle in degrees.items():
        for j in range(1, 7):
            mp = power_mod(m, p**j, p)
            diff = tuple(tuple((x - y) % p for x, y in zip(row, base))
                         for row, base in zip(mp, m))
            rank = rank_mod(diff, p)
            assert rank == 3 - sum(d for d in cycle if j % d == 0), (disc, p, j)
            if p <= 7:
                # The reduced density matrix has one equal weight per image point.
                counts = {}
                for v in product(range(p), repeat=3):
                    image = tuple(sum(x * y for x, y in zip(row, v)) % p for row in diff)
                    counts[image] = counts.get(image, 0) + 1
                assert len(counts) == p**rank and set(counts.values()) == {p**(3 - rank)}
    print(f"disc {disc:+}: Smith factors for N=1..{limit}, shifts 0 and 5; "
          f"entropy ranks for {len(primes)} good primes, powers 1..6")


if __name__ == "__main__":
    check(0, -2, -108)
    check(-4, -1, 229)
