"""Certify kernel signs for totally real S3 cubics by field discriminant.
Run: sage -python check_cubic_kernel_family.py [maximum discriminant]
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import isqrt

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
        _, nl, tl = sums(left)
        pr, _, _ = sums(right)
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


def check_field_list(fields, bound):
    """Independent covering search from the rank-two Hermite bound."""
    by_disc = defaultdict(list)
    for f in fields:
        disc = int(pari.nfdisc(f))
        if not (0 < disc <= bound and isqrt(disc)**2 != disc and f.polisirreducible()):
            raise ArithmeticError(f'Invalid cubic in list: {f}')
        if any(pari.nfisisom(f, g) for g in by_disc[disc]):
            raise ArithmeticError(f'Duplicate field: {f}')
        by_disc[disc].append(f)
    root = isqrt(bound) + 1
    # trace is 0 or 1, second coefficient >= -sqrt(bound)/3, and
    # norm^2 <= ((2*sqrt(bound)+1)/9)^3.
    max_norm = isqrt((2*root+1)**3 // 729) + 1
    for trace in (0, 1):
        for s in range(-(root//3+1), 1):
            for norm in range(-max_norm, max_norm+1):
                f = pari.Polrev([-norm, s, -trace, 1])
                disc = int(pari.poldisc(f))
                if disc <= 0 or isqrt(disc)**2 == disc or not f.polisirreducible():
                    continue
                d = int(pari.nfdisc(f))
                if d <= bound and not any(pari.nfisisom(f, g) for g in by_disc[d]):
                    raise ArithmeticError(f'Missing field at discriminant {d}: {f}')


def check_euler_coefficients(f, a):
    nf = pari.nfinit(f)
    combined = [0, 1] + [0]*(N-1)
    for p in range(2, N+1):
        if not pari.isprime(p):
            continue
        powers = [1]
        while p * powers[-1] <= N:
            powers.append(p*powers[-1])
        local = [1, -1] + [0]*(len(powers)-2)
        for prime_ideal in pari.idealprimedec(nf, p):
            degree = int(prime_ideal[3])
            for j in range(degree, len(local)):
                local[j] += local[j-degree]
        for j, pk in enumerate(powers[1:], start=1):
            for m in range(1, N//pk+1):
                if m % p != 0 and combined[m]:
                    combined[m*pk] = combined[m]*local[j]
    if a != combined[1:]:
        raise ArithmeticError(f'Local factor mismatch: {f}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bound', type=int, default=10000, nargs='?')
    bound = parser.parse_args().bound
    if bound < 1:
        parser.error('bound must be positive')
    check_splitting_pattern()
    fields = pari.nflist([3, 2], [1, bound], 0)
    check_field_list(fields, bound)
    zeta = pari.lfuncreate(1)
    counts = Counter()
    changes = []
    pattern_examples = []
    first = {}
    for f in sorted(fields, key=lambda f: int(pari.nfdisc(f))):
        d = int(pari.nfdisc(f))
        a = list(map(int, pari.lfunan(pari.lfundiv(pari.lfuncreate(f), zeta), N)))
        check_euler_coefficients(f, a)
        if a[0] != 1:
            raise ArithmeticError("Unexpected leading coefficient")
        c = 2*R.pi()/R(d).sqrt()
        r = (-c).exp()
        if (d <= 10000 and all(d % p for p in (2, 3, 5, 7, 11))
                and [a[p-1] for p in (2, 3, 5, 7, 11)] == [2, 0, -1, 0, 0]):
            pattern_examples.append(d)
        if d == 316:
            if not (r > R(7)/10 and sum(-v*Fraction(7,10)**j
                    for j,v in enumerate(a[:16]) if v < 0) > 1):
                raise ArithmeticError('Expected failure of first-term domination')
        if d == 2857:
            u = Fraction(5, 6)
            total = sum(v*u**j for j,v in enumerate(a))
            if not (as_ball(u) < r and total + geometric_tail(u) < -Fraction(1,5)):
                raise ArithmeticError('Expected negative exponential series')
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
    print('Five-prime pattern through 10000:', pattern_examples)
    for d, f, x, blocks in changes:
        print(f'Negative at x={x}: disc={d}, polynomial={f}, positive suffix masses on mesh 1/{blocks}')


if __name__ == '__main__':
    main()
