import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401


def generate_mesh(surf, lc=1e-2, dimension=2):
    meshes = []
    for cell in surf.cell:
        if cell.type == pv.CellType.QUAD:
            gmsh.initialize()
            for i, point in enumerate(cell.points):
                gmsh.model.geo.addPoint(point[0], point[1], point[2], lc, i + 1)
            gmsh.model.geo.addLine(1, 2, 1)
            gmsh.model.geo.addLine(2, 3, 2)
            gmsh.model.geo.addLine(3, 4, 3)
            gmsh.model.geo.addLine(4, 1, 4)
            gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
            gmsh.model.geo.addPlaneSurface([1], 1)
            gmsh.model.geo.synchronize()
            gmsh.model.mesh.generate(dimension)
            with tempfile.NamedTemporaryFile(
                mode="w+", encoding="utf-8", newline="\n", suffix=".msh"
            ) as fp:
                gmsh.write(fp.name)
                mesh = pv.read(fp.name)
                if surf.number_of_cells == 1:
                    gmsh.clear()
                    gmsh.finalize()
                    return mesh
            gmsh.clear()
            gmsh.finalize()
            meshes.append(mesh)
    return meshes
