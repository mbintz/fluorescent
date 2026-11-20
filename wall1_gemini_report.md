# Wall 1 — Round 2 Report (Gemini)
## Cubic Metaplectic $\theta_3$, Binary Quadratic Forms Under Dirichlet GRH, and an Indefinite Trace-Bundle $p$-Adic Detection Theorem on $E_K^3$

**Target:** $F = \mathbb{Q}(\sqrt[3]{2})$, $L_0 = \mathbb{Q}(\sqrt[3]{2}, \zeta_3)$, $\operatorname{Gal}(L_0/\mathbb{Q}) = S_3$, $K_0 = \mathbb{Q}(\sqrt{-3})$,
$$\zeta_F(s) = \zeta(s)\, L(s, f_{\chi_3}) = \zeta(s)\, L_{K_0}(s, \chi_3), \qquad f_{\chi_3}(z) = \eta(6z)\eta(18z) = \frac{1}{2}\!\left(\theta_{x^2+27y^2}(z) - \theta_{4x^2+2xy+7y^2}(z)\right).$$
Black-box inputs available: unconditional RH for $\zeta(s)$ and Dirichlet GRH for all $L(s,\chi)$ (`Main.lean`), CM/totally real ERH blueprint (`erh_totally_real_note.md`), and the Single-Triangle Weil Criterion (`frontier_a_report.md` §4).

---

## Executive Summary

1. **Door B1 (Cubic Metaplectic / Kubota–Patterson $\theta_3$ & Alpoge's Gauss-Sum Reciprocity):**
   - **Positive Automorphic Identity:** Using Eisenstein's cubic reciprocity law $\left(\frac{2}{c}\right)_3 = \left(\frac{c}{2}\right)_3$, the Fourier coefficients $\tau(\mu)$ of the Kubota–Patterson cubic theta function $\theta_3$ on $\widetilde{\mathrm{GL}}_2^{(3)}(\mathbb{A}_{K_0})$ satisfy $\tau(2\mu)\overline{\tau(\mu)} = \frac{\tau(2)}{\tau(1)}|\tau(\mu)|^2 \chi_3(\mu)$ for $(\mu,6)=1$. The product $\theta_3(2\cdot)\overline{\theta_3(\cdot)}$ is a **genuine non-metaplectic** automorphic form on $\Gamma_0(6)\backslash \mathbb{H}_3$ of nebentypus $\overline{\chi_3}$, yielding the exact Rankin–Selberg identity
     $$\bigl\langle \theta_3(2\cdot),\; \theta_3(\cdot)\, E^*_{\chi_3}(\cdot, 2w) \bigr\rangle \;\propto\; (\text{explicit } 2,3\text{-factors})\cdot \Lambda_{K_0}(w, \chi_3)\,\zeta_{K_0}(3w+1).$$
   - **Exact Obstructions:** (i) $\mathbb{H}_3$ has no complex/Shimura structure, no formal group, and no $D^p \equiv 0$ mechanism; (ii) the scattering-matrix poles of $E_{\chi_3}(\cdot, 2w)$ at $2w = \rho_0$ lie in $\operatorname{Re}(2w) < 1$ where resonances are permitted; (iii) attempting to inject the Heath-Brown–Patterson cubic large sieve via $\chi_3(c) = \widetilde{g}_3(1,c)\overline{\widetilde{g}_3(2,c)}$ fails identically because the bilinear reciprocity factors **cancel**: $\overline{\left(\frac{m}{n}\right)_3}\cdot \left(\frac{m}{n}\right)_3 = 1$.

2. **Door B2 (Binary Quadratic Forms $Q_1, Q_2$ Armed with Dirichlet GRH + CM-Field ERH):**
   - Under Dirichlet GRH for $L(s, \chi_{-3})$, Wall 1 ($\mathrm{GRH}(F)$) is equivalent to $\pi_{x^2+27y^2}(X) = \frac{1}{6}\operatorname{Li}(X) + O_\varepsilon(X^{1/2+\varepsilon})$, and by eta-positivity + Landau's theorem, even a **one-sided** bound $\sum_{p=x^2+27y^2 \le X}\log p \log(X/p) \le \frac{1}{6}X + O(X^\theta)$ (or $\ge \frac{1}{6}X - O(X^\theta)$) implies $L(s, f_{\chi_3}) \ne 0$ for $\operatorname{Re}(s) > \theta$.
   - **Exact Obstructions:** Although smooth Type-I sums $A_d(\phi; X) = \sum_{d \mid n} b_{f_{\chi_3}}(n)\phi(n/X)$ achieve full level of distribution $\vartheta = 1$ ($O_A(X^{-A})$ up to $d \le X^{1-\varepsilon}$ via Voronoi summation for $f_{\chi_3}$), **no pure sieve, Type-I/II bilinear argument, or de la Vallée Poussin positivity argument using RH($\zeta_{K_0}$) yields even a constant-width zero-free strip $\operatorname{Re}(s) > 1 - \delta$**: Type-I sums depend solely on holomorphy and the functional equation of $L(s, f_{\chi_3})$ (blind to zeros), Type-II sums factor over $\operatorname{Cl}(\mathbb{Z}[3\sqrt{-3}])$, Selberg's parity factor $2$ stops at $\frac{1}{3}X/\log X$, and in $3+4\cos\theta+\cos 2\theta$ the pole of $\zeta_{K_0}(s)$ at $s=1$ and the Gamma conductor $\frac{1}{2}\log|t|$ remain untouched by RH($\zeta_{K_0}$).
   - **Note on CM Elliptic Curves (Wall 1.5):** Even weight-2 CM elliptic curves $E_1: y^2=x^3+1$ and $E': y^2=x^3-2$ (related by $\psi_{E'} = \psi_{E_1}\cdot \chi_{-2}\cdot \chi_3$) are *not* covered by CM-field ERH because their Grossencharacter phase $\pi/|\pi| \in S^1$ has infinite order and cannot be isolated by finite Galois classes at supersingular primes.

3. **Door B3 (New Local $p$-Adic Breakthrough + Sharp Global Cohomological Obstruction on $E_K^3$):**
   - **Positive Local Theorem (Theorem 1):** Even though $F = \mathbb{Q}(\sqrt[3]{2})$ cannot be the center of $\operatorname{End}^0(A)$ for any abelian variety (Albert/Weil), $\mathcal{O}_F$ acts integrally on the **CM abelian threefold** $E_K^3$ ($E_K: y^2=x^3-x$, CM by $K = \mathbb{Q}(i)$) via $M_{\sqrt[3]{2}} = \left(\begin{smallmatrix} 0&0&2\\1&0&0\\0&1&0\end{smallmatrix}\right) \in M_3(\mathbb{Z})$. Taking the **trace-form Hermitian bundle** $L_H = L_{H_+} \otimes L_{H_-}^{-1}$ with $H = \left(\begin{smallmatrix} 1&0&0\\0&0&2\\0&2&0\end{smallmatrix}\right)$ (signature $(2,1)$) and explicit meromorphic theta quotient
     $$G_H(z_1, z_2, z_3) = \frac{\tilde\sigma(z_3)\,\tilde\sigma(z_1+z_2)^2}{\tilde\sigma(z_1)^2\,\tilde\sigma(z_2)^2}, \qquad \tilde\sigma(z) = \frac{\sigma_{E_K}(z)}{z},$$
     differentiated along the single $\sqrt[3]{2}$-eigendirection $D_1 = \alpha_1^2 \partial_{z_1} + \alpha_1 \partial_{z_2} + \partial_{z_3}$, the $p$-adic pole $\frac{c'}{p}(z_3^{p+1}+2z_1z_2^p+2z_2z_1^p) = \frac{c'}{p}\frac{w^{p+1}}{3^{p+1}}(1+\zeta_1^{-1}+\zeta_1^{-2})$ **cancels mod $p$ precisely at non-split places** ($\zeta_1 = \alpha_1^{p-1} \ne 1$). Across **all three splitting types** of primes $p$ inert in $\mathbb{Q}(i)$, the norm valuation is an **exact linear function of $b_{f_{\chi_3}}(p)$ at scale $k/p$**:
     $$\frac{1}{3}\, v_p\!\left(N_{F/\mathbb{Q}}\!\left(\frac{D_1^k G_H(0)}{\Omega^k}\right)\right) = \left(\frac{2}{3} - \frac{1}{3} b_{f_{\chi_3}}(p)\right)\frac{k}{p} + O\!\left(\frac{k}{p^2}\right),$$
     verified explicitly by exact rational arithmetic up to $k = 100$ for $p \in \{7, 11, 19, 23, 31, 43\}$.
   - **Sharp Global Obstruction (Theorem 2):** Any symmetric matrix $H \in \operatorname{Sym}_3(\mathbb{Z})$ achieving this cancellation at $p = 4x^2+2xy+7y^2$ must be a trace form $H_\gamma = \left(\begin{smallmatrix} a&b&c\\b&c&2a\\c&2a&2b\end{smallmatrix}\right)$, which is **never positive definite** (positivity of the three $2\times 2$ principal minors gives $ac>b^2, 2bc>4a^2, 2ab>c^2 \implies 2a^2b^2c^2 > 2a^2b^2c^2$). Consequently $H^0(E_K^3, L_H) = 0$ while $H^1(E_K^3, L_H) \ne 0$, reversing the jet-evaluation arrow from $H^0(L) \hookrightarrow \mathrm{Jets}_0$ to $\mathrm{Jets}_0 \hookrightarrow H^1(\mathfrak{m}_0^a L)$. Every meromorphic quotient $s_+/s_-$ loses the Archimedean–$p$-adic balance ($1 \cdot k\log k$ vs $\frac{1}{3} k\log k$) by Wirtinger zero density on the Kronecker leaf $W_1$, and attempting to flatten $s_-(w) = s_-(0) + O(w^{a+1})$ forces every inert prime $p \le a$ to divide $s_-(0)$ to order $\ge a/(p+1)$, annihilating the $p$-adic gain.

4. **Synthesis with GPT-6.2-Astra's Parallel Discovery (`wall1_astra_report.md`):**
   - We independently verified Astra's rational formal homomorphism $h(z) = \ell_1^{-1}(\ell_0(z)) \in \mathbb{Q}[[z]]$ between $E_0: y^2=x^3-2$ and $E_1: y^2=x^3-8$, confirming $d_7=7, d_{11}=7, d_{13}=91, d_{14}=637, d_{19}=12103, d_{25}=84721, d_{31}=7^4\cdot 13^2\cdot 19^1$ (zero factor of $31$), as well as Astra's Mellin identity and oscillation bounds.
   - Strikingly, **both** Astra's ordinary-prime map $h(z)$ ($\frac{2}{3}N\log N$ $p$-adic divisibility vs $1\cdot N\log N$ finite-radius Archimedean growth) and Gemini's supersingular-prime trace quotient $G_H(w)$ ($\frac{1}{3}k\log k$ vs $1\cdot k\log k$) independently hit the **exact same global barrier**: local $p$-adic detection at linear scale $k/p$ is *completely solved* inside standard CM geometry, while the missing piece is an **entire (order $\le 3$ or $2$) global automorphic/Arakelov realization** whose Archimedean growth matches the $p$-adic slope.

---

## 1. Door B1: Cubic Metaplectic $\theta_3$ and Gauss-Sum Reciprocity

### 1.1 Exact Conductor and Eisenstein Reciprocity for $\chi_3$

In $K_0 = \mathbb{Q}(\omega)$ ($\omega = e^{2\pi i/3}$), the ring of units $\mu_6 = \{\pm 1, \pm \omega, \pm \omega^2\}$ injects into $(\mathcal{O}_{K_0}/(6))^\times \cong \mathbb{F}_4^\times \times (\mathcal{O}_{K_0}/(3))^\times \cong C_3 \times C_6$. Writing $\psi_2(\alpha) = (\alpha \bmod 2) \in \mathbb{F}_4^\times = \{1,\omega,\omega^2\}$ and $\psi_3: (\mathcal{O}_{K_0}/(3))^\times/\{\pm 1\} \xrightarrow{\sim} \mu_3$ with $\psi_3(\omega) = \omega$, the anticyclotomic cubic ray-class character of conductor $(6)$ is
$$\chi_3(\alpha) = \psi_2(\alpha)\,\psi_3(\alpha)^{-1}.$$
For any primary element $c \equiv 1 \pmod 3$ coprime to $2$, $\psi_3(c) = 1$, and by Eisenstein's supplementary cubic reciprocity law:
$$\chi_3(c) = \left(\frac{2}{c}\right)_3 = \left(\frac{c}{2}\right)_3 = (c \bmod 2) \in \{1,\omega,\omega^2\}.$$
(Check: for $p=7$, $\pi = 1+3\omega \equiv 1+\omega \equiv \omega^2 \pmod 2$, and $2^{(7-1)/3} = 4 \equiv \omega^2 \pmod{\pi}$; for $p=31$, $\pi = -5-6\omega \equiv 1 \pmod 2$, and $4^3 \equiv 2 \pmod{31}$.)

### 1.2 Rankin–Selberg Realization of $L_{K_0}(w, \chi_3)$ via Kubota–Patterson $\theta_3$

Let $g_3(r, c) = \sum_{x \bmod c} \left(\frac{x}{c}\right)_3 e\!\left(\operatorname{Tr}_{K_0/\mathbb{Q}}\!\left(\frac{rx}{\sqrt{-3}\,c}\right)\right)$ be the cubic Gauss sum for primary $c \equiv 1 \pmod 3$, and let $\theta_3 = \operatorname{Res}_{s=4/3} E_3(\cdot, s)$ be the Kubota–Patterson cubic theta function on $\Gamma_3 \backslash \mathbb{H}_3$:
$$\theta_3(z, v) = c_0 v^{2/3} + \sum_{0 \ne \mu \in \lambda^{-3}\mathcal{O}_{K_0}} \tau(\mu)\, v\, K_{1/3}(4\pi |\mu| v)\, e\!\left(\operatorname{Tr}(\mu z)\right).$$
By Patterson (1977) Theorem 8.1 and Kazhdan–Patterson periodicity, normalized so $|\tau(1)| = 1$:
- For squarefree primary $c \equiv 1 \pmod 3$: $\tau(c) = \overline{g_3(1, c)} / |c|$ (so $|\tau(c)| = 1$).
- For primes $\pi \nmid 3$: $\tau(\pi^2) = 0$ and $\tau(\pi^3 m) = N(\pi)^{-1/2} \tau(m)$.
- Twisted multiplicativity for coprime $m, c$:
  $$g_3(1, mc) = \left(\frac{m}{c}\right)_3 \left(\frac{c}{m}\right)_3 g_3(1,m) g_3(1,c).$$

Specialize to $m = 2$ (inert prime in $K_0$, $N(2) = 4$, $|g_3(1,2)| = 2$, so $\tau(2) \ne 0$). For every primary squarefree $c$ coprime to $6$, cubic reciprocity gives $\left(\frac{2}{c}\right)_3 \left(\frac{c}{2}\right)_3 = \left(\frac{2}{c}\right)_3^2 = \overline{\chi_3(c)}$, whence after conjugation
$$\tau(2c) = \frac{\tau(2)}{\tau(1)}\, \chi_3(c)\, \tau(c).$$
Since $\chi_3(d^3) = 1$, periodicity $\tau(c d^3) = N(d)^{-1/2}\tau(c)$ extends this to **all** $\mu$ coprime to $6$:
$$\tau(2\mu)\,\overline{\tau(\mu)} = \frac{\tau(2)}{\tau(1)}\, |\tau(\mu)|^2\, \chi_3(\mu).$$
Moreover, conjugating $\gamma = \left(\begin{smallmatrix} a&b\\c&d\end{smallmatrix}\right) \in \Gamma_0(2) \cap \Gamma_3$ by $\left(\begin{smallmatrix} 2&0\\0&1\end{smallmatrix}\right)$ multiplies the Kubota cubic cocycle $\kappa_3(\gamma) = \left(\frac{d}{c}\right)_3$ by
$$\kappa_3\!\begin{pmatrix} a&2b\\c/2&d\end{pmatrix}\overline{\kappa_3\!\begin{pmatrix} a&b\\c&d\end{pmatrix}} = \overline{\left(\frac{d}{2}\right)_3} = \overline{\chi_3(d)}.$$
Hence $\theta_3(2\cdot)\overline{\theta_3(\cdot)}$ is a **genuine non-metaplectic** automorphic function on $\Gamma_0(6)\backslash \mathbb{H}_3$ with nebentypus $\overline{\chi_3}$. Pairing with the non-metaplectic Eisenstein series $E_{\chi_3}(\cdot, 2w)$ (measure $dx\,dy\,dv/v^3$; $\int_0^\infty v^2 K_{1/3}(4\pi|\mu|v)^2 v^{2w} dv/v^3 \propto N(\mu)^{-w}$) unfolds to:
$$\sum_{(\mu,6)=1} \frac{\tau(2\mu)\,\overline{\tau(\mu)}}{N(\mu)^w} = \frac{\tau(2)}{\tau(1)} \prod_{\pi \nmid 6} \frac{1 + \chi_3(\pi) N(\pi)^{-w}}{1 - N(\pi)^{-1-3w}} = \frac{\tau(2)}{\tau(1)}\, \frac{L_{K_0}^{(6)}(w, \chi_3)\,\zeta_{K_0}^{(6)}(3w+1)}{L_{K_0}^{(6)}(2w, \overline{\chi_3})}.$$
The denominator $L_{K_0}(2w, \overline{\chi_3})$ matches the scattering denominator of $E_{\chi_3}(\cdot, 2w)$ identically; clearing it with the completed Eisenstein series $E^*_{\chi_3}(\cdot, 2w) = \Lambda_{K_0}(2w, \overline{\chi_3}) E_{\chi_3}(\cdot, 2w)$ yields
$$\bigl\langle \theta_3(2\cdot),\; \theta_3(\cdot)\, E^*_{\chi_3}(\cdot, 2w) \bigr\rangle \;\propto\; (\text{explicit } 2,3\text{-factors})\cdot \Lambda_{K_0}(w, \chi_3)\,\zeta_{K_0}(3w+1).$$

### 1.3 Why Cubic Metaplectic $\theta_3$ and Cubic Gauss Sums Do Not Break Wall 1

1. **No spectral/pole contradiction:** A hypothetical off-line zero $\rho_0 = \beta + i\gamma$ ($\beta \in (\frac{1}{2}, 1)$) of $L_{K_0}(s, \overline{\chi_3})$ creates a pole of $E_{\chi_3}(\cdot, 2w)$ at $2w = \rho_0$, i.e., in the **left** half-plane $\operatorname{Re}(2w) < 1$ where scattering resonances of $\Gamma_0(6)\backslash\mathbb{H}_3$ are allowed (there are no residual poles in $\operatorname{Re}(2w) > 1$ for $\chi_3 \ne 1$).
2. **No algebraic/Bost/$D^p \equiv 0$ structure:** $\mathbb{H}_3 = \mathrm{SL}_2(\mathbb{C})/\mathrm{SU}(2)$ has no complex structure, no Shimura variety, no formal group, and no $\ell$-adic $D^\ell \equiv 0$ operator. (The Gross–Koblitz formula expresses $g_3(\pi)$ $p$-adically only at the *same* prime $p = N(\pi)$.)
3. **Reciprocity Cancellation Kills the Heath-Brown–Patterson Bilinear Sieve:** Heath-Brown–Patterson (1979) and Heath-Brown (2000) obtain power saving $\sum_{N(\pi) \le X} \widetilde{g}_3(\pi) \ll X^{1-\delta}$ because $\widetilde{g}_3(mn) = \overline{\left(\frac{m}{n}\right)_3}\widetilde{g}_3(m)\widetilde{g}_3(n)$ carries a **non-degenerate bilinear kernel** $\overline{\left(\frac{m}{n}\right)_3}$ to which the cubic large sieve applies. Writing $\chi_3(c) = \widetilde{g}_3(1, c)\overline{\widetilde{g}_3(2, c)}$ and splitting $c = mn$ gives
   $$\widetilde{g}_3(1, mn)\,\overline{\widetilde{g}_3(2, mn)} = \underbrace{\overline{\left(\frac{m}{n}\right)_3}\cdot \left(\frac{m}{n}\right)_3}_{=\; 1}\cdot \widetilde{g}_3(1,m)\overline{\widetilde{g}_3(2,m)}\cdot \widetilde{g}_3(1,n)\overline{\widetilde{g}_3(2,n)}.$$
   More generally, for $\widetilde{g}_3(1,c)^a \widetilde{g}_3(2,c)^b = \overline{\chi_3(c)}^b \widetilde{g}_3(1,c)^{a+b}$, the reciprocity coupling $\overline{\left(\frac{m}{n}\right)_3}^{a+b}$ survives **iff** $3 \nmid (a+b)$, precisely when the sum is an oscillatory Gauss-sum twist rather than a multiplicative character sum governing $L_{K_0}(s, \chi_3)$.
4. **Codebase audit (`lean/src/`):** Grep across `lean/src/` confirms that Alpoge–Claude's finalized proof does not use the sixfold cover of $\mathrm{GL}_5$ mentioned in `remark.pdf` (items 3, 16); `MetaplecticRepresentation` in `CompanionTheory/ThickeningEstimates` is purely the standard 2-fold Weil representation for unitary dual pairs.

---

## 2. Door B2: Binary Quadratic Form Prime Sums Armed with Dirichlet GRH & CM-Field ERH

### 2.1 Reduction via Dirichlet GRH + Eta Positivity

Let $Q_1(x,y) = x^2 + 27y^2$ and $Q_2(x,y) = 4x^2 + 2xy + 7y^2$ (discriminant $-108$, class group $\operatorname{Cl}(\mathcal{O}) = \{[Q_1], [Q_2], [\overline{Q_2}]\} \cong C_3$). For $(n,6) = 1$:
$$\frac{1}{2}\!\left(r_{Q_1}(n) + 2 r_{Q_2}(n)\right) = \sum_{d \mid n} \chi_{-3}(d), \qquad \frac{1}{2}\!\left(r_{Q_1}(n) - r_{Q_2}(n)\right) = b_{f_{\chi_3}}(n).$$
On primes $p > 3$: $r_{Q_1}(p) = 4$ (when $p \in Q_1$, density $1/6$) and $r_{Q_2}(p) = 2$ (when $p \in Q_2$, density $1/3$), giving $b_{f_{\chi_3}}(p) = 3\mathbf{1}_{p \in Q_1} - \mathbf{1}_{p \equiv 1 (3)}$. Since Dirichlet GRH gives $\sum_{p \equiv 1(3), p \le X} \log p \log(X/p) = \frac{1}{2}X + O(X^{1/2}\log^2 X)$, and $L(s, f_{\chi_3})$ has no real zeros in $(\frac{1}{2}, 1)$ (because $f_{\chi_3}(iy) = \eta(6iy)\eta(18iy) > 0$), Landau's theorem on the Mellin integral
$$S_2(X) := \sum_{n \le X} \Lambda(n) b_{f_{\chi_3}}(n)\log\!\left(\frac{X}{n}\right) = \frac{1}{2\pi i}\int_{(c)} \left(-\frac{L'}{L}(s, f_{\chi_3})\right)\frac{X^s}{s^2}\,ds$$
implies that for **any** $\theta \in [\frac{1}{2}, 1)$, **either** one-sided bound
$$\sum_{\substack{p = x^2 + 27y^2 \le X}} \log p \log\!\left(\frac{X}{p}\right) \;\le\; \frac{1}{6} X + O(X^\theta) \qquad \text{or} \qquad \ge\; \frac{1}{6} X - O(X^\theta)$$
is equivalent to $L(s, f_{\chi_3}) \ne 0$ for $\operatorname{Re}(s) > \theta$.

### 2.2 Sharp Obstructions to Sieve, Type I/II, and Positivity Attacks

1. **Full Level of Distribution $\vartheta = 1$ Is Still Blind to Zeros:**
   By Hecke multiplicativity and Voronoi summation for the holomorphic cusp form $f_{\chi_3} \in S_1(\Gamma_0(108), \chi_{-3})$, for any smooth compactly supported $\phi$ the Type-I divisor sums satisfy
   $$A_d(\phi; X) = \sum_{d \mid n} b_{f_{\chi_3}}(n)\,\phi(n/X) = O_A(X^{-A}) \qquad \text{for all } d \le X^{1-\varepsilon}$$
   (with the $k=d$ diagonal term contributing only $O(\sqrt{X})$ summed over $d \le \sqrt{X}$). Yet this gives **no** zero-free strip $\operatorname{Re}(s) > 1 - \delta$:
   - Every Type-I sum depends solely on the **holomorphy and functional equation** of $L(s, f_{\chi_3})$ (not of $L'/L$), which remain intact in the presence of arbitrary off-line zeros of $L(s, f_{\chi_3})$.
   - In Vaughan's identity with $UV \le X^{1-\varepsilon}$, balanced Type-II sums ($M, N \approx \sqrt{X}$) factor completely via $r_{Q_1}(mn) - r_{Q_2}(mn) = \left(\sum_{N(\mathfrak{a})=m}\chi_3(\mathfrak{a})\right)\left(\sum_{N(\mathfrak{b})=n}\chi_3(\mathfrak{b})\right) + \text{conj}$, yielding a **rank-1** bilinear matrix with zero cancellation unless cancellation in $\sum \mu(\mathfrak{a})\chi_3(\mathfrak{a})$ (equivalent to a zero-free strip for $L_{K_0}(s, \chi_3)$) is already known.
   - Selberg's linear upper-bound sieve with $\vartheta = 1$ incurs the **parity factor $2$**, giving only $\pi_{Q_1}(X) \le (2 + o(1)) \cdot \frac{1}{6}\frac{X}{\log X} = \frac{1}{3}\frac{X}{\log X}$ (since products $p_1 p_2$ and $p_1 p_2 p_3$ of $Q_2$-primes are represented by $Q_1$), far above the sharp constant $\frac{1}{6} + O(X^{-\delta})$ needed by Landau's criterion.
   - Fixing $y$ reduces $x^2 + 27y^2$ to the 1-variable Bunyakovsky/Landau problem (open even under GRH), while Heath-Brown's $p = x^3 + 2y^3$ captures only a thin $O(X^{2/3}/\log X)$ subset of $Q_1$-primes.

2. **De la Vallée Poussin / Rankin–Selberg Positivity Under RH($\zeta_{K_0}$):**
   Since $\rho_2 \otimes \rho_2 = \mathbf{1} \oplus \chi_{-3} \oplus \rho_2$, all tensor and symmetric powers of $\rho_2$ stay inside $\{\mathbf{1}, \chi_{-3}, \rho_2\}$. In the positivity inequality $3 + 4\operatorname{Re}(\chi_3(\mathfrak{p})N\mathfrak{p}^{-it}) + \operatorname{Re}(\chi_3(\mathfrak{p})^2 N\mathfrak{p}^{-2it}) \ge 0$, knowing RH for $\zeta_{K_0}(s)$ removes only the non-trivial zeros of $\zeta_{K_0}$, leaving both the **pole of $\zeta_{K_0}(s)$ at $s=1$** ($\frac{3}{\sigma - 1}$) and the **Gamma conductor** $\frac{5}{2}\log(|t|+2)$ of $L_{K_0}(s,\chi_3)$ intact; thus it does not even improve the classical de la Vallée Poussin / Mitsui zero-free region.

3. **Remark on Weight-2 CM Elliptic Curves (Wall 1.5):**
   The CM elliptic curves $E_1: y^2 = x^3 + 1$ and $E': y^2 = x^3 - 2$ (both with CM by $K_0$) have Grossencharacters related by
   $$\psi_{E'}(\pi) = \psi_{E_1}(\pi)\cdot \left(\frac{-2}{N(\pi)}\right)_2 \cdot \chi_3(\pi),$$
   so $L(s, E' \times E_1) = L(s, f_{\chi_3} \otimes \chi_{-2}) \cdot L_{K_0}(s, \chi_{-2}\chi_3 \psi_2)$. However, CM-field ERH (`erh_totally_real_note.md`) does **not** prove GRH for $L(s, E_1)$ or $L(s, E')$: in Alpoge's proof (`Formalism/IncomingBounds/IncomingBound.lean` & `GaussJetBounds/Statement.lean`), primes enter solely through Frobenius orbits on the finite Galois set $\operatorname{Hom}(E, \mathbb{C})$ at supersingular primes ($D^p \equiv 0$), which cannot detect the continuous Grossencharacter angle $\pi/|\pi| \in S^1$; at ordinary primes $p \equiv 1 \pmod 3$, $D^p - a_p D \equiv 0 \pmod p$ varies with $p$ and cannot be generated by a single global derivation $D$.

---

## 3. Door B3: The Indefinite Trace-Form Bundle on $E_K^3$ — Exact $p$-Adic Detection at Scale $k/p$ and the $H^1$ Obstruction

### 3.1 Embedding $\mathcal{O}_F$ into $\operatorname{End}(E_K^3)$ Without Violating Albert/Weil

Albert's classification restricts only the **center** of $\operatorname{End}^0(A)$ to be totally real or CM; it does **not** forbid $F = \mathbb{Q}(\sqrt[3]{2})$ from embedding into a matrix algebra $M_3(K) = \operatorname{End}^0(E_K^3)$ (or into a Type IV degree-3 division algebra $D/K_0$ ramified at $\mathfrak{q}, \bar{\mathfrak{q}}$ above $q=7$). Concretely, let
$$E_K: y^2 = x^3 - x \qquad (\text{CM by } K = \mathbb{Q}(i), \text{ supersingular at all } p \equiv 3 \pmod 4).$$
Then $\mathcal{O}_F = \mathbb{Z}[\alpha_1]$ ($\alpha_1 = \sqrt[3]{2}$) acts integrally on $B := E_K^3$ via the integer endomorphism
$$M_{\sqrt[3]{2}} = \begin{pmatrix} 0 & 0 & 2 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix} \in M_3(\mathbb{Z}) \subset \operatorname{End}(E_K^3).$$
Its invariant eigenderivation for $\alpha_1$ on $\operatorname{Lie}(E_K^3) = \mathbb{C}^3$ is $D_1 = \alpha_1^2 \partial_{z_1} + \alpha_1 \partial_{z_2} + \partial_{z_3}$, dual to the 1-parameter complex line
$$W_1: \quad (z_1, z_2, z_3) = \left(\frac{w}{3\alpha_1^2},\; \frac{w}{3\alpha_1},\; \frac{w}{3}\right).$$

### 3.2 Theorem 1 (Exact $p$-Adic Splitting Detection on $E_K^3$ at Order $k/p$)

At any prime $p \equiv 3 \pmod 4$ ($p > 3$, supersingular for $E_K$), the Weierstrass sigma function $\tilde\sigma(z) = \sigma_{E_K}(z)/z$ satisfies $\log \tilde\sigma(z) = \frac{c'}{p} z^{p+1} + (\text{terms of higher } p\text{-adic weight})$ with $c' \in \mathbb{Z}_p^\times$ (corresponding to `IsBiPower` with $\alpha=0, \beta=1$ in `Formalism/GaussJetBounds/Statement.lean`). For any symmetric integer matrix $H = (h_{k,\ell})_{0 \le k,\ell \le 2} \in \operatorname{Sym}_3(\mathbb{Z})$ (indexed in the ordering $(z_3, z_2, z_1)$), the canonical line bundle $L_H$ on $E_K^3$ has $p$-adic theta exponent
$$\beta_H(z) = \frac{c'}{p} \sum_{k,\ell=0}^2 h_{k,\ell}\, z_{3-k}\, z_{3-\ell}^p + \dots$$
Along the line $W_1$, writing $\zeta_1 := \alpha_1^{p-1}$:
$$\sum_{k,\ell=0}^2 h_{k,\ell}\, z_{3-k}\, z_{3-\ell}^p = \frac{w^{p+1}}{3^{p+1}} \sum_{k,\ell=0}^2 h_{k,\ell}\, \alpha_1^{-(k+\ell)}\, \zeta_1^{-\ell}.$$
Taking the trace-form matrix of $F = \mathbb{Q}(\sqrt[3]{2})$,
$$H = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 2 \\ 0 & 2 & 0 \end{pmatrix} = \underbrace{\begin{pmatrix} 2 & 0 & 0 \\ 0 & 3 & 2 \\ 0 & 2 & 3 \end{pmatrix}}_{H_+ > 0} - \underbrace{\begin{pmatrix} 1 & 0 & 0 \\ 0 & 3 & 0 \\ 0 & 0 & 3 \end{pmatrix}}_{H_- > 0},$$
realized explicitly by the meromorphic Weierstrass quotient
$$G_H(z_1, z_2, z_3) := \frac{\tilde\sigma(z_3)\,\tilde\sigma(z_1+z_2)^2}{\tilde\sigma(z_1)^2\,\tilde\sigma(z_2)^2},$$
we obtain along $W_1$:
$$z_3^{p+1} + 2\left((z_1+z_2)^{p+1} - z_1^{p+1} - z_2^{p+1}\right) \equiv z_3^{p+1} + 2 z_1 z_2^p + 2 z_2 z_1^p = \frac{w^{p+1}}{3^{p+1}}\!\left(1 + \zeta_1^{-1} + \zeta_1^{-2}\right) \pmod p.$$

**Theorem 1.** Let $p > 3$ be inert in $K = \mathbb{Q}(i)$ ($p \equiv 3 \pmod 4$) and let $\xi_k := k!\,[w^k]\,G_H(w) = D_1^k G_H(0) \in F$.
- At every place $\mathfrak{P} \mid p$ of $F$ of **degree $1$** ($\alpha_1 \in \mathbb{Z}_p$), $\zeta_1 \equiv 1 \pmod{\mathfrak{P}}$, so $1+\zeta_1^{-1}+\zeta_1^{-2} = 3 \not\equiv 0 \pmod{\mathfrak{P}}$; the $\frac{1}{p}w^{p+1}$ pole survives and $v_{\mathfrak{P}}(\xi_k) = \frac{k}{p^2-1} + O(\log k)$.
- At every place $\mathfrak{P} \mid p$ of $F$ of **degree $f \in \{2, 3\}$** ($\alpha_1 \notin \mathbb{Z}_p$), $\zeta_1$ is a primitive cube root of unity mod $\mathfrak{P}$, so $1+\zeta_1^{-1}+\zeta_1^{-2} \equiv 0 \pmod{\mathfrak{P}}$; the $\frac{1}{p}w^{p+1}$ pole **vanishes identically**, raising the valuation to $v_{\mathfrak{P}}(\xi_k) = \frac{k}{p} + O\!\left(\frac{k}{p^2}\right)$.

Summing over places $\mathfrak{P} \mid p$ weighted by residue degree $f_{\mathfrak{P}}$, the normalized norm valuation detects $b_{f_{\chi_3}}(p) \in \{+2, 0, -1\}$ **linearly across all three splitting types** at order $k/p$:
$$\frac{1}{3}\, v_p\!\left(N_{F/\mathbb{Q}}\!\left(D_1^k G_H(0)\right)\right) = \left(\frac{2}{3} - \frac{1}{3}\, b_{f_{\chi_3}}(p)\right)\frac{k}{p} + O\!\left(\frac{k}{p^2}\right) = \left(1 - \frac{a_{\zeta_F}(p)}{3}\right)\frac{k}{p} + O\!\left(\frac{k}{p^2}\right).$$

**Exact Rational Verification (computed in Python up to $k = 100$ for $E_K: y^2 = x^3 - x$):**

| Prime $p$ ($p \equiv 3 \bmod 4$) | Splitting in $F$ | $b_{f_{\chi_3}}(p)$ | Predicted $\frac{2 - b_f(p)}{3}$ | $v_p([w^{p+1}]\log G_H)$ | Observed $\frac{\frac{1}{3}v_p(N(\xi_k))}{k/p}$ ($k \le 100$) |
|---:|---|---:|---:|---:|---|
| $7$ | inert ($f=3$) | $-1$ | $1.0000$ | $0$ (cancelled!) | $k=56$: $1.0000$, $k=84$: $1.0000$, $k=100$: $0.9800$ |
| $19$ | inert ($f=3$) | $-1$ | $1.0000$ | $0$ (cancelled!) | $k=40,60,80,100$: $0.9500$ |
| $11$ | $(1,2)$ | $0$ | $0.6667$ | — (mixed) | $k=24..96$: $0.6111$, $k=100$: $0.6967$ |
| $23$ | $(1,2)$ | $0$ | $0.6667$ | — (mixed) | $k=24..96$: $0.6389$, $k=100$: $0.6133$ |
| $31$ | split $(1,1,1)$ | $+2$ | $0.0000$ | $-1$ (survives) | $k=32,64,96,100$: $0.0000$ |
| $43$ | split $(1,1,1)$ | $+2$ | $0.0000$ | $-1$ (survives) | $k=44,88,100$: $0.0000$ |

*(For comparison, the positive-definite identity bundle $I_3$ gives $v_p([w^{p+1}]\log G_{I_3}) = -1$ and $v_p(D_1^k G_{I_3}) \approx \frac{k}{p^2-1}$ at **all** of $p=7,19,31,43$.)*

### 3.3 Theorem 2 (The Sharp Signature / $H^1$ Obstruction)

Despite Theorem 1's exact $k/p$ detection, $G_H$ cannot enter Bost's slope inequality because of a tight three-part obstruction:

1. **Uniqueness & Indefiniteness of $H$:** Grouping $\sum_{k,\ell} h_{k,\ell}\alpha_1^{-(k+\ell)}\zeta_1^{-\ell}$ by $k+\ell \pmod 3$ shows that vanishing mod $p$ for both primitive cube roots $\zeta_1 \in \{\omega, \omega^2\}$ forces
   $$h_{12} = h_{21} = 2h_{00},\qquad h_{20} = h_{11} = h_{02},\qquad h_{10} = h_{01} = \tfrac{1}{2} h_{22},$$
   i.e., $H = H_\gamma = \left(\begin{smallmatrix} a&b&c\\b&c&2a\\c&2a&2b\end{smallmatrix}\right)$, the trace form $\operatorname{Tr}_{F/\mathbb{Q}}(\gamma xy)$. Positive definiteness of $H_\gamma$ requires positivity of the three $2\times 2$ principal minors:
   $$ac > b^2,\qquad 2bc > 4a^2,\qquad 2ab > c^2 \;\Longrightarrow\; 2a^2b^2c^2 > 2a^2b^2c^2,$$
   a contradiction. Every nonzero $H_\gamma$ has signature $(2,1)$ or $(1,2)$. (Curiously, the Hermitian curvature along the three eigenlines is $v_1^* H_\gamma v_1 = \tau_1(\gamma) > 0$ at the real place and $v_2^* H_\gamma v_2 = v_3^* H_\gamma v_3 = 0$ identically at the complex places!)
2. **Cohomological Arrow Reversal ($H^0 = 0, H^1 \ne 0$):** By Mumford–Kempf vanishing on abelian varieties, a non-degenerate line bundle $L_H$ of signature $(2,1)$ on $E_K^3$ has $H^0(E_K^3, L_H^{\otimes N}) = 0$ and concentrates in $H^1(E_K^3, L_H^{\otimes N})$. In the jet exact sequence $0 \to \mathfrak{m}_0^a L_H \to L_H \to L_H/\mathfrak{m}_0^a L_H \to 0$,
   $$0 \to H^0(L_H/\mathfrak{m}_0^a L_H) \xrightarrow{\;\delta\;} H^1(E_K^3, \mathfrak{m}_0^a L_H) \to H^1(E_K^3, L_H) \to 0,$$
   the jet arrow runs *into* $H^1$ rather than *from* $H^0$ into jets (and Serre duality sends $H^1(L_H)^\vee \cong H^2(L_{-H})$), blocking Bost's slope inequality.
3. **Inevitability of Poles / Denominator Collapse for Meromorphic Quotients $s_+/s_-$:**
   - The $p$-adic divisibility summed over primes $p \le k$ inert in $K$ is $\frac{1}{2}\cdot\frac{2}{3} k\log k = \frac{1}{3} k\log k$.
   - For any fixed holomorphic sections $s_\pm \in H^0(E_K^3, L_{H_\pm}^{\otimes N})$, Wirtinger's theorem / equidistribution of the irrational Kronecker leaf $W_1 \subset E_K^3$ guarantees that $s_-(w)$ has $\sim N(v_1^* H_- v_1) R^2$ zeros in $|w| \le R$; hence $F = s_+/s_-$ has finite radius of convergence $R = O(N^{-1/2})$ and $|D_1^k F(0)| \sim k! R^{-k} \approx \exp(1\cdot k\log k)$, losing by $\frac{2}{3} k\log k$.
   - Attempting to eliminate intermediate Leibniz terms by choosing $s_- \in H^0(E_K^3, L_{H_-}^{\otimes N})$ ($N \asymp a^{1/3}$) satisfying $s_-(w) = s_-(0) + O(w^{a+1})$ forces $U_-(T(w)) \equiv s_-(0)\exp(-N\beta_{H_-}(w)) \pmod{w^{a+1}}$. Since $U_-(T)$ is $p$-adically integral in $T$ (and $T(w)$ is $p$-integral through degree $p^2-1$), comparing the $w^{p+1}$ coefficient forces $p \mid s_-(0)$ (and in fact $v_p(s_-(0)) \ge \frac{a}{p+1} - O(\log a)$) for **every** inert prime $p \le a - 1$, completely annihilating the $p$-adic gain (and $N \asymp a^{1/3}$ already inflates the order-2 Cauchy bound of $s_+$ from $\frac{1}{2}a\log a$ to $\frac{2}{3}a\log a$).

---

## 4. Independent Cross-Check & Unified Comparison with Astra's Round 2 Discovery

We independently implemented and verified GPT-6.2-Astra's construction (`wall1_astra_report.md`):
- For $E_0: y^2 = x^3 - 2$, $E_1: y^2 = x^3 - 8$, the formal homomorphism $h(z) = \ell_1^{-1}(\ell_0(z)) \in \mathbb{Q}[[z]]$ gives
  $$h(z) = z - \frac{3}{7} z^7 - \frac{3}{182} z^{13} - \frac{3435}{24206} z^{19} - \frac{91173}{677768} z^{25} - \frac{13037361}{61676888} z^{31} + \dots$$
  and exact prime-to-6 jet denominators $d_7 = 7$, $d_{11} = 7$, $d_{13} = 7\cdot 13$, $d_{14} = 7^2\cdot 13$, $d_{19} = 7^2\cdot 13\cdot 19$, $d_{25} = 7^3\cdot 13\cdot 19$, $d_{31} = 7^4\cdot 13^2\cdot 19$ (no factor of $11, 23, 29, 31$).
- Both Astra's Euler ratio $\zeta_{K_0}^{(6)}(s)/L_f(s) = P_C(s)^3/P_C(3s)$, the dyadic Mellin transform $(2^s-2)\zeta(s)H(s)/(3s)$, the signs, and the unconditional oscillation bounds $|r| > 0.0353 > 0.03$ and $> 0.1163 > 0.11$ check out rigorously.

**Unified Geometric Diagnosis of Wall 1:**

| Aspect | Astra's $h(z) = \ell_1^{-1}(\ell_0(z))$ on $(E_0, E_1)$ | Gemini's $G_H(w)$ on $(E_K^3, L_H)$ |
|---|---|---|
| Ambient geometry | Ordinary CM pair ($K_0 = \mathbb{Q}(\sqrt{-3})$) | Supersingular CM threefold ($K = \mathbb{Q}(i)$) + $M_{\sqrt[3]{2}}$ |
| Local $p$-adic extraction ($p \le N$) | Exact $v_p(N!/d_N) = v_p(N!)\mathbf{1}_{p \notin C}$ | Exact $\frac{1}{3}v_p(N(D_1^N G_H)) = \frac{2-b_f(p)}{3}\frac{N}{p} + O(\frac{N}{p^2})$ |
| Total $p$-adic log-divisibility | $\frac{2}{3} N \log N$ | $\frac{1}{3} N \log N$ |
| Archimedean upper bound on $N![z^N](\cdot)$ | $1 \cdot N \log N$ (finite radius $R_h$) | $1 \cdot N \log N$ (poles on $Z(\theta_{H_-})$) |
| **Exact remaining Wall 1 gap** | Need global object of **order $\le 3$** ($\log|a_N| \le -\frac{1}{3}N\log N$) carrying denominator $d_N$ | Need global $H^0$ / positive-metric realization replacing $H^1(E_K^3, L_H)$ |

Both independent paths converge on the **exact same conclusion**: Wall 1 is **no longer** a local $p$-adic obstruction — $b_{f_{\chi_3}}(p)$ can be cleanly extracted at full linear scale $N/p$ inside ordinary or supersingular CM elliptic curves without violating Albert/Weil. What remains genuinely open is the **global Archimedean–cohomological realization** that upgrades a finite-radius formal map ($h$) or an $H^1$ indefinite theta quotient ($G_H$) into an entire / positive-metric Bost inequality beating the $1\cdot N\log N$ trivial radius bound.
