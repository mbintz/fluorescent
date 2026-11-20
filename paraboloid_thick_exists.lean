import Mathlib
import Formalism.FrobeniusOrbits.HostThickExists

open Finset

noncomputable section

/-!
# Variable-Dimension Base-Q Paraboloid Replacement for `ThickExists.lean`

Drop-in replacement for
`lean/src/Formalism/FrobeniusOrbits/FrobeniusOrbitsProofs/ThickExists.lean`
proving `Formalism.FrobeniusOrbits.hostThickExists : HostThickExists` verbatim with
`C = 6` (sharpening the original `C = 32`), with **zero** calls to Mathlib's
`Behrend.*` library (`Behrend.sphere`, `Behrend.map`, `Behrend.exists_large_sphere`),
no sphere-pigeonholing, and no external `Lemmata.GeneralBFactSecondLast` import.

Construction: for `S = ⌊√(log n / log L)⌋` and `Q = 2 * L * A`, map the full cube
`(Fin S → Fin A)` into `ℕ` by
  `v ↦ ∑ m : Fin S, v m * Q ^ m + Q ^ S * ∑ m : Fin S, (v m) ^ 2`.
The non-collinearity (`NoRel`) reduces in one pure-`ℤ` identity to
  `j * (i - j) * ∑ m, (v₂ m - v₁ m) ^ 2 = 0`.
-/

namespace Formalism.FrobeniusOrbits.ThickExists

lemma coeff_zero_top {B : ℤ} (hB : 0 < B) : ∀ {S : ℕ} (c : Fin S → ℤ) (top : ℤ),
    (∀ m, |c m| < B) → (∑ m, c m * B ^ (m : ℕ)) + top * B ^ S = 0 →
    (∀ m, c m = 0) ∧ top = 0 := by
  intro S
  induction S with
  | zero =>
    intro c top _ h
    refine ⟨fun m => Fin.elim0 m, ?_⟩
    simpa using h
  | succ S ih =>
    intro c top hc h
    have hsplit : (∑ m : Fin (S + 1), c m * B ^ (m : ℕ)) + top * B ^ (S + 1) =
        c 0 + B * ((∑ m : Fin S, c m.succ * B ^ (m : ℕ)) + top * B ^ S) := by
      rw [Fin.sum_univ_succ, Fin.val_zero, pow_zero, mul_one, mul_add, Finset.mul_sum]
      have hsum : ∑ m : Fin S, c m.succ * B ^ (m.succ : ℕ) =
          ∑ m : Fin S, B * (c m.succ * B ^ (m : ℕ)) :=
        Finset.sum_congr rfl (fun m _ => by rw [Fin.val_succ, pow_succ]; ring)
      rw [hsum, pow_succ]
      ring
    rw [hsplit] at h
    set R : ℤ := (∑ m : Fin S, c m.succ * B ^ (m : ℕ)) + top * B ^ S
    have hc0_eq : c 0 = -(B * R) := by linarith
    have hR0 : R = 0 := by
      by_contra hne
      obtain ⟨hlo, hhi⟩ := abs_lt.mp (hc 0)
      rcases lt_or_gt_of_ne hne with hlt | hgt
      · have : R ≤ -1 := by omega
        nlinarith
      · have : 1 ≤ R := by omega
        nlinarith
    have hc0 : c 0 = 0 := by rw [hc0_eq, hR0, mul_zero, neg_zero]
    obtain ⟨htail, htop⟩ := ih (fun m => c m.succ) top (fun m => hc m.succ) hR0
    exact ⟨fun m => Fin.cases hc0 htail m, htop⟩

def parabMap (Q : ℕ) {S : ℕ} (v : Fin S → ℕ) : ℕ :=
  (∑ m : Fin S, v m * Q ^ (m : ℕ)) + Q ^ S * ∑ m : Fin S, v m ^ 2

lemma base_lt (Q : ℕ) : ∀ {S : ℕ} (v : Fin S → ℕ), (∀ m, v m < Q) →
    ∑ m : Fin S, v m * Q ^ (m : ℕ) < Q ^ S := by
  intro S
  induction S with
  | zero => intro v _; simp
  | succ S ih =>
    intro v hv
    have h1 := ih (fun m => v m.succ) (fun m => hv _)
    have hsplit : ∑ m : Fin (S + 1), v m * Q ^ (m : ℕ) =
        v 0 + Q * ∑ m : Fin S, v m.succ * Q ^ (m : ℕ) := by
      rw [Fin.sum_univ_succ, Fin.val_zero, pow_zero, mul_one, Finset.mul_sum]
      congr 1
      refine Finset.sum_congr rfl (fun m _ => ?_)
      rw [Fin.val_succ, pow_succ]
      ring
    rw [hsplit, pow_succ]
    have h2 : Q * ((∑ m : Fin S, v m.succ * Q ^ (m : ℕ)) + 1) ≤ Q * Q ^ S :=
      Nat.mul_le_mul_left Q h1
    have h3 := hv 0
    nlinarith

lemma parabMap_lt {Q S A : ℕ} (hS : 1 ≤ S) (hA : 1 ≤ A) (hAQ : A ≤ Q)
    (v : Fin S → ℕ) (hv : ∀ m, v m < A) :
    parabMap Q v < S * A ^ 2 * Q ^ S := by
  have h1 : ∑ m : Fin S, v m * Q ^ (m : ℕ) < Q ^ S :=
    base_lt Q v (fun m => lt_of_lt_of_le (hv m) hAQ)
  have h2 : (∑ m : Fin S, v m ^ 2) + 1 ≤ S * A ^ 2 := by
    have hpt : ∀ m : Fin S, v m ^ 2 + 1 ≤ A ^ 2 := fun m => by
      have hm := hv m
      nlinarith
    have hsum : ∑ m : Fin S, (v m ^ 2 + 1) ≤ ∑ _m : Fin S, A ^ 2 :=
      Finset.sum_le_sum (fun m _ => hpt m)
    rw [Finset.sum_add_distrib, Finset.sum_const, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, smul_eq_mul, smul_eq_mul, mul_one] at hsum
    omega
  have hQpos : 0 < Q ^ S := pow_pos (by omega) S
  unfold parabMap
  nlinarith

lemma cast_parabMap (Q : ℕ) {S : ℕ} (v : Fin S → ℕ) :
    ((parabMap Q v : ℕ) : ℤ) =
      (∑ m : Fin S, (v m : ℤ) * (Q : ℤ) ^ (m : ℕ)) +
        (∑ m : Fin S, (v m : ℤ) ^ 2) * (Q : ℤ) ^ S := by
  simp only [parabMap, Nat.cast_add, Nat.cast_mul, Nat.cast_pow, Nat.cast_sum]
  ring

lemma paraboloid_rel {S : ℕ} (v₁ v₂ v₃ : Fin S → ℤ) (i j : ℤ) (hj : j ≠ 0) (hij : i ≠ j)
    (hlin : ∀ m, j * (v₂ m - v₁ m) = i * (v₃ m - v₁ m))
    (hsq : j * ((∑ m, v₂ m ^ 2) - ∑ m, v₁ m ^ 2) = i * ((∑ m, v₃ m ^ 2) - ∑ m, v₁ m ^ 2)) :
    v₂ = v₁ := by
  have hsum_sq : ∑ m, (j * (v₂ m ^ 2 - v₁ m ^ 2) - i * (v₃ m ^ 2 - v₁ m ^ 2)) = 0 := by
    simp only [Finset.sum_sub_distrib, ← Finset.mul_sum]
    linarith
  have hW : ∑ m, j * (i - j) * (v₂ m - v₁ m) ^ 2 = 0 := by
    have e : ∀ m, j * (i - j) * (v₂ m - v₁ m) ^ 2 =
        i * (j * (v₂ m ^ 2 - v₁ m ^ 2) - i * (v₃ m ^ 2 - v₁ m ^ 2)) -
          (2 * i * v₁ m + j * (v₂ m - v₁ m) + i * (v₃ m - v₁ m)) *
            (j * (v₂ m - v₁ m) - i * (v₃ m - v₁ m)) := fun m => by ring
    have e' : ∀ m, j * (i - j) * (v₂ m - v₁ m) ^ 2 =
        i * (j * (v₂ m ^ 2 - v₁ m ^ 2) - i * (v₃ m ^ 2 - v₁ m ^ 2)) := fun m => by
      rw [e m, hlin m, sub_self, mul_zero, sub_zero]
    rw [Finset.sum_congr rfl (fun m _ => e' m), ← Finset.mul_sum, hsum_sq, mul_zero]
  rw [← Finset.mul_sum] at hW
  have hne : j * (i - j) ≠ 0 := mul_ne_zero hj (sub_ne_zero.mpr hij)
  have hs0 := (mul_eq_zero.mp hW).resolve_left hne
  funext m
  have hm := (Finset.sum_eq_zero_iff_of_nonneg (fun m _ => sq_nonneg (v₂ m - v₁ m))).mp hs0 m
    (Finset.mem_univ m)
  have h0 := (pow_eq_zero_iff two_ne_zero).mp hm
  linarith

def parabSet (L S A : ℕ) : Finset ℕ :=
  (Finset.univ : Finset (Fin S → Fin A)).image
    (fun v => parabMap (2 * L * A) (fun m => (v m : ℕ)))

lemma noRel_parabSet (L S A : ℕ) (hL : 1 ≤ L) (hA : 1 ≤ A) :
    NoRel (parabSet L S A) L := by
  unfold NoRel
  intro s₁ hs₁ s₂ hs₂ s₃ hs₃ h12 h13 h23 i j hi0 hiL hj0 hjL hij heq
  rw [parabSet, Finset.mem_image] at hs₁ hs₂ hs₃
  obtain ⟨v₁, -, rfl⟩ := hs₁
  obtain ⟨v₂, -, rfl⟩ := hs₂
  obtain ⟨v₃, -, rfl⟩ := hs₃
  rw [cast_parabMap, cast_parabMap, cast_parabMap] at heq
  set B : ℤ := ((2 * L * A : ℕ) : ℤ)
  have hBpos : 0 < B := by
    have : 0 < 2 * L * A := by positivity
    exact_mod_cast this
  have hL' : (1 : ℤ) ≤ L := by exact_mod_cast hL
  have hbound : ∀ m : Fin S,
      |j * (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)) - i * (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ))| < B := by
    intro m
    have a1 : ((v₁ m : ℕ) : ℤ) < A := by exact_mod_cast (v₁ m).2
    have a2 : ((v₂ m : ℕ) : ℤ) < A := by exact_mod_cast (v₂ m).2
    have a3 : ((v₃ m : ℕ) : ℤ) < A := by exact_mod_cast (v₃ m).2
    have z1 : (0 : ℤ) ≤ ((v₁ m : ℕ) : ℤ) := by positivity
    have z2 : (0 : ℤ) ≤ ((v₂ m : ℕ) : ℤ) := by positivity
    have z3 : (0 : ℤ) ≤ ((v₃ m : ℕ) : ℤ) := by positivity
    have hd21 : |((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)| ≤ (A : ℤ) - 1 := abs_le.mpr ⟨by omega, by omega⟩
    have hd31 : |((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)| ≤ (A : ℤ) - 1 := abs_le.mpr ⟨by omega, by omega⟩
    have htri : |j * (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)) -
          i * (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ))| ≤
        |j| * |((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)| +
          |i| * |((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)| := by
      simpa only [abs_mul] using
        abs_sub (j * (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)))
          (i * (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)))
    have hA1 : (0 : ℤ) ≤ (A : ℤ) - 1 := by omega
    have hBval : B = 2 * (L : ℤ) * (A : ℤ) := by
      simp only [B]
      push_cast
      ring
    rw [hBval]
    nlinarith [abs_nonneg i, abs_nonneg j, abs_nonneg (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)),
      abs_nonneg (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ))]
  set top : ℤ :=
    j * ((∑ m : Fin S, ((v₂ m : ℕ) : ℤ) ^ 2) - ∑ m : Fin S, ((v₁ m : ℕ) : ℤ) ^ 2) -
      i * ((∑ m : Fin S, ((v₃ m : ℕ) : ℤ) ^ 2) - ∑ m : Fin S, ((v₁ m : ℕ) : ℤ) ^ 2)
  have hsum :
      (∑ m : Fin S, (j * (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)) -
          i * (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ))) * B ^ (m : ℕ)) + top * B ^ S = 0 := by
    have E :
        ∑ m : Fin S, (j * (((v₂ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ)) -
            i * (((v₃ m : ℕ) : ℤ) - ((v₁ m : ℕ) : ℤ))) * B ^ (m : ℕ) =
          ∑ m : Fin S, (j * (((v₂ m : ℕ) : ℤ) * B ^ (m : ℕ)) -
            j * (((v₁ m : ℕ) : ℤ) * B ^ (m : ℕ)) -
            i * (((v₃ m : ℕ) : ℤ) * B ^ (m : ℕ)) +
            i * (((v₁ m : ℕ) : ℤ) * B ^ (m : ℕ))) :=
      Finset.sum_congr rfl (fun m _ => by ring)
    rw [E, Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.sum_sub_distrib,
      ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum, ← Finset.mul_sum]
    linear_combination heq
  obtain ⟨hlin0, htop0⟩ := coeff_zero_top hBpos _ top hbound hsum
  have hsq : j * ((∑ m : Fin S, ((v₂ m : ℕ) : ℤ) ^ 2) - ∑ m : Fin S, ((v₁ m : ℕ) : ℤ) ^ 2) =
      i * ((∑ m : Fin S, ((v₃ m : ℕ) : ℤ) ^ 2) - ∑ m : Fin S, ((v₁ m : ℕ) : ℤ) ^ 2) := by
    dsimp only [top] at htop0
    linarith
  have hrel := paraboloid_rel (fun m => ((v₁ m : ℕ) : ℤ)) (fun m => ((v₂ m : ℕ) : ℤ))
    (fun m => ((v₃ m : ℕ) : ℤ)) i j (abs_pos.mp hj0) hij
    (fun m => by have h0 := hlin0 m; linarith) hsq
  have hv : v₂ = v₁ := funext fun m => Fin.ext (Nat.cast_injective (congrFun hrel m))
  exact h12 (by rw [hv])

lemma card_parabSet (L S A : ℕ) (hL : 1 ≤ L) (hA : 1 ≤ A) :
    (parabSet L S A).card = A ^ S := by
  rw [parabSet, Finset.card_image_of_injOn, Finset.card_univ, Fintype.card_fun,
    Fintype.card_fin, Fintype.card_fin]
  intro v _ w _ hvw
  have hc : ((parabMap (2 * L * A) (fun m => (v m : ℕ)) : ℕ) : ℤ) =
      ((parabMap (2 * L * A) (fun m => (w m : ℕ)) : ℕ) : ℤ) := by
    rw [hvw]
  rw [cast_parabMap, cast_parabMap] at hc
  set B : ℤ := ((2 * L * A : ℕ) : ℤ)
  have hBpos : 0 < B := by
    have : 0 < 2 * L * A := by positivity
    exact_mod_cast this
  have hbound : ∀ m : Fin S, |((v m : ℕ) : ℤ) - ((w m : ℕ) : ℤ)| < B := by
    intro m
    have a1 : ((v m : ℕ) : ℤ) < A := by exact_mod_cast (v m).2
    have a2 : ((w m : ℕ) : ℤ) < A := by exact_mod_cast (w m).2
    have z1 : (0 : ℤ) ≤ ((v m : ℕ) : ℤ) := by positivity
    have z2 : (0 : ℤ) ≤ ((w m : ℕ) : ℤ) := by positivity
    have hL' : (1 : ℤ) ≤ L := by exact_mod_cast hL
    have hA' : (1 : ℤ) ≤ A := by exact_mod_cast hA
    have hBval : B = 2 * (L : ℤ) * (A : ℤ) := by
      simp only [B]
      push_cast
      ring
    rw [hBval, abs_lt]
    constructor <;> nlinarith
  have hsum :
      (∑ m : Fin S, (((v m : ℕ) : ℤ) - ((w m : ℕ) : ℤ)) * B ^ (m : ℕ)) +
        ((∑ m : Fin S, ((v m : ℕ) : ℤ) ^ 2) - ∑ m : Fin S, ((w m : ℕ) : ℤ) ^ 2) * B ^ S = 0 := by
    simp only [sub_mul, Finset.sum_sub_distrib]
    linarith
  obtain ⟨hz, -⟩ := coeff_zero_top hBpos _ _ hbound hsum
  funext m
  have h0 := hz m
  exact Fin.ext (by omega)

lemma two_mul_le_exp {t : ℝ} (ht : 0 ≤ t) : 2 * t ≤ Real.exp t := by
  have h1 : (2 : ℝ) ≤ Real.exp 1 := by linarith [Real.add_one_le_exp (1 : ℝ)]
  have h2 : t ≤ Real.exp (t - 1) := by linarith [Real.add_one_le_exp (t - 1)]
  calc 2 * t ≤ Real.exp 1 * Real.exp (t - 1) := mul_le_mul h1 h2 ht (Real.exp_pos 1).le
    _ = Real.exp (1 + (t - 1)) := (Real.exp_add 1 (t - 1)).symm
    _ = Real.exp t := by ring_nf

end Formalism.FrobeniusOrbits.ThickExists

namespace Formalism.FrobeniusOrbits

set_option maxHeartbeats 1000000 in
open ThickExists in
theorem hostThickExists : HostThickExists := by
  unfold HostThickExists
  refine ⟨6, by norm_num, ?_⟩
  intro n L hL
  have hL2 : (2 : ℝ) ≤ L := by exact_mod_cast hL
  have hLpos : (0 : ℝ) < L := by linarith
  set y : ℝ := Real.log (L : ℝ)
  set x : ℝ := Real.log (n : ℝ)
  set s : ℝ := Real.sqrt (x * y)
  have hlog2_lo : (69 / 100 : ℝ) < Real.log 2 := by linarith [Real.log_two_gt_d9]
  have hlog2_hi : Real.log 2 < (7 / 10 : ℝ) := by linarith [Real.log_two_lt_d9]
  have hlog2_le_y : Real.log 2 ≤ y := Real.log_le_log (by norm_num) hL2
  have hy0 : 0 < y := by linarith
  by_cases hsmall : (n : ℝ) * Real.exp (-6 * s) / L ≤ 1
  · rcases Nat.eq_zero_or_pos n with hn | hn
    · refine ⟨∅, by simp, ?_, by simp [hn]⟩
      unfold NoRel
      intro s₁ hs₁
      simp at hs₁
    · refine ⟨{0}, ?_, ?_, ?_⟩
      · intro m hm
        rw [Finset.mem_singleton] at hm
        subst hm
        simpa using hn
      · unfold NoRel
        intro s₁ hs₁ s₂ hs₂ s₃ hs₃ h12
        rw [Finset.mem_singleton] at hs₁ hs₂
        exact absurd (hs₁.trans hs₂.symm) h12
      · rw [Finset.card_singleton, Nat.cast_one]
        exact hsmall
  push_neg at hsmall
  have hnpos : (0 : ℝ) < n := by
    rcases Nat.eq_zero_or_pos n with hn | hn
    · rw [hn] at hsmall
      norm_num at hsmall
    · exact_mod_cast hn
  have eL : Real.exp y = L := Real.exp_log hLpos
  have en : Real.exp x = n := Real.exp_log hnpos
  have e2 : Real.exp (Real.log 2) = 2 := Real.exp_log (by norm_num)
  have hpos : 0 < x + -6 * s - y := by
    rw [← Real.exp_lt_exp, Real.exp_zero, Real.exp_sub, Real.exp_add, eL, en]
    exact hsmall
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hxpos : 0 < x := by linarith
  have hs2 : s ^ 2 = x * y := Real.sq_sqrt (mul_pos hxpos hy0).le
  have hs6 : 6 * y < s := by
    by_contra hc
    push_neg at hc
    nlinarith [mul_nonneg hs0 (sub_nonneg.mpr hc), mul_pos hpos hy0, sq_nonneg y]
  have hspos : 0 < s := by linarith
  set S : ℕ := ⌊s / y⌋₊
  have hS1 : (S : ℝ) ≤ s / y := Nat.floor_le (div_nonneg hs0 hy0.le)
  have hS2 : s / y < S + 1 := Nat.lt_floor_add_one _
  have hSy : (S : ℝ) * y ≤ s := (le_div_iff₀ hy0).mp hS1
  have hSy2 : s < (S + 1) * y := (div_lt_iff₀ hy0).mp hS2
  have hS5 : (5 : ℝ) < S := by
    have h := lt_of_mul_lt_mul_right (show (6 : ℝ) * y < (S + 1) * y by linarith) hy0.le
    linarith
  have hS1nat : 1 ≤ S := by
    have : (1 : ℝ) ≤ S := by linarith
    exact_mod_cast this
  have hSpos : (0 : ℝ) < S := by linarith
  have hS2pos : (0 : ℝ) < S + 2 := by linarith
  have hcoef : 2 * Real.log 2 + 1 / 2 ≤ (11 / 4 : ℝ) * y := by linarith
  set a : ℝ := (x - (2 * Real.log 2 + y + (S : ℝ) / 2 + S * (Real.log 2 + y))) / (S + 2)
  have ha_eq : a * (S + 2) = x - (2 * Real.log 2 + y + (S : ℝ) / 2 + S * (Real.log 2 + y)) := by
    simp only [a]
    field_simp
  have ha_ge : Real.log 2 ≤ a := by
    rw [le_div_iff₀ hS2pos]
    have h1 : (S : ℝ) * (2 * Real.log 2 + 1 / 2 + y) ≤ (15 / 4 : ℝ) * s := by
      have h1a : (S : ℝ) * (2 * Real.log 2 + 1 / 2 + y) ≤ (S : ℝ) * ((15 / 4 : ℝ) * y) :=
        mul_le_mul_of_nonneg_left (by linarith) hSpos.le
      nlinarith
    have hring : Real.log 2 * ((S : ℝ) + 2) +
          (2 * Real.log 2 + y + (S : ℝ) / 2 + (S : ℝ) * (Real.log 2 + y)) =
        4 * Real.log 2 + y + (S : ℝ) * (2 * Real.log 2 + 1 / 2 + y) := by ring
    linarith
  set A : ℕ := ⌊Real.exp a⌋₊
  have h2le : (2 : ℝ) ≤ Real.exp a := by
    rw [← e2]
    exact Real.exp_le_exp.mpr ha_ge
  have hA1r : (1 : ℝ) ≤ A := by
    have hlt : Real.exp a < A + 1 := Nat.lt_floor_add_one _
    linarith
  have hA1 : 1 ≤ A := by exact_mod_cast hA1r
  have hA_le : (A : ℝ) ≤ Real.exp a := Nat.floor_le (Real.exp_pos a).le
  have hA_ge : Real.exp a / 2 ≤ A := by
    have hlt : Real.exp a < A + 1 := Nat.lt_floor_add_one _
    linarith
  have hSe : (S : ℝ) ≤ Real.exp ((S : ℝ) / 2) := by
    have h := two_mul_le_exp (show (0 : ℝ) ≤ (S : ℝ) / 2 by positivity)
    linarith
  have h4eq : (4 : ℝ) = Real.exp (2 * Real.log 2) := by
    rw [two_mul, Real.exp_add, e2]
    norm_num
  have h2Leq : (2 * L : ℝ) = Real.exp (Real.log 2 + y) := by
    rw [Real.exp_add, e2, eL]
  have hreal_n : (4 : ℝ) * L * S * (2 * L) ^ S * (A : ℝ) ^ (S + 2) ≤ n := by
    have hA_pow : (A : ℝ) ^ (S + 2) ≤ Real.exp a ^ (S + 2) := by gcongr
    calc (4 : ℝ) * L * S * (2 * L) ^ S * (A : ℝ) ^ (S + 2)
        ≤ Real.exp (2 * Real.log 2) * Real.exp y * Real.exp ((S : ℝ) / 2) *
            Real.exp (Real.log 2 + y) ^ S * Real.exp a ^ (S + 2) := by
          rw [← h4eq, eL, ← h2Leq]
          gcongr
      _ = Real.exp (2 * Real.log 2) * Real.exp y * Real.exp ((S : ℝ) / 2) *
            Real.exp ((S : ℝ) * (Real.log 2 + y)) * Real.exp (((S + 2 : ℕ) : ℝ) * a) := by
          rw [← Real.exp_nat_mul, ← Real.exp_nat_mul]
      _ = Real.exp (2 * Real.log 2 + y + (S : ℝ) / 2 + (S : ℝ) * (Real.log 2 + y) +
            ((S : ℝ) + 2) * a) := by
          push_cast
          rw [← Real.exp_add, ← Real.exp_add, ← Real.exp_add, ← Real.exp_add]
      _ = Real.exp x := by
          congr 1
          linear_combination ha_eq
      _ = n := en
  have hnat_n : 4 * L * (S * A ^ 2 * (2 * L * A) ^ S) ≤ n := by
    have hcast : ((4 * L * (S * A ^ 2 * (2 * L * A) ^ S) : ℕ) : ℝ) =
        (4 : ℝ) * L * S * (2 * L) ^ S * (A : ℝ) ^ (S + 2) := by
      push_cast
      rw [mul_pow, pow_add]
      ring
    exact_mod_cast (hcast.le.trans hreal_n)
  refine ⟨parabSet L S A, ?_, noRel_parabSet L S A (by omega) hA1, ?_⟩
  · intro m hm
    rw [parabSet, Finset.mem_image] at hm
    obtain ⟨v, -, rfl⟩ := hm
    have hAQ : A ≤ 2 * L * A := by nlinarith
    have hmlt := parabMap_lt hS1nat hA1 hAQ (fun k => (v k : ℕ)) (fun k => (v k).2)
    exact lt_of_lt_of_le (Nat.mul_lt_mul_of_pos_left hmlt (by omega)) hnat_n
  · rw [card_parabSet L S A (by omega) hA1, Nat.cast_pow]
    have hexp_ineq : x - 6 * s - y ≤ (S : ℝ) * (a - Real.log 2) := by
      have hmul_y :
          2 * s ^ 2 + 4 * (S : ℝ) * y * Real.log 2 +
              (S : ℝ) ^ 2 * y * (2 * Real.log 2 + 1 / 2 + y) ≤
            6 * ((S : ℝ) + 2) * s * y + 2 * y ^ 2 := by
        have ht1 : 2 * s ^ 2 ≤ 2 * (S : ℝ) * s * y + 2 * s * y := by
          nlinarith [mul_le_mul_of_nonneg_left hSy2.le hs0]
        have ht2 : (S : ℝ) ^ 2 * y ^ 2 ≤ (S : ℝ) * s * y + s * y := by
          have hSsq : (S : ℝ) ^ 2 * y ^ 2 ≤ s ^ 2 := by
            nlinarith [mul_nonneg (sub_nonneg.mpr hSy) (add_nonneg (mul_nonneg hSpos.le hy0.le) hs0)]
          nlinarith [mul_le_mul_of_nonneg_left hSy2.le hs0]
        have ht3 : (S : ℝ) ^ 2 * y * (2 * Real.log 2 + 1 / 2) ≤ (11 / 4 : ℝ) * (S : ℝ) * s * y := by
          have h3a : (S : ℝ) ^ 2 * y * (2 * Real.log 2 + 1 / 2) ≤
              (S : ℝ) ^ 2 * y * ((11 / 4 : ℝ) * y) :=
            mul_le_mul_of_nonneg_left hcoef (by positivity)
          have h3b : (S : ℝ) ^ 2 * y ^ 2 ≤ (S : ℝ) * y * s := by
            have := mul_le_mul_of_nonneg_left hSy (mul_nonneg hSpos.le hy0.le)
            linarith
          nlinarith
        have ht4 : 4 * (S : ℝ) * y * Real.log 2 ≤ 4 * s * y := by
          have h4a : 4 * (S : ℝ) * y * Real.log 2 ≤ 4 * (S : ℝ) * y * y :=
            mul_le_mul_of_nonneg_left hlog2_le_y (by positivity)
          have h4b : 4 * (S : ℝ) * y * y ≤ 4 * s * y := by
            have := mul_le_mul_of_nonneg_right hSy hy0.le
            linarith
          linarith
        have hrem : 0 ≤ (1 / 4 : ℝ) * (S : ℝ) * s * y + 5 * s * y + 2 * y ^ 2 := by positivity
        nlinarith
      have hmul_S2 : ((S : ℝ) + 2) * (x - 6 * s - y) ≤ ((S : ℝ) + 2) * ((S : ℝ) * (a - Real.log 2)) := by
        have hstep :
            ((S : ℝ) + 2) * (x - 6 * s - y) * y ≤
              ((S : ℝ) + 2) * ((S : ℝ) * (a - Real.log 2)) * y := by
          have h1 : ((S : ℝ) + 2) * ((S : ℝ) * (a - Real.log 2)) =
              (S : ℝ) * (x - (2 * Real.log 2 + y + (S : ℝ) / 2 + (S : ℝ) * (Real.log 2 + y)) -
                ((S : ℝ) + 2) * Real.log 2) := by
            linear_combination (S : ℝ) * ha_eq
          rw [h1]
          have hdiff :
              (S : ℝ) * (x - (2 * Real.log 2 + y + (S : ℝ) / 2 + (S : ℝ) * (Real.log 2 + y)) -
                  ((S : ℝ) + 2) * Real.log 2) * y -
                ((S : ℝ) + 2) * (x - 6 * s - y) * y =
              (6 * ((S : ℝ) + 2) * s * y + 2 * y ^ 2) -
                (2 * s ^ 2 + 4 * (S : ℝ) * y * Real.log 2 +
                  (S : ℝ) ^ 2 * y * (2 * Real.log 2 + 1 / 2 + y)) := by
            linear_combination 2 * hs2
          linarith
        exact le_of_mul_le_mul_right hstep hy0
      exact le_of_mul_le_mul_left hmul_S2 hS2pos
    have hcard_exp : (n : ℝ) * Real.exp (-6 * s) / L = Real.exp (x - 6 * s - y) := by
      rw [Real.exp_sub, show x - 6 * s = x + -6 * s by ring, Real.exp_add, en, eL]
    rw [hcard_exp]
    calc Real.exp (x - 6 * s - y)
        ≤ Real.exp ((S : ℝ) * (a - Real.log 2)) := Real.exp_le_exp.mpr hexp_ineq
      _ = Real.exp (a - Real.log 2) ^ S := Real.exp_nat_mul _ _
      _ = (Real.exp a / 2) ^ S := by rw [Real.exp_sub, e2]
      _ ≤ (A : ℝ) ^ S := by gcongr

end Formalism.FrobeniusOrbits
