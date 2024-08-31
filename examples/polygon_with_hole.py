r"""
Polygon with hole geometry example
----------------------------------

Polygon with hole geometry example.

"""

from __future__ import annotations

# import skgmsh as sg  # noqa: ERA001
import pyvista as pv

pv.Cube().plot(color="w", show_edges=True)

# shell = [(0, 0, 0), (0, 10, 0), (10, 10, 0), (10, 0, 0), (0, 0, 0)]  # noqa: ERA001
# holes = [[(2, 2, 0), (2, 4, 0), (4, 4, 0), (4, 2, 0), (2, 2, 0)]]  # noqa: ERA001
#
# alg = sg.Delaunay2D(shell=shell, holes=holes)  # noqa: ERA001
# mesh = alg.mesh  # noqa: ERA001
# mesh.plot(show_edges=True, color="white", cpos="xy")  # noqa: ERA001
