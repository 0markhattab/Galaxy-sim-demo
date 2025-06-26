

> Note
> This README accompanies the “Galaxy Simulation Demo”. It is intended for learners who know basic Python and want a qualitative feel for disk‑galaxy evolution without installing heavyweight N‑body / SPH codes.

---

## 1  Motivation & learning goals

- Visual intuition – observe how stellar rotation, gas clumping, H II regions, and super‑nova feedback interact over tens of Myr. 
 
- Modularity – illustrate how a Python project can be split into clear, testable modules (generation, simulation, visualisation).  

- Rapid iteration – every design choice (IMF, rotation curve, colour‑map) is a single constant you can tweak and immediately re‑render.

> **Pedagogy over precision: all physics is highly simplified so the whole run finishes in < 1 min on a laptop.

---

## 2  Physical ingredients & assumptions

| Component         | Representation                 | Key assumptions                                                                                     |
| ----------------- | ------------------------------ | --------------------------------------------------------------------------------------------------- |
| Stars         | ∼40 k tracer particles         | Thin exponential disk, flat rotation at 220 km s⁻¹, Kroupa‑like IMF (0.5–40 M☉).                    |
| Cold/Warm gas | 2‑D surface‑density grid       | Exponential profile plus fractal noise ⇒ clumps; rigid rotation (no self‑gravity).             |
| H II bubbles  | Red, semi‑transparent overlays | Procedural shells centred on random OB associations; temperature 10 000–30 000 K.                   |
| Super‑novae  | Yellow twinkles                | Massive stars (> 8 M☉) explode exactly at age = 10 Myr; inject visual flash + random velocity kick. |


---

## 3  Numerical scheme

- *Integrator – first‑order Euler (good enough for 50 Myr demo). Numba JIT boosts to ≈ 5 × 10⁶ star‑steps · s⁻¹.  
- *Gas advection – cheat by rigidly rotating the density map with `scipy.ndimage.rotate` (order = 1).  
- *Time step (`--dt_myr`) – default 0.025 Myr → 2 000 frames for the full 50 Myr run (playback at 24 fps ≈ 5× real‑time).

---



## Porting to JavaScript / Three.js

1. Export initial conditions from `generation.py` (e.g., FlatBuffers, JSON, or binary).  
2. Load data into GPU buffers; update positions in a WebGL2 transform‑feedback shader or CPU fallback (`d3-force`).  
3. Render gas as a screen‑space billboard textured with the rotating density map; blend using custom GLSL.  
4. Add GUI sliders (dat.GUI or Tweakpane) for star count, rotation speed, SN rate, etc.



