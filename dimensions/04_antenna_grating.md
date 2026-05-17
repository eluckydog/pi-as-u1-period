# Dimension 4: Symmetry as Engineering Constraint — π Sets Hardware Limits

> U(1) rotational symmetry → Noether's theorem → conservation of angular momentum.
> π doesn't appear as a measurement — it appears as a **hard physical bound** on what you can build.

---

## Antenna Array — Grating Lobe Condition

```
N-element linear array factor:
  AF(θ) = Σₙ₌₀ᴺ⁻¹ exp(j · k · d · n · sinθ)
        = sin(N·k·d·sinθ/2) / sin(k·d·sinθ/2)

Grating lobe condition:  k·d·sinθ = 2π·n   (n = ±1, ±2, ...)
  → d/λ = n / |sinθ|
  → minimum grating-lobe spacing: d = λ  (at θ = π/2)
  → safe spacing: d < λ/2
```

**λ/2 = π/k.** So `d < π/k` → no grating lobes.

**π directly determines the maximum antenna element spacing.** That's not a design choice — it's a mathematical floor. Violate it and your array radiates in unintended directions.

---

## AC Power Systems — Reactive Power Boundary

```
Complex power: S = V · I* = P + jQ
  P = |S| · cos φ   (active power, watts — does work)
  Q = |S| · sin φ   (reactive power, VAR — sloshes back and forth)

Power factor: pf = P/|S| = cos φ
```

| φ | Condition | Meaning |
|---|-----------|---------|
| φ = 0 | pf = 1 | Pure active — ideal |
| 0 < φ < π/4 | pf > 0.707 | Acceptable |
| φ = π/4 | pf = 0.707 | **Economic critical angle:** \|Q\| = P |
| φ > π/4 | pf < 0.707 | \|Q\| > P — more waste than work |
| φ = π/2 | pf = 0 | Pure reactive — completely useless |

**π/4 is the economic breakpoint** for power systems. Cross it and you're spending more on reactive slosh than on actual work. Utility companies fine you for pf < 0.9 (~φ > π/7).

---

## Rotating Machinery — Period as Diagnostic

```
Lagrangian U(1) invariance → angular momentum conservation
  θ → θ + α  (rotation)
  → dL/dt = 0  (angular momentum conserved)
  → ω = constant / I  (for fixed moment of inertia)

Period T = 2π/ω   Frequency f = ω/(2π)
```

**π's diagnostic role:** T deviates from 2π/ω → friction / load change / bearing failure. The expected value is 2π/ω; the deviation is the fault signature.

---

## The Pattern

| System | π's Role | Engineering Limit |
|--------|---------|-------------------|
| Antenna array | λ/2 = π/k | d < π/k → no grating lobes |
| AC power | cos φ | φ < π/4 → |Q| ≤ P |
| Rotating machine | T = 2π/ω | T offset → mechanical fault |

π doesn't set a preference. It sets a law.

---

*Part of [π as U(1) Period](../README.md) — cross-domain isomorphism map*