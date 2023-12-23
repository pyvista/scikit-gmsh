import gmsh
import pyvista as pv
from pvgmsh._version import __version__  # noqa: F401


def generate_mesh(surf, lc=1e-2):
    gmsh.initialize()
    for i, point in enumerate(surf.points):
        gmsh.model.geo.addPoint(point[0], point[1], point[2], lc, i + 1)
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(3, 2, 2)
    gmsh.model.geo.addLine(3, 4, 3)
    gmsh.model.geo.addLine(4, 1, 4)
    gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write("t1.msh")
    gmsh.clear()
    gmsh.finalize()
    mesh = pv.read("t1.msh")
    return mesh
