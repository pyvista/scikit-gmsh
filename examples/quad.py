from __future__ import annotations

import gmsh
import pyvista as pv

gmsh.initialize()
gmsh.open("quad.geo")
gmsh.model.mesh.generate(2)
gmsh.write("quad.vtk")
gmsh.finalize()

mesh = pv.read("quad.vtk")
mesh.plot(show_edges=True, color="w", cpos="xy")
