# Stage 0: Automated Import-DAG Cartography of `lean/src/`

Purely mechanical extraction from the Lean 4 import graph (zero manual categorization).

## 1. Global Reachability

- Total `.lean` modules in `lean/src/`: **175,187**
- Reachable from `Main.lean`: **175,187**
- Reachable from `Supplements.Kernels.MainTheorems` (RH + GRH): **175,179**
- Reachable from `MainConclusion.lean`: **175,174**
- In `Main` but outside `MainTheorems` (supplements/corollaries): **8**
- Unreachable from `Main`: **0**

### Modules in `Main` outside `MainTheorems` (by 2nd-level dir)
- `Development/AutomorphicArithmetic`: 4
- `Supplements/Kernels`: 2
- `Statements`: 1
- `Main`: 1

## 2. Cone Sizes of Top-Level Spine Anchors

| Anchor | Module | Transitive Cone Size | Top 3 subsystems in cone |
|---|---|---:|---|
| **MainConclusion** | `Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion` | 175,174 | `Development/AbelianVarietyTheory` (99,187), `Development/AutomorphicArithmetic` (18,425), `Development/AutomorphicSpectrum` (15,147) |
| **EveryCharacterOfLiteratureOfVWin** | `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.EveryCharacterOfLiteratureOfVWin` | 151,286 | `Development/AbelianVarietyTheory` (89,378), `Development/AutomorphicSpectrum` (12,740), `Development/AutomorphicArithmetic` (9,339) |
| **EveryCharacterE (hypsE2 + plugAll)** | `Development.AutomorphicArithmetic.ThetaCorrespondence.FockModels.EveryCharacterE` | 100,723 | `Development/AbelianVarietyTheory` (60,785), `GroundTheory/HeightsAndTheta` (6,379), `Development/AutomorphicSpectrum` (6,367) |
| **CharacterBoxes.EveryCharacter (plugAll?)** | `Development.AutomorphicArithmetic.CharacterBoxes.EveryCharacter` | 14,299 | `Formalism/PeriodIntegrals` (3,193), `Formalism/LocalToGlobal` (2,576), `Formalism/SharpRestriction` (2,038) |
| **VwinOfRow** | `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.VwinOfRow` | 157,604 | `Development/AbelianVarietyTheory` (92,324), `Development/AutomorphicSpectrum` (13,540), `Development/AutomorphicArithmetic` (11,840) |
| **TopMainZj (VWin literature seam)** | `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.TopMainZj` | 157,603 | `Development/AbelianVarietyTheory` (92,324), `Development/AutomorphicSpectrum` (13,540), `Development/AutomorphicArithmetic` (11,839) |
| **WindowBoundOfLiteratureLevel (vwin core)** | `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.WindowBoundOfLiteratureLevel` | 55,067 | `Development/AbelianVarietyTheory` (21,935), `Development/AutomorphicArithmetic` (10,580), `Development/AutomorphicSpectrum` (4,526) |
| **TopCovolSlim2Use (CovolX)** | `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.TopCovolSlim2Use` | 50,236 | `Development/AbelianVarietyTheory` (21,277), `Development/AutomorphicSpectrum` (5,928), `GroundTheory/HeightsAndTheta` (5,366) |
| **RowSrc (Row0b Galois LG)** | `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.RowSrc` | 66,168 | `Development/AbelianVarietyTheory` (31,624), `Development/AutomorphicArithmetic` (5,982), `Development/AutomorphicSpectrum` (5,655) |
| **GaloisRepresentationsOfThetaLift** | `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.GaloisRepresentationsOfThetaLift` | 61,081 | `Development/AbelianVarietyTheory` (30,482), `Development/AutomorphicArithmetic` (5,204), `Development/AutomorphicSpectrum` (4,758) |
| **TLiftK (ThetaParseval)** | `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.ThetaParseval.ThetaKernels.TLiftK` | 20,486 | `Development/AbelianVarietyTheory` (8,890), `Development/WeilBound` (1,763), `Development/AutomorphicSpectrum` (1,544) |
| **RecTExists (Local Langlands)** | `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.RecTExists` | 26,673 | `Development/AbelianVarietyTheory` (11,192), `Formalism/LocalToGlobal` (2,728), `Formalism/PeriodIntegrals` (2,619) |

## 3. Disjoint / Exclusive Breakdown of the Major Branches

- `plugAll` (`CharacterBoxes.EveryCharacter`) total cone: **14,299** files
- `hypsE2 \ plugAll` (`EveryCharacterE` minus `plugAll`): **86,424** files
- `VWinCore` (`WindowBoundOfLiteratureLevel`) total cone: **55,067** files
- `CovolX` (`TopCovolSlim2Use`) total cone: **50,236** files
- `Row0b` (`GaloisRepresentationsOfThetaLift` ∪ `TLiftK`) total cone: **66,167** files
- `LLC` (`RecTExists`) total cone: **26,673** files
- **Pure Literature-Seam proofs** (`MainConclusion` minus union of above 6 core anchors — i.e., theorems fed ONLY into `EveryCharacterOfLiteratureOfVWin` / `TopMainZj`): **29,885** files!

### What lives inside the `plugAll` (`CharacterBoxes.EveryCharacter`) cone? (by 2nd-level dir)
- `Formalism/PeriodIntegrals`: 3,193
- `Formalism/LocalToGlobal`: 2,576
- `Formalism/SharpRestriction`: 2,038
- `Development/AbelianVarietyTheory`: 1,654
- `ReciprocityTheory/ReductiveGroups`: 1,032
- `Formalism/HermitianCurvature`: 683
- `Formalism/GL3MeanSquares`: 438
- `Development/AutomorphicArithmetic`: 338
- `Formalism/ThetaLogCoordinates`: 285
- `Formalism/LocalRingCardinality`: 169
- `Formalism/GradedWeylDivisibility`: 103
- `Formalism/SatakeDualWeyl`: 85
- `Formalism/GaussJetBounds`: 85
- `Formalism/FlagUnipotentLattices`: 77
- `Formalism/SizeWindowBrackets`: 64
- `Formalism/QuotientMetricDivisors`: 63
- `Formalism/PadicSubsetSums`: 63
- `Formalism/LandauZeroFreeBounds`: 58
- `Formalism/RealPlaceAnalysis`: 54
- `Formalism/MahlerMeasure`: 54
- `Formalism/CharacterColumnKernels`: 54
- `Formalism/EllipticTorsion`: 48
- `Formalism/HarderNarasimhan`: 43
- `Formalism/HermitianLattices`: 43
- `Formalism/PolynomialDimension`: 41

### What lives inside `hypsE2 \ plugAll`? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 59,131
- `GroundTheory/HeightsAndTheta`: 6,379
- `Development/AutomorphicSpectrum`: 6,367
- `Formalism/LocalToGlobal`: 2,816
- `Development/WeilBound`: 2,306
- `ReciprocityTheory/ReductiveGroups`: 1,687
- `Formalism/HermitianCurvature`: 1,238
- `Formalism/PeriodIntegrals`: 1,091
- `Formalism/SharpRestriction`: 989
- `Development/AutomorphicArithmetic`: 694
- `Development/ResolutionOfSingularities`: 499
- `CompanionTheory/AutomorphicTheory`: 335
- `GroundTheory/GlobalFields`: 318
- `Formalism/WachLatticeTwists`: 262
- `ReciprocityTheory/L2DbarEstimates`: 226
- `CompanionTheory/SpectralGeometry`: 175
- `GroundTheory/ArithmeticGeometry`: 173
- `GroundTheory/AutomorphicForms`: 168
- `ReciprocityTheory/DualLattices`: 165
- `ReciprocityTheory/AnalyticForms`: 164

### What lives inside `VWinCore` (`WindowBoundOfLiteratureLevel`)? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 21,935
- `Development/AutomorphicArithmetic`: 10,580
- `Development/AutomorphicSpectrum`: 4,526
- `Formalism/LocalToGlobal`: 2,908
- `Formalism/PeriodIntegrals`: 2,718
- `Formalism/SharpRestriction`: 2,178
- `Development/WeilBound`: 1,809
- `ReciprocityTheory/ReductiveGroups`: 1,490
- `Formalism/HermitianCurvature`: 817
- `GroundTheory/AutomorphicForms`: 531
- `PositivityTheory/AutomorphicForms`: 445
- `Formalism/GL3MeanSquares`: 426
- `GroundTheory/GlobalFields`: 374
- `Formalism/ThetaLogCoordinates`: 285
- `ReciprocityTheory/L2DbarEstimates`: 225
- `GroundTheory/ProfiniteCohomology`: 218
- `Formalism/LocalRingCardinality`: 169
- `GroundTheory/LocalFields`: 157
- `ReciprocityTheory/DualLattices`: 114
- `ReciprocityTheory/SemistableReduction`: 114

### What lives inside `CovolX` (`TopCovolSlim2Use`)? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 21,277
- `Development/AutomorphicSpectrum`: 5,928
- `GroundTheory/HeightsAndTheta`: 5,366
- `Formalism/LocalToGlobal`: 2,737
- `Formalism/PeriodIntegrals`: 2,600
- `ReciprocityTheory/ReductiveGroups`: 2,061
- `Formalism/SharpRestriction`: 2,056
- `Development/WeilBound`: 1,314
- `Development/AutomorphicArithmetic`: 804
- `Formalism/HermitianCurvature`: 683
- `CompanionTheory/SpectralGeometry`: 544
- `Development/ResolutionOfSingularities`: 499
- `Formalism/GL3MeanSquares`: 426
- `GroundTheory/GlobalFields`: 316
- `Formalism/ThetaLogCoordinates`: 285
- `ReciprocityTheory/L2DbarEstimates`: 226
- `ReciprocityTheory/AnalyticForms`: 192
- `ReciprocityTheory/DualLattices`: 176
- `Formalism/LocalRingCardinality`: 169
- `GroundTheory/ArithmeticGeometry`: 167

### What lives inside `Row0b` (`GaloisRepresentationsOfThetaLift` ∪ `TLiftK`)? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 31,624
- `Development/AutomorphicArithmetic`: 5,981
- `Development/AutomorphicSpectrum`: 5,655
- `Development/WeilBound`: 4,032
- `Formalism/LocalToGlobal`: 2,994
- `Formalism/PeriodIntegrals`: 2,762
- `Formalism/SharpRestriction`: 2,142
- `ReciprocityTheory/ReductiveGroups`: 1,591
- `Development/EtaleCohomology`: 1,386
- `Formalism/HermitianCurvature`: 817
- `CompanionTheory/SpectralGeometry`: 726
- `GroundTheory/AutomorphicForms`: 537
- `Formalism/GL3MeanSquares`: 426
- `GroundTheory/GlobalFields`: 355
- `Formalism/ThetaLogCoordinates`: 285
- `GroundTheory/HeightsAndTheta`: 247
- `ReciprocityTheory/L2DbarEstimates`: 225
- `GroundTheory/PAdicHodge`: 225
- `GroundTheory/ProfiniteCohomology`: 219
- `GroundTheory/ArithmeticGeometry`: 181

### What lives inside `LLC` (`RecTExists`)? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 11,192
- `Formalism/LocalToGlobal`: 2,728
- `Formalism/PeriodIntegrals`: 2,619
- `Formalism/SharpRestriction`: 1,921
- `ReciprocityTheory/ReductiveGroups`: 1,392
- `Development/AutomorphicSpectrum`: 1,005
- `Formalism/HermitianCurvature`: 809
- `Formalism/GL3MeanSquares`: 426
- `GroundTheory/GlobalFields`: 348
- `Development/AutomorphicArithmetic`: 318
- `Formalism/ThetaLogCoordinates`: 285
- `GroundTheory/AutomorphicForms`: 245
- `ReciprocityTheory/L2DbarEstimates`: 223
- `GroundTheory/ProfiniteCohomology`: 218
- `Development/WeilBound`: 202
- `Formalism/LocalRingCardinality`: 169
- `GroundTheory/LocalFields`: 156
- `Formalism/GradedWeylDivisibility`: 103
- `CompanionTheory/HarishChandraModules`: 90
- `ReciprocityTheory/SemistableReduction`: 87

### What lives ONLY below the Literature Seam (`MainConclusion \ core_union`)? (by 2nd-level dir)
- `Development/AbelianVarietyTheory`: 22,145
- `Development/AutomorphicArithmetic`: 3,146
- `Development/AutomorphicSpectrum`: 2,425
- `Development/WeilBound`: 1,135
- `CompanionTheory/SpectralGeometry`: 433
- `GroundTheory/ProfiniteCohomology`: 231
- `CompanionTheory/RealGroups`: 97
- `Development/DiscreteGroups`: 87
- `ReciprocityTheory/ReductiveGroups`: 58
- `ReciprocityTheory/ClassFieldTheory`: 22
- `CompanionTheory/ThickeningEstimates`: 22
- `Formalism/LocalToGlobal`: 18
- `CompanionTheory/AutomorphicTheory`: 18
- `Formalism/PeriodIntegrals`: 14
- `GroundTheory/HeightsAndTheta`: 10
- `GroundTheory/TateCohomology`: 6
- `ReciprocityTheory/GaloisValuations`: 3
- `PositivityTheory/PublishedTheorems`: 3
- `Formalism/SharpRestriction`: 2
- `ReciprocityTheory/L2DbarEstimates`: 1
- `CompanionTheory/HarishChandraModules`: 1
- `ReciprocityTheory/NeutralLocalFields`: 1
- `GroundTheory/LocalFields`: 1
- `ReciprocityTheory/Hypotheses`: 1
- `ReciprocityTheory/GeometryOfNumbers`: 1

## 4. Direct Imports of Key Choke Points (Total Cone / Exclusive Cone)

### `CharacterBoxes.EveryCharacter (`plugAll`)`
- `Development.AutomorphicArithmetic.CharacterBoxes.ShapeWin` — cone: **14,018**, exclusive: **3,033**
- `Development.AbelianVarietyTheory.Proofs.GlobalInterpolation.ShapeOf` — cone: **10,921**, exclusive: **1**
- `Development.AutomorphicArithmetic.CharacterBoxes.SupplyChi` — cone: **1,330**, exclusive: **278**
- `Development.AutomorphicArithmetic.CharacterBoxes.Imprimitive` — cone: **11**, exclusive: **1**

### `EveryCharacterE (`hypsE2`)`
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.NonemptyHypsOfPublishedUE` — cone: **68,774**, exclusive: **8,733**
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.OpenFirstParametersOfPrintsUEStatement` — cone: **49,918**, exclusive: **0**
- `Development.AutomorphicArithmetic.ThetaCorrespondence.FockModels.ArakSwapCovol` — cone: **49,769**, exclusive: **20,079**
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.Fun0FitOfJoin` — cone: **42,005**, exclusive: **1,008**
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.RationalityOfThetaHypothesesStatement` — cone: **40,647**, exclusive: **19**
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.OntoXAndLamLowOfPublishedUE` — cone: **37,490**, exclusive: **0**
- `Development.AbelianVarietyTheory.Proofs.DivisorProofs.EvLgGGridAOfJoin` — cone: **34,719**, exclusive: **16**
- `Development.AutomorphicArithmetic.ThetaCorrespondence.FockModels.RealBranch` — cone: **29,485**, exclusive: **1,132**
- `Development.AbelianVarietyTheory.Proofs.GlobalInterpolation.LargeFieldLinkedBundlesExist` — cone: **28,337**, exclusive: **12**
- `Development.AbelianVarietyTheory.Proofs.GlobalInterpolation.OpenImpliesL3AtLinkedBundles` — cone: **28,295**, exclusive: **1**
- `Development.AbelianVarietyTheory.Proofs.GlobalInterpolation.OpenAndLinkedMonoExtension` — cone: **24,778**, exclusive: **0**
- `Development.AbelianVarietyTheory.Definitions.Divisors.HypothesisBundleConversions` — cone: **24,630**, exclusive: **0**
- `Development.AutomorphicArithmetic.ResidueCharacters.ClosedOfAll` — cone: **23,921**, exclusive: **8**
- `Development.AbelianVarietyTheory.Definitions.GlobalTwisting.BhattScholzeCrystallineLattices` — cone: **23,206**, exclusive: **0**
- `Development.AbelianVarietyTheory.Definitions.GlobalTwisting.DepthZeroSupport` — cone: **23,205**, exclusive: **0**
- `Development.AbelianVarietyTheory.Definitions.GlobalTwisting.GeometricWeakTiesOfStrong` — cone: **23,139**, exclusive: **0**
- `Development.AbelianVarietyTheory.Definitions.AutomorphicMembership.GKeyFin` — cone: **22,760**, exclusive: **0**
- `Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.RowRatWOfRowTest` — cone: **22,707**, exclusive: **1**
- `Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.ExistsUnlocalizedSaturatedState` — cone: **15,912**, exclusive: **0**
- `Development.AbelianVarietyTheory.Proofs.TwistedOperators.ThetaIntegralsOfMinguezStatement` — cone: **15,381**, exclusive: **0**

### `WindowBoundOfLiteratureLevel (`vwin_of_hypotheses_H_E_alt`)`
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.LinkedUnlE` — cone: **51,551**, exclusive: **54**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.DnEndsTop` — cone: **50,617**, exclusive: **38**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.Sp4In0` — cone: **50,605**, exclusive: **23**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.PublishedHypothesesFromPatching` — cone: **50,405**, exclusive: **930**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.AdjointLiftingOfCohomology` — cone: **48,502**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.HVCore` — cone: **40,797**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.CohInp` — cone: **37,617**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.KatoTwoWOfPublishedH` — cone: **36,168**, exclusive: **33**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.CarFillE` — cone: **30,047**, exclusive: **1**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.KFinal` — cone: **29,532**, exclusive: **2**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.AutEnd3AltAlt` — cone: **25,137**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.AfDesc` — cone: **24,574**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.AutomorphicFormHyp` — cone: **24,572**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.LitAut` — cone: **24,566**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.ThmS6CoreS` — cone: **24,546**, exclusive: **0**
- `Development.AutomorphicArithmetic.AutomorphicVarieties.ModularityArgument.ThresholdArguments.DenseThresholdCases.DiscreteSeriesCoefficientsCuspidal` — cone: **1**, exclusive: **0**

### `TopCovolSlim2Use (`CovolX`)`
- `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.HodgeBundleWeights.TopCovolSlim2Use` — cone: **49,833**, exclusive: **17,801**
- `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.TopCovolG` — cone: **32,434**, exclusive: **193**
- `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.LiftLambdaBound` — cone: **10,672**, exclusive: **0**
- `Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.CohomologicalCsdTempered` — cone: **1**, exclusive: **0**

### `GaloisRepresentationsOfThetaLift`
- `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.GeometricFlagBases.WeightOneGeometricRealization` — cone: **45,860**, exclusive: **15,440**
- `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.IntegralStructures.Development` — cone: **45,640**, exclusive: **15,220**

### `TLiftK`
- `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.ThetaParseval.ThetaKernels.TPGHolds` — cone: **20,484**, exclusive: **16,650**
- `Development.AutomorphicArithmetic.Foundations.GaloisRepresentations.ThetaParseval.HalfIndexLattices.TLiftK` — cone: **3,835**, exclusive: **1**

### `RecTExists`
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.CuspEx` — cone: **26,631**, exclusive: **4,538**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ExtDepth` — cone: **21,782**, exclusive: **9**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ExtDim` — cone: **21,773**, exclusive: **0**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ExtInj` — cone: **21,744**, exclusive: **16**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.RcTwOfSegments` — cone: **21,736**, exclusive: **1**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ExtDual` — cone: **21,736**, exclusive: **8**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ClBasic` — cone: **21,724**, exclusive: **0**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.Multi` — cone: **21,718**, exclusive: **0**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.TypeIff` — cone: **2,772**, exclusive: **1**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.LocalCentralUnits.ArtEx` — cone: **1,727**, exclusive: **0**
- `Development.DiscreteGroups.GlobalIrreducibility.DzLCusp` — cone: **1,071**, exclusive: **0**
- `Development.AutomorphicArithmetic.Foundations.LocalLanglands.RecTTransport` — cone: **1,067**, exclusive: **0**
- `Development.AbelianVarietyTheory.Proofs.InertiaEigenvalues.LanglandsExtensionUniqueOnCuspidal` — cone: **899**, exclusive: **0**

## 5. Complete Map of `Formalism/*` Modules in GRH (Where Each Enters)

| `Formalism/<submod>` | Files in GRH | Reached by core branches | Top external importers |
|---|---:|---|---|
| `LocalToGlobal` | 5,501 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (18679), `Development/AbelianVarietyTheory/Definitions` (869), `Development/AbelianVarietyTheory/BlockTheory` (458) |
| `PeriodIntegrals` | 4,350 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (722), `Formalism/LocalToGlobal/SiegelLatticeTheory` (490), `Formalism/HermitianCurvature/HermitianCurvatureProofs` (111) |
| `SharpRestriction` | 3,093 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (9356), `Formalism/LocalToGlobal/SiegelLatticeTheory` (393), `Development/AbelianVarietyTheory/Definitions` (350) |
| `HermitianCurvature` | 1,922 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (780), `Formalism/LocalToGlobal/SiegelLatticeTheory` (147), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (116) |
| `GL3MeanSquares` | 440 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (111), `Formalism/LocalToGlobal/SiegelLatticeTheory` (86), `Formalism/LocalToGlobal/GlobalTheory` (34) |
| `ThetaLogCoordinates` | 292 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/GrowthBounds` (34), `Formalism/LocalToGlobal/TorsionIntegrality` (22), `Lemmata/GeneralBFactLeftBisForm/Imports` (19) |
| `WachLatticeTwists` | 262 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift, RecTExists | `Development/AbelianVarietyTheory/Proofs` (35), `Formalism/SharpRestriction/LevelLetterCocycles` (5), `ReciprocityTheory/ReductiveGroups/TraceFormulas` (3) |
| `LocalRingCardinality` | 173 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (2879), `Development/AbelianVarietyTheory/BlockTheory` (163), `Development/AbelianVarietyTheory/Definitions` (130) |
| `GradedWeylDivisibility` | 103 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (202), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (59), `Formalism/LocalToGlobal/GroupLattices` (22) |
| `PieriBlockIdeals` | 98 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (77), `Development/AbelianVarietyTheory/Definitions` (4), `Formalism/LocalToGlobal/Columns` (2) |
| `AdmissibleDesigns` | 93 | EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift | `Development/AbelianVarietyTheory/Proofs` (13), `Development/AbelianVarietyTheory/Definitions` (1), `Development/AutomorphicArithmetic/AutomorphicVarieties` (1) |
| `GaussJetBounds` | 90 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/TorsionIntegrality` (25), `Development/AbelianVarietyTheory/Proofs` (23), `Formalism/ThetaLogCoordinates/UniformThetaSubstitution` (17) |
| `SatakeDualWeyl` | 85 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (661), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (43), `Formalism/SharpRestriction/GenusPolyhedralBounds` (40) |
| `PadicSubsetSums` | 82 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (43), `Formalism/SharpRestriction/LevelLetterCocycles` (27), `Lemmata/TwistedIdempotents/TwistedIdem` (13) |
| `FlagUnipotentLattices` | 77 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (66), `Formalism/SharpRestriction/CuspSpanNormBounds` (51), `Formalism/HermitianCurvature/HermitianCurvatureProofs` (7) |
| `SizeWindowBrackets` | 64 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/GlobalTheory` (26), `Formalism/SharpRestriction/GlobalSchurBounds` (14), `Formalism/LocalToGlobal/Columns` (7) |
| `QuotientMetricDivisors` | 63 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (211), `Formalism/LocalToGlobal/Divisibility` (27), `Formalism/MirabolicMackeyTheory/MirabolicMackeyProofs` (15) |
| `LandauZeroFreeBounds` | 58 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/GL3MeanSquares/GenusMeanAsymptotics` (31), `Development/AbelianVarietyTheory/Proofs` (5), `Development/AutomorphicArithmetic/MeanSquareBounds` (4) |
| `RealPlaceAnalysis` | 54 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (753), `Development/AutomorphicSpectrum/Proofs` (90), `CompanionTheory/AutomorphicTheory/PieriRules` (72) |
| `CharacterColumnKernels` | 54 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Development/AbelianVarietyTheory/Proofs` (41), `Formalism/SharpRestriction/LevelLetterCocycles` (13), `Formalism/WachLatticeTwists/RamifiedBlockRings` (13) |
| `MahlerMeasure` | 54 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/GrowthBounds` (18), `Lemmata/GeneralBFactLeftBisForm/Imports` (8), `Formalism/PolynomialDimension/MultinomialDepth` (7) |
| `EllipticTorsion` | 48 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/TorsionIntegrality` (10), `ReciprocityTheory/ReductiveGroups/UnramifiedIntegrals` (7), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (2) |
| `DistinguishedUnitIdeals` | 44 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/SharpRestriction/LevelLetterCocycles` (10) |
| `UnipotentAdelicQuotients` | 44 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (156), `CompanionTheory/SpectralGeometry/LocalGlobalProofs` (35), `Development/AutomorphicSpectrum/Proofs` (22) |
| `HermitianLattices` | 43 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (112), `Formalism/SharpRestriction/CuspSpanNormBounds` (30), `Lemmata/DualWeylPullback/DualWeylPull` (23) |
| `HarderNarasimhan` | 43 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (276), `Development/AutomorphicArithmetic/IntegralCasts` (33), `Lemmata/DualWeylPullback/DualWeylPull` (29) |
| `PolynomialDimension` | 41 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (37), `Formalism/SharpRestriction/GrowthBounds` (20), `Lemmata/DualWeylPullback/DualWeylPull` (5) |
| `TruncatedSeriesCounting` | 39 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/SharpRestriction/LevelLetterCocycles` (11), `Formalism/JumpKernelCokernel/JumpShiftProofs` (3), `Formalism/WachLatticeTwists/RamifiedBlockRings` (3) |
| `FilteredPoleLength` | 36 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/GenusPolyhedralBounds` (8), `ReciprocityTheory/ReductiveGroups/ArithmeticGeometry` (5), `Formalism/LocalToGlobal/ProjectiveLattices` (2) |
| `ZeroFreeRegion` | 34 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LandauZeroFreeBounds/ExceptionalZeroBounds` (12), `Formalism/GL3MeanSquares/GenusMeanAsymptotics` (5), `Formalism/SizeWindowBrackets/ChainSlopeWindows` (1) |
| `SubspaceCounting` | 32 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/GrowthBounds` (5), `Development/AbelianVarietyTheory/Proofs` (2), `Formalism/ThetaLogCoordinates/UniformThetaSubstitution` (2) |
| `FrobeniusOrbits` | 32 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (270), `Formalism/LocalToGlobal/KernelLattices` (14), `Formalism/LocalToGlobal/GlobalTheory` (13) |
| `FormalDegreeBessel` | 31 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (137), `Formalism/HermitianCurvature/HermitianCurvatureProofs` (89), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (58) |
| `JumpKernelCokernel` | 27 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/SharpRestriction/LevelLetterCocycles` (5) |
| `MirabolicMackeyTheory` | 26 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (51), `Formalism/LocalToGlobal/IndefiniteForms` (12), `Formalism/LocalToGlobal/Divisibility` (5) |
| `LogVandermondeBounds` | 26 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/GL3MeanSquares/HookFormulaTorsion` (13), `Formalism/LocalToGlobal/Columns` (5), `Formalism/LocalToGlobal/GlobalTheory` (4) |
| `MeanHeightDescent` | 24 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (48), `Development/AutomorphicArithmetic/IntegralCasts` (7), `Formalism/LocalToGlobal/LatticeGeometry` (2) |
| `BranchSandwichDivisors` | 22 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (30), `Formalism/LocalToGlobal/GlobalTheory` (10), `Formalism/LocalToGlobal/KernelLattices` (4) |
| `FormalGroupWitt` | 21 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/GL3MeanSquares/HookFormulaTorsion` (6), `Formalism/LocalToGlobal/TorsionIntegrality` (4), `Formalism/GaussJetBounds/GaussJetProofs` (3) |
| `IncomingBounds` | 21 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AutomorphicArithmetic/OrbitLabellings` (8), `Formalism/GaussJetBounds/GaussJetProofs` (5), `Formalism/LocalToGlobal/CharacterGerms` (4) |
| `CyclotomicNorms` | 21 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (50), `Development/AbelianVarietyTheory/BlockTheory` (9), `Formalism/LocalRingCardinality/SpanPowerMembership` (6) |
| `WeaklyAdmissibleFiltrations` | 20 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/LevelLetterCocycles` (23), `Development/AbelianVarietyTheory/BlockTheory` (19), `Development/AutomorphicArithmetic/IntegralCasts` (10) |
| `ThetaSupremumBounds` | 19 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/Divisibility` (3), `Development/AbelianVarietyTheory/Proofs` (3), `Development/AbelianVarietyTheory/BlockTheory` (2) |
| `LatticeSlopes` | 18 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HarderNarasimhan/HarderNarasimhanProofs` (35), `Formalism/NormUnitaryBounds/DetPolynomialWeights` (10), `Development/AutomorphicArithmetic/IntegralCasts` (3) |
| `RankGapBounds` | 17 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SizeWindowBrackets/ChainSlopeWindows` (6), `Formalism/PieriBlockIdeals/PieriColumnMinors` (5), `Formalism/SizeWindowBrackets/SecondKindBucket` (2) |
| `YangianSpanCharacter` | 17 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HermitianCurvature/HermitianCurvatureProofs` (6), `Formalism/HermitianCurvature/StatementFr` (2), `Formalism/SharpRestriction/CuspSpanNormBounds` (2) |
| `GaloisIrreducibility` | 17 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/PadicSubsetSums/StableGradedCounts` (4), `Formalism/CyclotomicNorms/NonsquarefreeBounds` (3), `Development/AutomorphicSpectrum/Proofs` (1) |
| `LogSumExpBounds` | 16 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds` (2), `Formalism/FlagUnipotentLattices/HalfDifferenceL1Bound` (1) |
| `GaussValuationBounds` | 16 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/SharpRestriction/LevelLetterCocycles` (4), `Formalism/TruncatedSeriesCounting/EtaDeterminantPolynomialIdentities` (2), `Formalism/EisensteinCokernelLengths/RationalTailBound` (2) |
| `CoboundaryTransfers` | 16 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/BlockTheory` (7), `Formalism/WachLatticeTwists/WachProductBases` (6), `Formalism/WachLatticeTwists/LagrangeExtensionCocycles` (2) |
| `TorsionNormIteration` | 15 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FormalGroupWitt/FormalGroupWittProofs` (4), `Development/AbelianVarietyTheory/Proofs` (3), `Formalism/GL3MeanSquares/HookFormulaTorsion` (1) |
| `ZetaNonvanishing` | 15 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/SizeWindowBrackets/ChainSlopeWindows` (3), `Formalism/SharpRestriction/GlobalSchurBounds` (2), `Formalism/ZeroFreeRegion/ZetaLogDerivativeBounds` (1) |
| `DoubleCosetMeasures` | 15 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (19), `Formalism/HermitianCurvature/HermitianCurvatureProofs` (15), `Formalism/PeriodIntegrals/UnitaryGroupMassFormula` (5) |
| `SuccessiveMinima` | 15 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Lemmata/DualWeylPullback/DualWeylPull` (10), `Formalism/HermitianLattices/HermitianLatticesProofs` (1), `Formalism/LocalToGlobal/GlobalTheory` (1) |
| `TameInertiaTowers` | 15 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FrobeniusOrbits/FrobeniusOrbitsProofs` (10), `Development/AutomorphicArithmetic/IntegralCasts` (3), `Lemmata/GeneralBFactLeftBisForm/Imports` (3) |
| `NormUnitaryBounds` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/GelfandTransference/HadamardGelfand` (2), `Development/AutomorphicSpectrum/Proofs` (1), `Formalism/GelfandTransference/Statement` (1) |
| `BehrendSets` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/GL3MeanSquares/HookFormulaTorsion` (2) |
| `CMTypeGalois` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Lemmata/DualWeylPullback/DualWeylPull` (11), `Formalism/DirichletDensity/DirichletDensityProofs` (2), `Formalism/DirichletDensity/Statement` (1) |
| `GrowthSums` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SharpRestriction/GrowthBounds` (6), `Formalism/ThetaLogCoordinates/UniformThetaSubstitution` (5), `Lemmata/GeneralBFactLeftBisForm/Imports` (1) |
| `LatticeTheta` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (17), `Formalism/HermitianLattices/FinalNeighbourConstruct` (1), `Formalism/SharpRestriction/CuspSpanNormBounds` (1) |
| `HyperbolicPlaceProducts` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds` (10), `Development/AbelianVarietyTheory/Proofs` (2), `Formalism/FlagUnipotentLattices/DetIndexProductPlacesInequalitySq` (2) |
| `FockGram` | 14 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (2), `Formalism/HermitianLattices/HermitianLatticesProofs` (2), `Development/AutomorphicArithmetic/IntegralCasts` (2) |
| `ResultantValuation` | 13 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/PadicSubsetSums/StableGradedCounts` (23), `Formalism/PadicSubsetSums/CentralIdempotents` (2), `Formalism/WachLatticeTwists/LagrangeExtensionCocycles` (1) |
| `FrobeniusContraction` | 13 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/GaussValuationBounds/GaussValueContraction` (9), `Formalism/EisensteinCokernelLengths/FactorialValuationBounds` (6), `Formalism/TruncatedSeriesCounting/EtaDeterminantPolynomialIdentities` (4) |
| `LatticeRigidity` | 12 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HermitianCurvature/HermitianCurvatureProofs` (4), `Formalism/FlagUnipotentLattices/HalfDifferenceL1Bound` (3), `Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds` (2) |
| `SobolevGaussianKernels` | 12 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FlagUnipotentLattices/PairingOrthogonalComplement` (4), `Formalism/FlagUnipotentLattices/MinkowskiFactorialBounds` (1) |
| `FrobeniusBaseCase` | 12 | EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift | `Formalism/LocalToGlobal/CharacterGerms` (3), `Development/AbelianVarietyTheory/Proofs` (1) |
| `EisensteinCokernelLengths` | 12 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/JumpKernelCokernel/LengthTheoremsWithEarlier` (3), `Formalism/PadicSubsetSums/StableGradedCounts` (3), `Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs` (1) |
| `LogFactorialIndices` | 11 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/FilteredPoleLength/LocalDescentLevels` (6), `Formalism/QuotientMetricDivisors/HermitianTwistDivisors` (4), `Formalism/SharpRestriction/GenusPolyhedralBounds` (4) |
| `WindowSums` | 11 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/SharpRestriction/LevelLetterCocycles` (5), `Formalism/TruncatedSeriesCounting/TruncatedSeriesProofs` (5), `Formalism/GaussValuationBounds/GaussValueContraction` (4) |
| `ThetaLiftIndependence` | 10 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Lemmata/DualWeylPullback/DualWeylPull` (8), `Formalism/SharpRestriction/CuspSpanNormBounds` (3), `Formalism/SharpRestriction/GenusPolyhedralBounds` (3) |
| `LagrangeIdealLifts` | 9 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/CoboundaryTransfers/GammaStableTransfers` (2), `Formalism/WachLatticeTwists/WachProductBases` (2), `Formalism/WachLatticeTwists/LagrangeExtensionCocycles` (2) |
| `WachModuleLifts` | 9 | EveryCharacterE, WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Formalism/SharpRestriction/LevelLetterCocycles` (5), `Formalism/GaussValuationBounds/GaussValueContraction` (3), `Formalism/WindowSums/StatementRelay` (1) |
| `DirichletDensity` | 8 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Lemmata/DualWeylPullback/DualWeylPull` (4), `Formalism/SharpRestriction/GlobalSchurBounds` (2), `Formalism/GL3MeanSquares/HookFormulaTorsion` (1) |
| `GelfandTransference` | 7 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AutomorphicSpectrum/Proofs` (5), `Formalism/SharpRestriction/Divisibility` (3), `Formalism/LatticeRigidity/RecursionUnrestrictedFalse` (1) |
| `TranslateCocycles` | 7 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LocalToGlobal/ExponentGrids` (8) |
| `PairingDivisors` | 7 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (538), `Formalism/LocalToGlobal/ExponentGrids` (4), `Development/AbelianVarietyTheory/BlockTheory` (3) |
| `LFunctionBounds` | 7 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/GL3MeanSquares/GenusMeanAsymptotics` (7), `Formalism/LandauZeroFreeBounds/ExceptionalZeroBounds` (2), `Formalism/ZeroFreeRegion/ZetaLogDerivativeBounds` (1) |
| `SmithDeterminants` | 6 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/MahlerMeasure/MahlerMeasureProofs` (1), `Formalism/FockGram/StatementFock` (1) |
| `SelfDualUnimodular` | 6 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LocalToGlobal/SiegelLatticeTheory` (5) |
| `GaloisCohomology` | 6 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (368), `Development/AutomorphicArithmetic/AutomorphicVarieties` (29), `Formalism/SharpRestriction/LevelLetterCocycles` (8) |
| `MonomialMeanResidues` | 6 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Development/AutomorphicSpectrum/Definitions` (2), `Formalism/LocalToGlobal/Columns` (1) |
| `ThickAverageLoss` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/SizeWindowBrackets/ChainSlopeWindows` (3), `Formalism/SizeWindowBrackets/FirstPrimeNeSecondPrime` (1) |
| `DivisorInequality` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/Divisibility` (2), `Formalism/LocalToGlobal/IndefiniteForms` (1) |
| `MoebiusJetDuality` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/DegreeFormula/Statement` (1) |
| `DegreeFormula` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (147), `Formalism/LocalToGlobal/LatticeGeometry` (5), `Development/AbelianVarietyTheory/Definitions` (4) |
| `FormalGroupLog` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/TorsionIntegrality` (11), `Formalism/EllipticTorsion/EllipticTorsionProofs` (6), `Formalism/LocalToGlobal/InertKernelTheory` (3) |
| `LogFactorialBounds` | 5 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/MeanHeightDescent/FlatDefect` (1), `Formalism/ThetaSupremumBounds/GaussianShiftBounds` (1), `Formalism/QuotientMetricDivisors/HermitianTwistDivisors` (1) |
| `TowerValuationBounds` | 4 | EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/ExponentGrids` (4), `Lemmata/PlaneOverMembership/PlOverOfMem` (1) |
| `DropLevelBounds` | 4 | EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift | `Development/AbelianVarietyTheory/Proofs` (6), `Formalism/LocalToGlobal/CharacterGerms` (5), `Development/AutomorphicArithmetic/OrbitLabellings` (2) |
| `CorankShare` | 3 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HarderNarasimhan/HarderNarasimhanProofs` (3), `Development/AutomorphicArithmetic/IntegralCasts` (2), `Lemmata/DualWeylPullback/DualWeylPull` (2) |
| `AdicCompletionExports` | 3 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LocalToGlobal/Divisibility` (1), `Formalism/AdmissibleDesigns/CycMatchRec` (1), `Formalism/AdmissibleDesigns/ExistsWildInertiaCyclotomicGenerator` (1) |
| `ConjugateSelfDual` | 3 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AutomorphicArithmetic/IntegralCasts` (5), `Formalism/SharpRestriction/ValuationFrobeniusEpsilon` (4), `Development/AbelianVarietyTheory/Proofs` (3) |
| `AlgebraicWeights` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalToGlobal/GaloisLevelStructure` (2), `Formalism/LocalToGlobal/NormalizedHeckeFactors` (1) |
| `JacquetSubsetSums` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (9), `Development/AbelianVarietyTheory/Counterexamples` (2), `Formalism/LocalToGlobal/IndefiniteForms` (1) |
| `LatticeLocalGlobal` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/LocalRingCardinality/DataArith` (2) |
| `GaussIdealIdentity` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AutomorphicArithmetic/IntegralCasts` (1), `Formalism/SharpRestriction/GenusPolyhedralBounds` (1) |
| `ArtinHasse` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Development/AbelianVarietyTheory/Proofs` (3), `Formalism/ThetaLogCoordinates/UniformThetaSubstitution` (1) |
| `WeightedDeltaMeans` | 2 | EveryCharacterE, TopCovolSlim2Use | `Formalism/LocalToGlobal/LatticeGeometry` (2) |
| `GammaFactorNonvanishing` | 2 | *(literature seam only)* | `Supplements/Kernels/MainTheorems` (1) |
| `JacobiWeightFamilies` | 2 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/TwistFamilyExistence/Statement` (1), `Formalism/WideWeightTheorem/Statement` (1) |
| `Statement` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/ZetaRealNonvanish` (1), `Formalism/StatementOC` (1) |
| `StatementFL` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LFunctionBounds/Statement` (1) |
| `PrimeAboveExistence` | 1 | WindowBoundOfLiteratureLevel, GaloisRepresentationsOfThetaLift | `Development/AutomorphicArithmetic/AutomorphicVarieties` (4), `Development/AutomorphicArithmetic/Foundations` (1) |
| `WideWeightTheorem` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/ThickAverageLoss/Statement` (1) |
| `ZetaNonvanishingGeneralWeights` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/ZetaNonvanishingChebyshevWeights` (1) |
| `ZetaRealNonvanish` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/DefsOC` (1), `Formalism/ZetaNonvanishing/MellinElem` (1), `Formalism/ZetaNonvanishing/Assembly` (1) |
| `ProductFormula` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HalfLinks/Statement` (1) |
| `StatementOC` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/StatementU` (1), `Formalism/StatementCM` (1), `Formalism/DefsOC` (1) |
| `ZetaNonvanishingChebyshevWeights` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/StatementFL` (1), `Formalism/HalfLinks/Statement` (1) |
| `HalfLinks` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/JacobiWeightFamilies/Statement` (1) |
| `DefsOC` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/ZetaNonvanishing/MellinSgen` (1), `Formalism/ZetaNonvanishing/MeasurableGchi` (1), `Formalism/ZetaNonvanishing/LandauEq` (1) |
| `TwistFamilyExistence` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, RecTExists | `Formalism/LandauZeroFreeBounds/SiegelWalfiszAP` (1) |
| `StatementCM` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HalfLinks/Statement` (1), `Formalism/ProductFormula/StatementOCCM` (1), `Formalism/CMTypeGalois/StatementGroup` (1) |
| `StatementU` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/ZetaNonvanishingGeneralWeights` (1), `Formalism/ZetaNonvanishing/GzLipschitz` (1), `Formalism/ZetaNonvanishing/ZetaLandau` (1) |
| `AlphaUniqueness` | 1 | CharacterBoxes.EveryCharacter, EveryCharacterE, WindowBoundOfLiteratureLevel, TopCovolSlim2Use, GaloisRepresentationsOfThetaLift, TLiftK, RecTExists | `Formalism/HermitianLattices/StatementTheta` (1), `Formalism/HermitianLattices/DiscrFinite` (1) |

## 6. Top Cross-Subsystem Hub Modules (Imported by >=3 Distinct 2nd-Level Subsystems)

- `Formalism.RealPlaceAnalysis.StatementE` — 20 subsystems, 217 direct importers
- `Formalism.SatakeDualWeyl.Statement` — 20 subsystems, 120 direct importers
- `Formalism.FormalDegreeBessel.StatementDS` — 16 subsystems, 37 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.CartanInvolutionConjTransposeMul` — 15 subsystems, 43 direct importers
- `Formalism.LocalRingCardinality.DataSpaces` — 14 subsystems, 58 direct importers
- `Formalism.CoboundaryTransfers.Statement` — 14 subsystems, 24 direct importers
- `Formalism.LocalRingCardinality.DataCD` — 13 subsystems, 118 direct importers
- `Formalism.HermitianLattices.StatementLat` — 13 subsystems, 47 direct importers
- `Formalism.FormalDegreeBessel.StatementG` — 13 subsystems, 44 direct importers
- `Formalism.FrobeniusOrbits.Statement` — 13 subsystems, 31 direct importers
- `Formalism.LocalRingCardinality.DataArith` — 13 subsystems, 29 direct importers
- `Formalism.LocalRingCardinality.DataCoeff` — 13 subsystems, 26 direct importers
- `Formalism.DegreeFormula.FlagDegFormula` — 13 subsystems, 25 direct importers
- `Formalism.GradedWeylDivisibility.FinalD` — 12 subsystems, 88 direct importers
- `Formalism.LocalRingCardinality.Params` — 12 subsystems, 47 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.ShiftedGeneratorEqIteSmulAdd` — 12 subsystems, 32 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.QuantumDetHighestWeightHolds` — 12 subsystems, 28 direct importers
- `Formalism.SharpRestriction.GrowthBounds.DataG` — 12 subsystems, 25 direct importers
- `Formalism.RealPlaceAnalysis.StatementA` — 12 subsystems, 23 direct importers
- `Formalism.FrobeniusOrbits.HostThickExists` — 12 subsystems, 21 direct importers
- `Formalism.SatakeDualWeyl.KpqSubgroupCompact` — 11 subsystems, 321 direct importers
- `Formalism.RealPlaceAnalysis.ThirdArithmeticHolds` — 11 subsystems, 235 direct importers
- `Formalism.GradedWeylDivisibility.DualWeylDominanceOf` — 11 subsystems, 95 direct importers
- `Formalism.HarderNarasimhan.StatementPl` — 11 subsystems, 63 direct importers
- `Formalism.LocalRingCardinality.DataRows` — 11 subsystems, 29 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.MemUnitaryGroupIffMulConjTranspose` — 11 subsystems, 26 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.IndefiniteUnitaryPreservesForm` — 11 subsystems, 23 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.ComplexifiedDerivativeCommutator` — 11 subsystems, 23 direct importers
- `Formalism.HarderNarasimhan.ShiftInvariance` — 10 subsystems, 252 direct importers
- `Formalism.RealPlaceAnalysis.FinalF` — 10 subsystems, 125 direct importers
- `ReciprocityTheory.GaloisValuations.Global` — 10 subsystems, 67 direct importers
- `Formalism.LocalRingCardinality.DataLevel` — 10 subsystems, 40 direct importers
- `Formalism.SharpRestriction.RamificationFrobenius.TotientGaloisClasses.ConjEMemHostFIff` — 10 subsystems, 36 direct importers
- `Formalism.SharpRestriction.GlobalSchurBounds.GeneralLinearActions.FrameTransport` — 10 subsystems, 35 direct importers
- `Formalism.SharpRestriction.GrowthBounds.UnramifiedQuadraticSetting` — 10 subsystems, 32 direct importers
- `Formalism.FormalDegreeBessel.StatementBF` — 10 subsystems, 20 direct importers
- `Formalism.SharpRestriction.GrowthBounds.DataGChain` — 10 subsystems, 16 direct importers
- `Formalism.RealPlaceAnalysis.RealPlaceTaylor.CompactCasimirHighestWeight` — 10 subsystems, 15 direct importers
- `Formalism.HermitianLattices.HermitianLatticesProofs.DualLattice` — 9 subsystems, 27 direct importers
- `Formalism.SharpRestriction.GrowthBounds.ObjPol` — 9 subsystems, 24 direct importers
