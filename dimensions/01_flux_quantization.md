# Dimension 1: Quantization as Detection — Deviation from π = Anomaly

> In any U(1)-symmetric system, normal behavior is locked to integer multiples of 2π.
> **Deviation from this value is the anomaly signal.**

---

## Magnetic Flux Quantization in Superconductors

```
Flux quantum: Φ₀ = h / (2e)

Going around a superconducting ring, the wavefunction phase must change by 2π·n (n integer).
If it doesn't, the wavefunction is not single-valued — superconductivity breaks.

Measured flux = Φ₀ · n   (n = integer)
```

**π's diagnostic role:** Half-integer flux (Φ₀/2) cannot arise from conventional s-wave pairing. It's direct evidence of **d-wave superconductivity** — the hallmark of high-Tc cuprates. You're not computing π; you're using π to read the pairing symmetry of the material.

---

## MRI Phase Wrapping Detection

```
MRI signal:  S(k) = ∫ ρ(x) · exp(−i · k · x) dx

Phase accumulation:  φ = γ · B · t   (Larmor precession)
When φ exceeds π, phase wrapping occurs.
```

**π's diagnostic role:** `φ > π` and sign(φ) reverses → aliasing artifact detected. Triggers automatic gradient adjustment or phase unwrapping. π is the phase-wrapping threshold.

---

## PLL Lock Detection

```
Phase-locked loop: VCO output tracks input phase
Lock condition: |φ_in − φ_vco| < π/2

Detection: phase difference exceeds [−π/2, +π/2] → loss of lock
→ re-scan / switch frequency source
```

**π's role:** π is the **lock/unlock boundary** in phase-locked loops. Crossing it means the PLL has lost its grip on the signal.

---

## The Pattern

| System | Normal = 2π·n | Anomaly = deviation | Action |
|--------|--------------|-------------------|--------|
| SC flux | Φ₀ · n | Φ₀/2 → d-wave pairing | Identify pairing symmetry |
| MRI phase | |φ| < π | |φ| > π → aliasing | Phase unwrapping |
| PLL | |Δφ| < π/2 | |Δφ| > π/2 → loss of lock | Re-acquisition |

π is the tick mark. The distance from the tick mark is information.

---

*Part of [π as U(1) Period](../README.md) — cross-domain isomorphism map*