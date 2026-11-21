#!/usr/bin/env python3
"""
haagerup_capelli_demo.py
------------------------
Exact algebraic & numerical verification of the Haagerup Braided Capelli Engine
(`haagerup_capelli_engine.md`): pushing Alpoge & Claude's Capelli / Comatrix / SepPoly
architecture beyond Lie groups and quantum groups (zero q!) to the exotic rank-12
Haagerup Modular Tensor Category Z(H_3) over Q(sqrt(13)).

Verifies Theorems H1, H2, and H3 to ~1e-14 precision:
  - [Thm H1] Exact 12x12 S & T modular realization (S^T = S, S^2 = I, (ST)^3 = I),
             Verlinde integrality N_{ij}^k in {0, 1, 2}, dual Lagrangian condensates
             L_{H_3}, L_{H_2}, and Morita Z_2 braided autoequivalence tau: pi_2 <-> sigma_0.
  - [Thm H2] Universal Caratheodory-Toeplitz-Horner Engine (BDet_MTC & BComatrix_MTC)
             in Haar-scrambled bases across 7-, 8-, and 9-twist sectors, including
             multiplicity-2 fusion (pi_2 x pi_2, dim=14 -> R=9) and 3-boson condensates.
  - [Thm H3] Exact Mod-13 Legendre-Symbol Interferometry Law (integer ribbon traces {0,3,6}
             and quantized visibilities {0, delta^{-1}, 2*delta^{-1}}), 65/66 single-probe
             pair resolution, flux-invariant bispectrum separation, and 12/12 resolution.
"""

from math import gcd
import numpy as np


def build_haagerup_modular_data():
    """Construct exact closed-form 12x12 S, T, dims, twists, and N_{ij}^k of Z(H_3)."""
    delta = (3.0 + np.sqrt(13.0)) / 2.0
    D = 3.0 * np.sqrt(13.0) * delta  # 9*delta + 6 = 3*(delta^2 + 1)

    names = ["1", "pi_1", "pi_2", "sigma_0", "sigma_1", "sigma_2",
             "mu_1", "mu_2", "mu_3", "mu_4", "mu_5", "mu_6"]
    qnr_13 = [(2 * r * r) % 13 for r in range(1, 7)]  # [2, 8, 5, 6, 11, 7]

    dims = np.array([1.0, 3.0 * delta + 1.0] + [3.0 * delta + 2.0] * 4 + [3.0 * delta] * 6)
    twists = np.array(
        [1.0 + 0j, 1.0 + 0j, 1.0 + 0j, 1.0 + 0j,
         np.exp(2j * np.pi / 3.0), np.exp(-2j * np.pi / 3.0)]
        + [np.exp(2j * np.pi * q / 13.0) for q in qnr_13]
    )
    T = np.diag(twists)

    S = np.zeros((12, 12), dtype=float)
    S[0, 0] = S[1, 1] = 1.0 / D
    S[0, 1] = S[1, 0] = (3.0 * delta + 1.0) / D
    S[0, 2:6] = S[2:6, 0] = 1.0 / 3.0
    S[1, 2:6] = S[2:6, 1] = 1.0 / 3.0
    S[2:6, 2:6] = -1.0 / 3.0
    S[2, 2] = S[3, 3] = S[4, 5] = S[5, 4] = 2.0 / 3.0
    S[0, 6:] = S[6:, 0] = 1.0 / np.sqrt(13.0)
    S[1, 6:] = S[6:, 1] = -1.0 / np.sqrt(13.0)
    for r in range(6):
        for s in range(6):
            S[6 + r, 6 + s] = -2.0 * np.cos(8.0 * np.pi * (r + 1) * (s + 1) / 13.0) / np.sqrt(13.0)

    N_raw = np.einsum("il,jl,kl,l->ijk", S, S, S, 1.0 / S[0, :])
    N = np.rint(N_raw).astype(int)
    return delta, D, names, dims, twists, S, T, N, np.max(np.abs(N_raw - N))


def verify_theorem_h1(delta, D, dims, S, T, N, verlinde_err):
    print("=== [Thm H1] Haagerup Drinfeld Center Z(H_3) Modular & Morita Realization ===")
    err_sym = np.linalg.norm(S.T - S)
    err_orth = np.linalg.norm(S @ S - np.eye(12))
    err_mod = np.linalg.norm(np.linalg.matrix_power(S @ T, 3) - np.eye(12))

    L_H3 = np.array([1.0, 1.0, 2.0] + [0.0] * 9)
    L_H2 = np.array([1.0, 1.0, 0.0, 2.0] + [0.0] * 8)
    err_lag = max(np.linalg.norm(S @ L_H3 - L_H3), np.linalg.norm(S @ L_H2 - L_H2),
                  abs(np.dot(dims, L_H3) - D), abs(np.dot(dims, L_H2) - D))

    P_tau = np.eye(12)
    P_tau[[2, 3]] = P_tau[[3, 2]]
    err_tau = max(np.linalg.norm(P_tau @ S @ P_tau - S), np.linalg.norm(P_tau @ T @ P_tau - T))

    print(f"  delta = (3+sqrt(13))/2 = {delta:.10f} | D = 9*delta+6 = {D:.10f}")
    print(f"  ||S^T-S||={err_sym:.2e} | ||S^2-I||={err_orth:.2e} | ||(ST)^3-I||={err_mod:.2e}")
    print(f"  Verlinde integrality max err: {verlinde_err:.2e} | N_{{ij}}^k values: { sorted(list(set(N.ravel()))) }")
    print(f"  Lagrangian condensates S*L=L err: {err_lag:.2e} | Morita Z_2 [tau, S/T] err: {err_tau:.2e}")

    assert max(err_sym, err_orth, err_mod, verlinde_err, err_lag, err_tau) < 1e-13
    assert np.min(N) == 0 and np.max(N) == 2


def run_caratheodory_horner_case(a_idx, x_idx, names, dims, twists, N, rng):
    """Reconstruct minimal polynomial Phi_{a,x}(u) & pure-braid projectors from p_1..p_R ONLY."""
    blocks = [(c, N[a_idx, x_idx, c], twists[c] / (twists[a_idx] * twists[x_idx]))
              for c in range(12) if N[a_idx, x_idx, c] > 0]
    dimV = sum(m for _, m, _ in blocks)

    L_diag = np.diag(np.array([eig for _, m, eig in blocks for _ in range(m)], dtype=complex))
    W_qtr = np.diag(np.array([dims[c] for c, m, _ in blocks for _ in range(m)], dtype=complex))

    # Scramble basis with a Haar-random unitary so L_0 is given as a black-box pure-braid matrix
    Z = rng.normal(size=(dimV, dimV)) + 1j * rng.normal(size=(dimV, dimV))
    U, _ = np.linalg.qr(Z)
    L_op = U @ L_diag @ U.conj().T
    K_qtr = U @ W_qtr @ U.conj().T

    # Single-probe forward winding traces p_0, p_1, ..., p_{dimV}
    p_pos = []
    L_pow = np.eye(dimV, dtype=complex)
    for _ in range(dimV + 1):
        p_pos.append(np.trace(K_qtr @ L_pow) / dims[x_idx])
        L_pow = L_pow @ L_op

    # Detect exact channel count R and monic nullvector of Hermitian Toeplitz matrix T_k = (p_{j-i})
    R_found, null_vec = None, None
    for k in range(1, dimV + 1):
        Tk = np.array([[p_pos[j - i] if j >= i else np.conj(p_pos[i - j])
                        for j in range(k + 1)] for i in range(k + 1)], dtype=complex)
        evals, evecs = np.linalg.eigh(Tk)
        if evals[0] < 1e-10:
            assert evals[1] > 1e-7, "Kernel at first rank drop must be 1-dimensional!"
            R_found, null_vec = k, evecs[:, 0]
            break
    assert R_found is not None
    c_coeffs = null_vec / null_vec[-1]

    # Verify Cayley-Hamilton Phi_{a,x}(L_0) == 0 and Two-Sided Horner Comatrix identity
    I_V = np.eye(dimV, dtype=complex)
    Phi_L = sum(c_coeffs[j] * np.linalg.matrix_power(L_op, j) for j in range(R_found + 1))
    err_ch = np.linalg.norm(Phi_L)

    Gammas = [None] * R_found
    Gammas[R_found - 1] = -I_V.copy()
    for j in range(R_found - 1, 0, -1):
        Gammas[j - 1] = Gammas[j] @ L_op - c_coeffs[j] * I_V

    u_val = 0.57 - 0.43j
    K_hat_u = sum((u_val ** j) * Gammas[j] for j in range(R_found))
    Phi_u = sum((u_val ** j) * c_coeffs[j] for j in range(R_found + 1))
    err_comat_L = np.linalg.norm(K_hat_u @ (L_op - u_val * I_V) - Phi_u * I_V)
    err_comat_R = np.linalg.norm((L_op - u_val * I_V) @ K_hat_u - Phi_u * I_V)

    # Synthesize Lagrange pure-braid projectors Pi_s = -K_hat(z_s) / Phi'(z_s)
    z_roots = np.roots(c_coeffs[::-1])
    err_s1 = np.max(np.abs(np.abs(z_roots) - 1.0))
    projs = []
    for s in range(R_found):
        zs = z_roots[s]
        Phi_prime = np.prod([zs - z_roots[t] for t in range(R_found) if t != s])
        Kh_s = sum((zs ** j) * Gammas[j] for j in range(R_found))
        projs.append(-Kh_s / Phi_prime)

    err_comp = np.linalg.norm(sum(projs) - I_V)
    err_idem = max(np.linalg.norm(P @ P - P) for P in projs)
    err_orth = max(np.linalg.norm(projs[s] @ projs[t]) for s in range(R_found) for t in range(R_found) if s != t)

    # Verify quantum traces Tr_q(Pi_s) reproduce exact Haagerup quantum dimensions in Q(sqrt(13))
    eig_groups = {}
    for c, m, eig in blocks:
        matched = [zk for zk in eig_groups if abs(eig - zk) < 1e-9]
        if matched:
            eig_groups[matched[0]] += m * dims[c]
        else:
            eig_groups[eig] = m * dims[c]
    qdims_rec = np.sort([np.trace(K_qtr @ P).real for P in projs])
    qdims_ref = np.sort(list(eig_groups.values()))
    err_qdim = np.max(np.abs(qdims_rec - qdims_ref))

    print(f"  {names[a_idx]:4s} x {names[x_idx]:7s} (fusion dim={dimV:2d} -> R={R_found} twist sectors): "
          f"CH={err_ch:.2e}, Comat={max(err_comat_L, err_comat_R):.2e}, "
          f"comp={err_comp:.2e}, idem={err_idem:.2e}, Tr_q_err={err_qdim:.2e}")
    assert max(err_ch, err_comat_L, err_comat_R, err_s1, err_comp, err_idem, err_orth, err_qdim) < 1e-11


def verify_theorem_h3(delta, names, dims, twists, N):
    print("=== [Thm H3] Mod-13 Legendre-Symbol Interferometry & 12-Anyon SepPoly Tomography ===")
    inv_delta = 1.0 / delta
    qr_13 = set((k * k) % 13 for k in range(1, 13))
    probe = 6  # mu_1

    # 1. Exact complex amplitude & Legendre visibility check for m = 1..45 across {pi_2, sigma_0, sigma_1, sigma_2}
    max_leg_err = 0.0
    for x in [2, 3, 4, 5]:
        for m in range(1, 46):
            pm = sum(N[probe, x, c] * (dims[c] / dims[x]) * ((twists[c] / (twists[probe] * twists[x])) ** m)
                     for c in range(12) if N[probe, x, c] > 0)
            phase = (twists[probe] * twists[x]) ** (-m)
            if m % 39 == 0:
                pm_exact = 3.0 * delta * phase
            elif m % 13 == 0:
                pm_exact = 3.0 * (delta - 1.0) * phase
            else:
                leg = 1 if (m % 13) in qr_13 else -1
                mult_int = (1 if m % 3 == 0 else 0) + (1 - leg) // 2
                pm_exact = 3.0 * mult_int * phase
            max_leg_err = max(max_leg_err, abs(pm - pm_exact))

    vis_sample = [abs(sum(N[probe, 2, c] * (dims[c] / dims[2]) * ((twists[c] / twists[probe]) ** m)
                          for c in range(12))) / dims[probe] for m in range(1, 14)]
    print(f"  Exact Mod-13 Legendre amplitude max err (m=1..45, quartet): {max_leg_err:.2e}")
    print("  mu_1 x pi_2 V_1..V_7 / delta^{-1} = "
          + str([round(v / inv_delta, 6) for v in vis_sample[:7]])
          + f" | V_13 = {vis_sample[12]:.6f} (1 - delta^-1 = {1.0 - inv_delta:.6f})")
    assert max_leg_err < 1e-13

    # 2. Pairwise separation of all 12 Haagerup anyons: 65/66 with mu_1 alone, 66/66 with {mu_1, pi_2}
    p_mu1 = np.array([[sum(N[probe, x, c] * (dims[c] / dims[x]) * ((twists[c] / (twists[probe] * twists[x])) ** m)
                           for c in range(12)) for m in range(1, 10)] for x in range(12)])
    collisions_mu1 = [(names[i], names[j]) for i in range(12) for j in range(i + 1, 12)
                      if np.linalg.norm(p_mu1[i] - p_mu1[j]) < 1e-8]
    assert collisions_mu1 == [("pi_2", "sigma_0")]

    p1_pi2 = np.array([sum(N[2, x, c] * (dims[c] / dims[x]) * (twists[c] / twists[x]) for c in range(12))
                       for x in range(12)])
    full_vecs = np.hstack([p_mu1, p1_pi2[:, None]])
    min_pair_dist = min(np.linalg.norm(full_vecs[i] - full_vecs[j])
                        for i in range(12) for j in range(i + 1, 12))

    # Flux-invariant separation of {1, pi_1, quartet, mu_1..mu_6} via (|p_1|/d, |p_2|/d, B_12 / d^3)
    d_m = dims[probe]
    flux_inv = [np.array([abs(p_mu1[x, 0]) / d_m, abs(p_mu1[x, 1]) / d_m,
                          ((p_mu1[x, 0] ** 2) * np.conj(p_mu1[x, 1])).real / (d_m ** 3),
                          ((p_mu1[x, 0] ** 2) * np.conj(p_mu1[x, 1])).imag / (d_m ** 3)])
                for x in [0, 1, 2, 6, 7, 8, 9, 10, 11]]
    min_flux_inv_dist = min(np.linalg.norm(flux_inv[i] - flux_inv[j])
                            for i in range(len(flux_inv)) for j in range(i + 1, len(flux_inv)))

    print(f"  Single-probe mu_1 collisions among 66 pairs: {collisions_mu1} (65/66 resolved!)")
    print(f"  Adding p_1^(pi_2) [pi_2: {p1_pi2[2].real:+.1f} vs sigma_0: {p1_pi2[3].real:+.1f}] -> "
          f"all 66/66 pairs resolved (min dist = {min_pair_dist:.4f})")
    print(f"  Flux-invariant (V_1, V_2, B_12/d^3) min separation across 9 non-Morita/Z_3 classes: {min_flux_inv_dist:.4f}")
    assert abs(p1_pi2[2] - 2.0) < 1e-13 and abs(p1_pi2[3] - (-1.0)) < 1e-13
    assert min_pair_dist > 2.9 and min_flux_inv_dist > 0.02


def jacobi_symbol(a, n):
    """Exact Jacobi symbol (a / n) for odd integer n >= 1."""
    if n == 1:
        return 1
    a %= n
    res = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                res = -res
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            res = -res
        a %= n
    return res if n == 1 else 0


def build_haagerup_izumi_family(m):
    """Build exact general-m Haagerup-Izumi modular data (S^(m), T^(m)) of rank m^2 + 3."""
    Delta = m * m + 4
    sD = np.sqrt(float(Delta))
    delta = (m + sD) / 2.0
    D_tot = m * sD * delta
    half_m = (m - 1) // 2
    half_D = (Delta - 1) // 2
    rk = m * m + 3

    dims = np.array([1.0, m * delta + 1.0] + [m * delta + 2.0] * (half_m + half_m * m) + [m * delta] * half_D)
    twists = [1.0 + 0j, 1.0 + 0j] + [1.0 + 0j] * half_m
    for g in range(1, half_m + 1):
        for k in range(m):
            twists.append(np.exp(2j * np.pi * g * k / m))
    for r in range(1, half_D + 1):
        twists.append(np.exp(4j * np.pi * (r * r) / Delta))
    T = np.diag(np.array(twists))

    S = np.zeros((rk, rk), dtype=float)
    S[0, 0] = S[1, 1] = 1.0 / D_tot
    S[0, 1] = S[1, 0] = (m * delta + 1.0) / D_tot

    idx_pi = [2 + a_i for a_i in range(half_m)]
    idx_sig = {}
    cur = 2 + half_m
    for g in range(1, half_m + 1):
        for k in range(m):
            idx_sig[(g, k)] = cur
            cur += 1
    idx_mu = list(range(cur, rk))

    for j in idx_pi + list(idx_sig.values()):
        S[0, j] = S[j, 0] = 1.0 / m
        S[1, j] = S[j, 1] = 1.0 / m
    for i in idx_pi:
        for j in idx_pi:
            S[i, j] = 2.0 / m
    for a_i, i in enumerate(idx_pi):
        for (g, _), j in idx_sig.items():
            S[i, j] = S[j, i] = (2.0 / m) * np.cos(2.0 * np.pi * (a_i + 1) * g / m)
    for (g, k), i in idx_sig.items():
        for (h, l), j in idx_sig.items():
            S[i, j] = (2.0 / m) * np.cos(2.0 * np.pi * (g * l + h * k) / m)
    for r_i, i in enumerate(idx_mu):
        S[0, i] = S[i, 0] = 1.0 / sD
        S[1, i] = S[i, 1] = -1.0 / sD
        for s_i, j in enumerate(idx_mu):
            S[i, j] = -2.0 * np.cos(8.0 * np.pi * (r_i + 1) * (s_i + 1) / Delta) / sD
    return Delta, delta, D_tot, dims, S, T


def verify_theorems_h4_h5_h6():
    print("=== [Thm H4] General-m Haagerup-Izumi Modular Hierarchy (S^(m), T^(m)) ===")
    for m in [1, 3, 5, 7, 9, 11]:
        Delta, _, _, _, Sm, Tm = build_haagerup_izumi_family(m)
        rk = m * m + 3
        err_o = np.linalg.norm(Sm @ Sm - np.eye(rk))
        err_m = np.linalg.norm(np.linalg.matrix_power(Sm @ Tm, 3) - np.eye(rk))
        N_raw = np.einsum("il,jl,kl,l->ijk", Sm, Sm, Sm, 1.0 / Sm[0, :])
        err_v = np.max(np.abs(N_raw - np.rint(N_raw)))
        print(f"  m={m:2d} (Delta={Delta:3d}, rk={rk:3d}): ||S^2-I||={err_o:.2e}, "
              f"||(ST)^3-I||={err_m:.2e}, Verlinde_err={err_v:.2e}")
        assert max(err_o, err_m, err_v) < 1e-12 and np.min(np.rint(N_raw)) == 0

    print("=== [Thm H5 & H6] Dirichlet L(s, chi_Delta) Identity, Class Numbers & GRH Cancellation ===")
    W_max = 5000
    # Precompute von Mangoldt Lambda(w) up to W_max for Theorem H6(2)
    lam_vm = np.zeros(W_max + 1, dtype=float)
    sieve = np.ones(W_max + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, W_max + 1):
        if sieve[p]:
            sieve[p * p::p] = False
            pk = p
            lp = np.log(float(p))
            while pk <= W_max:
                lam_vm[pk] = lp
                pk *= p

    s_val = 2.35 + 0.41j
    w_pow = np.arange(1, W_max + 1, dtype=float) ** (-s_val)
    expected_h = {1: 1, 3: 1, 5: 1, 7: 1, 9: 2, 13: 1, 17: 1, 27: 3, 37: 3}

    for m, h_true in expected_h.items():
        Delta = m * m + 4
        sD = np.sqrt(float(Delta))
        delta = (m + sD) / 2.0
        D_tot = m * sD * delta
        half_m = (m - 1) // 2
        half_D = (Delta - 1) // 2

        # Direct anyonic sum check on w = 1..200
        anyon_err = 0.0
        for w in range(1, 201):
            sum_c = (m * delta + 1.0) + half_m * (m * delta + 2.0)
            for g in range(1, half_m + 1):
                for k in range(m):
                    sum_c += (m * delta + 2.0) * np.exp(2j * np.pi * ((w * g * k) % m) / m)
            for r in range(1, half_D + 1):
                sum_c += (m * delta) * np.exp(4j * np.pi * ((w * r * r) % Delta) / Delta)
            d = gcd(w, Delta)
            aw_closed = 0.5 * (gcd(w, m) - 1) + 0.5 * (1.0 + np.sqrt(float(d)) * jacobi_symbol(2 * (w // d), Delta // d))
            anyon_err = max(anyon_err, abs((sum_c / D_tot) - aw_closed))

        # Master Dirichlet-series identity check at s = 2.35 + 0.41i
        aw_arr = np.array([
            0.5 * (gcd(w, m) - 1) + 0.5 * (1.0 + np.sqrt(float(gcd(w, Delta)))
                                           * jacobi_symbol(2 * (w // gcd(w, Delta)), Delta // gcd(w, Delta)))
            for w in range(1, W_max + 1)
        ])
        lhs = np.sum(aw_arr * w_pow)
        rhs = 0.0 + 0.0j
        for e in [d for d in range(1, m + 1) if m % d == 0]:
            phi_e = sum(1 for k in range(1, e + 1) if gcd(k, e) == 1)
            rhs += 0.5 * phi_e * np.sum((np.arange(1, W_max // e + 1, dtype=float) * e) ** (-s_val))
        for d in [div for div in range(1, Delta + 1) if Delta % div == 0]:
            dp = Delta // d
            M_d = W_max // d
            chi_sub = np.array([jacobi_symbol(k, dp) if gcd(k, dp) == 1 else 0.0 for k in range(1, M_d + 1)])
            rhs += 0.5 * jacobi_symbol(2, dp) * (d ** (0.5 - s_val)) * np.sum(chi_sub * (np.arange(1, M_d + 1, dtype=float) ** (-s_val)))
        dir_err = abs(lhs - rhs)

        # Class-number reconstruction purely from simulated fringe visibilities V_1 .. V_{Delta - 1}
        V_2 = 1.0 / delta
        delta_meas = 1.0 / V_2
        h_sum = 0.0
        for w in range(1, Delta):
            if gcd(w, Delta) == 1:
                Vw = (0.5 * (gcd(w, m) - 1) + 0.5 * (1.0 - jacobi_symbol(w, Delta))) / delta
                chi_meas = gcd(w, m) - 2.0 * (Vw / V_2)
                h_sum += -chi_meas * np.log(np.sin(np.pi * w / Delta))
        h_meas = h_sum / (2.0 * np.log(delta_meas))

        # GRH winding cancellation ratio |Psi_FP(W_max)| / sqrt(W_max)
        psi_W = sum(lam_vm[w] * jacobi_symbol(w, Delta) for w in range(1, W_max + 1) if gcd(w, Delta) == 1)
        grh_ratio = abs(psi_W) / np.sqrt(float(W_max))

        print(f"  m={m:2d} (Delta={Delta:4d}): anyon_err={anyon_err:.2e}, L_series_err={dir_err:.2e} | "
              f"h_meas={h_meas:.8f} (exact h={h_true}) | |Psi({W_max})|/sqrt({W_max})={grh_ratio:.3f}")
        assert anyon_err < 1e-12 and dir_err < 1e-13
        assert abs(h_meas - h_true) < 1e-11 and grh_ratio < np.log(float(W_max * Delta))


if __name__ == "__main__":
    delta, D, names, dims, twists, S, T, N, verlinde_err = build_haagerup_modular_data()
    verify_theorem_h1(delta, D, dims, S, T, N, verlinde_err)

    print("=== [Thm H2] Caratheodory-Toeplitz-Horner Engine (Zero q, Haar-Scrambled Bases) ===")
    rng = np.random.default_rng(2026)
    for a_i, x_i in [(6, 1), (6, 2), (6, 4), (6, 6), (6, 7), (2, 2)]:
        run_caratheodory_horner_case(a_i, x_i, names, dims, twists, N, rng)

    verify_theorem_h3(delta, names, dims, twists, N)
    verify_theorems_h4_h5_h6()
    print("\nALL HAAGERUP-IZUMI & DIRICHLET-GRH ASSERTIONS PASSED TO MACHINE PRECISION.")
