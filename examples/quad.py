r"""
Quad geometry example
---------------------

Quad geometry example.

"""

from __future__ import annotations

import pyvista as pv
import shapely

import skgmsh as sg

# Set global theme to allow empty meshes for demonstration
pv.global_theme.allow_empty_mesh = True

# Create a simple quad polygon
quad = shapely.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
alg = sg.Delaunay2D(shell=quad)

try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, color="w", cpos="xy")
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation failed: {e}")
