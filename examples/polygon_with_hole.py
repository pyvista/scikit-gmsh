r"""
Polygon with hole geometry example
----------------------------------

Polygon with hole geometry example.

"""

from __future__ import annotations

import skgmsh as sg

shell = [(0, 0, 0), (0, 10, 0), (10, 10, 0), (10, 0, 0), (0, 0, 0)]
holes = [[(2, 2, 0), (2, 4, 0), (4, 4, 0), (4, 2, 0), (2, 2, 0)]]

alg = sg.Delaunay2D(shell=shell, holes=holes)
alg.mesh.plot(show_edges=True, color="white", cpos="xy")
