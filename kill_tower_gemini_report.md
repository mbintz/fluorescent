# Killing the Behrend Set & Iwasawa Tower — Track 3 Report (Gemini)

**Scope:** Independent source audit of `/home/marcus/GitHub/mbintz/incandescent/lean/src/`, exact numerical/combinatorial checks (`IncomingBound` LP, Wach $p$-adic valuations, tower exponent polytope), and structural analysis of:
1. **Killing the Behrend set** (`remark.pdf` item 19 / footnote 7), with an exact necessity-and-sufficiency theorem tying Behrend to `ThickLe2` (`ro ≤ 2`) in Wach-module arc lifting.
2. **Killing / minimizing the 2-power cyclotomic Iwasawa tower** $H_e = (\mathbb{Z}/2^{e+2}\mathbb{Z})^\times / \{\pm 1\} \cong \mathbb{Z}/2^e\mathbb{Z}$, mapping every lower-bound wall and testing the `IncomingBound` LP, two-stage bootstrap, prime-conductor / small-degree families, and parameter retuning.

---

## Executive Verdict

1. **Behrend Set (`NoRel` / `WindowTwo` / `BehrendFree`):**
   - **Where Behrend actually lives:** Contrary to naive intuition, Behrend is **not** needed for `ThickAverage` (any $T_2$ with $\delta_2 \ge x^{-\varepsilon}$ works), **not** needed for `OrbitOne` on short orbits $\operatorname{ord}(h_l) \le 4 L_w$ (which uses *only* the trivial interval containment $T_2 \subset [0, n/(4 L_w))$), and **not** needed for `IncomingBound.lean` (which uses the *already-Bernoulli* top set `TT`, not `T2`). Behrend enters **solely** through Wach-module crystalline congruence-length bounds:
     - `HalfB` ($11 \le l < l_A$, long orbits): `WindowTwo` $\to$ `winClusters` $\to$ `Clusters (jA l)` $\to$ `ThickLe2` (`ro ≤ 2`) in [`WachCoordinates.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/WachCoordinates.lean#L21-L84).
     - `HalfCD` ($l \ge l_A$): `WindowTwo` $\to$ `NoThree` $\to$ `WordsNT` $\to$ `RowBoundsOfNonThickLetter` (which cuts at thin letters into arcs of $\le 2$ consecutive thick letters).
   - **Sharp Necessity-and-Sufficiency Dichotomy:**
     - **If `ro ≤ 2` (or `NoThree`) is kept pointwise for all long-orbit inert primes:** Behrend **cannot** be replaced by Bernoulli sampling, intervals, or Bohr sets. Because $l_A = \frac{k x^\varepsilon}{m \delta_2} \approx x^{4+12\varepsilon} \gg n \approx x^{2+8\varepsilon}$, inert primes hit all of $H_e$, so `NoThree` at density $\delta_2 \ge x^{-\varepsilon}$ is logically equivalent to a dense 3-AP-free set in $\mathbb{Z}/n\mathbb{Z}$ (where probabilistic alteration stalls at $\delta_2 \asymp n^{-1/2} \approx x^{-1}$, and even avoiding only alternating `up-down-up` triples forbids $x, x+h, x+2h$).
     - **If Wach-module arc lifting is extended from `ro ≤ 2` to constant `ro ≤ K` with $K = \lceil 15/\varepsilon \rceil + 50 = O(1/\varepsilon)$:** Behrend **dies completely** in 10 lines via independent Bernoulli sampling on $[0, n/(4 L_w))$ with $\delta_2 = x^{-\varepsilon/2}$ (strictly denser than Behrend's $\exp(-C\sqrt{\log n \log L_w})$, using the exact `TopsBad` machinery already formalized in [`BehrendSets/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/BehrendSets/Statement.lean#L101-L126)). Crucially, [`LocalTheoryWindows.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/LocalTheoryWindows.lean#L87-L120) and [`ArcLiftingSetup.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/ArcLiftingSetup.lean#L392-L450) **already support arbitrary `roMax = K`** in `UnivCore`, `KillerKap`, and `cls.card` — the *only* remaining bottleneck is extending `WordOK` / `ConstLift` past `up-down-up` ($s_0 < s_1 < s_2$), which we test numerically in $\mathbb{Z}_l[X]/(p_1^b)$ below.

2. **Iwasawa Tower $H_e = \mathbb{Z}/2^e\mathbb{Z}$ ($n = 2^e \asymp x^{2+8\varepsilon}$):**
   - **Hard Chebotarev floor ($n \ge x^{1/2 - \varepsilon}$):** Even in the abstract [`SizeConditions`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L112-L128) (and `phic_G`), any single fixed host field of degree $4n$ dumps at least the split-in-$F_1$ primes ($\operatorname{Frob}_p = c$, density $\sim 1/n$) into `phic`, forcing $\text{phic} \gtrsim \frac{x \log x}{n} \implies n \ge x^{1/2 - \varepsilon}$. Averaging upper bounds across a family of bounded-degree fields $f_i \le F$ leaves $\sum w_i (x/H_i) \ge x/F$, giving no saving.
   - **Why the proof actually sits at $n \asymp x^{2 + 8\varepsilon}$ (not $x^{1/2}$):** In [`DataParams.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalRingCardinality/DataParams.lean#L11-L141), `jG = 5` and `hExp = (jG - 1)/2 + 8ε = 2 + 8ε` arise from the closed algebraic squeeze (coupled with $f = [F:\mathbb{Q}] = 2n$ and $m \approx x^{1/2}$):
     $$C m^{j_G} (2n) L x^\varepsilon \;\le\; k \;\le\; m (n x^{-\varepsilon})^2 \quad \Longrightarrow \quad n \;\ge\; 2 C m^{j_G - 1} x^{3\varepsilon} \;\approx\; x^{(j_G - 1)/2} = x^2.$$
     This quadratic barrier is **independently reinforced** by `m^4 ≤ f = 2n` ([`StandingNumericalData.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean#L118)) and the linear short-order budget (`SizeOrders`), while `SizeLa`/`SizeRho` independently enforces $n \ge x^{3/2}$.
   - **Why the 2-power tower is uniquely optimal among abelian towers:** (i) 2-group parity `CInPhi` ensures $c \in \langle \operatorname{Frob}_l \rangle \iff \operatorname{Frob}_l = c$ (odd-order factors break `DefiniteLiftChain`); (ii) Lifting-The-Exponent gives the congruence threshold $l \equiv \pm 1 \pmod{4n/2^{j_0}} \implies l \ge 4n/J - 1$ (`ShortOrdLarge` / `ShortOrdSq`), whereas prime conductors $r$ admit small primes $l \sim r^{1/J}$ of short order and multiquadratic fields have exponent $2$.
   - **`IncomingBound` LP & Two-Stage Bootstrap:** Verified numerically that the `IncomingBound` LP holds identically down to the smallest even orbit length $d = 2$ (it imposes **zero** polynomial lower bound on $n$). Replacing `ThinScales`'s exponential $X' = \exp(x^{\varepsilon/3})$ by a polynomial $X' = x^B$ via a two-stage zero-free strip bootstrap relaxes the *upper* bound $w'' \ge \sqrt{b}$ and trims $O(\varepsilon)$ from `ShortOrdLin`, but leaves the leading tower exponent $\alpha = 2$ completely unchanged.

---

## 1. Complete Audit of Behrend Set (`T2`) Consumers in `lean/src/`

Tracing every reference to `T2`, `BehrendFree`, `SpaceFree`, `NoRel`, `WindowTwo`, `OrbitOne`, `Clusters`, and `NoThree` across the codebase isolates **exactly four** consumers:

| # | Consumer | Lean Source | Property of `T2` Actually Used | Needs Behrend? |
|---|---|---|---|---|
| 1 | Thick translate average | [`ThickAverage.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/ThickAverageProofs/ThickAverage.lean#L203-L250) | Density $\delta_2 = |T_2|/n \ge x^{-\varepsilon}$ only (`TranslateMean`) | **No** |
| 2 | Short-order inert orbits ($\operatorname{ord}(h_l) \le 4 L_w$) | [`BehrendSets/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/BehrendSets/Statement.lean#L72-L75), [`ConclusionR7abs.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/GlobalSchurBounds/ConclusionR7abs.lean#L147) | `OrbitOne`: $\le 1$ hit per coset, proved purely from $T_2 \subset [0, n/(4 L_w))$ | **No** |
| 3 | Large inert primes ($l \ge l_A$, `HalfCD`) | [`NotDvdCondN.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Definitions/GaloisGeometry/NotDvdCondN.lean#L73-L75), [`RowBoundsOfNonThickLetter.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Proofs/InertiaEigenvalues/RowBoundsOfNonThickLetter.lean#L97-L176) | `NoThree` (no 3 consecutive thick letters along `c0`-orbits; `sgc0`-orbits already satisfy `NoConsecutiveThickPlaces` for *any* $T_2$) | **Yes** if `ro ≤ 2`; **No** if `ro ≤ K` |
| 4 | Small inert primes ($11 \le l < l_A$, `HalfB`) | [`AtMostTwoThickInWindowLongOrbit.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/AtMostTwoThickInWindowLongOrbit.lean#L27-L54), [`CyclicWordMarkedClustersOfAtMostTwoInWindow.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Proofs/SatakeParameters/CyclicWordMarkedClustersOfAtMostTwoInWindow.lean#L21-L88), [`WachCoordinates.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/WachCoordinates.lean#L21-L162) | `WindowTwo` of width $L_w \ge 2 j_A(l) + 1 = O_\varepsilon(\log x)$ $\to$ `Clusters (jA l)` $\to$ `ThickLe2` (`ro ≤ 2`) | **Yes** if `ro ≤ 2`; **No** if `ro ≤ K` |

Note that the top set **`TT`** (density $\delta_1 = x^{-\varepsilon/8}$) is **already** constructed without Behrend via Bernoulli sampling (`SelectTops` / `TopsBad` in [`BehrendSets/StatementE.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/BehrendSets/StatementE.lean#L60-L87)) with constant window-multiplicity threshold $K_G = \lceil 8(h_G + 2)/\varepsilon \rceil = O(1/\varepsilon)$ ([`IsResidueClassZero.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/GrowthBounds/IsResidueClassZero.lean#L37-L41)).

---

## 2. Necessity-and-Sufficiency Theorem for Killing Behrend

### 2.1 Why Pointwise `ro ≤ 2` Forces a Behrend Set (Obstruction to Elementary Substitutes)

Suppose we retain `NoThree` / `WindowTwo` pointwise for all long-orbit inert primes $l$ (or even just $11 \le l < l_A$) while maintaining $\delta_2 \ge x^{-\varepsilon}$ (required because the signal in [`ThickAverageLoss/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L81-L97) is weighted by $\delta_2/2$ while unscaled losses such as `iv ≤ C x^{1/2+ε}` are independent of $\delta_2$).

1. **All steps in $H_e$ are realized:** Since $l_A = \frac{k x^\varepsilon}{m \delta_2} \approx x^{4+12\varepsilon} \gg n \approx x^{2+8\varepsilon}$, every $h \in H_e$ with $\operatorname{ord}(h) > 4 L_w$ occurs as $h_l$ for inert primes $l < l_A$.
2. **Translation invariance preserves 3-APs:** If $T_2$ contains $(x, x+h, x+2h)$, then *every* translate $T_2 + u_0$ contains $(x+u_0, x+u_0+h, x+u_0+2h)$. Thus averaging over $u_0 \in H_e$ does not dilute 3-APs.
3. **Failure of Bernoulli / Alteration / Intervals / Bohr sets at $K = 2$:**
   - **Random Bernoulli** on $[0, M)$ ($M = n/(4 L_w)$) with inclusion probability $p = 4 L_w \delta_2$ has $\mathbb{E}[\#\text{bad triples}] \asymp L_w^2 M^2 p^3$. Deletion/alteration requires $L_w^2 M^2 p^3 \le \frac{1}{2} M p \iff p \le (\sqrt{2} L_w \sqrt{M})^{-1}$, forcing $\delta_2 \lesssim n^{-1/2} L_w^{-1} \approx x^{-1} \ll x^{-\varepsilon}$.
   - **Intervals / $D$-dimensional Bohr sets** of density $\delta_2 \ge x^{-\varepsilon}$ have difference-set volume $\ge \delta_2$ (ruling out `WindowOne`) and contain $\Omega(\delta_2^3 n^2)$ 3-APs by Roth–Kelley–Meka (ruling out `WindowTwo` / `NoThree`).
   - **Even forbidding only `up-down-up` / `down-up-down` fails:** Along an inert orbit, `up`/`down` alternates every step (`Alternates W.up`), so any 3-AP $\{x, x+h, x+2h\}$ has step gaps $1, 1$ (both odd) and immediately creates an alternating `up-down-up` or `down-up-down` triple.
   - **Dropping bad windows at $K = 2$ into `cls` fails:** For $K = 2$, a random set produces a bad-window density of $(L_w p)^3 \approx x^{-3\varepsilon/2}$, which cannot absorb the factor $l_A \approx x^{4 + 12\varepsilon}$ separating `WordsB` ($\sim b/(l_A l)$) from trivial `eLift` ($\sim b/l$).

### 2.2 The Exact Behrend-Killer: Bernoulli `WindowK` ($K = O(1/\varepsilon)$) + `ArcAt` Extension

Replacing `WindowTwo` ($K = 2$) by **`WindowK`** with constant $K = \lceil 15/\varepsilon \rceil + 50 = O(1/\varepsilon)$ kills Behrend completely in ~10 lines of elementary probability:

**Lemma (Bernoulli Thick Set with `WindowK` and `OrbitOne`).**
Let $n = 2^e \le 2 x^{2 + 8\varepsilon}$, $L_w' = K \cdot L_w = O_\varepsilon(\log x)$, $M = \lfloor n / (4 L_w') \rfloor$, and $\delta_2 = x^{-\varepsilon/2}$. Form $T_2 \subseteq [0, M)$ by including each $s \in [0, M)$ independently with probability $p = 4 L_w' \delta_2 \ll x^{-\varepsilon/3}$. Then for sufficiently large $x$:
1. **Density (strictly better than Behrend):** $|T_2| \in [\frac{1}{2}\delta_2 n, 2\delta_2 n]$ with probability $1 - \exp(-\Omega(n x^{-\varepsilon/2}))$.
2. **`OrbitOne` (unchanged):** Since $T_2 \subset [0, n/(4 L_w'))$, every short orbit $\operatorname{ord}(h) \le 4 L_w'$ hits $T_2 + u_0$ in at most $1$ point, deterministically for every realization of $T_2$.
3. **`WindowK` pointwise for ALL $u_0, t, h \in H_e$ with $\operatorname{ord}(h) > 4 L_w'$:** There are at most $n^2 \le 4 x^{4 + 16\varepsilon}$ windows $W = \{t + i h : 0 \le i < L_w'\}$ (quantifying over $t \in H_e$ already absorbs all translates $u_0$). Each window consists of $L_w'$ distinct elements of $\mathbb{Z}/n\mathbb{Z}$, so
   $$\Pr\big[|W \cap T_2| \ge K + 1\big] \le \binom{L_w'}{K+1} p^{K+1} \le (4 (L_w')^2 \delta_2)^{K+1} \le x^{-(K+1)\varepsilon/3}.$$
   By union bound over all $n^2$ windows,
   $$n^2 \cdot x^{-(K+1)\varepsilon/3} \le 4 x^{4 + 16\varepsilon - (K+1)\varepsilon/3} \le 4 x^{-1} < \tfrac{1}{2} \qquad \text{for } K = \lceil 15/\varepsilon \rceil + 50.$$
4. **Cluster decomposition (`winClusters_K`):** Taking $L_w' \ge K j_A(l) + 1$, every thick letter lies in a maximal cluster of **$\le K$ thick letters** separated from all other clusters by at least $j_A(l)$ consecutive thin letters (`CutsOK`), with arc length $\ell_{\max} \le K j_A(l) + 1 = O_\varepsilon(\log x)$ and `roMax ≤ K`.

### 2.3 Exact Audit of What Wach Modules Already Have vs. What Needs Extending for `ro ≤ K`

Auditing [`LocalTheoryWindows.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/LocalTheoryWindows.lean#L72-L120), [`ArcLiftingSetup.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/ArcLiftingSetup.lean#L392-L450), [`DescentEstimateDownUp.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs/DescentEstimateDownUp.lean#L265-L485), [`LevelsModConstIffOfDownDown.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs/LevelsModConstIffOfDownDown.lean#L540-L635), and [`LinExtEqZeroOfMemExt.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs/LinExtEqZeroOfMemExt.lean#L502-L758) reveals:

- **Already proved for arbitrary `roMax = K`:**
  - `ArcAt` / `ArcAtCore` ([`LocalTheoryWindows.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/LocalTheoryWindows.lean#L103-L119)): $\kappa \le C\big((G' + \operatorname{ro}_{\max} S + 1)(\ell_{\max}+1) + (\operatorname{ro}_{\max}+1)\log_l h\big)$ and $|\text{cls}| \le \sum_c m \cdot \operatorname{ro}(c) \cdot (\ell(c)+1)$ — merely scales constants by $K = O(1/\varepsilon)$, which is completely absorbed into $x^\varepsilon$!
  - `UnivCore` and `KillerKap` ([`ArcLiftingSetup.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/ArcLiftingSetup.lean#L392-L450)): already parameterized by arbitrary `ro`.
  - `down_scalar` ([`DescentEstimateDownUp.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs/DescentEstimateDownUp.lean#L265-L275)): already holds for arbitrarily many `up` and `down` levels, yielding $\varpi^k w - \big(\prod_{s \in U} p_s^{b_s}\big)\varphi(d) \in (p_{s_*}^{b_{s_*}})$ for every $s_* \in D$.
  - Whenever $s_{\max} = \max(\text{th}) \in D$ (`down`), the Weierstrass degree of *all* earlier `up` letters sums geometrically:
    $$\sum_{u \in U} b_u l^u \le (b + \eta)\frac{l^{s_{\max}} - 1}{l - 1} < \frac{b + \eta}{l - 1} l^{s_{\max}} < b_{s_{\max}} l^{s_{\max}} \qquad (l \ge 11),$$
    **independent of $K$!** Similarly, at a root $\zeta_{s_{\max}}$ of $p_{s_{\max}}$, all earlier levels $s < s_{\max}$ contribute valuation $\sum_{s < s_{\max}} b_s l^{s - s_{\max}} \le \frac{b + \eta}{l - 1} \le \frac{b}{9}$, independent of $K$!
- **The single remaining local lemma to extend (`WordOK` / `ConstLift` for mixed alternating patterns like `up(s_0), down(s_1), up(s_2)`):**
  - Currently [`LocalTheoryWindows.WordOK`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/LevelLetterCocycles/LocalTheoryWindows.lean#L72-L85) handles all-`down`, all-`up`, one-`down`-above-`up`s, and one-`up`-above-`down`s; [`ThmEFull.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/DistinguishedUnitIdeals/DistinguishedOrderProofs/ThmEFull.lean#L19-L31) hardcodes the 5 cases with `ro ≤ 2`.
  - **Numerical $p$-adic test in $\mathbb{Z}_l[X]/(p_1^b)$** (with exact Lubin–Tate/Wach model $\varphi(X) = X(X+l)^{l-1}$, $p_s = \varphi^s(X) + l$, $s_0 = 0, s_1 = 1, s_2 = 2$):
    - For `l = 3, b = 2, 3, 4, 5`: $v_l(p_2^b \bmod p_1^b) = 2, 3, 3, 4$ whereas $v_l(p_0^b p_2^b \bmod p_1^b) = 2, 3, 4, 4$ (difference $\in \{0, 1\} \le \lceil b/l \rceil$).
    - For `l = 5, b = 2, 3, 4, 5`: $v_l(p_2^b \bmod p_1^b) = v_l(p_0^b p_2^b \bmod p_1^b) = 2, 3, 4, 5$ (difference $= 0$).
    - For all tested $l, b$: $v_l(p_0^b \bmod p_1^b) = 0$ (since $p_0^b$ is monic of degree $b < b l$).
  - This confirms that adding earlier `up` levels $s_0 < s_1$ perturbs the `consts_UD` valuation at $s_1$ by at most $O(b/l)$, while `Kills W F (c - u) (letπ ^ sA)` already holds at *every* thick `up` letter $u \in U$ with $s_A/(l-1) \le C b / l \ll b_u$. Thus replacing Behrend reduces cleanly to a purely local inductive peeling lemma for `ConstLift` / `WordOK` on $r \le K$ thick levels (no global or additive-combinatorial input whatsoever!).

---

## 3. Complete Anatomy of the Iwasawa Tower $H_e$ ($n = 2^e \asymp x^{2+8\varepsilon}$)

### 3.1 Exact Exponent Polytope: Why $n \asymp x^{2+8\varepsilon}$

Write $n = |H_e| = 2^e = x^\alpha$, $f = [F:\mathbb{Q}] = 2n$, $m = x^\mu$, $k = x^\kappa$, $L = x^\varepsilon$. Direct audit of [`DataParams.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalRingCardinality/DataParams.lean#L11-L169), [`PairRowIffQdRows.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L28-L33), [`ThickAverageLoss/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L81-L128), and [`StandingNumericalData.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean#L106-L136) gives the exact linear constraints on $(\alpha, \mu, \kappa)$ as $\varepsilon \downarrow 0$:

| Constraint | Source in `lean/src/` | Inequality | Leading Exponent Relation |
|---|---|---|---|
| Theta-chain length (`copy`, `frame`) | [`ThickAverageLoss/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L116) | $m \ge x^{1/2 - \varepsilon}$ | $\mu \ge \tfrac{1}{2}$ |
| Short-order top primes (`phic_G`, `adm3`) | [`ThickAverageLoss/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L119), [`SmallOrderPrimes.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/GrowthBounds/SmallOrderPrimes.lean#L100-L103) | $x / H \le x^{1/2 + \varepsilon}$ | $\alpha \ge \tfrac{1}{2}$ |
| Boolean word count (`k_low`, `GamP`) | [`DataParams.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalRingCardinality/DataParams.lean#L137), [`ShiftedParametersOfDifferingLetters.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/BruhatCellsKronecker/ShiftedParametersOfDifferingLetters.lean#L600-L621) | $C m^{j_G} f L x^\varepsilon \le k$ ($f = 2n$, $j_G = 5$) | $\kappa \ge j_G \mu + \alpha$ |
| Short-order inert primes (`ShortOrdSq`, `k_up`, `radius_ge_sqrt_ratio`) | [`DataParams.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalRingCardinality/DataParams.lean#L139-L141), [`ThickAverageLoss/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/ThickAverageLoss/Statement.lean#L120) | $k \le m (n x^{-\varepsilon})^2 \le x^{1/2} n^2 x^{-\varepsilon}$ | $\kappa \le \mu + 2\alpha$ |
| Standing degree assumption | [`StandingNumericalData.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/SharpRestriction/CuspSpanNormBounds/StandingNumericalData.lean#L118) | $m^4 \le f = 2n$ | $\alpha \ge 4\mu$ |
| `SizeLa` / `SizeRho` (`rho_le`) | [`DataParams.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/LocalRingCardinality/DataParams.lean#L51-L52), [`ExistsExplicitParameters.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Proofs/GlobalInterpolation/ExistsExplicitParameters.lean#L49-L57) | $2 n \delta_1 x^\varepsilon \Lambda_G \le k / x^2$? ($k \gtrsim n x^2$) | $\kappa \ge 2 + \alpha$ |

**Algebraic cancellation (`hExp = (jG - 1)/2`):** Combining `k_low` ($\kappa \ge j_G \mu + \alpha$) with `radius_ge_sqrt_ratio` ($\kappa \le \mu + 2\alpha$) cancels one factor of $n$:
$$\alpha \ge (j_G - 1)\mu = \frac{j_G - 1}{2} = 2 \qquad (\text{at } j_G = 5,\; \mu = \tfrac{1}{2}),$$
independently reproducing $\alpha = 2$ even if `m^4 ≤ f` is removed! Solving the LP across relaxation scenarios yields:
- **Current proof ($j_G = 5$):** $\alpha_{\min} = 2$ ($\mu = 0.5$, $\kappa = 4.5$, matching `RankVal` in [`PairRowIffQdRows.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/PairRowIffQdRows.lean#L28-L31)).
- **If `GamP` is improved to $j_G = 3$ and `m^4 ≤ f` + `SizeOrders` removed (keeping `SizeRho`):** $\alpha_{\min} = 1.5$ (blocked by `SizeRho` + `cap2`: $2 + \alpha \le 0.5 + 2\alpha \implies \alpha \ge 1.5$).
- **If `GamP` is improved to $j_G = 2$ and `m^4 ≤ f`, `SizeOrders`, `SizeRho` all removed:** $\alpha_{\min} = 0.5$ — hitting the **hard Chebotarev floor** `phic_G` ($\alpha \ge 1/2$).

### 3.2 Exact Numerical Verification of `IncomingBound.lean` at Small Orbit Lengths $d$

In [`IncomingBound.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/IncomingBounds/IncomingBound.lean#L18-L92), the LP on $\mathbb{Z}/d\mathbb{Z}$ ($d \ge 2$ even, $l \ge 3$) minimizes $\sum_s D_s \sigma_s$ subject to $0 \le \sigma_s \le 1$ and $l^i \sigma_s + \sigma_{s+i} \ge 1$ for odd $i < d$.
- At the **smallest** possible even orbit length $d = 2$, the dual polytope in $[0,1]^2$ has exact vertices $\big(\frac{1}{l+1}, \frac{1}{l+1}\big)$, $(1, 0)$, $(0, 1)$, and $(1, 1)$.
- Exact evaluation for $l \in \{3, 5, 11\}$ across uniform, spike, and threshold ratio vectors $D = (l, 1), (l+1, 1), (2l, 1)$ confirms `LemmaFb` ($F_{\text{num}} \ge \rho \sum D_s$) and `IncomingBound` ($\sum_{\sigma_s \ge 2/l} D_s \le \frac{1}{l} \sum D_s$) hold tightly at $d = 2$ (attaining $\frac{1}{l+1} < \frac{1}{l}$ at the $D = (l+1, 1)$ threshold).
- **Conclusion:** The `IncomingBound` LP imposes **zero** growth condition on the tower degree $n$ (it only requires $d \ge 2$ even).

### 3.3 Why Abelian Alternatives Fail & Why the Two-Stage Bootstrap Does Not Shrink $\alpha = 2$

1. **Uniqueness of the 2-power tower $H_e = \mathbb{Z}/2^e\mathbb{Z}$:**
   - **Odd-order factors** (e.g. $\mathbb{Q}(\zeta_{p_0^e})^+$ or prime conductor $r \equiv 3 \pmod 4$) violate `CInPhi` ([`BehrendSets/StatementE.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/BehrendSets/StatementE.lean#L25-L30), [`FrobeniusOrbits/Statement.lean`](file:///home/marcus/GitHub/mbintz/incandescent/lean/src/Formalism/FrobeniusOrbits/Statement.lean#L108)): any element $h \ne 1$ of odd order $d$ satisfies $(c_0, h)^d = (c_0, 1) = c$, making inert primes stay inert in $E/F$ and breaking `Even (orderOf h_l)`.
   - **Multiquadratic fields** have exponent $2$, so $\operatorname{ord}(h_p) \le 2$ for every prime $p$, destroying both `adm1` ($\operatorname{ord}(h_p) \ge x^{\varepsilon/4}$) and `ShortOrdSq`.
   - **Prime conductors $r = 2^a s + 1$** lose Lifting-The-Exponent (`OrdIff`): the congruence $l^{2^{j_0}} \equiv \pm 1 \pmod r$ has up to $2J$ roots scattered across $[1, r)$ as small as $r^{1/J}$, breaking `ShortOrdLarge` ($l \ge 4n/J - 1$). Even choosing $r \in [N, 2N]$ to avoid small primes $l \le R_0$ only reaches $R_0 \approx N / (J \log N)$ and gives a worse `SumSq` tail than $2^{e+2}$'s $O(J^2 \log n / n^2)$.
2. **Averaging over a family of bounded-degree CM fields ($f_i \le F$):**
   - Because `phic` enters as a non-negative upper bound $\text{phic}_i \ge c \frac{x \log x}{H_i}$ (Chebotarev density $1/H_i$ of primes splitting completely in $F_{1,i}$), any convex average satisfies $\sum_i w_i \text{phic}_i \ge c \frac{x \log x}{F} \gg x^{1/2}$ whenever $F = o(x^{1/2})$. And `m_i ≤ F^{1/4}` fails $m_i \ge x^{1/2-\varepsilon}$ identically unless $F \ge x^{2-4\varepsilon}$.
3. **Two-stage zero-free strip bootstrap on `ThinScales`:**
   - Suppose Stage 1 gives a zero-free strip $\operatorname{Re}(s) > 1 - \delta$ (for **all** characters of $E$, not just $\zeta$), allowing a polynomial thin cutoff $X' = x^B$ (with a polynomial $\theta = x^{-B\delta}$ rather than $\exp(-c x^{\varepsilon/8})$).
   - That shrinks $b'/b = x / X'$, relaxes the *upper* bound $n \le \sqrt{b}/X'$ from $w'' \ge \sqrt{b}$, and saves $O(\varepsilon)$ in `ShortOrdLin`'s $(\log X'')^2$ factor.
   - It **does not touch** any of the four barriers forcing $\alpha = 2$ (`k_low` vs `radius_ge_sqrt_ratio`, `m^4 ≤ f`, `SizeRho`, `phic_G`). Thus a two-stage bootstrap reduces the leading tower exponent by **zero** unless paired with a deep automorphic reduction of $j_G$ in `GamP` AND elimination of `m^4 ≤ f`, `SizeRho`, and `SizeOrders` (which even in the best case still stops at the Chebotarev wall $n \ge x^{1/2 - \varepsilon}$).
