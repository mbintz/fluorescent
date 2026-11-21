# Structural Atlas (Level 2): Standalone Mathematical Engines & Open Pressure Points

*An emergent inventory distilled directly from the six agnostic Wave 1 field notes—no forced analogies, no GRH hype. Grouped organically by the actual mathematics that appeared in the Lean code.*

---

## Part I. Genuinely Standalone Mathematical Engines Inside the Proof

Each item below is a clean, self-contained mathematical mechanism or library proved outright in `lean/src/` that makes sense **completely independently of RH/GRH**.

### A. Algebraic, Spectral & Representation-Theoretic Engines

1. **Yangian `qdet` → Quantum-Comatrix Branching → Radial Bessel Eigenvalue** *(Cluster 2)*
   - **What it does:** From $\mathfrak{gl}_n$ matrix-unit commutators alone, builds `qminor` / `qdet` ($T_{ab}(u)=u\delta_{ab}+E_{ab}$), proves RTT, centrality, and highest-weight eigenvalue $\prod_j(u-j+\nu_j)$; uses the quantum comatrix identity (`QComatrix`) to decompose restrictions into simultaneous Capelli eigenspaces $\operatorname{CapSp}(E,m)$ indexed by shifting one $m_i$ by $1$; and turns the $(1,1)$ entry of a radial differential operator on a Bessel cell $G=|D_{r+1}|^2-T_z T_{z'}|D_r|^2$ into an explicit scalar $GG(g)x_\rho(Y)$ per component.
   - **Source:** `Formalism/RealPlaceAnalysis/StatementE.lean:9`, `HermitianCurvature/CapelliDeterminantAndBranching.lean:99`, `HermitianCurvature/StatementQ.lean:693`.

2. **$2\times 2$ Weyl-Relation RTT, Word Fusion & Scalar-Test Operator Separation** *(Cluster 2)*
   - **What it does:** For any algebra with $cc^{-1}=1$, $pc=cp+c$, $T(Y)=\bigl(\begin{smallmatrix}Y+p&-c\\c^{-1}&0\end{smallmatrix}\bigr)$ satisfies auxiliary-space RTT with $R(d)=dI-P$ and $T(Y+1)^t J T(Y)=J$. `WordFusion` composes commuting factor families multiplicatively; `RTTSandwich` expresses commutators of $(0,0)$ sandwiched entries via the middle RTT defect; `RTTIndependence` recovers all 16 vector-valued entries from scalar functional tests (for $Y'\ne Y+1$).
   - **Source:** `Formalism/YangianSpanCharacter/StatementT.lean:7`, `HermitianCurvature/StatementW.lean:20`, `PeriodIntegrals/RTTIndependence.lean:11`.

3. **Quantitative Archimedean $U(n+1)\supset U(n)$ Discrete-Series Branching (`RealInputE`)** *(Cluster 3)*
   - **What it does:** Proves an explicit quantitative Gan–Gross–Prasad-type local period identity for discrete series of $U(p,q)$ on $n+1$ and $n$ variables far from the walls (gaps $\ge 1000(n+1)^3$): existence of lowest-$K$-type vector $v_0$, element $g_0$ with $\|g_0\|\le (8(n+1)B)^{10(n+1)}$, explicit positive branching constant $c>0$, matrix-coefficient decay $|\langle v,\pi(g)v\rangle| \le A\|g\|^{-20(n+1)^2}$, and $L^1$ decay $\mathrm{colLen}^{-(2n+7)}$.
   - **Source:** `Development/AutomorphicArithmetic/ThetaCorrespondence/RealBands/BranchDefs.lean:11`, `FockModels/RealBranch.lean:231`.

4. **Lacunary Lie-Algebra Rank Extraction (`DivWCoreLac`)** *(Cluster 6)*
   - **What it does:** Given a continuous semisimple $N$-dimensional representation of a compact group, monic degree-$n$ annihilating polynomials on a dense set, matching determinant character, and **one** element in the Lie algebra of the Zariski closure with $n$ distinct **lacunary** eigenvalues (no two disjoint nonempty subsets have the same average!), extracts an actual $n$-dimensional semisimple subrepresentation $r$ (such that the original embeds in $r^{\oplus k}$) with exact characteristic polynomial on the separable dense locus.
   - **Source:** `Development/WeilBound/CoreStatements/PadicHodgeComparison/CocharacterLieDivisors/DivWCoreLacUseType.lean:86`, `Development/EtaleCohomology/DivisorCycles/GoalHolds.lean:19`.

5. **Two-Lift Disjoint Parity Subtraction & Adelic Theta Parseval (`TLiftK` / `PPeelOne`)** *(Cluster 6)*
   - **What it does:** Explicitly proves an adelic Parseval identity on a fundamental domain for rational pairs, lifts an even-rank automorphic representation to **two** odd-rank targets augmented by disjoint character lists $\psi_{1,i}, \psi_{2,j}$, and peels off the auxiliary lines one by one from semisimple Galois representations by comparing characteristic polynomials.
   - **Source:** `Foundations/GaloisRepresentations/ThetaParseval/ThetaKernels/ParsevalRationalPairing.lean:16`, `SplitLineSubtraction/PPeelOne.lean:13`.

6. **Integral Weyl-Quotient $\ell$-Exponent Bounds (`PieriBlockIdeals` & `GradedWeylDivisibility`)** *(Cluster 2)*
   - **What it does:** Explicitly bounds the power $\ell^J$ annihilating weight components of $\nabla_\nu / \Delta_\nu$ over $\mathbb{Z}_{(\ell)}$ via Pieri path spaces and content-product integers $D_i$—complete with a kernel-checked counterexample at $\ell=13$ (`eExp = 142 > 140`) showing why naive closed-form upper bounds fail.
   - **Source:** `Formalism/GradedWeylDivisibility/StatementA.lean:24`, `Formalism/PieriBlockIdeals/StatementLD.lean:15`, `ExponentBoundCounterexample.lean:393`.

---

### B. Analytic, Harmonic & Inequality Engines

7. **Localized Landau–Pintz Window Zero-Free Theorem (`formB` / `lemmaL`)** *(Cluster 1)*
   - **What it does:** One-sided upper bounds $\mathrm{Gm}(y) \le y^\theta$ on sparse multiplicative windows $[Y, Y^{1+\delta}]$ (for arbitrarily large $Y$, any $\delta>0$) already rule out zeros with $\operatorname{Re} s > \theta$ for any positive Dirichlet series combination—proved via localized Mellin–Taylor coefficients concentrated in $[U, (1+\delta)U]$.
   - **Source:** `Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean:20`.

8. **Huge-Conductor Auxiliary Twist Averaging + Coset Fourier Isolator** *(Cluster 1)*
   - **What it does:** Embeds a target cyclic character group $\langle\psi\rangle$ in an auxiliary abelian CM field twisted by two giant primes $q,d$ ($\log q \approx Y^{\varepsilon/5}$), turning RH-at-scale-$x$ for every unwanted character into a short-sum mean-square / large-sieve theorem (`pairEx`); pairs with a $3 + 1_{A_0}$ coset-weight distribution whose Fourier transform is $1 + (3o+1)^{-1}\sum_{\chi\ne 1}\chi$.
   - **Source:** `Development/AutomorphicArithmetic/MeanSquareBounds/pairEx.lean:112`, `Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean:135`.

9. **Multi-Step Tower Error Recursion (`SharpRecursion`)** *(Cluster 2)*
   - **What it does:** Pure real inequality: if $\sigma_i \le (1+\varepsilon)\sqrt{1+e_i}\sigma_{i-1} + \sum_{t=2}^i a^{t-1}\sigma_{i-t}$ with $(r+1)(\varepsilon+a)\le 1$ and $0\le a\le \tfrac{1}{2}$, then $\sigma_{r+1}^2 \le [1+80(r+1)(\varepsilon+a)]\prod_{i=1}^{r+1}(1+e_i)\,\sigma_0^2$.
   - **Source:** `Formalism/HermitianCurvature/HermitianCurvatureProofs/SharpRecursion.lean:157`.

10. **Hörmander $L^2$-$\bar\partial$, Sharp Skoda Division & Point Ohsawa–Takegoshi on Stein Riemann Domains** *(Cluster 5)*
    - **What it does:** Self-contained 227-file (33.7k-line) complex-analytic library built over Stein Riemann domains (`EtaleStein`), proving Hörmander's estimate, Skoda $L^2$ division with the sharp constant $t/(t-(p-1))$, Riemann extension across hypersurfaces, and a compact-manifold Ohsawa–Takegoshi $L^2$ extension from finite transversal zero sets by passing to an étale frame off a divisor (avoiding complete-Kähler base curvature completely!).
    - **Source:** `ReciprocityTheory/L2DbarEstimates/HormanderEstimate/Hormander.lean:13`, `JacobianInterpolationStatement.lean:20`, `Development/AbelianVarietyTheory/Proofs/DivisorProofs/L2ExtensionLogCanonical.lean:13`.

11. **Abstract Pure-Real Bost Slope Engine & Hermitian-Lattice `goodBadCut`** *(Clusters 1, 5)*
    - **What it does:** (a) Pure-real 11-hypothesis engine chaining `count ≤ gain ≤ slope ≤ degree` with entropy error; (b) `slope_good_ge`: for any orthogonal idempotent $e$ with $g e(L)\subseteq L$, $\operatorname{rk}(L\cap\ker e) \le 3\delta\operatorname{rk} L$ ($\delta\le 1/12$), and slope range $Q$, removing the bad direction costs at most $\mu(L\cap\operatorname{im}e) \ge \mu(L) - 12\delta Q$.
    - **Source:** `Formalism/RankGapBounds/MeanBoundSecondForm.lean:37`, `Development/AbelianVarietyTheory/Proofs/DivisorProofs/MajAtAddRight.lean:111`.

---

### C. Geometric, Arakelov & Arithmetic Engines

12. **Complete Functorial Characteristic-0 Resolution of Singularities & Principalization (Kollár's Route)** *(Cluster 5)*
    - **What it does:** 499 files / 140,709 lines, zero `sorry`: derivative ideals, D-balanced / MC-invariant / tuned ideals $W(I,m)$, maximal contact uniqueness, smooth- and field-extension-functorial principalization and strong resolution of singularities. Arguably the single largest standalone reusable formalization artifact in the entire repo.
    - **Source:** `Development/ResolutionOfSingularities/Statements.lean`, `EmbeddedResolution/HironakaTheorem.lean:69`.

13. **Torsion-Free Nef Arithmetic Hilbert–Samuel & Axiomatic BGS Heights** *(Cluster 5)*
    - **What it does:** Proves the full Moriwaki-strength nef arithmetic Hilbert–Samuel theorem ($\log\#\{\text{small sections of }L^m\otimes N\} = \frac{a}{(D+1)!}m^{D+1} + o(m^{D+1})$) and Moriwaki bigness using Minkowski lattice-point counting, Bergman-kernel bounds, and Fubini–Study comparison—completely bypassing analytic torsion and Bismut–Lebeau machinery!
    - **Source:** `GroundTheory/HeightsAndTheta/Heights/HilbertSamuel/`, `Development/AbelianVarietyTheory/Proofs/DivisorProofs/ArithHilbertSamuelOfPrincipalisation.lean:11`.

14. **Stuhler–Grayson Harder–Narasimhan Theory for Euclidean & Hermitian Lattices** *(Cluster 3)*
    - **What it does:** General, Mathlib-shaped 43-file library establishing `muMax`, `muMin`, the HN polygon, degree supermodularity (`DegSupermod`), and variational slope characterizations (`MuChar`).
    - **Source:** `Formalism/HarderNarasimhan/Statement.lean:29`, `Formalism/LatticeSlopes/`.

15. **Prime-Uniform Single-Integer Trace Product & Cotangent-Length Inequality (`LemmaM`/`LemmaM'`)** *(Cluster 4)*
    - **What it does:** Bounds weight-$-1$ cotangent / Selmer lengths by $2\sum_\xi v_\ell(\xi(a))$ over a minimal deformation orbit cover, then converts bounded-trace automorphic families ($|t_s|\le 3$) into **one single nonzero rational integer** $n = \prod_{s,z} Q^e(t_s - (Q^{-e}z+1+Q^e z^{-1})) \in \mathbb{Z}$ simultaneously controlling $\sum_{\ell\in S} v_\ell(n)\log\ell \le \log|n|$ across all primes $\ell$ at once!
    - **Source:** `AutomorphicVarieties/CommutativeAlgebra/OrbitVanishingLocal.lean:111`, `AutomorphicVarieties/BuildingsResidueChars/FrobeniusTraceNormNonzeroLogBound.lean:24`.

16. **Finite-Exception Quadratic Scale-Window Lemma (`Window.lean`)** *(Cluster 4)*
    - **What it does:** Elementary, completely portable pigeonhole induction: given at most $R$ bad indices in any scale regime, extracts a full quadratic interval $[Y, Y^2] \subset [X^{1/J}, X]$ ($J = 2^{R+2}(C_t/\eta)^R$) on which every bad index $\le x^{C_t}$ is already $\le x^\eta$.
    - **Source:** `AutomorphicVarieties/LayeredIsomorphisms/Window.lean:7`, `Window1.lean:20`.

17. **Genericity by Algebraic Finiteness (`large₂` / `EvLgG` / `GKeyFin`)** *(Cluster 3)*
    - **What it does:** Clean formal framework for carrying properties across arbitrarily large coefficient fields outside finite algebraic exceptional sets + finite avoided prime sets, with monotonic parameter strengthening (`open_and_linked_of_stronger_extension`).
    - **Source:** `Definitions/AutomorphicMembership/CmQuadraticFormEqAlternatingForm.lean:100`, `GKeyFin.lean:30`.

18. **Integral $p$-adic Hodge Library + Weakened LLC Counting Converse** *(Clusters 3, 5, 6)*
    - **What it does:** Breuil–Kisin modules, $A_{\inf}$, prismatic Dieudonné, Wach modules, Herr complexes, Grothendieck–Messing, Fargues Hodge–Tate, Zarhin's trick, plus the clever finite counting converse (`CharPolOfInert.lean:114`) showing how a dummy separated wild parameter can still force every tame parameter back into the controlled depth-zero sector.

---

## Part II. Pressure Points, Fragile Joints & Potential Wave 2 Targets

Across all 6 independent scouts, a consistent set of **real mathematical pressure points** emerged—places where the proof is tightest, heaviest, most ad hoc, or least audited so far:

1. **The Three Unopened Inner Engines of `plugAll` (Cluster 1 leads):**
   - **`LinkG` (`linkG_concrete5` / `stLoss7`):** How inert-prime counts are actually converted into slope gain with loss $\le c\,n_T m b x^{e_L\varepsilon}$ at rank $k \approx x^{9/2}$.
   - **`LinkDIV` (`bRest_all` / `linkDIVt_closedK` / `BridgeRowsK`):** Where the degree upper bound comes from and how it meets `CovolX`'s `L3`.
   - **`LinkS` (`theoremS_transport_link_zero` / `frameF_of`):** How near-orthonormality of Gram matrices ($\eta_0, \eta_1, \sqrt{e_0} \le e^{-x^{\varepsilon/8}}$) is proved uniformly at rank $k \approx x^{9/2}$ (linking Cluster 1 directly to Cluster 2's Yangian/Bessel/curvature machinery!).
2. **The `ThirdPlaceSeries/HypsAlt` Live-Path Audit (Cluster 3 ↔ Cluster 6 lead):**
   - `EveryCharacterE.lean` (`hypsE₂`) is unused; the live proof runs through `ThirdPlaceSeries/` (`HypsAlt`), swapping `LocalLanglandsGL` → `RecTExists` and `CovolX` → `CovolumeBoundOfX`. Worth verifying the exact diff between `Hyps` and `HypsAlt` and how `RecTExists`'s dummy wild assignment interacts with every caller.
3. **The $O(b) = O(e^{x^\varepsilon})$ Deep-Cover Loss & Exponential Bad-Locus Requirement (Cluster 5):**
   - `RingAt` / `MapsAt` lose $O(b)$ passing to level-$15^e$ covers ($e \approx 3x^\varepsilon/\log 3$), forcing the entire proof to operate at exponential height $a = x e^{x^\varepsilon}$ and demanding bad rank fraction $\le 3 e^{-x^{\varepsilon/(7J)}}$. Any polynomial-scale improvement to `RingAt`/`MapsAt` would reshape the whole scale budget.
4. **Deformation-Orbit Cover Interface in `VWin` (Cluster 4):**
   - The sharpest joint in `VWin` is where the finite deformation family covers the points, avoids double-counting conjugates, keeps every trace difference nonzero, and injects into a Galois-stable trace family (`GaloisRepIneqOfAllIrreducibleNonvanishing.lean:158`). Also note `CountVOf` ignores `e = 1` and `ℓ ∈ B_χ` inside its proof—suggesting a stronger general high-conductor estimate already sits in the code!
5. **The `D7` / `Moduli` Non-Vacuity & Realization Seams (Clusters 1, 2, 5):**
   - `Moduli D l` is a hypothesis structure for unitary Shimura varieties (only Siegel $\mathcal{A}_{g,n}$ asserts existence via `SFam`), `LitThin` quantifies over a dummy `D : D7`, and Cluster 2 flagged the exact identification equalities (`TieIo`, `TieBm`, Haar density, intermediate $Y_j$ signature) as the key algebraic-to-analytic handoffs.
6. **Huge Unopened Sub-Cones Inside `Open0` (Cluster 3 lead):**
   - `diagonalRow_of_siegelWeil_unitary` (5,799 files) and `geometric_zero_condition_all` (12,049 files) are the two largest internal engines of `Open0` not yet opened in detail.
