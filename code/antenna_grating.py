"""Antenna Array Factor: π/k = λ/2 → grating lobe floor.
N-element linear array. Grating lobes appear when d ≥ λ.
Safe design: d < λ/2 = π/k — directly constrained by π.
"""
import numpy as np

def array_factor(theta, N=8, d_lambda=0.5):
    kd = 2 * np.pi * d_lambda
    psi = kd * np.sin(theta)
    af = np.sin(N * psi / 2) / (N * np.sin(psi / 2))
    mask = np.abs(np.sin(psi / 2)) < 1e-10
    af[mask] = 1.0
    return np.abs(af)


if __name__ == "__main__":
    thetas = np.linspace(-np.pi / 2, np.pi / 2, 501)
    print("Linear Array — Grating Lobe Condition")
    print(f"Element count: 8\n")
    print(f"  Grating lobe onset:  d = λ = 2π/k")
    print(f"  Safe design rule:    d < λ/2 = π/k\n")

    for d_l in [0.3, 0.45, 0.5, 0.55, 0.7, 1.0, 1.2]:
        af = array_factor(thetas, d_lambda=d_l)
        mid = len(af) // 2
        main = af[mid]
        grating = np.max(np.concatenate([af[:mid - 5], af[mid + 5:]]))
        status = "✓ SAFE" if d_l < 0.5 else "✗ GRATING LOBES (grating peak = {:.2f})".format(grating)
        print(f"  d/λ = {d_l:.2f}  |  main lobe = {main:.3f}  |  {status}")

    print(f"\n  Design constraint: d < π/k = λ/2 ≈ 0.50λ")
    print(f"  π sets the maximum element spacing — no design freedom.")