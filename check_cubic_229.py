"""Rigorous finite-height certificate for the conductor-229 Artin factor.

Run with sage -python check_cubic_229.py. The quadrature and truncation
bounds used here are proved in cubic_229.md. All transcendental operations
in the certificate use Arb real or complex balls through SageMath.
"""

from fractions import Fraction
from math import isqrt

from sage.all import ComplexBallField, RealBallField


R = RealBallField(512)
C = ComplexBallField(512)
H = R(1) / 20
J = 100
CUTOFF = 300
ERROR = R(1) / 10**15


def coefficients(limit):
    """Compute multiplicative coefficients from the local Artin polynomials."""
    smallest = list(range(limit + 1))
    for p in range(2, isqrt(limit) + 1):
        if smallest[p] == p:
            for n in range(p * p, limit + 1, p):
                if smallest[n] == n:
                    smallest[n] = p
    values = [0, 1] + [0] * (limit - 1)
    for n in range(2, limit + 1):
        p = smallest[n]
        if n == p:
            values[p] = (1 if p == 229 else
                         sum((j**3 - 4*j - 1) % p == 0 for j in range(p)) - 1)
            continue
        m = n
        while m % p == 0:
            m //= p
        if m > 1:
            values[n] = values[m] * values[n // m]
        else:
            # det(std) is the sign character, negative only for a transposition.
            det = 0 if p == 229 else (-1 if values[p] == 0 else 1)
            values[n] = values[p] * values[n // p] - det * values[n // (p*p)]
    return values


def quadrature_weights(values):
    scale = 2 * R.pi() / R(229).sqrt()
    weights = []
    for j in range(J + 1):
        u = j * H
        x = u.exp()
        total = R(0)
        for n in range(1, CUTOFF + 1):
            if n * x > CUTOFF:
                break
            if values[n]:
                total += values[n] * C(scale * n * x).bessel_K(0).real()
        weights.append(H * (u / 2).exp() * total)
    return weights


def certificate():
    height = R(10)
    end = J * H
    envelope = 576 * (height / 2).exp()
    grid_error = envelope / ((R.pi() / H).exp() - 1)
    mesh_tail = 288 * (-end.exp() / 3).exp()
    series_tail = (4 * H * (J + 1) * end.exp() * (-R(CUTOFF) / 5).exp()
                   / (1 - (-R(1) / 5).exp())**2)
    scale = 2 * R.pi() / R(229).sqrt()
    if not (scale > R(2)/5 and scale * (R(1)/2).cos() > R(1)/3
            and (-scale).exp() < R(2)/3 and (1 - (-R(1)/3).exp())**-2 < 16
            and end.exp() > 3 and grid_error + mesh_tail + series_tail < ERROR):
        raise ArithmeticError("The stated uniform quadrature bound failed")

    values = coefficients(CUTOFF)
    if values[1:17] != [1, 0, -1, 1, -1, 0, 0, 0, 0, 0, -1, -1, 0, 0, 1, 1]:
        raise ArithmeticError("Unexpected local coefficients")
    r = Fraction(2, 3)
    negative_mass = sum(max(-values[n], 0) * r**(n-1) for n in range(2, 17))
    negative_mass += r**16 * (17/(1-r) + r/(1-r)**2)
    if negative_mass >= Fraction(4, 5):
        raise ArithmeticError("Kernel positivity bound failed")
    print("Upper bound for the negative kernel mass:", negative_mass, flush=True)

    weights = quadrature_weights(values)
    derivatives = [[C(weights[j] * (j * H)**k) for j in range(1, J + 1)]
                   for k in range(4)]
    fourth_bound = 2 * sum(abs(weights[j]) * (j*H)**4 * (j*H).exp()
                           for j in range(1, J + 1))

    def jet(z, order):
        # Form powers before multiplying by uncertain Bessel coefficients.
        v = (H * z).exp()
        inverse = 1 / v
        result = [C(weights[0])] + [C(0) for _ in range(order)]
        pos = neg = C(1)
        for j in range(J):
            pos *= v
            neg *= inverse
            even = pos + neg
            odd = pos - neg
            for k in range(order + 1):
                result[k] += derivatives[k][j] * (odd if k % 2 else even)
        return result

    def segment(a, b, qa, qb, depth=0):
        mid = (a + b) / 2
        radius = abs(b - a) / 2
        qm, d1, d2, d3 = jet(mid, 3)
        variation = (abs(d1) * radius + abs(d2) * radius**2 / 2
                     + abs(d3) * radius**3 / 6 + fourth_bound * radius**4 / 24)
        if variation + ERROR < abs(qm) / 2:
            return (qb / qa).arg(), 1
        if depth >= 24:
            raise ArithmeticError("Unable to separate a boundary segment from zero")
        left, nl = segment(a, mid, qa, qm, depth + 1)
        right, nr = segment(mid, b, qm, qb, depth + 1)
        return left + right, nl + nr

    corners = [C(-1), C(1), C(1, 10), C(-1, 10), C(-1)]
    corner_values = [jet(z, 0)[0] for z in corners]
    angle = R(0)
    segments = 0
    for i in range(4):
        turn, count = segment(corners[i], corners[i+1], corner_values[i], corner_values[i+1])
        angle += turn
        segments += count
    winding = angle / (2 * R.pi())
    if not (winding > R(11)/2 and winding < R(13)/2):
        raise ArithmeticError(f"Unexpected winding enclosure {winding}")
    print(f"Boundary segments: {segments}. Winding enclosure: {winding}")

    # The endpoints are exact rationals. Every pair brackets a sign change.
    starts = [2614123, 4294614, 5628187, 6581842, 7581204, 8528305]
    for a in starts:
        ordinates = [R(a + i) / 10**6 for i in (0, 1)]
        left, right = (jet(C(0, t), 0)[0].real() for t in ordinates)
        if not ((left > ERROR and right < -ERROR) or (left < -ERROR and right > ERROR)):
            raise ArithmeticError(f"Sign change unresolved at {a}/10^6")
    for a in starts:
        print(f"Simple critical-line zero in ({a}/10^6, {a+1}/10^6)")


if __name__ == "__main__":
    certificate()
