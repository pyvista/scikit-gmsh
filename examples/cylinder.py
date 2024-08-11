"""scikit-gmsh package for 3D mesh generation test."""

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Cylinder(resolution=16)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, line_width=2, color="aliceblue", lighting=False, edge_color="gray")
delaunay_3d = sg.Delaunay3D(edge_source)
mesh = delaunay_3d.mesh
mesh.shrink(0.9).plot(show_edges=True, line_width=1, color="aliceblue", lighting=False, edge_color="gray")
