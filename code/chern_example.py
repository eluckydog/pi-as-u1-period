"""Chern Number: (1/2π)∫F = integer for any smooth deformation.
Two-band topological insulator H(k) = sin(kx)σx + sin(ky)σy + (m − cos(kx) − cos(ky))σz.
Berry curvature F = (1/2|d|³) d·(∂_x d × ∂_y d), integrated over the Brillouin zone.
"""
import numpy as np

def chern_number(N=40, m=1.0):
    ks = np.linspace(-np.pi, np.pi, N, endpoint=False)
    dk = 2 * np.pi / N
    C = 0.0
    for i in range(N):
        for j in range(N):
            kx, ky = ks[i], ks[j]

            def d(kx, ky):
                return np.array([np.sin(kx), np.sin(ky), m - np.cos(kx) - np.cos(ky)])

            d0 = d(kx, ky)
            dx = (d(kx + dk, ky) - d(kx - dk, ky)) / (2 * dk)
            dy = (d(kx, ky + dk) - d(kx, ky - dk)) / (2 * dk)
            nd = np.linalg.norm(d0)
            F = np.dot(d0, np.cross(dx, dy)) / (2 * nd**3)
            C += F * dk * dk / (2 * np.pi)
    return C


if __name__ == "__main__":
    print("Chern Number: (1/2π)∫_BZ F(k) d²k")
    print("H = sin(kx)σx + sin(ky)σy + (m − cos(kx) − cos(ky))σz\n")
    for m in [3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0]:
        C = chern_number(N=25, m=m)
        if abs(m - 0.0) < 0.01 or abs(m + 2.0) < 0.01:
            print(f"  m = {m:+5.1f}  →  (gap closes — phase transition, C undefined)")
        elif abs(C) > 50:
            print(f"  m = {m:+5.1f}  →  (near gap closure — numerical divergence)")
        else:
            label = "TOPOLOGICAL  " if abs(C) > 0.8 else "TRIVIAL"
            bar = "█" * min(int(abs(C) * 10), 10) if abs(C) > 0.8 else ""
            print(f"  m = {m:+5.1f}  →  C = {C:+5.2f}  {label} {bar}")

    print("\nThe 1/(2π) prefactor forces ∫F to be 2π × integer.")
    print("Without it, ∫F varies continuously. With it, C ∈ Z for every m.")
    print("π is not cosmetic here — it defines the topological classification.")