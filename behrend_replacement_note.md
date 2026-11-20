# Replacing the Behrend Set with an Explicit Paraboloid

![Replacing Behrend with a Paraboloid](./behrend_kill_minimal.png)

In `remark.pdf` (item 19, footnote 7) of Alpoge and Claude's Lean 4 RH/GRH formalization, a Behrend-type 3-AP-free set $T_2 \subset H_e = (\mathbb{Z}/2^{e+2}\mathbb{Z})^\times / \{\pm 1\} \cong \mathbb{Z}/2^e\mathbb{Z}$ is used to construct the thick places of the host CM field, with the remark:

> *"This is the sort of trick that intuitively to me is obviously going to be unnecessary."*

Auditing the Lean sources (`lean/src/`) shows that **Behrend's theorem itself drops out immediately** via an 8-line explicit fixed-dimension paraboloid, with zero downstream changes to the Wach-module or `IncomingBound` machinery.

*(Scope note: this is a mathematical and Lean-interface audit only. No repository files were edited, no Lean build was run, and nothing here is a verification of the overall RH claim.)*

---

## 1. What the Lean Proof Actually Consumes from $T_2$

In the host construction, $T_2 \subset \mathbb{N}$ is required to satisfy three conditions for window width $L = \texttt{Lwv} \le (4084 + 60/\varepsilon)\log x$ and cyclic order $n_0$ (with $n = o \cdot n_0 \asymp x^{2+8\varepsilon}$ and $o \le x^{\varepsilon/100}$):

1. **Range (`second_set_range`):** $\forall s \in T_2,\; 4 L s < n_0$.
2. **No 3-term linear relations (`second_set_no_relation`, `NoRel T2 L`):** for all $i, j \in \mathbb{Z}$ with $0 < |i|, |j| \le L$ and $i \neq j$, and all distinct $s_1, s_2, s_3 \in T_2$,
   $$j(s_2 - s_1) \neq i(s_3 - s_1).$$
3. **Density:** $|T_2|/n \ge x^{-\varepsilon}$.

Although `HostThickExists` / `SpaceExists` prove Behrend's sub-polynomial lower bound
$$|T_2| \ge \frac{n_0}{L} \exp\!\left(-C\sqrt{\log n_0 \log L}\right),$$
its **only** consumer (`winN'` in `lean/src/Formalism/SharpRestriction/GlobalSchurBounds/QuadraticLogDerivCongr.lean:1731-1805`) immediately weakens it to the polynomial density $|T_2|/n \ge x^{-\varepsilon}$ required by `SizeWindows`.

Because $\varepsilon > 0$ is fixed before $x \to \infty$, Behrend's pigeonholing over variable-dimension spheres is overkill: a fixed-dimension base-$Q$ paraboloid (Salem–Spencer / Moser style) gives polynomial density $n_0^{-O(1/d)}$ with $d = \lceil 8/\varepsilon \rceil$, which already beats $x^{-\varepsilon}$.

---

## 2. Explicit Replacement Theorem

**Theorem.** Let $L, d \ge 1$, $A \ge 2$, and set $Q := 2L(A - 1) + 1$. Define
$$T \;:=\; \left\{\, s(a) \;=\; \sum_{i=1}^{d} a_i Q^{i-1} \;+\; Q^{d}\sum_{i=1}^{d} a_i^{2} \;:\; a \in \{0, \dots, A-1\}^{d} \,\right\}.$$
Then:
1. $|T| = A^d$.
2. $\max T < d\,(2L)^d A^{d+2}$.
3. `NoRel T L` holds.

In particular, setting $\Gamma := 4 d L (2L)^d$ and $A := \lfloor (n_0 / \Gamma)^{1/(d+2)} \rfloor \ge 2$ gives $\forall s \in T,\; 4 L s < n_0$ and `NoRel T L`, so `HostThickOrbit` (`WindowTwo` and `OrbitOne`) applies verbatim.

### Proof

**(1) Size:** Since $0 \le a_i \le A - 1 < Q$ for every $i = 1, \dots, d$, the first $d$ base-$Q$ digits uniquely recover $a \in \{0, \dots, A-1\}^d$. Hence $a \mapsto s(a)$ is injective and $|T| = A^d$.

**(2) Range:** Since $2L(A-1) = Q - 1$, the lower $d$ digits satisfy $\sum_{i=1}^d a_i Q^{i-1} \le \frac{A-1}{Q-1}(Q^d - 1) < Q^d$. Also $1 + d(A-1)^2 \le d A^2$ (for $d \ge 1, A \ge 2$) and $Q = 2L(A-1) + 1 \le 2LA$ (for $L \ge 1$). Therefore
$$\max T \;<\; Q^d\big(1 + d(A-1)^2\big) \;\le\; (2LA)^d \cdot dA^2 \;=\; d\,(2L)^d A^{d+2}.$$
Multiplying by $4L$ yields $4 L \max T < \Gamma A^{d+2} \le n_0$.

**(3) `NoRel T L`:** Suppose $s_1, s_2, s_3 \in T$ satisfy $j(s_2 - s_1) = i(s_3 - s_1)$ with $0 < |i|, |j| \le L$ and $i \neq j$. Write $a^{(r)}$ for the digit vector of $s_r$, and set $\beta = j$, $\gamma = -i$, $\alpha = -(\beta + \gamma) \neq 0$. Defining
$$c_\nu := \beta\big(a_\nu^{(2)} - a_\nu^{(1)}\big) + \gamma\big(a_\nu^{(3)} - a_\nu^{(1)}\big) \quad (1 \le \nu \le d), \qquad c_{d+1} := \beta\big(\|a^{(2)}\|^2 - \|a^{(1)}\|^2\big) + \gamma\big(\|a^{(3)}\|^2 - \|a^{(1)}\|^2\big),$$
the relation becomes $\sum_{\nu=1}^d c_\nu Q^{\nu-1} + c_{d+1} Q^d = 0$. For each $1 \le \nu \le d$,
$$|c_\nu| \;\le\; (|\beta| + |\gamma|)(A - 1) \;\le\; 2L(A - 1) \;<\; Q.$$
Reducing modulo $Q$ inductively forces $c_1 = \dots = c_d = 0$, leaving $c_{d+1} Q^d = 0$, hence $c_{d+1} = 0$.

Since $\alpha + \beta + \gamma = 0$ with all three nonzero, after negating if necessary two coefficients $\lambda, \mu$ are positive and the third is $-(\lambda + \mu)$. Setting $\theta := \lambda/(\lambda + \mu) \in (0, 1)$, the vanishing of $c_1, \dots, c_d, c_{d+1}$ states that one digit vector equals $\theta p + (1-\theta) q$ while its squared norm equals $\theta\|p\|^2 + (1-\theta)\|q\|^2$. By strict convexity,
$$\theta\|p\|^2 + (1-\theta)\|q\|^2 - \|\theta p + (1-\theta)q\|^2 \;=\; \theta(1-\theta)\|p - q\|^2 \;=\; 0 \;\implies\; p = q,$$
so $s_1 = s_2 = s_3$. $\blacksquare$

*(Remark: taking $Q := 4L(A-1) + 1$ yields the `BehrendFree (2L)` variant by the identical proof.)*

### Density Check Against Lean Scales

Take $d := \lceil 8 / \varepsilon \rceil$ (with $0 < \varepsilon < 1/52$). From `PairRowIffQdRows.lean:26-29`, `ExistsThinPrimeSet.lean:17-18`, and `QuadraticLogDerivCongr.lean:1802`:
- $n_0 \le n \le 2 x^{2+8\varepsilon}$, $o = n/n_0 \le x^{\varepsilon/100}$, and $L \le (4084 + 60/\varepsilon)\log x$.
- For $x \ge x_0(\varepsilon)$, $A \ge \frac{1}{2}(n_0 / \Gamma)^{1/(d+2)} \ge 2$, so
  $$|T| \;=\; A^d \;\ge\; 2^{-d} \Gamma^{-\frac{d}{d+2}}\, n_0^{1 - \frac{2}{d+2}} \;\ge\; 2^{-d} \Gamma^{-1}\, n_0^{-\frac{2}{d+2}} \cdot n_0.$$
- Since $\frac{2}{d+2} < \frac{\varepsilon}{4}$ and $\varepsilon < \frac{1}{52}$, we have $n_0^{2/(d+2)} \le (2 x^{2+8\varepsilon})^{\varepsilon/4} < 2 x^{0.54\varepsilon}$.
- Meanwhile $2^d \Gamma = 4 d L (4L)^d = O_\varepsilon((\log x)^{d+1}) \le \frac{1}{2} x^{0.21\varepsilon}$ for $x \ge x_0(\varepsilon)$.

Combining these gives
$$\frac{|T|}{n} \;=\; \frac{|T|}{o \cdot n_0} \;\ge\; x^{-0.75\varepsilon} \cdot x^{-\varepsilon/100} \;=\; x^{-0.76\varepsilon} \;\ge\; x^{-\varepsilon}.$$

---

## 3. Lean Drop-In Footprint

| Status | Declarations / Files |
|---|---|
| **Deletable** | `BehrendBound`, `ThickSet`, `SpaceExists`, `HostThickExists`, `secondSet_card_lower_bound`, `CT2`, `winN'` (in `Formalism/BehrendSets/`, `Formalism/FrobeniusOrbits/HostThickExists.lean`, `Formalism/SharpRestriction/GlobalSchurBounds/QuadraticLogDerivCongr.lean`) |
| **Unchanged** | `second_set_range`, `second_set_no_relation`, `HostThickOrbit` (`WindowTwo`, `OrbitOne`), `winClusters`, `WachCoordinates` (`ThmELiftAt`, `CorAAt`), `LocalTheoryWindows` (`ArcAt`), `IncomingBound`, `ThickAverage`, `SizeWindows` |

---

## 4. What Still Keeps 3-AP-Freeness (and How to Kill It Too)

While Behrend's sphere-averaging theorem drops out immediately above, **3-AP-freeness itself cannot be replaced by Bernoulli sampling, intervals, or Bohr sets while keeping the current local crystalline theorems unchanged**:

- `ThickAverage` only sees $|T_2|/n$, `OrbitOne` only sees $T_2 \subset [0, n/(4L))$, and `IncomingBound.lean` operates on the *already-Bernoulli* top set `TT` (not $T_2$).
- The actual consumer of `NoRel` / `WindowTwo` is **Wach-module arc lifting** at inert primes: `NoThree` for $l \ge l_A$ (`WordsNT` / `ThmB`) and `Clusters (jA l)` $\to$ `ThickLe2` (`ro ≤ 2` thick letters per arc) for $11 \le l < l_A$ (`WachCoordinates.lean:21-162`).
- Because $l_A = \frac{k x^\varepsilon}{m\delta_2} \approx x^{4+12\varepsilon} \gg n \approx x^{2+8\varepsilon}$, inert primes realize all long-order steps $h \in H_e$, and translation by $u_0$ preserves 3-APs. Along an inert orbit, `up`/`down` signs alternate every step, so any 3-AP $\{x, x+h, x+2h\}$ creates an alternating `up-down-up` triple that fails `LocalTheoryWindows.WordOK` (`LocalTheoryWindows.lean:72-85`).

**To eliminate 3-AP-freeness completely:** raising the allowed thick-letter count per arc from `ro ≤ 2` to constant `ro ≤ K = O(1/ε)` allows replacing $T_2$ by an elementary Bernoulli sample on $[0, n/(4 K L))$ of density $\delta_2 = x^{-\varepsilon/2}$ (`WindowK` holds pointwise over all $n^2$ windows by a 10-line union bound with $K = \lceil 15/\varepsilon \rceil + 50$). On the LP side, `Fnum l d ((k-1) w)` appears identically in both `CorFromThmA` (`IncomingBound.lean:145`) and `InertBd` (`DepthNumbersThresholdEq.lean:151`), so 3-chain deviations cancel identically. Moreover, `UnivCore`, `KillerKap`, and `down_scalar` already accept arbitrary `roMax = K`; the sole remaining local task is extending `WordOK` / `ConstLift` past mixed alternating runs (`up-down-up`).

---

*Derived from a 3-agent audit of `lean/src/` (Claude Fable 5.2, GPT-6.2-Astra, and Gemini).*
