"""Prime-side Weil positivity for the Artin factor of discriminant 229.

Run with sage -python check_cubic_haar.py. The note cubic-haar-transfer.tex
gives the archimedean tail bound, the continuous minimum test, and the Gram
matrix normalization. All sign decisions below use Arb enclosures.
"""

from argparse import ArgumentParser
from bisect import bisect_right
from math import isqrt
from pathlib import Path
import re

import numpy as np
from scipy.linalg import solve_triangular
from sage.all import RealBallField, ZZ, matrix, pari, prime_range


R = RealBallField(384)
LOG2 = R(2).log()
CUTOFF = 2**20
CELLS = 160
TICK = LOG2 / 8


def prime_data(cutoff):
    f = pari("x^3-4*x-1")
    terms = {}
    for prime in prime_range(cutoff + 1):
        p = int(prime)
        degrees = [] if p == 229 else [int(d) for d in f.factormod(p, 1)[0]]
        log_p = R(p).log()
        q, j = p, 1
        while q <= cutoff:
            trace = 1 if p == 229 else sum(d for d in degrees if j % d == 0) - 1
            terms[q] = (trace, trace * log_p / R(q).sqrt(), j * log_p)
            q *= p
            j += 1
    return terms


class Triangle:
    def __init__(self, terms):
        self.keys = sorted(terms)
        self.mass = [R(0)]
        self.moment = [R(0)]
        for q in self.keys:
            _, weight, log_q = terms[q]
            self.mass.append(self.mass[-1] + weight)
            self.moment.append(self.moment[-1] + weight * log_q)

        self.linear = (R(229).log() - 2 * R.pi().log() - 2 * R.euler_constant()
                       - R.pi() - 6 * LOG2)
        self.constant = R.pi()**2 + 8 * R.catalan_constant()
        self.coeffs = [4 / (2 * R(m) + R(1)/2)**2 for m in range(512)]

    def value(self, length, cutoff):
        """Here cutoff is the exact integer part of exp(length)."""
        if length.is_zero():
            return R(0)
        ratio = (-2 * length).exp()
        # The grid begins at log(2)/8; the continuous test begins at log(2)/2.
        count = 512 if length < LOG2 / 3 else 128
        tail = self.coeffs[count-1] * ratio**count / (1 - ratio)
        series = R(0)
        for m in reversed(range(count)):
            series = self.coeffs[m] + ratio * series
        arch = (self.linear * length + self.constant
                - (-length / 2).exp() * series.add_error(tail))
        i = bisect_right(self.keys, cutoff)
        return arch - 2 * (length * self.mass[i] - self.moment[i])


def upward_events(terms):
    for q, (trace, weight, _) in terms.items():
        root = isqrt(q)
        if root * root != q:
            if trace > 0:
                yield q
        else:
            # Combine the two prime-power contributions at the same length.
            jump = weight - 2 * terms[root][1]
            if not (jump > 0 or jump < 0):
                raise ArithmeticError(f"Unresolved jump at {q}")
            if jump > 0:
                yield q


def certify_continuum(triangle, terms):
    events = sorted({2, CUTOFF, *upward_events(terms)})
    lower = None
    upper = None
    best_q = None
    for q in events:
        length = R(q).log() / 2
        energy = 4 * triangle.value(length, isqrt(q)) - triangle.value(2 * length, q)
        if not energy > 0:
            raise ArithmeticError(f"Unresolved Haar sign at {q}: {energy}")
        lower = energy.lower() if lower is None else min(lower, energy.lower())
        if upper is None or energy.upper() < upper:
            upper, best_q = energy.upper(), q
    print(f"Continuous test: {len(events)} endpoints and upward jumps. "
          f"Minimum on [log(2)/2, log({CUTOFF})/2] in "
          f"[{R(lower).lower().str(digits=12)}, {R(upper).upper().str(digits=12)}]; "
          f"best evaluated endpoint q={best_q}.")
    assert R(lower) > R("2.4656305709") and R(upper) < R("2.4656305710")


def certify_gram(triangle):
    values = [R(0)]
    for j in range(1, CELLS + 1):
        floor_exp = ZZ(2**j).nth_root(8, truncate_mode=True)[0]
        values.append(triangle.value(j*TICK, int(floor_exp)))
    lags = [values[1]]
    for j in range(1, CELLS):
        lags.append((values[j+1] - 2*values[j] + values[j-1]) / 2)

    # Round once. Checking signs over the integers avoids interval inflation
    # in a long sequence of Schur complements.
    scale = 2**50
    eta = R(1) / 10**6
    shifted = [lags[0] - 2 * eta, *lags[1:]]
    integers = [ZZ((scale*x).mid().round()) for x in shifted]
    assert all(abs(scale*x - m) < 1 for x, m in zip(shifted, integers))
    assert CELLS < scale*eta
    rounded = matrix(ZZ, CELLS, CELLS, lambda i, j: integers[abs(i-j)])
    # A real symmetric matrix C is positive definite if det(tI+C)
    # has strictly positive coefficients, since it has only real roots.
    assert all(a > 0 for a in (-rounded).charpoly().list())
    print(f"{CELLS} by {CELLS} block Gram matrix exceeds 10^-6 I "
          f"(exact characteristic polynomial, {CELLS + 1} positive coefficients).")
    return lags, values


def make_clock(lags):
    """Real orthogonal shift with the negative reflection on its last dimension."""
    lags = np.array([float(x.mid()) for x in lags])
    indices = np.arange(len(lags))
    gram = lags[np.abs(indices[:, None] - indices)]
    vectors = np.linalg.cholesky(gram).T
    # Projection of the last vector onto the first N-1. Reversing the
    # coefficients gives the projection of the first onto the last N-1.
    projection = solve_triangular(vectors[:-1, :-1], vectors[:-1, -1])
    residual = vectors[:, 0] - vectors[:, 1:] @ projection[::-1]
    last_image = vectors[:, 1:] @ projection - residual
    images = np.column_stack((vectors[:, 1:], last_image))
    clock = solve_triangular(vectors.T, images.T, lower=True).T
    probe = np.linalg.solve(np.eye(len(lags)) - clock, vectors[:, 0])
    return clock, probe


def check_clock(lags, triangle_values):
    clock, probe = make_clock(lags)
    error = np.linalg.norm(clock.T @ clock - np.eye(CELLS), ord=np.inf)
    orbit = [probe]
    for _ in range(CELLS):
        orbit.append(clock @ orbit[-1])
    haar_error = 0.0
    for k in range(1, CELLS // 2 + 1):
        difference = probe - 2 * orbit[k] + orbit[2*k]
        target = float((4 * triangle_values[k] - triangle_values[2*k]).mid())
        haar_error = max(haar_error, abs(difference @ difference - target))
    assert error < 1e-8 and haar_error < 1e-8
    print(f"Numerical clock: orthogonality residual {error:.2e}; "
          f"maximum Haar error over 80 lengths {haar_error:.2e}.")
    eigenvalues, modes = np.linalg.eig(clock)
    frequencies = np.angle(eigenvalues) / float(TICK)
    masses = np.abs(modes.conj().T @ probe)**2
    positive = np.flatnonzero(frequencies > 0)
    strongest = positive[np.argmax(masses[positive])]
    print(f"Strongest positive-frequency line: {frequencies[strongest]:.8f}, "
          f"probe weight {masses[strongest]:.8f}.")
    return frequencies, masses


def plot_spectrum(frequencies, masses, output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Use the companion certificate only after computing the clock spectrum.
    note = Path(__file__).with_name("cubic_229.md").read_text()
    endpoints = re.findall(r"^\| (\d+\.\d{6}) \| (\d+\.\d{6}) \|$", note, re.M)
    zeros = np.array([(float(a) + float(b))/2 for a, b in endpoints])
    assert len(zeros) == 6
    select = (frequencies > 0) & (frequencies < 10)
    f, m = frequencies[select], masses[select]
    fig, axes = plt.subplots(1, 2, figsize=(8.1, 2.75), width_ratios=(3.2, 1.25))
    teal, rust = "#006f78", "#a84116"
    for ax in axes:
        ax.vlines(f, 0, m, colors=teal, linewidth=1.35)
        ax.scatter(f, m, s=15, color=teal, label="Clock line", zorder=3)
        ax.scatter(zeros, zeros**-2, marker="D", s=39, facecolors="none",
                   edgecolors=rust, linewidths=1.3, label="Certified zero, weight 1/γ²",
                   zorder=4)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e3e7e8", linewidth=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel("Frequency")
        ax.tick_params(labelsize=8)
    axes[0].set(xlim=(0, 10), ylim=(-0.002, 0.16), ylabel="Probe weight",
                xticks=range(0, 11, 2), yticks=(0, 0.05, 0.1, 0.15))
    axes[0].set_title("First six positive zeros", loc="left", fontsize=11)
    axes[0].legend(frameon=False, loc="upper right", fontsize=8)
    axes[1].set(xlim=(4.24, 4.35), ylim=(-0.001, 0.062),
                xticks=(4.25, 4.30, 4.35), yticks=(0, 0.02, 0.04, 0.06))
    axes[1].set_title("Near the second zero", loc="left", fontsize=11)
    fig.tight_layout(pad=0.7, w_pad=1.5)
    fig.savefig(output, dpi=240, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--figure", type=Path, help="save the clock spectrum and certified zeros")
    arguments = parser.parse_args()
    data = prime_data(CUTOFF)
    assert [data[q][0] for q in (2, 3, 4, 97, 193, 229)] == [0, -1, 2, -1, 2, 1]
    print(f"{len(data)} prime powers through {CUTOFF}.", flush=True)
    triangle = Triangle(data)
    certify_continuum(triangle, data)
    spectrum = check_clock(*certify_gram(triangle))
    if arguments.figure:
        plot_spectrum(*spectrum, arguments.figure)
