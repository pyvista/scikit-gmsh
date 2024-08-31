r"""
Cylinder geometry example
-------------------------

Cylinder geometry example.

"""

from __future__ import annotations

import pyvista as pv

# import skgmsh as sg  # noqa: ERA001

edge_source = pv.Cylinder(resolution=16)
edge_source.plot(show_edges=True)
# edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)  # noqa: ERA001
# edge_source.plot(show_edges=True)  # noqa: ERA001
# alg = sg.Delaunay3D(edge_source)  # noqa: ERA001
# mesh = alg.mesh.shrink(0.9)  # noqa: ERA001
# mesh.plot(show_edges=True)  # noqa: ERA001
