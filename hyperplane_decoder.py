"""Statevector check of the optimal affine-hyperplane measurement over a prime field.

Run with OPENBLAS_NUM_THREADS=1 python3 hyperplane_decoder.py.
The simulator enumerates points. The circuit in the accompanying note uses
reversible field arithmetic and uniform-state preparation in their place.
"""

from itertools import product
from math import sqrt

import numpy as np


def optimal_success(q, dimension, copies, offsets):
    directions = (q**dimension - 1) // (q - 1)
    a = offsets / q**copies
    amplitude = (
        offsets - 1
        + (1 - 1 / directions) * sqrt(1 - a)
        + sqrt(1 + (directions - 1) * a) / directions
    ) / offsets
    return amplitude**2


class PlaneDecoder:
    """Coordinates for a full Fourier statevector and its promised subspace."""

    def __init__(self, q, dimension, copies):
        self.q = q
        self.dimension = dimension
        self.copies = copies
        self.points = np.array(list(product(range(q), repeat=dimension)))
        self.directions = np.array(
            [v for v in self.points if any(v) and v[np.flatnonzero(v)[0]] == 1]
        )
        n = len(self.points)
        m = len(self.directions)
        direction_of = np.full(n, -1, dtype=int)
        scalar_of = np.zeros(n, dtype=int)
        for i, d in enumerate(self.directions):
            for t in range(1, q):
                coords = tuple((t * d) % q)
                j = np.ravel_multi_index(coords, (q,) * dimension)
                direction_of[j] = i
                scalar_of[j] = t

        # A single nonzero frequency in the tuple fixes the common direction.
        # Group by that direction and the sum of all the scalar frequencies.
        buckets = [[] for _ in range(m * q)]
        for j, indices in enumerate(product(range(n), repeat=copies)):
            directions = {direction_of[i] for i in indices if i != 0}
            if len(directions) == 1:
                d = directions.pop()
                t = sum(scalar_of[i] for i in indices) % q
                buckets[q * d + t].append(j)
        self.buckets = [np.array(b, dtype=int) for b in buckets]

    def plane(self, direction, offset):
        one = (self.points @ self.directions[direction] % self.q == offset)
        one = one / np.linalg.norm(one)
        state = one
        for _ in range(1, self.copies):
            state = np.kron(state, one)
        return state

    def decode(self, state, nonzero_offsets):
        q, m = self.q, len(self.directions)
        shape = (q,) * (self.dimension * self.copies)
        freq = np.fft.ifftn(state.reshape(shape), norm="ortho").ravel()
        # Unprepare each uniform fiber, retaining its normalized coefficient.
        values = [freq[b].sum() / sqrt(len(b)) if len(b) else 0 for b in self.buckets]
        by_direction = np.array(values).reshape(m, q)
        theta = q ** (1 - self.copies)
        length = sqrt(1 + (m - 1) * theta)
        cos_angle = sqrt(1 - theta) / length
        sin_angle = sqrt(m * theta) / length
        common = by_direction[:, 0].sum() / sqrt(m)
        new_common = cos_angle * common + sin_angle * freq[0]
        by_direction[:, 0] += (new_common - common) / sqrt(m)
        decoded = np.fft.fft(by_direction, axis=1, norm="ortho")
        if nonzero_offsets:
            uniform_d = np.broadcast_to(decoded.mean(axis=0), decoded.shape)
            other_d = decoded - uniform_d
            allowed = np.r_[0, np.ones(q - 1)] / sqrt(q - 1)

            def rotate_offsets(rows, eigenvalue):
                # Rotate sqrt(G_full)|allowed> into the allowed mean.
                # Both vectors are real and constant on each of {0}, {1,...,q-1}.
                source = allowed + (sqrt(eigenvalue) - 1) * allowed.mean()
                diff = source / np.linalg.norm(source) - allowed
                norm = np.linalg.norm(diff)
                if norm < 1e-12:
                    return rows
                unit = diff / norm
                return rows - 2 * (rows @ unit)[:, None] * unit

            decoded = rotate_offsets(uniform_d, length**2) + rotate_offsets(other_d, 1 - theta)
            decoded = decoded[:, 1:]
        return decoded.ravel()


def check_geometry(q, r, k):
    decoder = PlaneDecoder(q, r, k)
    max_error = 0
    for nonzero in (False, True):
        labels = [(i, b) for i in range(len(decoder.directions)) for b in range(int(nonzero), q)]
        columns = np.column_stack([decoder.plane(i, b) for i, b in labels])
        measured = np.column_stack([decoder.decode(state, nonzero) for state in columns.T])
        gram = columns.T @ columns
        # Independent square root from the right singular vectors, including
        # the nullspace in the overcomplete one-copy, all-offset family.
        _, singular_values, right = np.linalg.svd(columns, full_matrices=False)
        expected = (right.T * singular_values) @ right
        successes = np.abs(measured.diagonal()) ** 2
        errors = (
            np.max(np.abs(measured - expected)),
            np.max(np.abs(measured.conj().T @ measured - gram)),
            np.max(np.abs(successes - optimal_success(q, r, k, q - int(nonzero)))),
        )
        max_error = max(max_error, *errors)
        if nonzero and q > 2 and k == 1:
            rng = np.random.default_rng(173)
            logical = rng.normal(size=(len(decoder.directions), q - 1))
            logical = logical + 1j * rng.normal(size=logical.shape)
            logical -= logical.mean(axis=1, keepdims=True)
            logical = logical.ravel() / np.linalg.norm(logical)
            recovered = decoder.decode(columns @ logical, True)
            max_error = max(max_error, np.max(np.abs(recovered - logical)))
    assert max_error < 1e-11, (q, r, k, max_error)
    return max_error


if __name__ == "__main__":
    for case in [(2, 3, 1), (2, 3, 2), (2, 2, 3), (3, 2, 1), (3, 2, 2),
                 (3, 2, 3), (3, 3, 1), (3, 3, 2), (5, 2, 1), (5, 2, 2),
                 (7, 2, 1)]:
        print(f"q={case[0]} r={case[1]} k={case[2]}   max error {check_geometry(*case):.2e}")
    for copies in (1, 2):
        print(f"q=17 r=64 k={copies}, nonzero offsets   "
              f"predicted success {optimal_success(17, 64, copies, 16):.9f}")
