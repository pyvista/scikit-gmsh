"""scikit-gmsh package for 3D mesh generation."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import gmsh
from pygmsh.helpers import extract_to_meshio
import pyvista as pv
import scooby

if TYPE_CHECKING:
    from collections.abc import Sequence

    import numpy as np

INITIAL_MESH_ONLY_2D = 3
FRONTAL_DELAUNAY_2D = 6
DELAUNAY_3D = 1

SILENT = 0

now = datetime.datetime.now(tz=datetime.timezone.utc)

# major, minor, patch
version_info = 0, 2, "dev0"

# Nice string for the version
__version__ = ".".join(map(str, version_info))


class Report(scooby.Report):  # type: ignore[misc]
    """
    Generate an environment package and hardware report.

    Parameters
    ----------
    ncol : int, default: 3
        Number of package-columns in html table; only has effect if
        ``mode='HTML'`` or ``mode='html'``.

    text_width : int, default: 80
        The text width for non-HTML display modes.

    """

    def __init__(self: Report, ncol: int = 3, text_width: int = 80) -> None:  # numpydoc ignore=PR01
        """Generate a :class:`scooby.Report` instance."""
        # mandatory packages
        core: list[str] = [
            "matplotlib",
            "numpy",
            "pooch",
            "pyvista",
            "scooby",
            "vtk",
            "gmsh",
            "meshio",
            "pygmsh",
            "pyvista",
        ]

        # optional packages
        optional: list[str] = [
            "imageio",
            "pyvistaqt",
            "PyQt5",
            "IPython",
            "colorcet",
            "cmocean",
            "ipywidgets",
            "scipy",
            "tqdm",
            "jupyterlab",
            "pytest_pyvista",
            "trame",
            "trame_client",
            "trame_server",
            "trame_vtk",
            "trame_vuetify",
            "jupyter_server_proxy",
            "nest_asyncio",
        ]

        extra_meta = [
            ("GPU Details", "None"),
        ]

        super().__init__(
            core=core,
            optional=optional,
            ncol=ncol,
            text_width=text_width,
            extra_meta=extra_meta,
        )


def delaunay_3d(
    edge_source: pv.PolyData,
    target_sizes: float | Sequence[float] | None = None,
) -> pv.UnstructuredGrid | None:
    """
    Delaunay 3D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    target_sizes : float | Sequence[float]
        Target mesh size close to the points.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 3D delaunay generation.

    Notes
    -----
    .. versionadded:: 0.2.0

    """
    points = edge_source.points
    faces = edge_source.regular_faces

    gmsh.initialize()
    gmsh.option.set_number("Mesh.Algorithm3D", DELAUNAY_3D)
    gmsh.option.set_number("General.Verbosity", SILENT)

    if isinstance(target_sizes, float):
        target_sizes = [target_sizes] * edge_source.number_of_points

    for i, (point, target_size) in enumerate(zip(points, target_sizes)):
        id_ = i + 1
        gmsh.model.geo.add_point(point[0], point[1], point[2], target_size, id_)

    surface_loop = []
    for i, face in enumerate(faces):
        gmsh.model.geo.add_line(face[0] + 1, face[1] + 1, i * 4 + 0)
        gmsh.model.geo.add_line(face[1] + 1, face[2] + 1, i * 4 + 1)
        gmsh.model.geo.add_line(face[2] + 1, face[3] + 1, i * 4 + 2)
        gmsh.model.geo.add_line(face[3] + 1, face[0] + 1, i * 4 + 3)
        gmsh.model.geo.add_curve_loop([i * 4 + 0, i * 4 + 1, i * 4 + 2, i * 4 + 3], i + 1)
        gmsh.model.geo.add_plane_surface([i + 1], i + 1)
        gmsh.model.geo.remove_all_duplicates()
        gmsh.model.geo.synchronize()
        surface_loop.append(i + 1)

    gmsh.model.geo.add_surface_loop(surface_loop, 1)
    gmsh.model.geo.add_volume([1], 1)

    gmsh.model.geo.synchronize()
    gmsh.model.mesh.generate(3)

    mesh = pv.wrap(extract_to_meshio())
    gmsh.clear()
    gmsh.finalize()

    ind = []
    for i, cell in enumerate(mesh.cell):
        if cell.type != pv.CellType.TETRA:
            ind.append(i)
    mesh = mesh.remove_cells(ind)
    mesh.clear_data()

    return mesh


def frontal_delaunay_2d(
    edge_source: pv.PolyData,
    target_sizes: float | Sequence[float] | None = None,
    recombine: bool = False,  # noqa: FBT001, FBT002
) -> pv.UnstructuredGrid | None:
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

    target_sizes : float
        Target mesh size close to the points.
        Default max size of edge_source in each direction.

    recombine : bool
        Recombine the generated mesh into quadrangles.

    Returns
    -------
    pyvista.UnstructuredGrid
        Mesh from the 2D delaunay generation.

    Notes
    -----
    .. versionadded:: 0.2.0

    """
    points = edge_source.points
    lines = edge_source.lines

    gmsh.initialize()
    if target_sizes is None:
        gmsh.option.set_number("Mesh.Algorithm", INITIAL_MESH_ONLY_2D)
        gmsh.option.set_number("Mesh.MeshSizeExtendFromBoundary", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromPoints", 0)
        gmsh.option.set_number("Mesh.MeshSizeFromCurvature", 0)
    else:
        gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)
    gmsh.option.set_number("General.Verbosity", SILENT)

    if target_sizes is None:
        target_sizes = 0.0

    if isinstance(target_sizes, float):
        target_sizes = [target_sizes] * edge_source.number_of_points

    embedded_points = []
    for target_size, point in zip(target_sizes, points):
        embedded_points.append(gmsh.model.geo.add_point(point[0], point[1], point[2], target_size))

    for i in range(lines[0] - 1):
        id_ = i + 1
        gmsh.model.geo.add_line(lines[i + 1] + 1, lines[i + 2] + 1, id_)

    gmsh.model.geo.add_curve_loop(range(1, lines[0]), 1)
    gmsh.model.geo.add_plane_surface([1], 1)
    gmsh.model.geo.synchronize()

    gmsh.model.mesh.embed(0, embedded_points, 2, 1)

    if recombine:
        gmsh.model.mesh.set_recombine(2, 1)

    gmsh.model.mesh.generate(2)
    mesh = pv.from_meshio(extract_to_meshio())
    gmsh.clear()
    gmsh.finalize()

    ind = []
    for index, cell in enumerate(mesh.cell):
        if cell.type in [pv.CellType.VERTEX, pv.CellType.LINE]:
            ind.append(index)

    return mesh.remove_cells(ind)


class Delaunay2D:
    """
    Delaunay 2D mesh algorithm.

    Parameters
    ----------
    edge_source : pyvista.PolyData
        Specify the source object used to specify constrained
        edges and loops. If set, and lines/polygons are defined, a
        constrained triangulation is created. The lines/polygons
        are assumed to reference points in the input point set
        (i.e. point ids are identical in the input and
        source).

    Notes
    -----
    .. versionadded:: 0.2.0

    """

    def __init__(
        self: Delaunay2D,
        edge_source: pv.PolyData,
    ) -> None:
        """Initialize the Delaunay2D class."""
        self._edge_source = edge_source
        self._mesh = frontal_delaunay_2d(edge_source)

    @property
    def edge_source(self: Delaunay2D) -> pv.PolyData:
        """Get the edge source."""
        return self._edge_source

    @property
    def mesh(self: Delaunay2D) -> pv.UnstructuredGrid:
        """Get the mesh."""
        return self._mesh


class FrontalDelaunay2D:
    """
    Frontal Delaunay 2D mesh algorithm.

    Parameters
    ----------
    points : np.ndarray
        Coordinates of the points to triangulate.

    """

    # TODO @tkoyama010: Need to consider how to handle gmsh with two or more instances. # noqa: FIX002, TD003

    def __init__(self: FrontalDelaunay2D, points: np.ndarray) -> None:  # noqa: ARG002
        """Initialize the FrontalDelaunay2D class."""
        gmsh.initialize()
        gmsh.option.set_number("Mesh.Algorithm", FRONTAL_DELAUNAY_2D)
        gmsh.option.set_number("General.Verbosity", SILENT)

    def __del__(self: FrontalDelaunay2D) -> None:
        """Finalize the FrontalDelaunay2D class."""
        gmsh.clear()
        gmsh.finalize()

    def enable_recombine(self: FrontalDelaunay2D) -> None:
        """Enable recombine the generated mesh into quadrangles."""
        # TODO @tkoyama010: Define ID of surface clearly. # noqa: FIX002, TD003
        gmsh.model.mesh.setRecombine(2, 1)
