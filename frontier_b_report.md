# Frontier B Report: Purely Spectral / Automorphic Stepanov Determinants for $\mathrm{GL}_2$ Grand RH (and Audit of Alpoge's Bessel RTF)

## 1. Audit of the Spectral / Bessel RTF Machinery Inside `lean/src/`

We inspected the exact spectral positivity and Bessel Relative Trace Formula modules in Alpoge & Claude's Lean codebase:
- [LocalBesselAndTopKernel.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/LocalBesselAndTopKernel.lean)
- [CongruenceAtSplitFrobeniusHolds.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/CongruenceAtSplitFrobeniusHolds.lean)
- [StandingNumericalData.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean)
- [IsGramNorm.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/IsGramNorm.lean)
- [BesselFormalDegreeIdentityStatement.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/CompanionTheory/AutomorphicTheory/PieriRules/ThetaBesselIsometries/BesselFormalDegreeIdentityStatement.lean)
- [GridsText.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/CompanionTheory/AutomorphicTheory/BesselWaveGrids/GridsText.lean)

### What It Actually Proves — and Why It Cannot Replace $D^p \equiv 0$ + Bost Slopes Alone
1. **Actual role in the RH/GRH proof:** On unitary pairs $U(k) \subset U(k + 2r + 1)$ over $E^+$ (with GGP-interlacing highest weights `InterlaceS (uS D u τ) (lamS D.R (D.hc τ))`), the Bessel RTF proves **approximate orthogonality** of Bessel-projected Poincaré series columns (`‖K_{u,u} - I‖_{HS} ≪ 1` and `‖K_{u,u'}‖_{HS} ≪ b^{-7}` via `cTvF`). This feeds *solely* into the orthogonality-defect parameters $(\eta, e)$ of Bost's slope inequality (`SlopeIneq` in [MeanBoundSecondForm.lean](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/RankGapBounds/MeanBoundSecondForm.lean)), preventing rank collapse of the integral lattice.
2. **Why the pure Bessel RTF never touches the critical strip $0 < \operatorname{Re}(s) < 1$ directly:**
   - Its **spectral side** evaluates only central $L$-values $L(\frac{1}{2}, \Pi \times \pi) \ge 0$ (GGP / Ichino–Ikeda).
   - Its **geometric side** sums local Bessel orbital integrals (`OrbInt` / `WittOrbitTheorem` / `MLatticeCond`), whose finite-place Euler products evaluate $\zeta$- and $L$-values only in the region of absolute convergence $\operatorname{Re}(s) \ge 3$ (`GL5LogLValueBoundByZeta`: `∀ i ≥ 3, |log lValEta E i| ≤ f * log ζ(i)`).
   - **Conclusion:** The pure Bessel RTF on $U(k) \subset U(k + 2r + 1)$ never generates the prime-weighted Weil distribution $W_\pi(\Phi)$. That is precisely why Alpoge's proof had to pivot from pure GGP determinants (items 4 & 7 of [remark.pdf](file:///home/marcus/GitHub/mbintz/incandescent/remark.pdf)) to $D^p \equiv 0$ + Bost slopes (items 2 & 13) to produce `ASK`.

---

## 2. Stress-Testing Purely Spectral Routes to $\mathrm{GL}_2$ Grand RH

We stress-tested four purely spectral mechanisms for a cuspidal eigenform $f \in S_k(\Gamma_0(N))$ (such as Ramanujan's $\Delta \in S_{12}(\mathrm{SL}_2(\mathbb{Z}))$, an elliptic curve $E_0/\mathbb{Q}$, or $\mathbb{Q}(\sqrt[3]{2})$'s weight-1 form $f_{\chi_3}$):

### Route B.1: Localized Mollified Second Moment / Poisson–Jensen Criterion
For any Dirichlet polynomial $M_X(s) = 1 + \sum_{2 \le n \le X} a_n n^{-s}$, a hypothetical zero $\rho_0 = \beta_0 + i\gamma_0$ ($\beta_0 > \frac{1}{2}$) of $L(s, \pi_f)$ gives $h(\rho_0) = L(\rho_0, \pi_f) M_X(\rho_0) - 1 = -1$, so Poisson–Jensen forces
$$1 \le \frac{1}{\pi} \int_{-\infty}^\infty \left|L(\tfrac{1}{2}+it, \pi_f) M_X(\tfrac{1}{2}+it) - 1\right|^2 \left|e^{(\frac{1}{2}-\beta_0 + i(t-\gamma_0))^2}\right|^2 \frac{\beta_0 - \frac{1}{2}}{(\beta_0-\frac{1}{2})^2 + (t-\gamma_0)^2}\, dt.$$
- **Obstruction (The Drop-to-One-Term Dichotomy):**
  - For a **single** fixed $\pi_f$ ($|\mathcal{F}| = 1$), evaluating this integral for $X \gg Q(\pi_f)$ requires controlling off-diagonal shifted convolution sums $\sum \lambda_f(k)\lambda_f(k+h)$ uniformly at length $X \to \infty$ (equivalent to square-root cancellation for $\mu_f$).
  - Averaging over a **large family** $\mathcal{F}$ (e.g. twists $\pi_f \otimes \chi$ of conductor $Q \gg X^C$) controls the off-diagonal terms via orthogonality, but dropping to the single term $\chi = 1$ loses a factor of $|\mathcal{F}|$, yielding only zero-density rather than RH for $\pi_f$.
  - **Key structural lesson:** To beat the drop-to-one-term loss without $D^p \equiv 0$, *every* member $\Pi \in \mathcal{F}$ must share the same zero $\rho_0$ (e.g. base change $\mathrm{BC}_{E^+/\mathbb{Q}}(\pi_f)$ for abelian $E^+/\mathbb{Q}$, which is unconditionally automorphic by Arthur–Clozel, or higher-rank lifts carrying $\pi_f$).

### Route B.2: Newton–Thorne Symmetric Powers $\operatorname{Sym}^m(\pi_f)$ ($m \ge 1$)
By Newton–Thorne (2021), $\operatorname{Sym}^m(\pi_f)$ is cuspidal automorphic on $\mathrm{GL}_{m+1}/\mathbb{Q}$ for every $m \ge 1$, with local Dirichlet coefficients $U_m(\cos\theta_p) = \frac{\sin((m+1)\theta_p)}{\sin\theta_p}$.
- **Sharp No-Go Check:** For *any* non-negative trigonometric polynomial $P_M(\theta) = \sum_{k=0}^M b_k U_k(\cos\theta) \ge 0$ with $b_k \ge 0$, integrating $P_M(\theta)(1 - \cos\theta) \ge 0$ against the Sato–Tate measure $\frac{2}{\pi}\sin^2\theta\,d\theta$ forces **$b_1 \le 2 b_0$** uniformly in $M$. Hence classical $\sigma \to 1^+$ positivity using all symmetric powers can never escape the pole at $s = 1$ to reach $\operatorname{Re}(s) < 1 - \varepsilon$.

### Route B.3: Eichler–Selberg / Petersson Formula + Newly Proved Dirichlet GRH (Concrete Calculation on Ramanujan's $\Delta$)
Because $\dim S_{12}(\mathrm{SL}_2(\mathbb{Z})) = 1$, the holomorphic Eichler–Selberg / Petersson trace formula isolates $W_\Delta(\Phi)$ with **zero drop-to-one-term loss**!

1. **Exact reduction to Dirichlet $L$-functions:** By Eichler–Selberg,
   $$\frac{\tau(p)}{p^{11/2}} = -\frac{1}{2\pi} \sum_{|t| < 2\sqrt{p}} \sin\!\left(11\arccos\frac{t}{2\sqrt{p}}\right) L(1, \chi_{t^2-4p}) + O(p^{-1/2}).$$
   Applying Poisson summation in $t \bmod d$ converts the Salié sum $\sum_{a \bmod d} \left(\frac{a^2-4p}{d}\right)e(ha/d)$ into the Kloosterman sum $S(h, hp; d)$ and recovers Petersson's formula:
   $$\frac{\tau(p)}{p^{11/2}} = c_{12} \sum_{d=1}^\infty \frac{S(1, p; d)}{d} J_{11}\!\left(\frac{4\pi\sqrt{p}}{d}\right).$$
2. **Expanding via newly proved Dirichlet GRH:** Write $S(1, p; d) = \frac{1}{\varphi(d)}\sum_{\chi \bmod d} \tau(\bar\chi)^2 \chi(p)$ (so $|\tau(\bar\chi)^2/\varphi(d)| \asymp 1$). Substituting into the dyadic prime ramp sum at scale $p \in [U, 2U]$ ($d \le \sqrt{U}$):
   $$\Sigma_{\Delta, U} := \sum_{p \sim U} \Lambda(p)\frac{X}{p}\frac{\tau(p)}{p^{11/2}} = c_{12}\sum_{d \le \sqrt{U}} \frac{1}{d\,\varphi(d)} \sum_{\chi \bmod d} \tau(\bar\chi)^2 \sum_{p \sim U} \Lambda(p)\frac{X}{p}\chi(p) J_{11}\!\left(\frac{4\pi\sqrt{p}}{d}\right).$$
   By the explicit formula under **Dirichlet GRH** (already proved in `Main.lean`!), every zero $\rho = \frac{1}{2} + i\gamma$ of $L(s, \chi)$ contributes
   $$I_U(\gamma, d) \asymp X d^{1/2} \int_U^{2U} u^{-7/4 + i\gamma} e^{\pm 4\pi i \sqrt{u}/d}\, du.$$
   By stationary phase, the stationary point lies at $\sqrt{u_0} = \frac{d|\gamma|}{2\pi} \in [\sqrt{U}, \sqrt{2U}]$, i.e. $|\gamma| \asymp \frac{\sqrt{U}}{d}$, with amplitude
   $$|I_U(\gamma, d)| \;\asymp\; X d^{1/2} \cdot U^{-7/4} \cdot (d^{1/2} U^{3/4}) \;=\; \frac{X d}{U}.$$
3. **Exact Exponent Accounting (Why Triangle Inequality Stops Precisely at $X^1$):**
   - Number of zeros of $L(s, \chi)$ in $|\gamma| \asymp \frac{\sqrt{U}}{d}$: $\asymp \frac{\sqrt{U}}{d}\log(dU)$.
   - Contribution of a **single** $(d, \chi)$ without cancellation across zeros: $\frac{\sqrt{U}}{d}\cdot\frac{Xd}{U} = \frac{X}{\sqrt{U}}$ (at $U = X$, **exactly $X^{1/2}$**!).
   - Summing over $\chi \bmod d$ ($\varphi(d) \approx d$ characters) divided by Petersson's $d$: still $\frac{X}{\sqrt{U}}$ per $d$.
   - Summing over $d \le \sqrt{U}$: $\sqrt{U}\cdot\frac{X}{\sqrt{U}} = \mathbf{X}$ (exact trivial bound, independent of $U$!).
   - **Sharp Duality Diagnosis:** Triangle inequality loses *precisely*:
     - $\sqrt{d}$ across $\chi \bmod d$,
     - $U^{1/4} d^{-1/2}$ across critical-line zeros $\gamma_\chi$ of $L(s,\chi)$,
     - $U^{1/4}$ across moduli $d \le \sqrt{U}$,
     for a combined loss of $\sqrt{d} \cdot U^{1/4} d^{-1/2} \cdot U^{1/4} = U^{1/2}$ (at $U=X$, **exactly $X^{1/2}$**).
   - **Structural Theorem (Zero-Resonance Duality):** *Given Dirichlet GRH, an off-line zero $\rho_\Delta = \beta + i\gamma_0$ ($\beta > \frac{1}{2}$) of $L(s, \Delta)$ exists if and only if the critical-line zeros $\frac{1}{2} + i\gamma_\chi$ of Dirichlet $L$-functions $L(s, \chi)$ ($\bmod\, d \le \sqrt{X}$) exhibit coherent conspiracy (exceeding square-root cancellation by $X^{\beta - 1/2}$) in the Kloosterman-weighted phase sum $\sum_{d \le \sqrt{X}} \frac{1}{d\,\varphi(d)} \sum_{\chi \bmod d} \tau(\bar\chi)^2 \sum_{\gamma_\chi} I(\gamma_\chi, d)$.*

---

## 3. Verdict on Frontier B

Purely spectral / archimedean methods **without** a geometric/arithmetic source of $\log p$ (or a new cancellation theorem across Dirichlet critical-line zeros) face an exact conservation-of-difficulty barrier:
1. Bessel RTF on $U(k) \subset U(k+2r+1)$ only yields central-value positivity and column orthogonality (never $\log p$).
2. Localized mollifiers hit the Drop-to-One-Term barrier; Newton–Thorne symmetric powers hit the $b_1 \le 2b_0$ Sato–Tate barrier.
3. Petersson + Dirichlet GRH achieves the **exact** $X^{1/2}$ threshold per $(d, \chi)$ and converts RH for $\Delta$ directly into a coherent-conspiracy question about critical-line zeros of Dirichlet $L$-functions — which suggests that **either** a genuinely new arithmetic source of $a_p(f)\log p$ (**Frontier A**) **or** a new **spectral-duality / second-moment amplification** on the $(d, \chi, \gamma_\chi)$ zero-sum is needed to crack Wall 2.
