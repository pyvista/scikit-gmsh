import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401


def delaunay_2d(poly_data, size=1e-2):
    """
    Parameters
    ----------
    poly_data : pv.PolyData
        Poly data to generate delaunay 2d mesh.

    size : float, optional
        Target mesh size close to the point.
        Defalut 1e-2.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 2D delaunay generation.

    Examples
    --------
    This example is inspired by Gmsh Python tutorial 1.
    See https://gmsh.info/doc/texinfo/gmsh.html#t1 .


    >>> import pvgmsh
    >>> import pyvista as pv
    >>> import numpy as np

    Define poly_data using PyVista.

    >>> vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0, 0.3, 0]])
    >>> faces = np.hstack([[4, 0, 1, 2, 3]])
    >>> poly_data = pv.PolyData(vertices, faces)
    >>> poly_data
    PolyData (...)
      N Cells:    1
      N Points:   4
      N Strips:   0
      X Bounds:   0.000e+00, 1.000e-01
      Y Bounds:   0.000e+00, 3.000e-01
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0

    Generate mesh using gmsh.

    >>> mesh = pvgmsh.delaunay_2d(poly_data)
    <BLANKLINE>
    >>> mesh
    UnstructuredGrid (...)
      N Cells:    816
      N Points:   407
      X Bounds:   0.000e+00, 1.000e-01
      Y Bounds:   0.000e+00, 3.000e-01
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   2
    """
    meshes = []
    for cell in poly_data.cell:
        if cell.type == pv.CellType.QUAD:
            gmsh.initialize()
            for i, point in enumerate(cell.points):
                gmsh.model.geo.addPoint(point[0], point[1], point[2], size, i + 1)
            gmsh.model.geo.addLine(1, 2, 1)
            gmsh.model.geo.addLine(2, 3, 2)
            gmsh.model.geo.addLine(3, 4, 3)
            gmsh.model.geo.addLine(4, 1, 4)
            gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
            gmsh.model.geo.addPlaneSurface([1], 1)
            gmsh.model.geo.synchronize()
            gmsh.model.mesh.generate(2)
            with tempfile.NamedTemporaryFile(
                mode="w+", encoding="utf-8", newline="\n", suffix=".msh"
            ) as fp:
                gmsh.write(fp.name)
                mesh = pv.read(fp.name)
                if poly_data.number_of_cells == 1:
                    gmsh.clear()
                    gmsh.finalize()
                    return mesh
            gmsh.clear()
            gmsh.finalize()
            meshes.append(mesh)
    return meshes
