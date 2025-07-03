r"""
Icosahedron geometry example
----------------------------

Icosahedron geometry example.

"""

# sphinx_gallery_thumbnail_number = 2 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

# Set global theme to allow empty meshes
pv.global_theme.allow_empty_mesh = True

edge_source = pv.Icosahedron()
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white")

# %%
# Generate the mesh.

delaunay_3d = sg.Delaunay3D(edge_source)
try:
    mesh = delaunay_3d.mesh
    if mesh.n_points > 0:
        mesh.shrink(0.9).plot(show_edges=True, color="white")
    else:
        print("Warning: Empty mesh generated")
except (ValueError, RuntimeError) as e:
    print(f"3D mesh generation failed: {e}")
