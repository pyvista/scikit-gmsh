"""scikit-gmsh package for polygon with hole mesh generation test."""

from __future__ import annotations

from shapely import Polygon

import skgmsh as sg

polygon_with_hole = Polygon(
    [(0, 0, 0), (0, 10, 0), (10, 10, 0), (10, 0, 0), (0, 0, 0)], holes=[[(2, 2, 0), (2, 4, 0), (4, 4, 0), (4, 2, 0), (2, 2, 0)]]
)

alg = sg.Delaunay2D(polygon_with_hole)
alg.mesh.plot(show_edges=True, color="white", cpos="xy")

# %%
# Change the cell size of the mesh.

alg.cell_size = 0.5
alg.mesh.plot(show_edges=True, color="white", cpos="xy")
