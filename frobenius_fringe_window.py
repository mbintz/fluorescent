"""Exact Frobenius weights and a finite Landau-window check for x^3-x-1.

Run python3 frobenius_fringe_window.py. No external packages are required.
The default window [1024, 32768] has upper endpoint 1024^(3/2).
The accompanying note derives the all-scales criterion for the splitting field.
"""

from bisect import bisect_right
from functools import cache
from math import isqrt


def primes_through(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytes(1 + (limit - p*p)//p)
    return [p for p in range(2, limit + 1) if sieve[p]]


def multiply_mod_cubic(left, right, p):
    """In F_p[X]/(X^3-X-1), X^3=X+1 and X^4=X^2+X."""
    a, b, c = left
    d, e, f = right
    cubic, quartic = b*f + c*e, c*f
    return ((a*d + cubic) % p, (a*e + b*d + cubic + quartic) % p,
            (a*f + b*e + c*d + quartic) % p)


def frobenius_order(p):
    """At a good prime, use the sign and the complete-splitting test."""
    if p == 23:
        raise ValueError("23 is ramified")
    if pow(p, 11, 23) != 1:  # quadratic discriminant character (-23/p)
        return 2
    x = (0, 1, 0)
    accum, power, exponent = (1, 0, 0), x, p
    while exponent:
        if exponent & 1:
            accum = multiply_mod_cubic(accum, power, p)
        power = multiply_mod_cubic(power, power, p)
        exponent //= 2
    return 1 if accum == x else 3


def euler_terms(limit):
    """Nonzero terms in the pentagonal expansion of product (1-q^j)."""
    terms = [(0, 1)]
    k = 1
    while k*(3*k-1)//2 <= limit:
        for j in (k*(3*k-1)//2, k*(3*k+1)//2):
            if j <= limit:
                terms.append((j, (-1)**k))
        k += 1
    return terms


def eta_coefficients(limit):
    """Coefficients of eta(z)eta(23z), independently of polynomial splitting."""
    result = [0] * (limit + 1)
    terms = euler_terms(limit - 1)
    for j, v in euler_terms((limit - 1)//23):
        shift = 1 + 23*j
        for i, u in terms:
            if i + shift > limit:
                break
            result[i + shift] += u*v
    return result


def ideal_phase(p, root):
    """Class of (p,w-root), w^2-w+6=0. Fix the cubic character by the reduced form."""
    a, b = p, 1 - 2*root
    while True:
        b += 2*a*((a-b)//(2*a))
        c, remainder = divmod(b*b + 23, 4*a)
        assert remainder == 0
        if a <= c:
            # The three reduced classes of discriminant -23.
            return {(1, 1): 0, (2, 1): 1, (2, -1): -1}[a, b]
        a, b = c, -b


def check_magnetic_branch(primes):
    """On split primes, compare the two conjugate ideal phases to rational Frobenius."""
    count = 0
    for p in primes:
        if pow(p, 11, 23) != 1:
            continue
        phases = [ideal_phase(p, r) for r in range(p) if (r*r-r+6) % p == 0]
        assert len(phases) == 2 and sum(phases) == 0
        order = frobenius_order(p)
        for m in range(1, 7):
            conjugate_sum = 2 if m*phases[0] % 3 == 0 else -1
            assert conjugate_sum == (2 if m % order == 0 else -1)
        count += 1
    return count


def check_principal_form(terms, limit):
    """4*(a^2+a*b+6*b^2)=(2*a+b)^2+23*b^2; enumerate all represented norms."""
    represented = set()
    for b in range(isqrt(4*limit//23) + 1):
        for t in range(b % 2, isqrt(4*limit - 23*b*b) + 1, 2):
            represented.add((t*t + 23*b*b)//4)
    split = 0
    for n, p, weight in terms:
        if p == 23 or n != p:
            continue
        assert (weight == 4) == (p in represented)
        split += weight == 4
    return split


def checked_weights(limit):
    coeff = eta_coefficients(limit)
    terms = []
    for p in primes_through(limit):
        order = None if p == 23 else frobenius_order(p)
        sign = 0 if p == 23 else (1 if pow(p, 11, 23) == 1 else -1)
        n, m = p, 1
        while n <= limit:
            if order is None:
                weight = 2  # Frobenius on the two-dimensional inertia invariants
            else:
                trace = 2 if m % order == 0 else (0 if order == 2 else -1)
                weight = trace**2
            # Logarithmic derivative of zeta * L(sign) * L(eta-product).
            artin_trace = 2*coeff[n] - coeff[p]*coeff[n//p]
            assert weight == 1 + sign**m + artin_trace, (p, m)
            terms.append((n, p, weight))
            n *= p
            m += 1
    return sorted(terms)


SCALE = 10**16
SERIES_TERMS = 20


def log_ratio_bounds(a, b):
    """Outward integer bounds for SCALE*log((1+a/b)/(1-a/b)), 0<=a/b<=1/3."""
    assert 0 <= 3*a <= b
    if not a:
        return 0, 0
    # Atanh series tail <= 9 / (4*(2J+1)*3^(2J+1)) < 1/SCALE.
    jmax = SERIES_TERMS
    assert 9*SCALE < 4*(2*jmax+1)*3**(2*jmax+1)
    lo = 0
    num, den = a, b
    for j in range(jmax):
        lo += (2*SCALE*num)//((2*j+1)*den)
        num *= a*a
        den *= b*b
    return lo, lo + jmax + 1


@cache
def log_bounds(n):
    e = n.bit_length() - 1
    base = 2**e
    two_lo, two_hi = log_ratio_bounds(1, 3)
    lo, hi = log_ratio_bounds(n-base, n+base)
    return e*two_lo + lo, e*two_hi + hi


def certify_window(terms, lower, upper, density_denominator=1):
    """Bound the deficit from 2*x*log(2)/density_denominator on a whole interval."""
    norms = []
    # Prefix bounds for S(x) = sum b_n log p, T(x) = sum b_n log p / n.
    sums = [(0, 0, 0, 0)]
    for n, p, weight in terms:
        if not weight:
            continue
        lo, hi = (weight*v for v in log_bounds(p))
        sl, sh, tl, th = sums[-1]
        sums.append((sl + lo, sh + hi, tl + lo//n, th + (hi+n-1)//n))
        norms.append(n)

    # B is affine between knots x=n and x=n/2. Subtraction of c*sqrt(x)
    # is convex there for c>=0, so checking both endpoints proves the bound.
    knots = {2*lower, 2*upper}
    for n in norms:
        for t in (n, 2*n):
            if 2*lower < t < 2*upper:
                knots.add(t)
    best = 0
    log_two_hi = log_bounds(2)[1]
    for t in knots:  # t=2*x
        sl, _, _, th = sums[bisect_right(norms, t//2)]
        _, sh, tl, _ = sums[bisect_right(norms, t)]
        main_upper = (t*log_two_hi + density_denominator-1)//density_denominator
        upper_bound = max(0, main_upper + t*(th - tl) + sh - 2*sl)
        num, den = 20000*upper_bound**2, t*SCALE**2
        k = isqrt(num//den)
        best = max(best, k + (k*k*den < num))
    return best, len(knots)


if __name__ == "__main__":
    lower, upper = 1024, 32768
    terms = checked_weights(2*upper)
    print(f"Verified {len(terms)} prime powers through {2*upper} against the eta product.")
    print(f"Checked {check_principal_form(terms, 2*upper)} completely split primes via principal norms.")
    split_count = check_magnetic_branch(primes_through(1000))
    print(f"Checked both prime-ideal phases at {split_count} split primes through 1000.")
    for p in (2, 5, 23, 59):
        print(f"b({p}) = {next(b for n, _, b in terms if n == p)}")
    centi, count = certify_window(terms, lower, upper)
    print(f"Certified B(x) <= {centi}/100 * sqrt(x) on [{lower}, {upper}] using {count} exact knot bounds.")
    principal = [(p, p, 1) for n, p, b in terms if n == p and p != 23 and b == 4]
    centi, count = certify_window(principal, lower, upper, density_denominator=6)
    print(f"Certified x*log(2)/3 - S_0(x) <= {centi}/100 * sqrt(x) on the same window ({count} knots).")
