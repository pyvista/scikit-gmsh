# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "pyvista",
#   "scikit-gmsh",
# ]
# ///

r"""
Constrain edge size for Delaunay2D
-----------------------------------

Constrain edge size for Delaunay2D.

"""

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Polygon(n_sides=16, radius=16)
mesh = sg.Delaunay2D(shell=edge_source.points).mesh

p = pv.Plotter()
p.add_mesh(mesh, show_edges=True)
p.add_mesh(pv.PolyData(edge_source.points), render_points_as_spheres=True, color="red", point_size=10)
p.view_xy()
p.show()

# %%
# With option `constrain_edge_size=True`, the edge size is constrained.

mesh = sg.Delaunay2D(shell=edge_source.points, constrain_edge_size=True).mesh
mesh.plot(show_edges=True, color="white", cpos="xy")

# %%
# Works with holes too!

hole1 = pv.Polygon(n_sides=6, radius=4).translate([-4.0, -4.0, 0.0])
hole2 = pv.Polygon(n_sides=8, radius=2).translate([4.0, 4.0, 0.0])
mesh = sg.Delaunay2D(shell=edge_source.points, holes=[hole1.points, hole2.points], constrain_edge_size=True).mesh
mesh.plot(show_edges=True, color="white", cpos="xy")
