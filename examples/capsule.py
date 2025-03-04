r"""
Capsule geometry example
-------------------------

Capsule geometry example.

"""

# sphinx_gallery_thumbnail_number = 3 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Capsule(resolution=10)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white")

# %%
# Create a 3D mesh from the edge source.

alg = sg.Delaunay3D(edge_source)
alg.mesh.shrink(0.9).plot(show_edges=True, color="white")

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.25
alg.mesh.plot(show_edges=True, color="white")
