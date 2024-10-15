r"""
Quad geometry example
---------------------

Quad geometry example.

"""

from __future__ import annotations

from pathlib import Path
import subprocess

import pyvista as pv
import shapely

shell = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)]
edge_source = shapely.Polygon(shell)

cell_size = 0.05

with Path("quad.geo").open("w") as f:
    for linearring in [edge_source.exterior, *list(edge_source.interiors)]:
        coords = linearring.coords[:-1].copy()
        for i, coord in enumerate(coords):
            x = coord[0]
            y = coord[1]
            z = coord[2]
            f.write("Point(" + str(i + 1) + ") = {" + str(x) + "," + str(y) + "," + str(z) + "," + str(cell_size) + "};\n")
    f.write("Line(1) = {1, 2};\n")
    f.write("Line(2) = {2, 3};\n")
    f.write("Line(3) = {3, 4};\n")
    f.write("Line(4) = {4, 1};\n")
    f.write("Line Loop(1) = {1, 2, 3, 4};\n")
    f.write("Plane Surface(1) = {1};\n")

subprocess.run(["gmsh", "quad.geo", "-2", "-o", "quad.vtk"], check=False)  # noqa: S603, S607

mesh = pv.read("quad.vtk")
mesh.plot(show_edges=True, color="w", cpos="xy")
