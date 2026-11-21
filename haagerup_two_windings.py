"""Exact separation certificate for a double winding of pi_2 in Z(H_3).

Run with python3 haagerup_two_windings.py. The balanced detector phase is
+2*pi/39. The twelve numbers printed are residues of its probabilities in
the label order of haagerup_capelli_engine.md, not physical probabilities.

Write z = exp(2*pi*i/39). Reduction z -> 9 in F_157 is a homomorphism on
the cyclotomic integers and on fractions whose denominators remain nonzero.
Distinct reductions imply distinct complex values. Complex conjugation is
performed before reduction, by using z^(-1) and the negative winding.
Modular data follow Evans and Gannon (arXiv:1006.1326) in the note's gauge.
"""

P = 157
Z = 9


def divide(a, b):
    return a * pow(b, -1, P) % P


def root(exponent):
    return pow(Z, exponent % 39, P)


# The positive real Gauss sum in the physical embedding reduces to this root.
assert pow(Z, 39, P) == 1 and root(3) != 1 and root(13) != 1
residues = {j*j % 13 for j in range(1, 13)}
sqrt13 = sum((1 if j in residues else -1)*root(3*j) for j in range(1, 13)) % P
assert sqrt13**2 % P == 13
delta = divide(3 + sqrt13, 2)
dims = [1, 3*delta+1] + [3*delta+2]*4 + [3*delta]*6
total_dim = 9*delta + 6
spins = [0]*4 + [13, 26] + [6*r*r % 39 for r in range(1, 7)]
labels = ("1", "pi_1", "pi_2", "sigma_0", "sigma_1", "sigma_2",
          "mu_1", "mu_2", "mu_3", "mu_4", "mu_5", "mu_6")


def s_entry(i, j):
    i, j = sorted((i, j))
    if i == 0:
        return divide(dims[j], total_dim)
    if i == 1:
        if j == 1:
            return divide(1, total_dim)
        return divide(dims[j] if j < 6 else -dims[j], total_dim)
    if j < 6:
        return divide(2 if (i, j) in ((2, 2), (3, 3), (4, 5)) else -1, 3)
    if i < 6:
        return 0
    exponent = 12*(i-5)*(j-5)
    return divide(-root(exponent)-root(-exponent), sqrt13)


def double_winding_readout(target):
    probe = 2  # pi_2
    plus = minus = 0
    for c in range(12):
        multiplicity = sum(divide(s_entry(probe, l)*s_entry(target, l)*s_entry(c, l),
                                  s_entry(0, l)) for l in range(12)) % P
        weight = divide(multiplicity*dims[c], dims[probe]*dims[target])
        spin = 2*(spins[c] - spins[probe] - spins[target])
        plus += weight * root(spin)
        minus += weight * root(-spin)
    # p_bright = [2 + z W_2 + z^(-1) conjugate(W_2)]/4.
    return divide(2 + Z*plus + root(-1)*minus, 4)


if __name__ == "__main__":
    values = [double_winding_readout(i) for i in range(12)]
    assert len(set(values)) == 12
    print("Reductions mod 157 of twelve distinct bright-port probabilities:")
    for label, value in zip(labels, values):
        print(f"{label:>7}  {value}")
