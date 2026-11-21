"""Exact multichannel leakage certificates for braids of Fibonacci anyons.

Run 'viz-python -B fibonacci_braid_certificate.py' or use Python with SymPy.
A fusion path starts at the vacuum. Zero denotes vacuum and one denotes tau.
A signed letter i exchanges strands |i| and |i|+1. Words are chronological.

For an input span P and a detected span Q of left-associated fusion paths,
H = P U^{-1} Q U P gives the detection probability by its expectation.
Its least and greatest eigenvalues give the extremes over the input span.
Set D to the product of its nonzero eigenvalues, with empty product 1.
This code computes D and its norm as integers in the appropriate rings.

Proof of the certificate
------------------------
Write z = exp(i*pi/5), phi = z + z^{-1}, t = 1/phi, and u = sqrt(t).
In the orthonormal fusion basis the mixing block is F R F, with
F = [[t,u],[u,-t]] and R = diag(z^{-4},z^3). Other blocks are phases.
Rescaling each fusion vector by u to the power of its number of vacuum
labels removes the odd powers of u. Each nontrivial mixing step changes
one label, and all the rescaling factors are algebraic units. Thus U,
its inverse, and the two coordinate projectors are integral over Z in
the cyclotomic gauge. Similarity preserves the characteristic polynomial.
In the physical gauge H is Hermitian, 0 <= H <= 1. Its characteristic
coefficients therefore lie in Z[z] intersect R = Z[phi].

If H has rank r, D is its last nonzero signed characteristic coefficient.
Write D = a+b*phi. Its nonzero rational norm I = a*a+a*b-b*b is an
integer. Reduction at any prime ideal above a rational prime not dividing
I preserves rank: D stays nonzero, and the larger minors already vanish.

For a bound on physical probabilities, work in the original orthonormal
gauge. Extend the second real embedding by z -> z^3, u -> i*sqrt(phi).
Every conjugated exchange and inverse is block diagonal, up to permutation.
The mixing block has diagonal magnitude phi and off-diagonal magnitude
sqrt(phi), so its operator norm is at most C = phi+sqrt(phi). Scalar
blocks have modulus one. Consequently the conjugate of H, formed with
U^{-1} rather than conjugate transpose, has norm at most C^(2*L) for L
crossings. Its r nonzero eigenvalues multiply to the conjugate of D.
Equivalently, log(1/D) + log|I| <= 2*L*r*log(C). This gives
1 <= |I| <= D*C^(2*L*r). In particular the smallest positive
eigenvalue of H is at least D >= |I|*C^(-2*L*r). A state having a
component in the kernel can have a smaller expectation.

The norm argument is adapted from the repository's BuildingsResidueChars/
FrobeniusTraceNormNonzeroLogBound.lean. Related scalar leakage bounds
appear in arXiv:2610.37552, Lemma 3.2. The Fibonacci gate conventions are
also given in arXiv:1310.4150. The many-channel application here is a
mathematical derivation, not a Lean formalization or a hardware test.
"""

from sympy import N, sqrt
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


FIELD = QQ.cyclotomic_field(10)
Z = FIELD.unit
T = Z**2 - Z**3  # phi^{-1}


def fusion_paths(strands, total=0):
    """Return the left-associated paths of a specified total charge."""
    if strands < 1 or total not in (0, 1):
        raise ValueError("Use positive strand count and total charge zero or one.")
    paths = [(0,)]
    for _ in range(strands):
        paths = [path + (charge,) for path in paths
                 for charge in ((0, 1) if path[-1] else (1,))]
    return [path for path in paths if path[-1] == total]


def exchange(paths, position, direction):
    """Exchange adjacent strands in the integral cyclotomic gauge."""
    if not paths or not 1 <= position < len(paths[0]) - 1 or direction not in (-1, 1):
        raise ValueError("Invalid exchange or empty fusion space.")
    vacuum_phase = Z**(-4 * direction)
    tau_phase = Z**(3 * direction)
    phase_difference = vacuum_phase - tau_phase
    mixing = (
        (T**2 * vacuum_phase + T * tau_phase, T * phase_difference),
        (T**2 * phase_difference, T * vacuum_phase + T**2 * tau_phase),
    )
    index = {path: j for j, path in enumerate(paths)}
    rows = [[FIELD.zero for _ in paths] for _ in paths]
    for col, path in enumerate(paths):
        left, right = path[position - 1], path[position + 1]
        if left == right == 1:
            for charge in (0, 1):
                target = path[:position] + (charge,) + path[position + 1:]
                rows[index[target]][col] = mixing[charge][path[position]]
        else:
            rows[col][col] = vacuum_phase if left == right else tau_phase
    return DomainMatrix(rows, (len(paths), len(paths)), FIELD)


def detected_operator(paths, word, inputs, detected):
    """Compute U^{-1}[inputs,detected] U[detected,inputs] exactly."""
    if not paths or not inputs:
        raise ValueError("The fusion space and input space must have positive dimension.")
    for subset in (inputs, detected):
        if len(set(subset)) != len(subset) or any(i < 0 or i >= len(paths) for i in subset):
            raise ValueError("Projectors require distinct, valid fusion path indices.")
    identity = DomainMatrix.eye((len(paths), len(paths)), FIELD).to_dense()
    forward = backward = identity
    gates = {}
    for letter in word:
        for sign in (letter, -letter):
            if sign not in gates:
                gates[sign] = exchange(paths, abs(sign), 1 if sign > 0 else -1)
        forward = gates[letter] * forward
        backward = backward * gates[-letter]
    return backward.extract(inputs, detected) * forward.extract(detected, inputs)


def golden_integer(value):
    """Convert an integral real cyclotomic element to the pair (a,b) for a+b*phi."""
    coeffs = value.to_list()
    if any(c.denominator != 1 for c in coeffs):
        raise ArithmeticError("Expected an algebraic integer.")
    cubic, quadratic, linear, constant = [0] * (4 - len(coeffs)) + list(map(int, coeffs))
    # phi = 1 + z^2 - z^3.
    if linear or cubic != -quadratic:
        raise ArithmeticError("Expected a real element of Z[z].")
    return constant - quadratic, quadratic


def certificate(operator):
    """Compute rank, nonzero eigenvalue product in Z[phi], and its signed norm."""
    coefficients = operator.charpoly()
    rank = len(coefficients) - 1
    while coefficients[rank] == FIELD.zero:
        rank -= 1
    a, b = golden_integer((-1)**rank * coefficients[rank])
    return rank, (a, b), a*a + a*b - b*b


def reduce_at_root(value, prime, root):
    """Evaluate an integral cyclotomic element at a root of Phi_10 modulo prime."""
    if (root**4 - root**3 + root**2 - root + 1) % prime:
        raise ValueError("The supplied residue is not a root of Phi_10.")
    result = 0
    for c in value.to_list():
        if c.denominator != 1:
            raise ArithmeticError("Expected integral coefficients.")
        result = (result * root + int(c)) % prime
    return result


def main():
    paths = fusion_paths(6)
    inputs = [i for i, path in enumerate(paths) if path[2] == 0]
    leakage = [i for i, path in enumerate(paths) if path[2] == 1]
    word = [2, 3, -4, -4, 3, -4, 3, 2]
    H = detected_operator(paths, word, inputs, leakage)
    rank, (a, b), norm = certificate(H)
    trace_coeff = golden_integer(-H.charpoly()[1])
    assert (rank, a, b, norm) == (2, 5867, -3626, 71)
    assert trace_coeff == (-237, 147)

    phi = (1 + sqrt(5)) / 2
    trace = trace_coeff[0] + trace_coeff[1] * phi
    determinant = a + b * phi
    radius = sqrt(trace**2 - 4 * determinant) / 2
    low, high = trace / 2 - radius, trace / 2 + radius
    print(f"Chronological braid: {word}")
    print(f"Rank: {rank}; trace: {trace}; determinant: {a} + ({b}) phi; norm: {norm}")
    print(f"Leakage eigenvalues: {N(low, 14)}, {N(high, 14)}")

    # 14 and 17 represent the two different values of phi in F_71.
    for root, expected_rank in ((14, 1), (17, 2)):
        rows = [[reduce_at_root(x, 71, root) for x in row] for row in H.to_list()]
        det_mod = (rows[0][0]*rows[1][1] - rows[0][1]*rows[1][0]) % 71
        assert any(x for row in rows for x in row)
        assert (2 if det_mod else 1) == expected_rank
        print(f"Modulo 71 at z={root}: {rows}; rank {expected_rank}")


if __name__ == "__main__":
    main()
