r"""
Polygon with hole geometry example
----------------------------------

Polygon with hole geometry example.

"""

# sphinx_gallery_thumbnail_number = 2 # noqa:ERA001

from __future__ import annotations

import pyvista as pv
import shapely

import skgmsh as sg

# Set global theme to allow empty meshes
pv.global_theme.allow_empty_mesh = True

# Create shell and hole polygons
shell = shapely.Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
hole = shapely.Polygon([(2, 2), (2, 4), (4, 4), (4, 2)])
alg = sg.Delaunay2D(shell=shell, holes=[hole])

# %%
# Generate the mesh.

try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, cpos="xy", color="white", line_width=2)
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation failed: {e}")

# %%
# Change the cell size of the mesh.

alg.cell_size = 2.0
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, cpos="xy", color="white", line_width=2)
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation failed: {e}")

# %%
# Enable recombine.

alg.enable_recombine()
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, cpos="xy", color="white", line_width=2)
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"Mesh generation failed: {e}")
