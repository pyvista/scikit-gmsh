"""scikit-gmsh package for 3D mesh generation test."""

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Cylinder(resolution=16)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True)
alg = sg.Delaunay3D(edge_source)
alg.mesh.shrink(0.9).plot(show_edges=True)

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.5
alg.mesh.plot(show_edges=True, color="white", cpos="xy")
