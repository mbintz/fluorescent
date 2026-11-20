"""Certify zeros on the Fricke-symmetric geodesic for the six signed cubic traces.

Run with sage -python check_cubic_geodesic_nodes.py. Coordinates printed are
x = sqrt(D) * Im(z). Reflection supplies the reciprocal root for each field.
"""
from fractions import Fraction
from functools import lru_cache

from check_cubic_kernel_family import C, N, R, as_ball, check_euler_coefficients, pari


SIGNED_DISCRIMINANTS = (1489, 4729, 5521, 7249, 8884, 9364)


def certify_nodes(coefficients, c):
    """Cover x >= 1 by strict sign or strict monotonicity certificates."""
    @lru_cache(maxsize=None)
    def parts(x, order):
        # Order 0 encloses B, and order 1 encloses -B'/c using K0' = -K1.
        t = c * as_ball(x)
        pos, neg = R(0), R(0)
        for n, coefficient in enumerate(coefficients, 1):
            if n*t > 42:
                break
            if coefficient:
                term = abs(coefficient) * n**order * C(n*t).bessel_K(order).real()
                if coefficient > 0:
                    pos += R(term)
                else:
                    neg += R(term)
        else:
            n = len(coefficients) + 1
        # First omitted index n. For nu=0,1 the integral representation gives
        # K_nu(k*t) <= K_nu(t) exp(-(k-1)*t). Also |a_k| <= k and
        # (n+j)^(1+order) <= n^(1+order) * (1+j)^2.
        r = (-t).exp()
        tail = R(C(t).bessel_K(order).real()) * r**(n-1) * n**(1+order) * (1+r)/(1-r)**3
        return pos, neg, tail

    def sign(left, right, order=0):
        pos_l, neg_l, tail_l = parts(left, order)
        pos_r, neg_r, _ = parts(right, order)
        if pos_r - neg_l - tail_l > 0:
            return 1
        if pos_l - neg_r + tail_l < 0:
            return -1
        return 0

    def point_sign(x):
        value = sign(x, x)
        if not value:
            raise ArithmeticError(f'Point sign unresolved at {x}')
        return value

    def roots(left, right, depth=0):
        if sign(left, right):
            return []
        if sign(left, right, order=1):
            initial = point_sign(left)
            if initial == point_sign(right):
                return []
            while right - left > Fraction(1, 2**16):
                mid = (left + right) / 2
                if point_sign(mid) == initial:
                    left = mid
                else:
                    right = mid
            return [(left, right)]
        if depth == 32:
            raise ArithmeticError(f'Unresolved interval {left}, {right}')
        mid = (left + right) / 2
        return roots(left, mid, depth+1) + roots(mid, right, depth+1)

    # For t >= 3/2, the leading K0(t) dominates all higher terms since
    # sum_{n>=2} n exp(-(n-1)t) <= (1-exp(-3/2))^(-2) - 1 < 1.
    bound = Fraction(1)
    while not c * as_ball(bound) > R(3)/2:
        bound *= 2
    if not ((1 - (-R(3)/2).exp())**(-2) < 2):
        raise ArithmeticError('Large-x inequality failed')
    if point_sign(Fraction(1)) != -1 or point_sign(bound) != 1:
        raise ArithmeticError('Unexpected endpoint signs')
    return roots(Fraction(1), bound)


def main():
    zeta = pari.lfuncreate(1)
    for disc in SIGNED_DISCRIMINANTS:
        fields = pari.nflist([3, 2], [disc, disc], 0)
        if len(fields) != 1:
            raise ArithmeticError(f'Expected one field at D={disc}')
        f = fields[0]
        coefficients = list(map(int, pari.lfunan(pari.lfundiv(pari.lfuncreate(f), zeta), N)))
        check_euler_coefficients(f, coefficients)
        intervals = certify_nodes(coefficients, 2*R.pi()/R(disc).sqrt())
        if len(intervals) != 1:
            raise ArithmeticError(f'D={disc}: found {len(intervals)} roots on x >= 1')
        left, right = intervals[0]
        print(f'D={disc}: one simple root on x >= 1, in ({left}, {right})', flush=True)


if __name__ == '__main__':
    main()
