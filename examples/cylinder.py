r"""
Cylinder geometry example
-------------------------

Cylinder geometry example.

"""

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Cylinder(resolution=16)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True)
delaunay_3d = sg.Delaunay3D(edge_source)

# %%
# Plot generated mesh.

delaunay_3d.mesh.shrink(0.9).plot(show_edges=True)
