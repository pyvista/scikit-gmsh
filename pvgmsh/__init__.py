import gmsh
import pyvista as pv


def generate_mesh(surf):
    gmsh.initialize()
    lc = 1e-2
    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(0.1, 0, 0, lc, 2)
    gmsh.model.geo.addPoint(0.1, 0.3, 0, lc, 3)
    p4 = gmsh.model.geo.addPoint(0, 0.3, 0, lc)
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(3, 2, 2)
    gmsh.model.geo.addLine(3, p4, 3)
    gmsh.model.geo.addLine(4, 1, p4)
    gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write("t1.msh")
    gmsh.clear()
    gmsh.finalize()
    mesh = pv.read("t1.msh")
    return mesh
