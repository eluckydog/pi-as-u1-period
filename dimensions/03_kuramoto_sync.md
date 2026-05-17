# Dimension 3: Synchronization as Threshold — π/2 is the Phase Transition

> Coupled oscillators sync or desync depending on phase difference.
> The boundary between order and chaos is exactly π/2.

---

## Kuramoto Model — The Canonical Coupled Oscillator

```
dθᵢ/dt = ωᵢ + (K/N) · Σⱼ sin(θⱼ − θᵢ)

Coupling term sin(θⱼ − θᵢ):
  Δθ ∈ [0, π/2]:   attractive  (promotes synchronization)
  Δθ ∈ [π/2, π]:   repulsive   (destroys synchronization)
  Δθ > π:           strongly repulsive
```

**Critical coupling K_c** corresponds to a phase transition near Δθ = π/2.

**π/2 = the sync/desync boundary.**

---

## Real-World Systems

| System | π's Role | Anomaly Signal | Consequence |
|--------|---------|---------------|-------------|
| **Power Grid** | Phase angle diff > π/2 → generator destabilization | Sudden frequency drop | Load shedding, cascading blackout |
| **Cardiac Pacemaker** (SA node) | Phase diff < π/4 → synchronized beating | Phase diff widens → arrhythmia | Atrial fibrillation |
| **Firefly Flashing** | Phase diff shrinks → synchronized flashing | Failure to sync → environmental stress | Disrupted mating |
| **5G Beamforming** | Array phase diff < π/8 → coherent beam | Phase error > π/4 → beam divergence | Coverage hole |

All four are the **same equation** with different parameters.

---

## The Pattern

```
Synchronization quality = f(|Δθ| − π/2)

  |Δθ| < π/2  →  attractive coupling  →  order emerges
  |Δθ| = π/2  →  critical point       →  phase transition  
  |Δθ| > π/2  →  repulsive coupling   →  chaos

π = the dial that turns order into chaos.
```

---

*Part of [π as U(1) Period](../README.md) — cross-domain isomorphism map*