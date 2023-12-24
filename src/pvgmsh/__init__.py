import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401

FRONTAL_DELAUNAY_2D = 6


def frontal_delaunay_2d(edge_source, mesh_size=1e-2):
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


    mesh_size : float, optional
        Target mesh mesh_size close to the point.
        Defalut 1e-2.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 2D delaunay generation.

    Examples
    --------
    Use the ``edge_source`` parameter to create a constrained delaunay
    triangulation.

    >>> import pyvista as pv
    >>> import pvgmsh
    >>> squar = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> squar = squar.rotate_z(45, inplace=False)
    >>> squar
    PolyData (...)
      N Cells:    1
      N Points:   4
      N Strips:   0
      X Bounds:   -5.657e+00, 5.657e+00
      Y Bounds:   -5.657e+00, 5.657e+00
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0
    >>> squar.points
    pyvista_ndarray([[-5.656854,  5.656854,  0.      ],
                     [ 5.656854,  5.656854,  0.      ],
                     [ 5.656854, -5.656854,  0.      ],
                     [-5.656854, -5.656854,  0.      ]], dtype=float32)
    >>> squar.faces
    array([], dtype=int64)
    >>> squar.lines
    array([5, 0, 1, 2, 3, 0])

    >>> tess = pvgmsh.frontal_delaunay_2d(edge_source=squar, mesh_size=1.0)
    <BLANKLINE>

    >>> tess
    UnstructuredGrid (...)
      N Cells:    398
      N Points:   198
      X Bounds:   -5.657e+00, 5.657e+00
      Y Bounds:   -5.657e+00, 5.657e+00
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0

    >>> plotter = pv.Plotter(off_screen=True)
    >>> _ = plotter.add_mesh(tess, show_edges=True)
    >>> plotter.show(cpos="xy", screenshot="frontal_delaunay_2d_01.png")
    """
    gmsh.initialize()
    gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)

    for i, point in enumerate(edge_source.points):
        gmsh.model.geo.add_point(point[0], point[1], point[2], mesh_size, i + 1)

    lines = edge_source.lines
    for i in range(lines[0] - 1):
        gmsh.model.geo.add_line(lines[i + 1] + 1, lines[i + 2] + 1, i + 1)

    gmsh.model.geo.add_curve_loop(range(1, lines[0]), 1)
    gmsh.model.geo.add_plane_surface([1], 1)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(2)

    with tempfile.NamedTemporaryFile(
        mode="w+", encoding="utf-8", newline="\n", suffix=".msh"
    ) as fp:
        gmsh.write(fp.name)
        mesh = pv.read(fp.name)
        mesh.clear_data()

    gmsh.clear()
    gmsh.finalize()
    return mesh


def delaunay_3d():
    """The Delaunay 3D mesh algorithm.

    Examples
    --------
    >>> import gmsh
    >>> gmsh.initialize()
    >>> lc = 1e-2
    >>> _ = gmsh.model.geo.add_point(0, 0, 0, lc, 1)
    >>> _ = gmsh.model.geo.add_point(0.1, 0, 0, lc, 2)
    >>> _ = gmsh.model.geo.add_point(0.1, 0.3, 0, lc, 3)
    >>> _ = gmsh.model.geo.add_point(0, 0.3, 0, lc, 4)
    >>> _ = gmsh.model.geo.add_line(1, 2, 1)
    >>> _ = gmsh.model.geo.add_line(3, 2, 2)
    >>> _ = gmsh.model.geo.add_line(3, 4, 3)
    >>> _ = gmsh.model.geo.add_line(4, 1, 4)
    >>> _ = gmsh.model.geo.add_curve_loop([4, 1, -2, 3], 1)
    >>> _ = gmsh.model.geo.add_plane_surface([1], 1)

    We change the mesh size to generate a coarser mesh

    >>> lc = lc * 4
    >>> gmsh.model.geo.mesh.set_size([(0, 1), (0, 2), (0, 3), (0, 4)], lc)

    We define a new point

    >>> _ = gmsh.model.geo.add_point(0.02, 0.02, 0.0, lc, 5)

    We have to synchronize before embedding entites:

    >>> gmsh.model.geo.synchronize()

    One can force this point to be included ("embedded") in the 2D mesh, using the
    `embed()' function:

    >>> gmsh.model.mesh.embed(0, [5], 2, 1)

    In the same way, one can use `embed()' to force a curve to be embedded in the
    2D mesh:

    >>> _ = gmsh.model.geo.add_point(0.02, 0.12, 0.0, lc, 6)
    >>> _ = gmsh.model.geo.add_point(0.04, 0.18, 0.0, lc, 7)
    >>> _ = gmsh.model.geo.add_line(6, 7, 5)

    >>> gmsh.model.geo.synchronize()
    >>> gmsh.model.mesh.embed(1, [5], 2, 1)

    Points and curves can also be embedded in volumes

    >>> gmsh.model.geo.extrude([(2, 1)], 0, 0, 0.1)
    [(2, 27), (3, 1), (2, 14), (2, 18), (2, 22), (2, 26)]

    >>> p = gmsh.model.geo.add_point(0.07, 0.15, 0.025, lc)

    >>> gmsh.model.geo.synchronize()
    >>> gmsh.model.mesh.embed(0, [p], 3, 1)

    >>> gmsh.finalize()
    """
    pass
