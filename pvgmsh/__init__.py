import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401


def delaunay_2d(edge_source, size=1e-2):
    """
    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).


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

    Define poly data using PyVista.

    >>> vertices = np.array([[0, 0, 0], [0.1, 0, 0], [0.1, 0.3, 0], [0, 0.3, 0]])
    >>> faces = np.hstack([[4, 0, 1, 2, 3]])
    >>> edge_source = pv.PolyData(vertices, faces)
    >>> edge_source
    PolyData (...)
      N Cells:    1
      N Points:   4
      N Strips:   0
      X Bounds:   0.000e+00, 1.000e-01
      Y Bounds:   0.000e+00, 3.000e-01
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0

    Generate mesh using gmsh.

    >>> mesh = pvgmsh.delaunay_2d(edge_source)
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
    for cell in edge_source.cell:
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
                if edge_source.number_of_cells == 1:
                    gmsh.clear()
                    gmsh.finalize()
                    return mesh
            gmsh.clear()
            gmsh.finalize()
            meshes.append(mesh)
    return meshes
