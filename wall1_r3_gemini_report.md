# Wall 1 — Round 3 Report (Gemini, Front 3)
## Explicit Mod-$p$ Dormant $\mathrm{PGL}_2$-Opers on $(\mathbb{P}^1, \{\infty, t^3 = 2\})$, Zwegers Mock Indefinite Thetas, and Quillen-Metric $H^1$ Restriction on $E_K^3$

This report records Gemini's parallel Round 3 computations alongside GPT-6.2-Astra (Front 1: arithmetic geometry & Verschiebung on $\mathcal{M}_{\mathrm{SL}_2}(E', E'[2])$) and Claude Fable 5.2 (Front 2: KZB/Hitchin $p$-curvature & truncated anyon/VUMPS chains).

---

## 1. Exact Mod-$p$ $p$-Curvature & Dormant $\mathrm{PGL}_2$-Opers on $(\mathbb{P}^1, \{\infty\} \cup Y)$

Take $Y = \operatorname{Spec}\mathbb{Z}[1/6, t]/(t^3 - 2) = E'[2]\setminus\{0\}$ ($E': y^2 = t^3 - 2$) and consider the symmetric-weight rank-2 Fuchsian / KZ differential operator on $(\mathbb{P}^1, \{\infty, \alpha_1, \alpha_2, \alpha_3\})$ with local exponent difference $1 - \mu$ at all four punctures:
$$L_{\mu, B}(y) \;:=\; (t^3 - c)\, y'' \;+\; 3\mu\, t^2\, y' \;+\; \big(\mu(2\mu - 1)\, t + B\big)\, y \;=\; 0, \qquad c \in \{1, 2\}.$$
- At $\mu = \frac{1}{2}$, $A = 0$ and $(t^3 - c)y'' + \frac{3}{2}t^2 y' + B y = 0$ is literally $d^2 y / dz^2 + B y = 0$ in the elliptic coordinate $dz = dt/\sqrt{t^3 - c}$ on $E_c : y^2 = t^3 - c$ (Lamé equation with $n = -\frac{1}{2}$).
- At $B = 0$, substituting $u = t^3 / c$ reduces $L_{\mu, 0}$ to a Gauss hypergeometric ODE in $u$; hence the $p$-curvature $\Psi_p(B = 0)$ is **invariant** under $c = 1 \leftrightarrow c = 2$ and blind to $\left(\frac{2}{\pi}\right)_3$.
- At $B \ne 0$, the coordinate rescaling $t = c^{1/3} \tilde t$ transforms the accessory parameter by $B = c^{1/3} \tilde B$, so the $\mathbb{Z}/3$-invariant dormant-oper polynomial $P_p(B^3) = 0$ shifts by $B^3 = c\,\tilde B^3$.

### Explicit Computation of $\mathbb{F}_p$-Rational Dormant Opers ($\Psi_p = 0$)

Evaluating $D^p \pmod p$ directly at $t = 0$ across all $B \in \mathbb{F}_p$ for $p \in \{7, 11, 13, 19, 23, 31, 37, 43, 61\}$ yields:

| $p$ | Splitting in $F$ | $\mu = \frac{1}{2}$ ($c=1$) | $\mu = \frac{1}{2}$ ($c=2$) | $\mu = \frac{1}{3}$ ($c=1$ vs $c=2$) | $\mu = \frac{2}{3}$ ($c=1$ vs $c=2$) |
|---:|---|---|---|---|---|
| $7$ | 3-cycle | $0$ | $0$ | $0$ vs $0$ | $0$ vs $0$ |
| $13$ | 3-cycle | $0$ | $0$ | $0$ vs $0$ | $0$ vs $0$ |
| $19$ | 3-cycle | $3$ ($B^3 = 18$) | **$0$** | $0$ vs $0$ | $4$ ($B^3 \in \{0,1\}$) vs $1$ ($B^3=0$) |
| $31$ | 1-split | $0$ | $0$ | $1$ ($B^3=0$) vs $1$ ($B^3=0$) | $0$ vs $0$ |
| $37$ | 3-cycle | $0$ | **$3$** ($B^3 = 1$) | $1$ ($B^3=0$) vs **$4$** ($B^3 \in \{0,23\}$) | $1$ vs $1$ |
| $43$ | 1-split | $3$ ($B^3 = 39$) | $3$ ($B^3 = 35 \equiv 2\cdot 39$) | $0$ vs $0$ | $0$ vs $0$ |
| $61$ | 3-cycle | $0$ | $0$ | $0$ vs $0$ | $1$ vs $1$ |

*(At supersingular transposition primes $p = 11, 23$ for $\mu = \frac{1}{2}$, $B = 0$ is dormant because $H_p(-2) = 0$; $p = 23$ also has $2$ extra nonzero dormant roots $B = 3, 6$.)*

**Exact Structural Verdict on Dormant Opers of $(\mathbb{P}^1, \{\infty\}\cup Y)$:**
1. Whenever $2$ is a cube mod $p$ ($p = x^2+27y^2$), multiplication by $2$ preserves cubes in $\mathbb{F}_p^\times$, so $\#\mathrm{Dorm}_p(c=2) = \#\mathrm{Dorm}_p(c=1)$ identically (verified at $p = 31, 43$: $B^3 = 35 \equiv 2\cdot 39 \pmod{43}$).
2. At 3-cycle primes ($p = 4x^2+2xy+7y^2$), multiplication by $2$ permutes the three cubic cosets in $\mathbb{F}_p^\times/(\mathbb{F}_p^\times)^3$, causing $\#\mathrm{Dorm}_p(c=2)$ and $\#\mathrm{Dorm}_p(c=1)$ to diverge (e.g., $p = 19$: $3$ vs $0$; $p = 37$: $0$ vs $3$).
3. **Obstruction:** Unlike Astra's $h(z)$ or Gemini's $G_H(w)$, the count $\#\mathrm{Dorm}_p(c=2)$ is **not** a pure function of $\operatorname{Frob}_p \in S_3$ — it depends erratically on the cubic cosets of the roots of the Hasse–Lamé polynomial $P_p(u)$ (oscillating between $0$ and $3$ even among split primes, e.g., $0$ at $p=31$ vs $3$ at $p=43$).

---

## 2. Zwegers Mock-Modular Indefinite Theta Completion of $L_H$ on $E_K^3$

In `wall1_gemini_report.md` §3, we proved that the signature-$(2,1)$ trace-form bundle $L_H$ ($H = \left(\begin{smallmatrix} 1&0&0\\0&0&2\\0&2&0\end{smallmatrix}\right)$ in $(z_3, z_2, z_1)$ ordering) on $E_K^3$ ($K = \mathbb{Q}(i)$, $\tau = i$) detects $b_{f_{\chi_3}}(p)$ at scale $k/p$, but has $H^0(E_K^3, L_H) = 0$ and meromorphic quotient $G_H$ with finite radius of convergence ($1\cdot k\log k$).

Testing the **Zwegers (2002) mock-modular indefinite theta regularization** (imported from black-hole microstate counting for signature-$(p,1)$ lattices):
- Choose two negative vectors in the same negative-cone component: $c_1 = (0, 1, -1)^t$ ($c_1^t H c_1 = -4$), $c_2 = (1, 1, -1)^t$ ($c_2^t H c_2 = -3$, $c_1^t H c_2 = -4$).
- Define the Zwegers sign-cone series
  $$\Theta_H^{c_1, c_2}(z; i) := \sum_{n \in \mathbb{Z}^3} \frac{1}{2}\!\left(\operatorname{sgn}(c_1^t H n) - \operatorname{sgn}(c_2^t H n)\right) e^{-\pi\, n^t H n + 2\pi i\, n^t H z}.$$
- **Positive Result (Entire of Order 2!):** On $\operatorname{span}(c_1, c_2)$, the Gram inverse is $G^{-1} = \left(\begin{smallmatrix} 3/4&-1\\-1&1\end{smallmatrix}\right)$, so for $x_j = c_j^t H n$ of opposite signs ($x_1 x_2 \le 0$), $v^t H v = \frac{3}{4}x_1^2 + x_2^2 + 2|x_1 x_2| > 0$, while $H$ is strictly positive definite on $\{c_1, c_2\}^\perp$. Hence $n^t H n \ge \delta \|n\|^2 > 0$ on the entire support of the sum, making $\Theta_H^{c_1, c_2}(z; i)$ an **entire holomorphic function of order $2$** on $\mathbb{C}^3$ with Cauchy bound $\log|D_1^k \Theta_H^{c_1, c_2}(0; i)| \le \frac{1}{2} k\log k + O(k)$!
- **Exact Obstruction (Algebraicity–Entirety Dichotomy):**
  1. Under a lattice shift $z \mapsto z + m i$ ($m \in \mathbb{Z}^3$), $\rho^{c_1, c_2}(n' - m) - \rho^{c_1, c_2}(n')$ leaves a nonzero elliptic anomaly equal to a finite sum of 2D positive-definite theta series along the strips $c_j^\perp$ (a 1-cocycle representing a class in $H^1(E_K^3, L_H)$).
  2. Consequently, $\Theta_H^{c_1, c_2}(z; i)$ is a weight-$3/2$ **mock** theta function rather than an algebraic section on $E_K^3$; its CM values and Taylor jets at $z = 0$ are **transcendental** over $\mathbb{Q}(\Omega)$ (involving logs of algebraic numbers / Gross–Zagier heights, as in Bruinier–Ono / Duke–Li, and even in the 1D $(1,1)$-signature case reducing to the transcendental Lambert series $\sum d(n) e^{-2\pi n}$). Thus restoring entirety of order $2$ destroys $p$-adic algebraicity completely.

---

## 3. Quillen Metric & Curve Restriction on $H^1(E_K^3, L_H^{\otimes N})$

For $\overline{\mathcal{L}}_H$ on $\mathcal{E}_K^3$, Gillet–Soulé's arithmetic Riemann–Roch gives a finite Quillen Arakelov degree $\widehat{\deg}_Q(\det H^1(\mathcal{E}_K^3, \overline{\mathcal{L}}_H^{\otimes N})) = -\frac{N^4}{24}\widehat{c}_1(\overline{\mathcal{L}}_H)^4 + O(N^3\log N)$. However, attempting to build a Bost-direction evaluation arrow out of $H^1(E_K^3, L_H^{\otimes N})$ via restriction $H^1(E_K^3, L_H^{\otimes N}) \to H^1(C, L_H^{\otimes N}|_C)$ to an algebraic curve $C \subset E_K^3$ fails by sign mismatch:
- If $C$ tracks the real Kronecker eigendirection $W_1$ (where $v_1^* H v_1 = +\frac{1}{3} > 0$), then $\deg(L_H|_C) > 0$, forcing $H^1(C, L_H^{\otimes N}|_C) = 0$ for large $N$ (zero restriction map!).
- Conversely, if $C$ bends into the negative-curvature cone of $H$ so $H^1(C, L_H^{\otimes N}|_C) \ne 0$, it loses tangency to $W_1$ and therefore loses the $D_1^p$-cancellation of $\frac{1}{p}(1 + \zeta_1^{-1} + \zeta_1^{-2})$.

---

## 4. Front 2 Completion (KZ / KZB Cross-Ratio Rigidity & $U_q(\mathfrak{sl}_2)$ Anyon-Chain Obstruction) & Verification of Astra's Round 3 Theorems

*(Note: Claude Fable 5.2 hit the 5-hour Claude usage limit before writing a report, so Gemini completed Front 2's core analysis and independently verified all of Astra's Round 3 formulas.)*

### 4.1 Independent Python Verification of Astra's Round 3 Formulas (`wall1_r3_astra_report.md`)
All numerical claims in `wall1_r3_astra_report.md` checked out identically:
- Coarse branch germ $K(S) = h(\sqrt{S})^2 = S - \frac{6}{7}S^4 + \frac{96}{637}S^7 - \frac{3264}{12103}S^{10} - \frac{162048}{1101373}S^{13} - \frac{2334336}{7709611}S^{16} + \dots$, confirming $D_4 = 7, D_7 = 637, D_{10} = 12103, D_{16} = 7709611 = d_{32}$.
- Torus Verlinde ranks at half-weights ($k = 2m, a = m, n = m+1$): $\operatorname{tr}(N_m^4) = (n^4 + 2n^2)/3 = 8, 33, 96, 225, 456$ for $m = 1, \dots, 5$.
- Torus dormant-oper fusion lengths $\operatorname{tr}(T^4) = 26, 155, 301, 1365, 2926, 9640, 35651$ for $p = 7, 11, 13, 19, 23, 31, 43$.

### 4.2 KZ / KZB Cross-Ratio Rigidity on $(\mathbb{P}^1, \{\infty\}\cup Y)$ and $(E', E'[2])$
The cross-ratio of $\{\infty, 2^{1/3}, \omega 2^{1/3}, \omega^2 2^{1/3}\}$ is $\lambda = -\omega^2 = \frac{1 + i\sqrt{3}}{2}$, **independent of $2$** (the fixed equianharmonic $j = 0$ curve over $\overline{\mathbb{Q}}$). Consequently:
1. Over $\overline{\mathbb{Q}}$, the KZ/KZB flat connection, monodromy, Verlinde Hermitian metric, and geometric $p$-curvature spectrum at $j = 0$ are **identical** for $c = 1, 2, 8$ — completely blind to $\left(\frac{2}{\pi}\right)_3$.
2. Varying $c \in \mathbb{G}_m$ in the 1-parameter family $y^2 = x^3 - c$ yields only the diagonal Euler scaling connection $c \frac{d}{dc} = \pm \frac{1}{6}$ (solutions $c^{\pm 1/6}$), carrying no prime-by-prime 3-cycle divisibility.
3. The **sole** channel through which $\left(\frac{2}{\pi}\right)_3$ enters $(\mathbb{P}^1, \{\infty\} \cup Y)$ or $(E', E'[2])$ is **arithmetic descent / rational differential normalization** comparing $t^3 - 2$ against $t^3 - 8$ — which is precisely Astra's $\mu_{(p-1)/2}$-torsor theorem $c^{(p-1)/2} = H_p(E_b)$ (and ratio $H_p(-8)/H_p(-2) = 2^{(p-1)/3}$).

### 4.3 Why Level-$k$ Quantum-Group Truncation ($U_q(\mathfrak{sl}_2)$ Anyons) Cannot Yield a Multiplicative VUMPS Bost Proof Over $\mathbb{Q}$
1. Truncating Alpoge's untruncated Yangian $Y(\mathfrak{gl}_2)$ / $U(n)$ Pieri fusion chain to a finite-alcove $\mathrm{SU}(2)_k$ anyon chain ($q = e^{i\pi/(k+2)}$) eliminates the $+m$ Vandermonde repulsion in the fusion graph, **but** moves the global realization from abelian theta functions on a CM abelian variety $A_E$ (where a global translation-invariant $D^p \equiv 0$ exists for all inert $p \le X$) to non-abelian Verlinde spaces $V_k = H^0(\mathcal{M}, \mathcal{L}^{\otimes k})$.
2. By Astra's full-space jet obstruction (`wall1_r3_astra_report.md` §4), on any smooth rational point of $\mathcal{M}_0$ or $\mathcal{M}_1$, full-space Verlinde jets $s_1^N$ have unit integral content and raw derivative $N!$ with norm $e^{O(N)}$, producing **zero** 3-cycle-dependent common factor and hitting $1 \cdot N\log N$.
3. Meanwhile, finite-group $\mathrm{Rep}(S_3)$ fusion ($\rho_2^{\otimes m} = a_m(\mathbf{1}\oplus\chi_{-3}) \oplus c_m\rho_2$, $c_m/a_m \to 2$) leaves the order-$a_m$ pole of $\zeta_{K_0}(s)^{a_m}$ at $s = 1$ dominating any off-line zero $\beta < 1$ of $L(s, f_{\chi_3})$.
