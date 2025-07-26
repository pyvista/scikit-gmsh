# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "pyvista",
#   "scikit-gmsh",
# ]
# ///

r"""
Icosahedron geometry example
----------------------------

Icosahedron geometry example.

"""

# sphinx_gallery_thumbnail_number = 2 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Icosahedron()
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white")

# %%
# Generate the mesh.

delaunay_3d = sg.Delaunay3D(edge_source)
delaunay_3d.mesh.shrink(0.9).plot(show_edges=True, color="white")
