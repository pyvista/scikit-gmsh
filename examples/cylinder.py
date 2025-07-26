r"""
Cylinder geometry example
-------------------------

Cylinder geometry example.

"""

# sphinx_gallery_thumbnail_number = 3 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

# Set global theme to allow empty meshes
pv.global_theme.allow_empty_mesh = True

edge_source = pv.Cylinder(resolution=16)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white", line_width=2)

# %%
# Generate the mesh.

alg = sg.Delaunay3D(edge_source)
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True)
        print(mesh)
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"3D mesh generation failed: {e}")

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.2
try:
    mesh = alg.mesh
    if mesh.n_points > 0:
        mesh.plot(show_edges=True, color="white", line_width=2)
    else:
        print("Warning: Empty mesh with smaller cell size generated")
except (ValueError, RuntimeError) as e:
    print(f"3D mesh generation with smaller cell size failed: {e}")
