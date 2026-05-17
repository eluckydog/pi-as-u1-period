"""Kuramoto Model: π/2 = synchronization phase transition.
N coupled oscillators with phase θᵢ and natural frequency ωᵢ.
Coupling sin(θⱼ−θᵢ): attractive for |Δθ| < π/2, repulsive beyond.
"""
import numpy as np

def kuramoto(N=200, K=1.0, dt=0.01, steps=3000):
    omega = np.random.normal(0, 0.5, N)
    theta = np.random.uniform(0, 2 * np.pi, N)
    for _ in range(steps):
        d = theta.reshape(1, -1) - theta.reshape(-1, 1)
        coupling = (K / N) * np.sum(np.sin(d), axis=1)
        theta += (omega + coupling) * dt
    return np.abs(np.mean(np.exp(1j * theta)))  # order parameter r ∈ [0, 1]

if __name__ == "__main__":
    print("Kuramoto Synchronization")
    print(f"Attractive: |Δθ| < π/2   |   Repulsive: |Δθ| > π/2\n")
    for K in [0.1, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0]:
        r = kuramoto(K=K)
        if r > 0.6:
            s = "SYNCHRONIZED"
        elif r > 0.2:
            s = "PARTIAL"
        else:
            s = "DESYNCHRONIZED"
        print(f"  K = {K:4.1f}  →  order r = {r:.3f}  ({s})")
    print(f"\nK_c ≈ π/4 ≈ {np.pi/4:.3f} — the threshold where coupling overcomes frequency dispersion")