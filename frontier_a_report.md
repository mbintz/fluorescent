# Frontier A research report

**The standard arithmetic relative trace formula does not give the proposed prime-by-prime inequality.** There is an explicit counterexample on \(X_0(32)\) for the requested curve \(E_0\). Its Hecke eigenvalue at 41 is \(10\), yet the Gross–Zagier local intersection term for \(T_{41}\) at 41 is **zero**. The same correspondence contributes **\(-4\log 3\)** at 3. This example already has a one-dimensional space of cusp forms, so perfect spectral isolation does not fix the mismatch.

Two results survive the tests.

1. **An exact height criterion for \(E_0\).** There is an explicit moving Hecke operator \(B_X\), including prime powers, and an explicit constant \(\kappa\), such that GRH for \(L(E_0,s)\) is equivalent to
   \[
   \sup_{X\ge2}\widehat h\!\left((B_X-\kappa\log X)P\right)<\infty
   \]
   for one specified algebraic point \(P\) of infinite order. The height is extended quadratically to real coefficients. Positivity of this height is automatic. **Uniform boundedness** is the missing arithmetic estimate.
2. **A smaller Weil test family for the three named forms.** For \(f_{\chi_3},f_{E_0}\), and \(\Delta\), GRH is equivalent to Weil positivity on just the triangles \(\Phi_L(v)=(L-|v|)_+\), for every sufficiently large \(L\). An independent fact about these particular forms makes the reduction work: their eta products are positive on the imaginary axis, excluding real zeros to the right of the center. The reduction requires no arithmetic GGP conjecture.

These are structural results and conditional reductions. I obtain no new zero-free half-plane for either wall.

## 1. The moving cutoff on \(X_0(32)\)

Take \(f=f_{E_0}\), \(N=32\), and the **auxiliary Heegner field** \(K=\mathbf Q(\sqrt{-7})\). The prime 2 splits in \(K\), the class number is one, and \(\mathcal O_K^\times=\{\pm1\}\). Choose a Heegner point \(x\) on \(X_0(32)\) for the maximal order. Put \(c=[x-\infty]\) and \(d=[x-0]\). The cuspidal difference is torsion, so \(c=d\) in \(J_0(32)(K)\otimes\mathbf R\). The modular curve has genus one, and its unique normalized weight-two cusp form is \(f\). Thus \(T_p c=a_p c\) for every odd prime \(p\). [Gross–Zagier, Chapters I–III](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01388809/fulltext.pdf) · [Level-32 newform and coefficients](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/32/2/a/a/)

Write \(H=\widehat h_K(c)\) in the Gross–Zagier normalization. For arbitrary real coefficients \(c_p\), their exact spectral formula is
\[
\begin{aligned}
\left\langle c,\sum_{p\le X,\ p\ne2}c_pT_p d\right\rangle_K
 &=H\sum_{p\le X,\ p\ne2}c_p a_p,\\
H&=\frac{\sqrt7}{8\pi^2(f,f)_{\Gamma_0(32)}}L'_{\rm cl}(1,f/K).
\end{aligned}
\]
Here \((f,f)=\int_{\Gamma_0(32)\backslash\mathfrak H}|f(z)|^2\,dx\,dy\). The derivative is that of the base change, with \(L_{\rm cl}(s,f/K)=L_{\rm cl}(s,f)L_{\rm cl}(s,f\otimes\chi_{-7})\). This distinction matters even for a perfectly isolated eigenform. [Cai–Shu–Tian, Theorem 1.1](https://msp.org/ant/2014/8-10/ant-v8-n10-p05-p.pdf)

For disjoint divisor representatives the exact geometric side, in the same height convention, is
\[
 \sum_{p\le X}c_p\left[
 -\sum_{v\nmid\infty}(\overline c^{\,\mathrm{ad}}\cdot\overline{T_p d})_v\log Nv
 +\sum_{v\mid\infty}\langle c,T_p d\rangle_v
 \right].
\]
The first divisor has been corrected vertically to have intersection zero with each fiber component. The last terms are the archimedean Néron symbols. One can move representatives when necessary, or use Gross–Zagier’s regularization. The global identity \(T_p d=a_p c\) takes place in the Jacobian. Substituting linearly equivalent representatives into a **single** local symbol changes it by a term \(\log|u(c)|_v\) for a principal divisor \(\operatorname{div}(u)\). Only the global sum cancels that change. [Gross–Zagier, I §4 and III (0.1)](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01388809/fulltext.pdf)

### A computed off-diagonal contribution

Use \(T_{41}\). Both 41 and 3 are inert in \(K\). There is no ideal of norm 41, so \(c\) and \(T_{41}d\), with the indicated divisor representatives, have disjoint support. In the Gross–Zagier formula at an inert rational prime \(\ell\), the relevant sum runs over
\[
                 0<n<\frac{41\cdot7}{32},\qquad \ell\mid n .
\]
The additional term proportional to the number of ideals of norm 41 vanishes.

- At \(\ell=41\) the sum is empty.
- At \(\ell=3\) the possibilities are \(n=3,6\). For \(n=3\), the remaining norm is \(287-32\cdot3=191\). This is a split prime in \(K\), giving two ideals. The factor \(\operatorname{ord}_3(3n)\) is 2, the norm-one ideal count is 1, and the discriminant factor is 1. For \(n=6\), the remaining norm is \(95=5\cdot19\). Both primes are inert, so the ideal count is zero.

Consequently, with the subscript denoting the sum over places above the rational prime,
\[
 \boxed{\ \langle c,T_{41}d\rangle_{41}=0,\qquad
         \langle c,T_{41}d\rangle_3=-4\log3,\qquad a_{41}(E_0)=10.\ }
\]
There is a whole family behind the zero. For every inert Hecke prime \(p\) in this example, the putative diagonal summation requires \(0<n<7p/32\) and \(p\mid n\). It is empty. [Gross–Zagier, III, Proposition 9.7](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01388809/fulltext.pdf) · [Fourier expansion of \(f_{E_0}\)](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/32/2/a/a/)

One can of course put \((\log p)\log(X/p)/p\) into \(c_p\). This produces precisely \(H\) times the requested first-prime sum. Gross–Zagier then gives an equality with a **signed sum over all places**. The remaining problem is to bound that sum with its cancellations intact.

## 2. Three attempts to force localization or positivity

### Special divisors and Poincaré tests

Kudla–Rapoport supply genuine single-prime support. For example, take the positive definite ternary index \(T=\operatorname{diag}(1,1,p)\) at an odd inert prime of their imaginary quadratic field. Then \(\mathrm{Diff}_0(T)=\{p\}\), and the local elementary divisors have exponents \(0,0,1\). In the setting of their Theorem 1.1, the \(T\)-component of the intersection is
\[
       \operatorname{length}\mathcal Z(T)\log p,
 \qquad E'_T(z,0)=C_1\,\operatorname{length}\mathcal Z(T)\log p\,q^T .
\]
Thus one can select a Fourier index and force its characteristic of support. The resulting coefficient measures a representation density and a cycle length. The identity supplies no factor \(a_p(f)\). For the cubic form, taking the defining imaginary quadratic field \(\mathbf Q(\sqrt{-3})\) makes the mismatch especially sharp: **every such inert prime has \(a_p(f_{\chi_3})=0\)**. The same observation applies to \(E_0\) over its CM field \(\mathbf Q(i)\). [Kudla–Rapoport, Theorem 1.1](https://www.math.uni-bonn.de/people/rapoport/myalggeom/preprints/special_cycles_on_unitaryII_nov4.pdf)

Pairing a modular generating series with a Poincaré series can extract a coefficient where the weight, representation, and pairing permit it. Projecting a cycle-valued series to \(f\) is a different operation. On the modular curve one can see the outcome exactly: Gross–Zagier’s height generating series has coefficients \(\langle c,T_n d\rangle\), and its \(f\)-component has coefficients \(H a_n(f)\). Neither operation proves that the \(p\)-supported part of a coefficient survives projection with that value. Arithmetic theta inner-product formulas can genuinely identify a cuspidal projection with a central \(L\)-derivative under their hypotheses. That still leaves a fixed derivative and the moving Hecke eigenvalue. [Gross–Zagier, Chapter I](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01388809/fulltext.pdf) · [Li–Liu, *Chow groups and \(L\)-derivatives*](https://annals.math.princeton.edu/2021/194-3/p06)

### A Hecke operator at the AFL differentiation place

There is a precise formulation of the proposed local modification. In Li–Rapoport–Zhang’s conventions, for matching regular semisimple elements and matched spherical data it reads
\[
 2\langle g\Delta,\mathbb T_\varphi\Delta\rangle_{\mathcal N_{n,n+1}}\log q
       =-\omega(\gamma)\,\partial\operatorname{Orb}(\gamma,\varphi').
\]
The authors prove their spherical-Hecke formula for \(n=1\). The arbitrary-rank version with moving spherical functions is a conjecture in that work. Howard also formulates an arithmetic Siegel–Weil version with Hecke operators and verifies a low-dimensional case. Thus the proposed placement of the operator has mathematical content, with an important distinction between the local theorems and the general assertion. [Li–Rapoport–Zhang, (1.0.4) and Theorem 1.0.1](https://link.springer.com/article/10.1007/s00229-024-01572-0) · [Howard, *Arithmetic Siegel–Weil for the spherical Hecke algebra*](https://arxiv.org/abs/2609.13435)

Even granting the full local conjecture, consider one factorizable regular global orbital term. Gather its factors away from \(p\) into \(A^p_\gamma(s)\), with the chosen normalizations. Differentiation gives
\[
 \left.\frac{d}{ds}\big[O_{\gamma,p}(h_p,s)A^p_\gamma(s)\big]\right|_{0}
 =
 O'_{\gamma,p}(h_p,0)A^p_\gamma(0)
 +O_{\gamma,p}(h_p,0)(A^p_\gamma)'(0).
\]
The proposed sum of test functions sums **both terms** over \(p\). A unit test function away from \(p\) can have a nonzero orbital derivative there. Zhang’s original global treatment also distinguishes the main local term from boundary and cohomological-trivialization contributions. [Wei Zhang, §3.3, (3.6)–(3.8)](https://math.mit.edu/~wz2113/math/online/AFL.pdf)

There are two legitimate modifications. One can retain the first summand by definition, obtaining a sum of marked local distributions. This requires a **new global comparison** to obtain an isolated \(f\)-spectral side. Or one can force an undifferentiated orbital factor to vanish on selected orbits, as in the singleton-difference construction. That condition is orbit-specific. On a holomorphic spectral term \(b_f(s)L_f^{\rm aux}(s)\) with \(L_f^{\rm aux}(0)=0\), forcing \(b_f(0)=0\) kills its first derivative too. A vanishing argument therefore has to specify the orbits it removes and the spectral term it preserves.

### The height matrix across primes

Let \(z\) be an \(f\)-eigenclass, and use the positive Néron–Tate pairing. For the real-eigenvalue forms in question,
\[
 M_{pq}=\langle T_pz,T_qz\rangle
       =\widehat h(z)a_p a_q,\qquad
 c^*Mc=\widehat h(z)\left|\sum_pc_pa_p\right|^2 .
\]
Every minor of size at least two vanishes. For \(E_0\), the submatrix on \(5,13\) is
\[
 \widehat h(z)\begin{pmatrix}4&-12\\-12&36\end{pmatrix}.
\]
So positive semidefiniteness holds for every size and sign of the prime sum. It supplies no upper bound or one-sided cancellation. For an unprojected class with orthogonal Hecke decomposition the matrix is \(\sum_g H_g a(g)a(g)^*\). A sufficiently strong **upper** estimate for this positive sum could bound an individual square. The Hodge index theorem alone supplies no such estimate. At level 32 even the other eigensystems are absent. [Gross–Zagier, I §4](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01388809/fulltext.pdf) · [Level-32 coefficients](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/32/2/a/a/)

## 3. What happens to the factor \(m\)

The standard arithmetic diagonal uses adjacent ranks. At the distinguished real place the usual signatures are \((n-2,1)\) and \((n-1,1)\). The varieties have dimensions \(n-2\) and \(n-1\), and their graph cycle has codimension \(n-1\) in a product of dimension \(2n-3\). Twice that codimension is the dimension plus one, as required for a height. Merely specifying \(U(n-1,1)\times U(n)\) with compact second factor does not specify this arithmetic diagonal. The associated GGP \(L\)-function is the Rankin–Selberg product of the two base changes, of degree \(n(n-1)\) over the base-change field. [Rapoport–Smithling–Zhang, *Arithmetic diagonal cycles*](https://doi.org/10.1112/S0010437X20007289) · [Wei Zhang, Conjecture 3.8](https://math.mit.edu/~wz2113/math/online/AFL.pdf)

Three scaling calculations distinguish possible mechanisms.

- **Repeated eigenclasses.** For \(z^{\oplus m}\) the linear pairing is \(mH\sum c_pa_p\), and its squared height after applying the cutoff is \(mH|\sum c_pa_p|^2\). Dividing by the corresponding height of the input cancels \(m\) exactly. More generally, for \(m\) independent cycles in the same Hecke eigenspace the matrix indexed by cycles and primes is \(H_{ij}a_pa_q\). Independence of the cycles does nothing to the rank in the prime indices. In the repository’s definite argument there really is an error term that gains on division by \(m\): the displayed size budget contains \(n_Ta_E(1+m^2/k)\), while the signal contains \(n_Tmb\) times a density, with \(a_E\le2Xb\). The leading ratio before density losses is \(O(X/m)\). No corresponding estimate follows from an identity of heights on the indefinite tower. [Lean growth inequality and size budget](/home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SizeWindowBrackets/GrowthBoundGivesRiemannHypothesis.lean:87)
- **Arthur blocks.** At an unramified place of residue size \(q\), a unitary character block \(\mu[t]\) contributes to the standard trace
  \[
                  \mu(\varpi)\sum_{j=0}^{t-1}q^{(t-1)/2-j}.
  \]
  For \(t>1\) this parameter is non-tempered. Its trace has magnitude at least \(q^{(t-1)/2}\). For a fixed \(t\), on degree-one primes with the triangular weight \((\log p)p^{-1/2}\log(X/p)\), the leading term alone has absolute budget of order \(X^{t/2}\) on a fixed splitting set of positive density. Already \(t=2\) costs order \(X\). A tempered arithmetic inner-product theorem cannot simply be applied to these blocks. With \(t=1\) there is still a different difficulty: writing two parameter traces as \(a+B\) and \(a+C\), their tensor-product trace with the second dual is \(|a|^2+a\overline C+B\overline a+B\overline C\). With \(O(m)\) auxiliary characters on each side, the last term has \(O(m^2)\) character pairs. At \(m\asymp\sqrt X\) this is \(O(X)\) pairs. This counts terms, without assuming they add with one sign. Their removal needs an identity or a bound. [Li–Liu, hypotheses on the tempered packet](https://annals.math.princeton.edu/2021/194-3/p06)
- **Higher derivatives.** Increasing the dimension of the ordinary arithmetic diagonal still gives a *first* derivative. Even if \(m\) sign-minus factors are arranged to vanish at the center \(s_0\), differentiation gives
  \[
      \left(\prod_{j=1}^m L_j\right)^{(m)}(s_0)
          =m!\prod_{j=1}^m L'_j(s_0).
  \]
  Repeating one factor produces a power of one central quantity. Genuine higher Gross–Zagier formulas over function fields use shtukas with multiple modifications; there the number of modifications is part of the geometric construction. The number-field tower in the question does not furnish that construction or a uniform bound on its Green functions. [Yun–Zhang, *Shtukas and the Taylor expansion of \(L\)-functions II*](https://annals.math.princeton.edu/2019/189-2/p02)

There is a further obstruction to deriving Weil positivity solely from determinants of central derivatives. Let \(0<a<1/2\) and \(F(z)=\cosh a+\cosh z\), with \(z\) measured from the center. It is the bilateral Laplace transform of the positive measure \(\cosh(a)\delta_0+(\delta_{-1}+\delta_1)/2\). Hence every matrix \((F^{(i+j)}(0))_{i,j=0}^d\) is positive semidefinite, for every \(d\). Yet \(F\) has zeros at \(z=\pm a+(2j+1)\pi i\). Convolving the measure with a uniform measure on an interval makes every finite moment matrix positive definite and retains these zeros. This counterexample concerns the proposed positivity inference. Extra arithmetic information, such as an identity for the logarithmic derivative with its Euler factors, can change the problem.

## 4. A bounded-height criterion with the correct scale

Use unitary normalization \(L_f(s)=L_{\rm cl}(s+(k-1)/2,f)\). Let \(b_f(p^j)\) be the sum of the \(j\)-th powers of the normalized local Euler roots, using the actual Euler factor at bad primes. Define
\[
 \begin{aligned}
 S_f(X)&=\sum_{p^j\le X}\frac{b_f(p^j)\log p}{p^{j/2}}\log(X/p^j),\\
 r_f&=\operatorname{ord}_{s=1/2}L_f(s),\qquad
 \kappa_f=\tfrac12\log N-\log(2\pi)+\frac{\Gamma'}{\Gamma}(k/2),\\
 R_f(X)&=S_f(X)-\kappa_f\log X+\tfrac12r_f(\log X)^2 .
 \end{aligned}
\]

**Proposition.** For a fixed self-dual holomorphic cuspidal newform as above, the following are equivalent:

1. GRH for \(L_f\).
2. \(R_f(X)=O_f(1)\) for all \(X\ge2\).
3. \(R_f(X)\ge -C_f\) for all \(X\ge2\).

**Proof.** Write \(L=\log X\). The Fourier transform of the triangle, with frequency \(t\), is
\[
 h_L(t)=\frac{2(1-\cos Lt)}{t^2},\qquad h_L(0)=L^2.
\]
The explicit formula reads \(W_f(\Phi_L)=A_f(L)-2S_f(e^L)\). Its conductor and gamma contribution is
\[
                   A_f(L)=2\kappa_f L+O_f(1).
\]
Indeed \(\int h_L(t)\,dt/(2\pi)=L\). After subtracting its value at zero, the real digamma integrand is \(O_f(t^2)\) near zero and \(O_f(\log(2+|t|))\) at infinity. Multiplication by \(h_L(t)\le4/t^2\) gives a uniformly bounded remainder. Under GRH the central zeros contribute \(r_fL^2\), and the other zeros contribute \(O_f(1)\), since \(\sum_{\gamma\ne0}\gamma^{-2}<\infty\). This proves 1 implies 2. [Bober, explicit formula and triangular test in the elliptic-curve normalization](https://msp.org/obs/2013/1-1/obs-v1-n1-p07-s.pdf)

For the converse, initially for \(\Re z>1/2\),
\[
 \int_1^\infty S_f(X)X^{-z-1}\,dX
                  =-\frac{1}{z^2}\frac{L_f'}{L_f}(1/2+z).
\]
Under 3, add a constant to make \(R_f+C_f\) nonnegative on \([1,\infty)\). Its Mellin transform differs from the displayed expression by a rational function with poles only at \(z=0\). If its abscissa of convergence were positive, Landau’s theorem would force a singularity at that **real** abscissa. The only candidate is a zero of \(L_f(1/2+z)\), where the residue is \(-\operatorname{ord}(L_f)/z^2<0\). This is impossible for a nonnegative integral approached from the right. Thus the transform is holomorphic on \(\Re z>0\), excluding complex zeros there as well. The functional equation finishes the proof.

This identifies the costs in the cutoff. With \(w_p=(\log p)p^{-1/2}\log(X/p)\), the prime number theorem gives \(\sum_{p\le X}w_p\sim4\sqrt X\). Using \(|b_f(p^j)|\le2\), the absolute budget of prime squares is \(O((\log X)^2)\), that of powers \(j\ge3\) is \(O(\log X)\), and finitely many bad primes cost \(O_f(\log X)\). Thus a prime-only estimate can target a polylogarithmic error. The **bounded remainder** requires retaining the prime powers, the archimedean linear term, and any central-rank quadratic term.

### The explicit operator for \(E_0\)

On the elliptic quotient use the classical Hecke operators and set
\[
 B_X=\sum_{\substack{p^j\le X\\p\ne2}}
 \frac{\log p}{p^j}\log(X/p^j)
       \bigl(T_{p^j}-pT_{p^{j-2}}\bigr),
\]
where the subtraction is omitted for \(j=1\) and \(T_1=1\). By the Hecke recursion the operator in parentheses has eigenvalue \(\alpha_{p,\rm cl}^j+\beta_{p,\rm cl}^j\). The Euler factor at 2 is trivial. Hence \(B_X\) acts on \(E_0\) by the exact scalar \(S_{E_0}(X)\).

Take \(P=(2,\sqrt6)\in E_0(\mathbf Q(\sqrt6))\). Under twisting it corresponds to \((12,36)\) on \(y^2=x^3-36x\). Its double has \(x\)-coordinate \(25/4\), so Nagell–Lutz proves it has infinite order. The form \(f_{E_0}=\eta(4z)^2\eta(8z)^2\) has positive Mellin integral at its center, hence \(r_{E_0}=0\). With \(\kappa=\tfrac12\log32-\log(2\pi)-\gamma\), we obtain
\[
 \boxed{\quad
 \mathrm{GRH}(E_0)\quad\Longleftrightarrow\quad
 \sup_{X\ge2}\widehat h\!\left((B_X-\kappa\log X)P\right)<\infty .
 \quad}
\]
Indeed the height equals \(\widehat h(P)|R_{E_0}(X)|^2\). A one-sided lower bound for the **linear** pairing with \(P\) also suffices by the proposition. Choosing this \(P\) removes any auxiliary conjecture about the nonvanishing of a Heegner height. This is an explicit arithmetic target, not an independent estimate for it. [Level-32 eta product](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/32/2/a/a/)

### Which one-sided sign works

For the repository’s nonprincipal smoothing, the corresponding definition is
\[
 G_f(x)=\sum_{n\le x}\Lambda_f(n)(x/n-1)+x(L_f'/L_f)(1).
\]
Its Mellin transform has principal term \(- (L_f'/L_f)(s)/[s(s-1)]\). At a real zero \(1/2<\beta<1\), its residue is **positive**, \(r_\beta/[\beta(1-\beta)]\). Thus an upper bound on \(-G_f\) allows this real-zero main term. Nonnegativity of the Dirichlet coefficients of \(-2\zeta'/\zeta+L_f'/L_f\) does not by itself remove it. The logarithmic triangle used above has a different denominator and the opposite residue sign. The repository itself distinguishes upper and lower versions of its oscillation statement. [Lean smoothing definition](/home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/StatementOC.lean:19) · [Lean upper and lower hypotheses](/home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/StatementOC.lean:22)

For the **three named forms** there is a direct repair. Their eta products are respectively \(\eta(6z)\eta(18z)\), \(\eta(4z)^2\eta(8z)^2\), and \(\eta(z)^{24}\). Each is strictly positive at \(z=iy\), \(y>0\). Cuspidality at both ends makes the Mellin integral converge for every real argument, and the completed \(L\)-function is positive there. In particular it has no real zero to the right of the center. Now \(W_f(\Phi_L)\ge0\) for all sufficiently large \(L\) implies \(S_f(e^L)\le\kappa_f L+O_f(1)\). Apply Landau to \(C(1+\log X)-S_f(X)\). Its transform has no possible real singularity on \(\Re z>0\), hence no complex pole there either. Conversely GRH gives \(W_f(\Phi_L)\ge0\) directly from \(h_L(\gamma)\ge0\). This proves the single-family Weil criterion stated at the outset. The proof uses all sufficiently large \(L\); the repository’s assertion about arbitrarily distant windows has stronger oscillation content and is stated for its own Dirichlet family. [Cubic eta product](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/108/1/c/a/) · [Elliptic eta product](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/32/2/a/a/) · [Discriminant form](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/1/12/a/a/) · [Lean window quantifiers](/home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/Window.lean:9)

## 5. What distinguishes the two walls

**Wall 1 admits an exact same-prime geometric realization in dimension zero.** Over \(\mathbf Z[1/6]\), take the finite étale scheme \(Y=\operatorname{Spec}\mathbf Z[1/6,t]/(t^3-2)\). It is also the scheme of nonzero 2-torsion points of \(y^2=x^3-2\). Its permutation representation is \(\mathbf 1\oplus\rho_{\rm std}\). Consequently, for every \(p\nmid6\) and every \(j\ge1\),
\[
 b_{f_{\chi_3}}(p^j)=\#Y(\mathbf F_{p^j})-1.
\]
The count is exactly the length of the fixed-point locus of the \(j\)-th Frobenius on the geometric fiber. At \(j=1\), identity, transposition, and three-cycle give \(2,0,-1\), respectively. The local factors at 2 and 3 of the cubic Artin quotient are trivial. Thus the proposition turns Wall 1 into a one-sided bound for an explicit weighted sum of **centered finite étale intersection lengths**. No moving modulus or weight-one projector is needed. Positivity of each uncentered length supplies no estimate for that discrepancy. [Cubic Artin representation and modular form](https://www.lmfdb.org/ModularForm/GL2/Q/holomorphic/108/1/c/a/)

The Stark regulator here can likewise be evaluated already. Writing \(a=\sqrt[3]2\), the class number is 1 and \(a-1\) is a fundamental unit. From \(\zeta_F=\zeta L_{f_{\chi_3}}\), \(\zeta(0)=-1/2\), and the analytic class number formula,
\[
          L'_{f_{\chi_3}}(0)=R_F=\log(1+a+a^2).
\]
This is one fixed special value. Darmon–Vonk’s RM points use real quadratic fields in a \(p\)-adic upper half-plane. The quadratic resolvent here is imaginary. Also, in the complex ball for \(U(2,1)\) the stabilizer of a negative line is compact, so a torus with a noncompact real factor cannot fix a point there. Passing to a real cycle or a regulator requires a new comparison with the moving discrepancy above. The known special value does not supply it. [Field and fundamental unit](https://www.lmfdb.org/NumberField/3.1.108.1) · [Darmon–Vonk, *Singular moduli for real quadratic fields*](https://www.math.mcgill.ca/darmon/pub/Articles/Research/69.DV1/paper.pdf)

**Wall 2 also admits exact same-prime intersections, with an instructive Hodge-index calculation.** At a good prime let \(q=p^j\), and let \(\Gamma\) be the graph of the \(q\)-power Frobenius on \(E_{\overline{\mathbf F}_p}\). Then \(\Gamma\cdot\Delta=\#E(\mathbf F_q)\). Put \(H=E\times\{0\}\), \(V=\{0\}\times E\), \(\Gamma^\circ=\Gamma-H-qV\), and \(\Delta^\circ=\Delta-H-V\). Direct intersection gives
\[
 (\Gamma^\circ)^2=-2q,\qquad
 (\Delta^\circ)^2=-2,\qquad
 -\Gamma^\circ\cdot\Delta^\circ=q+1-\#E(\mathbf F_q).
\]
The Hodge index inequality therefore gives exactly
\[
                   |q+1-\#E(\mathbf F_q)|\le2\sqrt q.
\]
After multiplying by \((\log p)q^{-1}\log(X/q)\), the mixed intersection is precisely the requested summand for \(S_E(X)\). This construction solves the **prime-label** problem outright, for CM and non-CM elliptic curves alike. Its positivity controls one fiber at a time. Summing those individual bounds leaves the \(O(\sqrt X)\) first-prime budget computed above. The bounded-height criterion requires cancellation down to an explicit linear function of \(\log X\) with bounded remainder for \(E_0\).

**Conclusion.** For a further arithmetic RTF attack, the missing ingredient can be specified numerically: a global comparison or inequality controlling these *centered same-prime traces across different residue characteristics*. The classical projected height has only one prime-direction in its Gram matrix. The AFL gives a genuine marked local derivative, and Kudla–Rapoport give genuine single-prime support, but neither supplies that cross-prime estimate. Wall 1 simplifies the local cycles to three étale points. The required global cancellation survives that simplification in full.