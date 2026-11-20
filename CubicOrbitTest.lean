import Std.Tactic

/-! Finite cubic coordinate in the signal-prime term of Loc.baseTerm.
The scalars A and B below are arbitrary values of the thick and thin
summands after evaluating the old coordinate at a fixed exponent. -/
namespace CubicOrbit

/-- A lift starting on sheet j, with Frobenius acting by d in Z/3. -/
def term (d j e A B : Nat) : Nat :=
  if (j + d * e) % 3 = 0 then A else B

theorem marked_split (e A B : Nat) : term 0 0 e A B = A := by
  simp [term]

theorem marked_three_cycle (e A B : Nat) :
    term 1 0 e A B = if e % 3 = 0 then A else B := by
  simp [term]

theorem odd_marked_return (e : Nat) (he : e % 2 = 1) :
    e % 3 = 0 ↔ e % 6 = 3 := by omega

theorem marked_inside_old_period (e : Nat) :
    (2 * e) % 6 = 0 ↔ e % 3 = 0 := by omega

theorem all_sources (d e A B : Nat) :
    term d 0 e A B + term d 1 e A B + term d 2 e A B = A + B + B := by
  unfold term
  split <;> split <;> split <;> omega

def roots (p : Nat) : List Nat :=
  (List.range p).filter fun t => decide (t^3 % p = (4*t+1) % p)

example : roots 97 = [] := by decide
example : roots 193 = [42, 157, 187] := by decide

-- The congruence and Euler-criterion data for the fixed abelian host.
example : 97 % 16 = 1 ∧ 193 % 16 = 1 ∧ 97 % 3 = 1 ∧ 193 % 3 = 1 := by decide
example : 97^35 % 71 = 70 ∧ 193^35 % 71 = 70 := by decide
example : 97^114 % 229 = 1 ∧ 193^114 % 229 = 1 := by decide

end CubicOrbit
