# The cubic of discriminant 229 and three tests of the slope argument

For $F=\mathbb Q[x]/(x^3-4x-1)$ put $A=\zeta_F/\zeta$. Write $k=\mathbb Q(\sqrt{229})$ and $L$ for the normal closure of $F$. Then $A=L_k(s,\xi)$ for an unramified ideal-class character of order three. This note gives a local divisibility calculation, a good-prime-pair theorem for the three auxiliary twists, and a finite classification of real cubic kernels. The twist proof uses the specified rational prime-progression estimates from the source as mathematical inputs. The new good-pair argument is a paper proof. The finite orbit identities and the two prime examples were checked independently with Lean 4.34.0. This work uses the declarations in the 4.33.1 archive without rebuilding it. [Field and normalization](cubic_229.md) · [Standalone Lean orbit check](CubicOrbitTest.lean) · [Reproducible kernel survey](check_cubic_kernel_family.py)

## 1. Where the cubic enters the divisibility inequality

**A pair of primes.** Use the fixed test host
$$
 M=\mathbb Q(\zeta_{16})^+(\sqrt{-3},\sqrt{-71}),\qquad B_0=kM,\qquad E=LM.
$$
The primes $97$ and $193$ are both $1\bmod 16$ and $1\bmod 3$. Both are quadratic nonresidues modulo $71$ and quadratic residues modulo $229$. Thus they have identical Frobenius in $B_0$, have the signal sign for $\mathbb Q(\sqrt{-71})$, and have period two there. The cubic has no root modulo $97$ and has the three roots $42,157,187$ modulo $193$. The period in $E$ is consequently six at $97$ and two at $193$. This is a test at a fixed auxiliary level. [Lean checks of the roots and abelian characters](CubicOrbitTest.lean) · [Archive signal orbit length](lean/src/Formalism/FrobeniusOrbits/HostOrbitCountSg.lean#L7)

**What the proven valuation bound reads.** At a source position $s$ in the top set, let $H_s$ be its first Young-diagram row length minus its second. Lean's local contribution is
$$
 \sum_{\substack{e\ge1\text{ odd}\\e\ne d_{\rm top}(s)}}
 [H_s/p^e-\operatorname{cap}(s+e)]_+,\qquad [u]_+=\max(u,0).
$$
The capacity is taken at the individual position $s+e$ *before* summing. For a signal orbit, an odd step from a top has the opposite sign bit, so $d_{\rm top}(s)=\infty$. The local jet inequality is valid for an admissible even period, including $3r$ when $r$ is even. It has additional terms involving the weights, $W_c$, and a loss linear in the period. The following calculation identifies the displayed contribution. It gives no automatic improvement of the full lower bound when one changes the weights. [Capacity and local term](lean/src/Formalism/SharpRestriction/Divisibility/ProductZerothFirstParts.lean#L157) · [Coefficient valuation bound](lean/src/Formalism/SharpRestriction/Divisibility/JetPolynomialLogs/LocalBoundElevenComparison.lean#L64) · [Identification with the geometric partner in the old host](lean/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/OrbitValuationBounds/SummableTruncatedGeometric.lean#L167)

Take an old signal top on sheet $0$ in the three-element fiber over $B_0$. Mark the destinations with the corrected old thick predicate **and** sheet $0$. At an exponent eligible under the old predicate, let $P_e=[H_s/p^e-b]_+$ and $Q_e=[H_s/p^e-b']_+$ be the evaluations of the thick and thin capacities. At $193$ the contribution is $P_e$. At $97$ it is
$$
 Q_e+\mathbf1_{3\mid e}(P_e-Q_e).
$$
The marked odd exponents at $97$ are $3,9,15,\ldots$. For a general old orbit of length $r$ prime to three, the new position of an old partner $i$ occurs at $i,i+r,i+2r$ modulo $3r$. Exactly one of them has the prescribed sheet. Eligibility in the old coordinates must still be imposed. These statements concern the cubic fiber over the split-in-$k$ branch. The full regular $S_3$ selector also requires the quadratic sign to be trivial.

**Both ends must be marked.** More generally let $T,S$ be the selected source and destination sheets. If the unmarked data agree on the sheets, the coefficient of $P_e-Q_e$ in the sum over sources is $|T\cap\gamma^{-e}S|$. With $T=S=\{0\}$ this detects the order-three return. With $T$ the entire fiber and $S=\{0\}$ the coefficient is one for every $e$, for split and nonsplit Frobenius alike. With one thick and two thin destinations the sum over all three equal sources is $P_e+2Q_e$ in both cases. This rules out the construction that pulls back every source and changes only the destination weights. [Machine-checked finite identity](CubicOrbitTest.lean)

**A check inside the local logarithm.** The source's actual letter logarithm at position $0$ has terms $p^{-m}X_{-2m\bmod d}^{p^{2m}}$. Set every coordinate except $X_0=X$ to zero. At period two the resulting series is $\sum_{m\ge0}X^{p^{2m}}/p^m$. At period six it is $\sum_{j\ge0}X^{p^{6j}}/p^{3j}$. Thus the coefficient of $X^{p^2}$ in $p$ times the specialized logarithm is $1$ at period two and $0$ at period six. The three-cycle is visible already in this formal series. [Jet logarithm and its allowed periods](lean/src/Formalism/LocalRingCardinality/DataJet.lean#L12)

**The remaining arithmetic issue can be tested term by term.** The abstract marked calculation needs a geometric theta expansion with the selected source diagrams, destination capacities, and the local admissibility conditions. The present host interface maps a partner to a sign bit and an element of the old abelian translation group. Both primes give the same partner coordinates there. There is also an explicit obstruction to simply inserting an old expansion on one sheet. For even period $r$, condition B2 requires every nonzero monomial with multiplicities $m_i$ to satisfy
$$
 p^r-1\ \mid\ \sum_{i=0}^{r-1}(-1)^i p^i m_i.
$$
At period $3r$ the modulus becomes $p^{3r}-1$. For example, $X_0^{p^r-1+p}X_1$ passes the old congruence and fails the new one. This counterexample concerns B2 itself. Copying the monomial multiplicatively around the three blocks instead multiplies its signed weight by $1+p^r+p^{2r}$ and restores the congruence, but does not distinguish the blocks. A genuine marked theta construction must reconcile these two requirements and verify the remaining conditions B0, B1, B3, and B4. I have traced the distinction through the local inequality and logarithm. Realization by the arithmetic theta family over $E$ remains open. [Torus action B2](lean/src/Formalism/SharpRestriction/Divisibility/ProductZerothFirstParts.lean#L40) · [Local admissibility](lean/src/Formalism/PeriodIntegrals/UnitaryGroupMassFormula/OrbitValuationBounds/AdmissibleOfJetBounds.lean#L13) · [Existing host partner](lean/src/Formalism/SharpRestriction/InertJacobiLevels/TiesCore.lean#L63)

## 2. One good pair for all three twists

**Theorem using the archived prime-progression estimates.** Fix $0<\varepsilon<1/52$, $a\ge1$, and a finite set of fixed Dirichlet characters $\eta_0$ (primitive representatives). For every sufficiently large $Y$, set $z=Y^{\varepsilon/5}$ and $z'=z(\log Y)^2$. There exist primes
$$
 e^{z/2}<q\le e^z,\ q\equiv3\pmod 8,\qquad
 e^{z'/2}<d\le e^{z'},\ d\equiv7\pmod {16},
$$
with $d\equiv-1\pmod q$ and $d\equiv-1\pmod p$ for every odd prime $p\le z$. Write $\chi_l(n)=(n/l)$. For every $\eta_0$ in the fixed set and each $\eta=\chi_q,\chi_d,\chi_q\chi_d$, let $P=L(s,V\otimes\eta_0\eta)$ be the primitive twist of the standard cubic Artin representation. Uniformly for $Y\le y\le Y^a$,
$$
 |G_P(y)|\le y^{1/2+\varepsilon/2},\qquad
 |P'(1)/P(1)|\le4\log y,
$$
in the centered normalization $G_P(y)=\sum_{n\le y} b_P(n)(y/n-1)+yP'(1)/P(1)$, where $-P'/P(s)=\sum b_P(n)n^{-s}$. In addition, the same pair may be chosen from the good Dirichlet rows of the archive for any one fixed modulus. Thus this supplies the nonabelian contribution on the **thick** scales for the discriminant-$229$ field. All thresholds may depend on $a,\varepsilon$ and the fixed characters. [Archived simultaneous Dirichlet rows](lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/PairShare.lean#L26)

**The two rational inputs.** At the first stage put $U=e^z$ and take the primes in $(\sqrt U,U]$ congruent to $3\bmod 8$. At the second take $U=e^{z'}$ and fix a first-stage $q$. The prescribed congruences on the new prime form one reduced class modulo $m_0=16q\prod_{2<p\le z}p$. Denote the appropriate prime set by $\mathcal P$. The source gives $|\mathcal P|\ge U^{9/10}$ and, for every fixed $K'\ge1$, $Z=Y^{400K'}$, the estimate
$$
 \sum_{l\in\mathcal P}\left|
 \sum_{n\le Z}\Lambda(n)\min(1,y/n)\,\kappa(n)\chi_l(n)
 \right|^2\ll y\log y\,|\mathcal P|,\quad Y\le y\le Y^{K'},\quad |\kappa(n)|\le1.
$$
The maximal-exception lemma in the source turns this into an $o(1)$ exceptional fraction for the supremum with threshold $y^{1/2+\tau}/2$, for every fixed $\tau>0$. The bounds are uniform in $q$ and in bounded coefficient sequences, including sequences chosen after $q$ is fixed. The hypotheses on the modulus hold because $\log m_0\le\log16+(1+\log4)z<4z$ for large $Y$, and each of its prime factors is at most $z$ or exceeds $Z$. At the first stage the modulus is $8$. Enlarging the fixed power $K'$ changes only the lower threshold on $Y$. [Progression size](lean/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/MSqCount.lean#L346) · [Mean-square estimate](lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/meanSqK.lean#L51) · [Maximal exceptional fraction](lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/BadShare.lean#L251) · [Modulus bound](lean/src/Development/AutomorphicArithmetic/MeanSquareBounds/LogOddM.lean#L9)

**Exceptional zeros for the moving factors.** Take $\delta=10^{-9}$. Each $P$ is a primitive finite-order Hecke $L$-function on $k$. Write $M$ for a fixed common multiple of the original conductors and $229$. At the first stage take $T=8MU$, and at the second take $T=8Me^zU$. In both cases $T\le U^{3/2}$ for sufficiently large $Y$, and the analytic conductor is $\ll_M U^3$, by the norm-conductor bound on the quadratic base. Thorner–Zaman's Theorem 1.2 for $n=1$ over $k$ bounds the number of characters with a zero in $\Re s>1-\delta$, $|\Im s|\le 2T$, by
$$
 \ll_M (U^3(2T)^2)^{10^7\delta}\ll_M U^{0.06}.
$$
For each fixed base twist and fixed first-stage prime at the second stage, different moving primes give different characters. At each prime of $k$ over the new prime, the unramified local extension of $\mathbb Q_l$ has a surjective norm on residue-field units, so the pulled-back quadratic character ramifies there. All other varying prime factors have been fixed. A union over the bounded number of base twists preserves a negligible exceptional fraction in each progression. [Thorner–Zaman, Theorem 1.2](https://arxiv.org/pdf/1906.07717)

**A short-polynomial approximation with the narrower box.** Choose $K'\ge a$ large enough that $400K'\delta/2>a+5$. Set $Z=Y^{400K'}$ and take $Y$ sufficiently large that $2Y^a<Z$. Use the cutoff
$$
 \phi(u)=2(1-u)_+-(1-2u)_+.
$$
It equals one through $u=1/2$, vanishes from $u=1$ onwards and takes values in $[0,1]$. Its Mellin transform is $(2-2^{-s})/[s(1+s)]$. For a factor with the preceding zero-free box,
$$
 -P'(1)/P(1)=\sum_{n\le Z}\frac{b_P(n)}{n}\phi(n/Z)+O(Y^{-a-1}).
$$
Indeed integrate $-(P'/P)(1+s)Z^s\widehat\phi(s)$ on $\Re s=1/\log Z$ and truncate at $T$. Absolute convergence and $|b_P(n)|\le2\Lambda(n)$ bound the omitted tails by $O((\log Z)/T)$. Shift to $\Re s=-\delta/2$, picking up the residue at zero. In this strip for $|\Im s|\le T$, the fixed-degree local logarithmic derivative formula gives $|P'/P(1+s)|\ll_\delta \log^2(\mathcal Q(2T+4)^2)$, where $\mathcal Q$ is the analytic conductor at height zero. The nearby zeros lie at distance at least $\delta/2$, by the larger box. The vertical integral is $O_\delta(Z^{-\delta/2}\log^2(\mathcal QT))$ and the horizontal integrals are $O_\delta(\log^2(\mathcal QT)/T^2)$. Here $\log(\mathcal QT)\ll Y$ and $T$ grows faster than every fixed power of $Y$. The choice of $K'$ gives the claimed error. [Hecke explicit formula and local zero bounds](https://msp.org/ant/2017/11-5/ant-v11-n5-p04-p.pdf)

**Putting the estimates on the same pair.** For a fixed base factor $P_0$ at either stage and fresh prime $l$, one has $b_P(n)=b_{P_0}(n)\chi_l(n)$ at all prime powers. At $l$ both sides vanish because the old representation is unramified and the twist is ramified. Substitution of the approximation yields
$$
 G_P(y)=-\sum_{n\le Z} b_{P_0}(n)\,\chi_l(n)\phi(n/Z)\min(1,y/n)+O(Y^{-1}).
$$
Thus $\kappa(n)=b_{P_0}(n)\phi(n/Z)/(2\Lambda(n))$, set to zero off prime powers, is a permissible fixed sequence. Use $\tau=\varepsilon/4$ in the maximal estimate. The factor of two and the approximation error are absorbed into $y^{1/2+\varepsilon/2}$. The defining identity for $G_P(y)$ then gives $|P'(1)/P(1)|\le |G_P(y)|/y+2\sum_{n\le y}\Lambda(n)/n\le 2\log y+O(1)$. Intersect the density-one first-stage sets for the fixed characters. For each surviving $q$, intersect the second-stage sets for $P_0=V\otimes\eta_0$ and $P_0=V\otimes\eta_0\chi_q$ for every $\eta_0$. The source's Dirichlet good rows have arbitrarily large relative share at both stages, so they can be imposed at the same time. This proves the theorem. If a bound for a product of a fixed number of factors is desired, use a smaller target exponent in the maximal estimate to absorb their number.

The cubic boxes here have fixed width $10^{-9}$, and the longer cutoff pays for that choice. The width $1/400$ in the Dirichlet `RealBox` remains available for its Dirichlet factors. The non-real Hecke factors use the separate thin-scale estimate. The theorem concerns a fixed background modulus, with the three specified moving twists. [Cubic thin-scale result](cubic_229.md#the-nonabelian-thin-scale-estimate) · [Source box definitions](lean/src/Development/AutomorphicArithmetic/CharacterBoxes/PairGood.lean#L12)

## 3. A certified classification of cubic kernels

**Theorem.** There are 366 totally real $S_3$ cubic fields $F$ of field discriminant $D\le10{,}000$, up to isomorphism. For 360 of them the Bessel kernel of $A_F=\zeta_F/\zeta$ is everywhere positive. For the other six it changes sign. For **all 366** one has
$$
 A_F(\sigma)>0\quad(\sigma>0),\qquad
 \zeta_F(\sigma)<0\quad(0<\sigma<1).
$$
Each bound on a transcendental quantity in the classification was checked with Arb ball arithmetic. The conclusion about the real interval concerns every point in it. [Executable certificate](check_cubic_kernel_family.py)

| First successful certificate or witness | Fields | Smallest field discriminant |
|---|---:|---:|
| Leading Bessel term dominates the negative terms by the exponential bound | 42 | 148 |
| Positivity of $P_F$ inside the Bessel integral | 309 more | 316 |
| Direct interval bounds on the integrated Bessel sum | 9 more | 2857 |
| Negative at $x=1$, positive for large $x$ | 6 | 1489 |

The six sign-changing discriminants are **1489, 4729, 5521, 7249, 8884, and 9364**. For instance the first field is defined by $x^3-4x^2-5x+1$. The categories in the table describe successive sufficient tests. The final sign classification is exhaustive.

### What small splitting patterns can prove

Write $A_F(s)=\sum a_n n^{-s}$ and $c_D=2\pi/\sqrt D$. Every local factor comes from a two-dimensional finite-image representation on inertia invariants, so $|a_n|\le d(n)\le n$. With $K_0$ the modified Bessel function, put
$$
 B_F(x)=\sum_{n\ge1} a_n K_0(c_Dnx),\qquad P_F(u)=\sum_{n\ge1}a_nu^{n-1}.
$$
The standard Artin factor is entire, has conductor $D$, and at both real gamma factors has even parity. Its completed functional equation has sign $+1$, from the quotient of the two completed Dedekind zeta functions. [Cubic Artin factors, Proposition 3.1](https://link.springer.com/article/10.1007/s00222-025-01373-6)

The Mellin transform and reflection give $B_F(x)=x^{-1}B_F(1/x)$. In particular it suffices to study $x\ge1$. For $t=c_Dx$ the Bessel integral gives
$$
 B_F(x)=\int_0^\infty e^{-t\cosh v}P_F(e^{-t\cosh v})\,dv .
$$
Positivity of $P_F$ on $[0,e^{-c_D}]$ is a sufficient test. At discriminant $316$ the negative relative mass in the old exponential domination test already exceeds one using only the first sixteen coefficients and $r=7/10<e^{-c_D}$. The full $P_F$ is positive on the required interval. At discriminant $2857$, the certificate gives $P_F(5/6)<-1/5$ with $5/6<e^{-c_D}$, and $B_F$ is still positive everywhere. Integration restores positivity in this example. [Mellin normalization and reflection proof](cubic_229.md#a-positive-kernel-and-real-axis-nonvanishing) · [Bessel integral](https://dlmf.nist.gov/10.32.E9)

**A five-prime sufficient condition.** For $D\le10{,}000$, suppose $2,3,5,7,11$ are unramified and have respective Frobenius classes
$$
 (\mathrm{identity},\ \mathrm{transposition},\ \text{three-cycle},\ \mathrm{transposition},\ \mathrm{transposition}).
$$
Then $B_F$ is everywhere positive for *any* behavior at the remaining primes. Discriminant $9281$ realizes the pattern. To verify the implication, write $n=hm$ with $h$ supported on these five primes and $m$ coprime to them. Compute $a_h$ from their Euler factors. For $m=1$ use $a_h$ itself, and for $m>1$ use the coefficient lower bound $-|a_h|d(m)$. The resulting polynomial through $n=320$, with the full worst-case tail subtracted, is strictly positive throughout $[0,47/50]$ by interval subdivision. This interval contains $[0,\exp(-2\pi/100)]$. The same test takes other specified local patterns as input. [Calculation in the checker](check_cubic_kernel_family.py)

### How the signs and the real-axis theorem were certified

For $N=320$ and $0\le u<1$, a tail bound used throughout is
$$
 R_N(u)=u^N\left(\frac{N+1}{1-u}+\frac{u}{(1-u)^2}\right).
$$
It bounds $\sum_{n>N}|a_n|u^{n-1}$. The first test sums the negative coefficients in absolute value against $e^{-c_D(n-1)}$ and uses $K_0(nt)\le e^{-(n-1)t}K_0(t)$. The second encloses the truncated $P_F$ by interval Horner evaluation and uses $R_N$ on each subinterval. For the remaining fields the third test splits the Bessel sum into positive and negative terms. On $[l,r]$ it evaluates the positive terms at $r$, the negative terms at $l$, and bounds all omitted negative terms at $l$ using $K_0(c_Dl)R_N(e^{-c_Dl})$. The code allows a shorter cutoff and uses the corresponding tail with that cutoff. Evaluation at a point with an upper enclosure below zero proves a negative witness. Once $c_Dx\ge3/2$ all fields pass the uniform leading-term test since $\sum_{n\ge2}n e^{-(n-1)3/2}<1$.

For each of the six witnesses, the certificate also proves **positive tail integrals**
$$
 H_F(a)=\int_a^\infty B_F(x)\,\frac{dx}{\sqrt x}>0\qquad(a\ge1).
$$
Above a dyadic endpoint $U$ this follows from the uniform large-$x$ test. Below $U$ we start with the lower bound zero at $U$, retain the strict positivity of the discarded infinite tail, and work back to $1$. If $m$ bounds $B_F$ below on a cell $[l,r]$, the entire cell adds at least $2m(\sqrt r-\sqrt l)$. The worst partial-cell loss is at most $2\max(0,-m)(\sqrt r-\sqrt l)$. Both checks are made for every cell. The six fields required mesh widths $1/2,1/8,1/4,1/4,1/2,1/2$, respectively, in the order listed above.

Set $D_F(v)=e^{v/2}B_F(e^v)$ and $J(v)=H_F(e^v)$. Then $D_F$ is even and $J'=-D_F$ on $v\ge0$. For real $z$, integration by parts yields
$$
 \frac{\Lambda_{A_F}(1/2+z)}{8}
 =\int_0^\infty D_F(v)\cosh(zv)\,dv
 =J(0)+\int_0^\infty J(v)\,z\sinh(zv)\,dv>0 .
$$
The boundary term at infinity vanishes by double-exponential decay. This proves the assertion for the six signed kernels as well as for the 360 positive ones. The gamma factors are positive at real $\sigma>0$, and the alternating series for $\zeta(\sigma)$ gives the claimed sign of $\zeta_F$ on $(0,1)$. In this range of discriminants, tail positivity is strictly more widely applicable than pointwise kernel positivity.

**A consequence for every Taylor order.** For all 366 fields, including the six with sign changes, define
$$
 b_j=\frac{\Lambda_{A_F}^{(2j+2)}(1/2)}{8(2j+2)},\qquad j\ge0.
$$
Differentiating the integral above and putting $u=v^2$ gives
$$
 b_j=\int_0^\infty J(v)v^{2j+1}\,dv
     =\tfrac12\int_0^\infty u^j J(\sqrt u)\,du .
$$
Thus the $b_j$ are the moments of a strictly positive density on $(0,\infty)$. In particular every even central derivative is positive, including order zero. Both Hankel matrices $(b_{i+j})_{0\le i,j\le h}$ and $(b_{i+j+1})_{0\le i,j\le h}$ have strictly positive determinants for every $h$. Indeed their quadratic forms integrate the square of a polynomial against this density or against $u$ times this density.

### Completeness and reproduction

Run `sage -python check_cubic_kernel_family.py`. The program obtains candidate fields with PARI's `nflist` and independently checks coverage by a trace-lattice search. The orthogonal projection of $\mathcal O_F\subset\mathbb R^3$ onto the plane perpendicular to $(1,1,1)$ has covolume $\sqrt{D/3}$, since $1$ is primitive in $\mathcal O_F$. The two-dimensional Hermite bound gives a nonzero projected vector of squared norm at most $2\sqrt D/3$. Lift it to $\alpha$ of trace $t\in\{0,1\}$ by translating by an integer and, if necessary, changing sign. This nonrational element generates the cubic. Its polynomial $X^3-tX^2+sX-n$ satisfies
$$
 (t^2-\sqrt D)/3\le s\le0,\qquad
 |n|^2\le ((2\sqrt D+1)/9)^3 .
$$
The first bound follows from the sum of squares of the embeddings and the second from the arithmetic-geometric mean inequality for their squares. The program enumerates this covering set of monic cubics, computes field discriminants, and checks isomorphisms, including pairwise distinctness within each listed discriminant. All $366\cdot320=117{,}120$ Dirichlet coefficients are also checked a second way. For every $p\le320$ the local series is $(1-T)\prod_{\mathfrak p\mid p}(1-T^{f_\mathfrak p})^{-1}$. This uses the actual residue degrees and covers ramified and index primes. [PARI number-field routines](https://pari.math.u-bordeaux.fr/dochtml/html-stable/General_number_fields.html) · [Code](check_cubic_kernel_family.py)

The local arithmetic and good-pair arguments concern the discriminant-$229$ slope program. The finite family theorem concerns the completed Artin factors on the real axis. The all-height cubic critical-line question still requires the arithmetic realization of the marked jets, the moving-field Selmer estimate, and the corresponding global slope and window arguments.
