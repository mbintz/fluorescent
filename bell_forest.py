"""Recover a hidden forest from pairs of locally Z-rotated graph states.

Run python3 bell_forest.py for the statevector and reconstruction checks.
decode_forest takes only the Bell outcomes, the register size, and optionally
a bound on the mismatch probability between the two phase settings.
"""

from collections import deque
from itertools import combinations, product
from math import ceil, log

import numpy as np


def peel_graph(n, outcomes, drift_error=0.0):
    """Return fringe edges and the vertices of the 2-core from (s,t) Bell labels."""
    masks = [0] * n
    syndromes = [0] * n
    if not 0 <= drift_error < 0.5:
        raise ValueError("The per-site flip probability must be below one half")
    if not outcomes:
        raise ValueError("Supply Bell measurement outcomes")
    for j, (s, t) in enumerate(outcomes):
        if not (0 <= s < 1 << n and 0 <= t < 1 << n):
            raise ValueError("A Bell label does not fit the register")
        for v in range(n):
            if (s >> v) & 1:
                masks[v] |= 1 << j
                if (t >> v) & 1:
                    syndromes[v] |= 1 << j

    tolerance = 0 if drift_error == 0 else int((1 + 2 * drift_error) * len(outcomes) / 8)
    active = set(range(n))
    queue = deque(range(n))
    edges = set()
    while queue:
        v = queue.popleft()
        if v not in active:
            continue
        if syndromes[v].bit_count() <= tolerance:
            active.remove(v)
            continue
        for w in active:
            if w == v:
                continue
            predicted = masks[v] & masks[w]
            if (syndromes[v] ^ predicted).bit_count() <= tolerance:
                edges.add((min(v, w), max(v, w)))
                syndromes[w] ^= predicted
                queue.append(w)
                break
        else:
            continue  # Reconsider v if a neighboring leaf is removed.
        active.remove(v)
    return edges, active


def decode_forest(n, outcomes, drift_error=0.0):
    edges, core = peel_graph(n, outcomes, drift_error)
    if core:
        raise ValueError("The data did not peel to a forest")
    return edges


def graph_state(n, edges, angles):
    labels = np.arange(1 << n)
    bits = (labels[:, None] >> np.arange(n)) & 1
    signs = np.ones(len(labels))
    for u, v in edges:
        signs *= 1 - 2 * bits[:, u] * bits[:, v]
    return signs * np.exp(1j * (bits @ angles)) / np.sqrt(len(labels))


def bell_amplitudes(n, edges, first_angles, second_angles):
    """Full two-copy statevector simulation of CNOT, H, and readout."""
    first = graph_state(n, edges, first_angles)
    second = graph_state(n, edges, second_angles)
    labels = np.arange(1 << n)
    pair = np.outer(first, second)
    after_cnot = pair[labels[:, None], labels[:, None] ^ labels]
    walsh = np.array([[(-1)**((int(t) & int(x)).bit_count()) for x in labels]
                      for t in labels]) / np.sqrt(len(labels))
    # Rows of the result index the measured target s; columns index t.
    return (walsh @ after_cnot).T


def bell_distribution(n, edges, first_angles, second_angles):
    return np.abs(bell_amplitudes(n, edges, first_angles, second_angles))**2


def predicted_distribution(n, edges, a, b):
    result = np.zeros((1 << n, 1 << n))
    for s in range(1 << n):
        parity = np.zeros(n, dtype=int)
        for u, v in edges:
            parity[u] ^= (s >> v) & 1
            parity[v] ^= (s >> u) & 1
        bits = (s >> np.arange(n)) & 1
        flip = np.sin((a + (1 - 2 * bits)*b) / 2)**2
        for t in range(1 << n):
            mismatch = ((t >> np.arange(n)) & 1) ^ parity
            result[s, t] = np.prod(np.where(mismatch, flip, 1 - flip)) / (1 << n)
    return result


def parity_samples(n, edges, rounds, rng, error=0.0):
    """Sample the proven mask law; discarded coordinates are filled arbitrarily."""
    out = []
    for _ in range(rounds):
        s_bits = rng.integers(2, size=n, dtype=np.uint8)
        t_bits = rng.integers(2, size=n, dtype=np.uint8)
        t_bits[s_bits == 1] = 0
        for u, v in edges:
            if s_bits[u] and s_bits[v]:
                t_bits[u] ^= 1
                t_bits[v] ^= 1
        if error:
            t_bits ^= (rng.random(n) < error) & (s_bits == 1)
        out.append(tuple(int.from_bytes(np.packbits(bits, bitorder="little").tobytes(),
                                        "little") for bits in (s_bits, t_bits)))
    return out


def echo_degrees(n, edges, angles, vertices):
    """Simulate two forward phase calls on an active subset (small registers)."""
    size = 1 << n
    labels = np.arange(size)
    supported = (labels & ~vertices) == 0
    diagonal = graph_state(n, edges, angles) * np.sqrt(size)
    state = np.where(supported, diagonal * diagonal[labels ^ vertices], 0)
    state /= np.sqrt(supported.sum())
    outcomes = labels[supported]
    walsh = np.array([[(-1)**((int(t) & int(x)).bit_count()) for x in outcomes]
                      for t in outcomes]) / np.sqrt(len(outcomes))
    probabilities = abs(walsh @ state[supported])**2
    assert np.max(probabilities) > 1 - 1e-12
    return int(outcomes[np.argmax(probabilities)])


def peel_full_sketch(fingerprints, syndromes):
    """Fast decoder for the active-oracle variant, using r-bit word keys."""
    catalog = {c: v for v, c in enumerate(fingerprints)}
    if 0 in catalog or len(catalog) != len(fingerprints):
        raise ValueError("Fingerprint collision; sample new masks")
    queue = deque(range(len(fingerprints)))
    syndromes = list(syndromes)
    edges = set()
    while queue:
        v = queue.popleft()
        if fingerprints[v] not in catalog:
            continue
        if syndromes[v]:
            w = catalog.get(syndromes[v])
            if w is None or w == v:
                continue
            edges.add((min(v, w), max(v, w)))
            syndromes[w] ^= fingerprints[v]
            queue.append(w)
        del catalog[fingerprints[v]]
    return edges, set(catalog.values())


def check():
    rng = np.random.default_rng(75209)
    max_error = 0.0
    edge_pool = list(combinations(range(4), 2))
    for graph in range(1 << len(edge_pool)):
        edges = [e for j, e in enumerate(edge_pool) if graph >> j & 1]
        a, b = rng.uniform(-np.pi, np.pi, (2, 4))
        for angles in (a, b):
            circuit = bell_distribution(4, edges, a, angles)
            expected = predicted_distribution(4, edges, a, angles)
            max_error = max(max_error, float(np.max(np.abs(circuit - expected))))
    assert max_error < 1e-12
    print(f"64 four-vertex graphs, matched and drifted phases: max probability error {max_error:.2e}")

    # Three equally spaced angles exactly integrate the two-copy phase twirl.
    twirled = []
    for edges in ([], [(0, 1), (1, 2)]):
        rho = np.zeros((64, 64), complex)
        for phases in product(range(3), repeat=3):
            angles = (2 * np.pi / 3) * np.array(phases)
            a = bell_amplitudes(3, edges, angles, angles).ravel()
            rho += np.outer(a, a.conj()) / 27
        assert np.max(abs(rho - np.diag(np.diag(rho)))) < 1e-12
        twirled.append(rho)
    distance = sum(abs(np.linalg.eigvalsh(twirled[0] - twirled[1]))) / 2
    assert abs((1 - distance)/2 - 5/16) < 1e-12
    print("Exact three-point phase twirl: Bell-diagonal; empty versus three-site path error 5/16")

    # End to end: feed samples from the two-copy circuit to the decoder.
    edges = {(0, 3), (1, 3), (2, 4), (3, 4), (4, 5)}
    for _ in range(30):
        angles = rng.uniform(-np.pi, np.pi, 6)
        probs = bell_distribution(6, edges, angles, angles).ravel()
        draws = rng.choice(len(probs), size=40, p=probs / probs.sum())
        assert decode_forest(6, [divmod(int(k), 64) for k in draws]) == edges
    print("30/30 six-vertex reconstructions using actual statevector outcome probabilities")
    angles = rng.uniform(-np.pi, np.pi, 6)
    degree = echo_degrees(6, edges, angles, 63)
    columns, sketches = [0]*6, [0]*6
    for j in range(24):
        s = int(rng.integers(64))
        other = 63 ^ s
        measured = echo_degrees(6, edges, angles, s) | (
            (degree ^ echo_degrees(6, edges, angles, other)) & other)
        for v in range(6):
            columns[v] |= ((s >> v) & 1) << j
            sketches[v] |= ((measured >> v) & 1) << j
    assert peel_full_sketch(columns, sketches) == (edges, set())
    print("Forward-oracle echo and fingerprint decoder verified on the six-vertex tree")

    n, delta = 256, 0.01
    rounds = ceil(log(2*n*n/delta) / log(4/3))
    for j in range(40):
        if j % 4 == 0:
            edges = {(0, v) for v in range(1, n)}
        elif j % 4 == 1:
            edges = {(v-1, v) for v in range(1, n)}
        else:
            edges = {(int(rng.integers(v)), v) for v in range(1, n) if rng.random() > 0.08}
        perm = rng.permutation(n)
        edges = {tuple(sorted((int(perm[u]), int(perm[v])))) for u, v in edges}
        assert decode_forest(n, parity_samples(n, edges, rounds, rng)) == edges
    print(f"40/40 labeled stars, paths, and forests on {n} vertices, {rounds} pairs each (mask-law simulation)")
    for _ in range(20):
        perm = rng.permutation(n).tolist()
        core = set(perm[:9])
        core_edges = {tuple(sorted(e)) for e in combinations(core, 2)}
        fringe = {tuple(sorted((perm[v], perm[int(rng.integers(v))]))) for v in range(9, n)}
        samples = parity_samples(n, core_edges | fringe, rounds, rng)
        assert peel_graph(n, samples) == (fringe, core)
    print("20/20 exact 2-cores and attached fringe edges on 256 vertices")
    error = 0.08
    n = 64
    rounds = ceil(32 * log(2*n*n/delta) / (1 - 2*error)**2)
    for _ in range(8):
        edges = {(int(rng.integers(v)), v) for v in range(1, n)}
        assert decode_forest(n, parity_samples(n, edges, rounds, rng, error), error) == edges
    print(f"8/8 additional {n}-vertex noisy reconstructions at flip probability {error}, {rounds} pairs")


if __name__ == "__main__":
    check()
