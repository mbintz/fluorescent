# Audit report: Package A (`DivWCoreLac`) and Package B (`PairBoundAbstract`, `TheoremFSharp`, `SharpRecursion`, `goodBadCut`)

**Path abbreviations.** All paths are under `lean/src/`:
- `DC/` = `Development/EtaleCohomology/DivisorCycles/`
- `CLD/` = `Development/WeilBound/CoreStatements/PadicHodgeComparison/CocharacterLieDivisors/`
- `ZCD/` = `Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/ZetaCharacterDivisibility/`
- `HC/` = `Formalism/HermitianCurvature/`
- `HN/` = `Formalism/HarderNarasimhan/`
- `CS/` = `Formalism/CorankShare/`

**Formalization status.** A grep for `sorry`, `axiom` and `admit` over `DC/`, the Package B proof files, `CS/`, `GoodBadCut.lean` and `MajAtAddRight.lean` found nothing. I read the source but did not build the project. I read the proofs of `ConjugateIdempotents`, `UnitFactorizationTheorem`, `MatUnitsOf`, `MinCongr`, `FinSubOf` and `FinEmbedPf` only at the level of their statements; they are standard Wedderburn and Gauss-elimination facts. My numerical checks are scratch scripts in `/tmp/audit_scripts/`; nothing in the repo was touched.

---

## 0. Verdict

| Item | What it really is | New? | CM/QI value |
|---|---|---|---|
| `DivWCoreLac` | A rigidity theorem in the style of Boston–Lenstra–Ribet (BLR), in dimension n. It *constructs* the n-dimensional rep r from minimal polynomials plus one lacunary Lie-algebra element, and works over ℓ-adic fields. | Real content in the ℓ-adic / profinite setting. Lacunarity is genuinely needed when the group is disconnected. I give a counterexample which also shows that the in-repo `DivWCoreSidon` is **false**. | **Low.** Over ℂ it follows from weight theory plus Clifford theory. The hypotheses force G° ⊂ ∏U(m_a) acting by standard reps. It never sees multiplicities and does not apply to S_z, N or other local charges. |
| `PairBoundAbstract` | Upper frame (Gram) bound plus the triangle inequality. | No. | None. |
| `TheoremFSharp` | Reverse Markov + a frame-codimension lemma + the Bost-type slope inequality + layer cake. | The packaging is reasonable; every part is textbook. The "−log\|I\| removal" is trivial. | The frame lemma `FrameLA1` is a small, usable lemma. Its constants are loose; I give improvements. |
| `SharpRecursion` | Discrete Grönwall with geometric memory. | No. The constant 80 can be replaced by **e²−1 ≈ 6.389, which is optimal**. | Folklore. |
| `goodBadCut` | Covolume sandwich under an orthogonal projection that is integral up to a factor g. | No (geometry of numbers). | None. |

---

## Package A — `DivWCoreLac`

### A.1 The exact theorem, without the Galois wrapper

**Definitions** (`CLD/DivWCoreLacUseType.lean`, `CLD/MeetsOpenCosets.lean`):
- **Lacunary** (`IsLac`, `DivWCoreLacUseType.lean:86-88`): e : [n] → K' is lacunary if for all disjoint nonempty A, B ⊆ [n], |B|·∑_{A} eᵢ ≠ |A|·∑_{B} eᵢ. Equivalently, **no two disjoint nonempty subsets have the same mean**. This is invariant under affine maps e ↦ αe+β. It implies injectivity (`DC/OpenCoset.lean:12-14`).
- **Completely reducible** (`IsSSMat`, `MeetsOpenCosets.lean:10-14`): every invariant subspace has an invariant complement.
- **In the Lie algebra of the Zariski closure** (`InLieZar ρ X`, `MeetsOpenCosets.lean:16-22`): for every polynomial f vanishing on ρ(Γ), df₁(X) = 0. So X ∈ Lie(G) ⊗ K', where G is the Zariski closure of ρ(Γ).

**Theorem A** (`DivWCoreLac`, `DivWCoreLacUseType.lean:90-117`).

*Setting:* Γ is a compact group; K is algebraically closed of characteristic 0 with a Hausdorff ring topology (ℂ, or Q̄_ℓ in the application); ρ: Γ → GL_N(K) is continuous and completely reducible.

*Hypotheses:*
- (H1) There is a dense S ⊆ Γ and, for each s ∈ S, a monic P_s of degree n with P_s(ρ(s)) = 0. In words: ρ(s) has at most n distinct eigenvalues, and P_s is a padded list of them with no multiplicities.
- (H2) Some X ∈ Lie(G) ⊗ K' has n distinct eigenvalues e₁,…,e_n, and they are lacunary.
- (H3) ψ: Γ → K^× is a continuous character with ψ(s) = (−1)ⁿ P_s(0) on S.

*Conclusion:* there is a continuous, completely reducible r: Γ → GL_n(K) such that:
- (C1) r ↪ ρ: there is an intertwiner A of rank n (`:105-106`).
- (C2) ρ ↪ r^{⊕k}: there is B of rank N with (r(g)⊗1_k)B = Bρ(g) (`:107-109`).
- (C3) charpoly(r(g)) annihilates ρ(g) for every g (`:110`).
- (C4) P_s annihilates r(s) (`:111`).
- (C5) det r = ψ (`:112`).
- (C6) {g : r(g) has n distinct eigenvalues} is open and dense (`:113-114`).
- (C7) charpoly r(s) = P_s whenever r(s) is regular, or whenever P_s is product-generic (`ProdGen`, `:56-58`, `:115-117`).

**Plain-language form.** (C1), (C2) and (C6) together say: ρ ≅ ⊕_a V_a ⊗ ℂ^{m_a}, where the V_a are pairwise non-isomorphic, ∑ dim V_a = n, r ≅ ⊕V_a, and a generic group element has n *pairwise distinct* eigenvalues on ⊕V_a. The multiplicities m_a are not determined, and cannot be: ρ and ρ⊕ρ have identical unweighted spectra.

**How it is used in the application.** `divSet_of` (`ZCD/PDivSet.lean:16-48`) calls the theorem with:
- Γ = Gal(Ω/E) and K = Q̄_ℓ;
- S = the Frobenius-type elements admitting a suitable Q;
- X = the Sen operator, supplied by `SenWLac` (`CLD/StGalW.lean:26-31`);
- e = a lacunary subset of the Hodge–Tate jumps (`HTLac`, `StGalW.lean:17-24`).

`divOne_of` (`ZCD/PDivOne.lean:35-72`) then feeds in inverse Frobenii at split places, using Satake polynomials as P_s. It matches charpoly r(Frob) with the Satake polynomial on the regular locus (`:66-72`). This is the classical step "the cohomology contains the expected n-dimensional Galois rep, given only the Eichler–Shimura-type relation P_v(Frob_v) = 0."

### A.2 How the Lean proof works

`goal_holds` (`DC/GoalHolds.lean:19-20`) calls `goal_of` (`DC/Imports.lean:6-26`). That repackages `plus_of` (`DC/DivPlus.lean:37-69`) and builds B from families T_j, T'_j with ∑T'_jT_j = 1 (`Imports.lean:13-26`). Writing p = (p₁,…,p_n) for the spectral idempotents of X, `plus_of` runs these steps (statements in `DC/OpenCoset.lean` and `DC/CycleCount.lean`):

1. **Specialize X to K** (`SpecLie`, `OpenCoset.lean:90-92`; proof `DC/SpecLiePf.lean:7-64`). Lacunarity is a finite list of non-vanishing conditions and "eᵢ is a root of the charpoly" is polynomial. A Nullstellensatz specialization lemma (`DC/SpecPtPf.lean:5-24`) finds a K-point X₀ ∈ Lie(G) with lacunary eigenvalues e₀.
2. **At most n eigenvalues everywhere** (`DegAll`, `CycleCount.lean:70-72`; `TanDeg`, `OpenCoset.lean:127-128`). "Minimal polynomial of degree ≤ n" is a Zariski-closed condition. By density and continuity it holds on all of ρ(Γ), on G, and on Lie(G).
3. **Spectral idempotents** (`Proj`, `CycleCount.lean:6-8`; `DC/ProjPf.lean:56-100`). Since minpoly(X) = ∏(x−eᵢ), X = ∑eᵢpᵢ, where pᵢ = Lagrange basis polynomial evaluated at X, and these form a complete orthogonal system.
4. **Off-diagonal blocks stay in the Lie algebra** (`Grade`, `CycleCount.lean:10-12`; `DC/GradePf.lean:85-134`). Lie(G) is ad_X-stable, and pᵢYp_j is an ad_X-eigenvector with eigenvalue eᵢ−e_j. `lac_key` (`GradePf.lean:45-77`) shows eᵢ−e_j = e_k−e_l with i≠j forces (k,l) = (i,j). A polynomial in ad_X (`:113-134`) then projects Y onto pᵢYp_j, so pᵢYp_j ∈ Lie(G). **Only the B₂ ("Sidon") part of lacunarity is used here:** the calls `hL {i}{k,j}`, `hL {i,l}{k}` and `hL {i,l}{k,j}` all involve sets of size ≤ 2.
5. **Diagonal Lie elements are scalar on blocks** (`DiagScalar`, `DC/DiagScalar2.lean:59-120`). If Y ∈ Lie(G) commutes with all pᵢ, then Ypᵢ = cᵢpᵢ. Otherwise sY + X ∈ Lie(G) would have more than n eigenvalues for generic s, contradicting step 2. This uses only injectivity.
6. **One-dimensional corners** (`AlgStruct`, `DC/AlgStruct2.lean:128-132`; multiplicativity in `S_mul`, `:52-93`). In env = the associative algebra generated by Lie(G), pᵢ a pᵢ ∈ K·pᵢ.
7. **env is semisimple** (`Semis`, `DC/SemisPf.lean:51-132`). It is normalized by ρ(Γ) and preserves every invariant subspace; with ρ semisimple, its Jacobson radical acts as 0.
8. **Key step: handling the component group** (`Key`, `CycleCount.lean:51-55`; `DC/SumMulSum.lean:90-176`). Fix g ∈ Γ and an open normal subgroup U.
   - q = ρ(g)⁻¹pρ(g) is another corner system. `IdemConj` gives a unit v ∈ env and a permutation π with v p_j = q_{π j} v.
   - `UnitFactorization` writes v = u·diag(d), with u a product of elementary unipotents 1 + p_j a p_k. Each lies in the Zariski closure of ρ(U) by `Unip` + `TanIndex` + `ZclMul` (`SumMulSum.lean:75-88`).
   - So x = ρ(g)u permutes the pᵢ by π.
   - **`TorusPt`** (`OpenCoset.lean:130-132`; `DC/TorusPtPf.lean:66-109`) produces a "generic torus point" t = ∑τ_j p_j in the Zariski closure of ρ(U) satisfying `MulLac`: (∏_O τ)^{|O'|} ≠ b(∏_{O'} τ)^{|O|} for disjoint O, O' and b in a finite set B. The construction uses the formal exponential τ_j = exp(e_j T) ∈ K[[T]] (`ExpVan`, `OpenCoset.lean:119-122`) plus Nullstellensatz specialization. The key identity is `E_ne` (`TorusPtPf.lean:30-38`): exp(aT) − b·exp(cT) = 0 forces b = 1 and a = c. So the only obstruction is |O'|∑_O e = |O|∑_{O'} e, which is exactly what lacunarity forbids (`:86`).
   - **`GenSpec`** (`DC/GenSpecProof.lean:102-166`): on a π-cycle O, every eigenvalue l of y = x·t satisfies l^{|O|} = (∏_O τ)·β, where β is an eigenvalue of x^{|O|}. So `MulLac` keeps the eigenvalues of different cycles apart.
   - **`CycleCount`** (`DC/CycleCount2.lean:70-173`): each k-cycle contributes the k distinct k-th roots of β, so y has n distinct eigenvalues. Since y has at most n eigenvalues (step 2), y is scalar on each π-fixed pᵢ (`fixed_scalar`, `:175-259`).
   - Output: (a) every coset gU contains an element ρ(g)·m, with m in the Zariski closure of ρ(U), that has n distinct eigenvalues; (b) pᵢρ(g) = pᵢw with w ∈ env whenever the corner is nonzero.
9. **Bigger algebra with the same corners** (`BigCorner`, `DC/BigCorner2.lean:107-114`). R = span(env·ρ(Γ)) is an algebra containing ρ(Γ) with one-dimensional corners.
10. **Build r** (`MatrixUnits₂`, `Rep`, `FinSub`, `FinEmbed`). Matrix units give R ≅ ⊕M_{d_a}(K) with ∑d_a = n. Then r(g) = Bρ(g)A with BA = 1, and ρ ↪ r^{⊕k} (`DivPlus.lean:50-52`, `:68`).
11. **Regular elements are dense** (`DenseAlg`, `DC/DenseAlg2.lean:48-108`; `FinDense`, `DC/FinDensePf.lean:18-35`; `OpenCoset`, `DC/OpenCosetPf.lean:19-25`). The discriminant of r(g) is continuous, so the regular locus is open. If it vanished on an open set, it would vanish on a whole coset of an open normal subgroup (by Noetherian Zariski stabilization — no analyticity needed). That contradicts 8(a).
12. **Determinant and characteristic polynomials** (`FinPoly`, `DC/FinPolyPf.lean:33-47`; `DivPlus.lean:59-66`). det r = ψ holds on S ∩ (regular locus), hence everywhere by continuity. The `ProdGen` clause of (C7) follows from the determinant.

**Where lacunarity enters:** exactly twice. Step 4 uses only the B₂ part; step 8 (`TorusPt`) uses full lacunarity, against arbitrary cycle structures of π.

### A.3 Is this already a known theorem?

- **Brauer–Nesbitt + Chebotarev** do not apply: they need traces or characteristic polynomials. Here only minimal polynomials (unweighted eigenvalues) are known.
- **Boston–Lenstra–Ribet (1991)**: if a *given* irreducible 2-dimensional r satisfies charpoly(r(g))(ρ(g)) = 0 for all g, then ρ ≅ r^m. (C3) is exactly BLR's hypothesis and (C2) a weak form of BLR's conclusion. Theorem A is an n-dimensional version **in which r is constructed rather than given**, and the rigidity is supplied by a lacunary Sen-type operator. Higher-dimensional BLR fails without extra input; lacunarity is that input.
- **Serre's Frobenius tori / Larsen–Pink**: step 8 is a "Zariski-generic torus point" argument of exactly this kind. **Sen's theorem** supplies X.

So every ingredient is classical. As far as I know the combination — producing r, handling disconnected monodromy via lacunarity, working purely algebraically over Q̄_ℓ — is not a named standard theorem. In the Galois setting I rate it a genuinely useful, nontrivial lemma.

### A.4 Counterexamples

**Counterexample 1 (connected group, physical).** Two qubits, Γ = SU(2) acting by ρ(U) = U⊗U, so N = 4 and ρ = spin-1 ⊕ spin-0.
- If U has eigenvalues z^{±1}, then U⊗U has eigenvalues z², 1, 1, z⁻². That is at most 3 distinct values; P_s = (x−z²)(x−1)(x−z⁻²) and ψ ≡ 1.
- X = S_z^tot = σ_z⊗1 + 1⊗σ_z lies in Lie(G) with eigenvalues {2, 0, −2}, so n = 3. These are not lacunary ({0} versus {2,−2}), and not even Sidon (0+0 = 2+(−2)).
- The conclusion fails. A 3-dimensional r ↪ ρ must be the spin-1 part, and ρ ↪ (spin-1)^{⊕k} is impossible because of the singlet.

**Counterexample 2 (disconnected group: the Sidon condition is not enough).** Let Γ = U(1)³ ⋊ ℤ/3, with ℤ/3 cyclically permuting the coordinates, ω = e^{2πi/3}, and z = z₁z₂z₃. Let ρ = M ⊕ W_ω ⊕ W_{ω²} (N = 5), where:
- M = Ind(χ_{(3,0,0)}): the torus acts by diag(z₁³, z₂³, z₃³) and the generator c acts by the 3-cycle;
- W_ω: the torus acts by z and c acts by ω;
- W_{ω²}: the torus acts by z and c acts by ω².

Check the hypotheses with n = 4:
- On the identity coset the eigenvalues are {z₁³, z₂³, z₃³, z}: 4 distinct.
- On the cosets c and c², M has characteristic polynomial x³ − z³, so the eigenvalues are z·{1, ω, ω²}: 3 distinct.
- P_s = (x³ − z³)(x − zωʲ) on the coset cʲ, which makes ψ(t·cʲ) = z⁴ωʲ a continuous character.
- X = diag(3x₁, 3x₂, 3x₃, s, s) with s = x₁+x₂+x₃ and generic xᵢ ∈ iℝ.
- e = (3x₁, 3x₂, 3x₃, s) is **Sidon**: the only linear relation among these vectors, (1,1,1,−3), is not of 2-versus-2 type.
- e is **not lacunary**: {s} versus {3x₁, 3x₂, 3x₃} have the same mean.

The only 4-dimensional subreps are M⊕W_ω and M⊕W_{ω²}. Each has a repeated eigenvalue on *entire open cosets*: zω or zω² appears twice. So (C6) fails, and (C2) fails too, since ρ has three distinct constituents of total dimension 5 > 4. I checked this numerically (`/tmp/audit_scripts/cex.py`): over 2000 random group elements the maximum number of distinct eigenvalues is 4, the B₂ check passes, and each 4-dimensional subrep has 3 distinct eigenvalues on cosets 1 and 2.

Consequences:
- **`DivWCoreSidon` (`DivWCoreLacUseType.lean:60-84`) is false as stated.** It is only defined in the repo, never proved. Do not target it.
- The higher-order part of lacunarity (here a 1-versus-3 relation) is necessary for disconnected groups.

### A.5 Over ℂ: minimal hypotheses and what they force

- **Connected G: the Sidon (B₂) condition suffices.** For connected G over ℂ, env = span ρ(G) (exp(Y) is a polynomial in Y in a finite-dimensional algebra). So steps 4–6 already give one-dimensional corners for span ρ(G), and steps 8–9 are unnecessary. Generic regular elements come from exp(tX). This is my derivation from the module structure; it is not formalized.
- **Sidon is not necessary.** SU(2)×SU(2) on ℂ²⊗ℂ² has weights ±a ±b, violating Sidon, yet the conclusion holds (r = ρ).
- **No condition on the eigenvalue set of X alone can be both necessary and sufficient.** {−2, 0, 2} arises from spin-1 (conclusion true) and from spin-1⊕spin-0 (conclusion false).
- **Other hypotheses.** Continuity is used only in steps 2, 11 and 12. Complete reducibility is automatic for compact groups over ℂ.

**What Sidon forces for connected G (my derivation).**
- A non-minuscule irreducible has an α-string of length ≥ 3, i.e. a 3-term arithmetic progression μ−α, μ, μ+α, which violates Sidon.
- Every minuscule representation other than the standard rep of SU(m) or its dual has a 2-versus-2 relation: Sp/SO vector reps (±εᵢ), ∧^k for 2 ≤ k ≤ m−2, spin reps, E₆, E₇.
- Tensor products λᵢ⊗μ_j give (λ₁+μ₁)+(λ₂+μ₂) = (λ₁+μ₂)+(λ₂+μ₁).
- Two isotypic blocks on the same SU(m) factor give another 2-versus-2 relation.

Hence **ρ(G°) ⊆ ∏_a U(m_a)⊗1_{k_a}, acting by standard (or dual) reps, with ∑m_a = n.** Under these hypotheses, every lacunary (or merely Sidon) configuration over ℂ is a "universal block ⊗ gauge space" (noiseless-subsystem) structure.

### A.6 Honest CM/QI assessment

1. **Multiplicities are never recovered.** The suggested use — "exact irrep multiplicities from unweighted eigenvalues" — is impossible in principle, and the theorem does not claim it.
2. **X must be a generator in the dynamical Lie algebra (DLA), not a conserved charge.** If X is central (a conserved charge that also lies in the DLA), then n = number of sectors, and (H1) forces the group to act by scalars on each block. That case is trivial.
3. **Standard charges and local Hamiltonians are not even Sidon.** S_z^tot and N have equally spaced spectra (3-term progressions). Field terms ∑hᵢZᵢ have spectra ∑±hᵢ, which are full of 2-versus-2 relations. By A.5, lacunarity is incompatible with any nontrivial action on two tensor factors.
4. **When it applies, the conclusion is directly visible.** Diagonalize X and test pᵢρ(g)pᵢ ∈ ℂpᵢ. Commutant-algebra methods (Moudgalya–Motrunich) give the full decomposition, multiplicities included, by linear algebra.
5. **Best possible niche:** a spectral certificate that a symmetric-circuit DLA acts as ⊕u(m_a) on n logical levels, from unlabeled eigenphases. But (H2) already presupposes a DLA element whose degeneracies match the gauge structure.

**Verdict:** not a publishable CM/QI theorem. Over ℂ it is classical (weights + Clifford theory) and inapplicable to realistic charges. Its real value is ℓ-adic.

---

## Package B

### B.1 `PairBoundAbstract` (`HC/StatementPB.lean:171-179`; proof `HC/HermitianCurvatureProofs/GrowthOfBasic.lean:464-517`)

**Setting** (`StatementPB.lean:15-109`). Terms t carry an operator part op_t ∈ H and a vector part v_t ∈ H₁, plus a row label row(t) whose row-group is io(row t) ∈ I (finite). For S ⊆ τ:
- part(S) = ∑_{t∈S} op_t;
- a_i(S) = ∑_{t∈S, io(row t)=i} v_t;
- Φ(S) = Γ₁∑_i‖a_i(S)‖².

**Hypotheses:**
- (NE) ‖part(S)‖² = Re∑_{ij}G_{ij}⟨a_i, a_j⟩ (`:86-87`);
- (GG) G ⪯ P_gΓ₁·I (`:89-90`);
- (RowOrth) v_t ⊥ v_{t'} when they share a group but not a row (`:92-94`);
- part(id) = 0;
- four pair-sum bounds, ε, ε, A and ε' (`:101-109`).

**Conclusion:** ‖K₀‖² ≤ (√(P_g(A+2ε)) + √(P_g(ε+ε')))²·dd.

**Proof:**
- ‖part(S)‖² ≤ λ_max(G)·∑‖a_i‖² = P_g Φ(S) (`t_EqualIota`, `:602`, via cI−G = ∑vv*; `t_PriceOfIota`, `:384-392`).
- Φ(S) = Γ₁·∑ over same-row pairs of Re⟨v_t, v_{t'}⟩ (`t_PairSplit`, `:695`; RowOrth kills cross-row pairs). Split by s0 into ≥2, =1-scalar and =1-nonscalar, and use |Re| ≤ |·| (`t_SubFamily`, `:421-462`).
- Finish with the triangle inequality (`t_TextClosing`, `:367-382`).

**Audit.** GGBound *is* the upper frame bound. There is no Schur test, no Welch bound (Welch bounds coherence from *below*; irrelevant here), no randomness and no subspace overlap. **It is elementary bookkeeping.** All the real content sits in the hypotheses RowBig, RowMain, …, which come from number-theoretic lattice counting elsewhere (`LoopsJoint`, `StatementPB.lean:410-420`). `PairBound` (`:220-234`, proof `:525-550`) only adds numerical inequalities.

### B.2 `TheoremFSharp` (statement `HN/StatementFrameF.lean:64-99`; proof `HN/HarderNarasimhanProofs/TheoremFSharp.lean:168-386`)

**Stripped statement** (Hermitian lattices over a CM field; think "Euclidean lattices"). Let cc ⊂ W be the target lattice of rank D, Nᵢ ⊂ Vᵢ source lattices of rank dᵢ, and Bᵢ: Vᵢ → W maps with Bᵢ(Nᵢ) ⊆ cc and height ≤ hᵢ. μ is the normalized slope, μ = 2·slope + const (`FrameHermSharpB.lean:80-100`). Assume:
1. ∑dᵢ(μ(Nᵢ) − hᵢ) ≥ s∑dᵢ: the mean source slope, height-corrected, is ≥ s;
2. μ_max(Nᵢ) − hᵢ ≤ s + u for all i;
3. μ_min(cc) ≥ s − HH;
4. at one complex place, after padding the target by κ₁ coordinates (with (1−δ)·|κ⊕κ₁| ≤ |κ|):
   - near-isometries: ∑‖γᵢBᵢ*Bᵢ − I‖²_HS ≤ e∑dᵢ, with e ≤ 1/4;
   - near-tight frame: tr Q² ≤ (1+η)(tr Q)²/dim, where Q = ∑γᵢBᵢBᵢ*.

**Conclusion:** μ(cc) ≥ s − (1−δ)⁻¹·[4u·log(1 + HH/u) + (η + 4√e)·HH].

**How the proof works.** For each τ ≥ 0, let Ñᵢ(τ) be the Harder–Narasimhan (HN) step of Nᵢ at level s − τ + hᵢ.
- **Reverse Markov** (`thmF_share`, `TheoremFSharp.lean:11-33`; `frameB_share`, `FrameHermSharpB.lean:25-60`): if the mean is ≥ s and all values are ≤ s+u, then #{values < s−τ} ≤ R·u/(u+τ). So ∑codim Ñᵢ(τ) ≤ (u/(u+τ))·∑dᵢ (`:225-275`).
- **Slope inequality**: Bᵢ(Ñᵢ(τ)) lies in the HN step St(τ) of cc (`:280-300`, via `slope_inequality_mean`, `SlopeIneqMean.lean:249`).
- **Frame lemma `FrameLA1`** (`StatementFrameF.lean:11-24`; proof `FrameLinearAlgebraFirst.lean:77-221`). Write W⊥ for the orthogonal complement of ∑Bᵢ(Nᵢ), w = dim W⊥, t = tr Q, R = ∑dᵢ, and ε for the total relative codimension.
  - Lower bound: t ≥ R(1−√e) (`fam_bound`, `SumNormSqLeHilbertSchmidt.lean:87`).
  - Upper bound: tr(P_{W⊥}Q) = ∑γᵢ‖Bᵢ*g_l‖² ≤ εR + R√(εe), because Bᵢ*g_l ∈ Nᵢ⊥ (`W_upper`, `:164`).
  - Second lower bound: tr(P_{W⊥}Q) ≥ (t/D)·w − √w·‖Q − (t/D)I‖_HS (`sum_re_inner_bound`, `:69`).
  - Flatness: ‖Q − (t/D)I‖²_HS ≤ ηt²/D (`:187-219`).
  - Combining them (`final_real1`, `:15-64`) gives w ≤ (η + 4ε + 4√e)·D.
- **Layer cake** (`CS/StatementFR.lean:47-52`; `LayerCakeFormula.lean:57-97`): #{slopes of cc < s−τ} ≤ w(τ)·D for τ ∈ [0, HH] gives μ(cc) ≥ s − ∫₀^{HH} w (`:374-386`), and ∫ 4u/(u+τ) dτ = 4u·log(1+HH/u) (`frameB_integral`).

**Sharpness and originality.**
- **The "−log|I| removal" is trivial.** `TheoremF` (`StatementFrameF.lean:61`) merely carries an extra −log|I|, and `theoremF_of_sharp` (`TheoremFSharp.lean:390-398`) derives it *from* FSharp using log|I| ≥ 0. The current proof never generates the penalty; nothing about Bost's inequality has been sharpened.
- **Free improvements visible in the code:**
  1. `final_real1` actually proves w ≤ (η + 4ε + 4√(εe))·D; it throws this away at `:64` via √(εe) ≤ √e. Feeding the per-level ε_τ = u/(u+τ) into the layer cake replaces the (4√e)·HH term by 8√(eu)·(√(u+HH) − √u) ≤ 8√(e·u·HH). That is a real gain when HH ≫ u.
  2. Using ∫min(1, w) instead of ∫w (relaxed at `:383-386`) saves about (4 log 4 − 3)u ≈ 2.5u.
  3. In the exact case (η = e = 0) the truth is w ≤ εD, not 4εD.
- **Comparisons.**
  - The frame lemma is the second-moment (Chebyshev) version of the standard fusion-frame argument w ≤ ∑‖Bᵢ‖²·codim(Nᵢ)/λ_min(Q). That is folklore; the only extra feature is robustness to ηD bad directions.
  - Layer cake + level-wise counting is the same mechanism as Ky Fan / majorization counting bounds; nothing deep.
  - Fannes–Audenaert is unrelated.
  - Relative to Bost's slope inequality, FSharp is a sensible "robust, averaged, almost-surjective" variant of μ_min(target) ≥ min μ_min(source) − height.
- **CM/QI:** slopes need arithmetic lattices. The nearest physics object is GKP / lattice codes, where nobody uses HN slopes over number fields. Only `FrameLA1` transfers, as a modest lemma ("images of nearly-full subspaces under an approximately tight frame span nearly everything"). It is roughly as good as what a random-subspace argument gives, up to constants.

### B.3 `SharpRecursion` (statement `HC/Statement.lean:7-14`; proof `HC/HermitianCurvatureProofs/SharpRecursion.lean:157-172`)

**Statement.** Assume 0 ≤ a ≤ ½, ε ≥ 0, (r+1)(ε+a) ≤ 1, eᵢ, σᵢ ≥ 0, and
σᵢ ≤ (1+ε)·√(1+eᵢ)·σ_{i−1} + ∑_{t=2}^{i} a^{t−1}σ_{i−t}.
Then σ_{r+1}² ≤ (1 + 80(r+1)(ε+a))·∏(1+eᵢ)·σ₀².

**Proof:**
- By induction, σᵢ ≤ Pᵢρⁱσ₀ with Pᵢ = ∏√(1+e_l) and ρ = 1+ε+2a (`growth`, `:70-115`, using ∑a^{t−1} ≤ 2a from `geom_le`, `:8-29`).
- Then (1+ε+2a)^{r+1} ≤ e^{2x} with x = (r+1)(ε+a), and e^x ≤ 1+2x.
- Finally (1+2x)⁴ ≤ 1+80x on [0, 1] (`quart`, `:117-121`; `pow_bound`, `:123-149`).

**Audit.**
- The eᵢ drop out exactly: normalize σ̃ = σ/P. Memory terms only get smaller, so eᵢ = 0 is the worst case.
- The worst case is therefore the equality recursion with eᵢ = 0. Its growth rate is the renewal root ρ* = 1 + ε + a + O(a² + aε), not 1+ε+2a.
- **Optimal constant: C* = e² − 1 ≈ 6.389.** Numerically, sup over the admissible region of (σ²−1)/x: r = 1999 gives 6.385 (ε only) and 6.378 (a only), approaching e²−1 as r → ∞ with x = 1 (`/tmp/audit_scripts/rec*.py`). So 80 is about 12.5× too large; even the proof's own ρ = 1+ε+2a would give e⁴−1 ≈ 53.6.
- **The form 1 + C(r+1)(ε+a) is sharp** (it cannot be sublinear in r, since (1+ε)^{2(r+1)} ≥ 1 + 2(r+1)ε). But that is just e^{2x} linearized on x ≤ 1.
- **Versus discrete Grönwall / Volterra:** this is a textbook Grönwall estimate with a summable geometric kernel. RG / MERA / AGSP error-propagation arguments use exactly this. It is folklore, not new.

### B.4 `goodBadCut` (statement `Formalism/MeanHeightDescent/MuMaxMinkowski.lean:41-60`; proof `Formalism/MeanHeightDescent/AverageDegreeBounds/GoodBadCut.lean:383-457`; used in `slope_good_ge`, `Development/AbelianVarietyTheory/Proofs/DivisorProofs/MajAtAddRight.lean:111-142`)

The `Formalism.ExtensionFiltration` namespace lives in these `MeanHeightDescent` files.

**Statement.** Let Λ be a lattice and e an orthogonal (self-adjoint) projection with g·e(Λ) ⊆ Λ. Set Λ_g = Λ ∩ ran e and Λ_b = Λ ∩ ker e. Then:
- rk Λ = rk Λ_g + rk Λ_b;
- deg Λ ≤ deg Λ_g + deg Λ_b + rk(Λ_b)·log g (×2 in μ-normalization), i.e. covol Λ ≥ covol Λ_g · covol Λ_b · g^{−rk Λ_b};
- μ(Λ_b) ≤ μ_max(M) for every M ⊇ Λ.

**Proof:** a sandwich argument. covol Λ = covol Λ_g · covol((1−e)Λ), and Λ_b ⊆ (1−e)Λ ⊆ g⁻¹Λ_b. In the code, the image g(1−e)Λ sits inside Λ_b (`:393-413`) and the height of the map g(1−e) is at most g (`:415-428`).

`slope_good_ge` turns this into μ(Λ_g) ≥ μ(Λ) − 12δQ when rk Λ_b ≤ 3δ·rk Λ (`numeric`, `:93-109`). It first upgrades the Pythagoras hypothesis to self-adjointness by polarizing at a complex place (`selfAdj_of_pyth`, `:55-89`).

**Audit.**
- The continuous analogue is Fischer's inequality, det G ≤ det G₁₁·det G₂₂ (subadditivity of Gaussian entropy).
- The lattice statement goes the *other* way, with an integrality penalty coming entirely from the index [(1−e)Λ : Λ_b] ≤ g^{rk}.
- It is standard geometry of numbers. There is no gentle-measurement or Rényi / entanglement-spectrum content, because "g·e(Λ) ⊆ Λ" has no Hilbert-space counterpart.

---

## Final ranking for CM/QI

1. **Only real mathematical content:** `DivWCoreLac`, and only in its native ℓ-adic setting. Its lacunarity hypothesis is genuinely necessary there (Counterexample 2), and the repo's `DivWCoreSidon` is false. For CM/QI it is either classical or inapplicable.
2. **Small usable lemma:** `FrameLA1` inside `TheoremFSharp`. Its constants can be tightened as described above; the arithmetic wrapper has no QI counterpart.
3. **Elementary or folklore:**
   - `SharpRecursion`: Grönwall; replace 80 by e²−1.
   - `PairBoundAbstract`: frame bound plus triangle inequality.
   - `goodBadCut`: covolume sandwich.

None of the four Package B items is stronger, cleaner or newer than what CM/QI researchers already use.
