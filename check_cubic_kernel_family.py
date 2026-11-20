"""Certify kernel signs for totally real S3 cubics by field discriminant.
Run: sage -python check_cubic_kernel_family.py [maximum discriminant]
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache

from sage.all import ComplexBallField, RealBallField, pari


R = RealBallField(256)
C = ComplexBallField(512)
N = 320


def as_ball(x):
    return R(x.numerator) / x.denominator


def geometric_tail(r):
    return r**N * ((N + 1) / (1 - r) + r / (1 - r)**2)


def polynomial_positive(a, r):
    """Horner enclosures including the full tail on each interval."""
    def check(left, right, depth):
        u = left.union(right)
        val = R(0)
        for coeff in reversed(a):
            val = u * val + coeff
        tail = geometric_tail(right)
        if val > tail:
            return True
        if val < -tail or depth == 20:
            return False
        mid = (right + left) / 2
        return check(left, mid, depth + 1) and check(mid, right, depth + 1)
    return check(R(0), r, 0)


def integrated_sign(a, c):
    """Bound the positive and negative Bessel sums separately at endpoints."""
    @lru_cache(maxsize=None)
    def sums(x):
        t = c * as_ball(x)
        pos = R(0)
        neg = R(0)
        # Tail bounds also cover any discarded terms beyond this adaptive cutoff.
        last = N
        for n, coeff in enumerate(a, start=1):
            if n*t > 35:
                last = n-1
                break
            if coeff:
                term = R(C(n*t).bessel_K(0).real())
                if coeff > 0:
                    pos += coeff * term
                else:
                    neg -= coeff * term
        r = (-t).exp()
        tail = (R(C(t).bessel_K(0).real()) * r**last *
                ((last + 1)/(1-r) + r/(1-r)**2))
        return pos, neg, tail

    def suffix_positive(upper):
        # Bound the mass of every suffix using dx/sqrt(x). The infinite
        # positive tail above upper can be discarded in the lower bound.
        for subdivision in (2, 4, 8, 16, 32, 64):
            mass = R(0)
            for j in reversed(range(subdivision, int(upper)*subdivision)):
                left, right = Fraction(j, subdivision), Fraction(j+1, subdivision)
                _, neg, tail = sums(left)
                pos, _, _ = sums(right)
                lower = pos - neg - tail
                cell = 2 * (as_ball(right).sqrt() - as_ball(left).sqrt())
                if not (lower > 0 or mass + lower*cell > 0):
                    break
                mass += lower*cell
            else:
                return subdivision
        raise ArithmeticError('Unresolved integrated tail mass')

    def point_negative(x):
        pos, neg, tail = sums(x)
        return pos - neg + tail < 0

    # Above this dyadic endpoint, sum n*r^(n-1) for n>=2 is below one.
    upper = Fraction(1)
    while not c * as_ball(upper) > R(3)/2:
        upper *= 2
    for x in (Fraction(1), Fraction(2)):
        if point_negative(x):
            return 'changes', (x, suffix_positive(upper))

    def check(left, right, depth):
        pl, nl, tl = sums(left)
        pr, nr, tr = sums(right)
        if pr - nl - tl > 0:
            return 'bessel', None
        mid = (left + right)/2
        if point_negative(mid):
            return 'changes', (mid, suffix_positive(upper))
        if depth == 24:
            raise ArithmeticError(f'Inconclusive interval: {left}, {right}')
        first = check(left, mid, depth+1)
        if first[0] == 'changes':
            return first
        return check(mid, right, depth+1)
    return check(Fraction(1), upper, 0)


def check_splitting_pattern():
    # Lower bound from small unramified Euler factors, with arbitrary local
    # behavior allowed at every other prime. The bound covers D <= 10000.
    traces = {2: 2, 3: 0, 5: -1, 7: 0, 11: 0}
    coeff = []
    for n in range(1, N+1):
        m, known = n, 1
        for p, trace in traces.items():
            previous, current = 0, 1
            determinant = -1 if trace == 0 else 1
            while m % p == 0:
                previous, current = current, trace*current - determinant*previous
                m //= p
            known *= current
        divisors = sum(m % j == 0 for j in range(1, m+1))
        coeff.append(known if m == 1 else -abs(known)*divisors)
    r = R(47)/50
    if not ((-2*R.pi()/100).exp() < r and polynomial_positive(coeff, r)):
        raise ArithmeticError('Local splitting criterion failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bound', type=int, default=10000, nargs='?')
    bound = parser.parse_args().bound
    if bound < 1:
        parser.error('bound must be positive')
    check_splitting_pattern()
    fields = pari.nflist([3, 2], [1, bound], 0)
    zeta = pari.lfuncreate(1)
    counts = Counter()
    changes = []
    first = {}
    for f in sorted(fields, key=lambda f: int(pari.nfdisc(f))):
        d = int(pari.nfdisc(f))
        a = list(map(int, pari.lfunan(pari.lfundiv(pari.lfuncreate(f), zeta), N)))
        if a[0] != 1:
            raise ArithmeticError("Unexpected leading coefficient")
        c = 2*R.pi()/R(d).sqrt()
        r = (-c).exp()
        negative = sum(-v*r**j for j,v in enumerate(a) if v < 0)
        if negative + geometric_tail(r) < 1:
            kind = 'leading'
        elif polynomial_positive(a, r):
            kind = 'polynomial'
        else:
            kind, witness = integrated_sign(a, c)
            if kind == 'changes':
                changes.append((d, str(f), *witness))
        first.setdefault(kind, (d, str(f)))
        counts[kind] += 1
    print('Field discriminant bound:', bound, ' Fields:', len(fields))
    for kind in ('leading', 'polynomial', 'bessel', 'changes'):
        print(kind, counts[kind], 'first', first.get(kind))
    for d, f, x, blocks in changes:
        print(f'Negative at x={x}: disc={d}, polynomial={f}, positive suffix masses on mesh 1/{blocks}')


if __name__ == '__main__':
    main()
