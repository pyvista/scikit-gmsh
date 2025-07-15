# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "scikit-gmsh",
# ]
# ///

r"""
Quad geometry example
---------------------

Quad geometry example.

"""

from __future__ import annotations

import skgmsh as sg

alg = sg.Delaunay2D2([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
alg.mesh.plot(show_edges=True, color="w", cpos="xy")
