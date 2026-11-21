#set document(title: "When fusion charge decides whether an anyon cloud is normalizable")
#set page(paper: "us-letter", margin: (x: 0.88in, top: 0.78in, bottom: 0.78in),
  numbering: "1", number-align: right)
#set text(font: "Libertinus Serif", size: 11pt)
#set par(justify: true, leading: 0.59em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(below: 0.62em)[#text(size: 19pt, weight: "bold")[#it.body]]
#show heading.where(level: 2): it => block(above: 0.83em, below: 0.3em)[#text(size: 13pt, weight: "bold")[#it.body]]
#let alg = link("https://arxiv.org/abs/math/0611412")[Li, Thms. 1.2 and 1.3]
#let wzw = link("https://arxiv.org/abs/2112.07195")[Gu, Haghighat and Liu, §4]
#let sewing = link("https://doi.org/10.2969/aspm/01910459")[Tsuchiya, Ueno and Yamada, §6]
#let vac = $bold(1)$

#text(size: 10pt, weight: "bold")[Structural Atlas · Engine 12]

= When fusion charge decides whether an anyon cloud is normalizable

Six identical Fibonacci anyons in a Gaussian trap can have two different short-distance thresholds, depending on what they fuse to. For the trial states below, the critical couplings are $13/75$ for vacuum charge and $1/5$ for charge $tau$. Between them, every proper subset has an integrable collision. Bringing all six together makes the vacuum-sector norm infinite. The $tau$ sector still defines a probability distribution, and its cloud radius has an exactly calculable law.

== Which anyon model?

Use the spin-one primary $tau$ in the integer-spin sector of the unitary $upright("SU")(2)_3$ Wess–Zumino–Witten model. Its primary weights and fusion rules are
$ h_#vac = 0, quad h_tau = 2/5, quad tau times tau = #vac + tau, quad #vac times c = c. $
Place $N>=2$ copies at $z_i in CC$, fix their total charge $b$, and insert its conjugate at infinity. Write $cal(F)_b$ for the collection of primary chiral blocks, using a positive braid-invariant Hermitian norm on the fusion labels and summing over external spin components, including at infinity. Use the diagonal sum of squared norms in a unitary fusion basis, so every allowed channel has positive weight. Fix the block normalization independently of the coupling. [#wzw; #sewing]

Choose a length $ell>0$ and a real coupling $alpha$. The joint position density before normalization is
$ exp(-sum_i abs(z_i)^2/(2ell^2)) norm(cal(F)_b(z))^2
  product_(i<j) abs((z_i-z_j)/ell)^(-2alpha) product_i d^2 z_i. $
Call its integral $Z_(N,b) (alpha)$. The scalar power comes from a holomorphic factor with exchange phase $exp(-i pi alpha)$ for a positive exchange. It retains the Fibonacci braid action on the internal space. Positive $alpha$ increases the weight of close particles. This choice of radial branch, the Gaussian, and the choice of blocks specify the trial ensemble. Finite $Z$ means a normalizable state or ensemble. A dynamical collapse or stability claim for a material would require a Hamiltonian and contact boundary conditions.

== Where engine 12 enters

Apply characteristic-zero principalization to the product of the collision ideals, all defined over $QQ$. On the resulting smooth space, the different rates at which groups of particles coincide can be read in separate coordinates. Each such rate carries a fusion label. Integrability then reduces to inequalities on these labelled coordinates, including constraints on which labels can occur together. The next page identifies the precise input to the engine and the resolution on which we compute its orders.

#pagebreak()
= Principalizing the collision ideals

Remove common translation, so $X=bb(A)^(N-1)$ with coordinates $z_i-z_1$ for $2<=i<=N$. For a subset $C$ with $m=abs(C)>=2$, let $Delta_C$ be its coincidence diagonal and $I_C=(z_i-z_j : i,j in C)$. Take $J=product_C I_C$ on $X$, with empty initial boundary. Here $X$ is smooth affine and $J$ is nonzero on its unique irreducible component, as witnessed by any configuration of distinct points. These are inputs to #raw("FunctorialResolution.functorialPrincipalizationCharZero") in the repository. Its field-extension property permits base change from $QQ$ to $CC$.

*Why its output supports the calculation.* On a principalization $Y$ of $J$, locally $J cal(O)_Y=(g)$ with $g$ nonzero. For each $C$, the fractional ideal $g^(-1) product_(D!=C) I_D cal(O)_Y$ inverts $I_C cal(O)_Y$. The blowup universal property therefore gives a simultaneous map from $Y$ to all $upright("Bl")_(Delta_C) X$. On the dense collision-free open set these maps agree with its natural embedding. Since $Y$ is reduced, the map factors through its closure in the product over $X$. This closure is the wonderful model $W$ of the diagonal arrangement. Thus the engine’s output maps to the explicit model on which we read the orders. [#alg]

Construct $W$ by blowing up the transforms of the diagonals in decreasing order of cardinality, retaining the pair diagonals as divisors. Its boundary divisors $E_C$ meet precisely in collections of nested or disjoint clusters. Near such a stratum each $E_C$ has its own coordinate $s_C=0$. For $V=product_(i<j)(z_i-z_j)$, the relevant orders at a generic point of $E_C$ are
$ upright("ord")_(E_C) V = binom(m,2), quad
  upright("ord")_(E_C) "Jac" = m-2. $
The first counts the pairs vanishing to first order. The second is the blowup Jacobian for a center of complex codimension $m-1$. The same orders hold in a corner, where the pullbacks are products of the corresponding coordinate powers times units. More generally, $I_D$ has order one there along $E_C$ exactly when $D subset.eq C$.

*Fusion supplies the third exponent.* In a sewing basis adapted to a nested collision tree, the chiral block contributes $s_C^(h_c-m h_tau)$ when $C$ fuses to $c$. Scaling the whole cluster scales all its leaves, hence the $m h_tau$ even for nested clusters. Descendants add nonnegative powers. Factorization gives bounded coefficients on compact shape charts and a nonzero primary coefficient on an open set for each allowed tree. At a binary tree this coefficient is a composition of nonzero primary spin intertwiners, with all external spin components retained. [#sewing]

Writing $r_C=abs(s_C)$, the radial density in that channel has factor
$ r_C^(2nu(m,c)-1) d r_C, quad
  nu(m,c) = m-1 + h_c - (2m)/5 - alpha binom(m,2). $
Consequently $Z$ is finite exactly when $nu(m,c)>0$ for every cluster and label that extends to the specified total charge, including $(N,b)$. Necessity follows on a positive-weight open set of shapes. Sufficiency follows by integrating the independent coordinates on normal-crossings charts. The unit sphere of relative shapes is compact and the Gaussian controls the remaining radial tail. This argument also handles disjoint collisions at distinct positions.

#pagebreak()
= A charge-selective interval for every $N>=6$

The vanishing condition $nu(m,c)=0$ for each charge gives
$ t_m^#vac = (6m-10)/(5m(m-1)), quad t_m^tau = 6/(5m). $
The first divergence occurs at the least of the $t_m^c$ allowed in the total sector. One can check extendibility by fusing $c$ with the possible charges of the complementary $N-m$ particles. The empty complement carries vacuum.

*Minimizing over all proper clusters.* The vacuum values for $m=2,3,4,5$ are $1/5,4/15,7/30,1/5$. They decrease from $m=3$ onward, and $t_m^tau>t_m^#vac$. For $N>=6$, the smallest proper-cluster value before imposing a total label is thus $min(1/5,t_(N-1)^#vac)$. Both entries are at least $t_N^tau$, since
$ t_(N-1)^#vac - t_N^tau = (2(N-6))/(5N(N-1)(N-2)). $
The full cluster itself always reaches $t_N^b$. It follows that
$ alpha_(c) (N,#vac) = (6N-10)/(5N(N-1)), quad alpha_(c) (N,tau) = 6/(5N). $
Throughout the open interval between them only the full vacuum cluster fails integrability. The width is $4/(5N(N-1))$. For $N>6$ the first divergence in each sector comes from a single full-cluster divisor. The upper endpoint for $N=6$ also has critical subclusters.

== A position observable

Let $R^2=sum_i abs(z_i-z_"cm")^2$, where $z_"cm"$ is the center of mass. The center-of-mass Gaussian factors out. On relative space the block is homogeneous of degree $h_b-N h_tau$ under positive dilations by primary covariance. Independently, the Knizhnik–Zamolodchikov dilation operator is $(bold(S)_"tot"^2 - 2N)/5$ on spin-one tensors. Its eigenvalues for six particles are $-12/5$ and $-2$, respectively. Separating $R$ from angles in $2(N-1)$ real dimensions gives
$ p(R) d R prop R^(2nu(N,b)-1) exp(-R^2/(2ell^2)) d R. $
The angular integral is finite in a normalizable sector by the proper-cluster test. Substituting $x=R^2/(2ell^2)$ gives a gamma distribution of unit rate and shape $nu(N,b)$, and $⟨R^2⟩=2ell^2 nu(N,b)$.

At the midpoint of the two thresholds, for every $N>=6$,
$ nu(N,tau)=1/5, quad nu(N,#vac)=-1/5. $
The surviving ensemble therefore has $⟨R^2⟩=(2ell^2)/5$. Its entire scaled radius distribution is the same for all these $N$. In the vacuum sector the norm integral with a lower cutoff $R>epsilon ell$ grows as $epsilon^(-2/5)$ as $epsilon$ tends to zero. At the lower threshold itself, that divergence is logarithmic. For six particles the midpoint is $alpha=14/75$, giving one concrete parameter choice for testing both laws. The cutoff here is on collective radius.

#pagebreak()
= When fusion removes a divergence

For five particles of vacuum total charge, set $delta=1/5-alpha>0$. The critical divisors at $delta=0$ are a pair in vacuum and the full five in vacuum. Geometrically, two disjoint pairs and the full cluster share a corner. In translation-reduced coordinates an explicit chart is
$ (z_1,z_2,z_3,z_4,z_5) = (0,r s,r,r(1+t),r u) $
with $u$ away from 0 and 1. The holomorphic Jacobian is $plus.minus r^3$. The pair product $V$ is $r^10 s t$ times a unit near $s=t=0$. Thus the three scale variables really are independent. For a critical pair, the margin is $delta$, and for the full cluster it is $10delta$.

Each critical scale contributes a factor of order $1/delta$, from integrating a power with exponent tending to $-1$. But two vacuum pairs leave one $tau$, and $#vac times #vac times tau = tau$. The coefficient with both pairs in vacuum vanishes identically in the chosen total sector. One vacuum pair and the full vacuum cluster can coexist because the remaining three $tau$ can fuse to vacuum. Their leading coefficient is nonzero on an open set. Positivity yields the lower bound there, while the compatible-tree expansion on finitely many shape charts gives the upper bound. Hence
$ Z_(5,#vac) (alpha) = Theta((1/5-alpha)^(-2)) quad (alpha arrow.t 1/5). $
Here $Theta$ means bounded above and below by positive constants times the indicated power. Counting intersecting geometric divisors without fusion would allow a third inverse power.

== Reproducing the calculation

The accompanying Python program uses exact fractions. For the divergence order at $alpha_c$ it maximizes, over compatible binary splits, the sum of both children’s orders plus one if the current vertex is critical. Every nested forest admits a binary refinement. In a unitary sewing basis each nonzero channel gives its own lower bound and the full positive sum gives the same upper order. The output includes the following cases.

#align(center)[#table(columns: 5, align: center, stroke: none, inset: (x: 12pt,y: 3pt),
table.hline(), [$N$], [$alpha_(c) (N,#vac)$], [Order], [$alpha_(c) (N,tau)$], [Order], table.hline(),
[3],[4/15],[1],[1/5],[1], [4],[1/5],[2],[1/5],[1], [5],[1/5],[2],[1/5],[2],
[6],[13/75],[1],[1/5],[3], [7],[16/105],[1],[6/35],[1], table.hline())]

#raw("python3 fibonacci_collision.py") checks the results against direct enumeration of all ordered fusion trees through $N=8$, contracts the five-spin tensors with two singlet-pair projectors, verifies both six-spin dilation eigenvalues directly on all 729 components of representative tensors, and integrates the radial law numerically. #raw("python3 fibonacci_collision.py --witness 5 1") prints a tree realizing order two. These checks concern the derived trial ensemble. The repository’s Lean theorem supplies the algebraic principalization step. The WZW sewing and the physical conclusions here are mathematical arguments outside Lean.

#pagebreak()
= A braid switches on a pair collision

The inclusive sum over all blocks is braid invariant. To see the effect of a particular braid, prepare a fusion state and use the same collision coordinates to read it out. Take three $tau$ anyons of total charge $tau$. Prepare particles 1 and 2 in their $tau$ channel. Compare two preparations, one with no winding and one with particle 2 taken once around particle 3 and returned to its initial position.

Set $alpha=1/5$. Keep the spectator and the pair center in a bounded bin away from other collisions. Integrate the trial-state weight over $epsilon < r < r_0$, where $r=abs(z_1-z_2)/ell$, in a fixed angular sector and branch. All preparations use the same Gaussian, detector and block normalization. Denote this local, unnormalized contact weight by $W(epsilon)$. The resolved exponent gives
$ nu(2,#vac)=0, quad nu(2,tau)=2/5. $
Thus a pure vacuum pair contributes $A log(1/epsilon)+O(1)$ to the detector for some $A>0$, whereas the prepared $tau$ pair gives a finite limit. In any superposition, the coefficient of the logarithm is $A$ times the squared modulus of its vacuum amplitude. The mixed term is integrable since its radial exponent is $-1+2/5$.

== The coefficient of the logarithm

Let $phi=(1+sqrt(5))/2$. In the unitary basis labelled by the charge of particles 1 and 2, take the standard recoupling and exchange matrices (up to basis phases)
$ F = mat(phi^(-1), phi^(-1/2); phi^(-1/2), -phi^(-1)), quad
  R = upright("diag")(e^(-4pi i/5),e^(3pi i/5)). $
The full winding is $U=F R^2 F$ up to the common scalar phase of the Abelian dressing. Its probability of converting the prepared pair to vacuum is
$ abs(U_(#vac,tau))^2 = phi^(-3) abs(e^(-8pi i/5)-e^(6pi i/5))^2
  = 4phi^(-3) sin^2 ((2pi)/5) = 3phi - 4. $
These matrices are the Fibonacci braid and recoupling data in a common ordering of channels. [#wzw, Eqs. 90 and 102–104]

The contact weight following the winding is therefore
$ W_"wound" (epsilon) = (3phi-4) A log(1/epsilon) + O(1). $
The winding turns a finite contact weight into a logarithm with *85.4102%* of the coefficient of a vacuum-pair control. The control removes the dependence on the trap length, the spectator bin, and the block amplitude. The ratio compares unnormalized weights at a common preparation normalization. Renormalizing the entire position distribution separately for each cutoff would define a different observable.
