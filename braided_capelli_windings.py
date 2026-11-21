"""Read a braided Capelli polynomial with a single species of winding probe.

Run OPENBLAS_NUM_THREADS=1 viz-python -B braided_capelli_windings.py.

Fix a simple target of SU(n)_k in the standard ribbon convention. Interfere
an unwound reference arm with an arm on which the *same* fundamental probe
winds m times before closure. The normalized topological fringe amplitude is
W_m = Tr_q(L^m)/(d_probe d_target), with W_0 = 1. The formula assumes the
categorical closure, coherent windings, and a calibrated complex fringe.

Write t = exp(2 pi i/(n+k)), M = sum(nu), and take row indices i = 0,...,n-1.
The physical roots are x_i = t^(nu_i-i-M/n), with fractional powers defined
by that exponential. The last term removes the U(1) phase of the demo's Hecke
loop, by subtracting M^2/n from the gl(n) quadratic Casimir. Thus det(x) is
t^(-n(n-1)/2), even if the size of the target's diagram is unknown.

Let P(z) = product_i(z-x_i) and D(s) = product_i(1-s x_i). A fundamental
fusion channel nu+e_i has normalized weight w_i = d_(nu+e_i)/(d_probe d_nu).
The q-Weyl dimension formula gives
    w_i = P(t x_i)/((t^n-1) x_i P'(x_i)).
A forbidden row or level-wall channel gives weight zero in the same formula.
The x_i are distinct because the descending shifted rows span less than n+k.
Comparing residues and values at zero gives
    P(t z)/P(z) = 1 + (t^n-1) sum_i w_i z/(z-x_i).
Expand at infinity with s=1/z. For d_j = [s^j]D(s) this gives
    (t^(n-j)-t^n) d_j = (t^n-1) sum_{m=1}^j W_m d_(j-m).
All denominators are nonzero for 1 <= j <= n. Unitarity gives
d_(n-j) = d_n conjugate(d_j), with d_n = (-1)^n det(x). Hence the first
floor(n/2) complex winding amplitudes recover every coefficient, including
roots absent from the physical loop spectrum. In Hecke framing, multiply the
physical roots by t^(M/n) to recover the original diagram's roots.

Uniqueness of the SU(n) charge follows by lifting the root angles in units
of 2 pi/(n+k). Their strictly decreasing lifts have span < n+k and fixed sum
-n(n-1)/2. Moving the cyclic cut by one increases the sum by n+k. A uniform
period shift increases it by n(n+k). Thus the fixed sum selects a unique
ordered lift, whose adjacent differences minus one are the Dynkin labels.
For literal Hecke partitions the shift nu -> nu + ell*(1,...,1) leaves the
root set and the size modulo n*ell unchanged. Fixing a representative matters.

For the SU(4)_4 demonstration the two opposite fringes can both occur among
eight fundamental anyons: the ordinary row diagrams are (3,3,1,1) and
(4,2,2,0). Removing one determinant column gives (2,2,0,0) for the former.
In a balanced interferometer p_bright = (1+Re(exp(i*delta) W_m))/2.
At delta=-pi/2 the two-winding bright-port probabilities are one and zero.

The initial winding cutoff is sharp as a bound uniform in the level. Write
r=floor(n/2), s=n-r and choose ell=4nrs, k=ell-n. Take a regular r-gon and
a regular s-gon rotated by t, both on the ell-th roots of unity. Their
polynomial (z^r-1)(z^s-t^s) has zero coefficients at indices 1,...,r-1 and
a nonzero coefficient at index r (also when r=s). Sorted integer exponents
give a valid partition: add i to exponent i and subtract the last row.
Physical normalization rotates the two polygons together. Now lift the
smallest exponent by ell and sort again. Physical normalization rotates all
roots by exp(-2 pi i/n). The two targets therefore have identical, zero first
r-1 fringes, and different nonzero r-th fringes by the recurrence. Even their
box counts agree modulo n since n divides ell. This proves sharpness for the
initial consecutive harmonics, without a claim about arbitrary probe choices.

The Newton identity is related to Gurevich, Pyatov and Saponov (0805.0177).
For the interferometric trace see Bonderson, Shtengel and Slingerland
(0707.4206). The multiple-winding protocol here specifies an ideal path
superposition, with fresh preparations for each winding number.
"""

from cmath import exp, pi
from itertools import combinations_with_replacement
from math import comb, prod, sin

import numpy as np
from sympy.polys.domains import QQ

from braided_capelli_anyon_demo import build_braid_and_antisymmetrizer, build_pure_braid_monodromy


def charges(n, k):
    for rows in combinations_with_replacement(range(k + 1), n - 1):
        yield rows[::-1] + (0,)


def dimension(rows, qints):
    return prod(qints[rows[i] - rows[j] + j - i] / qints[j - i]
                for j in range(len(rows)) for i in range(j))


def winding_data(rows, k, qints, phase, count):
    """Compute normalized traces from allowed fusion outputs and their dimensions."""
    n = len(rows)
    roots = [phase(n * (r - i) - sum(rows)) for i, r in enumerate(rows)]
    total_dimension = qints[n] * dimension(rows, qints)
    channels = []
    for i, x in enumerate(roots):
        child = list(rows)
        child[i] += 1
        if (i and child[i] > child[i - 1]) or child[0] - child[-1] > k:
            continue
        channels.append((x, dimension(child, qints) / total_dimension))
    return roots, [sum(w * x**m for x, w in channels) for m in range(count + 1)]


def reconstruct(n, k, moments):
    """Return D in ascending powers of s, using only W_1,...,W_floor(n/2)."""
    t = exp(2j * pi / (n + k))
    d = [0j] * (n + 1)
    d[0], d[n] = 1, (-1)**n * t**(-comb(n, 2))
    for j in range(1, n // 2 + 1):
        numerator = sum(moments[m-1] * d[j-m] for m in range(1, j+1))
        d[j] = (t**n - 1) * numerator / (t**(n-j) - t**n)
        if n-j != j:
            d[n-j] = d[n] * d[j].conjugate()
    return d


def floating_data(rows, k, count):
    n = len(rows)
    angle = pi / (n + k)
    qints = [sin(i * angle) / sin(angle) for i in range(n + k)]
    return winding_data(rows, k, qints, lambda a: exp(2j * angle * a / n), count)


def check_reconstruction():
    tested, largest_error = 0, 0.
    for n in range(2, 8):
        for k in range(1, 7):
            signatures = set()
            for rows in charges(n, k):
                roots, moments = floating_data(rows, k, n//2)
                recovered = reconstruct(n, k, moments[1:])
                # np.poly returns monic P in descending order, also D in ascending order.
                error = np.max(np.abs(np.poly(roots) - recovered))
                largest_error = max(largest_error, error)
                assert abs(moments[0] - 1) < 1e-12 and error < 1e-10
                key = tuple((round(w.real, 9), round(w.imag, 9)) for w in moments[1:])
                assert key not in signatures
                signatures.add(key)
                tested += 1
    return tested, largest_error


def check_su4_exact():
    """Exact, including the vanishing fringes, in Q(zeta_64) for SU(4)_4."""
    field = QQ.cyclotomic_field(64)
    g = field.unit
    powers = [field.one]
    for _ in range(63):
        powers.append(powers[-1] * g)
    q = powers[4]
    qints = [(q**i - q**(-i))/(q - q**-1) for i in range(8)]
    signatures = set()
    controls = {(2, 2, 0, 0): powers[16], (3, 2, 1, 0): field.zero,
                (4, 2, 2, 0): -powers[16]}
    for rows in charges(4, 4):
        _, (w0, w1, w2) = winding_data(rows, 4, qints, lambda a: powers[2*a % 64], 2)
        assert w0 == field.one
        if rows in controls:
            assert w1 == field.zero and w2 == controls[rows]
        signatures.add((w1, w2))
    assert len(signatures) == comb(7, 3)


def check_cutoff_examples():
    for n in range(2, 12):
        r, s = n // 2, n - n // 2
        ell = 4*n*r*s
        exponents = sorted([j * (ell//r) for j in range(r)]
                           + [1 + j * (ell//s) for j in range(s)], reverse=True)
        lifted = [exponents[-1] + ell] + exponents[:-1]
        signatures = []
        sectors = []
        for ordering in (exponents, lifted):
            last_row = ordering[-1] + n-1
            rows = tuple(a + i - last_row for i, a in enumerate(ordering))
            assert rows[0] <= ell-n and rows[-1] == 0
            sectors.append(rows)
            _, moments = floating_data(rows, ell-n, r)
            assert all(abs(w) < 1e-11 for w in moments[1:r])
            signatures.append(moments[r])
        assert (sum(sectors[0]) - sum(sectors[1])) % n == 0
        original, rotated = signatures
        assert abs(original - rotated) > 1e-6
        assert abs(rotated - exp(-2j*pi*r/n)*original) < 1e-10


def check_original_braids():
    """Direct pivot-weighted matrix trace of powers of the original demo's loop."""
    error = 0.
    for n, k in ((3, 3), (4, 4)):
        q = exp(1j * pi / (n+k))
        braid = build_braid_and_antisymmetrizer(n, q)[0]
        pivot = np.diag([q**(n-1-2*i) for i in range(n)])
        for bulk in (1, 2):
            rows = (1,) * bulk + (0,) * (n-bulk)
            target = np.eye(n) if bulk == 1 else (q * np.eye(n*n) - braid)/(q+q**-1)
            trace_weight = pivot
            for _ in range(bulk):
                trace_weight = np.kron(trace_weight, pivot)
            trace_weight = trace_weight @ np.kron(np.eye(n), target)
            loop = q**(-2*bulk/n) * build_pure_braid_monodromy(n, bulk, braid)
            _, moments = floating_data(rows, k, 4)
            for m, expected in enumerate(moments):
                signal = np.trace(trace_weight @ np.linalg.matrix_power(loop, m)) / np.trace(trace_weight)
                error = max(error, abs(signal - expected))
    assert error < 1e-12
    return error


if __name__ == "__main__":
    check_su4_exact()
    check_cutoff_examples()
    print("SU(4)_4: all 35 charges distinguished exactly by (W1,W2).")
    print("Dynkin (0,2,0): (0,+i); (1,1,1): (0,0); (2,0,2): (0,-i).")
    count, error = check_reconstruction()
    print(f"Reconstructed {count} sector polynomials; maximum coefficient error {error:.2e}.")
    print(f"Original Hecke matrix trace cross-check: maximum error {check_original_braids():.2e}.")
    for rows, label in (((1, 0, 0), "3"), ((1, 1, 0), "anti-3")):
        _, (_, w1, w2) = floating_data(rows, 3, 2)
        print(f"SU(3)_3 {label}: |W1|={abs(w1):.3f}, |W2|={abs(w2):.3f}.")
