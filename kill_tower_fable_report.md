# Track 2 report: the Behrend set

## Verdict

- **Behrend's theorem can go; a 3‑AP‑free thick set cannot**, unless the local crystalline theorems are extended. `BehrendBound`/`ThickSet`/`SpaceExists`/`HostThickExists` can be replaced by an explicit fixed‑dimension paraboloid set with a ten‑line proof (Theorem 1).
- **Interval and Bernoulli $T_2$ both fail**, and averaging over $u_0$ does not rescue either. Bernoulli fails unconditionally at every inert prime.
- **The 1‑step idea is half right.** For primes $l\ge l_A$ the proof already uses only "no three consecutive thick letters". The window $L_w$ exists only for inert primes $l<l_A$.
- **If Astra gets the tower degree down to $n\le x^{\varepsilon}$, Behrend dies for free**: $T_2=\{0\}$ satisfies everything.

I read Lean statements only. I did not compile anything or check any proof for soundness, and nothing here endorses the overall RH claim. No repository files were edited.

## 1. Why the proof uses a structured $T_2$

The chain, with the exact consumers:

1. `Choices.second_set_range` and `second_set_no_relation : NoRel T2 Lw` (`lean/src/Development/AutomorphicArithmetic/CoprimeRanks/SecondSetNoRelation.lean:51-52`) feed `hostThickOrbit` in `…/SatakeParameters/AtMostTwoThickInWindowLongOrbit.lean:30`, giving `WindowTwo` for orbits of order $>4L_w$.
2. `WindowTwo th L → Clusters th j` for $2j+1\le L$ (`CyclicWordMarkedClustersOfAtMostTwoInWindow.lean:21`), then `pageWord.HypA (depth L l)` (`TwistedDualPageWordClusterDepthLongOrbitStatement.lean:8`).
3. `Clusters` is a hypothesis of the local colength bound `CorA` (`lean/src/Formalism/SharpRestriction/LevelLetterCocycles/CrystallineMapLemmas.lean:103-116`, also `WachCoordinates.lean:146-161` with `ThickLe2` at `:21`). Its conclusion has the term $h/(l-1)^{j+1}$ with $h\approx b$.
4. For primes outside row B the proof uses `ThmB` clause 1 (`CrystallineMapLemmas.lean:89-92`): alternating word, **no three consecutive thick letters**, loss $h/l^2$.
5. These colengths become `len l ≤ C x^ε k b / l²` and the `Ld` slot (`lean/src/Formalism/ThickAverageLoss/Statement.lean:107-110`), then `LossBound`, then `topExcess ≤ Err`.

Three facts explain the asymmetry with `TT`:

- **The main term sees only the density of $T_2$.** `ThickPartTranslateMean` (`GrowthBoundGivesRiemannHypothesis.lean:43-48`) and `TranslateMean` use only $|T_2|$; any set of density $\delta_2$ gives $\delta_2\,b/2\cdot G_{\mathrm{sig}}$. All structure is demanded by the upper‑bound side.
- **Tops are cheap and tolerant.** `topsChoice` (`…/GlobalInterpolation/BernEqProd.lean:156-185`) allows up to $K_G=O(1/\varepsilon)$ tops per window of $L_2\le 1242/\varepsilon$ and bad tops with probability $C_b x^{-2}$. A bad top costs about $a_t\log p/p$, with no factor $k$.
- **Thick places carry the bulk $(k-1)b$ with $k\ge xm$.** No slot exists for an exceptional thick letter. The only slot for the cruder $kb/l^2$ loss is `Ld`, which requires $l>R$ and $\sum\log l/l^2\le x^{\varepsilon}/(HR)$ (`phi_i`, `phi_ii`). Only short‑order primes meet that, via `ShortOrdSq`.

The jet side is not the obstruction: `InertBd` (`…/Definitions/Jets/DepthNumbersThresholdEq.lean:148-151`) bounds the content by `Fnum` for an arbitrary weight profile. The obstruction is the crystalline side (`ThmB`, `CorA`, `ArcAt`).

A structural reason for "at most two" (my own analysis of `IsFlow`, not stated in Lean):

**Proposition 0.** Let $d$ be even, $l\ge3$, and let $D$ equal $B$ on a set of thick letters and $0$ elsewhere.
- For a pair $\{s,s+e\}$ with $e$ odd: $\mathrm{maxFlow}\in[B/l^{e},\,B/l^{e}+B/l^{d-e}]$.
- For a chain $\{s,s+1,s+2\}$: $\mathrm{maxFlow}\in[2B/l-B/l^2,\ 2B/l-B/l^2+B/l^{d-1}]$.

*Proof (chain).* Feasible flow: $x_{s,1}=B/l$, $x_{s+1,1}=(B-B/l)/l$. Dual certificate: $\sigma_{s+2}=l^{-(d-1)}$, $\sigma_{s+1}=1/l$, $\sigma_s=(1-1/l)/l$, $\sigma=1$ elsewhere; all `IsDual` constraints hold. The pair case is the same with one arc. ∎

So `Fnum` is pairwise additive on clusters of size at most 2 and first fails on a 3‑chain by exactly $B/l^{e_1+e_2}$. That is a main‑term‑sized quantity that `AskMainBalance` does not contain.

## 2. The replacement that works

**Theorem 1 (explicit `NoRel` set).** Let $L,d\ge1$, $A\ge2$, $Q:=2L(A-1)+1$, and
$$T:=\Big\{\,s(a)=\sum_{i=1}^{d}a_iQ^{i-1}+Q^{d}\sum_{i=1}^{d}a_i^2\ :\ a\in\{0,\dots,A-1\}^d\Big\}.$$
Then:
1. $|T|=A^d$.
2. $\max T<Q^d(1+d(A-1)^2)\le (2LA)^d\,dA^2$.
3. `NoRel T L` holds (`HostThickExists.lean:13-16`).

Hence if $4L(2LA)^d dA^2\le n$, then `∀ s ∈ T, 4*L*s < n` and `HostThickOrbit` (`HostThickExists.lean:22-29`) applies verbatim.

*Proof.* (1) and (2): the first $d$ digits are less than $Q$, so $s$ is injective, and $\sum_{i\le d}a_iQ^{i-1}<Q^d$.

(3): Suppose $j(s_2-s_1)=i(s_3-s_1)$ with $0<|i|,|j|\le L$, $i\ne j$. Put $\beta=j$, $\gamma=-i$, $\alpha=-(\beta+\gamma)\neq0$. Write $a^{(r)}$ for the digit vector of $s_r$ and
$$c_\nu=\beta\big(a^{(2)}_\nu-a^{(1)}_\nu\big)+\gamma\big(a^{(3)}_\nu-a^{(1)}_\nu\big),\qquad c_{d+1}=\beta\big(|a^{(2)}|^2-|a^{(1)}|^2\big)+\gamma\big(|a^{(3)}|^2-|a^{(1)}|^2\big).$$
The relation reads $\sum_{\nu\le d}c_\nu Q^{\nu-1}+c_{d+1}Q^d=0$ with $|c_\nu|\le 2L(A-1)<Q$. Reducing mod $Q$ repeatedly gives $c_1=\dots=c_d=0$, then $c_{d+1}=0$.

Since $\alpha+\beta+\gamma=0$ with all three nonzero, after a global sign two coefficients $\lambda,\mu$ are positive and the third is $-(\lambda+\mu)$. With $\theta=\lambda/(\lambda+\mu)$ one digit vector is $\theta p+(1-\theta)q$ and its square norm is $\theta|p|^2+(1-\theta)|q|^2$. The identity $\theta|p|^2+(1-\theta)|q|^2-|\theta p+(1-\theta)q|^2=\theta(1-\theta)|p-q|^2$ forces $p=q$. So $s_1=s_2=s_3$, contradicting distinctness. ∎

(With $Q=4L(A-1)+1$ the same proof gives `BehrendFree (2L)`.)

**Corollary (parameters).** Let $\Gamma=4dL(2L)^d$ and $A=\lfloor (n/\Gamma)^{1/(d+2)}\rfloor\ge2$. Then $|T|/n\ \ge\ 2^{-d}\,\Gamma^{-1}\,n^{-2/(d+2)}$.

Check against the Lean sizes:
- $n_0\le C_o\,x^{2+8\varepsilon}$ and $L=$ `Lwv` $\le(4084+60/\varepsilon)\log x$ (`ExistsThinPrimeSet.lean:17-18`, `PairRowIffQdRows.lean:26`).
- Take $d=\lceil 8/\varepsilon\rceil$. Then $n_0^{2/(d+2)}\le C_o\,x^{0.54\varepsilon}$ for $\varepsilon<1/52$, and $2^d\Gamma\le(4L)^{d+2}\le x^{0.2\varepsilon}$ for $x\ge x_0(\varepsilon)$.
- So $|T|\ge x^{-0.75\varepsilon}n_0/C_o$. With $n=o\cdot n_0$ and $o\le x^{\varepsilon/100}$ (`QuadraticLogDerivCongr.lean:1802`), this gives $x^{-\varepsilon}n\le|T|$.

**Where it drops in.**
- It supplies conjuncts 1, 2, 4, 5, 6 of `exists_thick_set_sizes` (`ExistsThinPrimeSet.lean:30-31`) and the fields `second_set_range`, `second_set_no_relation`.
- It does **not** prove conjunct 3 (the $\exp(-C\sqrt{\log n\log L})$ form), because its density is polynomial rather than sub‑polynomial.
- That form is consumed only by `winN'` (`…/GlobalSchurBounds/QuadraticLogDerivCongr.lean:1731-1734`), whose entire conclusion is `x^(-eps) ≤ T2.card / n`, which the Corollary proves directly.
- So `BehrendBound`, `ThickSet`, `SpaceExists`, `HostThickExists`, `secondSet_card_lower_bound`, `CT2` and `winN'` become deletable. `SizeWindows` (`x^(-ε) ≤ nT2/n`) is met unchanged.

## 3. The naive candidates

**Lemma 2 ($u_0$‑invariance).** For fixed $T,h,a,b$, the count $\#\{t:\ t,\ t+ah,\ t+bh\in T+u_0\}$ does not depend on $u_0$ (substitute $t\mapsto t+u_0$). So every translate has the same number of bad windows at every prime. The $u_0$‑average in `topExcess` (line 52) fixes the position of $T_2$ relative to tops and kills characters nontrivial on $H$; it cannot dilute internal configurations.

**Lemma 3 (three in a row is fatal).** Let $l$ be inert with step $h$, $\mathrm{ord}(h)\ge3$, and $x,x+h,x+2h\in T_2+u_0$. Inert words alternate up/down (`OrbitParity`, `lean/src/Formalism/RankGapBounds/ConjInOrbit.lean:16-17`). Then:
- `ThmB` clause 1 fails its no‑three hypothesis.
- `Clusters j` fails for every $j\ge1$ at $t=x+2h$ (both alternatives, checked directly).
- `ArcAt.WordOK` (`LocalTheoryWindows.lean:72-85`) fails: no cut can separate adjacent thick letters (`CutsOK:54`), and the types U,D,U match none of its four patterns.

So no local statement in the repository applies to that orbit.

| Candidate | Verdict | Mechanism |
|---|---|---|
| Bernoulli $T_2$, density $\delta\ge x^{-\varepsilon}$ | Fails unconditionally | For each $h$ of order $\ge3$ there are $\ge n/5$ disjoint triples, so $P(\text{no 3‑AP of step }h)\le(1-\delta^3)^{n/5}\le e^{-x^{2-3\varepsilon}/5}$. A union bound over $h$ shows Lemma 3 applies to **every** long‑orbit inert prime. Deleting bad triples needs $\delta\ll 1/(L\sqrt n)$, far below $x^{-\varepsilon}$. |
| Constant $\delta_2$ | Fails | $T_2$ must be 3‑AP‑free for every long‑order step; Roth forces $\delta_2\to0$. |
| Interval $[0,\delta_2n)$ | Fails (conditionally provable, see below) | Every $h$ with $\lvert h\rvert<\delta_2n/2$ gives three consecutive thick letters. Small‑order steps force $l\ge 2^{e}/L_w$ (`ShortOrdLarge`), but small‑$\lvert h\rvert$ steps do not force $l$ large. |
| Coset of $2^a\mathbb Z$, $2^a\le x^{\varepsilon}$ | Fails | Primes $l\equiv\pm1 \bmod 2^{a+2-c}$ see period‑$\le j$ or all‑thick words: no cuts exist and the pattern is DUDU. |
| 1‑step control only | Works for $l\ge l_A$, fails below | See §4. Still needs 3‑AP‑freeness. |

**The interval, precisely.** Under GRH for the characters mod $2^{e+2}d$, the bad inert primes have density about $\delta_2/2$ from $Y\ge x^{7\varepsilon}$ on (interval Fourier coefficients sum to $O(\log n)$; $\log d\le x^{\varepsilon}$). Then $\sum_{\text{bad}}\log l/l^2\gtrsim x^{-8\varepsilon}$, against the allowed $x^{\varepsilon}/(HR)\le x^{-1+3\varepsilon}L_w$. Unconditionally I cannot exhibit a small bad prime. But the proof would have to prove there are none below about $H$, and that statement contradicts the theorem being proved.

**Even with a hypothetical general local theorem**, Bernoulli $T_2$ would create about $n\delta_2^3$ chains per step, each adding $kb/l^{2}$ by Proposition 0. Relative to the signal this is $\gtrsim k\delta_2^2x^{-\varepsilon/5}/(\delta_1 m x^{1/2})\ge x^{1/2-3\varepsilon}$. This step is my estimate, not something stated in Lean.

## 4. Where $L_w$ comes from

- `lA = k x^ε /(m·de2)` (`lean/src/Formalism/LocalRingCardinality/DataParams.lean:36`) is defined so that $\sum_{l\ge l_A}\log l\cdot kb/l^2\approx kb/l_A$ sits inside the budget. For those primes only `ThmB` and "no three consecutive" are used.
- For $l<l_A$ the $1/l^2$ loss sums to about $kb\,x^{-\varepsilon/5}$, which exceeds the budget by at least $x^{1/2-2\varepsilon}$. So `CorA` needs depth $j$ with $(l-1)^j\ge l_A$ (`jA`, `…/GaloisGeometry/NotDvdCondN.lean:44`; `Lw_j`, `DataParams.lean:169`), i.e. window $2j+2$.
- The intuition "$\sum_{p>p_0}\log p/p^3$ is tiny" is right for top‑term tails (the `x/p0²` term in `serv_G`). It does not cover the bulk, which is larger by the factor $k$.
- `IncomingBound.lean` lines 107–126 (`dTop`, `topTerm`, `baseTerm`, `Wcap`) concern the **tops**: `TT` there is the top set, not $T_2$. `dTop` says a top's flow is exhausted at its nearest odd‑distance top. The LP handles top–top interaction exactly, which is why tops can be random.

**Possible simplification (not fully verified).** `split_tie` (`DataParams₂.lean:129`) with `splitBound := ⌊x^(eps/5)⌋` makes every odd prime $\le x^{\varepsilon/5}$ split in $K$. Every row‑B prime is therefore $>x^{\varepsilon/5}$ and $j_A(l)=O(1/\varepsilon)$. `Lw_j` quantifies over all $l\ge11$, which is what forces $L_w\asymp\log x$. Restricting it to inert primes would give $L_w=O(1/\varepsilon)$. The caveat is `weightLength_ge_depth : 10*j0+20 ≤ Lw` with $j_0\ge\log_5(nN/m)$ (`DataParams₂.lean:122-124`); I did not trace where $j_0$ is used.

## 5. The tower

- **$T_2$ itself places no lower bound on $n$.** If $n\le x^{\varepsilon}$, then $T_2=\{0\}$ has `NoRel` vacuously and density $1/n\ge x^{-\varepsilon}$. Behrend‑type structure is needed exactly because $n\gg x^{\varepsilon}$.
- **What forces $n$ large is elsewhere** (Astra's track), in `ThickAverageLoss/Statement.lean`:
  - `phic ≤ C x^ε x/H` with `x ≤ K x^(1/2+ε) H` (`:93`, `:119`).
  - `k·de2 ≤ K x^(1/2+ε) de1·H·R` (`:120`), the short‑orbit term.
  - `k_low : m^5·f ≤ k` (`DataParams.lean:137`), which is why $n\approx x^{2+8\varepsilon}$.
  - `topsChoice` needing orders $\ge x^{\varepsilon/4}$.

## Open item that would truly kill 3‑AP‑freeness

Extend `ArcAt.WordOK` / `ThmB` clause 1 to alternating arcs containing mixed‑type thick runs (UDU), and add the second‑order term of Proposition 0 to the main‑term identity. Nothing in the repository does this, and I do not have a proof.
