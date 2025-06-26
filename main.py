from __future__ import annotations
import argparse, os
from pathlib import Path
import numpy as np
from tqdm import trange

from modules.generation import generate_initial_conditions
from modules.simulation import step
from modules.visualization import render


def parse_args():
    p = argparse.ArgumentParser(description="Educational galaxy simulation demo")
    p.add_argument("--frames", type=int, default=200)
    p.add_argument("--dt_myr", type=float, default=0.025)
    p.add_argument("--out", type=str, default="output/frames")
    p.add_argument("--size", type=int, default=600, help="image size in px")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    Path(args.out).mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    stars, gas = generate_initial_conditions(seed=args.seed)

    for i in trange(args.frames, desc="Rendering"):
        sn_xy = step(stars, gas, args.dt_myr, rng)
        render(i, stars, gas, sn_xy, f"{args.out}/frame_{i:04d}.png", size=args.size)


if __name__ == "__main__":
    main()
