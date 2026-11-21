# Field Notes, Cluster 5: `CovolX` — Arakelov covolume, Hodge-bundle heights, L²-∂̄, resolution

*Read-only reconnaissance. I could not compile anything. Every claim below comes from reading the Lean source. "No `sorry`" means a text grep found none.*

---

## 0. Executive summary

1. **`CovolX` is not a volume bound for a Shimura variety.** It is a **lower bound on the Arakelov degree** (equivalently, an upper bound on the log-covolume) of a family of Hermitian 𝒪_K-lattices `M_j`, one for each lift level j = 1..m. Its main term is a **Hodge-weighted CM period** `logΩ = γ + log(π/v) − L'(1,χ_{−d})/L(1,χ_{−d})`. Its error term is `C · f·m·x^ε·e^{x^ε}·log log x`, which is huge.
2. **The proof has three layers.**
   - (A) A pure Hermitian-lattice "good/bad cut" lemma at the base point.
   - (B) Slope lower bounds proved on deep-level covers of unitary Shimura varieties, using an effective arithmetic Hilbert–Samuel inequality plus component-height lower bounds.
   - (C) Those height lower bounds come from `DeepStR`, an averaged arithmetic-volume bound, and the CM period enters through flat line bundles.
3. **Nothing in this cone depends on the open-literature parameter `O`.** All 15 inputs, and all 28 fields of `PublishedHodgeBundleTheorems`, are discharged by internally proved theorems. I checked every wrapper.
4. **Resolution of singularities is real and textbook-scale: 499 files but 140,709 lines.** It follows Kollár's *Lectures on Resolution* architecture (D-balanced, MC-invariant and tuned ideals; maximal contact; functorial principalization; affine embedding; gluing). It proves a smooth- and field-extension-functorial resolution rule.
5. **L²-∂̄ uses a clever reduction.** Everything is done on **Riemann domains spread over ℂⁿ** (`EtaleStein`). The L² extension theorem only extends from a **finite set of points**, and compact manifolds are reduced to the étale case by removing a divisor.
6. **Arithmetic Hilbert–Samuel avoids analytic torsion entirely.** It uses Minkowski lattice-point counting, Bergman-kernel bounds, Fubini–Study approximation, and an ample-to-nef step.

---

## 1. What exactly is `CovolX` / `CovolumeBoundOfX`?

### 1.1 The Lean definition

`lean/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LiftLambdaBound.lean:60`
```lean
def CovolumeBoundOfX : Prop := Closed FamHyp fun Fm CH =>
  ∃ C0 : ℝ, 0 ≤ C0 ∧ EventuallyAtAllPoints Fm fun _ _ _ p => ∀ C, C0 ≤ C → (p.S false).L3 (p.N C CH)
```
The sibling `CovolX` (`lean/src/Development/AbelianVarietyTheory/Definitions/Divisors/CovolXOfCovol.lean:278`) is identical, except that it uses `EvTied`, whose point filter is `RowsT = p.Rows ∧ RecTied`. `CovolumeBoundOfX` uses `RowsTAlt = p.PointConditions' ∧ RecTied` (`LiftLambdaBound.lean:17`). `CovolX.covol` (`CovolXOfCovol.lean:281`) turns it into the base `Covol` (`TupleReadBaseTupleEqFamily.lean:525`), provided `RecTied` holds eventually.

Unwinding each layer:

| Lean piece | Meaning | Source |
|---|---|---|
| `Closed 𝒞 P` | ∃ε₁>0 ∀ε∈(0,ε₁] ∃ constants `K : TransportedAlt` ∀ families `Fm : FamP ε` with `𝒞 Fm` and `Fm.Large K CH`: `P Fm CH` (uniformity over families) | `Formalism/SharpRestriction/ParamsHeightRankConstant.lean:159` |
| `FamHyp` | 14 conjuncts: `PageFix, PageWin, SmallFirstModulusBelowScale, TameDistinctF, ChosenWall, DGam ∣ minkM(…), BoxesF, QDRowsF, CYL ≤ 9, DGamSmooth, TwGood, ChosenE, TuSize, DGamSize` | `TupleReadBaseTupleEqFamily.lean:503` |
| `FamP ε` | for each scale x > x₁ and index ι ∈ Ix x: a datum `D x ι : D7`, size data `L x ι` with `L.sc.x = x`, `sc.eps = ε`; places of residue characteristic ≤ X''(n) lie in the support | `Formalism/SharpRestriction/ParConsts.lean` (`structure FamP`) |
| `Pt Fm x hx ι` | `PtAt (Fm.ex x hx ι) Fm.Csz`: a ~60-field bundle (Hecke row-side family `P`, core Shimura datum `T : CoreJ D`, real data `R`, weights `κ i`, frame ties `fw`, …) | `TupleReadBaseTupleEqFamily.lean:145, 501` |
| `p.S false` | an `IndefData` over the totally complex field K = `D.what₂.LL` | `TupleReadBaseTupleEqFamily.lean:290` |
| `S.L3 N` | `∀ j, lcv (S.XW j) (S.M j) / S.D ≤ N.l3 j` | `Formalism/LocalToGlobal/IndefiniteForms/IndefSide.lean:315` |
| `p.N C CH` | `IndefScale.num`, with `l3 j = l3m j + C · l3u` | `IndefSide.lean:224–228` |
| `l3m j` | `∑_{ρ∈Bool×A} ((k + j − 1) − (m − j)) · w_j(ρ) · logOm` | `Formalism/LocalToGlobal/Divisibility/ZscOfNum.lean:64` |
| `l3u` | `B0 · log(log x)` | `ZscOfNum.lean:66`; `NumericScaleExponentEqExtended.lean` (`ZscOfNum3_units`) |
| `B0` | `f · m · b · x^ε` | `Formalism/LocalToGlobal/Divisibility/Numbers.lean:74` |
| `b` | `exp(x^ε)` (and `L = x^ε`) | `Formalism/LocalRingCardinality/DataParams₂.lean:27–29` |
| `logOm` | `γ + log(π/v) − L'(1,χ_d)/L(1,χ_d)`, with χ_d the quadratic character mod the prime d | `Numbers.lean:64–68` |
| `w_j(ρ)` | the rational number `(hc ρ).e (j−1)`, a component of a Harish-Chandra parameter | `Numbers.lean:160–163` |
| `lcv X M` | `(2/[K:ℚ]) · log(2^{n_∞·rk} · \|d_K\|^{−rk/2} · covol(M, X))` | `Formalism/QuotientMetricDivisors/Statement.lean:34`; `Formalism/HarderNarasimhan/StatementPl.lean:29` |

### 1.2 The statement in standard notation

Fix ε small and constants K. Take any family of data satisfying `FamHyp` and the largeness conditions. Then there is a C₀ (uniform over the family) such that, for every scale x ≫ 1, every index ι, every point p meeting the row and tie conditions, every C ≥ C₀ and every lift level 1 ≤ j ≤ m:

$$
-\frac{2}{[K:\mathbb Q]}\,\frac{\widehat{\deg}(\overline{M}_j)}{D_S}+\frac{\mathrm{rk}\,M_j\log 2}{D_S}
\;\le\;
\underbrace{\sum_{\rho\in\{\pm\}\times A}\big((k+j-1)-(m-j)\big)\,w_j(\rho)\,\log\Omega}_{\text{Hodge weight}\times\text{CM period}}
\;+\;C\, f\, m\, x^{\varepsilon} e^{x^{\varepsilon}}\log\log x .
$$

Here:
- K is a totally complex field, and `M_j ⊂ K^{d_W(j)}` is the 𝒪_K-lattice of integral lifts, with a Hermitian metric `XW_j(v)` at each infinite place.
- `MeasAt` (`CovolXOfCovol.lean:81`) shows that the metric is a Petersson norm on cusp forms, up to a constant `c` with `|log c| ≤ C·unitE`.
- The weights `(k + j − 1) − (m − j)` are the Hodge-bundle weights of the level-j lift.

**Dependence on parameters:**
- **Linear** in the Hodge weights, through a single CM period `logΩ` (an L'/L(1) value for the imaginary quadratic host).
- **Error** linear in `f = 2·ord` and in `m`, but of size **e^{x^ε}** in the scale x.
- **No explicit dependence on the conductor**: field size enters only through `RecTied.core_size_le`, `fieldSz ≤ 217·zBase²` (`CovolXOfCovol.lean`, after line 161).

**Interpretation.** "Integral theta-lift lattices have Arakelov slope at least −(Hodge weight)·h_CM, up to an O(b)-sized error." `AnchorAt` (`CovolXOfCovol.lean:98`) cross-checks the main term: `|mainT − Σ_τ (p−q)·anchor_τ·logΩ| ≤ C·unitE`.

---

## 2. Proof architecture

### 2.1 Top call graph

`ThirdPlaceSeries/TopCovolSlim2Use.lean:16–22` takes 15 hypotheses and assembles four packages:

```
hX : HypothesesX := ⟨ToroidalForFanKS, SemiAbelianLieSeminegative,
                     green_of_regular greenRegularCharacters_holds,
                     PointSeparationPair, fubiniStudy_chowHeight_formula hP⟩
hF := toroidalChartsForFan_of hK
hH : HypothesesH := ⟨SiegelToroidalIntegral, hF, toroidalCharts_of_siegel_of_forFan, ArDegree⟩
VolumeEstimateHypotheses := ⟨chow_form_height_comparison,
                             small_sections_injective (exists_nonvanishing_of_toroidal …)⟩
Quoted := ⟨KawamataViehweg, L2ExtensionLogCanonical, SerreGAGA, NefNumerics,
           ChowFormExists, ChowFormIntExists, ChowFormHyperplaneSection, ProperIntersectionLength⟩
DeepStR := deep_slim_use Resolution Principalisation PoincaréLelongInv HSUse MoriwakiBig
                         FarguesExact Zarhin NefRR
→ topCovolG_alt_alt
```
(`Quoted` is defined at `Development/AbelianVarietyTheory/Definitions/Divisors/WellChosen.lean:22`. The two `VolumeEstimateHypotheses` components are at `HodgeBundleWeights/VolumeEstimateHypotheses.lean:9–11`.)

`ThirdPlaceSeries/TopCovolG.lean:39–58` is the real skeleton. It derives about 20 named `…Condition` predicates and closes with `covolX_of_truncation_badSet_lambda_lowBound`. Every `…Statement.lean` file in `ThirdPlaceSeries` is a one-line `first | exact …` re-export, for example `CovolXOfStepsStatement.lean:12` and `LowOfCoverHypothesesStatement.lean:12`.

### 2.2 Layer A: the base-point lattice inequality (`lcv_le`)

`lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/CovolumeFromGramAndBounds.lean:39–84` proves a four-step chain. Write E = `unitE p = l3u` and μ = `slope_sq`, where `muDef = 2·slope − log 2 + log|d_K|/[K:ℚ]`.

$$
\tfrac{\mathrm{lcv}(M_j)}{D}
\overset{\texttt{RecAt}}{\le} -\mu(L_{\rm good})
\overset{\texttt{slope\_good\_ge}}{\le} -\mu(L_{\rm type}) + 12\delta Q
\overset{\texttt{CoreAt}}{\le} -\mu_{\rm core} + C_1E + 12\delta Q
\overset{\texttt{LowAt}}{\le} \text{mainT} + (C_1+C_2)E + 12\delta Q,
$$

with δ = e^{−x^{ez/7}}, ez = ε/J, and Q = (x^A + x^B + C₁ + C₂ + 1)·E. Finally `exists_loss_le` (`:25`) gives 12δ(x^A + x^B + C) ≤ 1 for x ≥ x₀, so the δ-term is at most E.

The predicates are in `CovolXOfCovol.lean`: `GramAt :53`, `RecAt :57`, `CutAt :61`, `BadAt :69`, `LamAt :73`, `SizeAt :75`, `CoreAt :92`, `LowAt :96`.

**The engine `slope_good_ge`** (`lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MajAtAddRight.lean:111`) is a standalone theorem about Hermitian lattices over any totally complex number field. Assume:
- e is an idempotent that is orthogonal at every place (Pythagoras holds);
- g·e(L) ⊆ L;
- rk(L ∩ ker e) ≤ 3δ·rk L, with δ ≤ 1/12;
- μ_max(M) ≤ Q, μ(L) ≥ −Q, and 2·log g ≤ Q.

Then **μ(L ∩ im e) ≥ μ(L) − 12δQ.** In words: removing an exponentially thin bad direction costs at most δ times the slope range. It goes through `Formalism.ExtensionFiltration.goodBadCut`. `CutAt` supplies exactly these hypotheses, with g = |Gp| and 2·log|Gp| ≤ b.

### 2.3 Layer B: the lower bound `LowAt` via deep covers

`LowAt` says −mainT − C·E ≤ μ_core, where μ_core is the slope of the integral cusp-form lattice of the core weight on the base unitary Shimura variety (`muCore`, `CovolXOfCovol.lean:51`). It is the deepest input. It is proved on deep covers `Y : Deep T j`, defined at `lean/src/Development/AbelianVarietyTheory/Definitions/Divisors/NormNegCmConstantEqAtAllEmbeddings.lean:162`. Each such Y carries:
- a higher-level unitary Shimura variety `Xo₂`, with level `pd = 15^e` and e = ⌊3L/log 3⌋ (`expL`);
- a coefficient field c₂ with `fieldSz ≤ o`;
- uniformizations at every complex embedding and an open compact `Kf`;
- per-component invariants: height `ht`, degree `dg`, Arakelov degree `degC`, rank `rkC`, and slope `mu`.

The `LowCover.low_of_cover_hypotheses` chain (`TopCovolG.lean:57`) combines these steps (all predicates in `CovolXOfCovol.lean`):

| Step | Inequality | Role |
|---|---|---|
| `RingAt :116` | μ(latDeep) − 2b ≤ μ_core | the deep-cover lattice and the base lattice agree up to O(b) |
| `MapsAt :119`, `RkAt :125` | n maps φ_h: V_{G_s(−c₀)} → V_{G_k}, jointly injective, ‖φ‖² ≤ e^{2b}, with rank control | Bost-type slope transfer by multiplying with carrying sections θ (`Carries`, `SemiposAtOfPositive.lean`) |
| `GminAt :128` | latDeep is generated by vectors of norm ≤ e^{PP·κ} | successive-minima control |
| `FlatAt :135` | μ_Y(uM) − mainT − C·E ≤ μ_Y(G_s(−c₀)) | **the CM period enters here**: shifting the weight costs the flat degree |
| `UAt :138` | −C·E ≤ μ_Y(uM) | uniform slope lower bound on the cover |
| `SumAt :158` | 2·Σ degC / Σ rkC ≤ μ_Y(uM) | slope ≥ average of component degree/rank |
| `HSAt :153` | binT·dg·(lenT·ht − 3(d+1)\|ht\| − A·log(2+\|ht\|) − R) ≤ degC | **effective arithmetic Hilbert–Samuel**, with lenT = ⌈PP²·d²·k/m⌉ and binT = C(lenT − 1, d) |
| `HeightAt :146` | component heights ≥ −cs, and (1−ρ)·max(0, sl + cs) ≤ ht + cs + cc, with average sl ≥ −X | **component-height lower bound** |
| `DegAt :140`, `ShareAt :143` | degree pinching and binomial share | bookkeeping that makes the Hilbert–Samuel term summable |

**Where the CM period comes from.** `FlatDegree logOm` (`lean/src/Development/AbelianVarietyTheory/Definitions/Foundations/ExistsFlatSecRankZero.lean:751–754`) asserts flat sections on every component Z and CM-type element τ with degree `−flatDegVal = −((p−q)/2·logΩ + q(log d − lrd E))`. It is proved by `flatDeg_alt_alt` (`ThirdPlaceSeries/FlatDegreeStatement.lean`) from `flat_tensor_swap_isIso hP hP.q2 hP.q4`, i.e. from rank-one canonical extensions plus prismatic Dieudonné/Hodge theory. The underlying `FlatDegreeStatement` (`Development/AbelianVarietyTheory/BlockTheory/DivisorBase/AdelicDegreeTameRamification.lean:89`) requires `IsAbelianGalois ℚ E → TameAtRamified H`. **So it is a Colmez-type formula only for abelian CM fields with tame ramification**, which is the classically known case (Colmez, Obus). It is not general Colmez.

### 2.4 Layer C: `DeepStR`, the averaged arithmetic-volume bound

`lean/src/Development/AutomorphicSpectrum/Definitions/GlobalGeometry/ModelSmall.lean:63`:
```lean
def DeepStR : Prop := ∃ C ≥ 0, ∀ D T, LawsJ T → m² ≤ k → ∀ j, 1 ≤ j < m → ∀ (Y : Deep T.toCore j) e o,
  Y.Good e o → #primeFactors(M') ≤ 15 → MeanAll Y.U (xiR D) (ell D) C
```
`MeanAll` is at `lean/src/Development/AbelianVarietyTheory/Definitions/Divisors/SemiposAtOfPositive.lean:101`.

In words: for every regular weight u (`WtGap`: strictly decreasing with a gap g), the component average of the arithmetic-volume slope `compVolSlope` is at least −C·errX, where:
- errX = (log bndB + ℓ)·|u|₁ + q·Σ_τ (max u_τ − min u_τ);
- ℓ = `ell D` = log rd_E + |L'/L(1)| (`:105`).

The arithmetic volume is the counting volume `volL` (`:47`) of `smallL` (`:41`): cusp forms of weight τ·G that are integral at finite places and satisfy |f|² ≤ e^{2τt}·Bergman^τ pointwise. **This is a lower bound for heights of unitary Shimura varieties in terms of log-discriminant and L'/L(1).** It plays the same role as the Kudla–Rapoport–Yang / Bruinier–Burgos–Kühn / Hörmann arithmetic-volume formulas, but only as a non-effective inequality: C is existential.

`deep_slim_use` (`lean/src/Development/WeilBound/CoreStatements/AutomorphicKernels/MoriwakiBigness/HilbertSamuelApplications/AhSlimU.lean:9`) feeds `deepStR_of_use` (`DeepStROfUse.lean:12`):
- `ArithIntersectionSystem` (built from resolution, principalization and Poincaré–Lelong) and `HSUse` (arithmetic Kleiman + `G7` + arithmetic volume of nef bundles) combine with Moriwaki bigness and `ResK` into `lineOfLargeDegree`;
- that, with semi-abelian extension, Hodge–Tate (from Fargues), GAGA, quotient by finite flat, Zarhin and `NefRR`, gives `good_tower_volume_theorem_bis`;
- finally `deepStR_of_volume`.

`HeightCondition` (`ThirdPlaceSeries/HeightLowerBoundGeneral.lean:21`) is `height_of_meanAll_bound`, applied to `DeepStR`, the toroidal and semi-abelian geometry, carrying sections bounded by the Bergman kernel, and a weight "budget".

### 2.5 How the named literature pieces fit together

- **Chow forms and Fubini–Study.** `SelfIntersectionBound` (`VolumeEstimateHypotheses.lean:9`) says that for a model (X, L) of the image of a Hermitian lattice, ĉ₁(L(t))^{D+1} ≤ [K:ℚ]·(D+1)·deg·(h_image + t). That is the standard "self-intersection = (D+1)·deg·normalized height" identity, compared through the Chow height. `WellChosen` (`WellChosen.lean:38`) is arithmetic Bézout for a well-chosen family of D small sections. Its lower bound carries the constant (D+1)·H_{N−1}/2 (a harmonic number), which is the Fubini–Study height normalization of projective space.
- **Small sections.** `SmallSectionsInject` (`VolumeEstimateHypotheses.lean:10`) says that the count of small automorphic sections is at most the count of small sections of L^{8i} on the arithmetic model. This is the bridge from automorphic forms to Arakelov geometry.
- **Nadel / L² / Kawamata–Viehweg / point separation.** These sit in `Quoted` and `HypothesesX`. `PointSeparationPair` (`Development/AbelianVarietyTheory/PublishedTheorems/Divisors₂/PointSeparationPair.lean:15`) is an Angehrn–Siu-type separation of two closed points under klt and nef/big hypotheses. Kawamata–Viehweg is derived from Nadel vanishing (`kawamataViehweg_of_nadelVanishingPair`, at `EveryCharacterOfLiteratureOfVWin.lean:448`). These supply the nonvanishing and generation of sections used by `exists_nonvanishing_of_toroidal` and the carrying sections.
- **Toroidal compactifications** (`SiegelToroidalIntegral`, `ToroidalForFanKS`) supply smooth SNC models of the deep covers, Mumford charts, ampleness of ω^{Nk}(−boundary), and log Kodaira–Spencer.
- **Semi-abelian Lie seminegativity** (`InterNumDetNonposSplitTorus.lean:23`): every subbundle W ⊂ Lie G of a semi-abelian scheme over a smooth projective curve has deg det W ≤ 0. This is Faltings / Moret-Bailly semipositivity of the Hodge bundle, and it feeds `deepGood_of_toroidal_and_semiabelian`.
- **Grothendieck–Messing** gives `coverDegree_of_grothendieck_deformation` (degree control on covers via deformation theory).
- **Fargues and Zarhin** enter only through `DeepStR`: Hodge–Tate integrality of heights at p, and the trick of reducing to principally polarized abelian schemes.

---

## 3. Formalized standard theory vs. novel twists

### 3.1 Resolution of singularities: real Hironaka, Kollár's route

**Size.** `lean/src/Development/ResolutionOfSingularities/` has 499 files and **140,709 lines** (about 280 lines per file). The grep found no `sorry`, `axiom`, `admit` or `native_decide`.

| Subdirectory | Files / lines |
|---|---|
| `IdealPrincipalization` | 219 / 69,051 |
| `ResolutionDescent` | 69 / 14,354 |
| `EtaleCoordinates` | 45 / 14,050 |
| `DerivativeIdeal` | 38 / 9,546 |
| `StrongResolution` | 28 / 8,230 |
| `StrictTransformCharts` | 21 / 6,388 |
| `MaximalContactHypersurfaces` | 18 / 5,167 |
| `Foundations/Blowup` | 15 / 3,853 |

**Statement** (`Statements.lean`):
- `IsBlowup` (`:13`) is the honest universal property: the pullback of I is effective Cartier, and the map is terminal among such.
- `IsStrictNormalCrossings` (`:26`) uses a regular local stalk and a regular system of parameters generating the ideal as a monomial.
- `IsResolutionRuleCharZero` (`:126`): the top is smooth over k, the map is proper and an isomorphism over the smooth locus, the preimage of the smooth locus is dense, all centers lie over the non-smooth locus, and the reduced preimage is SNC.
- `FunctorialResolutionCharZero` (`:150`) additionally requires compatibility with smooth morphisms of any relative dimension (`IsSmoothFunctorialRule`) and with field extensions.

This is proved at `HasSimpleNormalCrossingsOfInStrictNormalCrossing.lean:15` from `EmbeddedResolution.strongResolutionOfSingularitiesCharZero` (`EmbeddedResolution/HironakaTheorem.lean:69`). It is then repackaged as `Hypotheses₂.ResolutionCharZero` (`Development/AutomorphicSpectrum/PublishedTheorems/Geometry₂/ConclusionOfSmooth.lean:53`), which also assumes `IsSeparated`.

**How they did it in "only" 499 files.** They did not take a shortcut. They followed Kollár's *Lectures on Resolution of Singularities* closely:
- **Derivative ideals.** `derivIdeal` and its iterates, with order-decrease lemmas (`DerivativeIdeal/DerivativeIdeal.lean:19, 217`).
- **D-balanced and MC-invariant ideals.** `IsDerivBalanced` and `IsMaxContactInvariant` (`MaximalContactHypersurfaces/MaxContactIdeal.lean:13, 49`).
- **Tuned ideals.** `tuningWeight m c = Σ (m − j)·c_j`, `tunedIdeal` (`TunedIdeal.lean:6, 100`), and `tuningExponent = (m−1)·lcm(1..m)` (`TunedSheaf.lean:34`). This is Kollár's W(I, m).
- **Maximal contact.** Maximal contact hypersurfaces with étale and chart uniqueness (`MaxContactEtaleUniqueness`, `MaxContactChartUniqueness`). Independence of the choice of hypersurface (`OrderReduction/IndependenceOfHypersurface.lean`) is what gives functoriality.
- **Induction.** Marked ideals, order reduction, the monomial case and divisor reduction, i.e. the usual induction on dimension.
- **Globalization.** Principalization with radical centers is applied to affine pieces embedded in 𝔸ⁿ (`AffineEmbedsIntoAffineSpace`). The pieces are glued using étale, open-immersion, field-base-change and smooth compatibility (`GlobalResolutionFromAffine.lean:359, 390`). Independence of the embedding comes from `closedEmbeddingsRelatedByAutomorphism`, which is Kollár's stabilization lemma.

**Notable details.**
- `ResolutionRuleCharZero` is a type-valued rule; existence is obtained by `choose` from the glued sequence (`GlobalResolutionFromAffine.lean:381`).
- In the final `BlowupSequence`, centers are arbitrary ideal sheaves. Smoothness of centers (`center_smooth`) lives in the internal `IdealBlowupSequence` and is used for the principalization statement, but it is not exported in `IsResolutionRuleCharZero`.

**Why it is in this cone.** Principalization drives the arithmetic Hilbert–Samuel theorem (`arithHilbertSamuel_of_principalisation`), `arCalc`, `cycleHeights_direct … resK`, and the `ArithIntersectionSystem` inside `DeepStR`. It is used to handle singular generic fibres.

### 3.2 L²-∂̄ (`ReciprocityTheory/L2DbarEstimates`): 227 files, 33,734 lines

**Model of complex geometry.**
- `EtaleStein n M` (`IsLocalHomeomorph.lean:111`): a local homeomorphism z: M → ℂⁿ together with a smooth plurisubharmonic exhaustion. So M is a **Stein Riemann domain spread over ℂⁿ**, and all analysis uses the pulled-back flat metric.
- `WeightedAtlas` (`PlurisubharmonicCharts/FamilyLeCoords.lean:14`) presents compact complex manifolds: holomorphic transition maps; line bundles as cocycles `g la i j` indexed by an abelian group `La` of bundle types (additive in `la`); smooth weights `ph` with the transformation rule ph_j = ph_i − log|g|²; the canonical bundle `kap` defined by Jacobian determinants; and volume μ = e^{ph kap}·Lebesgue in charts.

**Theorems.**
- **Hörmander** (`HormanderEstimate/Hormander.lean:13`). This is the textbook proof: Riesz representation on the range of the adjoint (`rieszOnRange`), from an a-priori inequality (`TestIneqStatement`) and Weyl-type regularity (`RegMStatement`), which are proved in `Localization`, `BasicIdentity`, `WeakHolomorphy` and `Mollifiers`. It solves ∂̄u = ∂̄F₀ for smooth F₀ with ‖F₀ − G‖² ≤ ∫ h·e^{−φ}, where |∂̄F₀ · ξ|² ≤ h·Levi(φ)(ξ). This is the (0,0)→(0,1) case, which is all that extension needs.
- **Skoda L² division** (`SStatement`, `JacobianInterpolationStatement.lean:20`), with the **sharp Skoda constant t/(t − (p−1))**.
- **L² Riemann extension** across hypersurfaces, plus the statement that hypersurfaces are null (`EXTStatement`, `EXTNullStatement`).
- **L² extension, "log-canonical" version** (`Development/AbelianVarietyTheory/PublishedTheorems/Divisors₂/L2ExtensionLogCanonical.lean:32`). This is an Ohsawa–Takegoshi–Demailly-type estimate:

$$\int 2^n\frac{|F|^2_{K+E}\,e^{-\psi}}{1+\delta^2\psi^2}\,d\mu \le \frac{34}{\delta}\,c_n\sum_{P}\mathrm{res}(f(P)),$$

  where ψ = log|s|² for n sections s whose common zero set is **finite and transversal** (nonzero Jacobian at each zero). It assumes curvature E + α·ψ ≥ 0 for α ∈ [1, 1+δ].

**The twist.** Extension is only **from a 0-dimensional subvariety**, not from a general submanifold. The proof (`Development/AbelianVarietyTheory/Proofs/DivisorProofs/L2ExtensionLogCanonical.lean:13`) first builds an **étale frame off the finite zero set** (`exists_etale_frame_off_finite_zeroSet`). This turns the compact manifold minus a divisor into an `EtaleStein` domain, and then runs Hörmander there. That avoids complete-Kähler metrics and curvature of the base metric entirely. It is clever and sufficient for Nadel vanishing, point separation, and nonvanishing of sections on toroidal models.

### 3.3 Heights and arithmetic Hilbert–Samuel (`GroundTheory/HeightsAndTheta`)

**Sizes.** The `Heights` subdirectories include `ComplexAnalyticSets` (994 files / 74,689 lines), `HilbertSamuel` (844 / 88,665), `KleimanAmpleness` (593 / 68,571), `DiscreteValuationNumbers` (429), `Intersections` (385), `HeightKernels` (339), `OrbitLimits` (334), `ArithmeticBezout` (305), `HodgeLowerBound` (276), `FiniteCovolume` (168), `ChowForms` (62) and `ChowlaSelberg` (58).

**Definitions** (`Development/AbelianVarietyTheory/Definitions/Divisors/ExistsIsClosedImmersionGenericPoint.lean`):
- `IsArithVar` (`:578`): k a domain, finite over ℤ; X integral, projective and flat over ℤ, of Krull dimension D+1.
- `HermLB` (`:659`): a line bundle with C^∞, conjugation-invariant weights at each embedding σ.
- `smallSec` (`:763`): sections with sup-norm ≤ 1 at every complex point.
- **Heights are defined axiomatically, BGS-style** (`IsArithHeight`, `:795`ff), by three axioms:
  - vertical: geometric self-intersection times log q on fibres over finite fields;
  - curves: the Arakelov degree of a curve;
  - recursion: m·h(Z) = Σ mult·h(div components) − ∫ log‖s‖·c₁^e.
- Self-intersection: `IsSelfInter a := ∃ h, IsArithHeight h ∧ h(generic point) = a` (`:820`).

**Arithmetic Hilbert–Samuel** (`Development/AbelianVarietyTheory/PublishedTheorems/Divisors₂/SmallSecTensTriv.lean:14`): for nef L and any N,

$$\log\#\{\text{small sections of }L^m\otimes N\} = \frac{a}{(D+1)!}m^{D+1}+o(m^{D+1}).$$

This is the full nef version (Moriwaki-strength).

**Proof route.**
- Ample case (`AmpleArithHilbertSamuelOfPrincipalisation.lean:26`): a base-point-free section tuple gives a projective embedding; compare with Fubini–Study weights (bounded difference); change the metric to compare small-section counts; twist by e^{tm} with t ≫ 1; and use that the self-intersection of canonical weights tends to 0.
- Ample to nef: `arithHilbertSamuel_nef_of_ample` (`ArithHilbertSamuelOfPrincipalisation.lean:11`).
- Tools: Minkowski counting (`PMinkowskiCount`) and local/uniform Bergman bounds (`PLocalBergmanBound`, `PUniformBergmanBound`).
- **No analytic torsion and no Bismut-style machinery**: a grep of `HeightsAndTheta/Heights/HilbertSamuel` finds nothing. This is a geometry-of-numbers plus Bergman-kernel proof, closer to Abbes–Bouche, Zhang and Yuan than to Gillet–Soulé's arithmetic Riemann–Roch.
- `MoriwakiBigStatement` (`ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/ArakelovGeometry/MoriwakiSt.lean:29`, arithmetic intersection ≤ arithmetic volume for nef bundles) and `NefRR` (`Development/AutomorphicSpectrum/PublishedTheorems/Geometry₂/NefRR.lean:8`, geometric Hilbert–Samuel in multi-graded charts) are proved *outright* (`hsUse_outright`, `moriwakiBig_outright`).

### 3.4 Other formalized "published" theorems in the cone (statement level only)

| Theorem | Statement (file:line) | Internal proof |
|---|---|---|
| Faltings–Chai for 𝒜_{g,n} | **asserts the existence of 𝒜_{g,n}** (`SFam`) over ℤ[ζ_n, 1/n] for odd n ≥ 3, its arithmetic toroidal compactification with semi-abelian extension, smoothness of relative dimension g(g+1)/2, ω^N generated, and ω^{Nk}(−∂) ample (`AutomorphicForms₂/SiegelToroidalIntegral.lean:145`) | `siegelToroidalIntegral_holds`, via polarized charts and degeneration data |
| Unitary toroidal + log Kodaira–Spencer | ∀ moduli `Xo : Moduli Dw l` ∃ a smooth SNC toroidal model with Mumford charts and log-KS (`Divisors₂/ToroidalCompactificationBis.lean:45`) | `toroidalForFanKS`, via rigid boundary charts |
| Grothendieck–Messing | lifts of abelian schemes over nilpotent PD thickenings ↔ admissible lifts of the Hodge filtration; full on objects and morphisms (`Divisors₂/CanonicalOfAbelianDeRham.lean:55–63`) | `grothendieckDeformation_of_lifting` |
| Fargues Hodge–Tate | ker HT ⟂ image of dlog under the Weil pairing, for p-divisible groups over 𝒪_C (`AutomorphicSpectrum/PublishedTheorems/Algebra₂/FarguesExact.lean:10`) | `UpperTheory.Lit.farguesExact` |
| Zarhin's trick | an abelian scheme over a valuation ring of an algebraically closed field with relatively ample L is a retract of a principally polarized one (`Algebra₂/ZarhinStatement.lean:21`) | via `dualAbelianScheme` |
| Nadel vanishing + isolated non-klt divisor | `Divisors₂/IsLogCanonicalMultipleCanonical.lean:574` | `NadelVanishingSeparation.NSI` |

(Paths in the first column without a prefix are under `lean/src/Development/AbelianVarietyTheory/PublishedTheorems/`.)

**Caveat.** `Moduli D l` (`ReciprocityTheory/ReductiveGroups/ArithmeticGeometry/BirationalGeometry/ToroidalCompactification/PushInvertible.lean:29`) is a **structure**: a quasi-projective smooth scheme with a universal object, representing the moduli problem on reduced test schemes, plus an unramifiedness condition. The unitary results are therefore stated for every given moduli space and do not construct it. Only the Siegel case asserts existence. I did not audit the degeneration-data construction; it is a large separate subsystem (3,505 file names in `AbelianVarietyTheory` match `degenerat|mumford|siegel|toroidal`).

---

## 4. Conditionality audit

`lean/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:215` defines `OpenLiteratureStatements` with only three fields: `caraianiLocalGlobalDual`, `localLanglandsExists : RecTExists`, and `galoisRepOfPolarizedPairLit`.

The call at `:812` passes `…_of_literature O` for every `CovolX` input. **I checked every relevant wrapper.** None of the 15 inputs, none of the 28 `PublishedHodgeBundleTheorems` fields (`:781`ff), and none of the auxiliary wrappers they call (`dual_abelian_scheme`, `abelian_lifting`, `abelian_de_rham`, `arith_hilbert_samuel`, `principalisation`, and so on) touches `O`. The only uses of `O.*` in the file are at lines 284, 460 and 618, all outside this cone.

**Conclusion:** `CovolX` is unconditional relative to Lean's axioms, provided the textual reading matches what compiles. `PublishedHodgeBundleTheorems.{p18, q2, q12}` are filled by `…_holds` theorems that ignore their argument (`HodgeBundleWeights/ToKnownTheoremsOf.lean:36–38`).

---

## 5. Surprises

1. **The name is misleading.** "Covolume" is the covolume of Hermitian lattices of integral lifts, not of an arithmetic group or Shimura variety. The main term is an L'/L(1) CM period times Hodge weights, which reads like a lower bound on Faltings heights of theta lifts.
2. **The error budget is exponential in the scale.** E = f·m·x^ε·e^{x^ε}·log log x, while the main term is O(|logΩ|·Σ weights). The deep-cover comparisons (`RingAt`: −2b; `MapsAt`: e^{2b}) lose O(b) = O(e^{x^ε}) in slope, and that loss sets the error size. `SizeAt :75` requires b ≤ E ≤ x^A·b and |mainT| ≤ x^A·b, so the theorem is accurate only to polynomial-in-x multiples of b. Whatever consumes `L3` downstream must live at that scale.
3. **Exponential smallness is essential.** `BadAt :69` needs the bad rank fraction to be at most 3·e^{−x^{ε/(7J)}} so it can beat the polynomial `LamAt` bound μ_max ≤ x^A·b (`exists_loss_le`). The top level j = m is handled separately by Green's regular characters (`lifts_badAt_last_of_green_cuspidal`, `ThirdPlaceSeries/CoveringBadLocusOfDescentSteps.lean:26`). The other levels go through descent on deep covers.
4. **The large exclusive cone is foundational geometry, not analysis.** The 17,801 files exclusive to the `HodgeBundleWeights` entry point are mostly 𝒜_g and unitary toroidal machinery, Grothendieck–Messing, prismatic Dieudonné and semi-abelian theory. The analytic L² part is only about 227 files.
5. **The CM-period input is restricted.** It only covers abelian CM fields with tame ramification. Any use of `CovolX` beyond that is blocked at `FlatDegreeStatement`, via `IsAbelianGalois ℚ E` and `TameAtRamified`.
6. **Resolution sits underneath arithmetic heights.** Principalization is upstream of arithmetic Hilbert–Samuel, `arCalc`, cycle heights and `ArDegree`. So Hironaka is load-bearing for `CovolX`.

---

## 6. Reusable engines (standalone math)

| Engine | Where | Comment |
|---|---|---|
| **Functorial char-0 resolution and principalization** | `Development/ResolutionOfSingularities/` | A complete Kollár-style development; arguably the most valuable artifact here |
| **Hörmander + Skoda (sharp constant) + L² Riemann extension on Stein Riemann domains** | `ReciprocityTheory/L2DbarEstimates/` | Self-contained, with its own model of complex geometry |
| **Point L² extension on compact manifolds** | `…/DivisorProofs/L2ExtensionLogCanonical.lean:13` | The étale-frame reduction is a reusable trick |
| **Nef arithmetic Hilbert–Samuel without torsion** | `…/ArithHilbertSamuelOfPrincipalisation.lean` and `GroundTheory/HeightsAndTheta/Heights/HilbertSamuel` | The axiomatic BGS height (`IsArithHeight`) is a nice interface |
| **Good/bad slope cut for Hermitian lattices** | `…/MajAtAddRight.lean:111` | Short, general, and useful in Bost's slope method |
| **Grothendieck–Messing, Fargues HT, Zarhin** | see §3.4 | Each is a stand-alone p-adic / abelian-scheme theorem |

---

## 7. Brittle joints and bottlenecks

1. **Sharpest quantitative bottleneck: `RingAt`/`MapsAt`.** These are the O(b) losses from passing to deep covers, and they dictate E ∝ e^{x^ε}. Improving the theorem means making the level-15^e cover comparison cost o(b). The level exponent e ≈ 3x^ε/log 3 (`expL`) ties the cover depth to the scale.
2. **Second bottleneck: `BadAt`.** It needs bad rank ≤ 3e^{−x^{ε/7J}}·rk. With ε < 1/52 (`Scale.eps_lt`) and J ≥ 1, the exponent is tiny; everything works only for x ≥ x₀(A, B, C₁, C₂), and x₀ is non-explicit.
3. **Non-effective constants.** C in `DeepStR` and C₁, C₂ in `CoreAt`/`LowAt` are existential, so the final C₀ = C₁ + C₂ + 1 is non-explicit (`CovolXOfSteps.lean:27`).
4. **Point filters.** `RowsTAlt` includes `RecTied = FieldSmall ∧ ESerTie` (`CovolXOfCovol.lean:161`). Applying `CovolX` downstream needs these at all large x, and `CovolX.covol` asks for them as an extra `Closed FamHyp` hypothesis.
5. **Junk values.** `slope_sq` is `if HasGram N then muDef … else 0` (`Development/AbelianVarietyTheory/Definitions/Foundations/IsProbabilityMeasureMuPart.lean:32`). `GramAt` supplies `HasGram` for the base lattices, but deep-cover slopes `slopeW_sq` depend on `GoodAt`. Worth auditing for vacuous cases.
6. **Hypothesis structures.** Since `Moduli D l` is assumed rather than constructed, statements are vacuous whenever no moduli space exists. That is harmless for this argument, but it hides the construction cost of unitary Shimura varieties.
7. **Not verified here:**
   - `Formalism.F.covol` (the base covolume in `HN.ht`);
   - the internal Faltings–Chai and degeneration-data proofs;
   - how `CompanionTheory/SpectralGeometry` (mostly `LocalGlobalProofs`: adelic characters, Euler products, self-dual lattice filtrations) feeds the cone. It appears to supply local-global measure and character infrastructure, but I did not trace the exact edge.

### Suggested follow-ups
- Audit `Formalism.F.covol` and `Formalism.HN.slope` for normalization.
- Trace `FlatDegreeSt` (`Development/AbelianVarietyTheory/Definitions/Divisors/HtValOnSubset.lean:118`) to see exactly how prismatic Dieudonné theory yields the Colmez value.
- Audit the existence of `SFam` (𝒜_{g,n}).
- Find the downstream consumer of `L3` to see whether the e^{x^ε} error is truly harmless there.
