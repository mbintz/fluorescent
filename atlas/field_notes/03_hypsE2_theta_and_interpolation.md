# Field Notes, Cluster 3: the `hypsE₂` engine (`EveryCharacterE`)

**How this was done.** I read the Lean code directly and rebuilt the import graph myself, with scripts kept in `/tmp/c3/` outside the repo. Nothing in the repo was edited. Every claim below cites the file and line where I read it. Where I'm interpreting rather than reading, I say so.

---

## 0. TL;DR

1. **`hypsE₂` is a short assembly theorem (about 25 lines) with no callers.** Neither `hypsE₂` nor `everyE₂` is used anywhere in the tree. The live route to `MainConclusion` goes through a renamed copy, `UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound`, at `…/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean:44`. That copy runs the same 10-step proof, but on a fresh structure `HypsAlt` (`…/ThirdPlaceSeries/Hyps.lean:22`) and with renamed constants. Its deeper layers reuse the original lemma library.
2. **The "42,387 exclusive files" is mostly a measurement artifact.** If you cut `EveryCharacterE` out of the graph, `MainConclusion`'s cone loses only **404 files**. 40,259 of the 42,387 are still reached by the live copy. So the cone is real, load-bearing code, but it isn't *owned* by `hypsE₂`.
3. **`ArakSwapCovol`'s "20,079 exclusive" is almost entirely CovolX.** 48,648 of its 49,769 cone files sit inside the CovolX anchor (`TopCovolSlim2Use`). Only 1,106 are exclusive once the anchors are excluded. `hypsE₂` never calls its theorem; it takes `CovolX` as a hypothesis. **But** this import is the *only* path to `Outright.lean`, which contains `moriwakiBig_outright` and `hsUse_outright`. The live final theorem calls both. Those 404 Arakelov/Hilbert–Samuel files are the real reason `EveryCharacterE` can't be deleted.
4. **34% of the exclusive files are one-line re-export wrappers.** 14,308 `…Statement.lean` files contain nothing but `first | exact @X | exact X | (intros; apply X <;> assumption)`. The remaining 28,079 files hold about 3.64M lines, roughly 156k theorems and 33k definitions.
5. **The mathematics, compressed.** Build families of CM-unitary arithmetic data (`D7`) over a growing parameter x. At each family point, construct theta-lift "rows": Hermitian lattices over a CM field, assembled from a 2-D grid of theta kernels along a Witt tower. Prove that these rows are
   - rational: a separating-functionals test, `RowTest`;
   - slope-bounded: `FUN` (μ_max), `L3` (covolume), `ON` (local indices);
   - linked to small-prime Galois data: `LinkN` and `BoundAtTwoThree`.
   
   A "global interpolation" mechanism (`Row`/`RL.At`/`Prm`) carries properties proved for large enough contexts to every family selection. The output is a 46-field `Hyps` record, which `plugAll` turns into L(χ,s) ≠ 0 for Re s > 1/2.

---

## 1. What `hypsE₂` states, and where it feeds

`lean/src/Development/AutomorphicArithmetic/ThetaCorrespondence/FockModels/EveryCharacterE.lean:41`:

```
hypsE₂ : S0.HypothesesUE → FunPr.Hypotheses₂ → ThetaIntegralsAgree → LocalMatching → CovolX
       → ∀ hL : LocalLanglandsGL,
         (∀ cDep, RL.At (prm1 hL cDep) (… Closed 𝒞 (BoundAtTwoAndThreeForFamily) …))
       → Nonempty (Hyps S0.NL DRS)
```

**The hypotheses are large, and they are real statements.**
- `S0.HypothesesUE` has **71 fields**, each a published theorem stated as a `Prop`. Examples: Clozel, Green, Chebotarev, Bhatt–Scholze, two different Siegel–Weil formulations, Casselman–Wallach, Labesse–Waldspurger, plus `litN`, `nLink`, local Tate duality and others (`…/Definitions/Divisors/HypothesisBundleConversions.lean:56`).
- `FunPr.Hypotheses₂` has **62 fields**, including `linnik`, `rallisInnerProductConvergent`, `howeDualityReal`, `siegelSetUnitary` and `minguezThetaGL` (`…/Definitions/Divisors/DiscreteSeriesHermitianUnique.lean:67`).
- I checked a sample: `LocalLanglandsGL` is a full ∃!-reciprocity-map statement with about 15 compatibility laws (`…/PublishedTheorems/AutomorphicForms₂/LocalLanglandsGL.lean:96`). `SiegelWeilUnitaryConvergent` equates an Eisenstein value with a theta mean (`…/SiegelWeil₂/SiegelWeilUnitaryConvergent.lean:18`).
- There is no `sorry` and no `axiom` anywhere in `lean/src`. No `Prop` is defined as a bare `True`.

**The target.** `Hyps N DR` (`…/Definitions/GlobalTwisting/APerTw.lean:23`) is a `Type 1` record with **46 fields**, starting with a family class `𝒜`, a raw selection `σ` and a function `cT`.
- Almost every field has the shape `Closed (D3 3 𝒜) (fun Fm _ => ∃ x0, ∀ x ≥ x0, ∀ i, P(Fm.D x i))`.
- Two fields carry the parameters: `rRows : R1.H_rRows DR 𝒜 σ` takes the row condition `DR := DRS` (`…/GlobalTwisting/DRS.lean:21`), and `nRest : N (D3 3 𝒜)` takes `N := S0.NL = Closed 𝒞 LinkN` (`…/GeometricWeakTiesOfStrong.lean:36`).

**The consumer.** `plugAll` (`…/CharacterBoxes/EveryCharacter.lean:9–21`) turns `Nonempty (Hyps …)` into `ZeroFreeAll` via `shape_of` and `zeroFreeAll_of_topG (la := 3/2)`. It then applies `imprimitive` to reach `UpperTheory.EveryCharacter`: for every Dirichlet χ and every s with Re s > 1/2, `LFunction χ s ≠ 0` unless χ = 1 and s = 1. `everyE₂` (`EveryCharacterE.lean:67–71`) is exactly `plugAll ∘ hypsE₂`, with the 2-and-3 hypothesis discharged by `boundAtTwoThree_at_prm_of_prints P.nLink`.

---

## 2. The objects you need to read the proof

| Object | Where | What it is |
|---|---|---|
| `D7` | `Formalism/LocalRingCardinality/RhoDetPrimeEqMuTildeMulChiPow.lean:76` | One "arithmetic point". It packages ranks `R`; a CM host `E/F` (`Host`, `DataHost.lean:39`) with auxiliary primes q, d, g₀, g₁ and pde ≡ 1 mod 15; a 2-power tower `QS`; a conductor ideal `ccK`; Hermitian spaces; row data `what₂` over a Galois, totally complex `LL`; Harish-Chandra parameters `hc`; words `u`; members (column chains, period maps); divisor data. |
| `primeClass` | `DataHost.lean:33` | Sorts primes into ram2 / ramQ / ramD / splitK (when (−d/p) = 1) / signal / inert. This is why 2 and 3 get special treatment (§6). |
| `FamP eps`, `FamClass`, `Closed` | `Formalism/SharpRestriction/ParConsts.lean:31`, `ParamsHeightRankConstant.lean:157,159` | A family is a map x ↦ (D x i, L x i) with about 30 coherence fields. `Closed 𝒞 P` means: there is ε₁ > 0 such that for every ε ≤ ε₁ some constant package K makes every `K`-large family in 𝒞 satisfy P. Everything is "uniform for x large". |
| `LinkN` | `Formalism/SharpRestriction/GlobalTheoremInputs.lean:45` | `etaSum L j ≤ dZ0 j · (C·(f·m·b·L² + log²x·Nc) + Σ_l shaLen·log l)`: twisted local η-weights are bounded by a polynomial plus the lengths of Sha (Tate–Shafarevich groups). |
| Bundles, `Row`, `RL.At`, `Prm` | `ValidForConstructedPointClassesEventuallyWorking.lean:268`; `GoodReductionCondition.lean:45`; `ThetaChr.lean:26,117` | `Row Q Lk H` says: some bundle predicate `E κ` holds *eventually in κ* at every linked bundle built at slot `Q`, and any family selection consistent with `E` satisfies `H`. `Prm` = (R-position, `NExt` extra data at the N-stage, `SExt`, geometry predicate). `RL.At p r := Lg1 KPx (IsBuiltE p.s) (IsGoodE p.s) (r · (IsLinked p))`. |
| `prm1`, `NEl`, `NEo`, `NEa` | `MultW.lean:44`; `SettingsFormsExistList.lean:26`; `ExistsUnlocalizedSaturatedState.lean:32`; `GKeyFin.lean` (`NEa`) | Parameters grow by stacking product types: `NEl` adds a `ListPin` (a grid whose field contains `LL0`, with full λ-ties); `NEo` adds `Org` (comes from a saturated, untwisted pre-state); `NEa … A` adds `PLift (A K B f T)`. |
| `IndefData` rows and slopes | `Formalism/LocalToGlobal/IndefiniteForms/IndefSide.lean:287,315,318,331` | `muMaxRR := HN.muMaxDef …` is the Arakelov maximal slope. `FUN : μ_max(RR) ≤ hh − meanLog κ`; `L3 : lcv(XW j, M j)/D ≤ l3 j` (log-covolume); `ON` bounds local indices at twisted places. |
| HN slope theory | `Formalism/HarderNarasimhan/Statement.lean:29,47,54`; `StatementPl.lean:67` | Stuhler–Grayson theory for Euclidean and Hermitian lattices: `muMax`, `muMin`, `hnStep`, the HN polygon; `DegSupermod` (degree is supermodular); `MuChar` (variational characterisation of μ_max/μ_min). |
| `large₂`, `EvLgG` | `…/AutomorphicMembership/CmQuadraticFormEqAlternatingForm.lean:100,138` | "Generic over big fields": there are **finite sets of algebraic numbers** S₁, S₂, finite prime sets P₁ and avoid-sets A such that every base B containing S₁ ∪ S₂, twisting at P₁ and avoiding A satisfies p. `EvLgG p` = eventually in the context, `large₂ K (p K)`. |
| `GridData`, `GridA` | `Formalism/…/GridData` (around line 335); `…/AutomorphicMembership/GKeyFin.lean:30–61` | See §6. |

---

## 3. The proof of `hypsE₂`, step by step

All line numbers are in `EveryCharacterE.lean`. The single real constant is `CF := max CF0 CF1`. It serves both as the grid-gap constant and as the dependence constant `cDep` in `prm1`.

| # | Line | Produces | Mathematical content (my reading) | Main inputs |
|---|---|---|---|---|
| 1 | 44 | `hS : FunctionalsSeparate` | For any nonzero row vector `w`, some automorphic coefficient functional (Ψ ∈ `Cols`, i.e. forms on `G.V(top 0)` at level `K⁺`) gives a **nonvanishing theta integral** `fPsiPhi ≠ 0`, for all constants CF ≥ **6510** and x large (`LevelPlusSubgroup.lean:65,83`). | `functionalsSeparate_free` (`RealBranch.lean:237`): the archimedean branching input `realInputE_holds` (line 231), unramified Howe duality `howeUnram_holds` (`SatakeParameters/RhoMemOfMkEq.lean:250`, proved, not assumed), Siegel–Weil. Its proof (`RealBands/FunctionalsSeparateFromRealInput.lean:7`) goes level tower → multiplicity spaces → convergence → archimedean period ≠ 0 → theta surjectivity → Bessel-period nonvanishing → separation. |
| 2 | 46 | `hRat : S0.RowRat` | **Rationality of theta rows.** `RowTest X`: finitely many ℂ-functionals ψᵢ separate `X.EE`, and `ψᵢ(Θ_t(j_R x)) ∈ v₀(K)` for every K-rational x (`Formalism/LocalToGlobal/IndefiniteReal/RationalAdjoints/RatZOfTests.lean:18`). In words, the theta map preserves K-structures. | `rationality_of_theta_hypotheses` (a wrapper for `RowTestAssembly.rowTest_atDat_of_join`), using SiegelSet, HoweDualityReal, Green, `JoinOut` (toric denominators, lattice-norm transport, zeta denominators), Hecke–Tate FE, `hA`, `hM`, `hS`. |
| 3 | 48 | `hFit : Fun0Fit Fld` | **Slope bound.** For every CF ≥ CF0, each family point carrying a grid satisfies `FUN`: μ_max(RR) ≤ hh − meanLog κ (`TwistedPlaceChoiceLiesOverPair.lean:306`). | `fun0Fit_of_join` → `fun0Fit_close`, plus `LamLow` from `ontoX_and_lamLow_of_classicalTheoremsUE`. |
| 4 | 49 | `∃ CF1, ∀ CF ≥ CF1, EvLgG (GridA CF)` | **Every evaluation grid can be completed to a full, field-rational theta choice, generically** (§6). | `evLgG_gridA_of_join` (`EvLgGGridAOfJoin.lean:88`): Weil-rep existence, `isEx_of_separates hS`, the `nf*` algebraicity lemmas, `lNe_of_functionalEquation` (Hecke L ≠ 0 from FE plus boundedness in strips), `gKeyFin` (finitely many grid keys), transfer lemmas `carry*`/`tr*`. |
| 5 | 52 | `∃ CF0, … → RL.At … FunctorialityCondition` | Promote (3) from family points to all linked bundles at the GridA-strengthened parameter. | `rowFun_at_gridA`, which lives in **`LargeFieldLinkedBundlesExist.lean`**. The file name doesn't match its content. |
| 6 | 55 | `Open0 (prm1 hL CF)` | Twelve bundle-row properties (`GeometricWeakTiesOfStrong.lean:40`): period admissibility, λ-positivity, divisor, decomposition, J-selection, tie, label, good reduction, geometric weak compatibility, multiplicity (`MIstar2`: period ratios are units), κ, and the differential/`DRS` row. | `open_of_hypothesesUE` (`DivisorProofs/OpenFirstParametersOfPublishedUE.lean:26`). Each field has its own published-input combinator: trace-formula inputs for λ and κ, local Langlands with Green and depth zero for good reduction, ray class fields for geometry, Siegel–Weil with doubling and strong approximation for multiplicity. |
| 7 | 56–59 | `Open0` at the stronger parameter | **Monotonicity.** Properties survive when more data is pinned at the N-stage (`NEa(NEo) → NEl`). | `open_and_linked_of_stronger_extension` (`GlobalInterpolation/OpenAndLinkedMonoExtension.lean`). |
| 8 | 60 | `hFun` | `FUN` at the strengthened parameter. | Step 5 applied to step 7. |
| 9 | 62 | `hL3 : RL.At … CovolumeBound'` | **Covolume bound `L3`** at linked bundles. | `linked_bundles_l3_of_open` → `eventual_L3_of_covolume` (`EventualL3OfCovolumeTied.lean:10`), which consumes `hX : CovolX` (`CovolXOfCovol.lean:278`, "eventually L3 at tied points"). |
| 10 | 65 | `Nonempty (Hyps S0.NL DRS)` | Final assembly (§4). | `nonempty_hyps_of_classicalTheoremsUE`. |

---

## 4. Inside the final assembly (`NonemptyHypsOfPublishedUE.lean:30–46`)

1. **Bundles exist.** `linked_bundle_construction_exists` → `member_bundles_large_ue` (`LinkedBundleConstructionExists.lean:25`).
   - `RowRat` feeds `doubling_inputs_imply` and then `exists_unlocalized_saturated_state`. Concretely, there is a starting state with no local twisting and all η = 0 (`ExistsUnlocalizedSaturatedState.lean`, `def ExistsUnlocalizedSaturatedState`).
   - `EvLgG A` lets bundle membership survive when the GridA pin is added (`member_preserved_large_grid`).
2. **2-and-3 bound → LinkN.** `NLink.Final.main` (`InertiaEigenvalues/LinkOfClosedAtFamily.lean`) turns `BoundAtTwoAndThree` at primes 2 and 3 into the full `LinkN` closure. It uses local Tate duality, local Euler characteristic, local finiteness, depth zero and LLC, and needs `maxHeartbeats 4000000`.
3. **Monotonicity again** moves `Open0` and `NL` to the strengthened parameter.
4. **All rows.** `allRows_of_open0` (`GlobalInterpolation/LinkedBundlesOfCasselmanWallach.lean:52`) builds an `AllRows` record with fields named like `Hyps`. Notably, `rRows` is assembled from `hPA ∧ hDivG ∧ good ∧ geo ∧ L3 ∧ FUN ∧ mi ∧ kap ∧ df` through `StageZeroRow.row_rRows_stage0`.
5. **Choose a class and selection.** `nonempty_hyps_of_allRows` (`GlobalInterpolation/NonemptyHypsOfAllRows.lean:14`) calls `UpperTheory.Top.classSel` to pick the family class and selection, and fills the remaining fields from outright lemmas (`litThin`, `wuDecayOfGap`, `rowsFinDim_link`, `rowsPos_typeP`, `genusMassAt_two`, …).

---

## 5. The mathematical story, stripped of boilerplate

This is my interpretation, grounded in the definitions above.

**(a) Theta grids and tower matching.** A `GridData` is a 2-D diagram of Hermitian spaces over the CM field. Its vertices are `.grid i j`, `.core i` and `.top j`; its arrows are `.right`, `.down`, `.coreUp/.coreDown` and `.col`. Each arrow is a (small space, big space) dual pair carrying a theta kernel `thetaKO`, realised in the **Fock model**: `fock`, pure tensors `pureTensorO`, vacuum vectors `IsVac` (`GridData.Weil.ker/kerA/fock/datum`). The "rows" are what you get by integrating automorphic coefficients against these kernels.

**(b) Tower steps cost Hecke L-values.** `ThetaIntegralsAgree` (`BlockTheory/DivisorBase/WeilTensorModels.lean:585`) has two step laws:
- `StepBeta` (q → q−1, the `.down` direction; line 559): the constants c and c₁ for U(a, b+2) and U(a, b) satisfy `c · L^{S₀}(χ, (a−b−2)/2 + 1) = u · c₁`, where u is an explicit unit-times-`stepFac` ideal-value factor.
- `StepAlpha` (p → p−1; line 571): the analogous law.

These are Rallis-inner-product / Kudla–Rallis tower relations. `LocalMatching` (line 581) supplies matched local data. Both are *hypotheses* of `hypsE₂`. Downstream they are discharged by `theoremK_head2` (`WeilBound/ThetaLifts/Reductions/FiniteClosure/TheoremKOfMod.lean`), from `EisBL` and `SiegelWeilStd`.

**(c) Rationality from separating functionals.** `FunctionalsSeparate` plus theta-integral rationality give `RowTest`: theta values of rational vectors are rational. This is a Shimura/Harris-style algebraicity mechanism, but phrased as "finitely many functionals separate, and each one takes rational values."

**(d) Rows are Hermitian vector bundles on Spec O_K, and the proof needs slope control.** Three bounds are used:
- `FUN` bounds μ_max of the row lattice;
- `L3` bounds its log-covolume;
- `ON` bounds the local index at each twisted place.

The slope theory underneath is genuine Stuhler–Grayson Harder–Narasimhan theory for Euclidean lattices: `muMax`/`muMin`, the HN polygon, supermodularity of degree, and the μ-characterisation. `L3` comes from Arakelov-geometric arithmetic bigness (the CovolX/Moriwaki branch).

**(e) Global interpolation, i.e. genericity by finiteness.** Every property is proved "eventually in the context and generically over big coefficient fields" (`large₂`). The exceptional sets are finite sets of **algebraic** numbers plus finite prime avoid-sets, in the spirit of Chebotarev. That is why the `nf*` algebraicity lemmas (`nfChars`, `nfRoot`, `nfPhase`, `nfJet`, `nfRatio`, `NFSq`) and `GKeyFin` (finitely many grid keys) sit at the heart of step 4. Each parameter strengthening (`NEl → NEo → NEa … GridA`) is safe because of the monotonicity lemma `open_and_linked_of_stronger_extension`.

**(f) Archimedean branching.** `RealInputE` (`RealBands/BranchDefs.lean:11`) makes the following claim:
- **Setting.** Discrete series π of U(p,q) on n+1 variables and σ on n variables, with Harish-Chandra parameters λ, μ satisfying the `Par` conditions (`TwistedInnerProducts/ProjExists.lean:52`): n ≥ 3, interlacing, gaps ≥ 1000(n+1)³, signature constraints.
- **Conclusion.** There are a lowest-K-type vector v₀, a group element g₀ with ‖g₀‖ ≤ (8(n+1)B)^{10(n+1)} (that bound appears in the `ProjLarge` component), and c > 0 such that the branching integral `∫ conj⟨v, π(h)v⟩·⟨b, σ(h)w'⟩ dh = c⟨w',w'⟩⟨b,w'⟩`.
- **Explicit decay.** `L¹ ≤ c·big·colLen^{−(2n+7)}`, plus derivative bounds and `|⟨v,π(g)v⟩| ≤ A·‖g‖^{−20(n+1)²}`.

This is a quantitative, nonvanishing archimedean Gan–Gross–Prasad-type local period for discrete series far from the walls. It is proved outright (`realInputE_holds`).

---

## 6. The two specific questions

### Why is `BoundAtTwoAndThreeForFamily` special?

**Definition.** `BoundAtTwoThree L ρ C` (`…/NonGaloisDescent/BoundAtTwoThreeFamily.lean:52`) requires the following at local places i with residue characteristic l = 2, or l = 3 with 3 ∉ `host.small`:

```
vcc(i,π) ≤ sPi(i,π) + midF(L,C) + VVr + vhE + epsL
midF = C·f·m·b·log x + C·x^C·large₂²        (line 33)
```

`BoundAtTwoAndThreeForFamily` (`BoundAtTwoAndThreeForFamily.lean:56`) is the family version, gated on a `Setup`: Fontaine data, hub data, `ShaFinOdd`, and so on.

**Why 2 and 3.**
- 2 is always in `host.small`, because the 2-power tower `QS` has 4 | QS. So at 2 the level exponent satisfies `s0 ≥ 2` (`ResidueCharacters/RowTwo.lean`).
- 3 is never q, d or gₖ (`ThreeHost.lean`: q ≠ 3 and q ≥ 11). When 3 ∉ small, `s0 = 1` and (−d/3) = 1 (`RowThree.lean`).

Both cases go through `bound_smallPrime_of_splitBound_cyclotomic…` with explicit constants **6000 / 30000**. Primes 2 and 3 are exactly where the general p-adic Hodge machinery (Wach-module and Fontaine-style bounds, `Formalism/WachLatticeTwists`: 202 exclusive files in this block) doesn't apply directly, so they are handled by hand.

**Status.** It's a *hypothesis* of `hypsE₂`, but `everyE₂` discharges it unconditionally. `boundAtTwoThree_at_prm_of_prints` (`ResidueCharacters/ClosedOfAll.lean:22`) proves it for **every** family via `closed_of_all`, with a trivial constant package (`⟨1, one_pos, … ⟨0, fun _ => 0, …⟩⟩`). The `RL.At`/bundle-point wrapper therefore carries no information here. My guess is that this is a historical seam, kept so the copied chain could substitute `BoundAtTwoThreeFamilyFonAlt` (`ThirdPlaceSeries/BoundAtTwoThreeFamilyFon.lean`).

**Where it is used.** `NLink.Final.main` turns it into the `LinkN` (Sha-length-weighted η) bound. It is the small-prime input into `Hyps.nRest`.

### What is `GridA`?

`GridA CF K B f T` (`GKeyFin.lean:61`) says: for **all** downstream stages (columns `C`, row-rest `W`, divisor stage `V`, S/N/GJ stages), `GridAt K.s CF X f (T.set f)` holds (line 49). Unpacked:
- for every size datum with `SqTop.Rec`, every realisation `R`, face `F` and Hida setting, with twisting off q₀ and χ-values in the prescribed Hecke-character set Ξ,
- **every** grid G₀ with gap constant CF can be replaced by a grid G **with the same key** (place v₀ of F, the place above it in E, and the Hecke characters χ_H; `gkeyOf`),
- such that G is `Full` (line 43): there is a complete theta choice ⟨W, M, ρ, ξ, …⟩ that `Is` valid, is `FieldOK`, and satisfies `SqIn` (the needed square roots lie in the coefficient field).

`EvLgG (GridA CF)` says this holds generically for large contexts. `GKeyFin` (line 30), finitely many keys for each pre-base and gap, is what keeps the exceptional set finite. In plain terms, GridA means "evaluation grids are realisable by rational theta data, up to finitely many bad choices."

---

## 7. Why 42,387 files? Cone anatomy

Method: I parsed the import graph of all 175,187 modules. `cone(EveryCharacterE) = 100,723`, and removing the six anchor cones (plugAll, VWinCore, CovolX, Row0b ×2, LLC) leaves **42,387**, matching Stage 0.

**Attributing the 42,387 files to the children of `EveryCharacterE` that reach them (anchors removed):**

| Reached only from these children | Files | Dominant directories |
|---|---:|---|
| NonemptyHyps ∩ OpenFirst | 12,494 | `Proofs/FlagMeasures` 3,013 · `DecoratedLatticeProofs` 2,069 · `SatakeParameters` 1,160 · `IwasawaDecomposition` 768 · `JetHarmonics` 755 |
| NonemptyHyps only | 7,818 | `InertiaEigenvalues` 2,690 · `IwasawaDecomposition` 2,090 · `SatakeParameters` 848 |
| NonemptyHyps ∩ OntoX | 3,602 | `DivisorProofs` 992 · `InertiaEigenvalues` 503 |
| Fun0Fit ∩ Rationality | 1,876 | `TwistedOperators` 992 · `DivisorProofs` 620 |
| ClosedOfAll ∩ NonemptyHyps | 1,388 | `InertiaEigenvalues` 859 · `WachLatticeTwists` about 80 |
| RealBranch only | 1,124 | `TwistedOperators` 916 · `HolomorphicDiscreteSeries` 62 |
| ArakSwapCovol only | 1,106 | `GroundTheory/HeightsAndTheta/Heights`: ComplexAnalyticSets 483, HilbertSamuel 138, KleimanAmpleness 92 |
| Fun0Fit only | 1,001 | `DivisorProofs` 865 |
| TheoremKOfMod only | 615 | `WeilBound/ThetaLifts/*` |
| PrismaticDieudonneHodge only | 547 | `DivisorProofs` 538 |

**Inside NonemptyHyps (33,353 files once the anchors are removed):**
- Open0 proof: 19,370. Its two heavy fields are the `MIstar2` multiplicity row via `diagonalRow_of_siegelWeil_unitary` (12,848) and `geometric_zero_condition_all` (12,049).
- Linked-bundle construction: 13,043.
- `NLink.Final` (p-adic Hodge theory and Galois cohomology): 7,797.
- OntoX/LamLow: 6,802.

These overlap.

**Corrections to the Stage 0 numbers:**
- **`ArakSwapCovol` 20,079 → 1,106.** Stage 0's figure excludes sibling cones only. Its cone is `TopCovolSlim2Use` plus `Moriwaki…Outright`, and 48,648 of its 49,769 files are in the CovolX anchor.
- **NonemptyHyps 8,733 → 7,818** once anchors are excluded.
- **"Exclusive 0" for children such as `OpenFirstParametersOfPrintsUEStatement`** only means they are nested inside NonemptyHyps. That child alone reaches 19,370 of the exclusive files.
- **Not really owned by `hypsE₂`.** The live copy (`SiegelEisensteinSecondTermHypotheses`, with `EveryCharacterE` banned from the graph) reaches 40,259 of the 42,387. Only 404 `MainConclusion` files depend on `EveryCharacterE` at all: 386 in `GroundTheory/HeightsAndTheta/Heights`, reached via `ArakSwapCovol → Outright.lean`.

**New machinery vs. formalised background:**

| Kind | Files | Lines / theorems |
|---|---:|---|
| Wrappers (one-line re-exports) | 14,308 | 207k lines |
| Real files | 28,079 | 3.64M lines; about 156k theorems, 33k defs; median file 50 lines, p90 222 |

- **Background theorems proved outright inside this cone, not assumed:**
  - Moriwaki bigness and arithmetic Hilbert–Samuel (`Outright.lean:9,13`, about 1,000 real files under `GroundTheory/HeightsAndTheta`);
  - unramified Howe duality (`RhoMemOfMkEq.lean:250`);
  - the prismatic Dieudonné/Hodge statement, which yields Fargues exactness (`PrismaticDieudonneHodge.lean`; 547 files);
  - Breuil–Kisin, A_inf and crystalline lattice theory (`InertiaEigenvalues/ExistsBreuilKisinModuleBasisOfFCrystal.lean:562`, `BreuilKisinFullFaithfulnessLatticeMorphism.lean:121`, `AinfInvPiModXiPowBoundedDenominator.lean:92`, `CrystallineLocalCoefficients.lean:81`);
  - Wach modules and Herr complexes (`Formalism/WachLatticeTwists`);
  - "Theorem K" tower constants (`TheoremKOfMod`);
  - Green's character theory (`SumRangeEqRoots.lean:225`).
- **Background theorems assumed as `Prop` hypotheses:** 71 + 62 published statements, plus LLC, CovolX, ThetaIntegralsAgree and LocalMatching. Most are discharged downstream in `EveryCharacterOfLiteratureOfVWin.lean:215–811`, outside this cluster.
- **New, bespoke machinery:** the `D7`/`FamP`/Bundle/`Row`/`RL.At`/`Prm` interpolation framework; `GridData` and `GridA`; `IndefData` rows with their slope bounds; the Open0 bundle rows (notably `MIstar2` from Siegel–Weil diagonal rows); member-bundle construction; the `NLink` assembly. My rough estimate is that this is the majority of the 28k real files, because the background-theorem areas listed above add up to only a few thousand files. That is an estimate, not a measurement.
- **Directory names are not a guide.** For example, `IwasawaDecomposition/` holds Galois representations, idempotents and geometric zero conditions. Use file names instead, which are descriptive.

---

## 8. Load-bearing ideas worth reusing outside GRH

1. **Harder–Narasimhan slope theory for Euclidean and Hermitian lattices** (`Formalism/HarderNarasimhan`, 43 files; `LatticeSlopes`, 18). It is general (any ring R, any lattice `ρ : V →+ E`) and Mathlib-shaped. These files are shared with the anchors, not exclusive.
2. **Quantitative archimedean branching (`RealInputE`):** explicit decay exponents and positive branching constants for U(n+1) ⊃ U(n) discrete series. This could be useful for Gan–Gross–Prasad and Ichino–Ikeda work.
3. **Genericity by algebraic finiteness (`large₂` / `EvLgG` / `GKeyFin`):** a reusable pattern for "true outside a finite, algebraically defined exceptional set, over big enough coefficient fields."
4. **Fock-model theta grids with the StepAlpha/StepBeta tower laws:** a formal framework for chains of seesaw identities.
5. **Integral p-adic Hodge theory** (Breuil–Kisin, A_inf, Wach modules, Herr complexes) as stand-alone libraries.
6. **`Formalism/WachLatticeTwists/Statement.lean`:** clean DVR length inequalities (`StatRowColength`, `SubmoduleLengthBound`, `StatDualColength`).

---

## 9. Brittle joints and oddities

- **Dead entry point.** `hypsE₂` and `everyE₂` have zero callers. The live chain is the `…_alt` copy (`SiegelEisensteinSecondTermHypotheses.lean:44,69`; `TopPlug.lean`), built on fresh types: `HypsAlt` instead of `Hyps`, `DefiniteSideCondition` instead of `DRS`, `parametersOfDependence` instead of `prm1`, `RecTExists` instead of `LocalLanglandsGL`, `CovolumeBoundOfX` instead of `CovolX`. Deep lemmas are shared: `realInputE_holds`, `evLgG_gridA_of_exGrid`, `nfAll_of`, `VolRatioFromSiegelWeil.volumeRatio`. Any audit of the live proof should start from the copy, not from `hypsE₂`. There are 2,251 files in `ThirdPlaceSeries/`.
- **`EveryCharacterE` survives only as an import hub.** The live `every_character_of_literature_of_vWin` (`EveryCharacterOfLiteratureOfVWin.lean:810–811`) calls `moriwakiBig_outright` and `hsUse_outright`, and those are reachable only through `EveryCharacterE → ArakSwapCovol → Outright.lean`. Deleting `EveryCharacterE` would break the build for that reason alone.
- **`CovE` (`EveryCharacterE.lean:73–86`) is unused.** Its 13 fields are exactly the 16 hypotheses of `topCovolSlim2_free` minus {MoriwakiHS, MoriwakiBig, FarguesExact}, which are the three discharged outright by `Outright.lean` and `PrismaticDieudonneHodge`. It looks like the start of a CovolX-free variant ("everyE₃") that was never written.
- **`topCovolSlim2_free` ignores two of its arguments.** It takes the Moriwaki statements and drops them (`fun h₁ h₂ hPL _ _ => …`, `ArakSwapCovol.lean:12–14`).
- **Wrapper tactic.** `first | exact @X | exact X | (intros; apply X <;> assumption)` appears in 14,308 files, which strongly suggests machine-generated scaffolding. It also hides elaboration failures behind fallbacks.
- **File names don't match contents.** `LargeFieldLinkedBundlesExist.lean` contains `rowFun_at_gridA`; the actual linked-bundle existence result is `member_bundles_large_ue` in `LinkedBundleConstructionExists.lean`.
- **Positional projections encode parameter inclusion.** Proofs like `(fun _ _ _ _ _ _ _ _ _ _ _ _ _ x => ⟨x.1.1⟩)` (lines 58, 61, 64) project through the nested products `NEa(NEo) ⊂ NEo ⊂ NEl ⊂ NEb`. Reordering any `NExt` would silently break them.
- **Large heartbeat budgets.** `maxHeartbeats 4000000` (`LinkOfClosedAtFamily.movable_pin`), `2000000` plus `synthInstance 400000` (`ExistsUnlocalizedSaturatedState`), and 1,000,000 in every wrapper.
- **Two distinct Siegel–Weil hypotheses.** `Published.SiegelWeilUnitaryConvergent` (Eisenstein value = theta mean) and `HeckeCharacterZeroLocus.SiegelWeilU.SiegelWeilUnitaryConvergent` (theta mean = ∏ local densities; `Formalism/UnipotentAdelicQuotients/SiegelWeilUnitaryConvergent.lean:46`) are separate fields of `HypothesesUE`.
- **Magic constants.** CF ≥ 6510 (`FunctionalsSeparate`), 6000/30000 (rows at 2 and 3), gaps ≥ 1000(n+1)³, decay exponent 20(n+1)², and `VWin := ∀ ψ, VWinAt ψ 401`.
- **One constant, two roles.** A single `max CF0 CF1` serves as both the grid gap and the "dependence" constant of `prm1`. That's fine logically, but it couples the two sub-arguments.

---

## 10. Leads for Wave 2

1. **Audit the live `…_alt` chain against `hypsE₂`.** Diff `HypsAlt` against `Hyps` and `DefiniteSideCondition` against `DRS`. Check whether `final_alt_alt` really drops `DepthZeroWild` (compare `CFinal.lean:20` with `NonemptyHypsOfPublishedUE.lean:36`). Confirm that `RecTExists` and `CovolumeBoundOfX` are at least as strong as `LocalLanglandsGL` and `CovolX`.
2. **Biggest sub-cones to open next.** `diagonalRow_of_siegelWeil_unitary` (5,799 files; `RowDiag`/`RankMu` in `LatticeFrames/NotInhAbsOfGamLe.lean:56` and `KerInclOn.lean:26`) and `geometric_zero_condition_all` (12,049).
3. **Check the `StepAlpha`/`StepBeta` L-value factors against the published tower formulas.** Specifically the `charL` evaluation points and the `stepFac` ideal powers in `WeilTensorModels.lean:559–581`.
4. **Check that `RealInputE`'s constants are plausible.** Compare the exponents in `ProjLarge` and `RealInputE` with known matrix-coefficient decay for discrete series.
5. **Pin down where `Hyps` fields become analytic content.** Trace `shape_of`/`TopG` → `zeroFreeAll_of_topG` (`CharacterBoxes/ZeroFreeAllOfTopG.lean:26`) to see which of the 46 fields actually reach the explicit formula (`Formalism/SharpRestriction/RamificationFrobenius/…/ExplicitFormulaErrorOfHostConditions.lean`).
6. **Fix the cone metric.** Recompute Stage 0's "exclusive" numbers against the anchors and with nested children folded into their parents. Better still, track *term-level* use (which constants appear in proof terms) rather than imports, because import cones overstate ownership here by about 100×.
