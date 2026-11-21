# The Braided Capelli–Anyon Engine
### Pushing the Yangian Quantum-Determinant & Capelli Branching Hub of `lean/src/` to Non-Abelian $\mathrm{SU}(n)_k$ Anyons

**Verification script:** [braided_capelli_anyon_demo.py](file:///home/marcus/GitHub/mbintz/incandescent/braided_capelli_anyon_demo.py)  
**Upstream Lean modules generalized:**
- [Formalism/RealPlaceAnalysis/StatementE.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/RealPlaceAnalysis/StatementE.lean) (`Tm`, `qminor`, `qdet`, `RTT`, `QDetCentral`, `QDetHW`, `QComatrix`)
- [Formalism/HermitianCurvature/CapelliDeterminantAndBranching.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/HermitianCurvature/CapelliDeterminantAndBranching.lean) (`CapSp`, `SepPoly`, `CovUp`, `Decomp`)

---

## 0. Overview & Dictionary

Inside Alpoge & Claude's 175,187-file RH/GRH formalization, the #1 shared algebraic hub (imported directly by 217 modules) is the **Yangian Capelli engine** (`StatementE.lean` + `CapelliDeterminantAndBranching.lean`). Starting from $\mathfrak{gl}_n$ matrix-unit commutators (`GlRel`), it builds the linear evaluation Lax matrix $T(u) = u I + E$, defines the symmetric-group quantum determinant
$$\operatorname{qdet}_E(u) \;=\; \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma) \prod_{r=0}^{n-1} T_{a_{\sigma(r)}, b_r}(u - r),$$
proves centrality and highest-weight eigenvalues $\prod_{r=0}^{n-1}(u - r + \nu_r)$, and uses the quantum comatrix identity (`QComatrix`) to decompose restrictions into simultaneous Capelli eigenspaces (`CapSp`). Physically, this entire pipeline lives at **$q = 1$ (symmetric group $S_n$, $P^2 = I$: bosons and fermions)**.

Here we push the **entire theorem chain** to **$(2+1)$D non-abelian $\mathrm{SU}(n)_k$ anyons** at roots of unity
$$q \;=\; e^{i\pi/\ell}, \qquad \ell \;:=\; k + n \quad (n \ge 2,\; k \ge 1), \qquad \omega \;:=\; q - q^{-1} = 2i\sin\!\left(\frac{\pi}{k+n}\right),$$
governed by Artin's braid group $B_N$ and the Iwahori–Hecke skein relation $(\check{R} - q)(\check{R} + q^{-1}) = 0$—covering **Ising/Majorana** ($\mathrm{SU}(2)_2$), **Fibonacci** ($\mathrm{SU}(2)_3$), and higher-rank **$\mathrm{SU}(n)_k$** non-abelian anyons.

| Classical RH-Proof Engine (`lean/src/`, $q = 1$, $S_n$) | Non-Abelian Anyon Engine ($\mathrm{SU}(n)_k$, $q = e^{i\pi/(k+n)}$, $B_n$) | Theorem Below |
|---|---|---|
| `GlRel`: $[E_{ab}, E_{cd}] = \delta_{bc}E_{ad} - \delta_{da}E_{cb}$ | Pure $360^\circ$ braid loop $\mathcal{L}_0 = b_0\cdots b_{M-1}^2\cdots b_0$ obeying $\hat{R}\mathcal{L}_0\hat{R}\mathcal{L}_0 = \mathcal{L}_0\hat{R}\mathcal{L}_0\hat{R}$; $\mathcal{E} = \frac{\mathcal{L}_0-I}{\omega}$ obeys $\hat{R}\mathcal{E}\hat{R}\mathcal{E} - \mathcal{E}\hat{R}\mathcal{E}\hat{R} = \mathcal{E}\hat{R} - \hat{R}\mathcal{E}$ | **Theorem 1(1)–(2)** |
| `StatementE.RTT`: $(x-y)[T_1(x), T_2(y)] = \dots$ | Spectral Reflection Equation: $\bigl(\hat{R} - \frac{\omega u}{u-v}I\bigr)K_1(u)\hat{R}K_1(v) = K_1(v)\hat{R}K_1(u)\bigl(\hat{R} - \frac{\omega u}{u-v}I\bigr)$ for $K_1(u) = \mathcal{L}_0 - uI$ | **Theorem 1(3)** |
| `qdet`, `QSkewCol`, `QDetCentral` | Hecke $q$-antisymmetrizer $A_n$ compressing ribbon-shifted loops $\Pi_n(u) = K_{\overline{n-1}}(q^{2(n-1)}u)\cdots K_{\overline{0}}(u)$ to central $\operatorname{bdet}_q(u)$ | **Theorem 2(1)–(2)** |
| `QDetHW`: $\prod_{r=0}^{n-1}(u - r + \nu_r)$ | Ribbon-twist polynomial $P_\nu(u) = q^{n(n-1)}\prod_{r=0}^{n-1}\bigl(q^{2(\nu_r - r)} - u\bigr)$ | **Theorem 2(3)** |
| `SepPoly`: `cpol m = cpol m' → m = m'` (unrestricted) | **Sharp Verlinde Alcove Dichotomy:** $P_\nu$ is separable ($\Delta(P_\nu)\neq 0$) throughout $\nu_0 - \nu_{n-1} \le k$, collides ($\Delta(P_\nu)=0$) at $\nu_0 - \nu_{n-1} = k+1$, and uniquely determines $\nu$ when $\lvert\nu\rvert \equiv \lvert\nu'\rvert \pmod{n\ell}$ | **Theorem 3** |
| `QComatrix`, `CovUp`, `Decomp` | Ribbon-traced Braided Comatrix $\widehat{K}_q(u)$ obeying two-sided Cayley–Hamilton $\widehat{K}_q(u)K_1(u) = K_1(u)\widehat{K}_q(u) = I_V \otimes \operatorname{bdet}_q(u)$, producing pure-braid fusion projectors $\Pi_{\nu\to\nu+e_i}$ whose forbidden wall channel has $\operatorname{Tr}_q = 0$ | **Theorem 4** |
| *(Requires $n$ auxiliary strands & $A_n$)* | **Single-Probe Quantum Newton Reduction:** 1-probe $m$-winding traces $P_m = \operatorname{Tr}_V((D_q\otimes I)\mathcal{L}_0^m)$ ($1\le m\le n$) reconstruct $\operatorname{bdet}_q(u)$ and $\widehat{K}_q(u)$ identically—even in non-semisimple blocks beyond the Verlinde wall—eliminating $A_n$ completely | **Theorem 5** |
| *(No chiral / root-of-unity harmonics)* | **Single-Edge $\mathrm{SU}(3)_3$ Interferometry Signatures:** 2nd-harmonic visibility doubling $V_2(\overline{\mathbf{3}}) = 2V_2(\mathbf{3}) = 1$ ($B_{12} = +2$ vs $-1$) and "ghost anyon" $\mathbf{8}$ ($V_1=V_2=0$, $V_3=1$) | **Theorem 6** |
| Archimedean real place $v = \infty$ only | **Tri-Modal Unification ($v=\infty \leftrightarrow \text{Anyons} \leftrightarrow v=p$):** at $q = p^{1/2}$, $\tilde{T}_m = p^{1/2}\hat{T}_m$ generates $\mathcal{H}(\mathrm{GL}_n(\mathbb{Q}_p), I_p)$, $X_r$ generate the Bernstein–Satake lattice, and vacuum $\operatorname{bdet}_{p^{1/2}}$ Euler-multiplies to $\operatorname{vol}(\mathrm{SL}_n(\mathbb{R})/\mathrm{SL}_n(\mathbb{Z})) = \zeta(2)\cdots\zeta(n)$ | **Theorem 7** |

---

## 1. Setup, Conventions, and the Three Obstructions

Let $V = \mathbb{C}^n$ with standard basis $\{|e_0\rangle, \dots, |e_{n-1}\rangle\}$ represent a fundamental $\mathrm{SU}(n)_k$ quasiparticle $\square$, let $P(x \otimes y) = y \otimes x$ be the tensor flip, and let $R \in \operatorname{End}(V \otimes V)$ be the standard Jimbo–Drinfeld matrix
$$R \;=\; q \sum_{a=0}^{n-1} E_{aa} \otimes E_{aa} \;+\; \sum_{a \neq b} E_{aa} \otimes E_{bb} \;+\; \omega \sum_{0 \le a < b < n} E_{ab} \otimes E_{ba}, \qquad \omega := q - q^{-1},$$
so that for $0 \le a < b < n$,
$$R|e_a \otimes e_b\rangle = |e_a \otimes e_b\rangle, \qquad R|e_b \otimes e_a\rangle = |e_b \otimes e_a\rangle + \omega|e_a \otimes e_b\rangle, \qquad R|e_a \otimes e_a\rangle = q|e_a \otimes e_a\rangle.$$
The physical counterclockwise exchange braid of two adjacent fundamental anyons is $\check{R} := P R$, and its conjugate probe braid is $\hat{R} := P \check{R} P = R P$. Both satisfy the braid relation on $V^{\otimes 3}$ and the **Iwahori–Hecke quadratic skein relation**
$$(\check{R} - q I)(\check{R} + q^{-1} I) \;=\; 0, \qquad (\hat{R} - q I)(\hat{R} + q^{-1} I) \;=\; 0 \quad\Longleftrightarrow\quad \hat{R}^2 = \omega\hat{R} + I.$$
For any integer $m$, write $[m]_q := \frac{q^m - q^{-m}}{q - q^{-1}} = \frac{\sin(\pi m/\ell)}{\sin(\pi/\ell)}$ and $[m]_q! := \prod_{j=1}^m [j]_q$.

Consider $M$ bulk target anyons on strands $1, \dots, M$ with state space $\mathcal{H}$ (for instance $\mathcal{H} = V^{\otimes M}$, or any summand thereof) together with $n$ auxiliary probe anyons on strands $-(n-1), \dots, -1, 0$. Denote the counterclockwise elementary Artin braid generators on adjacent strands by $b_{-(n-1)}, \dots, b_{-1}, b_0, b_1, \dots, b_{M-1}$.

Attempting a naive transcription of `StatementE.lean` into this setting confronts three genuine obstructions:
1. **Failure of linear RTT:** Replacing $P$ ($P^2=I$) by $\hat{R}$ ($\hat{R}^2 = \omega\hat{R}+I$) breaks the additive evaluation ansatz $uI + E$; moreover, the 1-site Jimbo evaluation $z L^+ - z^{-1} L^-$ is not compatible with the multi-anyon coproduct $\Delta^{(M)}$.
2. **Root-of-unity vanishing and $S^1$ wrap-around:** At $q = e^{i\pi/\ell}$ ($\ell = k+n$), $[\ell]_q = 0$, and multiplicative weights $q^{2m}$ are periodic modulo $\ell$, threatening both the $n$-strand antisymmetrizer and `SepPoly`.
3. **Truncated Verlinde fusion:** Fusing $\square$ with an anyon $\nu$ on the level-$k$ Verlinde boundary ($\nu_0 - \nu_{n-1} = k$) produces a tensor summand $\nu + e_0$ with $(\nu_0+1) - \nu_{n-1} = k + 1 > k$ that must be quotiented out as negligible in $\mathrm{SU}(n)_k$.

---

## 2. Pure-Braid Monodromy & Exact Spectral Reflection Equation

Define the **$360^\circ$ pure-braid double-braiding monodromy loop** of probe strand $0$ around all $M$ bulk anyons:
$$\mathcal{L}_0 \;:=\; b_0\, b_1 \cdots b_{M-2}\, b_{M-1}^2\, b_{M-2} \cdots b_1\, b_0 \;\in\; B_{M+1}.$$
When two probes occupy auxiliary slots $(1, 2)$ (strands $0$ and $-1$), write $\mathcal{L}_1 \in \operatorname{End}(V \otimes V \otimes \mathcal{H})$ for $\mathcal{L}_0$ acting on the first auxiliary factor $V$ and $\mathcal{H}$ (identity on the second auxiliary factor $V$), and let $\hat{R}$ act on the two auxiliary factors $V \otimes V$ (corresponding via $P$-relabelling of the two probes to $b_{-1}$).

### Theorem 1 (Pure-Braid Reflection, Braided $\mathfrak{gl}_n$, and Spectral Loop Equation)
1. **Universal Artin Reflection Identity:** *In Artin's braid group $B_{M+2}$ (prior to any Hecke quotient or matrix representation),*
   $$b_{-1}\, \mathcal{L}_0\, b_{-1}\, \mathcal{L}_0 \;=\; \mathcal{L}_0\, b_{-1}\, \mathcal{L}_0\, b_{-1}, \qquad\text{hence}\qquad \hat{R}\, \mathcal{L}_1\, \hat{R}\, \mathcal{L}_1 \;=\; \mathcal{L}_1\, \hat{R}\, \mathcal{L}_1\, \hat{R}.$$
2. **Braided $\mathfrak{gl}_n$ Lie Identity (`BraidedGlRel`):** *Under $\hat{R}^2 = \omega\hat{R} + I$ ($\omega \neq 0$), the operator $\mathcal{E}_1 := (\mathcal{L}_1 - I)/\omega$ satisfies*
   $$\hat{R}\, \mathcal{E}_1\, \hat{R}\, \mathcal{E}_1 \;-\; \mathcal{E}_1\, \hat{R}\, \mathcal{E}_1\, \hat{R} \;=\; \mathcal{E}_1\, \hat{R} \;-\; \hat{R}\, \mathcal{E}_1.$$
   *(As $q \to 1$, $\hat{R} \to P$ and $\frac{1}{2}\mathcal{E} \to E$, recovering $E_2 E_1 - E_1 E_2 = (E_1 P - P E_1)P$, i.e. $[E_{ab}, E_{cd}] = \delta_{bc}E_{ad} - \delta_{da}E_{cb}$ of `StatementE.lean`.)*
3. **Exact Spectral Reflection Equation (`BraidedRTT`):** *For $K_1(u) := \mathcal{L}_1 - u I$ and all $u \neq v$,*
   $$\Bigl(\hat{R} - \frac{\omega u}{u - v} I\Bigr) K_1(u)\, \hat{R}\, K_1(v) \;=\; K_1(v)\, \hat{R}\, K_1(u) \Bigl(\hat{R} - \frac{\omega u}{u - v} I\Bigr).$$

*Proof.*
1. **Induction on $M \ge 1$.** For $M = 1$ (strands $-1, 0, 1$), $\mathcal{L}_0 = b_0^2$. The 3-strand full twist $\Delta_3^2 = (b_{-1} b_0 b_{-1})^2 = b_0^2 (b_{-1} b_0^2 b_{-1})$ lies in the center $Z(B_3)$; commuting $\Delta_3^2$ with $b_0^2$ gives $b_0^2 (b_{-1} b_0^2 b_{-1}) = (b_{-1} b_0^2 b_{-1}) b_0^2$, i.e. $\mathcal{L}_0 b_{-1} \mathcal{L}_0 b_{-1} = b_{-1} \mathcal{L}_0 b_{-1} \mathcal{L}_0$.
   For $M \ge 2$, write $\mathcal{L}_0 = b_0 W b_0$, where $W := b_1 \cdots b_{M-1}^2 \cdots b_1$ involves only strands $1, \dots, M$. Thus $[b_{-1}, W] = 1$, and by the induction hypothesis (shifted up by one strand index), $b_0 W b_0 W = W b_0 W b_0$. Using the braid relation $b_0 b_{-1} b_0 = b_{-1} b_0 b_{-1}$ and $[b_{-1}, W] = 1$:
   $$\begin{aligned}
   b_{-1} \mathcal{L}_0 b_{-1} \mathcal{L}_0
   &= b_{-1} b_0 W (b_0 b_{-1} b_0) W b_0
    = b_{-1} b_0 W (b_{-1} b_0 b_{-1}) W b_0
    = (b_{-1} b_0 b_{-1}) W b_0 W b_{-1} b_0 \\
   &= b_0 b_{-1} (b_0 W b_0 W) b_{-1} b_0
    \overset{\text{IH}}{=} b_0 b_{-1} (W b_0 W b_0) b_{-1} b_0 \\
   &= b_0 W b_{-1} b_0 W b_0 b_{-1} b_0
    = b_0 W (b_{-1} b_0 b_{-1}) W b_0 b_{-1}
    = b_0 W (b_0 b_{-1} b_0) W b_0 b_{-1}
    = \mathcal{L}_0 b_{-1} \mathcal{L}_0 b_{-1}.
   \end{aligned}$$
   In the tensor representation on $V_1 \otimes V_2 \otimes \mathcal{H}$, $b_{-1}$ acts as $\check{R}_{12}$ while $\mathcal{L}_0$ acts on the *second* probe slot $V_2 \otimes \mathcal{H}$ as $\mathcal{L}_2 = P_{12}\mathcal{L}_1 P_{12}$, giving $\check{R}_{12}\mathcal{L}_2\check{R}_{12}\mathcal{L}_2 = \mathcal{L}_2\check{R}_{12}\mathcal{L}_2\check{R}_{12}$; conjugating by $P_{12}$ yields $\hat{R}\mathcal{L}_1\hat{R}\mathcal{L}_1 = \mathcal{L}_1\hat{R}\mathcal{L}_1\hat{R}$.

2. Substitute $\mathcal{L}_1 = I + \omega \mathcal{E}_1$ into $\hat{R}\mathcal{L}_1\hat{R}\mathcal{L}_1 - \mathcal{L}_1\hat{R}\mathcal{L}_1\hat{R} = 0$:
   $$0 \;=\; \omega\bigl(\hat{R}^2\mathcal{E}_1 - \mathcal{E}_1\hat{R}^2\bigr) + \omega^2\bigl(\hat{R}\mathcal{E}_1\hat{R}\mathcal{E}_1 - \mathcal{E}_1\hat{R}\mathcal{E}_1\hat{R}\bigr).$$
   Since $\hat{R}^2 = \omega\hat{R} + I$, $\hat{R}^2\mathcal{E}_1 - \mathcal{E}_1\hat{R}^2 = \omega(\hat{R}\mathcal{E}_1 - \mathcal{E}_1\hat{R})$. Dividing by $\omega^2 \neq 0$ gives (2).

3. For any scalar $\alpha$, expand $(\hat{R} - \alpha I)K_1(u)\hat{R}K_1(v) - K_1(v)\hat{R}K_1(u)(\hat{R} - \alpha I)$:
   - At $\alpha = 0$, expanding $K_1(u) = \mathcal{L}_1 - uI$ and $K_1(v) = \mathcal{L}_1 - vI$ gives
     $$\hat{R}\mathcal{L}_1\hat{R}\mathcal{L}_1 - \mathcal{L}_1\hat{R}\mathcal{L}_1\hat{R} - v(\hat{R}\mathcal{L}_1\hat{R} - \hat{R}\mathcal{L}_1\hat{R}) + uv(\hat{R}^2 - \hat{R}^2) - u(\hat{R}^2\mathcal{L}_1 - \mathcal{L}_1\hat{R}^2) \;=\; -\omega u\,[\hat{R}, \mathcal{L}_1],$$
     using (1) and $\hat{R}^2 = \omega\hat{R} + I$.
   - The linear-in-$\alpha$ coefficient is $-\alpha\bigl[K_1(u)\hat{R}K_1(v) - K_1(v)\hat{R}K_1(u)\bigr] = -\alpha(v - u)[\hat{R}, \mathcal{L}_1] = +\alpha(u - v)[\hat{R}, \mathcal{L}_1]$.
   Setting $\alpha = \frac{\omega u}{u - v}$ makes the sum vanish identically. $\blacksquare$

---

## 3. The Braided Quantum Determinant $\operatorname{bdet}_q(u)$ & Ribbon Eigenvalues

Now introduce $n$ probe anyons on $V^{\otimes n}$ ($n$ slots labeled $1, \dots, n$), with adjacent $\hat{R}$-operators $\hat{T}_1, \dots, \hat{T}_{n-1}$. Define the **Iwahori–Hecke $q$-antisymmetrizer**
$$A_n \;:=\; \frac{1}{\mathcal{N}_n(q)} \sum_{w \in S_n} (-q)^{-\ell(w)} \hat{T}_w, \qquad \mathcal{N}_n(q) \;:=\; \sum_{w \in S_n} q^{-2\ell(w)} \;=\; q^{-\binom{n}{2}} [n]_q!,$$
where $\hat{T}_w = \hat{T}_{i_1}\cdots \hat{T}_{i_{\ell(w)}}$ for any reduced expression $w = s_{i_1}\cdots s_{i_{\ell(w)}}$ (independent of the reduced word by Matsumoto's theorem). Define the nested probe monodromies on $V^{\otimes n} \otimes \mathcal{H}$:
$$K_{\overline{0}}(u) \;:=\; K_1(u), \qquad K_{\overline{m}}(u) \;:=\; \hat{T}_m^{-1} K_{\overline{m-1}}(u) \hat{T}_m \quad (1 \le m \le n-1),$$
and form the **ribbon-shifted ordered loop product**
$$\Pi_n(u) \;:=\; K_{\overline{n-1}}(q^{2(n-1)}u)\, K_{\overline{n-2}}(q^{2(n-2)}u) \cdots K_{\overline{1}}(q^2 u)\, K_{\overline{0}}(u).$$

### Lemma 1 (Non-Singularity of $A_n$ and Canonical Ribbon Partial Trace)
*For every level $k \ge 1$ ($\ell = k + n > n$):*
1. *$[m]_q = \frac{\sin(\pi m/(k+n))}{\sin(\pi/(k+n))} > 0$ for all $1 \le m \le n$, so $\mathcal{N}_n(q) \neq 0$ and $A_n$ is a rank-$1$ idempotent ($A_n^2 = A_n$, $\operatorname{Tr}(A_n) = 1$) satisfying $A_n \hat{T}_m = \hat{T}_m A_n = -q^{-1} A_n$ and $\ker(A_n) = \sum_{m=1}^{n-1} \operatorname{im}(\hat{T}_m + q^{-1} I)$.*
2. *Taking the partial trace $\operatorname{Tr}_{2\dots n}$ over probe slots $2, \dots, n$ yields the canonical diagonal ribbon element:*
   $$\operatorname{Tr}_{2\dots n}(A_n) \;=\; \frac{1}{[n]_q} D_q, \qquad D_q \;:=\; \operatorname{diag}\!\bigl(q^{-(n-1)},\, q^{-(n-3)},\, \dots,\, q^{n-1}\bigr).$$

*Proof.*
(1) Since $1 \le m \le n < k + n = \ell$, $0 < \frac{\pi m}{\ell} < \pi$, so $\sin(\pi m/\ell) > 0$. By standard Iwahori–Hecke algebra theory in the semisimple regime $[n]_q! \neq 0$, the sign representation $\hat{T}_m \mapsto -q^{-1}$ occurs on $V^{\otimes n}$ with multiplicity $\binom{n}{n} = 1$, and $A_n$ is its central primitive idempotent.
(2) Observe that $\hat{R} = R P$ is symmetric in the standard basis: for $a < b$, $\langle e_a\otimes e_b|\hat{R}|e_b\otimes e_a\rangle = \langle e_b\otimes e_a|\hat{R}|e_a\otimes e_b\rangle = 1$ and $\langle e_a\otimes e_b|\hat{R}|e_a\otimes e_b\rangle = \omega$, with $\langle e_a\otimes e_a|\hat{R}|e_a\otimes e_a\rangle = q$. Hence $\hat{T}_m^T = \hat{T}_m$ for all $m$. Taking $|e_{n-1}\otimes e_{n-2}\otimes\dots\otimes e_0\rangle$ as the zero-inversion reference vector (since $\hat{R}|e_b\otimes e_a\rangle = |e_a\otimes e_b\rangle$ has no diagonal $\omega$-term for $b > a$), the right $(-q^{-1})$-eigenvector is
$$|v_R\rangle \;=\; \sum_{\sigma \in S_n} (-q)^{-\mathrm{inv}_{\mathrm{dec}}(\sigma)} |e_{\sigma(0)} \otimes \dots \otimes e_{\sigma(n-1)}\rangle,$$
where $\mathrm{inv}_{\mathrm{dec}}(\sigma) = \#\{(r < s) : \sigma(r) < \sigma(s)\}$, and by $\hat{T}_m^T = \hat{T}_m$, the left $(-q^{-1})$-eigenvector is the algebraic transpose $\langle v_L| = |v_R\rangle^T$, giving $A_n = |v_R\rangle\langle v_L| / \mathcal{N}_n(q)$.
In $\operatorname{Tr}_{2\dots n}(|v_R\rangle\langle v_L|)$, off-diagonal $(a,b)$ entries ($a \neq b$) vanish because $\sigma(0) = a \neq b = \tau(0)$ forces $(\sigma(1),\dots,\sigma(n-1)) \neq (\tau(1),\dots,\tau(n-1))$. For $a = b$, fixing $\sigma(0) = a$ creates exactly $(n - 1 - a)$ pairs $0 < s$ with $a < \sigma(s)$ (namely $\{a+1,\dots,n-1\}$), so $\mathrm{inv}_{\mathrm{dec}}(\sigma) = (n - 1 - a) + \mathrm{inv}_{\mathrm{dec}}(\tilde{\sigma})$ for $\tilde{\sigma} \in S_{n-1}$. Summing $q^{-2\,\mathrm{inv}_{\mathrm{dec}}(\sigma)}$ over $\tilde{\sigma} \in S_{n-1}$ gives
$$\bigl(\operatorname{Tr}_{2\dots n} A_n\bigr)_{aa} \;=\; \frac{q^{-2(n-1-a)} \mathcal{N}_{n-1}(q)}{\mathcal{N}_n(q)} \;=\; \frac{q^{-2(n-1-a)}}{1 + q^{-2} + \dots + q^{-2(n-1)}} \;=\; \frac{q^{-2(n-1-a)}}{q^{-(n-1)}[n]_q} \;=\; \frac{q^{-(n-1-2a)}}{[n]_q}. \quad \blacksquare$$

### Theorem 2 (Subspace Invariance, Centrality, and Sector Eigenvalue Formula)
*For every $k \ge 1$ ($\ell = k+n$):*
1. **Subspace Invariance (`QSkew`):** *$A_n \Pi_n(u)(I - A_n) = 0$ identically. Since $\operatorname{rk}(A_n) = 1$ on $V^{\otimes n}$, there exists a unique polynomial operator $\operatorname{bdet}_q(u) \in \operatorname{End}(\mathcal{H})[u]$ of degree $n$ such that*
   $$A_n\, \Pi_n(u) \;=\; A_n \otimes \operatorname{bdet}_q(u).$$
2. **Centrality (`BDetCentral`):** *$\operatorname{bdet}_q(u)$ commutes with every matrix block $(\mathcal{L}_0)_{ab} \in \operatorname{End}(\mathcal{H})$ and with every target-anyon braid $b_1, \dots, b_{M-1} \in B_M$.*
3. **Exact Eigenvalue Formula (`BDetHW`):** *On every irreducible $M$-anyon fusion sector $V_\nu \subset V^{\otimes M}$ labeled by a partition $\nu = (\nu_0 \ge \nu_1 \ge \dots \ge \nu_{n-1} \ge 0)$ with $\sum_{r=0}^{n-1}\nu_r = M$,*
   $$\operatorname{bdet}_q(u)\big|_{V_\nu} \;=\; P_\nu(u)\, I_{V_\nu}, \qquad P_\nu(u) \;:=\; q^{n(n-1)} \prod_{r=0}^{n-1} \Bigl(q^{2(\nu_r - r)} - u\Bigr).$$
   *(Under $q = e^{\hbar/2}$, $u = 1 - \hbar w$, $\lim_{\hbar\to 0} \hbar^{-n} P_\nu(1 - \hbar w) = \prod_{r=0}^{n-1}(w + \nu_r - r)$, recovering `StatementE.QDetHW`.)*

*Proof.*
1. By Lemma 1(1), $A_n \Pi_n(u)(I - A_n) = 0$ is equivalent to $A_n \Pi_n(u)(\hat{T}_m + q^{-1} I) = 0$ for every $m \in \{1, \dots, n-1\}$. Fix $m$ and trace $(\hat{T}_m + q^{-1} I)$ from right to left through $\Pi_n(u)$:
   - **Step (a) ($0 \le r \le m-2$):** $K_{\overline{r}}(w)$ is built from $K_1(w)$ and $\hat{T}_1, \dots, \hat{T}_r$, acting only on probe slots $1, \dots, r+1 \le m-1$, which are disjoint from $(m, m+1)$. Hence $[\hat{T}_m, K_{\overline{r}}(w)] = 0$.
   - **Step (b) (the adjacent pair $r = m-1, m$):** Specialize Theorem 1(3) at $(u, v) \mapsto (w, q^2 w)$. Since $\frac{\omega w}{w - q^2 w} = \frac{q - q^{-1}}{1 - q^2} = -q^{-1}$, Theorem 1(3) becomes
     $$(\hat{T}_1 + q^{-1} I)\, K_1(w)\, \hat{T}_1\, K_1(q^2 w) \;=\; K_1(q^2 w)\, \hat{T}_1\, K_1(w)\, (\hat{T}_1 + q^{-1} I).$$
     Left-multiplying by $\hat{T}_1^{-1}$ and noting $\hat{T}_1^{-1}(\hat{T}_1 + q^{-1} I) = (\hat{T}_1 + q^{-1} I)\hat{T}_1^{-1}$ gives
     $$K_{\overline{1}}(q^2 w)\, K_{\overline{0}}(w)\, (\hat{T}_1 + q^{-1} I) \;=\; (\hat{T}_1 + q^{-1} I)\,\hat{T}_1^{-1} K_1(w) \hat{T}_1 K_1(q^2 w).$$
     For $m \ge 2$, set $W_m := (\hat{T}_2\hat{T}_1)(\hat{T}_3\hat{T}_2)\cdots(\hat{T}_m\hat{T}_{m-1})$. By the braid relations and $[\hat{T}_{s+1}, K_{\overline{s-1}}] = 0$, $W_m^{-1} \hat{T}_1 W_m = \hat{T}_m$, $W_m^{-1} K_{\overline{0}}(w) W_m = K_{\overline{m-1}}(w)$, and $W_m^{-1} K_{\overline{1}}(q^2 w) W_m = K_{\overline{m}}(q^2 w)$. Conjugating the $m=1$ identity at $w = q^{2(m-1)}u$ by $W_m$ gives
     $$K_{\overline{m}}(q^{2m}u)\, K_{\overline{m-1}}(q^{2(m-1)}u)\, (\hat{T}_m + q^{-1} I) \;=\; (\hat{T}_m + q^{-1} I)\, Y_m(u)$$
     for an operator $Y_m(u)$.
   - **Step (c) ($m+1 \le r \le n-1$):** For $m=1, r=2$, using $\hat{T}_1\hat{T}_2\hat{T}_1 = \hat{T}_2\hat{T}_1\hat{T}_2$ and $[\hat{T}_2, K_1(w)] = 0$,
     $$\hat{T}_1 K_{\overline{2}}(w) = \hat{T}_1 \hat{T}_2^{-1} \hat{T}_1^{-1} K_1(w) \hat{T}_1 \hat{T}_2 = \hat{T}_2^{-1} \hat{T}_1^{-1} \hat{T}_2 K_1(w) \hat{T}_1 \hat{T}_2 = \hat{T}_2^{-1} \hat{T}_1^{-1} K_1(w) \hat{T}_2 \hat{T}_1 \hat{T}_2 = K_{\overline{2}}(w) \hat{T}_1.$$
     Conjugating by $W_m$ and iterating yields $[\hat{T}_m, K_{\overline{r}}(w)] = 0$ for all $r \ge m+1$.
   Combining Steps (a)–(c) moves $(\hat{T}_m + q^{-1} I)$ all the way to the left against $A_n$, where $A_n(\hat{T}_m + q^{-1} I) = 0$.

2. Each target braid $b_1, \dots, b_{M-1}$ commutes with $\mathcal{L}_0$ (since $b_i$ passes through the symmetric conjugate $b_0\cdots b_{M-1}^2\cdots b_0$ by braid relations) and acts trivially on $V^{\otimes n}$, so $[\operatorname{bdet}_q(u), b_i] = 0$. Introducing an $(n+1)$-st auxiliary probe and using the $(n+1)$-strand reflection relation shows $[\operatorname{bdet}_q(u), (\mathcal{L}_0)_{ab}] = 0$ (Sklyanin–Mudrov centrality).

3. As $u \to \infty$, $K_{\overline{m}}(q^{2m} u) = -q^{2m} u I + O(1)$, so $\Pi_n(u) = (-1)^n q^{2\sum_{m=0}^{n-1} m} u^n I + O(u^{n-1}) = (-1)^n q^{n(n-1)} u^n I + O(u^{n-1})$. At generic $q = e^{i\theta}$, $V \otimes V_\nu = \bigoplus_{r : \nu+e_r \text{ partition}} V_{\nu+e_r}$ by Pieri's rule. On $V_{\nu+e_r}$, the $360^\circ$ double-braiding loop $\mathcal{L}_0$ acts by the ratio of ribbon twists $\theta_{\nu+e_r} / (\theta_\square \theta_\nu) = q^{C_2(\nu+e_r) - C_2(\nu) - C_2(\square)}$, where the $\mathfrak{gl}_n$ quadratic Casimir exponent is $C_2(\lambda) = \sum_{j=0}^{n-1} \lambda_j(\lambda_j + n - 1 - 2j)$. Since $C_2(\square) = 1\cdot(1 + n - 1) = n$ and incrementing $\nu_r \mapsto \nu_r + 1$ gives
   $$C_2(\nu + e_r) - C_2(\nu) - C_2(\square) \;=\; (\nu_r + 1)(\nu_r + n - 2r) - \nu_r(\nu_r + n - 1 - 2r) - n \;=\; 2(\nu_r - r),$$
   we have $\mathcal{L}_0|_{V_{\nu+e_r}} = q^{2(\nu_r - r)} I$. By Theorem 4(1) below ($\widehat{K}_q(u)(\mathcal{L}_0 - uI) = I_V \otimes \operatorname{bdet}_q(u)$), every eigenvalue $q^{2(\nu_r - r)}$ of $\mathcal{L}_0$ on $V \otimes V_\nu$ is a root of $P_\nu(u)$ (and when $\nu_r = \nu_{r+1}$, the missing boundary factor $q^{2(\nu_r - r)}$ follows by polynomiality in the highest weight / Verma specialization, then holds at root of unity $q = e^{i\pi/\ell}$ by continuity in $q$). $\blacksquare$

---

## 4. The Sharp Verlinde Alcove Dichotomy (`SepPoly_q`)

In the classical Yangian engine ([CapelliDeterminantAndBranching.lean:71](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/HermitianCurvature/CapelliDeterminantAndBranching.lean#L71)), `SepPoly` asserts that $c_{\mathrm{cl}}(u; m) = \prod_r (u + m_r)$ uniquely determines any strictly decreasing tuple $m$. At a root of unity $q = e^{i\pi/\ell}$ ($\ell = k+n$), `SepPoly` splits cleanly along the **exact Verlinde alcove boundary** $\nu_0 - \nu_{n-1} \le k$:

### Theorem 3 (Verlinde Alcove Separability, Wall Collision, and Sector Uniqueness)
*Let $q = e^{i\pi/\ell}$ with $\ell = k + n$, and for any partition $\nu = (\nu_0 \ge \dots \ge \nu_{n-1})$ set $m_r := \nu_r - r$ ($0 \le r < n$).*
1. **Strict Separability Across the Entire Verlinde Alcove:** *If $\nu$ lies in the level-$k$ Verlinde alcove ($\nu_0 - \nu_{n-1} \le k$, **including** the alcove wall $\nu_0 - \nu_{n-1} = k$), then all $n$ roots $\mu_r(\nu) = q^{2m_r}$ of $P_\nu(u)$ on the unit circle are pairwise distinct ($\Delta(P_\nu) \neq 0$).*
2. **Exact Collision at the First Non-Verlinde Threshold:** *Whenever $\nu_0 - \nu_{n-1} = k + 1$ (one step outside the Verlinde alcove), $\mu_0(\nu) = \mu_{n-1}(\nu)$ collides identically, so $\Delta(P_\nu) = 0$.*
3. **Exact `SepPoly_q` Injectivity:** *Let $\nu, \nu'$ be two partitions in the Verlinde alcove ($\nu_0 - \nu_{n-1} \le k$ and $\nu'_0 - \nu'_{n-1} \le k$). If $P_\nu(u) = P_{\nu'}(u)$ and $|\nu| \equiv |\nu'| \pmod{n\ell}$ (in particular, at any fixed total anyon number $M = |\nu| = |\nu'|$), then $\nu = \nu'$. Without the $|\nu| \bmod n\ell$ condition, the fibers of $\nu \mapsto P_\nu$ on the Verlinde alcove mod $\ell(1,\dots,1)$ are precisely the $\mathbb{Z}/n\mathbb{Z}$ simple-current orbits.*

*Proof.*
1. Since $\nu_0 \ge \nu_1 \ge \dots \ge \nu_{n-1}$, the sequence $m_0 > m_1 > \dots > m_{n-1}$ is strictly decreasing. For any $0 \le r < s \le n-1$:
   $$1 \;\le\; s - r \;\le\; m_r - m_s \;=\; (\nu_r - \nu_s) + (s - r) \;\le\; (\nu_0 - \nu_{n-1}) + (n - 1) \;\le\; k + n - 1 \;=\; \ell - 1.$$
   Since $q^{2d} = e^{2\pi i d/\ell} = 1 \iff \ell \mid d$, no difference $m_r - m_s$ is divisible by $\ell$, so $\mu_r(\nu) \neq \mu_s(\nu)$ for all $r \neq s$.
2. When $\nu_0 - \nu_{n-1} = k + 1$, $m_0 - m_{n-1} = (k + 1) + (n - 1) = k + n = \ell$, so $\mu_0(\nu) = q^{2(m_{n-1}+\ell)} = q^{2m_{n-1}} = \mu_{n-1}(\nu)$, giving a repeated root and $\Delta(P_\nu) = 0$.
3. Suppose $P_\nu(u) = P_{\nu'}(u)$ with both $m, m'$ strictly decreasing of span $m_0 - m_{n-1} \le \ell - 1$ and $m'_0 - m'_{n-1} \le \ell - 1$. Then $\{m_0, \dots, m_{n-1}\}$ and $\{m'_0, \dots, m'_{n-1}\}$ reduce modulo $\ell$ to the same $n$-element subset $\bar{S} \subset \mathbb{Z}/\ell\mathbb{Z}$. Any strictly decreasing lift of $\bar{S}$ to $\mathbb{Z}$ contained in an interval of length $< \ell$ is uniquely obtained from $m$ by cutting the cyclic order on $\mathbb{Z}/\ell\mathbb{Z}$ at index $s \in \{0, 1, \dots, n-1\}$—adding $+\ell$ to the smallest $s$ entries $(m_{n-s}, \dots, m_{n-1})$ and reordering—plus a uniform shift $c\ell$ ($c \in \mathbb{Z}$). Summing all $n$ entries gives
   $$|\nu'| - \binom{n}{2} \;=\; \sum_{r=0}^{n-1} m'_r \;=\; \sum_{r=0}^{n-1} m_r + s\ell + cn\ell \;=\; |\nu| - \binom{n}{2} + (s + cn)\ell.$$
   If $|\nu'| \equiv |\nu| \pmod{n\ell}$, then $n\ell \mid (s + cn)\ell \implies n \mid s$; since $0 \le s < n$, $s = 0$, so $m'_r = m_r + c\ell$. At fixed $M = |\nu| = |\nu'|$, $(s + cn)\ell = 0$ also forces $c = 0$, giving $m' = m$ and $\nu' = \nu$. Varying $s \in \mathbb{Z}/n\mathbb{Z}$ corresponds in $\mathrm{SU}(n)_k$ to cyclic rotation of extended Dynkin labels, i.e. fusion with the $\mathbb{Z}/n\mathbb{Z}$ simple-current generator. $\blacksquare$

---

## 5. Braided Quantum Comatrix, Fusion Projectors & Wall Annihilation

Write $\Pi_n(u) = C_L(u)\, K_1(u)$, where
$$C_L(u) \;:=\; K_{\overline{n-1}}(q^{2(n-1)}u)\, K_{\overline{n-2}}(q^{2(n-2)}u) \cdots K_{\overline{1}}(q^2 u)$$
has degree $n - 1$ in $u$. Using Lemma 1(2), define the **Braided Quantum Comatrix** on $V \otimes \mathcal{H}$ by taking the ribbon-normalized partial trace over probe strands $2, \dots, n$:
$$\widehat{K}_q(u) \;:=\; \bigl([n]_q D_q^{-1} \otimes I_{\mathcal{H}}\bigr)\,\operatorname{Tr}_{2\dots n}\!\bigl(A_n\, C_L(u)\bigr) \;\in\; \operatorname{End}(V \otimes \mathcal{H})[u].$$

### Theorem 4 (Two-Sided Braided Cayley–Hamilton, Fusion Projectors & Verlinde Truncation)
1. **Two-Sided Braided Comatrix Identity (`BComatrix`):** *Identically on $V \otimes \mathcal{H}$,*
   $$\widehat{K}_q(u)\, K_1(u) \;=\; K_1(u)\, \widehat{K}_q(u) \;=\; I_V \otimes \operatorname{bdet}_q(u).$$
   *Consequently, substituting $u = \mathcal{L}_0$ in the central-coefficient polynomial $\operatorname{bdet}_q(u) = \sum_{s=0}^n u^s (I_V \otimes B_s)$ gives the braided Cayley–Hamilton theorem $\sum_{s=0}^n \mathcal{L}_0^s (I_V \otimes B_s) = 0$.*
2. **Pure-Braid Fusion-Channel Projectors (`CovUp_q`):** *Let $\nu$ lie in the Verlinde alcove ($\nu_0 - \nu_{n-1} \le k$), and let $V_\nu \subseteq \operatorname{CapSp}_q(\nu) := \bigcap_{u\in\mathbb{C}} \ker(\operatorname{bdet}_q(u) - P_\nu(u)I)$. Because the roots $\mu_i(\nu) = q^{2(\nu_i - i)}$ ($0 \le i < n$) are simple by Theorem 3(1), the pure-braid operators*
   $$\Pi_{\nu \to \nu + e_i} \;:=\; -\,\frac{\widehat{K}_q\bigl(\mu_i(\nu)\bigr)\big|_{V \otimes V_\nu}}{P'_\nu\bigl(\mu_i(\nu)\bigr)} \qquad (0 \le i < n)$$
   *are well-defined, mutually orthogonal idempotents ($\Pi_i \Pi_j = \delta_{ij}\Pi_i$) summing to $\sum_{i=0}^{n-1} \Pi_{\nu \to \nu+e_i} = I_{V \otimes V_\nu}$, with $\mathcal{L}_0 \Pi_i = \mu_i(\nu)\Pi_i$ and $\operatorname{im}(\Pi_i) \subseteq \operatorname{CapSp}_q(\nu + e_i)$ ($\Pi_i = 0$ automatically whenever $\nu_{i-1} = \nu_i$ so $\nu + e_i$ is not a partition).*
3. **Automatic Negligibility at the Verlinde Wall:** *When $\nu$ lies on the Verlinde wall ($\nu_0 - \nu_{n-1} = k$), $\Pi_{\nu \to \nu + e_0}$ is well-defined by Theorem 3(1), and its pivotal quantum trace on $V \otimes V_\nu$ vanishes identically:*
   $$\operatorname{Tr}_q\!\bigl(\Pi_{\nu \to \nu + e_0}\bigr) \;=\; 0, \qquad \operatorname{Tr}_q(X) := \operatorname{Tr}\!\bigl((D_q^{-1})^{\otimes(M+1)} X\bigr).$$
   *Passing to the semisimplified Modular Tensor Category $\mathrm{SU}(n)_k = \widetilde{\mathrm{Rep}}(U_q(\mathfrak{sl}_n))/\mathcal{N}$ (quotienting by negligible morphisms of zero quantum trace) kills $\Pi_{\nu \to \nu + e_0}$ and leaves $\sum_{i:\,\nu+e_i \in \mathrm{Alc}_k} \Pi_{\nu \to \nu+e_i} = I_{V \boxtimes_{\mathrm{Ver}} V_\nu}$.*

*Proof.*
1. Because $K_1(u) = \mathcal{L}_0 - uI$ acts only on probe slot $1$ and $\mathcal{H}$ (it is the identity on probe slots $2, \dots, n$), partial trace over slots $2, \dots, n$ is right-$K_1(u)$-linear:
   $$\operatorname{Tr}_{2\dots n}\!\bigl(A_n C_L(u)\bigr)\, K_1(u) \;=\; \operatorname{Tr}_{2\dots n}\!\bigl(A_n C_L(u) K_1(u)\bigr) \;=\; \operatorname{Tr}_{2\dots n}\!\bigl(A_n \Pi_n(u)\bigr) \;\overset{\text{Thm 2(1)}}{=}\; \operatorname{Tr}_{2\dots n}(A_n) \otimes \operatorname{bdet}_q(u).$$
   By Lemma 1(2), $\operatorname{Tr}_{2\dots n}(A_n) = \frac{1}{[n]_q} D_q$; left-multiplying by $[n]_q D_q^{-1} \otimes I_{\mathcal{H}}$ proves $\widehat{K}_q(u) K_1(u) = I_V \otimes \operatorname{bdet}_q(u)$.
   Write $\operatorname{bdet}_q(u) = \sum_{s=0}^n u^s B_s$ ($B_n = (-1)^n q^{n(n-1)} I_{\mathcal{H}}$) and $\widehat{K}_q(u) = \sum_{s=0}^{n-1} u^s \Gamma_s$. Equating powers of $u$ in $\bigl(\sum_{s=0}^{n-1} u^s \Gamma_s\bigr)(\mathcal{L}_0 - u I) = \sum_{s=0}^n u^s (I_V \otimes B_s)$ gives the backward Horner recursion $\Gamma_{n-1} = -(I_V \otimes B_n)$ and $\Gamma_{s-1} = \Gamma_s \mathcal{L}_0 - (I_V \otimes B_s)$ ($1 \le s \le n-1$), with $\Gamma_0 \mathcal{L}_0 = I_V \otimes B_0$. By Theorem 2(2), every $I_V \otimes B_s$ commutes with $\mathcal{L}_0$; hence by backward induction each $\Gamma_s$ is a polynomial in $\mathcal{L}_0$ with coefficients commuting with $\mathcal{L}_0$, so $[\widehat{K}_q(u), K_1(u)] = 0$ and $\sum_{s=0}^n \mathcal{L}_0^s (I_V \otimes B_s) = 0$.

2. Restricting to $V \otimes V_\nu$ sets $I_V \otimes \operatorname{bdet}_q(u) = P_\nu(u) I_{V\otimes V_\nu}$, so (1) gives
   $$-\widehat{K}_q(u)\big|_{V\otimes V_\nu}\, (u I - \mathcal{L}_0) \;=\; P_\nu(u) I_{V\otimes V_\nu} \qquad\text{and}\qquad P_\nu(\mathcal{L}_0)\big|_{V\otimes V_\nu} = 0.$$
   Writing $P_\nu(u) = c_{\mathrm{lead}}\prod_{j=0}^{n-1}(u - \mu_j(\nu))$ with $c_{\mathrm{lead}} = (-1)^n q^{n(n-1)}$, polynomial division in $u$ yields
   $$-\widehat{K}_q(u)\big|_{V\otimes V_\nu} \;=\; \frac{P_\nu(u) I - P_\nu(\mathcal{L}_0)}{u I - \mathcal{L}_0}\bigg|_{V\otimes V_\nu} \;\xrightarrow{u \to \mu_i(\nu)}\; c_{\mathrm{lead}} \prod_{j \neq i} \bigl(\mathcal{L}_0 - \mu_j(\nu) I\bigr).$$
   Since $\mu_0(\nu), \dots, \mu_{n-1}(\nu)$ are pairwise distinct by Theorem 3(1) and $P_\nu(\mathcal{L}_0) = c_{\mathrm{lead}}\prod_{j=0}^{n-1}(\mathcal{L}_0 - \mu_j(\nu) I) = 0$, dividing by $P'_\nu(\mu_i(\nu)) = c_{\mathrm{lead}}\prod_{j \neq i}(\mu_i(\nu) - \mu_j(\nu)) \neq 0$ produces the exact Lagrange spectral idempotents $\Pi_i = \prod_{j \neq i}\frac{\mathcal{L}_0 - \mu_j(\nu) I}{\mu_i(\nu) - \mu_j(\nu)}$ of $\mathcal{L}_0$, which satisfy $\Pi_i \Pi_j = \delta_{ij}\Pi_i$ and $\sum_{i=0}^{n-1} \Pi_i = I_{V\otimes V_\nu}$.

3. When $\nu_0 - \nu_{n-1} = k$, $\Pi_{\nu \to \nu+e_0}$ projects $V \otimes V_\nu$ onto the Weyl/tilting summand of highest weight $\nu + e_0 = (\nu_0 + 1, \nu_1, \dots, \nu_{n-1})$ (multiplicity $\operatorname{mult}(\nu)$). By the quantum Weyl character formula evaluated at the pivotal element $D_q^{-1} = \operatorname{diag}(q^{n-1}, q^{n-3}, \dots, q^{-(n-1)})$,
   $$\operatorname{Tr}_q\!\bigl(\Pi_{\nu \to \nu+e_0}\bigr) \;=\; \operatorname{mult}(\nu) \prod_{0 \le a < b < n} \frac{[(\nu+e_0)_a - (\nu+e_0)_b + b - a]_q}{[b - a]_q}.$$
   For $(a, b) = (0, n-1)$, the numerator factor is $[(\nu_0 + 1) - \nu_{n-1} + n - 1]_q = [k + n]_q = [\ell]_q = \frac{\sin(\pi)}{\sin(\pi/\ell)} = 0$, while every denominator factor $[b - a]_q$ has $1 \le b - a \le n - 1 < \ell$ and is strictly nonzero. Hence $\operatorname{Tr}_q(\Pi_{\nu \to \nu+e_0}) = 0$ identically. $\blacksquare$

---

## 6. Physical Payoff & Machine-Precision Verification

### Multi-Probe Fabry–Pérot Anyon Interferometry & Chiral Charge Resolution
In $(2+1)$D Fabry–Pérot / Mach–Zehnder double-braiding interferometry (Stern–Halperin 2006; Bonderson–Shtengel–Slingerland 2006), a single fundamental probe anyon $\square$ tunneling around an island of $M$ localized bulk anyons implements $\mathcal{L}_0$ and measures only its scalar expectation value $\operatorname{Tr}_q(\mathcal{L}_0)/d_\square = S_{\square, \nu}/S_{0, \nu}$, leaving two blind spots in higher-rank non-abelian phases:
1. **Chiral charge-conjugation degeneracy:** In $\mathrm{SU}(3)_3$ ($\ell = 6$, $q = e^{i\pi/6}$), the triplet $\mathbf{3} = (1,0,0)$ and anti-triplet $\overline{\mathbf{3}} = (1,1,0)$ share identical quantum dimension $d_{\mathbf{3}} = d_{\overline{\mathbf{3}}} = 2$ and identical topological spin $h_{\mathbf{3}} = h_{\overline{\mathbf{3}}} = \frac{2}{9}$. Yet our $3$-probe Braided Capelli polynomial separates them **even up to arbitrary $U(1)$ phase rotation**:
   - $P_{\mathbf{3}}(u)$ has roots at angles $(+2, -2, -4)\frac{\pi}{6}$ — counterclockwise arc steps $(2, 4, 6)\frac{\pi}{6}$ on $S^1$;
   - $P_{\overline{\mathbf{3}}}(u)$ has roots at angles $(+2, 0, -4)\frac{\pi}{6}$ — counterclockwise arc steps $(4, 2, 6)\frac{\pi}{6}$ on $S^1$, the **mirror-image scalene triangle**.
2. **Pure-braid state-selective fusion:** Evaluating the Braided Comatrix $\widehat{K}_q(\mu_i(\nu))$ synthesizes exact fusion-channel projectors $\Pi_{\nu \to \nu+e_i}$ out of pure topological braids alone, without microscopic Hamiltonian access.

### Verification Summary (`braided_capelli_anyon_demo.py`)
Running `python3 braided_capelli_anyon_demo.py` verifies Theorems 1–4 across four non-abelian anyon models:

| Phase | $q = e^{i\pi/\ell}$ | Spectral RE Err | Ribbon $\operatorname{Tr}$ Err | Comatrix / CH Err | Wall Fusion Tested | Forbidden $\lvert\operatorname{Tr}_q\rvert$ | Allowed Verlinde $\operatorname{Tr}_q$ |
|---|---|---:|---:|---:|---|---:|---|
| **Ising / Majorana** $\mathrm{SU}(2)_2$ | $e^{i\pi/4}$ | $5.2\times 10^{-15}$ | $0.0$ | $3.2\times 10^{-15}$ | $(2,0)\times\square \to (2,1)$ | $1.2\times 10^{-15}$ | $+1.414214 = \sqrt{2} = d_\sigma$ |
| **Fibonacci** $\mathrm{SU}(2)_3$ | $e^{i\pi/5}$ | $9.7\times 10^{-15}$ | $1.8\times 10^{-16}$ | $1.3\times 10^{-14}$ | $(3,0)\times\square \to (3,1)$ | $1.4\times 10^{-15}$ | $+1.618034 = \varphi = d_\tau$ |
| **Golden** $\mathrm{SU}(3)_2$ | $e^{i\pi/5}$ | $4.0\times 10^{-14}$ | $6.7\times 10^{-16}$ | $1.1\times 10^{-13}$ | $(2,1,0)^{\oplus 2}\times\square \to \overline{\mathbf{6}}\oplus\overline{\mathbf{3}}$ | $8.9\times 10^{-16}$ | $+2.000000 = 2d_{\overline{\mathbf{6}}},\; +3.236068 = 2\varphi$ |
| **Chiral** $\mathrm{SU}(3)_3$ | $e^{i\pi/6}$ | $2.9\times 10^{-16}$ | $5.4\times 10^{-16}$ | $1.1\times 10^{-15}$ | Chiral $\mathbf{3}$ vs $\overline{\mathbf{3}}$ ($M=1,2$) | — | Mirror-image $(2,4,6)$ vs $(4,2,6)$ root triangles |

---

## 7. Single-Probe Multi-Winding Quantum Newton Reduction (Eliminating $A_n$)

At first sight, constructing $\operatorname{bdet}_q(u)$ and $\widehat{K}_q(u)$ in §§3–5 appears to require $n$ simultaneous probe quasiparticles and physical implementation of the $n$-strand Hecke $q$-antisymmetrizer $A_n$. Remarkably, because $\ell = k + n > n$ keeps $[1]_q, \dots, [n]_q$ strictly invertible, **all $n$-probe operators collapse identically to polynomial combinations of single-probe multi-winding Fabry–Pérot traces** $P_1, \dots, P_n$—even on non-semisimple indecomposable tilting blocks beyond the Verlinde wall.

For each integer $m \ge 1$, define the **single-probe $m$-winding left ribbon trace** on $\mathcal{H}$:
$$P_m \;:=\; \operatorname{Tr}_V\!\bigl((D_q \otimes I_{\mathcal{H}})\,\mathcal{L}_0^m\bigr) \;=\; \sum_{a=0}^{n-1} q^{-(n - 1 - 2a)} \bigl(\mathcal{L}_0^m\bigr)_{aa} \;\in\; \operatorname{End}(\mathcal{H}),$$
where $D_q = \operatorname{diag}\bigl(q^{-(n-1)}, q^{-(n-3)}, \dots, q^{n-1}\bigr)$ is the probe-side ribbon weight from Lemma 1(2). *(Note the natural chirality pairing: closing a right tensor factor uses the pivotal element $D_q^{-1}$ of Theorem 4(3), whereas closing the leftmost probe factor $V$ uses $S^{-2} \leftrightarrow D_q$.)*

### Theorem 5 (Operator-Level Quantum Newton Identities & 1-Probe Comatrix Synthesis)
*Let $\Omega_n := \{q \in \mathbb{C}^\times : [1]_q [2]_q \cdots [n]_q \neq 0\}$ (which contains every root of unity $q = e^{i\pi/(k+n)}$ with $k \ge 1$ as well as every real prime parameter $q = p^{1/2}$). Define $E_0 := I_{\mathcal{H}}$ and define $E_1, \dots, E_n \in \operatorname{End}(\mathcal{H})$ recursively from the single-probe winding operators $P_1, \dots, P_n$ by*
$$[r]_q\, E_r \;=\; q^{r - n} \sum_{m=1}^{r} (-1)^{m-1}\, P_m\, E_{r - m} \qquad (1 \le r \le n).$$
*Then on $\mathcal{H} = V^{\otimes M}$ for **every** $M \ge 0$ and **every** $q \in \Omega_n$ (including $M > k$ at $q = e^{i\pi/(k+n)}$, where $V^{\otimes M}$ is non-semisimple):*
1. **Centrality & Commutativity:** *Every $P_m$ and $E_r$ commutes with $U_q(\mathfrak{gl}_n)$, with $B_M$, and pairwise ($[P_m, P_{m'}] = [E_r, E_{r'}] = 0$).*
2. **Exact Elimination of $A_n$ for $\operatorname{bdet}_q(u)$:** *The $n$-probe Braided Quantum Determinant $\operatorname{bdet}_q(u) = \sum_{s=0}^n u^s B_s$ equals*
   $$B_s \;=\; q^{n(n-1)} (-1)^s E_{n - s} \quad (0 \le s \le n), \qquad \operatorname{bdet}_q(u) \;=\; q^{n(n-1)} \sum_{r=0}^{n} (-1)^{n-r} u^{n-r} E_r.$$
3. **1-Probe Braided Comatrix & Fusion Projectors:** *Setting $\Gamma_{n-1} := -(I_V \otimes B_n)$ and $\Gamma_{s-1} := \Gamma_s \mathcal{L}_0 - (I_V \otimes B_s)$ ($1 \le s \le n-1$) reconstructs $\widehat{K}_q(u) = \sum_{s=0}^{n-1} u^s \Gamma_s$—and hence every fusion projector $\Pi_{\nu \to \nu + e_i}$—purely from a **single** probe anyon's braidings $\mathcal{L}_0$ and its $1$- to $n$-winding traces $P_1, \dots, P_n$.*

*Proof.*
1. Under the coproduct $\Delta(e_a) = e_a \otimes k_a + 1 \otimes e_a$, $\Delta(f_a) = f_a \otimes 1 + k_a^{-1} \otimes f_a$, $\Delta(k_a) = k_a \otimes k_a$ ($k_a = q^{E_{aa} - E_{a+1,a+1}}$) intertwined by $\check{R} = PR$, any $U_q(\mathfrak{gl}_n)$-commuting operator $X = \sum_{c,d} E_{cd} \otimes X_{cd} \in \operatorname{End}(V \otimes \mathcal{H})$ satisfies $k_a X_{a+1,a} = q^2 X_{a+1,a} k_a$ (from $[X, \Delta(k_a)] = 0$) and $[X_{aa}, e_a] = k_a X_{a+1,a}$, $[X_{a+1,a+1}, e_a] = -X_{a+1,a} k_a$, $[X_{cc}, e_a] = 0$ ($c \notin \{a, a+1\}$) (from $[X, \Delta(e_a)] = 0$). Weighting by $d_c = q^{-(n-1-2c)}$ ($d_{a+1} = q^2 d_a$) cancels $d_a k_a X_{a+1,a} - d_{a+1} X_{a+1,a} k_a = 0$, and similarly for $f_a$. Taking $X = \mathcal{L}_0^m$ shows that $P_m$ commutes with $U_q(\mathfrak{gl}_n)$ (and clearly with $B_M$).

2. Assume first that $q \in \Omega_n$ is **not** a root of unity, so $V^{\otimes M} \cong \bigoplus_{\nu \vdash M} V_\nu^{\oplus \mathrm{mult}(\nu)}$ is semisimple. On $V \otimes V_\nu = \bigoplus_r V_{\nu+e_r}$, $\mathcal{L}_0 = \sum_r \mu_r \Pi_{\nu\to\nu+e_r}$ with $\mu_r = q^{2 m_r}$, $m_r = \nu_r - r$. By (1) and Schur's lemma on $V_\nu$, $\operatorname{Tr}_V((D_q \otimes I_{V_\nu})\Pi_{\nu\to\nu+e_r}) = w_r(\nu) I_{V_\nu}$ for a scalar $w_r(\nu)$. Applying $\operatorname{Tr}_{V_\nu}(D_q^{\otimes M} -)$ to both sides and using symmetry of Schur polynomials $s_\lambda(q^{-(n-1)}, \dots, q^{n-1}) = s_\lambda(q^{n-1}, \dots, q^{-(n-1)}) = \dim_q(V_\lambda)$ gives
   $$w_r(\nu) \;=\; \frac{\dim_q(V_{\nu + e_r})}{\dim_q(V_\nu)} \;=\; \prod_{j \neq r} \frac{[m_r - m_j + 1]_q}{[m_r - m_j]_q} \;=\; q^{-(n-1)} \prod_{j \neq r} \frac{q^2 \mu_r - \mu_j}{\mu_r - \mu_j}$$
   (which automatically vanishes whenever $\nu_{r-1} = \nu_r$, since $m_{r-1} = m_r + 1$). Hence $P_m|_{V_\nu} = \sum_{r=0}^{n-1} w_r(\nu) \mu_r^m I_{V_\nu}$.
   Since $\mu_0, \dots, \mu_{n-1}$ are distinct at generic $q$, Lagrange partial-fraction expansion of $\prod_{j=0}^{n-1}\frac{q^2 z - \mu_j}{z - \mu_j}$ in $z$ gives identically:
   $$\prod_{j=0}^{n-1} \frac{q^2 z - \mu_j}{z - \mu_j} \;=\; q^{2n} \;+\; \sum_{r=0}^{n-1} \frac{(q^2 - 1)\mu_r \prod_{j\neq r}(q^2\mu_r - \mu_j)}{\prod_{j\neq r}(\mu_r - \mu_j)} \cdot \frac{1}{z - \mu_r} \;=\; q^{2n} \;+\; q^n(q - q^{-1}) \sum_{r=0}^{n-1} \frac{w_r(\nu)\, \mu_r}{z - \mu_r}.$$
   Substituting $z = t^{-1}$, setting $E(t) := \prod_{j=0}^{n-1}(1 - \mu_j t) = \sum_{r=0}^n (-1)^r E_r t^r$, and expanding $\frac{\mu_r}{t^{-1} - \mu_r} = \sum_{m=1}^\infty \mu_r^m t^m$ yields
   $$q^{2n} E(q^{-2} t) \;=\; \left(q^{2n} + q^n(q - q^{-1})\sum_{m=1}^\infty P_m\big|_{V_\nu}\, t^m\right) E(t).$$
   Equating coefficients of $t^r$ ($1 \le r \le n$) gives $q^{2n}(1 - q^{-2r})E_r = q^n(q - q^{-1})\sum_{m=1}^r (-1)^{m-1} P_m E_{r-m}$, which divides by $q^{2n-r}(q - q^{-1})$ to the Quantum Newton recursion $[r]_q E_r = q^{r-n}\sum_{m=1}^r (-1)^{m-1} P_m E_{r-m}$. Comparing $P_\nu(u) = q^{n(n-1)}\prod_{j=0}^{n-1}(\mu_j - u) = q^{n(n-1)}\sum_{s=0}^n (-1)^s E_{n-s} u^s$ with $\operatorname{bdet}_q(u)|_{V_\nu} = P_\nu(u) I_{V_\nu}$ proves $B_s = q^{n(n-1)}(-1)^s E_{n-s}$ on all of $V^{\otimes M}$ for every non-root-of-unity $q \in \Omega_n$.

3. Finally, regard $q$ as a complex variable on $\Omega_n$. Because $\check{R}(q)$, $\hat{T}_m(q)$, and $\hat{T}_m(q)^{-1} = \hat{T}_m(q) - \omega I$ all have matrix entries in $\mathbb{Z}[q, q^{-1}]$, both the $n$-probe coefficients $B_s(q)$ (via $A_n(q)$) and the 1-probe Quantum Newton operators $q^{n(n-1)}(-1)^s E_{n-s}(q)$ (via $([r]_q)^{-1}$, $1 \le r \le n$) have matrix entries in $\mathbb{Z}[q, q^{-1}, ([n]_q!)^{-1}]$—holomorphic everywhere on $\Omega_n$. Since they coincide on the dense complement of roots of unity in $\Omega_n$, they are **identically equal as matrices on $V^{\otimes M}$ at every point of $\Omega_n$** (including $q = e^{i\pi/(k+n)}$ for all $M$, even when $M > k$ and $V^{\otimes M}$ is non-semisimple!). Part (3) then follows immediately from the backward Horner identity of Theorem 4(1) (and `[P_m, P_{m'}] = 0` holds on all of $\Omega_n$ by the same Zariski-density principle). $\blacksquare$

---

## 8. Experimental Predictions for Single-Edge $\mathrm{SU}(3)_3$ Fabry–Pérot Interferometry

Theorem 5 turns multi-probe Capelli spectroscopy into **harmonic analysis of a single Fabry–Pérot interferometer** (already used experimentally to observe fractional statistics via 1st/2nd/3rd tunneling harmonics $e^{im\phi_0}$, where $\phi_0 = 2\pi \Phi/\Phi_0$ is the unknown Aharonov–Bohm background phase per winding). For a fundamental probe $\square = \mathbf{3}$ ($d_{\mathbf{3}} = [3]_q$) winding $m$ times around a localized bulk quasiparticle $\nu$, the normalized $m$-th harmonic tunneling visibility is
$$V_m(\nu) \;:=\; \frac{\lvert p_m(\nu)\rvert}{d_{\mathbf{3}}} \;\in\; [0, 1], \qquad p_m(\nu) \;:=\; P_m\big|_{V_\nu} \;=\; \sum_{r=0}^{n-1} \frac{d_{\nu+e_r}}{d_\nu}\,\mu_r(\nu)^m,$$
and the **bicoherence** $B_{12}(\nu) := p_1(\nu)^2\,\overline{p_2(\nu)}$ is **strictly invariant under arbitrary magnetic-flux offsets** $p_m \mapsto e^{im\phi_0} p_m$.

### Theorem 6 (2nd-Harmonic Chiral Doubling & 3rd-Harmonic Ghost Revival in $\mathrm{SU}(3)_3$)
*In $\mathrm{SU}(3)_3$ ($q = e^{i\pi/6}$, $\ell = 6$, $d_{\mathbf{3}} = 2$), single-probe Fabry–Pérot interferometry exhibits two sharp, parameter-free signatures:*
1. **2nd-Harmonic Chiral Doubling ($\mathbf{3}$ vs. $\overline{\mathbf{3}}$):** *Although the triplet $\mathbf{3} = (1,0,0)$ and anti-triplet $\overline{\mathbf{3}} = (1,1,0)$ have identical 1st-harmonic visibility $V_1(\mathbf{3}) = V_1(\overline{\mathbf{3}}) = \frac{1}{2}$, at the 2nd harmonic $\overline{\mathbf{3}}$ constructively phase-locks to **100% visibility—double that of $\mathbf{3}$**—with opposite-sign bicoherence:*
   $$\begin{aligned}
   \mathbf{3} = (1,0,0): \quad & p_m(\mathbf{3}) = 2\cos\!\left(\frac{m\pi}{3}\right)
   &&\Longrightarrow\quad V_1 = \frac{1}{2},\;\; V_2 = \mathbf{\frac{1}{2}},\;\; V_3 = 1,\;\; B_{12}(\mathbf{3}) = \mathbf{-1}, \\
   \overline{\mathbf{3}} = (1,1,0): \quad & p_m(\overline{\mathbf{3}}) = \frac{3}{2}e^{im\pi/3} + \frac{1}{2}e^{-2im\pi/3}
   &&\Longrightarrow\quad V_1 = \frac{1}{2},\;\; V_2 = \mathbf{1},\;\; V_3 = \frac{1}{2},\;\; B_{12}(\overline{\mathbf{3}}) = \mathbf{+2}.
   \end{aligned}$$
2. **"Ghost Anyon" 3rd-Harmonic Revival ($\mathbf{8}$):** *A localized adjoint octet $\mathbf{8} = (2,1,0)$ ($d_{\mathbf{8}} = 3$) has **identically zero** interference visibility at both the 1st and 2nd harmonics, followed by **100% full-contrast revival** at the 3rd harmonic:*
   $$p_m(\mathbf{8}) \;=\; \frac{2}{3}\bigl(1 + e^{2\pi i m/3} + e^{-2\pi i m/3}\bigr) \;=\; \begin{cases} 2 & \text{if } 3 \mid m, \\ 0 & \text{if } 3 \nmid m \end{cases}
   \quad\Longrightarrow\quad V_1(\mathbf{8}) = 0,\;\; V_2(\mathbf{8}) = 0,\;\; V_3(\mathbf{8}) = \mathbf{1}.$$

*Proof.* At $\ell = 6$, $([1]_q, [2]_q, [3]_q, [4]_q, [5]_q) = (1, \sqrt{3}, 2, \sqrt{3}, 1)$.
1. For $\mathbf{3} = (1,0,0)$ ($d_{\mathbf{3}} = 2$), $\mathbf{3} \boxtimes \mathbf{3} = \mathbf{6}_{(2,0,0)} \oplus \overline{\mathbf{3}}_{(1,1,0)}$ with $d_{\mathbf{6}} = \frac{[3]_q[4]_q[1]_q}{[1]_q[2]_q} = 2$ and $d_{\overline{\mathbf{3}}} = 2$, so $w = (1, 1, 0)$ at $\mu = (e^{i\pi/3}, e^{-i\pi/3}, e^{-2i\pi/3})$, giving $p_m(\mathbf{3}) = 2\cos(m\pi/3)$, $p_1 = 1$, $p_2 = -1$, $B_{12} = -1$.
   For $\overline{\mathbf{3}} = (1,1,0)$ ($d_{\overline{\mathbf{3}}} = 2$), $\mathbf{3} \boxtimes \overline{\mathbf{3}} = \mathbf{8}_{(2,1,0)} \oplus \mathbf{1}_{(1,1,1)}$ with $d_{\mathbf{8}} = \frac{[2]_q[4]_q[2]_q}{[1]_q[2]_q} = 3$ and $d_{\mathbf{1}} = 1$, so $w = (\frac{3}{2}, 0, \frac{1}{2})$ at $\mu = (e^{i\pi/3}, 1, e^{-2i\pi/3})$. At $m = 1$, $p_1(\overline{\mathbf{3}}) = \frac{3}{2}e^{i\pi/3} + \frac{1}{2}e^{-2i\pi/3} = e^{i\pi/3}$ ($|p_1| = 1$). At $m = 2$, $e^{2i\pi/3} = e^{-4i\pi/3}$ aligns both channels in phase: $p_2(\overline{\mathbf{3}}) = (\frac{3}{2} + \frac{1}{2})e^{2i\pi/3} = 2e^{2i\pi/3}$ ($|p_2| = 2 = d_{\mathbf{3}}$, $B_{12} = e^{2i\pi/3}\cdot 2e^{-2i\pi/3} = +2$).
2. For $\mathbf{8} = (2,1,0)$ ($d_{\mathbf{8}} = 3$), $\mathbf{3} \boxtimes \mathbf{8} = (3,1,0) \oplus \overline{\mathbf{6}}_{(2,2,0)} \oplus \mathbf{3}_{(2,1,1)}$. Computing Weyl dimensions at $\ell = 6$ gives $d_{(3,1,0)} = \frac{[3]_q[5]_q[2]_q}{[1]_q[2]_q} = 2$, $d_{(2,2,0)} = \frac{[1]_q[4]_q[3]_q}{[1]_q[2]_q} = 2$, and $d_{(2,1,1)} = \frac{[2]_q[3]_q[1]_q}{[1]_q[2]_q} = 2$—equal relative weights $w = (\frac{2}{3}, \frac{2}{3}, \frac{2}{3})$ at $\mu = (q^4, 1, q^{-4}) = (e^{2\pi i/3}, 1, e^{-2\pi i/3})$, the exact cube roots of unity! $\blacksquare$

---

## 9. Tri-Modal Unification ($v = \infty \leftrightarrow \text{Anyons} \leftrightarrow v = p$) & Manin's Tamagawa Volume

Finally, Theorem 5 reveals that the Braided Capelli engine is a **single universal polynomial identity over $\mathbb{Z}[q, q^{-1}, ([n]_q!)^{-1}]$** uniting all three arenas with which this investigation began: the Archimedean Yangian of `lean/src/`, $(2+1)$D non-abelian anyons, and non-Archimedean $p$-adic Hecke arithmetic in Yuri Manin's [*Reflections on Arithmetical Physics*](file:///home/marcus/GitHub/mbintz/incandescent/manin_reflection.pdf).

### Theorem 7 (Bernstein–Satake Commutativity, $p$-adic Iwahori–Hecke Specialization & Tamagawa Volume)
1. **Universal Bernstein–Jucys–Murphy Lattice:** *On $V^{\otimes n} \otimes \mathcal{H}$, define $X_1 := \mathcal{L}_1$ and $X_{r+1} := \hat{T}_r X_r \hat{T}_r$ ($1 \le r \le n-1$). Then $X_1, \dots, X_n$ **commute pairwise** ($[X_r, X_s] = 0$) in the group algebra of $B_{M+n}$, generating the affine Hecke Bernstein–Zelevinsky lattice subalgebra.*
2. **$p$-adic Iwahori–Hecke Specialization ($q = p^{1/2}$):** *At $q = p^{1/2}$ ($p$ any rational prime), $p^{1/2} \in \Omega_n$ for every $n \ge 2$, and the rescaled probe generators $\tilde{T}_m := p^{1/2}\hat{T}_m$ satisfy*
   $$(\tilde{T}_m - p I)(\tilde{T}_m + I) \;=\; 0,$$
   *the defining quadratic relation of the **$p$-adic Iwahori–Hecke algebra $\mathcal{H}\bigl(\mathrm{GL}_n(\mathbb{Q}_p), I_p\bigr)$**, while symmetric polynomials in $X_1, \dots, X_n$ realize the spherical Satake algebra $\mathcal{H}\bigl(\mathrm{GL}_n(\mathbb{Q}_p), \mathrm{GL}_n(\mathbb{Z}_p)\bigr)$.*
3. **Adelic Vacuum Euler Product = Manin's Fundamental Volume:** *In the vacuum sector $M = 0$ ($\nu = (0,\dots,0)$, where $P_m = [n]_{p^{1/2}}$), the reciprocal 1-probe Quantum Newton polynomial $E_{0, p^{1/2}}(t) = \sum_{r=0}^n (-1)^r E_r(0; p^{1/2})\, t^r = \prod_{r=0}^{n-1}(1 - p^{-r} t)$ reproduces the local Macdonald–Godement–Jacquet spherical Euler factor $E_{0, p^{1/2}}(p^{-s})^{-1} = \prod_{r=0}^{n-1}\zeta_p(s + r)$. Stripping the central $\mathrm{GL}_1$ mode ($r = 0$) at $s = 1$ and taking the Euler product over all primes $p$ yields*
   $$\prod_{p \text{ prime}} \frac{1 - p^{-1}}{E_{0, p^{1/2}}(p^{-1})} \;=\; \prod_{p \text{ prime}} \prod_{r=1}^{n-1} (1 - p^{-(r+1)})^{-1} \;=\; \zeta(2)\zeta(3)\cdots\zeta(n) \;=\; \operatorname{vol}\!\bigl(\mathrm{SL}_n(\mathbb{R})/\mathrm{SL}_n(\mathbb{Z})\bigr),$$
   *recovering Manin's exact adelic volume formula ([manin_reflection.pdf](file:///home/marcus/GitHub/mbintz/incandescent/manin_reflection.pdf), p. 527) directly from the vacuum roots of $\operatorname{bdet}_{p^{1/2}}$.*

*Proof.*
1. For $r=1, s=2$, $X_2 X_1 = \hat{T}_1 \mathcal{L}_1 \hat{T}_1 \mathcal{L}_1 = \mathcal{L}_1 \hat{T}_1 \mathcal{L}_1 \hat{T}_1 = X_1 X_2$ is Theorem 1(1). For general $1 \le r < s \le n$, prove $[X_r, X_s] = 0$ by induction on $s$: if $r < s - 1$, $[\hat{T}_{s-1}, X_r] = 0$ (disjoint probe strands), so $X_s X_r = \hat{T}_{s-1} X_{s-1} \hat{T}_{s-1} X_r = \hat{T}_{s-1} X_{s-1} X_r \hat{T}_{s-1} \overset{\text{IH}}{=} \hat{T}_{s-1} X_r X_{s-1} \hat{T}_{s-1} = X_r X_s$. For $r = s - 1$ ($s \ge 3$), using $\hat{T}_{s-1}\hat{T}_{s-2}\hat{T}_{s-1} = \hat{T}_{s-2}\hat{T}_{s-1}\hat{T}_{s-2}$, $[\hat{T}_{s-1}, X_{s-2}] = 0$, and the $s-1$ case $X_{s-2}\hat{T}_{s-2} X_{s-2}\hat{T}_{s-2} = \hat{T}_{s-2} X_{s-2}\hat{T}_{s-2} X_{s-2}$:
   $$\begin{aligned}
   X_{s-1} X_s
   &= \hat{T}_{s-2} X_{s-2} (\hat{T}_{s-2}\hat{T}_{s-1}\hat{T}_{s-2}) X_{s-2} \hat{T}_{s-2}\hat{T}_{s-1}
    = \hat{T}_{s-2} X_{s-2} (\hat{T}_{s-1}\hat{T}_{s-2}\hat{T}_{s-1}) X_{s-2} \hat{T}_{s-2}\hat{T}_{s-1} \\
   &= \hat{T}_{s-2}\hat{T}_{s-1} X_{s-2} \hat{T}_{s-2} X_{s-2} (\hat{T}_{s-1}\hat{T}_{s-2}\hat{T}_{s-1})
    = \hat{T}_{s-2}\hat{T}_{s-1} (X_{s-2} \hat{T}_{s-2} X_{s-2} \hat{T}_{s-2}) \hat{T}_{s-1}\hat{T}_{s-2} \\
   &\overset{\text{IH}}{=} (\hat{T}_{s-2}\hat{T}_{s-1} \hat{T}_{s-2}) X_{s-2} \hat{T}_{s-2} X_{s-2} \hat{T}_{s-1}\hat{T}_{s-2}
    = \hat{T}_{s-1}\hat{T}_{s-2} \hat{T}_{s-1} X_{s-2} \hat{T}_{s-2} \hat{T}_{s-1} X_{s-2} \hat{T}_{s-2} \\
   &= \hat{T}_{s-1}\hat{T}_{s-2} X_{s-2} (\hat{T}_{s-1}\hat{T}_{s-2}\hat{T}_{s-1}) X_{s-2} \hat{T}_{s-2}
    = \hat{T}_{s-1}\hat{T}_{s-2} X_{s-2} (\hat{T}_{s-2}\hat{T}_{s-1}\hat{T}_{s-2}) X_{s-2} \hat{T}_{s-2} \;=\; X_s X_{s-1}.
   \end{aligned}$$
2. Multiplying $(\hat{T}_m - p^{1/2} I)(\hat{T}_m + p^{-1/2} I) = 0$ by $p$ gives $(\tilde{T}_m - p I)(\tilde{T}_m + I) = 0$.
3. At $M = 0$ ($\nu = 0$) and $q = p^{1/2}$, Theorem 2(3) and Theorem 5(2) give $E_{0, p^{1/2}}(t) = \prod_{r=0}^{n-1}(1 - p^{-r} t) = (1 - t)\prod_{r=1}^{n-1}(1 - p^{-r} t)$. Evaluating $\frac{1 - p^{-1}}{E_{0, p^{1/2}}(p^{-1})} = \prod_{r=1}^{n-1}(1 - p^{-(r+1)})^{-1}$ and multiplying over all primes $p$ yields $\prod_{k=2}^n \zeta(k) = \operatorname{vol}(\mathrm{SL}_n(\mathbb{R})/\mathrm{SL}_n(\mathbb{Z}))$ by Siegel–Weil ($\tau(\mathrm{SL}_n) = 1$). $\blacksquare$
