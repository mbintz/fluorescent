I've traced `LinkS` from `LinkAlt` down to the abstract Gram-operator engine and found where each of its inputs is proved. The main findings: the bound `exp(-x^{ε/8})` is a cosmetic weakening of much stronger bounds. The whole off-diagonal estimate is an explicit hypothesis of `LinkAlt`, proved elsewhere. And `LinkS_at` holds vacuously unless a "T-window" condition, supplied separately, holds. Paths below are relative to `lean/src/`. I did not edit any files.

---

# How `LinkS` is proved

## 0. Summary

- **What `LinkS` says.** Fix one auxiliary automorphic datum `D : D7`. For each word `u` there is a linear map `Pu(u) : Cu(u) → HH` into a fixed finite-dimensional space of automorphic forms with `dim HH = Dall`. Concretely `Pu` is a Poincaré-series map. `KD u u'` is the normalized Gram operator `Pu(u)*·Pu(u')`. `LinkS` says three things:
  - each normalized `Pu(u)` is close to an isometry;
  - for `u ≠ u'`, the overlaps are at the level you would expect from random subspaces: `‖KD u u'‖²_HS ≲ du·du'/D*`;
  - `Dall ≈ D*`.
- **What is actually proved** is much stronger than `exp(-x^{ε/8})`:
  - `eta0 = b⁻⁶ = exp(-6x^ε)`;
  - `eta1 = exp(-c₇·r·f·log r)`;
  - `e0 = 2C0/Γ + 2exp(-kf·log k)`, with `Γ = exp(C_Γ·m⁵·f·x^ε)`.

  The eighth root `y = x^{ε/8}` comes only from rewriting `L = x^ε = y⁸`.
- **The logical shape is unusual.** `LinkS_at` is an implication from a window condition. When the window fails, the proof picks `eta0 = eta1 = e0 = 0` and the statement holds vacuously.
- **The off-diagonal estimate is not proved in `LinkAlt`.** It enters as the explicit hypothesis `sO : TheoremSSelected`, which is literally the off-diagonal bound. In the live chain it is discharged in `Development/AbelianVarietyTheory/Proofs/FlagMeasures/OffK0Closed.lean:673`, starting from the Siegel–Weil formula.

---

## 1. The objects in concrete notation (Q1)

### 1.1 The containers

- `D7` (`Formalism/LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean:76–334`) bundles:
  - ranks `R`, a host CM field `E/F`, Hermitian spaces `sp`;
  - row data `what₂ : Rows.Data R` (line 87);
  - per-word members `mem u` (line 104);
  - Gram data `s : S.Draft.SData …` (line 226).
- `Rows.Data` (`Formalism/LocalRingCardinality/DataRows.lean:36–168`) holds the abstract `Word : Type` (line 110), `Dall : ℕ` (line 68) and `Dstar : ℝ` (line 85).
- `SData` (`Formalism/SharpRestriction/CuspSpanNormBounds/DataS.lean:13–84`) holds:
  - a finite-dimensional Hilbert space `HH` (lines 33–36);
  - per-word finite-dimensional Hilbert spaces `Cu u` (lines 38–41);
  - continuous linear maps `Pu u : Cu u →L[ℂ] HH` (line 43);
  - a term expansion `Term u u'`, `aTerm : Term u u' → (Cu u' →L Cu u)`, and an `F`-valued invariant `Gterm` (lines 50–61).

### 1.2 Ranks

From `Formalism/LocalRingCardinality/Params.lean`:

| Symbol | Definition | Line |
|---|---|---|
| `f` | `2·n`, the number of archimedean places | 30 |
| `r` | `k + m − 1`, the rank of the Hermitian space | 32 |
| `rS` | `m/2 − 1` | 38 |
| base signature | `(k + rS, rS + 1)` | 44 |

`ThmSOwn.size_numbers_of_hypotheses` (`FlagStabilizerTensors/ThmSOwn.lean:770`) records `m = 2rS + 2`.

### 1.3 Words

`Word` is an abstract finite type. It is injected into binary strings by `letter : Word → Fin (k−2) → Bool` with `letter_inj` (`DataS.lean:25–27`).

A word changes the Harish-Chandra parameters at every archimedean place:
- `u_{l+1} = v_l − 1/2 − (letter u l ? Δ : 0)`, where `v_l − v_{l+1} = 4Δ` (`DataS.lean:22–31`);
- the first and last entries are frozen (`hcW_first`, `hcW_last`, `RhoDetPrime…lean:101–102`).

`StandingNumericalData` (`CuspSpanNormBounds/StandingNumericalData.lean:84–98`) adds:
- the `U(k)` parameter `uS u τ` interlaces the big discrete-series parameter `lamS` (line 94);
- distinct words differ at every place: `u ≠ u' → uS u τ ≠ uS u' τ` (line 96).

Each word also carries an auxiliary split prime `T_u = (mem u).A.T` (`DataKernels.lean:107`).

### 1.4 The spaces `Cu(u)` and `duS(u)`

**Abstract model.** `s_Cu : s.Cu u ≃ₗ (mem u).A.Mu0` is an isometry (`RhoDetPrime…lean:233, 303–305`).
- `Mu0` is a finite-dimensional subspace of functions `cls 0 × Y 0 → ℂ`.
- It is stable under the action `rhoT` of `(F_v)^×`, where the `F_v` are finite fields of size `T`, one for each of `f` places (`DataKernels.lean:107–128`).
- `duS u := finrank Mu0` (`RhoDetPrime…lean:345–346`).

**Concrete model.** `HidaSetting` (`HaarTransversals/HidaSetting.lean:179–328`) gives a unitary group `G = U(V)` with `n = r` (line 195). The flag data are:
- `rS` hyperbolic pairs `eX, fY` (lines 207–211);
- an anisotropic vector `zu u` with `⟨zu,zu⟩ = −T_u` (lines 217–218);
- a positive-definite rank-`k` complement carrying a finite-dimensional rep `piLoc u v` of Harish-Chandra type `(hcW u)` (lines 288–291).

A vector `Wu u` satisfies `IsWu` (lines 151–156, 311–317):
- `W(s·x) = ψ(s)·ρ(s)·W(x)` on the subgroup `Sinf`;
- `W` reproduces under convolution with `ph`;
- `W` is L²-normalized.

Here `ph` is built from formal degrees (line 355). My reading: `ph` is a discrete-series pseudo-coefficient and `Wu` is a Bessel/Gelfand–Graev-type model vector. That is an interpretation, not something the code states.

`Cu X u hK` is the space of "columns" (`PoincareInHH.lean:144–145`). It is identified with `D.s.Cu u` through `SIso` and `ConcTie` (`ThmSOwn.lean:387–392`; `RowsConc.lean:57`, where `duC = duS`).

### 1.5 The Hilbert space `HH` and `Dall`

- `s_HH : finrank s.HH = Dall` (`RhoDetPrime…lean:231`).
- Concretely `HHX X = RowsDef.HHB X.B X.Rph` is a subspace of `L²(G(F)\G(𝔸))` (`PoincareInHH.lean:206`).
- `Pu` maps `T ↦ Pser T`, where `Pser T(x) = Σ_{δ ∈ Dt} Ph_T(δx)`. This is a Poincaré series over a transversal of `S_rat\G(F)` (`PoincareInHH.lean:149–150, 163–166, 179–186, 208–218`).
- `Ph_T` combines `ψ_fin`, the level character `χ₂` and `T(Wu(y_∞))` on `N_fin·H_fin·x_u·K₂` (lines 159–166).
- Membership in `HHX` requires `Re(Rph(Pu T)) = Pu T` (line 199). These are the archimedean projector and the level idempotent.

### 1.6 The Gram operator

`RelevantZeroGramTerms.lean`:

```
KD u u' := Kmat D.s u u'                                    (line 509)
Kmat u u' := (c0 u · c0 u')^{-1/2} • (Pu u)† ∘ (Pu u')      (lines 339–343)
c0 u := volN u · volH u / dimPi u                           (line 337)
dimPi u := ∏_τ dim π_{u,τ}                                  (line 335)
hsNormSq A := Re⟨A,A⟩_HS                                    (lines 324–325)
```

- `L.hsSq u u' = hsSqD = ‖KD u u'‖²_HS` (`LocalRingCardinality/DataParamsS.lean:8`).
- In the concrete model `c0 = volN·volH / dim Vpi` (`PoincareConstantEq.lean:50–59`). This normalization makes the identity double-coset contribute exactly `id` (`IdCellDiag`).
- Unfolding `Pu*Pu'` gives a sum over terms `t`. A term is a row-representative lattice `Λ` plus a class of flags (`ClosedLocalOrbits/TermDef.lean:150–154`).
- The term invariant is `Gval = |det Ẑ_{r+1}|² − T·T'·|det Ẑ_r|²`, computed from the cross-Gram matrix of the two flags (`FlagUnipotentLattices/MemOfOrthogonalAnisotropic.lean:81–86`).

### 1.7 `Dstar`

`Dstar` is pinned in three places:
- `Dstar_eq : (mem u).A.Dstar = what₂.Dstar` (`RhoDetPrime…lean:160`);
- `ConcTie: DstC X = what₂.Dstar`, where `DstC = I.Dstar(fdegAll …) μf fund e` (`RowsConc.lean:32, 57`);
- `Sz.SizeData.Dstar = vol(n) · idxRow · ∏_w dsig(w)`, with `n = k + m − 1` (`HermitianCurvature/StatementSz.lean:61, 79–84`). Here `vol(n)` is the volume of the rank-`n` group, `idxRow` is the level-index factor at the two level primes `g₁, g₂`, and `dsig` are the formal degrees.

The matching column count is `ColumnCount: du = vol(k) · idxCol · ∏ dimPi · (T^k − 1)^f` (`StatementSz.lean:102–103`). So `du ∝ T^{fk}` and `D*/du` is a ratio of volumes, formal degrees and level indices.

### 1.8 Reading `LinkS` as a statement about subspaces

For random subspaces of dimensions `du, du'` in a space of dimension `D`, one expects `‖P_u P_{u'}‖²_HS ≈ du·du'/D`. `LinkS` asserts:
- off-diagonal blocks satisfy `‖KD u u'‖² ≤ (1+η₀)·du·du'/D*`;
- diagonal blocks satisfy `‖KD u u − id‖² ≤ e₀·du`;
- `Dall ≤ (1+η₁)·D*`.

`ChosenCode` (`GlobalSchurBounds/Chosen.lean:56–57`) requires `#Words ≥ C0·Γ²·x^{CH}`. Together with the window this forces `Σ_u du ≳ D*·x^{CH}`, so the family is heavily overcomplete. The near-orthogonality is therefore of the "random overlap" kind, not literal orthogonality.

---

## 2. How the proof decomposes (Q2)

### Layer A — choosing η and the vacuous branch

`linkS_of_standing_hypotheses` (`CuspSpanNormBounds/StandingHypothesesHoldFamily.lean:628–651`) does the following:
- If `Win` holds (`Win` is defined at lines 594–596 and equals the `LinkS_at` premise), it calls `eF_nonneg_and_le_exp_neg` (lines 206–268) and `linkS_concl` (lines 186–204).
- Otherwise it returns `⟨0,0,0,…, fun h => absurd h hW⟩` (lines 650–651).

`linkS_concl` sets:
- `eta0 := b⁻⁶`;
- `e0 := FrobeniusProjectedBounds.eF D C0 = 2C0/Γ + 2exp(−kf·log k)` (`FrobeniusProjectedBounds.lean:164`);
- `eta1 := exp(−c₇·r·f·log r)`.

### Layer B — four kernel clauses plus a dimension count

`Conclusion1` (`AdmissibleBoundsFromSource.lean:212–218`, also `ThmSOwn.lean:37–49`) splits each kernel as `Kmat = K⁰ + Kpp`. Here `Kpp` sums the degenerate terms `{Gterm = 0, not the identity term}`:

| Clause | Statement |
|---|---|
| **ClKppOff** | `Kpp(u,u') = 0` for `u ≠ u'` |
| **ClKppDiag** | `‖Kpp(u,u)‖² ≤ du·exp(−kf·log k)` |
| **ClOff** | `‖Kmat(u,u') − Kpp‖² ≤ (1 + b⁻⁶)·du·du'/D*` |
| **ClDiag** | `‖Kmat(u,u) − Kpp − id‖² ≤ Γ·du²/D*` |

The dimension count `adm7` (`FrobeniusProjectedBounds.lean:105–106`) is `|Dall − D*| ≤ exp(−c·r·f·log r)·D*`.

Two consequences:
- **Off-diagonal output.** `linkS_concl` (lines 196–199) gets the off-diagonal part of `LinkS` from ClKppOff and ClOff.
- **Diagonal output.** `diag_unproj` (lines 144–184) applies `‖A+B‖² ≤ 2‖A‖² + 2‖B‖²` together with the upper half of `Win`, `du ≤ Γ⁻²·D*·C0` (line 149). This turns `Γ·du²/D*` into `C0·du/Γ`.

### Layer C — moving to the concrete term operator

`hsNormSq_Kpp`, `kpp_zero`, `hsNormSq_off` and `hsNormSq_diag` (`ThmSOwn.lean:288–379`) transport everything through `SIso`. The result:
- ClOff becomes `‖(Y.tO u u').K0‖²`;
- ClDiag becomes `‖K0 − oneC‖²`;
- the degenerate parts become `‖part degSet‖²`.

Here `Y.tO` is a `PB.Terms` object (`HermitianCurvature/StatementPB.lean:15–38`). It has:
- term operators `op`, sorted into id / degenerate / generic / non-generic sets (lines 45–61);
- auxiliary vectors `vec`, grouped into rows;
- a "local Gram" matrix `GG`;
- a pair-collision index `s0`.

### Layer D — the abstract pair-bound engine (pure linear algebra)

`PB.PairBoundAbstract` (`StatementPB.lean:171–179`):

> If `‖part S‖² = Σ_{ij} GG_ij⟨vecPart_i, vecPart_j⟩` (`NormExpansionOn`, lines 86–87), `GG ≤ Pg·Γ₁·I` (`GGBound`, lines 89–90), rows are orthogonal, `CorankPos` holds and `IdZero` holds, then
> `‖K0‖² ≤ (√(Pg(A+2ε)) + √(Pg(ε+ε')))²·dd`,
> given `RowBig ≤ ε·dd`, `RowNotScalar ≤ ε·dd`, `RowMain ≤ A·dd` and `RowNG ≤ ε'·dd` (lines 101–109).

`PB.PairBound` (lines 220–234) plugs in the specific sizes:

| Quantity | Value | Source |
|---|---|---|
| `Pg` | `(1+3/g₁)^f·(1+3/g₂)^f ≤ exp(6b⁻⁷)` | `NumPrice` (181–185), using `g_i ≥ (kb)⁸` |
| `A` | `(1+δ)·e₁`, with `δ ≤ b⁻⁷` and `e₁ ≤ exp(12f·2^{−(k−2r−2)})` | — |
| loops `ε` | `exp(−c·k·f·log k)` | — |
| non-generic `ε'` | `2^{−(k−2r−5)}·exp(Cn·(2r+2)⁵·f·log b)` | — |

`SqrtSumSqLeOneAddInvPowSix` (lines 206–209) closes the bound to `1 + b⁻⁶`.

`MainRow` (lines 381–398) supplies the main term `Γ₁·Σ ≤ (1+δ)·e₁·(d·d'/D*)` with `δ = C(r+1)(C/Th)^f ≤ b⁻⁷`. That threshold comes from `Sz.FinalSmall` and `ThetaPower` (`StatementSz.lean:492–507`).

Instantiation chain:
- `TheoremS.pbApplied` (`FlagStabilizerTensors/TheoremS.lean:19–47`) is `t_PairBoundFromLocal t_MainRow t_PairBound …`.
- `SpectralTiesReal.theoremS_rec` (lines 147–239) instantiates it with `MassData` built from the concrete model.
- The diagonal case reuses the same engine with `A = gamB = exp(C_B·m⁵·f·log b)` (`RowsPos.lean:43–47, 210–240`; `RowsConc.lean:52`).

### Layer E — where each input comes from

**Finite-place / arithmetic / counting**

- **ClKppOff** (`Closed.KppOffC_holds`, `ClosedVolumeStatements/FullExistsTiedHolds.lean:36–41`): degenerate cross-word terms vanish. The proof goes through `covariantRepZero_of_lemmaV` (averaging against a nontrivial `ψ_∞` on unipotent stabilizers, `schurNFC`).
- **ClKppDiag** (`RowsPos.kernel_diagonal_positive hTy`, `RowsPos.lean:202–208`): `pairs_degree_bound` (lines 95–182) bounds degenerate pairs through `TypeAt` and Kloosterman-diagonal machinery (import line 2), with `Pg ≤ 2` at the level primes. `TypeP` is proved in `Development/AbelianVarietyTheory/Proofs/FlagMeasures/RowsPosTypeP.lean:9` from Bessel multiplicity one plus a large-gap discrete-series statement, so it is partly archimedean.
- **Level-prime price** `Pg`: `ggBound` with `card Fq ≥ 3` (`RowsPos.lean:194–196`), plus `GGNumeric` (`StatementPB.lean:130–131`).
- **Dimension count** `h30 : CountAllPointsClass PLevT'` (`CuspSpanNormBounds/BridgeCountE.lean:45–73`):
  - The statement is `|Dcount − D*| ≤ exp(−c·n·f·log n)·D*` for the level idempotent `e` with `IsLevelCharIdem` (lines 31–35).
  - It holds under an archimedean gap `h ≥ C·n¹⁹·f⁵·log(b·rd)`.
  - `PLevT'` (`FlagStabilizerTensors/CountT.lean:38–39`) adds `InstTie` (signature, volume and class items) and `1 ≤ qqI`.

**Archimedean / harmonic-analytic / spectral**

- **`WuDecayOfGap`** (`RootLatticeThresholds/WuDecayAll.lean:25–27`): under `GapHyp` (`r ≥ 1801` and HC gaps `≥ 16r¹⁹`, `ConcreteSettingExists.lean:13–15`), each `Wu` satisfies `WuReprod ∧ WuWeighted` and `ph` is integrable. Proved as `GlobalTheory.wuDecayOfGap := CompanionTheory.Lime.BM.wuDecayOfGap_holds'`, which uses `besselMapUniqGap`.
- **`MainRow` threshold `Th ≥ k^{cExp}`**: comes from `ThetaPower` / `ThetaLower` (`StatementSz.lean:478–501`). These are lower bounds on cut thresholds built from `xHat`, `lamHat`, `lamPrimeHat`. The local Bessel objects are `LocBessel.J/beta`, using `QuantumDeterminants.besselJ` and Capelli operators `capelliH` (`RelevantZeroGramTerms.lean:460–534`).
- **`CarrierFull` / `PB.RealInputs`** (`SpectralTiesReal.lean:57–73`; `StatementPB.lean:309–312`): `GramPSD`, `EstWave`, `PoissonInput`, `EstLift`, `EstBlock`, `Cutoff`, discharged via `carrierP` (`OffK0Closed.lean:665–671`).
- **`LoopRowS`**: proved in `ThirdPlaceSeries/LoopRowsOfRowsFinDim.lean:11–16` from:
  - large-gap discrete series and Bessel multiplicity one;
  - `discreteSeriesCoef_pointwiseBound_unconditional`;
  - `wuDecayOfGap`;
  - volume ratios from Siegel–Weil.

  So the "loops" bound, although stated abstractly via lattice sums (`LoopsInput`, `StatementPB.lean:400–420`), is supplied by an archimedean-decay route.
- **`RowNGP` / `RowMainEqP`**: from `rowNGP_of_siegelWeil` and `rowMainEqP_of_siegelWeil` (`HypothesesNonemptyOfUnramifiedExponents.lean:58–59`). I did not open their proofs.
- **Siegel–Weil** (`HeckeCharacterZeroLocus.SiegelWeilU.SiegelWeilUnitaryConvergent`, `UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean:15–49`): finite volume plus "theta mean = `g_∞(T)·∏_v g_v(T)`" for `2n < M`. Proved at `CompanionTheory/SpectralGeometry/LocalGlobalProofs/AdelicAnalysis/Imports.lean:10`.

**Algebraic / combinatorial assembly**

| Input | Content |
|---|---|
| `ResidEv` | `rdE ≥ 2 ∧ ArithmeticConditionsOfDatum`, free via `residEv_free` (`ResidEvFree.lean:91–98`) |
| `TFrame` | `1 ≤ Tr(w)·kaS^{2rS}` (`CuspSpanNormBounds/PExtra.lean:247–249`) |
| `RowsFinDim` | finite-dimensionality, `CompanionTheory/…/AutomorphicFormsFiniteDimensional.lean:25` |
| `TheoremSSelected` / `LoopRowS` | the off-diagonal and loop clauses themselves (`ThmSOwn.lean:669–674, 1015–1024`) |
| Assembly theorems | `PB.FourParts`, `SplitSum`, `PairSplit`, `SubFamily`, `NormSqAddBoundBySqrtSum` are pure Hilbert-space bookkeeping |

**Where `LinkAlt`'s hypotheses are discharged in the live chain**

| Hypothesis | Discharged by |
|---|---|
| `hWu` | `GlobalTheory.wuDecayOfGap` |
| `hRF` | `rowsFinDim_link` |
| `sTy` | `rowsPos_typeP` |
| `sNG` | `rowNGP_of_siegelWeil` |
| `sM` | `rowMainEqP_of_siegelWeil` (`HypothesesNonemptyOfUnramifiedExponents.lean:57–59`) |
| `sLp`, `sO`, `hTF` | `at_choice_alt hSW` (`ThirdPlaceSeries/AtChoice.lean:16–23`) |
| `sO` specifically | `CarrierGap.offDiag (swxs_of_siegelWeil hSW) (rowNGP_of_siegelWeil hSW) …` |
| `h30` | `CountsIrreducibilityConstants'`, via `row_counts_of_labels_alt hSW` |

All of these are threaded through `AllRowsAlt` → `nonempty_hyps_of_allRows_alt` (`ThirdPlaceSeries/NonemptyHypsOfAllRows.lean:19–101`) → `HypsAlt`.

---

## 3. Where `exp(-x^{ε/8})` comes from (Q3)

It is purely a weakening at the end:
- `scL_eq` rewrites `L.sc.L = (x^{ε/8})⁸` (`StandingHypothesesHoldFamily.lean:616–620`).
- `size_thresholds` (lines 48–72) gives `Y0` with `(2C0+2)·e^{−c·y⁸} ≤ e^{−2y}` and `y ≤ c₇·8c·y⁸`.
- `eF_nonneg_and_le_exp_neg` then proves each bound by monotonicity, using `y ≤ y⁸` and `8Λ ≤ k ≤ r·f·log r`.

The real sizes:

| Quantity | Value | Origin |
|---|---|---|
| `eta0` | `b⁻⁶ = exp(−6x^ε)` | off-diagonal engine target, `AdmissibleBoundsFromSource.lean:35` |
| `eta1` | `exp(−c₇·r·f·log r)`, `r ≥ k` | dimension count |
| `√e0` | `≤ √(2C0·e^{−Λ} + 2e^{−kf·log k})`, `Λ = C_Γ·m⁵·f·x^ε` | diagonal |

So `eta0` is the weakest of the three.

What sets `eta0` (`StatementPB.lean:206–209`) is the requirement `Pg ≤ exp(6b⁻⁷)` together with `δ ≤ b⁻⁷`:
- `Pg` is the local Gram/index factor at the two level primes, made small by `g_i ≥ (kb)⁸` (`StandingNumericalData.lean:126`; `NumPrice`).
- `δ` is the main-row correction `C(r+1)(C/Th)^f`, made small by the archimedean threshold `Th ≥ k^{c}` (`FinalSmall`).

`ε/8` is not intrinsic to `LinkS`. The same scale appears elsewhere as `Scale.delta1 = x^{−ε/8}` (`DataParams₂.lean:45`) and in `ChThin_at` (`Chosen.lean:47–49`).

---

## 4. Why the window involves `Γ²`, and where `m⁵·f·L` comes from (Q4)

**Γ is the auxiliary prime's "GamP".**
- `SizeData₂.Gam_eq : log (mem u).A.GamP = C_Γ·m⁵·f·L` (`DataParams₂.lean:174–176`).
- `gamOf_eq` gives `GamOf L = GamP` (`StandingHypothesesHoldFamily.lean:119–121`).
- `T_win` (`RhoDetPrime…lean:153–154`, `DataKernels.lean:157–159`) pins `T_u^{fk} ≈ D*/(du*·GamP²)` within a factor `(1+1/(fk))^{fk} ≤ e`.

`LinkAlt.lean:37` computes `exp 1 ≤ 3` locally, which is suggestive of this `e` factor, but the fact is not used afterwards. The same window appears as `Sz.SizeData.ChoiceOfT` (`StatementSz.lean:105–106`) and as `ChosenProviso` (`Chosen.lean:53–54, 75`).

**How Γ enters the Gram estimate.**
- The diagonal main term (equal-word scalar pairs) is only bounded by `gamB·dd` with `gamB = exp(C_B·m⁵·f·log b)` (`RowsPos.RowMainEqP`, `RowsPos.lean:43–47`). It is not bounded by `(1+δ)·dd` as in the off-diagonal case.
- The non-generic rows carry `epsNG = 2^{−(k−2rS−5)}·exp(C₄·m⁵·f·log b)` (`RowsConc.lean:49–52`).
- `DiagLP` needs `C_Γ ≥ max C_B C₄ + 1` (`RowsPos.lean:49–56`; `GamDef`, `AdmissibleBoundsFromSource.lean:47`). This yields ClDiag `≤ Γ·du²/D*`.
- The window's upper half turns this into `C0·du/Γ` (`diag_unproj`).
- So `Γ²` appears in the window precisely so that `Γ·(du/D*) ≈ Γ⁻¹`.

**Why the rank must be large.** `StandingHypotheses` requires `8C_Γ ≤ C'` and `C'·m⁵·f·L ≤ k` (`StandingNumericalData.lean:117`). `NumNG` (`StatementPB.lean:199–201`) uses this to get `2^{−k/2}·exp(C·m⁵·f·log b) ≤ e^{−k/5}`. So `k ≳ m⁵·f·L`, i.e. Γ's exponent, is the rank needed for the `2^{−k}` local saving to beat Γ.

The `m⁵·f·L` at code level is literally `(2r+2)⁵·f·log b` in `RowNG`/`SizeNumbers` (`StatementPB.lean:218, 232–233`). I did not trace why the exponent is 5 inside the proofs of `RowNGP`/`RowMainEqP`. Your exponents `m ≈ x^{1/2−ε/16}`, `f ≈ x^{2+8ε}`, `k ≈ x^{9/2+10ε}` are consistent with `k ≥ C'·m⁵·f·x^ε` by arithmetic, but I did not find them stated in the code I read.

---

## 5. Structural audit (Q5)

### Where the heavy lifting is

- **The abstract skeleton is generic Hilbert-space algebra**: `PB.Terms`, `PairBoundAbstract`, `diag_unproj`, `linkS_concl`. It turns an absolutely convergent term expansion of `Pu*Pu'` into the three bounds, given:
  - a Gram-matrix factorization with `GG ≤ Pg·Γ₁·I`;
  - row orthogonality;
  - corank positivity;
  - five numerical inputs (main / loops / non-generic / degenerate / count).
- **The actual mathematics is in those inputs**:
  1. `MainRow`: a Siegel–Weil mass identity, `RowMain ≤ (1+δ)·e₁·du·du'/D*`, with archimedean thresholds;
  2. loops and collisions with `s0 ≥ 2` or non-scalar pairs;
  3. non-generic corank-one pairs;
  4. vanishing of degenerate cross terms by unipotent averaging;
  5. the dimension count `Dall ≈ D*`.

  The main row is the step that produces the leading constant `1`; everything else is error terms.

### Generic versus arithmetic-specific

- The generic part is a standalone deterministic theorem: an operator family with a summable term decomposition, PSD local Gram bounds, and pairwise collision bounds yields "random-model" overlaps. It is stated without arithmetic in `StatementPB.lean:15–234`.
- Everything that yields `dd = du·du'/D*` is arithmetic-specific:
  - `D*` as volume × level index × formal degree;
  - `du` as a column count;
  - the requirement that the main row equals exactly this ratio.

### Things worth flagging

1. **`TheoremSSelected` is a hypothesis of `LinkAlt`** (`LinkAlt.lean:28–29`), and it *is* the off-diagonal clause (`ThmSOwn.lean:669–674`). The off-diagonal content lives in `OffK0Closed.lean:633–683`. Similarly `LoopRowS` (`sLp`) supplies the diagonal loop bounds.
2. **`LinkS` is conditional on the window.** It holds vacuously when the window fails (`StandingHypothesesHoldFamily.lean:650–651`). The window is supplied separately by `ChosenE`/`ChosenProviso`, which is a premise of `LinkGLOBAL` (`GlobalTheoremInputs.lean:162–164`).
3. **Siegel–Weil enters as a field** of `UnitaryGroupThirdPlaceHypotheses` (`ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean:64`). Where it is instantiated (`EveryCharacterOfLiteratureOfVWin.lean:708`), the instantiation ignores its `O` argument and returns the in-repo proof.
4. **The `[Fact …]` instances** used by `theoremS_leaves_of_carrierG` (`OffK0Closed.lean:632`) are discharged by global instances that call theorems, e.g. `FactsDS.lean:16–22` and `HermRepUnram.lean:9`. I did not audit those theorems.
5. **`SiegelMassRatio` (`adm12`) and `AdmissibleBoundsFromSource.admitted`** are not on the traced `ThmSOwn` path. Mass enters through `MassDataHyp`/`SWXS` instead.

### `ThirdPlaceSeries` chain versus `LinkAlt`

`link_alt_alt_bis` (`ThirdPlaceSeries/LinkAltAltBis.lean:16–48`) is the same proof as `link_alt`, with renamed selection types (`TwistSelection`/`SelectionSpectralCondition` instead of `TSel`/`SelS`). Both call `theoremS_transport_link_zero` identically. `TopShape.lean:55` uses the former and `CharacterBoxes/ShapeWin.lean:49` the latter. I found no mathematical difference.

---

## 6. What I did not trace

- The internals of `RowNGP`, `RowMainEqP`, `CountAllPointsClass` and `TypeP`. I stopped at their top-level proofs.
- The cores behind `pbApplied`: `t_MainRow`, `t_PairBound`, `localCores`, `globalCores`.
- The modules you named under `MainJoint`, `StatementJ/JC`, `SharpRecursion`, `RealInputsClosedAdmissibleSettings`, `OscillatoryIntegralBounds`, `LoopsCut`, `ThetaSupremumBounds` and `PeriodIntegrals` beyond the references above. I did not confirm their exact role on this path.
