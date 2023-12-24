"""PvGmsh package for 3D mesh generation."""

import gmsh
import pyvista as pv
import tempfile
from pvgmsh._version import __version__  # noqa: F401
import numpy as np

FRONTAL_DELAUNAY_2D = 6


def frontal_delaunay_2d(edge_source, target_size=None):
    """The Frontal-Delaunay 2D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).


    target_size : float, optional
        Target mesh size close to the points.
        Defalut max size of edge_source in each direction.

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
    >>> geometry = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> geometry = geometry.rotate_z(45, inplace=False)
    >>> geometry
    PolyData (...)
      N Cells:    1
      N Points:   4
      N Strips:   0
      X Bounds:   -5.657e+00, 5.657e+00
      Y Bounds:   -5.657e+00, 5.657e+00
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0
    >>> geometry.points
    pyvista_ndarray([[-5.656854,  5.656854,  0.      ],
                     [ 5.656854,  5.656854,  0.      ],
                     [ 5.656854, -5.656854,  0.      ],
                     [-5.656854, -5.656854,  0.      ]], dtype=float32)
    >>> geometry.faces
    array([], dtype=int64)
    >>> geometry.lines
    array([5, 0, 1, 2, 3, 0])

    >>> mesh = pvgmsh.frontal_delaunay_2d(geometry, target_size=1.0)
    <BLANKLINE>

    >>> mesh
    UnstructuredGrid (...)
      N Cells:    398
      N Points:   198
      X Bounds:   -5.657e+00, 5.657e+00
      Y Bounds:   -5.657e+00, 5.657e+00
      Z Bounds:   0.000e+00, 0.000e+00
      N Arrays:   0

    >>> plotter = pv.Plotter(off_screen=True)
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> _ = plotter.add_mesh(geometry, show_edges=True, line_width=4, color="blue")
    >>> _ = plotter.add_points(
    ...     geometry.points, style="points", point_size=20, color="blue"
    ... )
    >>> plotter.show(cpos="xy", screenshot="frontal_delaunay_2d_01.png")
    """
    gmsh.initialize()
    gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)

    for i, point in enumerate(edge_source.points):
        if target_size is None:
            gmsh.model.geo.add_point(
                point[0],
                point[1],
                point[2],
                np.max(
                    np.abs(geometry.bounds[1] - geometry.bounds[0]),
                    np.abs(geometry.bounds[3] - geometry.bounds[2]),
                    np.abs(geometry.bounds[5] - geometry.bounds[4]),
                ),
                i + 1,
            )
        else:
            gmsh.model.geo.add_point(point[0], point[1], point[2], target_size, i + 1)

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
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_point(X, X, X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_line(X, X, X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_curve_loop([X, X, X, X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_plane_surface([X], X)
    >>> _ = gmsh.model.geo.add_surface_loop([X], X)
    >>> _ = gmsh.model.geo.add_volume([X], X)
    >>> gmsh.model.geo.synchronize()
    >>> gmsh.model.mesh.generate(3)
    >>> with tempfile.NamedTemporaryFile(
    ...     mode="w+", encoding="utf-8", newline="\n", suffix=".msh"
    ... ) as fp:
    ...     gmsh.write(fp.name)
    ...     mesh = pv.read(fp.name)
    ...     mesh.clear_data()
    >>> gmsh.clear()
    >>> gmsh.finalize()
    >>> plotter = pv.Plotter(off_screen=True)
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> plotter.show(screenshot="delaunay_3d_01.png")
    """
    pass
