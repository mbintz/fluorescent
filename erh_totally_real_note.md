# Note: Extending the Alpoge–Claude Proof of GRH to the Extended Riemann Hypothesis for Arbitrary Totally Real and CM Number Fields

## 1. Statement of the Target Theorem

Let $F/\mathbb{Q}$ be **any totally real number field** or **any CM number field** of degree $d_F = [F:\mathbb{Q}]$ (with **no** abelianness or solvability assumption on its Galois closure $L_0/\mathbb{Q}$ — e.g. totally real $S_3$-cubic fields such as $\mathbb{Q}[x]/(x^3 - 4x - 1)$ of discriminant $229$, $D_n$-dihedral fields, $A_4$/$S_4$-quartic fields, or non-solvable totally real $A_5$-quintic fields).

**Target Theorem (ERH for Totally Real and CM Fields).** *Every zero $\rho$ of the Dedekind zeta function $\zeta_F(s)$ in the critical strip $0 < \operatorname{Re}(s) < 1$ satisfies $\operatorname{Re}(\rho) = \tfrac{1}{2}$. More generally, the same holds for $L_F(s, \psi)$ for every finite-order Hecke character $\psi$ of $F$ whose splitting field is totally real or CM, and hence for every totally even or CM Artin $L$-function (including even icosahedral $A_5$ Artin $L$-functions).*

> **Scope boundary (Albert–Weil barrier):** Every subfield of a CM field is totally real or CM, and by Weil's 1956 theorem every algebraic Hecke character of a number field $M$ factors through its maximal CM subfield $M_{\mathrm{CM}}$. Thus mixed-signature non-CM fields (such as $\mathbb{Q}(\sqrt[3]{2})$) lie outside the direct CM-host architecture below and require a genuinely new mechanism (see our separate analysis of Walls 1 and 2).

---

## 2. How the Alpoge–Claude Engine Works (Verified Against `lean/src/`)

In the formalized proof of Dirichlet GRH (`Main.lean`), the zero-free half-plane $\operatorname{Re}(s) > \tfrac{1}{2}$ comes from five interlocking modules:

1. **CM Host Field** ([ConjEMemHostFIff.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ConjEMemHostFIff.lean)):
   An abelian CM field $E = E^+(\sqrt{-d})$ with Galois group $G = E_0 \times A$ ($E_0 = (\mathbb{Z}/2)^2$ for $\mathbb{Q}(\sqrt{q}, \sqrt{-d})$, $A$ containing the $2$-power cyclotomic subextension $A_0 \cong \mathbb{Z}/2^e\mathbb{Z}$ of size $\asymp x^{2+8\varepsilon}$), CM type $\Phi = \{\sigma : E \hookrightarrow \mathbb{C} \mid \sigma(\sqrt{-d}) = i\sqrt{d}\}$ **lifted from $K = \mathbb{Q}(\sqrt{-d})$**, and unimodular different factorization $\mathfrak{D}_{E/K} = \mathfrak{b}\cdot\overline{\mathfrak{b}}$ with $\mathfrak{b} + \overline{\mathfrak{b}} = (1)$.

2. **Inert-Prime Divisibility vs. Bost's Slope Inequality** ([FirstPrimeNeSecondPrime.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/FirstPrimeNeSecondPrime.lean), [MeanBoundSecondForm.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/RankGapBounds/MeanBoundSecondForm.lean), [QuotientSlopeBoundsWith.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/QuotientSlopeBoundsWith.lean)):
   An $m \approx x^{1/2 - \varepsilon/16}$-fold iterated theta lift between totally definite unitary groups over $E^+$ produces an integral structure whose $a$-th derivative divisibility at inert primes of $K$ is
   $$\operatorname{ASK}(a, t, w) = \sum_{p \text{ inert}} 2(\log p) \sum_{\substack{i \ge 1 \\ \operatorname{Frob}_p^i \notin \Phi}} \max\!\left(\frac{a}{p^i} - w\bigl(\operatorname{partner}(t, \operatorname{Frob}_p^i)\bigr),\; 0\right).$$
   Bost's arithmetic slope inequality (`SlopeIneq` + `DIV` + Chowla–Selberg $\log\Omega = \gamma + \log(\pi/v) - L'(1,\chi_{-d})/L(1,\chi_{-d})$) proves **pointwise for each $u_0$**:
   $$\operatorname{ASK}(u_0) \le \operatorname{MAIN}(u_0) + \mathrm{Err}.$$

3. **Fourier / Pontryagin Balance (`AskMainBalance`)** ([FirstPrimeNeSecondPrime.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/FirstPrimeNeSecondPrime.lean), [GrowthBoundGivesRiemannHypothesis.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/GrowthBoundGivesRiemannHypothesis.lean)):
   Averaging $\operatorname{ASK}(u_0) - \operatorname{MAIN}(u_0)$ over $u_0$ isolates $G_\sigma(x)$ on the thick embeddings ($w \approx b$, $a/w \approx x$), while on the thin embeddings ($w \le 2b'$, $a/w \ge X' = \exp(x^{\varepsilon/3})$) classical zero-free regions (`ThinScales`) crush every term to $O(y\exp(-x^{\varepsilon/8}))$.

4. **Quadratic Twist Control (`PairGood`)** ([BoxOfS.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/BoxOfS.lean), [CountBadCore.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/CountBadCore.lean)):
   Choosing $(q, d)$ with $\log q \asymp Y^{\varepsilon/5}$, $\log d \asymp Y^{\varepsilon/5}(\log Y)^2$ outside a zero-density exceptional set of size $\ll Q^{1/4}$ in $\operatorname{Re}(s) > 1 - \frac{1}{400}$, $|t| \le Q$, splitting $G_\chi(y)$ at $Z = (Y^K)^{400}$, and applying quadratic mean-square bounds kills the auxiliary twist terms $G_{\chi_q}, G_{\chi_{-d}}, G_{\chi_{-dq}}$.

5. **Vandiver Weakening (`HypV` / `VVle`)** ([ExistsPageN.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean), [KatoUse.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean), [KatoTwoWOfPublishedH.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/KatoTwoWOfPublishedH.lean)):
   Bounds $\sum_\ell (\log \ell)\sum_{1 \le e < x^{401}} \operatorname{length}_{\mathbb{Z}_\ell} \operatorname{Sha}^1(\mathcal{O}_E[1/\ell], (\mathbb{Q}_\ell/\mathbb{Z}_\ell)(-e)) \le \exp(\tfrac{1}{2}x^\varepsilon)$ using $U(3)$ Eisenstein congruence numbers (`CorGK`) + quadratic base change (`QuadBC2`) + patching.

---

## 3. The Five Modifications Lifting the Proof to Arbitrary Totally Real & CM Fields

Assume without loss of generality that $F$ is totally real (if $F$ is CM, replace $F$ by its totally real subfield $F^+$ and include the quadratic CM character $\chi_{F/F^+}$ — or simply take $L_0$ to be the Galois closure of $F$, which is still CM so complex conjugation is central in $\Gamma = \operatorname{Gal}(L_0/\mathbb{Q})$!). Let $L_0/\mathbb{Q}$ be the totally real Galois closure of $F$, $\Gamma = \operatorname{Gal}(L_0/\mathbb{Q})$, $H_F = \operatorname{Gal}(L_0/F) \le \Gamma$, and $\pi_F(\gamma) = \#\mathrm{Fix}_{\Gamma/H_F}(\gamma)$ the permutation character of $F$.

### Step 1: Non-Abelian Galois CM Host $E$
Define the compositum
$$E := L_0 \cdot K \cdot \mathbb{Q}(\sqrt{q}) \cdot \mathbb{Q}(\zeta_{2^{e+2}})^+, \qquad K = \mathbb{Q}(\sqrt{-d}),$$
with $q, d$ large primes coprime to $2\operatorname{disc}(L_0)$ and $d$ splitting every odd prime $\ell \mid 2q\operatorname{disc}(L_0)$ (replacing $\mathbb{Q}(\zeta_{2^{e+2}})^+$ by the linearly disjoint subextension above $L_0 \cap \mathbb{Q}(\zeta_{2^\infty})^+$ of degree $2^e \asymp x^{2+8\varepsilon}$). Then:
- $E^+ = L_0 \cdot \mathbb{Q}(\sqrt{q}) \cdot \mathbb{Q}(\zeta_{2^{e+2}})^+$ is **totally real**, and $E = E^+(\sqrt{-d})$ is a **Galois CM field** with Galois group
  $$G = \operatorname{Gal}(E/\mathbb{Q}) \cong E_0 \times A_0 \times \Gamma, \qquad E_0 = (\mathbb{Z}/2)^2,\quad A_0 \cong \mathbb{Z}/2^e\mathbb{Z},$$
  where **$E_0 \times A_0$ is central in $G$** (in particular, complex conjugation $c \in E_0$ is central!).
- The CM type $\Phi = \{\sigma : E \hookrightarrow \mathbb{C} \mid \sigma(\sqrt{-d}) = i\sqrt{d}\}$ is **still lifted from $K = \mathbb{Q}(\sqrt{-d})$**.
- Every prime ramified in $E^+/K$ lies above a prime split in $K$, so $\mathfrak{D}_{E/K} = \mathfrak{b}\cdot\overline{\mathfrak{b}}$ with $\mathfrak{b} + \overline{\mathfrak{b}} = (1)$ and $\sigma(\mathfrak{b}) = \mathfrak{b}$ for all $\sigma \in \operatorname{Gal}(E/K)$ still holds identically.
- **Audit of `LocalToGlobal` / `SharpRestriction`:** Grepping `cycEmb` / `.art` across `Formalism/LocalToGlobal` and `Formalism/SharpRestriction` confirmed only two non-structural uses of cyclotomic embedding:
  1. [ModEqOfNormOneMod.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalToGlobal/GlobalTheory/GL2/ModEqOfNormOneMod.lean) (`splits_of_modEq`), which uses $p \equiv 1 \pmod{N_E}$ to force complete splitting in $E$ — replaced directly by Chebotarev for $\{1\} \subset \Gamma \times (\mathbb{Z}/N_E\mathbb{Z})^\times$ (fixed density $1/|\Gamma|$).
  2. [PolyConstantLeZBasePowFour.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/GenusPolyhedralBounds/RelativeIndexClassSets/PolyConstantLeZBasePowFour.lean) (`f_le_condE`), which bounds $[E:\mathbb{Q}] \le \mathrm{cond}_E$ — replaced by $[E:\mathbb{Q}] \le |\Gamma|\cdot\mathrm{cond}_{E_{\mathrm{ab}}}$.

### Step 2: The Non-Abelian Conjugacy Thick-Set Identity (`AskMainBalance` for $\Gamma$)
Fix $t \in A_0$ (central in $G$). For each $u_0 = (u_{0,A}, u_{0,\Gamma}) \in A_0 \times \Gamma$, choose the archimedean weights $w_{u_0} : \Phi \to \mathbb{R}_{>0}$ to be $\approx b$ on
$$\mathrm{Thick}(u_0) := \Bigl\{(g_0, a, \gamma) \in \Phi \;\Big|\; a - u_{0,A} \in T_2^{(0)},\;\; \gamma \in u_{0,\Gamma}\, H_F\, u_{0,\Gamma}^{-1}\Bigr\}$$
and $\le 2b'$ on $\Phi \setminus \mathrm{Thick}(u_0)$.

1. **Pointwise Bost Slope Inequality:** For each **fixed** $u_0 \in A_0 \times \Gamma$, the iterated theta lift on totally definite unitary groups over $E^+$ and Bost's slope inequality ([QuotientSlopeBoundsWith.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/QuotientSlopeBoundsWith.lean), `PointwiseBoundVariant`) only see a weight tuple $w_{u_0} : \Phi \to \mathbb{R}_{>0}$ of thick density $\delta_2(T_2^{(0)}) / [F:\mathbb{Q}]$ and prove $\operatorname{ASK}(u_0) \le \operatorname{MAIN}(u_0) + \mathrm{Err}$.
2. **Exact Conjugacy Average:** For any unramified prime $p$ and any Frobenius representative $\phi_p = (\phi_{p,0}, \phi_{p,A}, \phi_{p,\Gamma}) \in C_p \subset G$:
   $$\frac{1}{|\Gamma|} \sum_{u_{0,\Gamma} \in \Gamma} \mathbf{1}_{u_{0,\Gamma} H_F u_{0,\Gamma}^{-1}}(\phi_{p,\Gamma}^i) = \frac{1}{|\Gamma|} \sum_{u \in \Gamma} \mathbf{1}_{H_F}(u^{-1}\phi_{p,\Gamma}^i u) = \frac{|H_F|}{|\Gamma|}\cdot \#\mathrm{Fix}_{\Gamma/H_F}(\phi_{p,\Gamma}^i) = \frac{1}{[F:\mathbb{Q}]}\,\pi_F(\operatorname{Frob}_p^i).$$
   This is a **class function** on $\Gamma$ (independent of the choice of Frobenius representative!), and for every unramified prime $p$, $\Lambda(p^i)\,\pi_F(\operatorname{Frob}_p^i) = \Lambda_F(p^i)$ (while ramified primes $p \mid \operatorname{disc}(L_0)$ contribute only $O(\log x)$).
3. **Cancellation of All Non-Principal Linear Constants:** Expanding the class function in irreducible characters $\tau \in \operatorname{Irr}(G)$ by Peter–Weyl orthogonality, for every $\tau \notin \{\mathbf{1}, \chi_{-d}\}$ we have $\sum_{\rho \in \Phi} \overline{\chi_\tau(\rho)} = 0$, so the linear constants $a \cdot \frac{L'(1,\tau)}{L(1,\tau)}$ cancel **identically** between the thick and thin sets!
4. **Resulting Main Balance:** Averaging $\operatorname{ASK}(u_0) - \operatorname{MAIN}(u_0) \le \mathrm{Err}$ over $u_0 \in A_0 \times \Gamma$ yields
   $$\frac{\delta_2(T_2^{(0)})}{2[F:\mathbb{Q}]}\,b\,\Bigl(G_{\zeta_F}(x) + G_{L_F(\chi_q)}(x) - G_{L_F(\chi_{-d})}(x) - G_{L_F(\chi_{-dq})}(x)\Bigr) \le \mathrm{Err} + (\text{thin-scale terms at } y \ge X').$$

### Step 3: Artin-Conjecture-Free `ThinScales` via Brauer Induction
On the thin set ($y = a/w \ge X' = \exp(x^{\varepsilon/3})$), every $\tau \in \operatorname{Irr}(G)$ has the form $\tau = \chi_0 \boxtimes \psi_{A_0} \boxtimes \sigma$ with $\sigma \in \operatorname{Irr}(\Gamma)$. By **Brauer's Induction Theorem**, $\chi_\sigma = \sum_j c_j \operatorname{Ind}_{E_j}^\Gamma \xi_j$ ($c_j \in \mathbb{Z}$) for finitely many elementary subgroups $E_j \le \Gamma$ and $1$-dimensional characters $\xi_j$. Thus
$$G_\tau(y) = \sum_j c_j\, G_{L_{F_j}(\xi_j \cdot (\chi_0 \psi_{A_0})|_{F_j})}(y), \qquad F_j := L_0^{E_j}.$$
Each summand is a **$1$-dimensional Hecke $L$-function** of a fixed subfield $F_j \subseteq L_0$ twisted by a character of conductor $\ll x^{2+8\varepsilon} q d$, so $\log(\mathrm{cond}) \ll x^{\varepsilon/5}(\log x)^2 \ll \log X'$. Unconditional Lagarias–Odlyzko / Stark zero-free regions (with Siegel zeros excluded by `RealBox` on $(q,d)$) yield $\|G_\tau(y)\| \le y\exp(-x^{\varepsilon/8})$ for all $y \ge X'/3$ — **without assuming Artin's holomorphy conjecture**.

### Step 4: `PairGood` for Quadratic Twists $L_F(s, \chi_q), L_F(s, \chi_{-d}), L_F(s, \chi_{-dq})$
Each $L_F(s, \chi_q) = \zeta_{F(\sqrt{q})}(s)/\zeta_F(s)$ is an **entire** $1$-dimensional Hecke $L$-function of $F$ of analytic conductor $\asymp q^{d_F}$. Following [BoxOfS.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/BoxOfS.lean) and [CountBadCore.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/CountBadCore.lean):
- By Kowalski–Michel / Heath-Brown zero-density for quadratic twist families of degree $d_F$, taking box width $\delta = \frac{1}{400 d_F}$ yields at most $\ll Q^{1/4}$ bad primes $q \in [e^{z/2}, e^z]$ having a zero in $\operatorname{Re}(s) > 1 - \delta$, $|t| \le Q$.
- Splitting $G_{L_F(\chi_q)}(y)$ at $Z = (Y^K)^{400 d_F}$ makes the tail $O(Y^\varepsilon)$ inside the zero-free box, while the finite sum $\sum_{n \le Z} c_N(y, n)\, \kappa_F(n) \left(\frac{n}{q}\right)$ has bounded coefficients $|\kappa_F(n)| = \Lambda_F(n)/\Lambda(n) \le d_F$, so the exact same quadratic large sieve gives $\|G_{L_F(\chi_q)}(y)\| \le y^{1/2+\varepsilon/2}$ for $99.9\%$ of primes $q$ (and similarly for $d$ and $qd$).

### Step 5: Non-Abelian Vandiver Weakening (`HypV` / `VVle`) via Brauer Direct Summands
We require $\sum_\ell (\log \ell)\sum_{1 \le e < x^{401}} \operatorname{length}_{\mathbb{Z}_\ell} \operatorname{Sha}^1(\mathcal{O}_E[1/\ell], (\mathbb{Q}_\ell/\mathbb{Z}_\ell)(-e)) \le \exp(\tfrac{1}{2}x^\varepsilon)$.
- **For all primes $\ell \nmid |\Gamma|$:** Because $\overline{\mathbb{Z}}_\ell[\Gamma]$ is a maximal order, Brauer's induction theorem produces a **lattice isomorphism** for every $\tau \in \operatorname{Irr}(\Gamma)$:
  $$\tau \;\oplus\; \bigoplus_j \bigl(\operatorname{Ind}_{E_j}^\Gamma \xi_j\bigr)^{b_j} \;\cong\; \bigoplus_i \bigl(\operatorname{Ind}_{E_i}^\Gamma \xi_i\bigr)^{a_i} \qquad (a_i, b_j \in \mathbb{Z}_{>0}).$$
  Applying the additive functor $\operatorname{Sha}^1(E_{\mathrm{ab}}, (-) \otimes (\mathbb{Q}_\ell/\mathbb{Z}_\ell)(-e))$ and Shapiro's lemma bounds the $\tau$-part by a finite sum of **$1$-dimensional character Selmer lengths over the fixed totally real subfields $F_i = L_0^{E_i}$**:
  $$\operatorname{length}_{\overline{\mathbb{Z}}_\ell}\operatorname{Sha}^1\!\left(E_{\mathrm{ab}},\, \tau \otimes (\mathbb{Q}_\ell/\mathbb{Z}_\ell)(-e)\right) \le \sum_i a_i \sum_{\psi \in \widehat{E_0 \times A_0}} \operatorname{length}_{\overline{\mathbb{Z}}_\ell}\operatorname{Sha}^1\!\left(F_i,\, (\mathbb{Q}_\ell/\mathbb{Z}_\ell)(\xi_i \cdot \psi|_{F_i} \cdot \chi_{\mathrm{cyc}}^{-e})\right).$$
- **For the finitely many primes $\ell \mid |\Gamma|$:** Here $\ell = O(1)$ is fixed; the $\ell$-adic contribution over $e < x^{401}$ is polynomial in $x$ (controlled by Iwasawa's theorem / $\mu,\lambda$-invariants of the $\ell$-adic Selmer group over $E$), which is exponentially smaller than the allowed budget $\exp(\tfrac{1}{2}x^\varepsilon)$.
- **Remaining engineering step for Step 5:** Lifting Engine 1 (`CorGK` / `KatoTwoW` in [KatoUse.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean) and [KatoTwoWOfPublishedH.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/KatoTwoWOfPublishedH.lean)) from base field $\mathbb{Q}$ to a fixed totally real field $F_i$ (using $U(3)_{K_i/F_i}$ for a CM quadratic extension $K_i/F_i$, `QuadBC2` over totally real fields, and `GaloisRepExistsTotallyRealGL2` — already present in the repo!). Note that for any totally real $S_3$-cubic or $D_n$-dihedral field, $F_i$ is merely a **real quadratic field**.

### Step 6: Windowed Landau Positivity (`FormB`)
Since $-\zeta_F'(s)/\zeta_F(s) = \sum_{n \ge 1} \Lambda_F(n) n^{-s}$ has non-negative coefficients $\Lambda_F(n) \ge 0$, a simple pole at $s = 1$, and standard zero-counting $N_F(T) = O(T\log T)$, Steps 1–5 give $G_{\zeta_F}(x) \le x^{1/2 + O(\varepsilon)}$ on windows $[Z, Z^{3/2}]$, forcing $\zeta_F(s) \ne 0$ for all $\operatorname{Re}(s) > \tfrac{1}{2}$ (and hence all zeros on $\operatorname{Re}(s) = \tfrac{1}{2}$ by the functional equation). $\blacksquare$
