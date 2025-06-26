from __future__ import annotations
import numpy as np

__all__ = [
    "StarArray",
    "GasGrid",
    "generate_initial_conditions",
]

class StarArray(np.recarray):
    """Structured ndarray holding stellar phase‑space + metadata."""

    pass

class GasGrid:
    """2‑D logarithmic surface‑density grid (kpc ➜ px)."""
    def __init__(self, nx: int = 1024, size_kpc: float = 30.0, seed: int | None = None):
        rng = np.random.default_rng(seed)
        self.size_kpc = size_kpc
        self.nx = nx
        # Exponential disk + Perlin‑like noise for clumpiness
        x = np.linspace(-size_kpc/2, size_kpc/2, nx)
        X, Y = np.meshgrid(x, x)
        r = np.hypot(X, Y)
        sigma0 = 10**7  # M☉ kpc⁻²
        self.density = sigma0 * np.exp(-r / 4.0)
        # add fractal noise
        self.density *= (1 + 0.4 * rng.standard_normal((nx, nx)))

    def rotate(self, angle_rad: float):
        """Rigidly rotate the grid by given angle (nearest‑neighbour)."""
        from scipy.ndimage import rotate as _rot
        self.density = _rot(self.density, np.degrees(angle_rad), reshape=False, order=1, mode="wrap")

StarDtype = np.dtype([
    ("x",  "f8"), ("y",  "f8"), ("z",  "f8"),
    ("vx", "f8"), ("vy", "f8"), ("vz", "f8"),
    ("mass", "f4"),              # M☉
    ("age",  "f4"),              # Myr
    ("sn_timer", "f4"),          # counts down to explosion
])

_KMS_TO_KPCMYR = 1.022  # 1 km/s = 1.022 kpc / Gyr ≈ 0.001022 kpc / Myr
V_CIRC = 220 * _KMS_TO_KPCMYR  


def _generate_stars(n: int, seed: int | None = None) -> StarArray:
    rng = np.random.default_rng(seed)
    stars = np.recarray(shape=n, dtype=StarDtype)

    # Radial exponential disk (scale length 5 kpc)
    r = rng.exponential(scale=5.0, size=n)
    phi = rng.uniform(0, 2*np.pi, n)
    z = rng.normal(loc=0.0, scale=0.3, size=n)  # thin disk

    stars.x, stars.y = r * np.cos(phi), r * np.sin(phi)
    stars.z = z

    # Circular velocities (flat curve)
    v_phi = V_CIRC * np.ones_like(r)
    stars.vx = -v_phi * np.sin(phi)
    stars.vy =  v_phi * np.cos(phi)
    stars.vz = rng.normal(scale=5e-3, size=n)   # km/s converted ➜ ~0.005 kpc/Myr vertical motions

    # Initial masses (Kroupa‑like IMF, truncated 0.5–40 M☉)
    m = (rng.pareto(1.35, n) + 1) * 0.5
    stars.mass = np.clip(m, 0.5, 40)

    # Ages 0–49 Myr (so some explode during 50 Myr sim)
    stars.age = rng.uniform(0, 49, n)

    # sn_timer: pick massive stars >8 M☉, schedule explosion at 10 Myr total age
    stars.sn_timer = np.where(stars.mass > 8, 10 - stars.age, -1.0)

    return stars.view(StarArray)


def generate_initial_conditions(n_stars: int = 40000, grid_n: int = 1024, seed: int | None = None):
    stars = _generate_stars(n_stars, seed)
    gas = GasGrid(nx=grid_n, seed=seed)
    return stars, gas

