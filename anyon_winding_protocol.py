"""Choose winding probes for a definite simple total charge.

Run: viz-python -B anyon_winding_protocol.py

A setting (p,m) uses one probe p coherently wound m times before categorical
closure. The reference arm is unwound. Balancing on p x a gives eigenvalue
theta_c/(theta_p theta_a) on each copy of c, and its normalized trace weight
is N_pa^c d_c/(d_p d_a). Collect equal phases. Two targets with the same
weighted phase distribution for p give identical results at every winding.
For spins of period L, Fourier inversion proves the converse. Positive and
negative winding amplitudes are conjugate, so m <= floor(L/2) suffices.

There is also a bound independent of L. If the union of the phase supports
for two candidate targets has K elements, equality of moments through
h=floor(K/2) gives equality at -h,...,h. Any K consecutive such equations
form an invertible Vandermonde matrix after multiplying its columns by
nonzero phases. Hence all weights on the union coincide.

For a modular theory one winding with all simple probe species gives the
invertible S matrix up to nonzero row and column scalings. A subset of rows
is sufficient for definite charges if its columns are pairwise distinct.
For distribution tomography on fresh, identically prepared targets, the
augmented real measurement matrix (normalization, real and imaginary parts)
must instead have full column rank. A peripheral loop acts as a scalar at
fixed target charge and cannot recover internal fusion-space coherences.

The search below measures cost in distinct (probe, winding) settings. Monte
Carlo shots are separate. A balanced port at phase delta has probability
(1 + Re(exp(i*delta)*W))/2. Complex responses upper-bound discrimination
at any fixed phase. The displayed adaptive example needs just one chosen
reference phase per node.

Sources: Bonderson, Shtengel & Slingerland, arXiv:0707.4206, Eq. (2.38).
Cui, Hong & Wang, arXiv:1401.7096, Sec. 2 and Tables 1-2 for D(S3).
"""

from fractions import Fraction
from functools import cache
from itertools import combinations

from sympy.polys.domains import QQ


def phase_weights(probe, target, fusion, dimensions, spins, period):
    """spins contain integer exponents; dimension scalars support exact division."""
    weights = {}
    for charge, multiplicity in fusion[probe, target].items():
        phase = (spins[charge] - spins[probe] - spins[target]) % period
        weight = multiplicity * dimensions[charge] / (dimensions[probe] * dimensions[target])
        weights[phase] = weights.get(phase, 0) + weight
    assert sum(weights.values()) == 1
    return weights


def responses(targets, probes, fusion, dimensions, spins, powers):
    """Supply a list of exact root powers compatible with the dimension field."""
    rows = {}
    period = len(powers)
    for probe in probes:
        weights = [phase_weights(probe, a, fusion, dimensions, spins, period) for a in targets]
        for m in range(1, period // 2 + 1):
            rows[probe, m] = tuple(sum(w * powers[m*j % period] for j, w in dist.items())
                                   for dist in weights)
    return rows


def shortest_fixed(rows, candidates):
    """Small-model exhaustive search. Each setting must resolve some target pair."""
    pairs = frozenset(combinations(candidates, 2))
    coverage = {key: {(i, j) for i, j in pairs if values[i] != values[j]}
                for key, values in rows.items()}
    useful = [key for key in rows if coverage[key]]
    if set().union(*(coverage[k] for k in useful)) != pairs:
        return None
    for count in range(len(useful) + 1):
        for settings in combinations(useful, count):
            if set().union(*(coverage[k] for k in settings)) == pairs:
                return settings


def minimum_adaptive_depth(rows, candidates):
    """Minimize the worst number of ideal settings along a decision-tree branch."""
    @cache
    def depth(group):
        if len(group) <= 1:
            return 0
        best = float("inf")
        for values in rows.values():
            branches = {}
            for i in group:
                branches.setdefault(values[i], []).append(i)
            if len(branches) > 1:
                best = min(best, 1 + max(depth(tuple(part)) for part in branches.values()))
        return best
    return depth(tuple(candidates))


def double_s3():
    labels = "ABCDEFGH"
    # Table 2 of Cui, Hong & Wang in alphabetic order. Each entry lists
    # simple outputs in a multiplicity-free product.
    upper_triangle = (
        "A B C D E F G H",
        "A C E D F G H",
        "ABC DE DE GH FH FG",
        "ACFGH BCFGH DE DE DE",
        "ACFGH DE DE DE",
        "ABF CH CG",
        "ABG CF",
        "ABH",
    )
    fusion = {}
    for i, row in enumerate(upper_triangle):
        for j, outputs in enumerate(row.split(), i):
            fusion[labels[i], labels[j]] = fusion[labels[j], labels[i]] = dict.fromkeys(outputs, 1)
    dims = dict(zip(labels, map(Fraction, (1, 1, 2, 3, 3, 2, 2, 2))))
    spins = dict(zip(labels, (0, 0, 0, 0, 3, 0, 2, 4)))
    field = QQ.cyclotomic_field(6)
    z = field.unit  # embedded as exp(+i*pi/3)
    powers = [z**j for j in range(6)]
    rows = responses(labels, labels, fusion, dims, spins, powers)
    one, zero, third = field.one, field.zero, field.convert(Fraction(1, 3))
    half = field.convert(Fraction(1, 2))
    assert rows["C", 1] == (one, one, one, zero, zero, -half, -half, -half)
    assert rows["D", 1] == (one, -one, zero, third, -third, zero, zero, zero)
    assert rows["D", 2][5:] == (one, z**2, z**4)
    for p in labels:
        # A single available species always has a pair invisible to all windings.
        a, b = ("C", "F") if p in "DE" else ("A", "B")
        assert phase_weights(p, a, fusion, dims, spins, 6) == phase_weights(p, b, fusion, dims, spins, 6)
    generated = {"A"}
    for _ in range(4):
        generated.update({c for a in generated for c in fusion["D", a]})
    assert generated == set(labels)
    assert phase_weights("D", "C", fusion, dims, spins, 6) == {0: Fraction(1, 2), 3: Fraction(1, 2)}

    targets = range(len(labels))
    fixed = shortest_fixed(rows, targets)
    adaptive = minimum_adaptive_depth(rows, targets)
    assert len(fixed) == 3 and adaptive == 2
    one_winding = {setting: values for setting, values in rows.items() if setting[1] == 1}
    assert len(shortest_fixed(one_winding, targets)) == 4
    assert minimum_adaptive_depth(one_winding, targets) == 3
    print("Minimum number of preselected settings:", len(fixed), fixed)
    print("Minimum worst-case adaptive depth:", adaptive)
    print("Restricted to one winding: 4 preselected settings or worst-case adaptive depth 3.")
    print("C once at phase 0: A,B,C -> 1; D,E -> 1/2; F,G,H -> 1/4 (port probabilities).")
    print("A,B,C: D once at phase 0 -> 1, 0, 1/2.")
    print("D,E:   D once at phase 0 -> 2/3, 1/3.")
    print("F,G,H: D twice at phase pi/2 -> 1/2, (2-sqrt(3))/4, (2+sqrt(3))/4.")


if __name__ == "__main__":
    double_s3()
