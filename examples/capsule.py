r"""
Capsule geometry example
-------------------------

Capsule geometry example.

"""

# sphinx_gallery_thumbnail_number = 1 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Capsule(resolution=3)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True)
alg = sg.Delaunay3D(edge_source)
alg.mesh.shrink(0.9).plot(show_edges=True)
