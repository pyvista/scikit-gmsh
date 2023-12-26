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
    >>> import pvgmsh as pg

    >>> geometry = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> geometry = geometry.rotate_z(45, inplace=False)

    >>> mesh = pg.frontal_delaunay_2d(geometry, target_size=1.0)
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

    if target_size is None:
        target_size = np.max(
            np.abs(geometry.bounds[1] - geometry.bounds[0]),
            np.abs(geometry.bounds[3] - geometry.bounds[2]),
            np.abs(geometry.bounds[5] - geometry.bounds[4]),
        )

    for i, point in enumerate(edge_source.points):
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
    >>> _ = gmsh.model.geo.add_point(0, 0, 0, 1.0, 1)
    >>> _ = gmsh.model.geo.add_point(1, 0, 0, 1.0, 2)
    >>> _ = gmsh.model.geo.add_point(1, 1, 0, 1.0, 3)
    >>> _ = gmsh.model.geo.add_point(0, 1, 0, 1.0, 4)
    >>> _ = gmsh.model.geo.add_point(0, 0, 1, 1.0, 5)
    >>> _ = gmsh.model.geo.add_point(1, 0, 1, 1.0, 6)
    >>> _ = gmsh.model.geo.add_point(1, 1, 1, 1.0, 7)
    >>> _ = gmsh.model.geo.add_point(0, 1, 1, 1.0, 8)
    >>> _ = gmsh.model.geo.add_point(1, 1, 1, 1.0, 9)
    >>> _ = gmsh.model.geo.add_line(1, 2, 1)
    >>> _ = gmsh.model.geo.add_line(2, 3, 2)
    >>> _ = gmsh.model.geo.add_line(3, 4, 3)
    >>> _ = gmsh.model.geo.add_line(4, 1, 4)
    >>> _ = gmsh.model.geo.add_line(1, 5, 5)
    >>> _ = gmsh.model.geo.add_line(2, 6, 6)
    >>> _ = gmsh.model.geo.add_line(3, 7, 7)
    >>> _ = gmsh.model.geo.add_line(4, 8, 8)
    >>> _ = gmsh.model.geo.add_line(8, 7, 9)
    >>> _ = gmsh.model.geo.add_line(7, 6, 10)
    >>> _ = gmsh.model.geo.add_line(6, 5, 11)
    >>> _ = gmsh.model.geo.add_line(5, 8, 12)
    >>> _ = gmsh.model.geo.add_curve_loop([1, 2, 3, 4], 1)
    >>> _ = gmsh.model.geo.add_curve_loop([3, 8, 9, -7], 3)
    >>> _ = gmsh.model.geo.add_curve_loop([4, 5, 12, -8], 5)
    >>> _ = gmsh.model.geo.add_curve_loop([7, 10, -6, 2], 7)
    >>> _ = gmsh.model.geo.add_curve_loop([1, 6, 11, -5], 9)
    >>> _ = gmsh.model.geo.add_curve_loop([9, 10, 11, 12], 11)
    >>> _ = gmsh.model.geo.add_plane_surface([1], 1)
    >>> _ = gmsh.model.geo.add_plane_surface([3], 2)
    >>> _ = gmsh.model.geo.add_plane_surface([5], 3)
    >>> _ = gmsh.model.geo.add_plane_surface([7], 4)
    >>> _ = gmsh.model.geo.add_plane_surface([9], 5)
    >>> _ = gmsh.model.geo.add_plane_surface([11], 6)
    >>> _ = gmsh.model.geo.add_surface_loop([6, 2, 4, 5, 1, 3], 1)
    >>> _ = gmsh.model.geo.add_volume([1], 1)
    >>> gmsh.model.geo.synchronize()
    >>> gmsh.model.mesh.generate(3)
    >>> element_types, element_tags, node_tags = gmsh.model.mesh.getElements()
    >>> element_types
    array([ 1,  2,  4, 15], dtype=int32)
    >>> element_tags

    >>> node_tags

    >>> fp = tempfile.NamedTemporaryFile(mode="w+", suffix=".msh")
    >>> gmsh.write(fp.name)
    >>> mesh = pv.read(fp.name)
    <BLANKLINE>
    >>> fp.close()
    >>> mesh.clear_data()
    >>> mesh
    UnstructuredGrid (...)
      N Cells:    69
      N Points:   15
      X Bounds:   0.000e+00, 1.000e+00
      Y Bounds:   0.000e+00, 1.000e+00
      Z Bounds:   0.000e+00, 1.000e+00
      N Arrays:   0

    >>> gmsh.clear()
    >>> gmsh.finalize()

    >>> plotter = pv.Plotter(off_screen=True)
    >>> _ = plotter.add_mesh(mesh, show_edges=True, line_width=4, color="white")
    >>> plotter.show(screenshot="delaunay_3d_01.png")
    """
    pass
