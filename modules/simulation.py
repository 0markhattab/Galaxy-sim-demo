from __future__ import annotations
import numpy as np
from numba import njit, prange
from modules.generation import StarArray, GasGrid, V_CIRC

_DT_SN_FLASH = 0.01  

@njit(parallel=True)
def _advance_positions(x, y, vx, vy, dt):
    for i in prange(x.size):
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt


def step(stars: StarArray, gas: GasGrid, dt_myr: float, rng: np.random.Generator):
    """Advance stars + gas grid, return coordinates of any SN flashes."""
    # --- stars ---
    _advance_positions(stars.x, stars.y, stars.vx, stars.vy, dt_myr)
    stars.age += dt_myr

    sn_indices = stars.sn_timer > 0
    stars.sn_timer[sn_indices] -= dt_myr

    flashes = (sn_indices) & (stars.sn_timer < 0)
    sn_xy = (stars.x[flashes], stars.y[flashes]) if flashes.any() else None

    # remove exploded stars (turn into 1 M☉ remnants and kick)
    stars.mass[flashes] = 1.0
    kicks = rng.normal(scale=0.05, size=flashes.sum())
    stars.vx[flashes] += kicks
    stars.vy[flashes] += kicks

    gas.rotate(angle_rad=V_CIRC * dt_myr / gas.size_kpc)

    return sn_xy
