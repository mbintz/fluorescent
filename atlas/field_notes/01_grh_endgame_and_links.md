# Cluster 1 Field Notes: the GRH endgame and the nine-link machine (`plugAll` / `topDesWin` / `zeroFreeAll_of_topG`)

I read everything below directly from the Lean code, and paths are relative to `lean/src/`. When I am interpreting what a structure means rather than restating it, I say so ("reading:"). I traced the links' own proofs only to their top-level files; Section 10 lists the subtrees I did not open.

---

## 0. Bottom line

1. **`plugAll` is a conditional theorem.** Its cone (14,299 files) proves
   `Green ∧ VWin ∧ Nonempty (Hyps (Closed · LinkN) DRS) → ∀χ, L(s,χ) ≠ 0 for Re s > 1/2`
   (`Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean:16-18`). The three antecedents are built elsewhere. `EveryCharacterE.lean:66-71` supplies them through `green_of_regular P.greenRegularCharacters`, `hV`, and `hypsE₂ …`. Most of the real arithmetic therefore lives outside this cluster. This cone is the **reduction**: it shows what those inputs give.
2. **The contradiction runs on a classical, fully formalized Landau-type oscillation lemma.** Suppose a one-sided bound Gm(y) ≤ y^θ holds on multiplicative windows [Y, Y^{3/2}] for arbitrarily large Y, where Gm is a positive-coefficient combination of smoothed Chebyshev remainders over the cyclic group ⟨ψ⟩. Then L(s, ψ^k) has no zeros with Re s > θ. Everything else exists to produce **Gm(x) ≤ x^{1/2+9ε}** at the window points, for every ε > 0.
3. **That upper bound comes from an upper bound on a weighted count of inert primes in an auxiliary CM abelian field** (the "host"). It is converted into a bound on character sums by an exact identity (`AskMainBalance`, ASK − MAIN = De) and a Fourier-weight trick on the host's group. The prime count is bounded by a **pure real-number "slope inequality" engine** with 11 hypotheses: a degree upper bound, a slope lower bound, a gain-vs-loss bound, counts, and parameter smallness. Reading: it looks like Arakelov-style lattice slopes and heights.
4. **The nine links are the 11 hypotheses of that engine, bundled per family.** Eight are inputs or intermediate implications. One, `LinkGLOBAL`, is the assembly step whose conclusion is `ChainTied`, the giant existential that ties the abstract engine to concrete family data.
5. **The exponent 1/2 is a parameter choice.** It is not an output of the slope inequality. `RankVal` forces the number of "lifts" m ≈ x^{1/2−ε/16} (`Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean:28-32`). The engine's error terms have size about a·(1 + m²/k)/m per unit, and balancing them gives √x. So the real question is whether the slope and degree inequalities hold uniformly at such large ranks (k ≈ x^{9/2}, group order n ≈ x^{2+8ε}).

---

## 1. What enters and what exits

**Output.** `UpperTheory.EveryCharacter` (`EveryCharacter.lean:13-14`):
for all N, all χ mod N and all s with Re s > 1/2, and (χ ≠ 1 or s ≠ 1), L(s, χ) ≠ 0.

**Imprimitive reduction.** `Imprimitive.lean:5-35` derives this from `ZeroFreeAll` (primitive characters only, `Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ExplicitFormulaErrorOfHostConditions.lean:11-18`). It uses L(s, χ) = L(s, χ*) ∏_{p|N}(1 − χ*(p)p^{−s}) and the fact that |χ*(p)p^{−s}| < 1 when Re s > 0. This is clean and standard.

**Inputs of `plugAll` / `plugWin`** (`EveryCharacter.lean:8-11`):

| Input | What it is | Where it is used in the cone |
|---|---|---|
| `hG : GlobalTheory.GLq.Green` | Green's (1955) classification: cuspidal irreducible characters of GL_d(F_g) are in bijection with "prime labels" of degree d, with degree ∏_{i=1}^{d−1}(g^i − 1) (`Development/AbelianVarietyTheory/Definitions/NonGaloisDescent/LabelDatum.lean:108-112`) | only in `link_irr`, i.e. the LinkIRR bound (row loss δ is tiny) |
| `hV : VWin` | for every primitive ψ, `VWinAt ψ 401` (`CharacterBoxes/ExistsPageN.lean:44-49`): a bound on Galois-cohomology "Sha lengths" of abelian "χ-fields" (§3.4) | `supplyChi` builds host families; HypV feeds LinkN to DIVinN |
| `h : Nonempty (Hyps N DRS)` with N = `Closed · LinkN` | a ~45-field bundle (`Definitions/GlobalTwisting/APerTw.lean:23-91`) containing the **family class 𝒜 itself**, selections σ, and every per-family hypothesis that `TopShape` demands | `shape_of` unpacks it into `TopShape` (`Proofs/GlobalInterpolation/ShapeOf.lean:6-15`) |

**Oddity.** `plugWin` passes `trivial trivial` for the `V` and `NR` slots of `TopShape True True …` (`EveryCharacter.lean:11`). Two hypothesis slots are therefore vestigial.

**Literature inputs hiding inside `Hyps`.** These fields are imported, not proved in the cone:
- `hLit : LitThin` (`Formalism/SharpRestriction/GlobalSchurBounds/MainSup.lean:88-90`, components at `ShortIntervalPrimes.lean:128-161`):
  - (a) a zero-density bound: Σ over primitive χ of conductor ≤ Q of the number of zeros with Re ρ ≥ 1 − 1/400 and |Im ρ| ≤ Q is ≤ C₁Q^{1/4};
  - (b) the Landau–Page zero-free region with at most one simple real exceptional zero, plus de la Vallée Poussin's region for ζ;
  - (c) a truncated explicit formula for ψ₀(u, χ);
  - (d) the zero count ≪ log(N(|t|+2)) in unit windows.
- `hG : ∀ D, GenusMassAt D 2`: the Siegel mass formula for rank-2 definite hermitian lattices (`Formalism/LocalToGlobal/GlobalTheory/GL5/DiscreteSeriesOfFormalDegree.lean:112-114`).
- `hU : ∀ D, MassRatioUnderVolume D`.
- `nRest : Closed (D3 3 𝒜) LinkN`: **LinkN itself is an input**.
- Several more: `hWu`, `hRF`, `sTy`, `sNG`, `sM`, `sLp`, `sO`, `h30`, `zL`, `tie`, `irrC`, …

A scan of the CharacterBoxes, DedekindLFunctions, PrimitiveCosets, MeanSquareBounds, SizeWindowBrackets, RankGapBounds, GlobalSchurBounds and RamificationFrobenius directories found no `sorry` and no `axiom`, and `lean/src` contains no top-level `axiom` declarations at all.

---

## 2. Layer A: the analytic endgame (classical, self-contained)

### 2.1 Objects

For a Dirichlet character χ, define the smoothed remainder (`TotientGaloisClasses/Analytic.lean:14-24`, `Formalism/StatementOC.lean:11-13`):

$$g_\chi(y)=\sum_{n\le y}\Lambda(n)\chi(n)\Big(\tfrac yn-1\Big)+y\,\frac{L'}{L}(1,\chi)\quad(\chi\ne1),\qquad G(y)=\sum_{n\le y}\Lambda(n)\Big(\tfrac yn-1\Big)-y(\log y-1-\gamma).$$

The kernel (y/n − 1)₊ has Mellin weight 1/(s(s−1)). Shifting contours, g_χ(y) = −Σ_ρ y^ρ/(ρ(ρ−1)) + O(log y): an absolutely convergent explicit formula. So "g_χ(y) ≪ y^{1/2+ε}" is the natural GRH-strength statement.

For a primitive ψ, let Λ_ψ = `Level.cyc ψ`, the primitive versions of the cyclic group ⟨ψ⟩ of order o (`ExplicitFormulaErrorOfHostConditions.lean:121`). Define

$$\mathrm{Gm}_{\Lambda}(y)=G(y)+\frac1{3o+1}\sum_{\chi\in\langle\psi\rangle\setminus\{1\}}\mathrm{Re}\,g_\chi(y)$$

(`:36-38`; `psK = none` for cyclic levels, `:105-114`). The Dirichlet coefficients are Λ(n)·(3o + o·1[ψ(n)=1])/(3o+1) ≥ 0, so the combination is positive.

### 2.2 The Landau window lemma (`formB`)

`Level.FormBAt la` (`TotientGaloisClasses/Window.lean:30-31`) says: if {x : Gm(x) ≤ x^θ} contains a window [Y, Y^{la}] beyond every point, then there are no zeros with Re s > θ. It is proved for every la > 1 by `UpperTheory.Comparison₂.formB` (`PrimitiveCosets/Imports.lean:8-19`), which reduces to `Deduction.zeroFree_of_rpow_window` (`DedekindLFunctions/LandauTheorems/ZeroFreeOfRpowWindow.lean:11-14`) and then `lemmaL` (`lemmaL.lean:13-22`).

The mechanism (`landauWindow.lean:20-73`):
- Take Taylor coefficients of order k ≈ U = log Y of the Mellin transform Φ at σ > 2.
- The kernel u^k e^{−σu}/k! concentrates in the log-window [U, (1+δ)U].
- The one-sided bound R − Gm ≥ 0 gives ‖Φ_k(σ+iγ)‖ + Re Φ_k(σ) ≤ C e^{ηU}/(σ−θ)^k for every γ.
- A zero at β + iγ with β > θ makes Φ_k(σ+iγ) grow like (σ−β)^{−k}.
- `landau_window_contra` turns c/d^k ≤ M/e^k + C e^{ηU}/E^k with d < e ≤ E into a contradiction.

**This is a reusable engine.** It is a localized Landau/Pintz theorem: one-sided bounds on sparse multiplicative windows already force zero-freeness.

### 2.3 Driving a hypothetical off-line zero to a contradiction

`level_of_tiedWin` (`TotientGaloisClasses/TopWin.lean:68-81`). Suppose L(s, ψ^k) = 0 with Re s > 1/2.
1. Set Δ = min(Re s − 1/2, 1/2).
2. Choose ε so small that (e_D + e_L + 7)ε ≤ Δ/2 (`exists_small_eps`, `:59-66`).
3. Take the family Fm(ε) promised by `ChebyshevInequalityAtWindowScale`. It has windows [Y, Y^{3/2}] and `ChainTied` on them.
4. `ChebyshevInequalityOnWindows` (`:26-28`) gives Gm(x) ≤ x^{1/2+(e_D+e_L+7)ε} ≤ x^{1/2+Δ/2} on those windows.
5. `formB` with θ = 1/2 + Δ/2 < Re s contradicts the zero.

In the live instantiation, e_D = Cabs = 2 and e_L = 0 (`ShapeWin.lean:46`; `LinkGl.lean`'s `LinkGLOBAL Fm 2 CH 3 2 0`), so the exponent is **1/2 + 9ε**.

`zeroFreeAll_of_topG` (`CharacterBoxes/ZeroFreeAllOfTopG.lean:26-34`) feeds this with la = 3/2 and G = `GChi ψ`. `TopG` (`:12-14`) is the statement "for every la > 1 and every host requirement G with `HostExW la G.req` and HypV, `FamilyClassConnected (G.cls la)`".

### 2.4 From `ChainTied` to the Gm bound

`level_gm_le_on_family_scales` (`PrimitiveCosets/LevelGmLeOnFamilyScales.lean:28-30`) goes through `windowInequality_of_artinInputs` (`WindowInequalityOfArtinInputs.lean:17-25`) to `core_gm` (`CoreGm.lean:12-74`):

> EAtH Λ H TT x ε C ∧ CoreAtH H TT e_D e_L K c_HH e_K ε x ⟹ Gm_Λ(x) ≤ x^{1/2+(e_D+e_L+7)ε}.

`core_gm` is the junction where Layers B–D (below) meet. It calls `Deduction.ch_core` (character balance) and `Deduction.ch_top` (gap bound from the abstract engine).

---

## 3. Layer B: the host field and three kinds of characters

### 3.1 What a host is

A `Frame` (`ZsmulGeneratorEqZeroOfProjection.lean:15-23`) is a finite abelian group A of order n with a surjection to a cyclic 2-group H(e) and a distinguished cyclic subgroup A₀ = ⟨a₀⟩. Its group GG = (±1 × ±1) × A.

A `HostRaw` (`ConjEMemHostFIff.lean:12-49`) is a **Galois CM number field E/ℚ** with Gal(E/ℚ) ≅ GG. It contains √−d, embeds in ℚ(ζ_{QS·q·d}), and has an explicit Artin map art: (ℤ/QS·q·d)^× → GG. Its constraints include 2^{e+2} | QS, (−d/l) = 1 for odd l | QS, and art(−1) = complex conjugation. Here q and d are primes. The degree is [E:ℚ] = 4n (`:195`).

Sizes, from `RankVal` (`PairRowIffQdRows.lean:28-32`):
- n ≈ x^{2+8ε}
- m ≈ √(x·x^{−ε/8})
- k ≈ x^{9/2+10ε}

`PageN` (`ExistsPageN.lean:39`) pins 2^e ≈ x^{2+8ε}.

### 3.2 Three kinds of characters

Characters of E split three ways (`Analytic.lean:136`; `PrimitiveCosets/CoreAtH.lean:24-25`):
- **Kept**: the members of Λ_ψ = ⟨ψ⟩, all even type (`KeptInXp`). These are the targets.
- **Bounded**: the other even characters and all odd characters. `boundedTw_key` (`CharacterBoxes/BoundedTw.lean:5-43`) shows every bounded character is induced by a twist
  $$\mathrm{tw}(\xi,q,d,i,j)(a)=\xi(a)\Big(\tfrac aq\Big)^i\Big(\tfrac ad\Big)^j,\qquad (i,j)\ne(0,0),$$
  with ξ mod ψ.N (`PairGood.lean:9-10`).
- **Thin-scale behavior of all characters**: for y ≥ exp(x^{ε/3})/3, `ThinScales` (`SizeWindowBrackets/GrowthBoundGivesRiemannHypothesis.lean:55-56`) requires ‖g(y)‖ ≤ θy with θ tiny (`CostWindows`: 2f(x+1)θ ≤ 1/x, `SChain.lean:50-51`). This is a PNT-in-progressions statement at astronomically large y, fed by `ChebyshevCharacterBound` (decay exp(−c x^{ε/8}), `Analytic.lean:145-147`), classical zero-free regions (`LitThin`), and `RealBox`/`ZeroBox`.

### 3.3 The key trick: the characters you do not control get gigantic conductors

`WinPair` (`ExistsPageN.lean:27-37`) requires:
- log q ≈ Y^{ε/5} and log d ≈ Y^{ε/5} log²Y, with Y ≤ x ≤ Y²;
- q ≡ 3 (mod 8), d ≡ 7 (mod 16), q | d+1;
- p | d+1 for every odd p ≤ Y^{ε/5}.

So the bounded characters have conductors ≈ exp(x^{ε/5}), which is far larger than x. For those, the RH-strength statement at the single scale x,

> `PairGood.bounds` (`PairGood.lean:21-23`): ‖g_χ(y)‖ ≤ y^{1/2+ε/2} and |L'/L(1,χ)| ≤ 4 log y for Y ≤ y ≤ X,

is a short-sum statement. `QH.pairEx` (`MeanSquareBounds/pairEx.lean:112`) proves it by **averaging over (q, d)**: `pair_exists` → `pair_share`, `meanSqK`, `kappa4`, together with zero-free boxes `ZeroBox` at 1 − 1/400 up to height ≈ 8M·exp(Y^{ε/5})… (`PairGood.lean:12-16`).

This is the single most interesting conceptual move in the cone. "RH at x" is needed only for twisted characters whose conductor dwarfs x. For a positive proportion of twists, that is a large-sieve fact.

The same trick covers the three quadratic characters ψ ∈ {psC, chC, chpsC} in `ValuesAtX` (`GrowthBoundGivesRiemannHypothesis.lean:67-69`). The host-side packaging is `EAtH` (`ExplicitFormulaErrorOfHostConditions.lean:144-151`), with fields o_eq, kept, ps, shares, bdG, bdL, plus the requirement `GChi ψ` (`CharacterBoxes/Supply.lean:42-43`).

### 3.4 What `VWin` / `HypV` say

`VVle E t B` (`ExistsPageN.lean:12-17`):
- for every prime p and 0 < e < t, the Sha length is finite;
- Σ_{l∈S} log l · Σ_{1≤e<t} shaLen_l(e) ≤ B.

`VWinAt ψ 401` (`:44-47`) asks for this with t = ⌊x^{401}⌋ and B = √(exp(x^ε)) for every "χ-field" `IsChiField ψ e q d E` (`:19-25`): the abelian field cut out by a ≡ ±1 mod 2^{e+2}, ψ(a) = 1, (a/q) = (a/d) = 1.

`HypV` (`DivinNOfHypV.lean:10-11`) is the same bound evaluated on family members with B = √b, where b = e^{x^ε}.

Reading: this is an Iwasawa/Lichtenbaum-type size bound on Tate–Shafarevich groups of Tate twists over abelian fields. The constant 401 is just 400 + 1, because `eventually_rank_le_rpow_of_lt_one_div_fiftytwo` shows R.t ≤ x^{400} (`CharacterBoxes/EventuallyRankLeRpowOfLtOneDivFiftytwo.lean:5-7`).

---

## 4. Layer C: an exact prime-count identity and character balance

### 4.1 Arithmetic side vs. main term

The definitions are in `SizeWindowBrackets/FirstPrimeNeSecondPrime.lean:68-100`.
- `GPsi D ell ψ y` is g for the host character ψ, using `primVal` (coset means over inertia) and ℓ(ψ) = L'/L(1, ψ).
- **ASK**(a, t, w) = Σ_{p inert} 2 log p · Σ_i (a/p^i − w(partner(t, i·Frob_p)))₊ + log d · (ramified-at-d term). This is a weighted count of inert primes at height a, cut off at w.
- **MAIN**(a, w) = a·(log a − 1 − γ + ℓ(χ_C) − (1/|Φ|) Σ_ρ log w_ρ).
- **AskMainBalance**: ASK − MAIN = De, where De = |Φ|^{−1} Σ_{g∉Φ} Σ_ψ ψ̄(g) w·GPsi(ψ, a/w). It is proved as `colour_balance` (`ChainSlopeWindows/StronglyIrreducible.lean:695`).

So an upper bound ASK ≤ MAIN + E becomes an upper bound on a character combination of the g's.

### 4.2 Thick vs. thin

`th_le` (`LandauTheorems/ChCore.lean:75-152`):
- At thick nodes, b ≤ w ≤ b + η + 1, so a/w ≈ x: this is the RH scale.
- At thin nodes, w ≤ 2b′, so a/w ≥ X′/3 = exp(x^{ε/3})/3: this is the PNT scale, absorbed by `ThinScales` and `LipW`.

The scale parameters are in `Formalism/LocalRingCardinality/DataParams₂.lean:27-45`: L = x^ε, b = e^L, a = xb, X′ = exp(x^{ε/3}), b′ = a/X′.

### 4.3 The Fourier weight trick (where `3` and `4` come from)

`Frame.Shares TT δ` (`ExplicitFormulaErrorOfHostConditions.lean:135-140`) requires the test set TT to hit each A₀-coset γ with frequency
- λ_γ = 4/(3o+1) for γ ∈ A₀,
- λ_γ = 3/(3o+1) otherwise,

with error x^{−1+ε}. The Fourier transform of this distribution over characters of A/A₀ is 1 on the trivial character and **1/(3o+1)** on every non-trivial one. That is exactly the weight `wt` in Gm_Λ (`:36`; `CharsA` in `SplitInertia.lean:54-61`).

So averaging De over t ∈ TT and translates u ∈ A₀ (`sum_A`, `sum_Th`, `ChCore.lean:28-73`) isolates GmA. `ch_core` (`ChCore.lean:343-349`) states:

> GmA(x) ≤ x^{1/2+(C+3)ε} + SigA(x), provided gap(u) ≤ x^{Cε}·errorBracket for all u ∈ A₀.

Here SigA = Σ_{bounded ψ} ‖GPsi(ψ, x)‖ (`SplitInertia.lean:39-40`). It is controlled by `sigA_le` (`CoreGm.lean:62`) from `BoundedCharsPointwise`.

### 4.4 Where the exponent 1/2 comes from

`errorBracketSizeWindows` (`ErrorFormsWeakWindowsFalse.lean:133-135`) is
n_T·a_E·(1 + m²/k) + m(2n·m·b·x^ε + …).
`RestSize` (`SChain.lean:53-58`) gives x^{1/2−ε} ≤ m and k ≤ n²x^{1/2−ε}; `ErrWindows0` gives m ≤ x^{1/2+ε/2} and xm ≤ k. After normalizing by the n_T·m·b mass, the dominant term is ≈ a_E/(m·b) ≈ x/m ≈ x^{1/2}. **The √x is m.** The size choice m ≈ √x is the only place it enters.

---

## 5. Layer D: the abstract slope/height inequality engine

`Formalism/RankGapBounds/MeanBoundSecondForm.lean:37-82` defines `Data U0 W Top m f`. It is a bag of reals indexed by translates u₀ ∈ U₀ and "words" u ∈ W(u₀):
- d (ranks), T (a level prime per word), μ_N, μ_N^max, h (heights), μ_M, μ_M^max, E_{e,j};
- per u₀: μ_CC, μ_CC^min, Fo, Ga ("gain"), Ta, ASK, IO, HH, δ, η, e.

`PointwiseBoundVariant` (`SizeWindowBrackets/QuotientSlopeBoundsWith.lean:72-75`) states: 11 hypotheses imply ASK(u₀) ≤ Main(u₀) + ErrX5at(u₀). It is proved by `each_unit_bound_statement` (`ChainSlopeWindows/LevelOfCongruence.lean:175-200`) using `linarith` and monotonicity only. **The engine is pure real-number algebra.** The 11 hypotheses (`SChain.lean:17-19`) are:

| Hypothesis | Content (MeanBoundSecondForm line) | Role |
|---|---|---|
| `DIV` (:118) | μ_CC + h_u − Fo ≤ Σ_t [m(φ(a_t) − a_t log Ω) − a_t log T_u] + c_Div(n_T a L_a + m(B₀+N_c)x^{e_Div ε}), with φ(y) = y log y − y and log Ω = γ + log(π/v) − L′/L | **degree upper bound** |
| `SlopeIneq` (:151) | s − log\|W\| − (1−δ)^{−1}[4u_F log(1 + HH/u_F) + (η + 4√e)HH] ≤ μ_CC, where s = wmean_d(μ_N − h) | **slope lower bound** with an entropy term |
| `SlopesN` (:143) | μ_M + Ga + Fo − Ee − Lo ≤ μ_N, and μ_N^max ≤ μ_M^max + Ga + Fo − Ee + … | gain raises slopes |
| `Losses` / `LossBounds` (:148; QSBW:34) | ASK − Ga ≤ LoP = c_Loss n_T m b x^{e_L ε} | **prime count ≤ gain** |
| `Count` (:131) | (1/f)Σ_ρ log(w_ρ v/π)·m + m·lg − … ≤ log T_u ≤ c·mL | level prime T sized by the weights |
| `EComp` (:123) | \|E_{e,j} − (Σ_t a_t)·lg\| ≤ c_E B₀ | local contributions ≈ main |
| `HComp` (:126) | h_u + Σ a_t log T_u nearly independent of u | |
| `Slopes` (:139) | bounds on μ_M, μ_M^max | |
| `HHBound` (:158) | s − μ_CC^min ≤ HH ≤ x^{c_HH} b | |
| `FParams` (:161) | δ ≤ δ̄, η ≤ η̄, e ≤ ē | smallness |
| `HidaSetting` (:111) | positivity | |

**How the inequalities clash.** Chain them:
ASK ≤ Ga + LoP (Losses) → Ga ≤ μ_N − μ_M − Fo + Ee + Lo (SlopesN) → average to s → s ≲ μ_CC + entropy (SlopeIneq) → μ_CC ≤ [DIV main] − h + Fo (DIV).

The main terms then cancel to exactly MAIN:
- m·a(log a − 1 − γ + L′/L) − m·a·log(π/v) from DIV,
- minus a·log T ≥ a·Σ_j (1/f)Σ_ρ log w + a·m·log(v/π) + a·m·lg from Count;
- the ±m·a·log(π/v) terms cancel, and m·a·lg cancels against Ee via EComp.

The remainder is Main(u₀) = Σ_j Σ_t a_t(log a_t − 1 − γ + LpL − (1/f) Σ_ρ log w_{jρ}). I did this matching by hand from the definitions. It is strong evidence that the engine is set up to reproduce the prime-count main term from a height main term.

**Surprise (interpretive).** log Ω = γ + log(π/v) − L′/L(1, χ_C) (`:88`) has the shape of the Chowla–Selberg/Colmez period formula: the Faltings height of CM objects involves L′/L(1, χ_K), γ and log π. If that reading is right, **the L′/L(1, χ_{−d}) term in MAIN is literally a CM period**. The prime count is being compared against heights of CM objects at height scale a = x·e^{x^ε}.

---

## 6. The nine links decoded

All definitions are in `Formalism/SharpRestriction/GlobalTheoremInputs.lean`. "Eventually" means ∃x₀ ∀x ≥ x₀ ∀ members i ∈ Fm.Ix x.

| Link (line) | Mathematical content | Engine slot it feeds | Produced by (cone top) |
|---|---|---|---|
| **LinkN** (40-47) | if Sha is finite, then for each lift j: η-sum = Σ_{w: μ_w ≠ μ₀} ℓ_w·e_w·η_j(w) ≤ dZ₀(j)·[C(f·m·b·L² + log²x·N_c) + Σ_l log l·Σ_{e<t} shaLen_l(e)] | → DIVinN | **input** (`nRest` in Hyps) |
| **LinkEta** (49-50) | eventually `LocsCoverTw`: twist loci cover | antecedent of LinkDIVt | `link_eta` from `tied_families_of_choice` (`LinkEta.lean`) |
| **LinkIRR** (55-57) | eventually δ_p ≥ 0 and δ_p ≤ exp(−x^{ε/(7J)}). δ_p is the fraction of lost rows: Drows = (1 − δ_p)·Dall (`LocalRingCardinality/DataRows.lean:69-71`) | δ in SlopeIneq / FParams | `link_irr hGreen …` (**uses Green**) |
| **SmallLevelRankEq** (52-53) | eventually dZ₀(j) = D₀ for all lifts j | lets LinkN become DIVinN | `smallLevelRankEq_closed_of_levelProjection_surjective` from input `zL` |
| **LinkDIVt** (94-95) | LinkEta → DIVinN → LinkDIV. LinkDIV_at (77-89) is a 9-fold conjunction: OneMap, **sFrame + μ_max ≤ x^{CH}·b** (HHBound), ZeroAbove, BesselId, RRFull, HN-height ≤ h, **μ_dual + h − Fo ≤ MAIN + C\|TT\|aL_a + Cm(B₀+N_c)x^{Cabs·ε}** (DIV), **\|ΣE − Σa·log(g₀g₁)\| ≤ CB₀** (EComp), **h-oscillation** (HComp) | DIV, EComp, HComp, HHBound, Lat | `linkDIVt_closedK` on `BridgeRowsK`, built at `ShapeWin.lean:36-41` from `link_brest`, `wire_sel`, `closed_family_admissible_twist_link`, `selection_closed_of_wu_decay` |
| **NuFullF ∧ J.MuRank** (72; hRk) | ChosenE → full rank of the N-lattices ∧ rank compatibility | with LinkDIV gives LinkMu (`DesWin.lean:31`) | `link_gl … .1` via `FamGLmin.muRank` |
| **LinkG** (122-140) | at each inert place w (resChar ≤ X″): Σ_j Σ_t (vonMangoldtClassSum − loss) − m·flG ≤ Σ_j gain_j(w) − τ(w), and 0 ≤ gain ≤ 4\|TT\|a/p; plus local lattice inclusions and orbit bounds | **SlopesN, Losses** (gain vs prime count) | `link_g` → `linkG_concrete5` |
| **LinkS** (145-156) | TuSize → near-orthonormal Gram data: off-diagonal ‖K_{uu′}‖²_HS ≤ (1+η₀)d_u d_{u′}/D*, ‖K_{uu} − 1‖²_HS ≤ e₀d_u, Dall ≤ (1+η₁)D*, with η₀, η₁, √e₀ ≤ exp(−x^{ε/8}) | η, e in SlopeIneq | `link_alt` → `theoremS_transport_link_zero` |
| **LinkGLOBAL** (162-164) | ChosenE → (LinkG ∧ LinkS ∧ LinkIRR ∧ LinkDIV ∧ LinkMu) → ∃K, c_HH, e_K, C_L, x₀: ChainTied on Fm.Win ∩ [x₀, ∞) | **assembly** | `link_gl … .2` = `FamGLmin.link8` → `linkGLOBAL7_min` (`GlobalSchurBounds/LinkMin.lean:723`) → `linkCore` (`LossesSmallShares.lean:38`) |

**Supporting notions.**
- **HypV** (`DivinNOfHypV.lean:10-11`): eventually VVle(E_host, t, √b). It turns the Sha term in LinkN into ≤ b, giving DIVinN: η-sum ≤ D₀·C·x^ε(B₀ + N_c) (`divinN_at`, `:76-115`, using log²x ≤ x^ε).
- **ChainTied** (`GlobalSchurBounds/TieGlobal.lean:97-114`): ∃ a base member i₀, a point map pt: A → Ix x, an abstract `Data`, constants C with eDiv ≤ e_D and eLoss ≤ e_L. The data is tied to the family by `TiePts` / `TieGlobal` / `TieLocal` / `TieArith` / `Ident`. Then `SizeData₂` (the 11 hypotheses), `ErrWindows`, `BNBounds`, `GrowthInequalityRemainingHyps` (sizes, ThinScales, ValuesAtX), `CostWindows` and `RestSize` all hold. It is mostly a dictionary plus the engine's hypotheses.
- **Closed 𝒞 P** (`ParamsHeightRankConstant.lean:159-161`): for small ε there is a threshold K = (pre, mid, last) such that every Fm ∈ 𝒞 whose constants dominate K satisfies P. `FamP.Large` (`:138-140`) is three-tiered: mid thresholds depend on `cOut`, last thresholds on `cOut ++ cMid CH`. It encodes "choose constants in order".
- **DesignExists 𝒞 C₀** (`:187-190`): for small ε and every K, some Fm ∈ 𝒞 is Large(K) and satisfies ChosenE, TuSize and DGamSize. Supplied by `link_ex` (`LinkEx.lean:15-37`) from `hEx minkowski_bound_rat`, `hTu`, `hn4` and `hLit`.
- **Des / D3** (`DesignExistsDes.lean:10-13`, `ClassOfRecordOfChoice.lean:48`): D3 3 𝒜 = Des(WithChN 𝒜) 3 = class ∧ DGamSmooth ∧ TwGood ∧ ∃CH ChosenE ∧ TuSize ∧ DGamSize.
- **FamilyClassConnected ℰ** (`DivinNOfHypV.lean:13-15`): ∃e_D, e_L, ε₁ such that for every ε < ε₁ some Fm ∈ ℰ is ChainTied at all large window points. **Misnomer**: no connectedness is involved. It is "a tied family exists at every small ε".

**`topDesWin` (`DesWin.lean:11-31`) is pure logic.** It intersects the nine Closed facts, takes the threshold K, asks DesignExists for a Large(K) family, then wires: DIVinN ← (HypV, LinkN, SmallLevelRankEq) → LinkDIV ← LinkDIVt; LinkMu ← (LinkDIV, rank, μ_Tu, μ_DGam); finally LinkGLOBAL.

---

## 7. The whole contradiction in one chain

Fix ψ and a putative zero with Re ρ > 1/2, and choose ε ≪ Re ρ − 1/2. Then:

1. **Supply.** `supplyChi` (`SupplyChi.lean:8-16`) uses VWin and pairEx to give host fields E at every scale s in a scale set of window ratio 3/2. Each E satisfies EAtH(⟨ψ⟩, …, C = 4) and VVle(√b). In E, the bounded characters have RH-at-x by averaging over (q, d), and the thin scales have classical PNT.
2. **Families.** Hyps provides a family class 𝒜 of such data with all ~45 structural facts. `ExS` and `link_ex` give a family Fm(ε) in 𝒜 ∩ GChi.cls(3/2) with constants above any threshold.
3. **Links.** The nine links hold for Fm. LinkGLOBAL gives ChainTied at every window point x.
4. **Engine.** ChainTied yields ASK ≤ MAIN + x^{(e_D+e_L+3)ε}·errorBracket (`ch_top`, `ChTop.lean:37-72`).
5. **Balance.** The identity ASK − MAIN = De and the Fourier-weight averaging give Gm_⟨ψ⟩(x) ≤ x^{1/2+9ε} on [Y, Y^{3/2}] for arbitrarily large Y (`ch_core`, `core_gm`).
6. **Landau.** The window lemma (`formB`) contradicts the zero.

---

## 8. Conceptual weight vs. plumbing

**Heavy and mathematical:**
- the Landau window lemma (Layer A, about 30 files in `LandauTheorems/`, fully proved);
- the twist-averaging that gives `pairEx` (`MeanSquareBounds/`, 35 files);
- the identity ASK − MAIN = De (`colour_balance`);
- the Fourier-weight design (λ = 4 or 3 over 3o+1);
- **above all, the content of LinkDIV (degree upper bound), LinkS + LinkIRR (slope lower bound with near-orthonormality and tiny row loss), and LinkG (gain ≥ prime count)**.

Whether those three can hold simultaneously at ranks k ≈ x^{9/2} is the crux. Here the 2,038 SharpRestriction files and 2,576 LocalToGlobal files of the cone do their work.

**Plumbing:**
- `topDesWin`, `shapeWin`, `shape_of`, `Closed.and` / `imp`;
- the ChainTied ↔ CoreAtH ↔ FamCoreConstantBounds transports (`tiedCore_of_chainTied`, `LevelGmLeOnFamilyScales.lean:13-26`);
- the Data engine itself (`linarith` over 11 hypotheses);
- the `Large` / `TransportedAlt` threshold bookkeeping;
- `FamCore`'s ~40 equality fields (`SharpRestriction/FamCore.lean:71-139`) forcing all members at a scale to share q, d, QS, Artin data and word codes.

---

## 9. Surprises and reusable engines

1. **A localized Landau theorem** (`DedekindLFunctions/LandauTheorems/`): one-sided bounds on sparse windows [Y, Y^{1+δ}] for any δ > 0 suffice for zero-freeness of any `CharFamily`. It is portable to other positive Dirichlet series.
2. **The huge-conductor twist trick**: RH-at-a-single-scale for characters twisted by (·/q)(·/d) with log q ≈ x^{ε/5}, via mean squares and `ZeroBox` density. It is reusable for any "make the bad L-functions generic" argument.
3. **The Fourier-weight test set**: a coset distribution 3 + 1_{A₀} produces the positive kernel 1 + (3o+1)^{−1}Σχ. This gives a combinatorial way to isolate ⟨ψ⟩ inside a host's character group.
4. **The abstract slope engine**: an Arakelov-flavored "count ≤ gain ≤ slope ≤ degree" inequality in pure reals. It can be reused, or audited for tightness, independently of everything else.
5. **The Chowla–Selberg-shaped log Ω** in the main term (interpretive).

---

## 10. Brittle joints, magic constants, open threads (Wave 2)

**Constants:**
- **la = 3/2** is just the window ratio. `formB` works for any la > 1, and `VWinAt` uses [Y, Y²].
- **401** = (R.t ≤ x^{400}) + 1.
- **1/52** is the global ε ceiling (`HType.eps_lt`, `Scale.eps_lt`). I did not find its source; it probably comes from exponent budgets like 2 + 8ε and 9/2 + 10ε.
- **2** = Cabs = e_D, the exponent of x^{Cabs·ε} in LinkDIV. **3** = C₀, the design constant, so D3 3. e_L = 0.
- **A = 26** gives p₀(k) = k²x^{26} (`DataParams₂.lean:41-43`).
- **1 − 1/400** in ZeroBox and LitThin; **Q^{1/4}** in the zero-density input.
- Congruences q ≡ 3 (mod 8), d ≡ 7 (mod 16), q | d+1.
- **(3/2)^{1/ez}** threshold in `linkIRR_of_join_ex`; **exp(−x^{ε/8})**, **exp(−x^{ez/7})**.

**Oddities:**
- `LitThin` quantifies `∀ D : D7` over statements that **ignore D** (`adm6 (_D : D7)`). The bundle is vacuous if D7 is empty. In practice the families inhabit it, but the dummy argument is fragile.
- `V` and `NR` in TopShape are set to `True`.
- **LinkN is assumed** (nRest), not proved, here. Its proof (`boundAtTwoThree_at_prm_of_prints P.nLink`, `EveryCharacterE.lean:71`) is the real "η-twist controlled by Sha" content and belongs to Wave 2.
- The `Large`-threshold game lets constants such as CTu and CH grow without limit. Wave 2 should check that no link becomes easy when its constant is huge. LinkDIV's CH appears as x^{CH}·b in HHBound and in the code-size bound `CodeUpF`.

**Deeper branches to open in Wave 2:**
- (a) `linkG_concrete5` and `stLoss7`: is gain ≥ inert-prime count proved with the claimed loss LoP ≈ n_T·m·b·x^{e_Lε}?
- (b) `bRest_all` / `linkDIVt_closedK`: where the **degree upper bound** comes from (BridgeRowsK, `wire4F`).
- (c) `theoremS_transport_link_zero` + `frameF_of`: the near-orthonormality and the entropy slope bound, uniform in rank k ≈ x^{9/2}.
- (d) `FamGLmin` fields (`LogXLowerFamilyOfTheorems.lean:39-50`): mass ratio, base volume = mass, σ-degree bounds, all derived from `tie`, `hU`, `hG`.
- (e) Who constructs the family class 𝒜 in Hyps, and whether its existence is non-vacuous at the extreme sizes n ≈ x^{2+8ε}, k ≈ x^{9/2}, a = x·e^{x^ε}.
- (f) The `VWin` proof cone (`VwinOfRow`), i.e. Sha bounds for χ-fields.
- (g) `green_of_regular`.
