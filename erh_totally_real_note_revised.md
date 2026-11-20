# Extending the Dirichlet GRH argument to totally real and CM fields

## 1. The conjecture and the scope of the argument

Let $F$ be totally real or CM. The target is that every zero of $\zeta_F$ in $0<\Re s<1$ lies on $\Re s=1/2$. The original proposal also asks for finite-order Hecke characters with totally real or CM splitting fields and for the corresponding Artin factors. These remain targets. Brauer induction gives meromorphic identities. Deducing a critical-line statement for Artin factors requires tracking poles as well as zeros in the region under discussion. For CM $F$, the identity $\zeta_F=\zeta_{F^+}L_{F^+}(\chi_{F/F^+})$ leaves a quadratic Hecke factor to treat. The discriminant-$229$ case admits a more explicit analysis below. [Original proposal](erh_totally_real_note.md) · [Cubic case and proofs](cubic_229.md)

The field-theoretic restriction on a CM host is genuine. Every subfield of a CM field is totally real or CM. The assertion about algebraic Hecke characters in the original scope discussion needs a qualification. Descent of the infinity type leaves a possible finite-order twist. An ideal-class character already has trivial infinity type and can carry all its information in that twist. The cubic example realizes precisely this possibility. [Patrikis, *Variations on a theorem of Tate*, Lemma 2.3.4](https://arxiv.org/abs/1207.6724)

## 2. The archived argument

The source declares a result about Dirichlet $L$-functions. Its arithmetic construction chooses a cyclotomic CM host, an imaginary quadratic field $K=\mathbb Q(\sqrt{-d})$, a growing real $2$-power cyclotomic layer, and auxiliary quadratic characters. The slope argument compares a weighted inert-prime divisibility sum $\mathrm{ASK}$ with an archimedean main term. For weights of size $b$, the quotient $a/b$ probes the target scale $x$. Smaller weights probe $y\ge X'/3$ with $X'=\exp(x^{\varepsilon/3})$. A finite Fourier identity isolates four thick terms. The argument also needs suitable pairs $(q,d)$, bounds for arithmetic cohomology on the moving host, and a positive-oscillation theorem on windows. The discussion here uses the declarations and their hypotheses. [Main declaration](lean/src/Main.lean) · [Weighted balance](lean/src/Formalism/SizeWindowBrackets/FirstPrimeNeSecondPrime.lean#L68) · [Thin scales](lean/src/Formalism/SizeWindowBrackets/GrowthBoundGivesRiemannHypothesis.lean#L55)

## 3. The proposed extension, step by step

### Step 1. Constructing the CM host

Write $L_0$ for the totally real Galois closure of $F$, $\Gamma=\operatorname{Gal}(L_0/\mathbb Q)$, and $H=\operatorname{Gal}(L_0/F)$. For the auxiliary signs used by the source, set
$$
 B_e=\mathbb Q(\zeta_{2^{e+2}})^+,\qquad
 M=B_e(\sqrt{-q},\sqrt{-d}),\qquad E=L_0M .
$$
In the archived parameter range $q\equiv3\pmod8$, the character $(\cdot/q)$ belongs to $\mathbb Q(\sqrt{-q})$. Complex conjugation reverses both imaginary square roots. The real compositum in $E$ is $E^+=L_0B_e(\sqrt{qd})$ when these quadratic signs are independent. The CM type can still be pulled back from $K$. [Identification of the auxiliary character](lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/HostFacts.lean#L197) · [Prime congruences](lean/src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean#L27)

**Correction to the direct product.** Put $D=L_0\cap M$. Restriction identifies $\operatorname{Gal}(E/\mathbb Q)$ with pairs in $\Gamma\times\operatorname{Gal}(M/\mathbb Q)$ agreeing on $D$. A direct product follows when $D=\mathbb Q$. If $L_0=\mathbb Q(\sqrt2)$, every nontrivial layer of the real cyclotomic $2$-tower contains $L_0$. Passing higher in that tower cannot produce a linearly disjoint layer. For the discriminant-$229$ cubic, disjointness does hold when $229\nmid 2qd$, as proved in the companion note.

**Arithmetic hypotheses.** The source's host includes an embedding into a cyclotomic field and a surjective homomorphism from residue-class units to its Galois group. Either condition forces that group to be abelian. Replacing a single splitting lemma by Chebotarev leaves these hypotheses to reconstruct. The absolute density of complete splitting is $1/[E:\mathbb Q]$. In the direct-product case $1/|\Gamma|$ is the relative density among primes already split in $M$. Uniform height bounds for a prime, when needed, require quantitative estimates. A factorization of the relative different into coprime conjugate ideals also requires checking the ramification of $E/K$ at each new prime, including dyadic primes. [Host data](lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ConjEMemHostFIff.lean#L33) · [Surjectivity and Frobenius hypotheses](lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/ConjEMemHostFIff.lean#L87)

### Step 2. Selecting the thick embeddings

Use the coordinate convention of the thick-average module. There $E_0=(\mathbb Z/2)^2$, the CM type has first coordinate zero, and a thick place has $E_0$-coordinate $(0,1)$. In the direct-product case the corrected proposed selector is
$$
 g_0=(0,1),\qquad a-u_A\in T_2,\qquad \gamma\in uHu^{-1}.
$$
The original selector included both $(0,0)$ and $(0,1)$. Its Fourier coefficient at the second sign vanishes, already over $\mathbb Q$. Keeping $(0,1)$ restores the four sign coefficients. The partner map adds complex conjugation, so the selected Frobenius sign is $(1,0)$. Its indicator is $(1-\chi_{-d})(1+\chi_{-q})/4$. Thus the product character in the fourth term corresponds to $\mathbb Q(\sqrt{qd})$. [CM type, conjugation, and thick places](lean/src/Formalism/ThickAverageLoss/PartnersToFactorsAt.lean#L20) · [Four-term signal](lean/src/Formalism/ThickAverageLoss/PartnersToFactorsAt.lean#L92)

**Exact permutation identity.** Let $V=\mathbb C[\Gamma/H]$, $d_F=[F:\mathbb Q]$, and $\pi_F=\operatorname{tr}_V$. Each coset fixed by $g$ has $|H|$ representatives $u$ with $u^{-1}gu\in H$. Hence
$$
 \frac{1}{|\Gamma|}\sum_u\mathbf1_{uHu^{-1}}(g)=\frac{\pi_F(g)}{d_F}.
$$
At an unramified prime, multiplication by $\log p$ recovers the Dedekind von Mangoldt coefficient from $\pi_F(g^j)$. At **every** prime, with inertia $I$ and any Frobenius lift $g$, the exact formula is
$$
 \frac{\Lambda_F(p^j)}{\log p}
 =\operatorname{tr}(g^j\mid V^I)
 =\frac1{|I|}\sum_{h\in I}\pi_F(g^j h).
$$
Indeed the average over $I$ projects onto $V^I$. The Frobenius cycles on the inertia orbits have lengths equal to the residue degrees of the primes of $F$ over $p$. For the source's kernel $x/n-1$, a raw local sum with bounded coefficients $a_j$ is $x\sum_{j\ge1}a_j/p^j+O_p(\sup_j|a_j|\log(2x))$. Retaining the Euler factor or compensating its linear term is essential to the claimed logarithmic error. [Source inertia average and centered sum](lean/src/Formalism/SizeWindowBrackets/FirstPrimeNeSecondPrime.lean#L61)

**Geometric input still needed.** For $H=\langle(12)\rangle$ in $S_3$, one fixed selector distinguishes $(12)$ and $(13)$. A rational prime specifies only their conjugacy class. One must either realize the weights at a chosen place and establish compatible averaging, or construct a class-invariant selector directly. Irreducible character orthogonality applies to the class average. The vanishing of the sum of an irreducible character over the kernel of a quadratic character follows by taking subgroup invariants, but turning it into cancellation of analytic constants requires the balance identity with the correct local and linear terms. The source's pointwise slope implication assumes divisibility, counting, height, slope, and loss estimates for the chosen data. Repeating a density calculation does not establish these inputs. [Pointwise implication](lean/src/Formalism/SizeWindowBrackets/QuotientSlopeBoundsWith.lean#L72)

### Step 3. Thin scales and Brauer induction

For a fixed $\Gamma$, Brauer induction expresses each Artin logarithmic derivative as an integral linear combination of Hecke logarithmic derivatives over fixed intermediate fields. One can use this on a common zero-free region. If a rational twist of conductor $m$ is pulled back to $F_j$, the norm of its conductor can grow as $m^{[F_j:\mathbb Q]}$. The degree enters the logarithmic estimates. The archive's exceptional-zero exclusion, `RealBox`, quantifies over real **Dirichlet** characters of the host. Proving the requisite exclusions or bounds for the new Hecke factors is a separate step. For the $S_3$ cubic every nonabelian constituent is induced from an order-three character over one real quadratic field. Its rational twists remain non-real as Hecke characters. This proves the needed thin-scale decay for that constituent. [Definition of RealBox](lean/src/Development/AutomorphicArithmetic/CharacterBoxes/PairGood.lean#L32) · [Cubic thin-scale estimate](cubic_229.md#the-nonabelian-thin-scale-estimate)

### Step 4. Selecting good quadratic twists

At unramified primes the twisted coefficients are $\Lambda_F(p^j)\eta(p)^j$, and $0\le\Lambda_F(p^j)\le d_F\log p$ also holds at ramified primes by the inertia formula. This gives bounded weights for a finite large-sieve sum. The proposed $O(Q^{1/4})$ exceptional set, its height, the simultaneous choices for $q,d,qd$, and the resulting uniform bound on thick scales require a family estimate with those parameters. The archived counting theorem quantifies over primitive Dirichlet characters. The theorem of Kowalski and Michel concerns specified families of cuspidal representations of $\mathrm{GL}_n/\mathbb Q$ with explicit hypotheses and height dependence. Degree alone does not give the exponents asserted in the proposal. [Lean exceptional-set theorem](lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/CountBadCore.lean#L18) · [Kowalski–Michel](https://msp.org/pjm/2002/207-2/pjm-v207-n2-p08-p.pdf)

### Step 5. The Selmer bound on a moving field

The required estimate sums $\ell$-adic Selmer lengths over $\ell$ and $1\le j<x^{401}$, with budget $\exp(x^\varepsilon/2)$. Away from the relevant group orders one can choose a finite splitting coefficient DVR and compare integral summands, with lengths normalized after extending coefficients. Shapiro and induction reduce which Selmer groups need estimates. One still needs upper bounds for those groups. Projecting to auxiliary characters at primes dividing the auxiliary group order also needs a separate integral argument. At fixed bad $\ell$, the ground field $E$ varies with $q,d,e$. A fixed-tower Iwasawa estimate supplies no uniform bound on its invariants across these fields.

In Lean, `VAt` applies the bound to fields satisfying `IsChiField`, which includes an embedding into a cyclotomic field. The cited `KatoUse` input takes a newform and a representation of $G_{\mathbb Q}$. A realization of Galois representations over totally real fields would supply only part of the requested Selmer estimate. This remains an arithmetic problem even for the cubic. [Field hypothesis and bound](lean/src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean#L19) · [Kato input](lean/src/Development/AutomorphicArithmetic/AutomorphicVarieties/UnitaryThreeGroups/KatoUse.lean#L13)

### Step 6. Turning windows into a zero-free half-plane

The source's window statement starts from a zero of a retained Dirichlet factor and forces a positive excursion of the centered prime sum in every sufficiently large multiplicative window. Its quantifiers matter. For $\zeta_F$, one needs this oscillation statement with the Dedekind Euler factors, pole subtraction, and window lengths of the proposed argument. Nonnegativity of $\Lambda_F$ and a zero-counting estimate do not on their own furnish that deduction. For the cubic, the companion note proves positivity of a different, explicit Mellin kernel and gives a finite-height zero count. The all-height window and slope estimates remain open in this argument. [Window definitions](lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/Window.lean#L24) · [Discriminant-229 results](cubic_229.md)
