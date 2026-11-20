**There is an exact local theorem on the four-punctured sphere.** At equal parabolic weight differences \(1/2\), bundle Verschiebung is a degree-\(p\) morphism of \(\mathbb P^1\) with empty base locus. On the same pointed curve, the dormant \(\mathrm{PGL}_2\)-oper scheme with local exponent differences \(1/2\) has equation
\[
\boxed{\quad c^{(p-1)/2}=H_p(E'),\qquad
H_p(E')=[x^{p-1}](x^3-2)^{(p-1)/2}.\quad}
\]
This gives the entire finite scheme, including its nilpotents and the Frobenius action on its geometric points. Comparing it with the corresponding oper scheme for \(y^2=x^3-8\) detects **every three-cycle prime** through a cubic character. At \(p=19\), the two schemes even have the same Frobenius orbit sizes, while the comparison still detects the three-cycle.

There is also an upgrade of the Round 2 jet theorem. At the rational branch point of the coarse parabolic moduli line, the \(N\)-jet of the induced formal map has exact denominator **\(d_{2N}\)**. In particular, \(7\) first appears in coarse degree \(4\). Its Archimedean raw derivatives still attain coefficient \(1\) in front of \(N\log N\).

The four-marked torus gives a different answer. Its moduli space has dimension **four**. I obtain a genus-three equivariant Quot model, an explicit Frobenius pullback, equations for the destabilized locus, and finite-prime computations for dormant opers. The distinction between the sphere and the torus comes from the genera of their **parabolic double covers**, respectively one and three.

## 1. The two integral models and their Verlinde spaces

Write \(R=\mathbb Z[1/6]\). I use trivial determinant for the underlying rank-two bundle and a full flag at each of the four marks. The weight \(a/k\) means the **difference** of the two flag weights, with integrable \(\mathfrak{sl}_2\) label \(a\) at level \(k\). I take the weight at the distinguished mark to be the same as at the other three for the explicit half-weight models. Changing that fourth weight can change the answer.

### The sphere

At four equal differences \(1/2\), there is an isomorphism over \(R\)
\[
\mathcal M_0 \simeq \operatorname{Pic}^0(E')/\{\pm1\}
                 \simeq \mathbb P^1_R.
\]
The coordinate in the last presentation is the Weierstrass \(x\)-coordinate. Its four strictly semistable points are \(\infty\) and \(x^3=2\). In particular \(x=0\) is a rational stable coarse point.

Here is the construction that also identifies the Frobenius map. Normalize the flag weights to \((0,1/2)\) and tensor the underlying bundle by \(\mathcal O(-\infty)\), so the parabolic degree is zero. The order-two root stack of the branch divisor is \([E'/\{\pm1\}]\). The corresponding bundle upstairs has ordinary trivial determinant, equivariant determinant the sign character, and one \(+\) and one \(-\) eigenline at each ramification point. Its polystable representatives are
\[
L\oplus[-1]^*L,\qquad L\in\operatorname{Pic}^0(E'),
\]
with the involution exchanging the summands. At \(L^2=\mathcal O\) the mixed inertia selects the two opposite linearizations. Forgetting equivariance gives the ordinary elliptic fixed-determinant moduli line. The exchange construction gives its inverse on coarse moduli. Both constructions descend over \(R\). This uses the parabolic/root-stack equivalence and the elliptic description by the Jordan–Hölder line factors. [Borne, *Fibrés paraboliques et champ des racines*](https://arxiv.org/abs/math/0604458) · [Oprea, elliptic moduli and the Abel–Jacobi presentation](https://mathweb.ucsd.edu/~doprea/verlinde.pdf)

There is another explicit model away from the central wall. For four equal \(0<a/k<1/2\), semistability forces the underlying bundle on \(\mathbb P^1\) to be trivial. A positive-degree summand would destabilize even if it contained no flag. A negative-degree line cannot destabilize even if it contains all four. Thus the coarse space is the quotient of four flag lines by \(\mathrm{PGL}_2\), with equal linearization. Over the splitting ring this is the bracket cross-ratio line. Over \(R\) the last three factors are the Weil restriction from \(Y\). The bracket relation gives a descended projective line of a rank-two module, which is free over \(R\). At the central wall a fourth strictly semistable point appears. This matters when choosing a point for jets.

### The torus

For four full flags the stable dimension is \(3(g-1)+4=4\) at \(g=1\). The three-dimensional problem arises with three full flags, or after removing a flag by a central boundary weight.

At the half-weights there is an explicit double cover over \(R\):
\[
 C:\ W^4=X^3 Z-2Z^4,\qquad
 \pi:C\longrightarrow E',\qquad (x,w)\longmapsto(x,w^2).
\]
It is a smooth plane quartic of genus three. Indeed \(\operatorname{div}(y)=Y-3O\) on \(E'\), so the branch divisor is exactly \(O+Y\). Write \(\iota(w)=-w\). After the same normalization, now tensoring by \(\mathcal O_{E'}(-O)\), the coarse model is the S-equivalence quotient of semistable rank-two bundles \(W_C\) on \(C\) with

- an \(\iota\)-linearization,
- ordinary determinant \(\mathcal O_C\) with sign linearization,
- mixed inertia \(+\oplus-\) at the four ramification points.

This gives a finite Quot presentation if desired. Use the plane polarization and equivariant quotients
\[
\mathcal O_C(-2)\otimes(R^6_+\oplus R^6_-)\twoheadrightarrow W_C,
\qquad P_{W_C}(t)=8t-4.
\]
Take the semistable locally free locus with the specified determinant, inertia, and induced framing of \(H^0(W_C(2))\), and quotient by change of the two frames. The twist has slope \(8>2g(C)-1\), hence is generated and has vanishing \(H^1\). Its two eigenspaces each have dimension six, by descent and Riemann–Roch. Ordinary semistability upstairs suffices because a destabilizing maximal subbundle is unique and therefore equivariant. Keeping the linearization in this presentation matters. A fixed coarse point in the unmarked genus-three moduli space forgets that information. [Borne–Vistoli, parabolic sheaves and root stacks](https://arxiv.org/abs/1001.0466)

### Exact ranks and the proposed \(S_3\)-action

Let \(N_a\) be the level-\(k\) fusion matrix indexed by \(0\le i,j\le k\), with
\[
(N_a)_{ij}=
\mathbf1_{\{|i-j|\le a\le\min(i+j,\,2k-i-j),\ i+j+a\ {\rm even}\}}.
\]
For labels \((b,a,a,a)\), the characteristic-zero ranks are
\[
\dim V_{0;k}=(N_bN_a^3)_{00},\qquad
\dim V_{1;k}=\operatorname{tr}(N_bN_a^3).
\]
In particular, four equal labels on the sphere give \(\min(a,k-a)+1\). At half-weights write \(k=2m,\ a=m,\ n=m+1\). Then
\[
\boxed{\dim V_{0;2m}=n,\qquad
       \dim V_{1;2m}=\frac{n^4+2n^2}{3}.}
\]
On the sphere the polarization is \(\mathcal O(m)\). On the torus the trace reduces to \(\sum_{j=0}^{n-1}\csc^4(\pi(j+1/2)/n)\). The first five positive-level torus ranks are \(8,33,96,225,456\), also checked by integer fusion-matrix multiplication. The fourth-power growth independently detects the missing dimension. [Laszlo–Sorger, parabolic determinant lines and conformal blocks](https://numdam.org/item/ASENS_1997_4_30_4_499_0/)

**The arithmetic \(S_3\) in the question does not supply a linear \(\rho_2\)-isotypic component of \(V_k/\mathbb Q\).** On \(V_k\otimes L_0\) it supplies semilinear descent. In a descended basis this acts on the coefficients. The fixed rational space has trivial action. If one restricts scalars on the *whole* \(L_0\)-space, the normal basis theorem gives \(d\) copies of the regular representation, hence \(2d\) copies of \(\rho_2\) for \(d=\dim V_k\). This multiplicity is already present for an arbitrary rational vector space of dimension \(d\).

There is a concrete geometric check. An automorphism of the pointed sphere fixing \(\infty\) is affine. Preserving the three roots forces its translation to vanish and its multiplier to lie in \(\mu_3\). The origin-preserving automorphisms of \(E'_{\overline{\mathbb Q}}\) likewise induce only \(C_3\) on the three nonzero two-torsion points. A transposition of the labels consequently requires some additional identification or transport.

One can see exactly where a large *auxiliary* \(\rho_2\) does occur. On the split small-weight flag quotient, actively permute three flag factors. The two-dimensional bracket space is the standard \(S_3\)-module, and the degree-\(a\) section space is its symmetric power. If \(t_a=1,-1,0\) according as \(a=0,1,2\bmod3\), the standard multiplicity is
\[
\frac{a+1-t_a}{3}.
\]
This calculation uses an active permutation on a split flag model. It does not turn arithmetic descent, or an anyon braid, into that operator on the given rational fiber.

## 2. Bundle Verschiebung

On the sphere, relative Frobenius pullback acts on the parameter \(L\) by
\[
F_{E'/\mathbb F_p}^*:\operatorname{Pic}^0(E'^{(p)})
 \longrightarrow\operatorname{Pic}^0(E').
\]
Under the principal polarization this is elliptic Verschiebung. Thus its quotient \(R_p\) is characterized over \(\mathbb F_p\) by
\[
 x([p]P)=R_p(x(P)^p),\qquad \deg R_p=p.
\]
It is defined everywhere. Every bundle in the exchange construction pulls back to another semistable bundle. In the ordinary case \(R_p\) is separable. For the supersingular primes \(p\equiv2\bmod3\), elliptic Frobenius has trace zero, so \(F^2=[-p]\) and \(R_p(x)=x^p\).

The degree-\(p^2\) map in the wildcard is real. It is the quotient of \([p]=V\circ F\), and it occurs as a **Higgs–de Rham flow** for a specified family of parabolic Higgs bundles. Applying that theorem to relative pullback of the bundles above would introduce an extra factor of \(p\) in the degree and in the polarization. [Lam–Litt, Theorem 1.11 and §4](https://www.cambridge.org/core/journals/compositio-mathematica/article/geometric-local-systems-on-the-projective-line-minus-four-points/DED411AC50E97203F716C173585DC1FD)

Here are finite-field checks. I computed \(R_p\) from the elliptic division polynomials, canceled the common factors, and extracted the polynomial \(p\)-th roots in numerator and denominator. The tangent multiplier is in the parameter \(1/x\) at \(\infty\).

| \(p\) | Roots of \(x^3-2\) | \(H_p(E')\) | \((\deg\mathrm{num},\deg\mathrm{den})\) of \(R_p\) | \(R_p(1)\) | Tangent multiplier |
|---:|---|---:|---:|---:|---:|
| 7 | none | 1 | \((7,6)\) | 1 | 1 |
| 11 | 7 | 0 | \((11,0)\) | 1 | 0 |
| 13 | none | 8 | \((13,12)\) | 7 | 12 |
| 19 | none | 12 | \((19,18)\) | 15 | 11 |
| 23 | 16 | 0 | \((23,0)\) | 1 | 0 |
| 31 | 4, 7, 20 | 4 | \((31,30)\) | 1 | 16 |
| 43 | 20, 32, 34 | 8 | \((43,42)\) | 26 | 21 |

For example,
\[
 R_7(x)=\frac{x^7+4x^4+6x}{x^6+2x^3+1}\pmod7.
\]
The last column is \(H_p(E')^2\), because \(1/x\) has order two upstairs. In particular \(p=13\) and \(43\) even have the same integer representative for \(H_p\), despite opposite cubic splitting behavior.

If \(R_p=A/B\) in degree-\(p\) homogeneous coordinates, its action on central theta sections is exactly
\[
 H^0(\mathcal O(m))\longrightarrow H^0(\mathcal O(pm)),
 \qquad s\longmapsto s(A,B).
\]
It has rank \(m+1\) in every good characteristic. Consequently any integral lift of this coefficient matrix has a maximal minor that is a \(p\)-adic unit. **All its nonzero Smith factors are units**, at three-cycle primes as well as identity primes. This is a quantitative obstruction to extracting a common divisibility factor from the full section pullback.

### What changes on the torus and at other weights

On the torus the same operation is \(W_C\mapsto F_C^*W_C\) on the equivariant genus-three model. There is also an explicit formula downstairs. Let \(B\) be the original trivial-determinant bundle, let \(m_p=(p-1)/2\), and start with \(F^*B((1-p)O)\). At each mark with local parameter \(t\) and adapted frame whose first vector spans the flag, replace the first pulled-back generator by
\[
 t^{-m_p}F^*e_1
\]
and keep the second generator. The new first generator gives the new flag. Changing the lift of the original flag changes the pulled-back generator by a multiple of \(t^p\), so this prescription is intrinsic. The determinant is trivial since \(O+Y\sim4O\). This computes the rational moduli map wherever the result is semistable. It also explains the level multiplication: each positive elementary modification contributes the flag line to determinant of cohomology. For the level-two line with four label-one factors the exponent on each dual flag becomes \(2m_p+1=p\), and the fixed-determinant level becomes \(2p\), up to a constant line from the base.

One explicit surface in the fourfold is parametrized by
\[
 \operatorname{Prym}(C/E')/\{\pm1\},\qquad
 L\longmapsto L\oplus\iota^*L
\]
with exchange linearization. Frobenius is everywhere defined on this family and restricts to Prym Verschiebung. On the two anti-invariant differentials \(dx/w^3,x\,dx/w^3\), Cartier is zero for **all six listed primes \(p\equiv3\bmod4\)**. At \(13\) its matrix is \(\operatorname{diag}(11,8)\). For \(p\equiv1\bmod4\) the entry in row \(j\), column \(i\), for \(i,j=0,1\), is
\[
 [x^{(j+1)p-1-i}](x^3-2)^{3(p-1)/4}.
\]
For \(p\equiv3\bmod4\), Cartier would land in the opposite order-four character, whose holomorphic differential space is zero. Thus the fourfold contains a surface with a genuine change of differential rank **among the three-cycle primes themselves**.

For other weights even the target of Frobenius needs checking. On a tame root stack of order \(r\), Frobenius multiplies inertia characters by \(p\bmod r\). For example a difference \(1/5\) at \(p=7\) becomes \(2/5\), which differs also up to interchanging the two characters. An isomorphism between the two coarse projective lines would be extra data. There is no weight-independent Lattès self-map furnished by this operation.

## 3. Dormant opers with all four radii \(\boldsymbol{\pm1/4}\)

I fixed these radii because a \(\mathrm{PGL}_2\) radius is **half the exponent difference**, up to sign. Specifying the parabolic polarization alone does not specify an oper radius. The choice here is the one for which the order-two cover removes the projective singularities. Wakabayashi’s correspondence for maximally destabilized parabolic bundles uses its own pullback and weight hypotheses, including weights with denominator \(p^N\). Its enumerative formula cannot simply be applied to the base scheme of the tame half-weight map. [Wakabayashi, *Frobenius pull-back of parabolic bundles and dormant opers*, Theorems B–C](https://arxiv.org/html/2408.12267v1)

### The full sphere fiber and its arithmetic

Put \(f=x^3+b\), with \(b=-2\) or \(-8\), and take \(D=2y\,d/dx\) on \(E_b\). The projective oper with accessory parameter \(c\) is represented by
\[
 4f\,u''+2f'u'-cu=0.
\]
The exponent difference at each of the four marks is \(1/2\). These equations exhaust the oper line: once the double-pole parts are fixed, differences of projective connections form \(H^0(\mathbb P^1,K^2(D_{\rm marks}))\), which is one-dimensional, and \(c\) spans that space. Upstairs the equation is simply \(D^2u=cu\). The companion matrix \(A\) satisfies \(A^2=cI\), while \(D^{[p]}=H_p(E_b)D\). Its \(p\)-curvature vanishes precisely when
\[
 A^p-H_p(E_b)A=(c^{m_p}-H_p(E_b))A=0.
\]
An entry of \(A\) is \(1\), so this calculation gives the **scheme-theoretic equation**. It also agrees with the independent fusion-theoretic degree \(m_p\) for these radii. [Aoyama–Morita–Wakabayashi, §3, particularly Theorem 3.4](https://arxiv.org/html/2605.17973v1)

When \(H\ne0\), arithmetic Frobenius acts on the accessory coordinates by \(c^p=H^2c\). When \(H=0\), the fiber is one rational point thickened to length \(m_p\). In the table, \(r\times d\) means \(r\) closed points of residue degree \(d\).

| \(p\) | Cubic class | \(H_p(-2)\) | Oper fiber for \(-2\) | \(H_p(-8)\) | Oper fiber for \(-8\) |
|---:|---|---:|---|---:|---|
| 7 | three-cycle | 1 | \(3\times1\) | 4 | \(1\times3\) |
| 11 | transposition | 0 | one point, length 5 | 0 | one point, length 5 |
| 13 | three-cycle | 8 | \(3\times2\) | 11 | \(1\times6\) |
| 19 | three-cycle | 12 | \(3\times3\) | 8 | \(3\times3\) |
| 23 | transposition | 0 | one point, length 11 | 0 | one point, length 11 |
| 31 | identity | 4 | \(3\times5\) | 4 | \(3\times5\) |
| 43 | identity | 8 | \(3\times7\) | 8 | \(3\times7\) |

**Exact comparison theorem.** For \(p\equiv1\bmod3\), the two dormant fibers, with their accessory-coordinate \(\mu_{m_p}\)-actions, are isomorphic as \(\mu_{m_p}\)-torsors over \(\mathbb F_p\) exactly when \(p\) is an identity prime of \(L_0\).

Indeed,
\[
 \frac{H_p(-8)}{H_p(-2)}=2^{(p-1)/3}.
\]
Two such torsors are isomorphic precisely when this ratio belongs to \((\mathbb F_p^\times)^{m_p}=\{1,-1\}\). The ratio is a cube root of unity, so the condition is exactly that it equal \(1\). At \(19\) forgetting the torsor action discards the distinction. This identifies both the arithmetic invariant and the precise information lost by an unstructured point count. The comparison uses two fixed rational equations and their fixed differential normalizations.

### The torus fiber and the destabilized locus

There are explicit equations for the **full** torus oper fiber as well. With the same invariant derivation on \(E'\), write \(D^2u=Uu\), where
\[
 U(P)=-\frac3{16}\sum_{T\in E'[2]}x(P-T)
       +\frac{a_0+a_1x+a_2y+a_3x^2}{y}.
\]
The first term fixes the double-pole coefficient at each mark, since the indicial difference is \(1/2\). The four remaining functions are a basis of \(H^0(E',\mathcal O(O+Y))\). Starting from \((u_0,v_0)=(1,0)\), form
\[
 u_{j+1}=Du_j+Uv_j,\qquad v_{j+1}=u_j+Dv_j.
\]
Then the fiber is cut out in \(\mathbb A^4_{\mathbb F_p}\) by **all coefficients** of \(u_p=0,\ v_p=H_p(E')\) as identities of rational functions on \(E'\). This follows by writing \(D^j u=u_j u+v_j Du\). Differentiating the order-\(p\) identity gives the other row of the companion-system identity.

I computed a one-parameter slice as a check that also gives actual closed-point information. Since \(E'[2]=[2]^{-1}(O)\), pull back the one-mark equation
\[
 D^2u=(c-3x/16)u
\]
by the étale map \([2]\). Dormancy can be tested before that pullback. I ran the recurrence in \(\mathbb F_p[c,x,y]/(y^2-x^3+2)\) and took the monic gcd in \(c\) of every coefficient of \(u_p,v_p-H_p\). The middle column is the resulting **scheme equation on this slice**.

| \(p\) | Polynomial in \(c\) on the slice | Rational \(c\) | Length of full four-mark oper fiber |
|---:|---|---|---:|
| 7 | \(c^2\) | \(0\) | 26 |
| 11 | \(c^3-5\) | \(3\) | 155 |
| 13 | \(c^3+4\) | none | 301 |
| 19 | \(c^5+4c^2\) | \(0\) | 1,365 |
| 23 | \(c^6-8c^3-1\) | none | 2,926 |
| 31 | \(c^8+4c^5-2c^2\) | \(0\) | 9,640 |
| 43 | \(c^{11}-2c^8-19c^5-10c^2\) | \(0\) | 35,651 |

The last column is a geometric **length**, obtained independently from dormant fusion and finite flatness. Explicitly, put \(q=\lfloor(p-1)/4\rfloor\), index \(0\le i,j\le(p-3)/2\), and set
\[
 T_{ij}=\mathbf1_{\{|i-j|\le q\le\min(i+j,p-2-i-j)\}}.
\]
Gluing four three-point vertices in a loop gives \(\operatorname{tr}(T^4)\). The labeling convention sends \(q\) to \(\pm(2q+1)/2=\pm1/4\) in \(\mathbb F_p\). Finite flatness transports that length to this particular pointed CM curve. The rational-point column concerns only the displayed slice. [Wakabayashi, dormant-oper TQFT and trivalent graphs](https://arxiv.org/abs/2209.08528) · [Aoyama–Morita–Wakabayashi, radius convention and finite flatness in §3](https://arxiv.org/html/2605.17973v1)

There is an exact geometric test for the **whole Frobenius-destabilized locus** on the torus model. For a semistable \(W_C\), if \(F_C^*W_C\) is unstable, its maximal line \(L\) is \(\iota\)-equivariant. Its degree \(d\) satisfies
\[
 0<2d\le\deg\omega_C=4.
\]
Indeed its second fundamental form into \((F_C^*W_C/L)\otimes\omega_C\) is nonzero, since a horizontal destabilizing line would descend and destabilize \(W_C\). Thus **only \(d=1,2\) can occur**. Writing \(r_T\) for the ramification points, the set-theoretic test is
\[
 \exists\, S\subset E'[2],\quad M\in\operatorname{Pic}(E'),\quad
 2\deg M+|S|\in\{1,2\},\quad
 H^0\!\left(C,F_C^*W_C\otimes
  \big(\pi^*M(\textstyle\sum_{T\in S}r_T)\big)^{-1}\right)\ne0.
\]
The list exhausts the possible equivariant lines by canceling their inertia characters and descending the remainder. A nonzero section in this test saturates to a positive-degree line, which proves the converse. For \(d=2\) the second fundamental form is an isomorphism and gives an oper upstairs. For \(d=1\) it has a zero divisor of degree two. Thus an enumeration of maximally destabilized objects alone would leave out a possible stratum.

The oper computation also supplies examples in the maximal stratum. Pull a downstairs radius-\(\pm1/4\) projective connection to \(C\). In a ramified coordinate \(t=s^2\), the Schwarzian change cancels its prescribed double pole; a simple pole downstairs contributes a regular term upstairs. This gives a regular equivariant projective oper. Choose \(L=\pi^*\mathcal O_{E'}(O)\), with \(L^2=\omega_C\) as ordinary lines, and use sign determinant equivariantly. The determinant-normalized rank-two oper lift has top line \(L\) of degree two. At a dormant parameter, Cartier descent gives \(W_C\). It is stable: a line of nonnegative degree in \(W_C\) would pull back into the top line, and saturation would force its pulled-back degree to equal \(2\), impossible for \(p>3\). This explains geometrically why this construction gives destabilization on the torus whereas the sphere's degree-\(p\) map has empty base locus. I have given a cohomological test for the full unstable locus, without identifying its scheme multiplicities with the oper lengths in the table.

## 4. Exact coarse jets and the Archimedean barrier

Let \(E_0:y^2=x^3-2,\ E_1:y^2=x^3-8\), and let \(h\) be the normalized rational formal homomorphism from Round 2. Quotienting by inversion gives a formal germ between the two central parabolic moduli lines at \(\infty\). Their coarse coordinates can both be written \(S=1/x\); their arithmetic branch divisors differ. In the Round 2 coordinates \(x=z^{-2}\), the germ is
\[
 K(S)=h(\sqrt S)^2
 =S-\frac67S^4+\frac{96}{637}S^7-\frac{3264}{12103}S^{10}+\cdots .
\]

**Exact jet theorem.** Over \(R\), the least common denominator of the whole substitution \(N\)-jet of \(K\) is
\[
 \boxed{\displaystyle
 D_N=d_{2N}=
 \prod_{\operatorname{Frob}_p\text{ a three-cycle}}
 p^{v_p((2N)!)}.}
\]
The upper bound follows by restricting the Round 2 substitution to the even subring through degree \(2N\). For the matching lower bound, at a three-cycle prime pass to the unramified ordinary multiplicative coordinate \(X\). Inversion is \(X\mapsto X^{-1}\), so \(w=X+X^{-1}-2\) is an integral coarse parameter. Up to integral parameter changes, the map is \(X^u+X^{-u}-2\), where \(u=\sqrt[3]{2}\). Its coefficient of \(w^n\) is
\[
 \frac{2u^2\prod_{j=1}^{n-1}(u^2-j^2)}{(2n)!}.
\]
This is the expansion of \(2\cosh(ut)-2\) in \(2\cosh t-2\). Every numerator factor is a unit because \(\bar u\notin\mathbb F_p\). Taking \(n=N\) proves sharpness. Direct rational substitution matrices gave \(D_4=7,\ D_7=637,\ D_{10}=12103,\ D_{16}=7709611\). [Round 2 formal homomorphism and its denominator proof](/home/marcus/GitHub/mbintz/incandescent/wall1_astra_report.md)

There is a stable-point version. Take the points over \(x=0\) with \(y_0=\sqrt{-2}\), \(y_1=2\sqrt{-2}\). Translate to the origins upstairs, apply \(h\), translate back, and descend locally by \(x\). Conjugation negates both chosen points, so the coarse germ is rational. Both quotient maps are étale there at every \(p>3\). Its denominator is therefore exactly \(d_N\). The doubling in \(d_{2N}\) measures the ramification at the strictly semistable branch point.

Two Archimedean calculations put limits on what these constructions yield.

**First, the new branch germ has finite analytic radius.** On the real identity component, continue from \(\infty\) to the first nonzero half period of \(E_0\). There \(S=2^{-1/3}\), and the inverse elliptic integral has square-root branching. If \(\Omega_i\) is the positive real period for the specified invariant differential, then \(\Omega_1=\Omega_0/u\). At elliptic logarithm \(\Omega_0/2\), the target is consequently at \(u/2\) of its real period. Its \(1/x\) coordinate has nonzero derivative there. The branch survives in \(K\). Hence its radius satisfies \(0<R_K\le2^{-1/3}\), and Cauchy–Hadamard and Stirling give the sharp statement
\[
 \limsup_{N\to\infty}
 \frac{\log |K^{(N)}(0)|}{N\log N}=1 .
\]

**Second, positivity alone gives no class-dependent gain for full-space jets.** On the sphere, take the standard lattice of \(H^0(\mathbb P^1,\mathcal O(m))\) and probability Fubini–Study \(L^2\) norm. At the rational stable point \(x=0\), the coefficient and raw-derivative evaluation norms are exactly
\[
 \|[x^j]\|=\sqrt{(m+1)\binom mj},\qquad
 \|\partial_x^j|_0\|=j!\sqrt{(m+1)\binom mj}.
\]
The coefficient functional has integral content one, witnessed by \(x^j\). The mean Arakelov slope in this normalization is \(m/4+O(\log m)\), by summing the logarithms of the monomial norms. At \(m=j=N\), the raw jet has log norm \(N\log N+O(N)\). Rescaling a fixed continuous line metric on the compact coarse line changes the degree-\(m\) norm comparison by at most \(e^{O(m)}\). A numerical Quillen slope would additionally require a metric normalization and integral lattices, including at the omitted primes.

The full-space obstruction has a fourfold version. At a smooth stable rational point, take a sufficiently ample power and sections \(s_0,s_1\) with \(s_0\) nonvanishing and \(t=s_1/s_0\) a parameter in the chosen tangent direction. In level proportional to \(N\), the section \(s_1^N\) has leading coefficient one in this frame, integrally outside a fixed finite set of primes. Its raw derivative is \(N!\), and its norm costs at most \(e^{O(N)}\). Conversely, Cauchy on a fixed coordinate disk gives the upper bound \(N!e^{O(N)}\) for the raw jet in this regime with the sup norm. A passive integral Artin twist repeats the Smith factors. None of these operations supplies a three-cycle-dependent common factor.

**The missing ingredient for a global slope argument is a specified arithmetic formal direction or constrained space of sections that does both jobs simultaneously**: it must retain the cubic Frobenius comparison in its integral jets and admit a stronger Archimedean estimate in the same jet normalization. The oper torsors retain the comparison, and the coarse germ realizes it in one rational jet map. The full positive theta space admits unit jets, and the specific ramified germ has the sharp raw-derivative growth above. These results give local theorems and quantitative obstructions for the proposed maps. A constant-width zero-free strip remains open.