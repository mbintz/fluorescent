"""Exact two-probe Borromean interferometer in the Haagerup center.

    sage -python haagerup_borromean.py /tmp/haagerup-borromean-input --fetch

The first run needs curl and about 3 MiB of published CSV data. Subsequent
runs with the same directory work offline. The two targets are entries 3
and 4 of the algebraic archive. Entry 9 has twist exp(4 pi i / 13), called
mu_1 in haagerup_capelli_engine.md. Other archives can order simples differently.

For the ordered strands (a,a,x), use A = sigma_1^2, B = sigma_2^2 and close
A B A^-1 B^-1 with the categorical trace. Divide by d_a^2 d_x so the
unlink gives 1. The calculation uses exact field arithmetic throughout.
Only the display of the physical amplitudes and probabilities uses decimals.

Sources: Mäurer, Thiel and Vercleyen, arXiv:2601.20012, sections 3.1–3.3;
tensorcategories.github.io/TensorCategories.jl/stable/F-symbols/SkeletalFusion/
for the column-major packing of multiplicity indices.
"""

import argparse
import hashlib
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from sage.all import AA, QQ, QQbar, NumberField, PolynomialRing, diagonal_matrix, matrix


REVISION = "80dcdbed43194f3641099fdd6d732ee4b950cbba"
SOURCE = f"https://raw.githubusercontent.com/TensorCategories/F-Symbols-Double-Haagerup/{REVISION}/AlgebraicSymbols"
INPUT_DIGEST = "3fdfc17865ab838c37d88457784c5cb062c96174164a7a6b77d5661778512646"
PROBE = 9
TARGETS = {3: "pi_2", 4: "sigma_0"}
OUTPUTS = range(1, 13)
POLY = PolynomialRing(QQ, "t")([
    1, 1, 2, 2, 2, 1, -1, -4, -8, -12, -15, -15, -10, -51, -31, -57,
    -27, -2, 59, 141, 229, 313, 342, 285, 85, -285, 342, -313, 229,
    -141, 59, 2, -27, 57, -31, 51, -10, 15, -15, 12, -8, 4, -1, -1,
    2, -2, 2, -1, 1,
])
FIELD = NumberField(POLY, "t")


def verify_inputs(directory, fetch):
    sources = ["Double_Haagerup_R_symbols.csv", "S_matrix.csv"]
    sources.extend(f"Double_Haagerup_F_symbols/9_9_{x}_{d}.csv"
                   for x in TARGETS for d in OUTPUTS)
    digest = hashlib.sha256()
    for source in sorted(sources, key=lambda s: Path(s).name):
        path = directory / Path(source).name
        if fetch and not path.exists():
            directory.mkdir(parents=True, exist_ok=True)
            with TemporaryDirectory(dir=directory) as tmp:
                download = Path(tmp) / path.name
                subprocess.run(["curl", "-fsSL", "--retry", "2", "-o", str(download),
                                f"{SOURCE}/{source}"], check=True)
                download.replace(path)
        digest.update(path.name.encode() + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    if digest.hexdigest() != INPUT_DIGEST:
        raise ValueError(f"Input files differ from the pinned algebraic archive at {REVISION}")


def symbols(path, select):
    for line in path.read_text().splitlines():
        *indices, coefficients = line.split(";")
        indices = tuple(map(int, indices))
        if select(indices):
            terms = coefficients.strip()[1:-1].replace("//", "/").split(",")
            yield indices, FIELD([QQ(term.strip()) for term in terms])


def associator(path):
    entries = list(symbols(path, lambda key: True))
    # The CSV indices enumerate the entries of vec(F) in a nested loop.
    # They cannot be used as direct (row, column) pairs at multiplicity two.
    entries.sort(key=lambda row: tuple(row[0][i] for i in (7, 4, 9, 8, 6, 5)))
    left = sorted({key[7:] for key, _ in entries})
    right = sorted({key[4:7] for key, _ in entries})
    size = len(left)
    assert len(right) == size and len(entries) == size**2
    change = matrix(FIELD, size, size, [v for _, v in entries]).transpose()
    return change, left, right


def amplitudes(directory):
    dims = {j: v for (_, j), v in symbols(directory / "S_matrix.csv", lambda k: k[0] == 1)}
    pairs = {(PROBE, PROBE)} | {(i, j) for x in TARGETS for i, j in [(PROBE, x), (x, PROBE)]}
    r = {}
    for (i, j, c, u, v), value in symbols(directory / "Double_Haagerup_R_symbols.csv",
                                           lambda k: k[:2] in pairs):
        assert u == v == 1  # Every binary channel used for a full winding is simple.
        r[i, j, c] = value
    theta = 1 / r[PROBE, PROBE, PROBE]**2  # Ribbon balancing on the probe output.
    assert theta**13 == 1 and theta != 1
    normalized = {}
    for target in TARGETS:
        unlink = hopf_chain = commutator = FIELD.zero()
        for d in OUTPUTS:
            f, left, right = associator(directory / f"9_9_{target}_{d}.csv")
            a = diagonal_matrix(FIELD, [r[PROBE, PROBE, e]**2 for e, _, _ in left])
            phases = [r[PROBE, target, e] * r[target, PROBE, e] for e, _, _ in right]
            b = f * diagonal_matrix(FIELD, phases) * f.inverse()
            unlink += dims[d] * len(left)
            hopf_chain += dims[d] * (a * b).trace()
            commutator += dims[d] * (a * b * a.inverse() * b.inverse()).trace()
        assert unlink == dims[PROBE]**2 * dims[target]
        assert hopf_chain == 0  # The closure of A B is a chain of Hopf links.
        normalized[target] = commutator / unlink
    return theta, dims[PROBE], normalized


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="directory for the 26 source CSV files")
    parser.add_argument("--fetch", action="store_true", help="download missing source CSVs")
    args = parser.parse_args()
    verify_inputs(args.directory, args.fetch)
    theta, probe_dimension, values = amplitudes(args.directory)
    # Solve independently for the partial traces in the real cyclotomic basis.
    cosines = [theta**j + theta**(-j) for j in range(1, 7)]
    basis = matrix(QQ, [c.vector() for c in cosines]).transpose()
    assert basis.rank() == 6
    physical_theta = QQbar.zeta(13)**2
    physical_basis = [AA(physical_theta**j + physical_theta**(-j)) for j in range(1, 7)]
    physical_dimension = 3 * (3 + AA(13).sqrt()) / 2
    expected = {3: (-9, -15, -6, -12, -21, -12), 4: (3, 3, -6, 0, 3, -9)}
    for x, value in values.items():
        coefficients = basis.solve_right((probe_dimension**2 * value).vector())
        assert tuple(coefficients) == expected[x]
        w = sum(c * b for c, b in zip(coefficients, physical_basis)) / physical_dimension**2
        print(f"{TARGETS[x]:7}  coefficients = {tuple(coefficients)}")
        print(f"         W = {float(w):+.12f}  P_bright = {float((1+w)/2):.12f}")
    assert values[3] != values[4]


if __name__ == "__main__":
    main()
