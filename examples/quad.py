r"""
Quad geometry example
---------------------

Quad geometry example.

"""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Optional

import pyvista as pv
import shapely


class Delaunay2D:
    """Delaunay2D class."""

    def __init__(self, shell: shapely.Polygon, holes: Optional[list[shapely.Polygon]] = None) -> None:
        """Create a Delaunay2D object."""
        self.shell = shapely.Polygon(shell)
        self.holes = [shapely.Polygon(hole) for hole in holes] if holes else []
        self._generate_mesh()

    def _generate_mesh(self) -> None:
        cell_size = 0.05
        with Path("quad.geo").open("w") as f:
            for linearring in [self.shell.exterior, *list(self.shell.interiors), *self.holes]:
                coords = linearring.coords[:-1].copy()
                for i, coord in enumerate(coords):
                    x = coord[0]
                    y = coord[1]
                    z = coord[2]
                    f.write("Point(" + str(i + 1) + ") = {" + str(x) + "," + str(y) + "," + str(z) + "," + str(cell_size) + "};\n")
                for i, _ in enumerate(coords[:-1]):
                    f.write("Line(" + str(i + 1) + ") = {" + str(i + 1) + ", " + str(i + 2) + "};\n")
                f.write("Line(" + str(len(coords)) + ") = {" + str(len(coords)) + ", 1};\n")
                f.write("Line Loop(1) = {")
                for i in range(len(coords) - 1):
                    f.write(str(i + 1) + ", ")
                f.write(str(len(coords)) + "};\n")
                f.write("Plane Surface(1) = {1};\n")

        subprocess.run(["gmsh", "quad.geo", "-2", "-o", "quad.vtk"], check=False)  # noqa: S603, S607

        self.mesh = pv.read("quad.vtk")


alg = Delaunay2D([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
alg.mesh.plot(show_edges=True, color="w", cpos="xy")
