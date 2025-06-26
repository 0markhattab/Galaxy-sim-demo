from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

_GAS_CMAP = "Blues_r"
_HII_COLOR = (0.8, 0.3, 0.3, 0.4)  

def _draw_gas(ax, gas):
    im = ax.imshow(gas.density, extent=[-gas.size_kpc/2, gas.size_kpc/2]*2,
                   origin="lower", cmap=_GAS_CMAP,
                   norm=LogNorm(vmin=1e6, vmax=1e8), alpha=0.9)
    return im


def _draw_stars(ax, stars):
    ax.scatter(stars.x, stars.y, s=0.2, c="white", marker=".", linewidths=0)


def _draw_sn(ax, sn_xy):
    if sn_xy is None:
        return
    x, y = sn_xy
    ax.scatter(x, y, s=15, c="yellow", marker="*", linewidths=0.2)


def render(frame_idx: int, stars, gas, sn_xy, out_path: str, size: int = 600):
    fig = plt.figure(figsize=(size/100, size/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], facecolor="black")
    ax.set_xlim(-gas.size_kpc/2, gas.size_kpc/2)
    ax.set_ylim(-gas.size_kpc/2, gas.size_kpc/2)
    ax.axis("off")

    _draw_gas(ax, gas)
    _draw_stars(ax, stars)
    _draw_sn(ax, sn_xy)

    fig.savefig(out_path, dpi=100)
    plt.close(fig)
