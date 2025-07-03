r"""
Capsule geometry example
-------------------------

Capsule geometry example.

"""

# sphinx_gallery_thumbnail_number = 3 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

# Set global theme to allow empty meshes
pv.global_theme.allow_empty_mesh = True

edge_source = pv.Capsule(resolution=10)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white")

# %%
# Create a 3D mesh from the edge source.

alg = sg.Delaunay3D(edge_source)
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.shrink(0.9).plot(show_edges=True, color="white")
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"3D mesh generation failed: {e}")

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.25
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, color="white")
    else:
        print("Warning: Empty mesh with smaller cell size generated")
except (ValueError, RuntimeError) as e:
    print(f"3D mesh generation with smaller cell size failed: {e}")
