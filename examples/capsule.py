r"""
Capsule geometry example
-------------------------

Capsule geometry example.

"""

# sphinx_gallery_thumbnail_number = 1 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Capsule(resolution=9)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True)

# %%
# Create a 3D mesh from the edge source.

alg = sg.Delaunay3D(edge_source)
alg.mesh.shrink(0.9).plot(show_edges=True)

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.5
alg.mesh.plot(show_edges=True)
