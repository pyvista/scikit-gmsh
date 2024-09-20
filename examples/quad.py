import gmsh

gmsh.initialize()
gmsh.open("quad.geo")
gmsh.model.mesh.generate(2)
gmsh.write("quad.vtk")
gmsh.finalize()

import pyvista as pv
mesh = pv.read("quad.vtk")
mesh.plot(show_edges=True, color="w", cpos="xy")
