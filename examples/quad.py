r"""
Quad geometry example
---------------------

Quad geometry example.

"""

from __future__ import annotations

from pathlib import Path
import subprocess

import pyvista as pv

with Path("quad.geo").open("w") as f:
    f.write("lc = 0.05;\n")
    f.write("Point(1) = {0, 0, 0, lc};\n")
    f.write("Point(2) = {1, 0, 0, lc};\n")
    f.write("Point(3) = {1, 1, 0, lc};\n")
    f.write("Point(4) = {0, 1, 0, lc};\n")
    f.write("Line(1) = {1, 2};\n")
    f.write("Line(2) = {2, 3};\n")
    f.write("Line(3) = {3, 4};\n")
    f.write("Line(4) = {4, 1};\n")
    f.write("Line Loop(1) = {1, 2, 3, 4};\n")
    f.write("Plane Surface(1) = {1};\n")

subprocess.run(["gmsh", "quad.geo", "-2", "-o", "quad.vtk"], check=False)  # noqa: S603, S607

mesh = pv.read("quad.vtk")
mesh.plot(show_edges=True, color="w", cpos="xy")
