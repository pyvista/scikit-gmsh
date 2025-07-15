# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "pyvista",
#   "scikit-gmsh",
# ]
# ///

r"""
Cylinder geometry example
-------------------------

Cylinder geometry example.

"""

# sphinx_gallery_thumbnail_number = 3 # noqa:ERA001

from __future__ import annotations

import pyvista as pv

import skgmsh as sg

edge_source = pv.Cylinder(resolution=16)
edge_source.merge(pv.PolyData(edge_source.points), merge_points=True, inplace=True)
edge_source.plot(show_edges=True, color="white", line_width=2)

# %%
# Generate the mesh.

alg = sg.Delaunay3D(edge_source)
mesh = alg.mesh
mesh.plot(show_edges=True)

# %%
# Output the information of the mesh.

print(mesh)

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.2
alg.mesh.plot(show_edges=True, color="white", line_width=2)
