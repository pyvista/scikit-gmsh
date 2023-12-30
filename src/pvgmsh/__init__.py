"""PvGmsh package for 3D mesh generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyvista as pv

import gmsh
import numpy as np
from pygmsh.helpers import extract_to_meshio
from pyvista.core.utilities import fileio

from pvgmsh._version import __version__  # noqa: F401

FRONTAL_DELAUNAY_2D = 6


def frontal_delaunay_2d(
    edge_source: pv.PolyData,
    target_size: float | None,
) -> pv.UnstructuredGrid:
    """
    Frontal-Delaunay 2D mesh algorithm.

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
    >>> import pvgmsh as pm

    >>> edge_source = pv.Polygon(n_sides=4, radius=8, fill=False)
    >>> edge_source = edge_source.rotate_z(45, inplace=False)
    >>> mesh = pm.frontal_delaunay_2d(edge_source, target_size=1.0)

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
    >>> _ = plotter.add_mesh(edge_source, show_edges=True, line_width=4, color="blue")
    >>> _ = plotter.add_points(edge_source.points, style="points", point_size=20, color="blue")
    >>> plotter.show(cpos="xy", screenshot="frontal_delaunay_2d_01.png")
    """
    gmsh.initialize()
    gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)

    if target_size is None:
        target_size = np.max(
            np.abs(edge_source.bounds[1] - edge_source.bounds[0]),
            np.abs(edge_source.bounds[3] - edge_source.bounds[2]),
            np.abs(edge_source.bounds[5] - edge_source.bounds[4]),
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
    mesh = fileio.from_meshio(extract_to_meshio())
    gmsh.clear()
    gmsh.finalize()
    return mesh
