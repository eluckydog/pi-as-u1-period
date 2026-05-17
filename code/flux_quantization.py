"""Superconducting Flux Quantization: Φ = n·Φ₀ = n·h/(2e).
Phase winding around a ring must be 2π·n for single-valued wavefunction.
The 2 in the denominator comes from Cooper pairs (charge 2e).
"""
import numpy as np


def simulate_flux_measurement(true_n, noise_frac=0.02):
    phi0 = 2.067833848e-15  # Wb
    measured = true_n * phi0 + np.random.normal(0, noise_frac * phi0)
    measured_n = round(measured / phi0)
    return phi0, measured, measured_n


if __name__ == "__main__":
    phi0 = 2.067833848e-15
    print("Flux Quantization in Superconducting Ring")
    print(f"Φ₀ = h/(2e) = {phi0:.3e} Wb\n")
    print("Phase winding: ∮∇φ·dl = 2π·n  →  n integer (single-valuedness)")
    print("Fluxoid: Φ + (m/e²)∮J_s/ρ·dl = n·Φ₀\n")

    np.random.seed(42)
    for true_n in [1, 2, 3, 4, 5]:
        _, measured, measured_n = simulate_flux_measurement(true_n)
        match = "✓" if measured_n == true_n else "✗ MISMATCH"
        print(f"  true n = {true_n}  →  measured = {measured:.3e} Wb  →  n = {measured_n}  {match}")

    print(f"\nHalf-integer detection: Φ₀/2 = {phi0/2:.3e} Wb")
    print("d-wave pairing signature — impossible in s-wave (requires sign change)")
    print("\nThe factor 2 in h/(2e) comes from Cooper pair charge 2e.")
    print("Phase must change by 2π (not π) for the pair wavefunction.")
    print("π locks flux to integer multiples of Φ₀ through U(1) single-valuedness.")