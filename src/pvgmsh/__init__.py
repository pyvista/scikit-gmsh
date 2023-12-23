import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401


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

    >>> tess = frontal_delaunay_2d(edge_source=squar, mesh_size=1.0)
    <BLANKLINE>

    >>> tess.clear_data()
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
    >>> plotter.show(cpos="xy", screenshot="delaunay_2d_01.png")
    """
    gmsh.initialize()
    gmsh.option.set_number("Mesh.Algorithm", 6)
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
    gmsh.clear()
    gmsh.finalize()
    return mesh
