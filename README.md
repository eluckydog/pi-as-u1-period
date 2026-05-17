# π as U(1) Period: Four Faces of One Constant

> We set out to beat Chudnovsky. We failed. We found something better.

---

## The Experiment

In May 2026, a non-mathematician working alongside an AI agent asked a genuinely ambitious question:

> **Can an ordinary person + AI design a π computation algorithm that surpasses what human geniuses built?**

We threw everything at it. Four independent paths explored, 26 arctan decompositions searched, brute-force BBP scans in 6 non-standard bases, Chowla-Selberg + Gamma methods analyzed, quantum phase estimation investigated, Monte Carlo convergence tested, motivic integration consulted.

**The honest answer: No.** Every path converged to the same frontier. Chudnovsky's algorithm + binary splitting is already optimal for computing decimal digits of π. A simpler representation is blocked by the Kontsevich-Zagier conjecture — π is a period of the Tate motive Z(1), and you cannot cheat the motive. The search space for "a faster π algorithm" is effectively closed.

But we didn't walk away empty-handed. The search itself revealed something the benchmarks never show:

**π is not just a number to compute. It is the period of U(1) — the simplest continuous symmetry in physics.** Once you see π as a *structure* rather than a *target*, four practical dimensions open up. This repo documents the discovery we made instead of the victory we imagined.

---

## The Core Insight

U(1) is the simplest compact Lie group: `{e^(iθ) | θ ∈ [0, 2π)}`. Its period is **2π**.

Any physical system with U(1) rotational symmetry implicitly carries π inside it. Four domains—superconductivity, topology, synchronization, engineering—look unrelated but share **one mathematical skeleton**. The moment you recognize it, π transforms from a *number to be computed* into a *ruler to measure the world*.

## The Cross-Domain Map

| Dimension | Physical System | Formula (skeletal) | π's Semantic Role | Critical Threshold | Real-World Impact |
|-----------|----------------|-------------------|-------------------|-------------------|-------------------|
| **Diagnostic Ruler** | Superconducting flux, MRI, PLL | Φ = Φ₀·n, Φ₀ = h/2e | Deviation from 2π·n = anomaly | Half-integer flux → unconventional pairing | Fault detection, phase unwrapping |
| **Topological Constraint** | Quantum Hall, DNA supercoiling | C = (1/2π)∫F d²k | Forces integer quantization | Any non-zero C → protected edge state | Resistance standard (±10⁻⁹), anticancer drug targets |
| **Phase Transition** | Kuramoto oscillators, power grid | θ̇ᵢ = ωᵢ − (K/N)Σ sin(θⱼ−θᵢ) | π/2 = sync/desync boundary | Phase diff > π/2 → cascade failure | Grid stability, cardiac pacing, 5G beamforming |
| **Engineering Bound** | Antenna array, AC power | AF = sin(Nψ)/sin(ψ), ψ = (πd/λ)sinθ | λ/2 = π/k → grating lobe floor | cosφ < cos(π/4) → reactive > active | Antenna spacing, power factor correction |

## Why One Repo?

A superconductivity researcher doesn't read antenna design papers. An arrhythmia cardiologist doesn't study Chern classes.

But each of these is ~2KB. Nobody would clone a 2KB standalone repo. **The cross-domain isomorphism is the only thing that makes this worth open-sourcing.** Split them apart, and you destroy the product.

One repo says: *"Look at the same structure under four different lamps. The lamps are different. The structure is the same."*

## Structure

```
pi-as-u1-period/
├── README.md                           (this file)
├── dimensions/
│   ├── 01_flux_quantization.md         Quantization as Detection
│   ├── 02_chern_topology.md            Topology as Protection
│   ├── 03_kuramoto_sync.md             Synchronization as Threshold
│   └── 04_antenna_grating.md           Symmetry as Engineering Constraint
├── code/
│   ├── pi_toolkit.py                   AGM / Chudnovsky / Borwein / BBP
│   ├── bbp_searcher.py                 arctan decomposition + BBP base detection
│   ├── kuramoto_demo.py                Synchronization phase transition at π/2
│   ├── chern_example.py                Chern number quantization by 1/2π
│   ├── antenna_grating.py              Grating lobe onset at d = λ/2 = π/k
│   └── flux_quantization.py            Flux quantum = h/(2e), 2π phase winding
└── LICENSE
```

## Quick Start

```bash
# π computation benchmark
python code/pi_toolkit.py --benchmark

# Search arctan decompositions for π
python code/bbp_searcher.py --find pi

# Run dimension demos
python code/kuramoto_demo.py       # sync/desync phase transition
python code/chern_example.py       # integer quantization by 1/2π
python code/antenna_grating.py     # grating lobe onset
python code/flux_quantization.py   # flux quantum = h/(2e)
```

## Philosophy

**Inward**: Chudnovsky computing 100 trillion digits of π — measuring π itself.  
**Outward**: using π as a *ruler* to detect, protect, and bound physical systems — letting π's structure reveal order in the world.

> U(1) symmetry breaking = useful information.  
> π is the tick mark on that axis.

---

*Built with math-science workspace, May 2026 — the month we failed to beat Chudnovsky and found something better.*