"""scikit-gmsh package for 3D mesh generation test."""

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Capsule(resolution=3)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True)
alg = sg.Delaunay3D(edge_source)
alg.mesh.shrink(0.9).plot(show_edges=True)
